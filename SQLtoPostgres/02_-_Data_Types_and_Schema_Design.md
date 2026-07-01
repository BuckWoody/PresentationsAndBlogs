![](graphics/microsoftlogo.png)

# Workshop: PostgreSQL for the SQL Server Database Professional

#### <i>A SQL Server to PostgreSQL Skilling</i>


<p style="border-bottom: 1px solid lightgrey;"></p>

<img style="float: left; margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/textbubble.png"> <h2>Module 02 – Data Types and Schema Design</h2>

*Estimated Time: 60 minutes (≈20 minutes lecture, ≈40 minutes hands-on)*

In this module you will build the workshop sample schema in PostgreSQL, translating SQL Server DDL patterns as you go. You will learn the type-mapping rules that cover 95% of real-world migrations, understand how PostgreSQL handles auto-increment columns and sequences differently from SQL Server's `IDENTITY`, and learn the DDL differences around constraints, defaults, and computed columns.

<p style="border-bottom: 1px solid lightgrey;"></p>

<h2><img style="float: left; margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/pencil2.png">2.1 – Data Type Mapping: SQL Server to PostgreSQL</h2>

The table below maps the most common SQL Server data types to their PostgreSQL equivalents. Study this carefully — type mismatches are the most common source of errors in migrations.

| SQL Server Type | PostgreSQL Equivalent | Notes |
|---|---|---|
| `INT` / `INTEGER` | `INTEGER` or `INT4` | Direct equivalent |
| `BIGINT` | `BIGINT` or `INT8` | Direct equivalent |
| `SMALLINT` | `SMALLINT` or `INT2` | Direct equivalent |
| `TINYINT` | `SMALLINT` | PostgreSQL has no 1-byte integer; use `SMALLINT` (2 bytes) |
| `BIT` | `BOOLEAN` | SQL Server: 0/1/NULL. PostgreSQL: `true`/`false`/NULL |
| `DECIMAL(p,s)` / `NUMERIC(p,s)` | `NUMERIC(p,s)` | Direct equivalent |
| `FLOAT` | `DOUBLE PRECISION` or `FLOAT8` | IEEE 754 64-bit |
| `REAL` | `REAL` or `FLOAT4` | IEEE 754 32-bit |
| `MONEY` / `SMALLMONEY` | `NUMERIC(19,4)` | No native MONEY type in PostgreSQL; use NUMERIC |
| `CHAR(n)` | `CHAR(n)` | Direct equivalent (blank-padded) |
| `VARCHAR(n)` | `VARCHAR(n)` | Direct equivalent |
| `VARCHAR(MAX)` | `TEXT` | PostgreSQL TEXT has no length limit |
| `NCHAR(n)` | `CHAR(n)` | PostgreSQL databases are typically created as UTF-8 (encoding is chosen per database), so no N-prefix is needed. |
| `NVARCHAR(n)` | `VARCHAR(n)` | PostgreSQL databases are typically created as UTF-8 (encoding is chosen per database), so no N-prefix is needed.|
| `NVARCHAR(MAX)` | `TEXT` | PostgreSQL databases are typically created as UTF-8 (encoding is chosen per database), so no N-prefix is needed. |
| `TEXT` (deprecated in SS) | `TEXT` | Same name, similar behavior |
| `DATETIME` | `TIMESTAMP` | PostgreSQL TIMESTAMP has microsecond precision |
| `DATETIME2(7)` | `TIMESTAMP(6)` | 6 decimal places = microseconds (max in PG) |
| `SMALLDATETIME` | `TIMESTAMP(0)` | No seconds fractions |
| `DATE` | `DATE` | Direct equivalent |
| `TIME(7)` | `TIME(6)` | 6 decimal places |
| `DATETIMEOFFSET` | `TIMESTAMPTZ` | Timezone-aware timestamp |
| `UNIQUEIDENTIFIER` | `UUID` | Direct equivalent; use `gen_random_uuid()` |
| `VARBINARY(MAX)` | `BYTEA` | Binary data; different literal syntax |
| `XML` | `XML` | XML type exists; `XMLQUERY`/`XMLTABLE` differ |
| `JSON` (NVARCHAR) | `JSON` or `JSONB` | PostgreSQL has native JSON types (covered in Module 06) |
| `GEOGRAPHY` | `geometry` / `geography` (PostGIS) | Requires PostGIS extension |
| `ROWVERSION` / `TIMESTAMP` | no direct equivalent | Use `xmin` system column or `updated_at` trigger column |
| `IDENTITY(1,1)` | `SERIAL` or `GENERATED ALWAYS AS IDENTITY` | See section 2.2 below |

