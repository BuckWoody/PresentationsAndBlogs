![](graphics/microsoftlogo.png)

# Workshop: PostgreSQL for the SQL Server Database Professional

#### <i>A Microsoft-style Course — SQL Server & PostgreSQL Track</i>

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
-- Add a JSONB column to the person table:
ALTER TABLE person.person ADD COLUMN profile JSONB;

-- Update with JSON data:
UPDATE person.person
SET profile = '{
    "contact": {"phone": "555-1234", "email": "jsmith@example.com"},
    "preferences": {"newsletter": true, "theme": "dark"},
    "orders": [{"year": 2023, "count": 5}, {"year": 2024, "count": 12}]
}'
WHERE last_name = 'Smith'
LIMIT 1;

-- Query JSON fields:
SELECT business_entity_id,
       first_name,
       profile->>'contact'                             AS contact_json,
       profile #>> '{contact,email}'                  AS email,
       profile #>> '{preferences,theme}'              AS theme,
       jsonb_array_length(profile->'orders')           AS order_year_count
FROM person.person
WHERE profile IS NOT NULL;

-- Filter on a JSON field value:
SELECT * FROM person.person
WHERE profile @> '{"preferences": {"newsletter": true}}';

-- Create a GIN index for fast containment queries:
CREATE INDEX idx_person_profile_gin ON person.person USING GIN (profile);

