![](graphics/microsoftlogo.png)

# Workshop: PostgreSQL for the SQL Server Database Professional

#### <i>A SQL Server to PostgreSQL Skilling</i>


<p style="border-bottom: 1px solid lightgrey;"></p>

<img style="float: left; margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/textbubble.png"> <h2>Module 06 – Advanced Features and Migration</h2>

*Estimated Time: 60 minutes (≈20 minutes lecture, ≈40 minutes hands-on)*

In this final module you will explore the features that make PostgreSQL stand apart — not just as a SQL Server replacement, but as a platform with capabilities that go beyond SQL Server's defaults. You will also review the tools and strategies for migrating existing SQL Server workloads to PostgreSQL.

<p style="border-bottom: 1px solid lightgrey;"></p>

<h2><img style="float: left; margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/pencil2.png">6.1 – JSONB: PostgreSQL's Native Document Storage</h2>

SQL Server stores JSON as `NVARCHAR(MAX)` and provides a set of functions (`JSON_VALUE`, `JSON_QUERY`, `OPENJSON`) to parse it at query time. PostgreSQL has two native JSON types:

- **`JSON`** — Stores the input text exactly (including whitespace and duplicate keys). Parsing happens at query time.
- **`JSONB`** — Stores JSON in a decomposed binary format. Parsed once on insert; subsequent queries are faster. Supports indexing. This is the recommended type for nearly all use cases.

**JSONB vs. SQL Server JSON:**

| Operation | SQL Server | PostgreSQL JSONB |
|---|---|---|
| Store JSON | `NVARCHAR(MAX)` | `JSONB` column |
| Extract a value | `JSON_VALUE(col, '$.key')` | `col->>'key'` or `col #>> '{key}'` |
| Extract an object | `JSON_QUERY(col, '$.obj')` | `col->'obj'` or `col #> '{obj}'` |
| Check key exists | `ISJSON(col) > 0 AND JSON_VALUE(col,'$.k') IS NOT NULL` | `col ? 'key'` |
| Containment | (no equivalent) | `col @> '{"key":"value"}'::jsonb` |
| Array elements | `OPENJSON(col)` | `jsonb_array_elements(col)` |
| Index on JSON field | Not possible on NVARCHAR directly | `CREATE INDEX ON t ((col->>'key'))` or GIN index |

**JSONB operators:**

```sql
-- -> returns JSONB (objects/arrays):
SELECT '{"name":"Alice","age":30}'::jsonb -> 'name';          -- Returns "Alice" (JSONB)

-- ->> returns TEXT:
SELECT '{"name":"Alice","age":30}'::jsonb ->> 'name';         -- Returns Alice (TEXT)

-- #> for nested path (returns JSONB):
SELECT '{"address":{"city":"Seattle"}}'::jsonb #> '{address,city}';

-- #>> for nested path (returns TEXT):
SELECT '{"address":{"city":"Seattle"}}'::jsonb #>> '{address,city}';

-- ? key exists:
SELECT '{"name":"Alice"}'::jsonb ? 'name';   -- TRUE

-- @> containment (does the left contain the right?):
SELECT '{"name":"Alice","active":true}'::jsonb @> '{"active":true}'::jsonb;  -- TRUE

-- jsonb_set: update a value inside JSONB (like JSON_MODIFY in SQL Server):
SELECT jsonb_set('{"name":"Alice","age":30}'::jsonb, '{age}', '31');
```

**Working with JSONB columns:**

```sql
-- Add a JSONB column to the authors table:
ALTER TABLE authors ADD COLUMN profile JSONB;

-- Update with JSON data (target a single author by primary key):
UPDATE authors
SET profile = '{
    "contact": {"phone": "555-1234", "email": "abennet@example.com"},
    "preferences": {"newsletter": true, "theme": "dark"},
    "sales": [{"year": 2023, "count": 5}, {"year": 2024, "count": 12}]
}'
WHERE au_id = '409-56-7008';

-- Query JSON fields:
SELECT au_id,
       au_fname,
       profile->>'contact'                             AS contact_json,
       profile #>> '{contact,email}'                  AS email,
       profile #>> '{preferences,theme}'              AS theme,
       jsonb_array_length(profile->'sales')            AS sales_year_count
FROM authors
WHERE profile IS NOT NULL;

-- Filter on a JSON field value:
SELECT * FROM authors
WHERE profile @> '{"preferences": {"newsletter": true}}';

-- Create a GIN index for fast containment queries:
CREATE INDEX idx_authors_profile_gin ON authors USING GIN (profile);

-- Create a B-tree index on a specific JSON path:
CREATE INDEX idx_authors_email ON authors ((profile #>> '{contact,email}'));
```