**Important type behavior differences:**

- **String comparisons:** PostgreSQL string comparisons are **case-sensitive** by default. `WHERE name = 'Smith'` will *not* match `'smith'`. SQL Server is case-insensitive by default (based on collation). Use `LOWER()` or the `ILIKE` operator for case-insensitive matching in PostgreSQL: `WHERE name ILIKE 'smith'`.
- **NULL comparisons:** Standard SQL — no difference. Both require `IS NULL` / `IS NOT NULL`.
- **Boolean literals:** PostgreSQL uses `TRUE`/`FALSE` or `'t'`/`'f'`. SQL Server uses `1`/`0` or the BIT type.
- **Date literals:** PostgreSQL prefers ISO 8601: `'2024-01-15'`. SQL Server accepts many formats; standardize on ISO 8601 in both.

<h3>2.2 – Auto-Increment Columns: IDENTITY vs. SERIAL vs. GENERATED</h3>

SQL Server's `IDENTITY(seed, increment)` column attribute has three PostgreSQL equivalents. Understanding all three is important because you will encounter all of them in real-world code. Note, the code below is for review, you will get errors if you run them since the data already exists. These statements are meant to illustrate a concept:

**Option 1: SERIAL / BIGSERIAL (traditional, pre-SQL-standard)**

```sql
-- SQL Server:
CREATE TABLE jobs (
    job_id   SMALLINT     IDENTITY(1,1) NOT NULL,
    job_desc VARCHAR(50)  NOT NULL
);

-- PostgreSQL (SERIAL shorthand):
CREATE TABLE jobs (
    job_id   SMALLSERIAL  NOT NULL,     -- expands to SMALLINT with a sequence
    job_desc VARCHAR(50)  NOT NULL
);
-- BIGSERIAL is the BIGINT version; SMALLSERIAL is the SMALLINT version
```

`SERIAL` is syntactic sugar that creates a sequence object and sets the column default to `nextval('jobs_job_id_seq')`. The sequence is named `<table>_<column>_seq` automatically.

**Option 2: GENERATED ALWAYS AS IDENTITY (SQL standard, preferred for new code - This is for Postgres)**

```sql
CREATE TABLE jobs (
    job_id   SMALLINT     GENERATED ALWAYS AS IDENTITY,
    job_desc VARCHAR(50)  NOT NULL
);

-- Or with explicit start/increment:
CREATE TABLE jobs (
    job_id   SMALLINT     GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1),
    job_desc VARCHAR(50)  NOT NULL
);
```

`GENERATED ALWAYS` prevents explicit inserts of the identity value. Use `GENERATED BY DEFAULT` if you need to override (e.g., during a migration).