-- Create a B-tree index on a specific JSON path:
CREATE INDEX idx_person_email ON person.person ((profile #>> '{contact,email}'));
```

<p style="border-bottom: 1px solid lightgrey;"></p>

<h2><img style="float: left; margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/pencil2.png">6.2 – Extensions: PostgreSQL's Superpower</h2>

Extensions are the mechanism by which PostgreSQL's functionality is expanded. They are roughly equivalent to SQL Server's Features (e.g., Full-Text Search, Reporting Services) except they install at the database level, not the server level, and the community maintains hundreds of them.

Install an extension with `CREATE EXTENSION`:

```sql
CREATE EXTENSION IF NOT EXISTS <extension_name>;
```

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

```sql
CREATE EXTENSION IF NOT EXISTS postgis;

-- Add a geometry column:
ALTER TABLE person.address ADD COLUMN geolocation GEOMETRY(Point, 4326);

-- Update with coordinates (latitude/longitude):
UPDATE person.address
SET geolocation = ST_SetSRID(ST_MakePoint(-122.3321, 47.6062), 4326)
WHERE city = 'Seattle';

-- Find addresses within 50km of a point:
SELECT address_line1, city
FROM person.address
WHERE ST_DWithin(
    geolocation::geography,
    ST_SetSRID(ST_MakePoint(-122.3321, 47.6062), 4326)::geography,
    50000  -- 50km in meters
);

-- Create a spatial index:
CREATE INDEX idx_address_geolocation ON person.address USING GIST (geolocation);
```

**pg_trgm — Fuzzy text matching (very useful for search-as-you-type):**

```sql
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- Find names similar to a misspelling:
SELECT last_name,
       similarity(last_name, 'Smyth') AS sim_score
FROM person.person
WHERE similarity(last_name, 'Smyth') > 0.3
ORDER BY sim_score DESC;

-- Create a trigram index for fast similarity searches:
CREATE INDEX idx_person_last_name_trgm
    ON person.person USING GIN (last_name gin_trgm_ops);

-- Now LIKE with leading wildcard is fast (impossible to index in SQL Server):
SELECT * FROM person.person WHERE last_name LIKE '%ith%';
```

**pgvector — AI vector embeddings:**

```sql
-- Install pgvector (requires separate installation: https://github.com/pgvector/pgvector)
CREATE EXTENSION IF NOT EXISTS vector;

-- Create a table with a vector column (for AI embeddings):
CREATE TABLE product_embeddings (
    product_id  INTEGER PRIMARY KEY,
    description TEXT,
    embedding   vector(1536)   -- OpenAI Ada-002 dimension
);

-- Find the 5 most similar products to a given embedding:
SELECT product_id, description,
       embedding <=> '[0.1, 0.2, ...]'::vector AS distance
FROM product_embeddings
ORDER BY distance
LIMIT 5;

-- Create an approximate nearest-neighbor index (HNSW):
CREATE INDEX ON product_embeddings USING hnsw (embedding vector_cosine_ops);
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
CREATE FOREIGN TABLE remote_orders (
    order_id   INTEGER,
    order_date TIMESTAMP,
    customer_id INTEGER
)
SERVER remote_pg_server
OPTIONS (schema_name 'sales', table_name 'sales_order_header');

-- Query it just like a local table:
SELECT COUNT(*) FROM remote_orders WHERE order_date > '2024-01-01';
```

**Connecting to SQL Server from PostgreSQL using tds_fdw:**

```sql
-- Install tds_fdw from: https://github.com/tds-fdw/tds_fdw
CREATE EXTENSION tds_fdw;

CREATE SERVER sqlserver_link
    FOREIGN DATA WRAPPER tds_fdw
    OPTIONS (servername '192.168.1.100', port '1433', database 'AdventureWorks2022');

CREATE USER MAPPING FOR postgres
    SERVER sqlserver_link
    OPTIONS (username 'sa', password 'YourSQLPassword');

CREATE FOREIGN TABLE sqlserver_contacts (
    business_entity_id INTEGER,
    first_name         VARCHAR(50),
    last_name          VARCHAR(50)
)
SERVER sqlserver_link
OPTIONS (query 'SELECT BusinessEntityID, FirstName, LastName FROM Person.Person');

SELECT * FROM sqlserver_contacts LIMIT 10;
```

**Logical Replication — PostgreSQL equivalent of transactional replication:**

```sql
-- On the publisher (source) server:
-- Set wal_level = logical in postgresql.conf

CREATE PUBLICATION aw_pub FOR TABLE person.person, sales.sales_order_header;

-- On the subscriber (destination) server:
CREATE SUBSCRIPTION aw_sub
    CONNECTION 'host=publisher-host port=5432 dbname=adventureworks user=replicator password=ReplicaPass1!'
    PUBLICATION aw_pub;
```

This replicates specific tables from one PostgreSQL instance to another, supporting cross-version replication and selective table replication — something SQL Server transactional replication also supports but with more configuration overhead.

<p style="border-bottom: 1px solid lightgrey;"></p>

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/point1.png"><b>Activity 6.1 – Work with JSONB and Extensions</b></p>

<p><img style="margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/checkmark.png"><b>Steps</b></p>

**Step 1 — Load JSONB profile data for multiple persons:**

```sql
\c adventureworks

-- Update several persons with JSONB profile data:
WITH updates AS (
    SELECT business_entity_id,
           jsonb_build_object(
               'contact', jsonb_build_object(
                   'email', 'person' || business_entity_id || '@example.com',
                   'phone', '555-' || LPAD((business_entity_id * 37 % 10000)::TEXT, 4, '0')
               ),
               'preferences', jsonb_build_object(
                   'newsletter', (business_entity_id % 2 = 0),
                   'theme', CASE WHEN business_entity_id % 3 = 0 THEN 'dark'
                                 WHEN business_entity_id % 3 = 1 THEN 'light'
                                 ELSE 'auto' END
               ),
               'tags', jsonb_build_array(
                   CASE (business_entity_id % 3) WHEN 0 THEN 'vip' WHEN 1 THEN 'standard' ELSE 'new' END
               )
           ) AS profile_data
    FROM person.person
    LIMIT 100
)
UPDATE person.person p
SET    profile = u.profile_data
FROM   updates u
WHERE  p.business_entity_id = u.business_entity_id;
```

**Step 2 — Query JSONB fields:**

```sql
-- Extract specific fields using JSONB operators:
SELECT business_entity_id,
       first_name,
       last_name,
       profile ->> 'preferences'                       AS preferences_json,
       (profile -> 'preferences' ->> 'newsletter')::BOOLEAN AS newsletter,
       profile -> 'preferences' ->> 'theme'            AS theme,
       profile -> 'tags' ->> 0                         AS first_tag
FROM person.person
WHERE profile IS NOT NULL
LIMIT 10;

-- Filter: find all VIP customers who want newsletters:
SELECT first_name, last_name
FROM person.person
WHERE profile @> '{"tags": ["vip"]}'::jsonb
  AND profile @> '{"preferences": {"newsletter": true}}'::jsonb;

-- Count persons by theme preference:
SELECT profile -> 'preferences' ->> 'theme' AS theme,
       COUNT(*) AS person_count
FROM person.person
WHERE profile IS NOT NULL
GROUP BY theme
ORDER BY person_count DESC;
```

**Step 3 — Install and use pg_trgm for fuzzy search:**

```sql
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- Find names similar to a misspelling:
SELECT last_name,
       ROUND(similarity(last_name, 'Smyth')::NUMERIC, 3) AS score
FROM person.person
WHERE similarity(last_name, 'Smyth') > 0.2
ORDER BY score DESC
LIMIT 10;

-- Create trigram index for LIKE acceleration:
CREATE INDEX idx_person_last_name_trgm
    ON person.person USING GIN (last_name gin_trgm_ops);

-- A LIKE with a leading wildcard — normally impossible to index:
EXPLAIN ANALYZE
SELECT first_name, last_name
FROM person.person
WHERE last_name LIKE '%son%';   -- Can use GIN trigram index
```

**Step 4 — Use the tablefunc extension for PIVOT-like operations:**

```sql
-- The PostgreSQL equivalent of SQL Server's PIVOT operator:
CREATE EXTENSION IF NOT EXISTS tablefunc;

-- Count persons by person_type and email_promotion level (pivot):
SELECT *
FROM crosstab(
    'SELECT person_type, email_promotion, COUNT(*)::INT
     FROM person.person
     GROUP BY person_type, email_promotion
     ORDER BY 1, 2',
    'VALUES (0), (1), (2)'
) AS ct(person_type TEXT, promo_0 INT, promo_1 INT, promo_2 INT);

-- SQL Server equivalent:
-- SELECT person_type, [0], [1], [2]
-- FROM (SELECT person_type, email_promotion FROM person.person) src
-- PIVOT (COUNT(email_promotion) FOR email_promotion IN ([0],[1],[2])) pvt;
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
pgloader mssql://sa:password@192.168.1.100/AdventureWorks2022 postgresql://postgres:password@localhost/adventureworks_migrated
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
-- CREATE TRIGGER trg_orders_audit
-- ON sales.SalesOrderHeader
-- AFTER INSERT, UPDATE
-- AS BEGIN
--     INSERT INTO audit_log (table_name, action, row_id)
--     SELECT 'SalesOrderHeader', 'INSERT/UPDATE', i.SalesOrderID
--     FROM inserted i;
-- END;

-- PostgreSQL requires a trigger FUNCTION + a trigger binding:
CREATE OR REPLACE FUNCTION sales.trg_orders_audit_fn()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO audit_log (table_name, action, row_id, changed_at)
    VALUES ('sales_order_header', TG_OP, NEW.sales_order_id, NOW());
    RETURN NEW;    -- RETURN OLD for DELETE triggers
END;
$$;

CREATE TRIGGER trg_orders_audit
    AFTER INSERT OR UPDATE
    ON sales.sales_order_header
    FOR EACH ROW
    EXECUTE FUNCTION sales.trg_orders_audit_fn();
```

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/point1.png"><b>Activity 6.2 – Migration Simulation: Convert a SQL Server Object to PostgreSQL</b></p>

<p><img style="margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/checkmark.png"><b>Steps</b></p>

**Step 1 — Create an audit log table:**

```sql
CREATE TABLE audit_log (
    audit_id    INTEGER      GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    table_name  VARCHAR(128) NOT NULL,
    action      VARCHAR(10)  NOT NULL,
    row_id      INTEGER      NOT NULL,
    changed_at  TIMESTAMP    NOT NULL DEFAULT NOW(),
    changed_by  VARCHAR(100) NOT NULL DEFAULT current_user
);
```

**Step 2 — Create an audit trigger on sales_order_header:**

```sql
CREATE OR REPLACE FUNCTION sales.trg_orders_audit_fn()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    IF TG_OP = 'INSERT' OR TG_OP = 'UPDATE' THEN
        INSERT INTO audit_log (table_name, action, row_id)
        VALUES ('sales_order_header', TG_OP, NEW.sales_order_id);
        RETURN NEW;
    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO audit_log (table_name, action, row_id)
        VALUES ('sales_order_header', TG_OP, OLD.sales_order_id);
        RETURN OLD;
    END IF;
END;
$$;

CREATE TRIGGER trg_orders_audit
    AFTER INSERT OR UPDATE OR DELETE
    ON sales.sales_order_header
    FOR EACH ROW
    EXECUTE FUNCTION sales.trg_orders_audit_fn();
```

**Step 3 — Test the trigger:**

```sql
-- Insert a new order:
INSERT INTO sales.sales_order_header
    (sales_order_number, customer_id, subtotal, tax_amt, freight)
VALUES ('SO-AUDIT-001', 1, 200.00, 20.00, 10.00);

-- Update an order:
UPDATE sales.sales_order_header
SET subtotal = 250.00
WHERE sales_order_number = 'SO-AUDIT-001';

-- Delete an order:
DELETE FROM sales.sales_order_header
WHERE sales_order_number = 'SO-AUDIT-001';

-- Check the audit log:
SELECT * FROM audit_log ORDER BY audit_id;
```

**Step 4 — Simulate the MERGE statement (SQL Server) in PostgreSQL using INSERT ... ON CONFLICT:**

```sql
-- SQL Server MERGE equivalent in PostgreSQL:
-- In SQL Server:
-- MERGE INTO sales.currency AS target
-- USING (VALUES ('USD','US Dollar'),('EUR','Euro'),('GBP','British Pound')) AS src(code,name)
-- ON target.currency_code = src.code
-- WHEN MATCHED THEN UPDATE SET name = src.name
-- WHEN NOT MATCHED THEN INSERT (currency_code, name) VALUES (src.code, src.name);

-- PostgreSQL INSERT ... ON CONFLICT (UPSERT):
INSERT INTO sales.currency (currency_code, name)
VALUES
    ('USD', 'US Dollar'),
    ('EUR', 'Euro'),
    ('GBP', 'British Pound'),
    ('JPY', 'Japanese Yen')
ON CONFLICT (currency_code)
DO UPDATE SET
    name          = EXCLUDED.name,
    modified_date = NOW();

-- Verify:
SELECT * FROM sales.currency ORDER BY currency_code;
```

The `EXCLUDED` table (equivalent to `source` in SQL Server MERGE) contains the values that would have been inserted.

**Step 5 — Review the full workshop by examining the adventureworks schema:**

```sql
-- What we have built today:
\dt person.*
\dt sales.*
\df sales.*     -- List all functions
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
