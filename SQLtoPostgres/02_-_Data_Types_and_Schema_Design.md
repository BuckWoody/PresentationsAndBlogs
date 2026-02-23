![](graphics/microsoftlogo.png)

# Workshop: PostgreSQL for the SQL Server Database Professional

#### <i>A Microsoft-style Course — SQL Server & PostgreSQL Track</i>

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
| `NCHAR(n)` | `CHAR(n)` | PostgreSQL is always UTF-8; no N-prefix needed |
| `NVARCHAR(n)` | `VARCHAR(n)` | PostgreSQL is always UTF-8 |
| `NVARCHAR(MAX)` | `TEXT` | PostgreSQL TEXT is always Unicode |
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

SQL Server's `IDENTITY(seed, increment)` column attribute has three PostgreSQL equivalents. Understanding all three is important because you will encounter all of them in real-world code:

**Option 1: SERIAL / BIGSERIAL (traditional, pre-SQL-standard)**

```sql
-- SQL Server:
CREATE TABLE orders (
    order_id   INT          IDENTITY(1,1) NOT NULL,
    order_date DATE         NOT NULL
);

-- PostgreSQL (SERIAL shorthand):
CREATE TABLE orders (
    order_id   SERIAL       NOT NULL,     -- expands to INT with a sequence
    order_date DATE         NOT NULL
);
-- BIGSERIAL is the BIGINT version; SMALLSERIAL is the SMALLINT version
```

`SERIAL` is syntactic sugar that creates a sequence object and sets the column default to `nextval('orders_order_id_seq')`. The sequence is named `<table>_<column>_seq` automatically.

**Option 2: GENERATED ALWAYS AS IDENTITY (SQL standard, preferred for new code)**

```sql
CREATE TABLE orders (
    order_id   INT          GENERATED ALWAYS AS IDENTITY,
    order_date DATE         NOT NULL
);

-- Or with explicit start/increment:
CREATE TABLE orders (
    order_id   INT          GENERATED ALWAYS AS IDENTITY (START WITH 1000 INCREMENT BY 1),
    order_date DATE         NOT NULL
);
```

`GENERATED ALWAYS` prevents explicit inserts of the identity value. Use `GENERATED BY DEFAULT` if you need to override (e.g., during a migration).