<p style="border-bottom: 1px solid lightgrey;"></p>

<h2><img style="float: left; margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/pencil2.png">6.2 – Extensions: PostgreSQL's Superpower</h2>

Extensions are the mechanism by which PostgreSQL's functionality is expanded. They are roughly equivalent to SQL Server's Features (e.g., Full-Text Search, Reporting Services) except they install at the database level, not the server level, and the community maintains hundreds of them.

Install an extension with `CREATE EXTENSION`:

```sql
CREATE EXTENSION IF NOT EXISTS <extension_name>;
```

**Important — `CREATE EXTENSION` does not download anything.** This is the single biggest surprise for SQL Server professionals. `CREATE EXTENSION` only *registers* an extension whose binary files (a `.dll` plus `.control` and `.sql` script files) are **already present on the server**. If those files are not on disk, you get an error like:

```
ERROR:  could not open extension control file
"C:/Program Files/PostgreSQL/16/share/extension/vector.control": No such file or directory
```

So there are always two phases: **(1) acquire the extension's files onto the server at the OS level, then (2) register it in each database with `CREATE EXTENSION`.** On Windows, how you accomplish phase 1 depends on which of three tiers the extension falls into.

**Tier 1 — Bundled `contrib` extensions (already on disk):**

Many extensions ship with the standard PostgreSQL Windows installer (the EDB build from <https://www.postgresql.org/download/windows/>) as part of the `contrib` modules. These require **no acquisition step at all** — the files are already in `C:\Program Files\PostgreSQL\<version>\share\extension\`. You only run `CREATE EXTENSION`.

This tier includes `pg_stat_statements`, `pg_trgm`, `tablefunc`, `postgres_fdw`, `uuid-ossp`, `pgcrypto`, `hstore`, `ltree`, and `intarray` — every extension used in this module's activities except PostGIS and pgvector. You can confirm what is available on your server with:

```sql
-- Lists every extension whose files are present and installable:
SELECT name, default_version, installed_version, comment
FROM pg_available_extensions
ORDER BY name;
```

If an extension appears in this view, phase 1 is already done and you can skip straight to `CREATE EXTENSION`.

**Tier 2 — Stack Builder extensions (downloaded via a GUI):**

**PostGIS** is the headline example. It is not in the base installer, but the EDB Windows installer ships a companion utility called **Stack Builder** (Start menu → *PostgreSQL <version>* → *Application Stack Builder*, or `StackBuilder.exe` in the `bin` folder) that downloads and installs it for you:

1. Launch **Application Stack Builder**.
2. Select your PostgreSQL installation from the dropdown, then **Next**.
3. Expand the **Spatial Extensions** category.
4. Check the latest **PostGIS … Bundle** for your PostgreSQL version, then **Next**.
5. Accept the defaults; Stack Builder downloads and runs the bundle installer, placing `postgis*.dll` and the control/script files into your PostgreSQL `lib` and `share\extension` folders.

If Stack Builder is blocked by a corporate firewall, you can instead download the standalone PostGIS bundle installer directly from <https://postgis.net/documentation/getting_started/install_windows/> and run it against your existing PostgreSQL installation. **Version-match matters:** a PostGIS bundle built for PostgreSQL 16 will not load into PostgreSQL 17, so always pick the bundle that matches your server's major version. Only after the files are on disk does this work:

```sql
CREATE EXTENSION IF NOT EXISTS postgis;
```

**Tier 3 — Build-from-source extensions (compiler required):**

**pgvector** is the example used later in this module. There is no Stack Builder entry and no bundled binary, so on Windows you compile it with the Microsoft Visual C++ toolchain:

1. Install **Visual Studio** (Community edition is fine) with the **"Desktop development with C++"** workload, which provides `nmake` and the MSVC compiler.
2. Open the **x64 Native Tools Command Prompt for VS** as Administrator (a regular PowerShell or `cmd` window will not have `nmake` on its path).
3. Point the build at your PostgreSQL installation and compile:

```bat
REM Tell the build where PostgreSQL lives (adjust the version):
set "PGROOT=C:\Program Files\PostgreSQL\16"

REM Fetch the source and build it:
cd %TEMP%
git clone --branch v0.8.0 https://github.com/pgvector/pgvector.git
cd pgvector
nmake /F Makefile.win
nmake /F Makefile.win install
```

That `install` step copies `vector.dll` into the PostgreSQL `lib` folder and `vector.control` into `share\extension`. You can verify before registering:

```bat
dir "C:\Program Files\PostgreSQL\16\lib\vector.dll"
dir "C:\Program Files\PostgreSQL\16\share\extension\vector.control"
```

Only then will this succeed:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

**A note on `pg_cron`:** it appears in the table below for completeness as the conceptual analog of SQL Server Agent, but the upstream project targets Linux and is **not officially supported on Windows**. On a Windows server, use SQL Server Agent's true PostgreSQL counterpart — **pgAgent** (available through Stack Builder under *Add-ons, tools and utilities*) — or the Windows Task Scheduler driving `psql` scripts.

**One more reminder — extensions that also preload a library:** `pg_stat_statements` (and `pg_cron` where supported) are special. Even though their files ship with the installer, they must additionally be listed in `shared_preload_libraries` in `postgresql.conf` and require a service restart *before* `CREATE EXTENSION` will work — see the detailed two-phase procedure in Module 04, section 4.4. Most other extensions (PostGIS, pg_trgm, tablefunc, postgres_fdw, pgvector, etc.) need only the file acquisition above plus `CREATE EXTENSION`, with no preload or restart.

**Commonly used extensions and their SQL Server analogs:**

| Extension | Description | SQL Server Equivalent |
|---|---|---|
| `pg_stat_statements` | Query performance tracking | Query Store |
| `uuid-ossp` | UUID generation functions | `NEWID()`, `NEWSEQUENTIALID()` |
| `pgcrypto` | Cryptographic functions | `HASHBYTES()`, `ENCRYPTBYKEY()` |
| `PostGIS` | Geospatial types, functions, indexes | SQL Server Spatial (geometry/geography types) |
| `pg_trgm` | Trigram fuzzy text matching | Fuzzy search via CONTAINS/FREETEXT (FTS) |
| `pg_partman` | Automated table partitioning management | SQL Agent + maintenance scripts |
| `pgvector` | Vector embeddings for AI/ML workloads | No equivalent (new in SQL Server 2025 preview) |
| `pg_cron` | Cron-style job scheduling | SQL Server Agent |
| `postgres_fdw` | Foreign data wrapper for other PostgreSQL instances | Linked Servers |
| `tablefunc` | `crosstab()` pivot function | `PIVOT` operator |
| `hstore` | Key-value store column type | No direct equivalent |
| `ltree` | Hierarchical label tree type | HierarchyID |
| `intarray` | Integer array operations | No equivalent |

**PostGIS — Spatial data (most important extension for enterprise work):**

On Windows, acquire the PostGIS files first via Stack Builder (Tier 2 above) — the `CREATE EXTENSION` below will fail until the bundle is installed and version-matched to your server.

```sql
CREATE EXTENSION IF NOT EXISTS postgis;

-- Add a geometry column to the authors table:
ALTER TABLE authors ADD COLUMN geolocation GEOMETRY(Point, 4326);

-- Update with coordinates (latitude/longitude) for Berkeley, CA authors:
UPDATE authors
SET geolocation = ST_SetSRID(ST_MakePoint(-122.2730, 37.8716), 4326)
WHERE city = 'Berkeley';

-- Find authors within 50km of a point (downtown San Francisco):
SELECT address, city
FROM authors
WHERE ST_DWithin(
    geolocation::geography,
    ST_SetSRID(ST_MakePoint(-122.4194, 37.7749), 4326)::geography,
    50000  -- 50km in meters
);

-- Create a spatial index:
CREATE INDEX idx_authors_geolocation ON authors USING GIST (geolocation);
```

**pg_trgm — Fuzzy text matching (very useful for search-as-you-type):**

```sql
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- Find names similar to a misspelling:
SELECT au_lname,
       similarity(au_lname, 'Smyth') AS sim_score
FROM authors
WHERE similarity(au_lname, 'Smyth') > 0.3
ORDER BY sim_score DESC;

-- Create a trigram index for fast similarity searches:
CREATE INDEX idx_authors_lname_trgm
    ON authors USING GIN (au_lname gin_trgm_ops);

-- Now LIKE with leading wildcard is fast (impossible to index in SQL Server):
SELECT * FROM authors WHERE au_lname LIKE '%ee%';
```

**pgvector — AI vector embeddings:**

```sql
-- On Windows, build and install pgvector first (Tier 3 above: Visual C++ + nmake).
-- This CREATE EXTENSION fails until vector.dll and vector.control are on disk:
CREATE EXTENSION IF NOT EXISTS vector;

-- Create a table with a vector column (for AI embeddings):
CREATE TABLE title_embeddings (
    title_id    VARCHAR(6) PRIMARY KEY,
    description TEXT,
    embedding   vector(1536)   -- OpenAI Ada-002 dimension
);

-- Find the 5 most similar titles to a given embedding:
SELECT title_id, description,
       embedding <=> '[0.1, 0.2, ...]'::vector AS distance
FROM title_embeddings
ORDER BY distance
LIMIT 5;

-- Create an approximate nearest-neighbor index (HNSW):
CREATE INDEX ON title_embeddings USING hnsw (embedding vector_cosine_ops);
```

<p style="border-bottom: 1px solid lightgrey;"></p>

<h2><img style="float: left; margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/pencil2.png">6.3 – Foreign Data Wrappers and Logical Replication</h2>

**Foreign Data Wrappers (FDW)** are PostgreSQL's equivalent of SQL Server Linked Servers. They allow you to query remote data sources — including other PostgreSQL instances, SQL Server, MySQL, Oracle, flat files, and REST APIs — as if they were local tables.

```sql
-- Connect one PostgreSQL instance to another:
CREATE EXTENSION IF NOT EXISTS postgres_fdw;

CREATE SERVER remote_pg_server
    FOREIGN DATA WRAPPER postgres_fdw
    OPTIONS (host 'remote-pg-host', port '5432', dbname 'production');

CREATE USER MAPPING FOR app_user
    SERVER remote_pg_server
    OPTIONS (user 'remote_user', password 'remote_password');

-- Create a foreign table (equivalent to a Linked Server table):
CREATE FOREIGN TABLE remote_sales (
    stor_id   CHAR(4),
    ord_num   VARCHAR(20),
    ord_date  TIMESTAMP,
    title_id  VARCHAR(6)
)
SERVER remote_pg_server
OPTIONS (schema_name 'public', table_name 'sales');

-- Query it just like a local table:
SELECT COUNT(*) FROM remote_sales WHERE ord_date > '1994-01-01';
```

**Connecting to SQL Server from PostgreSQL using tds_fdw:**

```sql
-- Install tds_fdw from: https://github.com/tds-fdw/tds_fdw
CREATE EXTENSION tds_fdw;

CREATE SERVER sqlserver_link
    FOREIGN DATA WRAPPER tds_fdw
    OPTIONS (servername '192.168.1.100', port '1433', database 'pubs');

CREATE USER MAPPING FOR postgres
    SERVER sqlserver_link
    OPTIONS (username 'sa', password 'YourSQLPassword');

CREATE FOREIGN TABLE sqlserver_authors (
    au_id     VARCHAR(11),
    au_fname  VARCHAR(20),
    au_lname  VARCHAR(40)
)
SERVER sqlserver_link
OPTIONS (query 'SELECT au_id, au_fname, au_lname FROM dbo.authors');

SELECT * FROM sqlserver_authors LIMIT 10;
```

**Logical Replication — PostgreSQL equivalent of transactional replication:**

```sql
-- On the publisher (source) server:
-- Set wal_level = logical in postgresql.conf

CREATE PUBLICATION pubs_pub FOR TABLE authors, sales;

-- On the subscriber (destination) server:
CREATE SUBSCRIPTION pubs_sub
    CONNECTION 'host=publisher-host port=5432 dbname=pubs user=replicator password=ReplicaPass1!'
    PUBLICATION pubs_pub;
```

This replicates specific tables from one PostgreSQL instance to another, supporting cross-version replication and selective table replication — something SQL Server transactional replication also supports but with more configuration overhead.

<p style="border-bottom: 1px solid lightgrey;"></p>

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/point1.png"><b>Activity 6.1 – Work with JSONB and Extensions</b></p>

<p><img style="margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/checkmark.png"><b>Steps</b></p>

**Step 1 — Load JSONB profile data for multiple authors:**

```sql
\c pubs

-- Update authors with JSONB profile data.
-- The authors primary key (au_id) is a text value, so we derive an integer
-- seed with ROW_NUMBER() to drive the synthetic data generation:
WITH numbered AS (
    SELECT au_id,
           ROW_NUMBER() OVER (ORDER BY au_id) AS n
    FROM authors
),
updates AS (
    SELECT au_id,
           jsonb_build_object(
               'contact', jsonb_build_object(
                   'email', 'author' || n || '@example.com',
                   'phone', '555-' || LPAD((n * 37 % 10000)::TEXT, 4, '0')
               ),
               'preferences', jsonb_build_object(
                   'newsletter', (n % 2 = 0),
                   'theme', CASE WHEN n % 3 = 0 THEN 'dark'
                                 WHEN n % 3 = 1 THEN 'light'
                                 ELSE 'auto' END
               ),
               'tags', jsonb_build_array(
                   CASE (n % 3) WHEN 0 THEN 'vip' WHEN 1 THEN 'standard' ELSE 'new' END
               )
           ) AS profile_data
    FROM numbered
)
UPDATE authors a
SET    profile = u.profile_data
FROM   updates u
WHERE  a.au_id = u.au_id;
```

**Step 2 — Query JSONB fields:**

```sql
-- Extract specific fields using JSONB operators:
SELECT au_id,
       au_fname,
       au_lname,
       profile ->> 'preferences'                       AS preferences_json,
       (profile -> 'preferences' ->> 'newsletter')::BOOLEAN AS newsletter,
       profile -> 'preferences' ->> 'theme'            AS theme,
       profile -> 'tags' ->> 0                         AS first_tag
FROM authors
WHERE profile IS NOT NULL
LIMIT 10;

-- Filter: find all VIP authors who want newsletters:
SELECT au_fname, au_lname
FROM authors
WHERE profile @> '{"tags": ["vip"]}'::jsonb
  AND profile @> '{"preferences": {"newsletter": true}}'::jsonb;

-- Count authors by theme preference:
SELECT profile -> 'preferences' ->> 'theme' AS theme,
       COUNT(*) AS author_count
FROM authors
WHERE profile IS NOT NULL
GROUP BY theme
ORDER BY author_count DESC;
```

**Step 3 — Install and use pg_trgm for fuzzy search:**

`pg_trgm` is a bundled `contrib` extension (Tier 1), so its files already ship with the Windows installer — `CREATE EXTENSION` works with no prior download:

```sql
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- Find names similar to a misspelling:
SELECT au_lname,
       ROUND(similarity(au_lname, 'Smyth')::NUMERIC, 3) AS score
FROM authors
WHERE similarity(au_lname, 'Smyth') > 0.2
ORDER BY score DESC
LIMIT 10;

-- Create trigram index for LIKE acceleration:
CREATE INDEX idx_authors_lname_trgm
    ON authors USING GIN (au_lname gin_trgm_ops);

-- A LIKE with a leading wildcard — normally impossible to index:
EXPLAIN ANALYZE
SELECT au_fname, au_lname
FROM authors
WHERE au_lname LIKE '%ee%';   -- Can use GIN trigram index
```

**Step 4 — Use the tablefunc extension for PIVOT-like operations:**

```sql
-- The PostgreSQL equivalent of SQL Server's PIVOT operator:
CREATE EXTENSION IF NOT EXISTS tablefunc;

-- Count authors by state and contract status (pivot):
SELECT *
FROM crosstab(
    'SELECT state, contract, COUNT(*)::INT
     FROM authors
     WHERE state IS NOT NULL
     GROUP BY state, contract
     ORDER BY 1, 2',
    'VALUES (0), (1)'
) AS ct(state TEXT, no_contract INT, under_contract INT);

-- SQL Server equivalent:
-- SELECT state, [0], [1]
-- FROM (SELECT state, contract FROM dbo.authors) src
-- PIVOT (COUNT(contract) FOR contract IN ([0],[1])) pvt;
```

<p style="border-bottom: 1px solid lightgrey;"></p>

<h2><img style="float: left; margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/pencil2.png">6.4 – Migration from SQL Server to PostgreSQL</h2>

When migrating an existing SQL Server workload to PostgreSQL, the effort falls into three categories: schema migration, data migration, and code migration (T-SQL to PL/pgSQL).

**Migration tools:**

**1. AWS Schema Conversion Tool (SCT) / AWS DMS**

AWS SCT analyzes your SQL Server schema and stored procedures and generates PostgreSQL-compatible DDL with an assessment report showing what can be automatically converted and what requires manual work.

- [AWS SCT Download](https://docs.aws.amazon.com/SchemaConversionTool/latest/userguide/CHAP_UserInterface.html)
- [AWS DMS for SQL Server to PostgreSQL](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Source.SQLServer.html)

**2. EDB Migration Portal**

EnterpriseDB's free web-based migration assessment tool. Upload your SQL Server schema DDL and receive a PostgreSQL conversion report.

- [EDB Migration Portal](https://www.enterprisedb.com/products/migration-portal)

**3. pgLoader**

An open-source tool that can migrate data and schema from SQL Server (via ODBC/FreeTDS) to PostgreSQL in a single streaming command.

```bat
REM pgLoader command-line migration (Linux/macOS primarily):
pgloader mssql://sa:password@192.168.1.100/pubs postgresql://postgres:password@localhost/pubs_migrated
```

- [pgLoader Documentation](https://pgloader.io/)
- [pgLoader SQL Server to PostgreSQL](https://pgloader.readthedocs.io/en/latest/ref/mssql.html)

**4. Microsoft SSMA (SQL Server Migration Assistant)**

Microsoft's own free tool for migrating from SQL Server to Azure Database for PostgreSQL.

- [SSMA for PostgreSQL](https://learn.microsoft.com/en-us/sql/ssma/postgresql/sql-server-migration-assistant-for-postgresql-sybasetosql)

**Migration checklist for a SQL Server-to-PostgreSQL migration:**

```
Phase 1 – Assessment
  ☐ Run EDB Migration Portal or AWS SCT on the schema
  ☐ Identify unsupported objects (CLR, linked servers, SQL Agent jobs)
  ☐ Identify T-SQL features requiring rewrite (MERGE, OUTPUT INTO, FOR XML, etc.)
  ☐ Identify IDENTITY columns and plan SEQUENCE/SERIAL strategy
  ☐ Note collation differences (case-insensitive → case-sensitive)
  ☐ Estimate data volume and migration window

Phase 2 – Schema Migration
  ☐ Convert data types (MONEY→NUMERIC, TINYINT→SMALLINT, NVARCHAR→VARCHAR, etc.)
  ☐ Convert DDL (IDENTITY→GENERATED, square brackets→lowercase)
  ☐ Convert views (remove WITH NOEXPAND, check hints)
  ☐ Convert stored procedures/functions (T-SQL→PL/pgSQL)
  ☐ Convert triggers (INSERTED/DELETED→NEW/OLD, SET NOCOUNT→default PG behavior)

Phase 3 – Data Migration
  ☐ Disable FK constraints and indexes for bulk load
  ☐ Use COPY or pg_dump from SQL Server export for initial load
  ☐ Re-enable constraints, run ANALYZE
  ☐ Validate row counts and key samples
  ☐ Reset sequences to max(id) + 1

Phase 4 – Application Testing
  ☐ Update connection strings (SQL Server driver → psycopg2/npgsql/pg driver)
  ☐ Handle case-sensitivity in string comparisons
  ☐ Verify ORM mappings (Entity Framework, Hibernate, SQLAlchemy)
  ☐ Load test and tune (random_page_cost, work_mem, connection pooling)

Phase 5 – Cutover
  ☐ Set up logical replication for near-zero-downtime cutover
  ☐ Plan rollback procedure
  ☐ Monitor pg_stat_activity and pg_stat_statements post-cutover
```

**Trigger syntax — a common migration pain point:**

```sql
-- SQL Server trigger:
-- CREATE TRIGGER trg_titles_audit
-- ON dbo.titles
-- AFTER INSERT, UPDATE
-- AS BEGIN
--     INSERT INTO audit_log (table_name, action, row_id)
--     SELECT 'titles', 'INSERT/UPDATE', i.title_id
--     FROM inserted i;
-- END;

-- PostgreSQL requires a trigger FUNCTION + a trigger binding:
CREATE OR REPLACE FUNCTION trg_titles_audit_fn()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO audit_log (table_name, action, row_id, changed_at)
    VALUES ('titles', TG_OP, NEW.title_id, NOW());
    RETURN NEW;    -- RETURN OLD for DELETE triggers
END;
$$;

CREATE TRIGGER trg_titles_audit
    AFTER INSERT OR UPDATE
    ON titles
    FOR EACH ROW
    EXECUTE FUNCTION trg_titles_audit_fn();
```

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/point1.png"><b>Activity 6.2 – Migration Simulation: Convert a SQL Server Object to PostgreSQL</b></p>

<p><img style="margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/checkmark.png"><b>Steps</b></p>

**Step 1 — Create an audit log table:**

```sql
CREATE TABLE audit_log (
    audit_id    INTEGER      GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    table_name  VARCHAR(128) NOT NULL,
    action      VARCHAR(10)  NOT NULL,
    row_id      VARCHAR(6)   NOT NULL,
    changed_at  TIMESTAMP    NOT NULL DEFAULT NOW(),
    changed_by  VARCHAR(100) NOT NULL DEFAULT current_user
);
```

**Step 2 — Create an audit trigger on titles:**

```sql
CREATE OR REPLACE FUNCTION trg_titles_audit_fn()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    IF TG_OP = 'INSERT' OR TG_OP = 'UPDATE' THEN
        INSERT INTO audit_log (table_name, action, row_id)
        VALUES ('titles', TG_OP, NEW.title_id);
        RETURN NEW;
    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO audit_log (table_name, action, row_id)
        VALUES ('titles', TG_OP, OLD.title_id);
        RETURN OLD;
    END IF;
END;
$$;

CREATE TRIGGER trg_titles_audit
    AFTER INSERT OR UPDATE OR DELETE
    ON titles
    FOR EACH ROW
    EXECUTE FUNCTION trg_titles_audit_fn();
```

**Step 3 — Test the trigger:**

```sql
-- Insert a new title (publisher 1389 already exists in pubs):
INSERT INTO titles
    (title_id, title, type, pub_id, price)
VALUES ('AUD001', 'Auditing for Fun and Profit', 'business', '1389', 29.99);

-- Update the title:
UPDATE titles
SET price = 34.99
WHERE title_id = 'AUD001';

-- Delete the title:
DELETE FROM titles
WHERE title_id = 'AUD001';

-- Check the audit log:
SELECT * FROM audit_log ORDER BY audit_id;
```

**Step 4 — Simulate the MERGE statement (SQL Server) in PostgreSQL using INSERT ... ON CONFLICT:**

```sql
-- SQL Server MERGE equivalent in PostgreSQL:
-- In SQL Server:
-- MERGE INTO dbo.publishers AS target
-- USING (VALUES ('9970','Tech Press Books','Austin'),
--               ('9971','Data Lake Media','Denver')) AS src(pub_id, pub_name, city)
-- ON target.pub_id = src.pub_id
-- WHEN MATCHED THEN UPDATE SET pub_name = src.pub_name, city = src.city
-- WHEN NOT MATCHED THEN INSERT (pub_id, pub_name, city) VALUES (src.pub_id, src.pub_name, src.city);

-- PostgreSQL INSERT ... ON CONFLICT (UPSERT).
-- Note: pub_id has a CHECK constraint allowing the fixed set or any '99%' value,
-- so the new publishers below use 99-prefixed IDs. Publisher 1389 already exists,
-- which exercises the UPDATE-on-match path:
INSERT INTO publishers (pub_id, pub_name, city, country)
VALUES
    ('9970', 'Tech Press Books', 'Austin',  'USA'),
    ('9971', 'Data Lake Media',  'Denver',  'USA'),
    ('1389', 'Algodata Infosystems (updated)', 'Berkeley', 'USA')
ON CONFLICT (pub_id)
DO UPDATE SET
    pub_name = EXCLUDED.pub_name,
    city     = EXCLUDED.city;

-- Verify:
SELECT pub_id, pub_name, city, country FROM publishers ORDER BY pub_id;
```

The `EXCLUDED` table (equivalent to `source` in SQL Server MERGE) contains the values that would have been inserted.

**Step 5 — Review the full workshop by examining the pubs schema:**

```sql
-- What we have built today:
\dt public.*
\df public.*     -- List all functions
\dT             -- List all custom types/extensions

-- Final schema summary:
SELECT table_schema, table_name,
       (SELECT COUNT(*) FROM information_schema.columns c
        WHERE c.table_schema = t.table_schema
          AND c.table_name   = t.table_name) AS column_count
FROM information_schema.tables t
WHERE table_type = 'BASE TABLE'
  AND table_schema NOT IN ('pg_catalog','information_schema')
ORDER BY table_schema, table_name;
```

<p style="border-bottom: 1px solid lightgrey;"></p>

<p><img style="margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/owl.png"><b>For Further Study</b></p>

**Migrations**
- [Migration Tooling from Tim Chapman](https://github.com/timchapman/sqlserver-to-postgresql)

**JSONB and JSON:**
- [PostgreSQL Documentation — JSON Functions and Operators](https://www.postgresql.org/docs/current/functions-json.html)
- [PostgreSQL Documentation — JSON Types](https://www.postgresql.org/docs/current/datatype-json.html)

**Extensions:**
- [PostgreSQL Extension Network (PGXN)](https://pgxn.org/)
- [PostGIS Documentation](https://postgis.net/documentation/)
- [pgvector — Vector Similarity Search](https://github.com/pgvector/pgvector)
- [pg_trgm Documentation](https://www.postgresql.org/docs/current/pgtrgm.html)
- [pg_cron — Job Scheduling](https://github.com/citusdata/pg_cron)
- [tablefunc — crosstab/pivot](https://www.postgresql.org/docs/current/tablefunc.html)

**Foreign Data Wrappers:**
- [PostgreSQL Documentation — Foreign Data](https://www.postgresql.org/docs/current/ddl-foreign-data.html)
- [tds_fdw — SQL Server/Sybase FDW](https://github.com/tds-fdw/tds_fdw)

**Replication:**
- [PostgreSQL Documentation — Logical Replication](https://www.postgresql.org/docs/current/logical-replication.html)

**Migration Tools:**
- [AWS Schema Conversion Tool](https://docs.aws.amazon.com/SchemaConversionTool/latest/userguide/CHAP_UserInterface.html)
- [EDB Migration Portal](https://www.enterprisedb.com/products/migration-portal)
- [pgLoader](https://pgloader.io/)
- [Microsoft SSMA for PostgreSQL](https://learn.microsoft.com/en-us/sql/ssma/postgresql/sql-server-migration-assistant-for-postgresql-sybasetosql)
- [Azure Database Migration Service](https://learn.microsoft.com/en-us/azure/dms/tutorial-sql-server-to-azure-postgresql)

**General PostgreSQL for SQL Server Professionals:**
- [Use The Index, Luke — SQL Performance for PostgreSQL](https://use-the-index-luke.com/)
- [The Art of PostgreSQL (book)](https://theartofpostgresql.com/)
- [Postgres Weekly Newsletter](https://postgresweekly.com/)
- [Citus Data Blog](https://www.citusdata.com/blog/)
- [depesz Blog — Postgresql DBA Resources](https://www.depesz.com/)
- [Microsoft Resource Center for Postgres](https://techcommunity.microsoft.com/blog/adforpostgresql/introducing-postgresql-hub-for-azure-developers/4522897)

<p style="border-bottom: 1px solid lightgrey;"></p>

<p><img style="margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/owl.png"><b>Congratulations!</b></p>

You have completed the **PostgreSQL for the SQL Server Database Professional** workshop! You now have the tools, vocabulary, and hands-on experience to:

- Navigate a PostgreSQL cluster and understand how it maps to your SQL Server knowledge
- Design schemas using the correct PostgreSQL data types and DDL patterns
- Translate T-SQL queries and stored procedures into PostgreSQL and PL/pgSQL
- Create and tune indexes, read EXPLAIN ANALYZE output, and identify performance problems
- Administer users, roles, backups, and monitoring in PostgreSQL
- Leverage PostgreSQL-specific advanced features including JSONB, extensions, FDW, and replication
- Plan and execute a migration from SQL Server to PostgreSQL

The next step is to apply these skills to a real workload at your organization. Use the references at the end of each module to deepen your knowledge in the areas most relevant to your work.

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/geopin.png"><b>Return to Workshop Home</b></p>

Return to <a href="README.md" target="_blank">the workshop README</a>.