**Sequences directly (equivalent to SQL Server's CREATE SEQUENCE):**

```sql
CREATE SEQUENCE job_id_seq START WITH 1 INCREMENT BY 1;

SELECT nextval('job_id_seq');      -- Get next value
SELECT currval('job_id_seq');      -- Current value in this session
SELECT setval('job_id_seq', 14);   -- Reset (e.g., after a bulk load)
```

SQL Server also supports `CREATE SEQUENCE` (since SQL Server 2012) — the syntax is nearly identical.

<h3>2.3 – Schema Design Differences</h3>

**Default schema:** In SQL Server, the default schema for a user is typically `dbo`. In PostgreSQL, the default schema is `public`. This difference matters in connection strings, ORMs, and migration scripts.

**Quoting identifiers:** PostgreSQL folds unquoted identifiers to lowercase (Authors becomes authors); SQL Server preserves the original case and compares case-insensitively by default.

**Computed columns:** SQL Server supports `AS (expression) PERSISTED` computed columns. PostgreSQL supports generated columns using a similar syntax:

```sql
-- SQL Server:
ALTER TABLE authors ADD full_name AS (au_fname + ' ' + au_lname) PERSISTED;

-- PostgreSQL (generated column, always stored):
ALTER TABLE authors ADD COLUMN full_name TEXT
    GENERATED ALWAYS AS (au_fname || ' ' || au_lname) STORED;
```

**CHECK, DEFAULT, and UNIQUE constraints:** Syntax is nearly identical in both systems. PRIMARY KEY and FOREIGN KEY syntax is the same.

**Temporary tables:** Both systems support temp tables. The syntax differs slightly:

```sql
-- SQL Server:
CREATE TABLE #temp_sales (stor_id CHAR(4), qty INT, amount DECIMAL(10,2));

-- PostgreSQL:
CREATE TEMP TABLE temp_sales (stor_id CHAR(4), qty INT, amount NUMERIC(10,2));
-- or:
CREATE TEMPORARY TABLE temp_sales (stor_id CHAR(4), qty INT, amount NUMERIC(10,2));
```

PostgreSQL temporary tables are session-scoped by default (same as SQL Server's `#` temp tables). There is no equivalent to SQL Server's `##` global temp tables.

<p style="border-bottom: 1px solid lightgrey;"></p>

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/point1.png"><b>Activity 2.1 – Create the Pubs Sample Schema in PostgreSQL</b></p>

<p><img style="margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/checkmark.png"><b>Description</b></p>

In this activity you will translate several SQL Server `CREATE TABLE` statements from the pubs sample database into PostgreSQL DDL, applying the type-mapping rules from section 2.1. You will then verify the schema in both psql and pgAdmin.

<p><img style="margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/checkmark.png"><b>Steps</b></p>

**Step 1 — Connect to the pubs database in psql:**

```bash
psql -U postgres -h localhost -d pubs
```

**Step 2 — Observe the `authors` table. Study the type translations:**
Hint: You can use the meta-command of `!` to call to the OS shell, and use this command to list the DDL used for the creation of an object: 

`\! pg_dump -U postgres -d pubs --schema-only -t authors --no-owner --no-privileges`

```sql
-- Original SQL Server DDL (from pubs):
-- CREATE TABLE [dbo].[authors](
--     [au_id]    [varchar](11)   NOT NULL,
--     [au_lname] [varchar](40)   NOT NULL,
--     [au_fname] [varchar](20)   NOT NULL,
--     [phone]    [char](12)      NOT NULL DEFAULT ('UNKNOWN'),
--     [address]  [varchar](40)   NULL,
--     [city]     [varchar](20)   NULL,
--     [state]    [char](2)       NULL,
--     [zip]      [char](5)       NULL,
--     [contract] [bit]           NOT NULL
-- );

-- PostgreSQL equivalent:
CREATE TABLE authors (
    au_id    VARCHAR(11)  NOT NULL
                 CONSTRAINT UPKCL_auidind PRIMARY KEY
                 CHECK (au_id ~ '^\d{3}-\d{2}-\d{4}$'),
    au_lname VARCHAR(40)  NOT NULL,
    au_fname VARCHAR(20)  NOT NULL,
    phone    CHAR(12)     NOT NULL DEFAULT 'UNKNOWN',
    address  VARCHAR(40)  NULL,
    city     VARCHAR(20)  NULL,
    state    CHAR(2)      NULL,
    zip      CHAR(5)      NULL
                 CHECK (zip ~ '^\d{5}$'),
    contract SMALLINT     NOT NULL    -- BIT → SMALLINT (0/1)
);
```

Note the key differences:
- `[varchar]` / `[char]` → `VARCHAR` / `CHAR` (PostgreSQL databases are typically created as UTF-8 (encoding is chosen per database), so no N-prefix is needed.)
- `[bit]` → `SMALLINT` (pubs uses 0/1 convention; alternatively use `BOOLEAN`)
- Square bracket quoting → no quoting needed (use snake_case)
- `CHECK` constraints using regex (`~`) replace the original T-SQL constraints

**Step 3 — Observe the `publishers` and `titles` tables with additional type mappings:**

```sql
CREATE TABLE publishers (
    pub_id   CHAR(4)      NOT NULL
                 CONSTRAINT UPKCL_pubind PRIMARY KEY
                 CHECK (pub_id IN ('1389','0736','0877','1622','1756')
                        OR pub_id LIKE '99%'),
    pub_name VARCHAR(40)  NULL,
    city     VARCHAR(20)  NULL,
    state    CHAR(2)      NULL,
    country  VARCHAR(30)  NULL DEFAULT 'USA'
);

CREATE TABLE titles (
    title_id  VARCHAR(6)      NOT NULL CONSTRAINT UPKCL_titleidind PRIMARY KEY,
    title     VARCHAR(80)     NOT NULL,
    type      CHAR(12)        NOT NULL DEFAULT 'UNDECIDED',
    pub_id    CHAR(4)         NULL REFERENCES publishers(pub_id),
    price     NUMERIC(10,4)   NULL,      -- was MONEY
    advance   NUMERIC(10,4)   NULL,      -- was MONEY
    royalty   INT             NULL,
    ytd_sales INT             NULL,
    notes     VARCHAR(200)    NULL,
    pubdate   TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP  -- was DATETIME / getdate()
);
```

Note how `MONEY` becomes `NUMERIC(10,4)` and `getdate()` becomes `CURRENT_TIMESTAMP`.

**Step 4 — Observe the `jobs` table using SMALLSERIAL (auto-increment):**

```sql
CREATE TABLE jobs (
    job_id   SMALLSERIAL  PRIMARY KEY,                                        -- was IDENTITY(1,1)
    job_desc VARCHAR(50)  NOT NULL DEFAULT 'New Position - title not formalized yet',
    min_lvl  SMALLINT     NOT NULL CHECK (min_lvl >= 10),                     -- was TINYINT
    max_lvl  SMALLINT     NOT NULL CHECK (max_lvl <= 250)                     -- was TINYINT
);
```

Note how `TINYINT` becomes `SMALLINT` (PostgreSQL has no 1-byte integer type).

**Step 5 — Observe the `employee` table with a foreign key and regex CHECK:**

```sql
CREATE TABLE employee (
    emp_id    VARCHAR(9)   NOT NULL CONSTRAINT PK_emp_id PRIMARY KEY
                               CHECK (emp_id ~ '^[A-Z]{3}[1-9][0-9]{4}[FM]$'
                                   OR emp_id ~ '^[A-Z]-[A-Z][1-9][0-9]{4}[FM]$'),
    fname     VARCHAR(20)  NOT NULL,
    minit     CHAR(1)      NULL,
    lname     VARCHAR(30)  NOT NULL,
    job_id    SMALLINT     NOT NULL DEFAULT 1 REFERENCES jobs(job_id),
    job_lvl   SMALLINT     NULL DEFAULT 10,                                   -- was TINYINT
    pub_id    CHAR(4)      NOT NULL DEFAULT '9952' REFERENCES publishers(pub_id),
    hire_date TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP                 -- was DATETIME / getdate()
);
```

**Step 6 — Observe the foreign key constraint between tables:**

```sql
ALTER TABLE titles
    ADD CONSTRAINT fk_titles_publishers
    FOREIGN KEY (pub_id)
    REFERENCES publishers (pub_id)
    ON DELETE SET NULL;
```

**Step 7 — Inspect the created objects:**

```sql
-- List tables (psql):
\dt public.*

-- Describe a table's columns and constraints:
\d titles
\d employee

-- Or using information_schema:
SELECT column_name, data_type, character_maximum_length,
       is_nullable, column_default
FROM information_schema.columns
WHERE table_schema = 'public'
  AND table_name   = 'titles'
ORDER BY ordinal_position;
```

**Step 8 — Insert test rows and verify defaults and constraints:**

```sql
-- Insert a publisher:
INSERT INTO publishers (pub_id, pub_name, city, state)
VALUES ('1389', 'Algodata Infosystems', 'Berkeley', 'CA');

-- Insert a title (price uses NUMERIC, pubdate defaults to now()):
INSERT INTO titles (title_id, title, type, pub_id, price, advance, royalty, ytd_sales)
VALUES ('BU1032', 'The Busy Executive''s Database Guide', 'business', '1389',
        19.99, 5000.00, 10, 4095);

-- Verify the inserted data:
SELECT title_id, title, type, price, pubdate
FROM titles;
-- pubdate should be automatically set to the current timestamp
```

<p style="border-bottom: 1px solid lightgrey;"></p>

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/point1.png"><b>Activity 2.2 – Compare Data Type Behavior: Case Sensitivity and Boolean</b></p>

<p><img style="margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/checkmark.png"><b>Steps</b></p>

**Step 1 — Demonstrate case sensitivity:**

```sql
-- Insert rows with mixed case last names:
INSERT INTO authors (au_id, au_lname, au_fname, phone, contract)
VALUES ('111-11-1111', 'Smith',  'John',  '415 000-0001', 1),
       ('222-22-2222', 'SMITH',  'Jane',  '415 000-0002', 1),
       ('333-33-3333', 'smith',  'Bob',   '415 000-0003', 1);

-- Case-sensitive match (PostgreSQL default):
SELECT au_fname, au_lname
FROM authors
WHERE au_lname = 'Smith';     -- Returns only 'Smith', NOT 'SMITH' or 'smith'

-- Case-insensitive with ILIKE (PostgreSQL-specific):
SELECT au_fname, au_lname
FROM authors
WHERE au_lname ILIKE 'smith';  -- Returns all three rows

-- Case-insensitive with LOWER():
SELECT au_fname, au_lname
FROM authors
WHERE LOWER(au_lname) = 'smith';  -- Returns all three rows

-- SQL Server equivalent of ILIKE:
-- WHERE au_lname = 'smith' COLLATE SQL_Latin1_General_CP1_CI_AS
```

**Step 2 — Demonstrate SMALLINT (BIT) vs. PostgreSQL BOOLEAN:**

```sql
-- pubs uses SMALLINT with 0/1 for the contract column (mirroring T-SQL BIT)
SELECT au_fname, au_lname, contract
FROM authors
WHERE contract = 1;    -- Under contract

SELECT au_fname, au_lname, contract
FROM authors
WHERE contract = 0;    -- Not under contract

-- If you prefer native PostgreSQL BOOLEAN semantics, you can cast:
SELECT au_fname, au_lname, contract::boolean
FROM authors
WHERE contract::boolean = TRUE;

-- In SQL Server you would write: WHERE contract = 1
-- PostgreSQL BOOLEAN short form (WHERE is_active) has no SQL Server equivalent,
-- but it is available if you convert the column type to BOOLEAN.
```

<p style="border-bottom: 1px solid lightgrey;"></p>

<p><img style="margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/owl.png"><b>For Further Study</b></p>

- [PostgreSQL Documentation — Data Types](https://www.postgresql.org/docs/current/datatype.html)
- [PostgreSQL Documentation — CREATE TABLE](https://www.postgresql.org/docs/current/sql-createtable.html)
- [PostgreSQL Documentation — Sequences](https://www.postgresql.org/docs/current/sql-createsequence.html)
- [PostgreSQL Documentation — Generated Columns](https://www.postgresql.org/docs/current/ddl-generated-columns.html)
- [EDB — SQL Server to PostgreSQL Type Mapping](https://www.enterprisedb.com/blog/microsoft-sql-server-mssql-vs-postgresql-comparison-details-what-differences)
- [AWS — Schema Conversion Tool Documentation](https://docs.aws.amazon.com/SchemaConversionTool/latest/userguide/CHAP_UserInterface.html)
- [Microsoft — SQL Server Data Types Reference](https://learn.microsoft.com/en-us/sql/t-sql/data-types/data-types-transact-sql)
- [PostgreSQL Documentation — Collation Support](https://www.postgresql.org/docs/current/collation.html)

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/geopin.png"><b>Next Steps</b></p>

Next, continue to <a href="03_-_TSQL_to_PL_pgSQL.md" target="_blank"><i>Module 03 – T-SQL to PL/pgSQL</i></a>.