**Sequences directly (equivalent to SQL Server's CREATE SEQUENCE):**

```sql
CREATE SEQUENCE order_id_seq START WITH 1 INCREMENT BY 1;

SELECT nextval('order_id_seq');      -- Get next value
SELECT currval('order_id_seq');      -- Current value in this session
SELECT setval('order_id_seq', 1000); -- Reset (e.g., after a bulk load)
```

SQL Server also supports `CREATE SEQUENCE` (since SQL Server 2012) — the syntax is nearly identical.

<h3>2.3 – Schema Design Differences</h3>

**Default schema:** In SQL Server, the default schema for a user is typically `dbo`. In PostgreSQL, the default schema is `public`. This difference matters in connection strings, ORMs, and migration scripts.

**Quoting identifiers:** PostgreSQL treats unquoted identifiers as **lowercase**. This is the opposite of SQL Server, which is case-insensitive. If you create a table as `CREATE TABLE "Orders"`, you must always quote it: `SELECT * FROM "Orders"`. Best practice: use all-lowercase, snake_case names in PostgreSQL and avoid quoted identifiers.

**Computed columns:** SQL Server supports `AS (expression) PERSISTED` computed columns. PostgreSQL supports generated columns using a similar syntax:

```sql
-- SQL Server:
ALTER TABLE person ADD full_name AS (first_name + ' ' + last_name) PERSISTED;

-- PostgreSQL (generated column, always stored):
ALTER TABLE person ADD COLUMN full_name TEXT
    GENERATED ALWAYS AS (first_name || ' ' || last_name) STORED;
```

**CHECK, DEFAULT, and UNIQUE constraints:** Syntax is nearly identical in both systems. PRIMARY KEY and FOREIGN KEY syntax is the same.

**Temporary tables:** Both systems support temp tables. The syntax differs slightly:

```sql
-- SQL Server:
CREATE TABLE #temp_orders (order_id INT, amount DECIMAL(10,2));

-- PostgreSQL:
CREATE TEMP TABLE temp_orders (order_id INT, amount NUMERIC(10,2));
-- or:
CREATE TEMPORARY TABLE temp_orders (order_id INT, amount NUMERIC(10,2));
```

PostgreSQL temporary tables are session-scoped by default (same as SQL Server's `#` temp tables). There is no equivalent to SQL Server's `##` global temp tables.

<p style="border-bottom: 1px solid lightgrey;"></p>

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/point1.png"><b>Activity 2.1 – Create the AdventureWorks Sample Schema in PostgreSQL</b></p>

<p><img style="margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/checkmark.png"><b>Description</b></p>

In this activity you will translate several SQL Server `CREATE TABLE` statements from AdventureWorks into PostgreSQL DDL, applying the type-mapping rules from section 2.1. You will then verify the schema in both psql and pgAdmin.

<p><img style="margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/checkmark.png"><b>Steps</b></p>

**Step 1 — Connect to the adventureworks database in psql:**

```bash
psql -U postgres -h localhost -d adventureworks
```

**Step 2 — Create the `person.address` table. Study the type translations:**

```sql
-- Original SQL Server DDL (from AdventureWorks2022):
-- CREATE TABLE [Person].[Address](
--     [AddressID]    [int] IDENTITY(1,1) NOT NULL,
--     [AddressLine1] [nvarchar](60)      NOT NULL,
--     [AddressLine2] [nvarchar](60)      NULL,
--     [City]         [nvarchar](30)      NOT NULL,
--     [PostalCode]   [nvarchar](15)      NOT NULL,
--     [ModifiedDate] [datetime]          NOT NULL DEFAULT(getdate()),
--     [rowguid]      [uniqueidentifier]  NOT NULL DEFAULT(newid())
-- );

-- PostgreSQL equivalent:
CREATE TABLE person.address (
    address_id    INTEGER      GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    address_line1 VARCHAR(60)  NOT NULL,
    address_line2 VARCHAR(60)  NULL,
    city          VARCHAR(30)  NOT NULL,
    postal_code   VARCHAR(15)  NOT NULL,
    modified_date TIMESTAMP    NOT NULL DEFAULT now(),
    rowguid       UUID         NOT NULL DEFAULT gen_random_uuid()
);
```

Note the key differences:
- `[nvarchar]` → `VARCHAR` (PostgreSQL is always Unicode)
- `IDENTITY(1,1)` → `GENERATED ALWAYS AS IDENTITY`
- `getdate()` → `now()` or `CURRENT_TIMESTAMP`
- `newid()` → `gen_random_uuid()` (requires `pgcrypto` extension, or use `uuid-ossp`)
- Square bracket quoting → no quoting needed (use snake_case)

**Step 3 — Enable the uuid-ossp extension (if gen_random_uuid() is unavailable on your PostgreSQL version):**

```sql
-- gen_random_uuid() is built-in since PostgreSQL 13.
-- For older versions, enable this extension:
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
-- Then use uuid_generate_v4() instead of gen_random_uuid()
```

**Step 4 — Create more tables with additional type mappings:**

```sql
CREATE TABLE person.person (
    business_entity_id  INTEGER      GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    person_type         CHAR(2)      NOT NULL,
    first_name          VARCHAR(50)  NOT NULL,
    middle_name         VARCHAR(50)  NULL,
    last_name           VARCHAR(50)  NOT NULL,
    email_promotion     SMALLINT     NOT NULL DEFAULT 0,    -- was TINYINT
    is_active           BOOLEAN      NOT NULL DEFAULT TRUE, -- was BIT
    demographics        XML          NULL,
    modified_date       TIMESTAMP    NOT NULL DEFAULT now()
);

CREATE TABLE sales.currency (
    currency_code  CHAR(3)      NOT NULL PRIMARY KEY,   -- was NCHAR(3)
    name           VARCHAR(50)  NOT NULL,
    modified_date  TIMESTAMP    NOT NULL DEFAULT now()
);

CREATE TABLE sales.sales_order_header (
    sales_order_id          INTEGER          GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    order_date              TIMESTAMP        NOT NULL DEFAULT now(),
    ship_date               TIMESTAMP        NULL,
    status                  SMALLINT         NOT NULL DEFAULT 1,  -- was TINYINT
    online_order_flag       BOOLEAN          NOT NULL DEFAULT TRUE,
    sales_order_number      VARCHAR(25)      NOT NULL,
    customer_id             INTEGER          NOT NULL,
    ship_to_address_id      INTEGER          NULL,
    subtotal                NUMERIC(19,4)    NOT NULL DEFAULT 0.00,  -- was MONEY
    tax_amt                 NUMERIC(19,4)    NOT NULL DEFAULT 0.00,
    freight                 NUMERIC(19,4)    NOT NULL DEFAULT 0.00,
    total_due               NUMERIC(19,4)    GENERATED ALWAYS AS
                                (subtotal + tax_amt + freight) STORED,
    modified_date           TIMESTAMP        NOT NULL DEFAULT now()
);
```

Note how `MONEY` becomes `NUMERIC(19,4)` and `TINYINT` becomes `SMALLINT`. The computed column syntax (`total_due`) uses `GENERATED ALWAYS AS ... STORED`.

**Step 5 — Add a foreign key constraint:**

```sql
ALTER TABLE sales.sales_order_header
    ADD CONSTRAINT fk_soh_address
    FOREIGN KEY (ship_to_address_id)
    REFERENCES person.address (address_id)
    ON DELETE SET NULL;
```

**Step 6 — Inspect the created objects:**

```sql
-- List tables (psql):
\dt person.*
\dt sales.*

-- Describe a table's columns and constraints:
\d sales.sales_order_header

-- Or using information_schema:
SELECT column_name, data_type, character_maximum_length,
       is_nullable, column_default
FROM information_schema.columns
WHERE table_schema = 'sales'
  AND table_name   = 'sales_order_header'
ORDER BY ordinal_position;
```

**Step 7 — Insert a test row and verify the generated column:**

```sql
INSERT INTO person.address (address_line1, city, postal_code)
VALUES ('123 Main St', 'Seattle', '98101');

INSERT INTO sales.sales_order_header
    (sales_order_number, customer_id, subtotal, tax_amt, freight)
VALUES ('SO-0001', 1, 100.00, 10.00, 5.00);

SELECT sales_order_id, subtotal, tax_amt, freight, total_due
FROM sales.sales_order_header;
-- total_due should be 115.00, computed automatically
```

<p style="border-bottom: 1px solid lightgrey;"></p>

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/point1.png"><b>Activity 2.2 – Compare Data Type Behavior: Case Sensitivity and Boolean</b></p>

<p><img style="margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/checkmark.png"><b>Steps</b></p>

**Step 1 — Demonstrate case sensitivity:**

```sql
-- Insert rows with mixed case names:
INSERT INTO person.person (person_type, first_name, last_name)
VALUES ('IN', 'John',  'Smith'),
       ('IN', 'JOHN',  'SMITH'),
       ('IN', 'john',  'smith');

-- Case-sensitive match (PostgreSQL default):
SELECT first_name, last_name
FROM person.person
WHERE first_name = 'John';     -- Returns only 'John', NOT 'JOHN' or 'john'

-- Case-insensitive with ILIKE (PostgreSQL-specific):
SELECT first_name, last_name
FROM person.person
WHERE first_name ILIKE 'john';  -- Returns all three rows

-- Case-insensitive with LOWER():
SELECT first_name, last_name
FROM person.person
WHERE LOWER(first_name) = 'john';  -- Returns all three rows

-- SQL Server equivalent of ILIKE:
-- WHERE first_name = 'john' COLLATE SQL_Latin1_General_CP1_CI_AS
```

**Step 2 — Demonstrate Boolean vs. BIT:**

```sql
-- PostgreSQL BOOLEAN accepts TRUE/FALSE, 'true'/'false', 't'/'f', 1/0
SELECT is_active FROM person.person WHERE is_active = TRUE;
SELECT is_active FROM person.person WHERE is_active = 'true';
SELECT is_active FROM person.person WHERE is_active;   -- Short form works!
SELECT is_active FROM person.person WHERE NOT is_active;

-- In SQL Server you would write: WHERE is_active = 1
-- The PostgreSQL short form (WHERE is_active) has no SQL Server equivalent
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
