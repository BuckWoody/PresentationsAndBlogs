![](graphics/microsoftlogo.png)

# Workshop: PostgreSQL for the SQL Server Database Professional

#### <i>A SQL Server to PostgreSQL Skilling</i>


<p style="border-bottom: 1px solid lightgrey;"></p>

<img style="float: left; margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/textbubble.png"> <h2>Module 03 – T-SQL to PL/pgSQL</h2>

*Estimated Time: 60 minutes (≈20 minutes lecture, ≈40 minutes hands-on)*

This module is the practical heart of the workshop for developers. You will work through the most common T-SQL constructs and their PL/pgSQL (and standard SQL) equivalents — from basic `SELECT` differences through stored functions, procedures, error handling, and anonymous blocks.

<p style="border-bottom: 1px solid lightgrey;"></p>

<h2><img style="float: left; margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/pencil2.png">3.1 – SELECT Statement Differences</h2>

Most of your `SELECT` queries will work with minor modifications. The table below covers the most common translation points:

| T-SQL Pattern | PostgreSQL Equivalent | Notes |
|---|---|---|
| `SELECT TOP 10 * FROM t` | `SELECT * FROM t LIMIT 10` | PostgreSQL uses standard SQL LIMIT/OFFSET |
| `SELECT TOP 10 PERCENT * FROM t` | `SELECT * FROM t LIMIT (SELECT CEIL(COUNT(*)*0.1) FROM t)` | No direct PERCENT equivalent; use a subquery |
| `SELECT * FROM t WITH (NOLOCK)` | `SELECT * FROM t` | MVCC means dirty reads are impossible; no NOLOCK needed |
| `ISNULL(col, 0)` | `COALESCE(col, 0)` | COALESCE is standard SQL and works in both |
| `NULLIF(a, b)` | `NULLIF(a, b)` | Identical in both |
| `col1 + col2` (string concat) | `col1 \|\| col2` | PostgreSQL uses `\|\|` for string concatenation |
| `GETDATE()` | `NOW()` or `CURRENT_TIMESTAMP` | |
| `GETUTCDATE()` | `NOW() AT TIME ZONE 'UTC'` or `CURRENT_TIMESTAMP AT TIME ZONE 'UTC'` | |
| `CONVERT(VARCHAR, col, 101)` | `TO_CHAR(col, 'MM/DD/YYYY')` | |
| `CAST(col AS VARCHAR(10))` | `CAST(col AS VARCHAR(10))` or `col::VARCHAR(10)` | PostgreSQL `::` cast operator is very common |
| `LEN(col)` | `LENGTH(col)` | |
| `SUBSTRING(col, 1, 5)` | `SUBSTRING(col FROM 1 FOR 5)` or `SUBSTR(col, 1, 5)` | |
| `CHARINDEX('x', col)` | `POSITION('x' IN col)` or `STRPOS(col, 'x')` | |
| `STUFF(col, 1, 3, 'abc')` | `OVERLAY(col PLACING 'abc' FROM 1 FOR 3)` | |
| `REPLICATE('x', 5)` | `REPEAT('x', 5)` | |
| `LTRIM(RTRIM(col))` | `TRIM(col)` or `BTRIM(col)` | PostgreSQL TRIM removes both ends |
| `DATEDIFF(day, d1, d2)` | `d2::DATE - d1::DATE` or `EXTRACT(DAY FROM (d2-d1))` | *Note: If d1/d2 are timestamps, d2 - d1 yields an interval, and EXTRACT(DAY FROM interval) returns only the days field of the normalized interval — e.g. EXTRACT(DAY FROM (TIMESTAMP '2024-03-01' - TIMESTAMP '2024-01-01')) = 0, not 60, because the interval is normalised to 2 mons. (DATEDIFF(day,…) would return 60.)
If d1/d2 are dates, d2 - d1 is already an integer count of days, so wrapping it in EXTRACT(DAY FROM …) is wrong (EXTRACT does not take an integer).
The first alternative, d2::DATE - d1::DATE, is correct (returns integer days).* |
| `DATEADD(day, 7, d)` | `d + INTERVAL '7 days'` | |
| `YEAR(d)` / `MONTH(d)` / `DAY(d)` | `EXTRACT(YEAR FROM d)` / `EXTRACT(MONTH FROM d)` / `EXTRACT(DAY FROM d)` | |
| `FORMAT(n, 'N2')` | `TO_CHAR(n, 'FM999,999.00')` | |
| `NEWID()` | `gen_random_uuid()` | |
| `@@IDENTITY` / `SCOPE_IDENTITY()` | `RETURNING id` clause or `currval()` | See section 3.2 below |
| `PRINT 'message'` | `RAISE NOTICE 'message'` | |
| `BEGIN TRAN / COMMIT / ROLLBACK` | `BEGIN / COMMIT / ROLLBACK` | |

**String concatenation is a common gotcha.** SQL Server uses `+` for strings; PostgreSQL uses `||`. However, the `CONCAT()` function works in both and is null-safe:

```sql
-- SQL Server:
SELECT au_fname + ' ' + au_lname AS full_name FROM authors;

-- PostgreSQL (using ||):
SELECT au_fname || ' ' || au_lname AS full_name FROM authors;

-- PostgreSQL (using CONCAT — null-safe, works in both systems):
SELECT CONCAT(au_fname, ' ', au_lname) AS full_name FROM authors;
```

**Getting the last inserted identity value** is handled very differently in PostgreSQL:

```sql
-- SQL Server:
INSERT INTO jobs (job_desc, min_lvl, max_lvl) VALUES ('Data Engineer', 50, 150);
SELECT SCOPE_IDENTITY();

-- PostgreSQL Option 1: RETURNING clause (preferred — atomic with the INSERT):
INSERT INTO jobs (job_desc, min_lvl, max_lvl) VALUES ('Data Engineer', 50, 150)
RETURNING job_id;

-- PostgreSQL Option 2: currval() (requires sequence name, session-specific):
INSERT INTO jobs (job_desc, min_lvl, max_lvl) VALUES ('Data Engineer', 50, 150);
SELECT currval(pg_get_serial_sequence('jobs', 'job_id'));
```

The `RETURNING` clause is the PostgreSQL best practice. It is safer than `SCOPE_IDENTITY()` because it returns the value atomically with the insert and works correctly in multi-row inserts.

<h3>3.2 – Date and Time Arithmetic</h3>

PostgreSQL date arithmetic is more expressive than T-SQL but uses different syntax:

```sql
-- Days between two dates:
SELECT '2024-12-31'::DATE - '2024-01-01'::DATE;     -- Returns integer 365
-- T-SQL: SELECT DATEDIFF(day, '2024-01-01', '2024-12-31')

-- Add an interval:
SELECT NOW() + INTERVAL '7 days';
SELECT NOW() + INTERVAL '1 month 15 days 3 hours';
-- T-SQL: SELECT DATEADD(day, 7, GETDATE())

-- Extract components:
SELECT EXTRACT(YEAR  FROM NOW()),
       EXTRACT(MONTH FROM NOW()),
       EXTRACT(DOW   FROM NOW()),    -- Day of week: 0=Sunday
       EXTRACT(EPOCH FROM NOW());    -- Seconds since Unix epoch

-- Truncate to beginning of period (like SQL Server DATETRUNC, added in 2022):
SELECT DATE_TRUNC('month', NOW());   -- First day of current month at midnight
SELECT DATE_TRUNC('year',  NOW());   -- Jan 1 of current year at midnight

-- Age between two dates (returns interval):
SELECT AGE('2024-12-31'::DATE, '1990-06-15'::DATE);
```

<h3>3.3 – CTEs and Window Functions</h3>

CTEs (`WITH` clauses) and window functions work in both systems. The syntax is mostly identical. The key differences:

- PostgreSQL CTEs are **optimization fences** by default (evaluated once, independently of the outer query). Since PostgreSQL 12, you can add `WITH ... AS (NOT MATERIALIZED ...)` to allow the planner to inline the CTE. SQL Server inlines CTEs by default.
- PostgreSQL supports **`FILTER (WHERE ...)`** in aggregate window functions, which has no T-SQL equivalent.
- PostgreSQL supports **recursive CTEs** using `WITH RECURSIVE` (SQL Server uses `WITH` and the recursion is implied by the self-reference).

```sql
-- Recursive CTE (almost identical syntax):
-- SQL Server:
WITH job_hierarchy AS (
    SELECT job_id, job_desc, min_lvl, 1 AS level
    FROM jobs WHERE min_lvl = 10
    UNION ALL
    SELECT j.job_id, j.job_desc, j.min_lvl, h.level + 1
    FROM jobs j
    JOIN job_hierarchy h ON j.min_lvl = h.min_lvl + 50
)
SELECT * FROM job_hierarchy;

-- PostgreSQL (add RECURSIVE keyword):
WITH RECURSIVE job_hierarchy AS (
    SELECT job_id, job_desc, min_lvl, 1 AS level
    FROM jobs WHERE min_lvl = 10
    UNION ALL
    SELECT j.job_id, j.job_desc, j.min_lvl, h.level + 1
    FROM jobs j
    JOIN job_hierarchy h ON j.min_lvl = h.min_lvl + 50
)
SELECT * FROM job_hierarchy;
```

<p style="border-bottom: 1px solid lightgrey;"></p>

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/point1.png"><b>Activity 3.1 – Translate Common T-SQL Queries to PostgreSQL</b></p>

<p><img style="margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/checkmark.png"><b>Steps</b></p>

Open psql or pgAdmin Query Tool connected to the `pubs` database and run each pair of queries. Observe the syntax differences.

**Step 1 — Connect to pubs and verify sample data:**

```sql
-- Confirm the authors table is populated:
SELECT au_id, au_fname, au_lname, city, state, contract
FROM authors
ORDER BY au_lname;

-- Confirm the titles table is populated:
SELECT title_id, title, type, pub_id, price, ytd_sales
FROM titles
ORDER BY title;
```

**Step 2 — TOP vs. LIMIT:**

```sql
-- T-SQL equivalent:
-- SELECT TOP 3 au_fname, au_lname FROM authors ORDER BY au_lname;

-- PostgreSQL:
SELECT au_fname, au_lname
FROM authors
ORDER BY au_lname
LIMIT 3;

-- OFFSET (paging) — no T-SQL equivalent without ROW_NUMBER workaround:
SELECT au_fname, au_lname
FROM authors
ORDER BY au_lname
LIMIT 3 OFFSET 3;   -- Rows 4-6 (second page)
```

**Step 3 — String concatenation, COALESCE, and casting:**

```sql
-- Build a display name with concatenation:
SELECT au_fname || ' ' || au_lname          AS full_name_pipe,
       CONCAT(au_fname, ' ', au_lname)      AS full_name_concat,
       COALESCE(address, '(no address)')    AS address_or_none,
       contract::TEXT                       AS contract_as_text,
       (contract = 1)                       AS contract_as_bool
FROM authors;
```

**Step 4 — Date functions:**

```sql
-- Use the titles pubdate column for date arithmetic:
SELECT title,
       pubdate,
       pubdate::DATE                                  AS pub_date_only,
       (CURRENT_DATE - pubdate::DATE)                AS days_since_pub,
       EXTRACT(YEAR  FROM pubdate)                   AS pub_year,
       EXTRACT(MONTH FROM pubdate)                   AS pub_month,
       DATE_TRUNC('month', pubdate)                  AS month_start,
       pubdate + INTERVAL '365 days'                 AS one_year_after_pub
FROM titles
WHERE pubdate IS NOT NULL;
```

**Step 5 — RETURNING clause (getting inserted ID):**

```sql
-- Insert a new job and get the generated job_id back atomically:
INSERT INTO jobs (job_desc, min_lvl, max_lvl)
VALUES ('Database Administrator', 100, 200)
RETURNING job_id, job_desc;

-- Multi-row insert with RETURNING:
INSERT INTO jobs (job_desc, min_lvl, max_lvl)
VALUES
    ('Data Engineer',   75, 175),
    ('Analytics Lead', 100, 200)
RETURNING job_id, job_desc, min_lvl, max_lvl;
```

**Step 6 — Window functions with FILTER:**

```sql
-- Standard window functions (identical to T-SQL):
SELECT au_fname,
       au_lname,
       state,
       contract,
       ROW_NUMBER()  OVER (ORDER BY au_lname, au_fname)          AS row_num,
       RANK()        OVER (PARTITION BY state ORDER BY au_lname)  AS rank_in_state,
       COUNT(*)      OVER (PARTITION BY state)                    AS authors_in_state,
       SUM(contract) OVER (ORDER BY au_lname ROWS UNBOUNDED PRECEDING) AS running_contracted
FROM authors;

-- FILTER clause on aggregates (PostgreSQL-specific, no T-SQL equivalent):
SELECT
    COUNT(*)                                      AS total_authors,
    COUNT(*) FILTER (WHERE contract = 1)          AS under_contract,
    COUNT(*) FILTER (WHERE contract = 0)          AS no_contract,
    COUNT(*) FILTER (WHERE state = 'CA')          AS california_authors
FROM authors;
```

<p style="border-bottom: 1px solid lightgrey;"></p>

<h2><img style="float: left; margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/pencil2.png">3.4 – PL/pgSQL: Stored Procedures and Functions</h2>

PostgreSQL's procedural language is **PL/pgSQL**. It is similar in spirit to T-SQL but has different syntax and some important semantic differences.

**Key structural differences:**

| Concept | T-SQL | PL/pgSQL |
|---|---|---|
| Declare local variable | `DECLARE @var INT = 0;` | `DECLARE var INT := 0;` |
| Assign to variable | `SET @var = 5` or `SELECT @var = col FROM ...` | `var := 5;` or `SELECT col INTO var FROM ...` |
| Print/debug output | `PRINT 'msg'` | `RAISE NOTICE 'msg: %', value;` |
| IF/ELSE | `IF ... BEGIN ... END ELSE ...` | `IF ... THEN ... ELSE ... END IF;` |
| WHILE loop | `WHILE condition BEGIN ... END` | `WHILE condition LOOP ... END LOOP;` |
| FOR loop (integer) | `DECLARE @i INT = 1; WHILE @i <= 10 BEGIN SET @i += 1 END` | `FOR i IN 1..10 LOOP ... END LOOP;` |
| FOR loop (cursor) | Explicit cursor DECLARE/OPEN/FETCH | `FOR row IN SELECT ... LOOP ... END LOOP;` |
| Return a result set | `SELECT ... FROM ...` inside SP | Use `RETURNS SETOF` function or `RETURNS TABLE` |
| Error handling | `BEGIN TRY ... END TRY BEGIN CATCH ... END CATCH` | `BEGIN ... EXCEPTION WHEN ... THEN ... END;` |
| Raise an error | `RAISERROR('msg', 16, 1)` or `THROW` | `RAISE EXCEPTION 'msg';` |
| Check rows affected | `@@ROWCOUNT` | `GET DIAGNOSTICS row_count = ROW_COUNT;` |
| Stored procedure | `CREATE PROCEDURE` | `CREATE PROCEDURE` (PostgreSQL 11+) or `CREATE FUNCTION` |
| Function returning scalar | `CREATE FUNCTION ... RETURNS INT` | `CREATE FUNCTION ... RETURNS INT` |
| Anonymous block | Not supported (use ad-hoc T-SQL) | `DO $$ ... $$;` |

**PL/pgSQL function structure:**

```sql
-- SQL Server equivalent:
-- CREATE PROCEDURE dbo.usp_get_author_sales_total
--     @au_id    VARCHAR(11),
--     @total    MONEY OUTPUT
-- AS BEGIN
--     SELECT @total = SUM(t.price * s.qty)
--     FROM titleauthor ta
--     JOIN titles t  ON t.title_id = ta.title_id
--     JOIN sales  s  ON s.title_id = ta.title_id
--     WHERE ta.au_id = @au_id;
-- END;

-- PostgreSQL FUNCTION (for scalar returns):
CREATE OR REPLACE FUNCTION get_author_sales_total(p_au_id VARCHAR(11))
RETURNS NUMERIC(10,4)
LANGUAGE plpgsql
AS $$
DECLARE
    v_total NUMERIC(10,4);
BEGIN
    SELECT COALESCE(SUM(t.price * s.qty), 0)
    INTO   v_total
    FROM   titleauthor ta
    JOIN   titles t ON t.title_id = ta.title_id
    JOIN   sales  s ON s.title_id = ta.title_id
    WHERE  ta.au_id = p_au_id;

    RETURN v_total;
END;
$$;

-- Call it:
SELECT get_author_sales_total('409-56-7008');
```

**Important:** In PostgreSQL, stored procedures (`CREATE PROCEDURE`) cannot return result sets in the same way SQL Server procedures can. To return a result set, you write a **function** using `RETURNS TABLE(...)` or `RETURNS SETOF record`. Procedures are used for transactions and side effects; functions are used for returning data.

```sql
-- Function returning a table (equivalent to a SQL Server SP that does SELECT):
CREATE OR REPLACE FUNCTION get_titles_for_author(p_au_id VARCHAR(11))
RETURNS TABLE (
    title_id   VARCHAR(6),
    title      VARCHAR(80),
    type       CHAR(12),
    price      NUMERIC(10,4),
    ytd_sales  INT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT t.title_id,
           t.title,
           t.type,
           t.price,
           t.ytd_sales
    FROM   titles t
    JOIN   titleauthor ta ON ta.title_id = t.title_id
    WHERE  ta.au_id = p_au_id
    ORDER BY t.title;
END;
$$;

-- Call like a table:
SELECT * FROM get_titles_for_author('409-56-7008');
```

**Error handling:**

```sql
CREATE OR REPLACE FUNCTION safe_insert_title(
    p_title_id    VARCHAR(6),
    p_title       VARCHAR(80),
    p_type        CHAR(12),
    p_pub_id      CHAR(4),
    p_price       NUMERIC(10,4)
)
RETURNS VARCHAR(6)
LANGUAGE plpgsql
AS $$
DECLARE
    v_new_id  VARCHAR(6);
BEGIN
    INSERT INTO titles (title_id, title, type, pub_id, price)
    VALUES (p_title_id, p_title, p_type, p_pub_id, p_price)
    RETURNING title_id INTO v_new_id;

    RETURN v_new_id;

EXCEPTION
    WHEN unique_violation THEN
        RAISE NOTICE 'Title ID % already exists', p_title_id;
        RETURN NULL;
    WHEN foreign_key_violation THEN
        RAISE EXCEPTION 'Publisher ID % does not exist', p_pub_id;
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Unexpected error: %', SQLERRM;
END;
$$;
```

**DO blocks (anonymous PL/pgSQL — equivalent to ad-hoc T-SQL scripts with variables):**

```sql
-- SQL Server ad-hoc:
-- DECLARE @counter INT = 0;
-- WHILE @counter < 5 BEGIN
--     PRINT 'Row ' + CAST(@counter AS VARCHAR);
--     SET @counter = @counter + 1;
-- END;

-- PostgreSQL DO block:
DO $$
DECLARE
    v_counter INTEGER := 0;
BEGIN
    WHILE v_counter < 5 LOOP
        RAISE NOTICE 'Row %', v_counter;
        v_counter := v_counter + 1;
    END LOOP;
END;
$$;
```

<p style="border-bottom: 1px solid lightgrey;"></p>

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/point1.png"><b>Activity 3.2 – Write PL/pgSQL Functions and Procedures</b></p>

<p><img style="margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/checkmark.png"><b>Steps</b></p>

**Step 1 — Create and call the scalar function:**

```sql
-- Create the function from section 3.4:
CREATE OR REPLACE FUNCTION get_author_sales_total(p_au_id VARCHAR(11))
RETURNS NUMERIC(10,4)
LANGUAGE plpgsql
AS $$
DECLARE
    v_total NUMERIC(10,4);
BEGIN
    SELECT COALESCE(SUM(t.price * s.qty), 0)
    INTO   v_total
    FROM   titleauthor ta
    JOIN   titles t ON t.title_id = ta.title_id
    JOIN   sales  s ON s.title_id = ta.title_id
    WHERE  ta.au_id = p_au_id;
    RETURN v_total;
END;
$$;

-- Call with an existing author:
SELECT get_author_sales_total('409-56-7008');
SELECT get_author_sales_total('999-99-9999');   -- Author that doesn't exist — returns 0 due to COALESCE
```

**Step 2 — Create the table-returning function:**

```sql
CREATE OR REPLACE FUNCTION get_titles_for_author(p_au_id VARCHAR(11))
RETURNS TABLE (
    title_id   VARCHAR(6),
    title      VARCHAR(80),
    type       CHAR(12),
    price      NUMERIC(10,4),
    ytd_sales  INT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT t.title_id,
           t.title,
           t.type,
           t.price,
           t.ytd_sales
    FROM   titles t
    JOIN   titleauthor ta ON ta.title_id = t.title_id
    WHERE  ta.au_id = p_au_id
    ORDER BY t.title;
END;
$$;

SELECT * FROM get_titles_for_author('409-56-7008');
SELECT * FROM get_titles_for_author('267-41-2394');
```

**Step 3 — Create a PostgreSQL PROCEDURE with transaction control:**

```sql
-- Procedures in PostgreSQL (11+) support COMMIT/ROLLBACK inside them
-- This is something SQL Server procedures also support
CREATE OR REPLACE PROCEDURE transfer_title_to_publisher(
    p_title_id      VARCHAR(6),
    p_source_pub    CHAR(4),
    p_target_pub    CHAR(4)
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Update the publisher on the title
    UPDATE titles
    SET    pub_id = p_target_pub
    WHERE  title_id = p_title_id
      AND  pub_id   = p_source_pub;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Title % not found for publisher %', p_title_id, p_source_pub;
    END IF;

    RAISE NOTICE 'Title % transferred from publisher % to publisher %',
        p_title_id, p_source_pub, p_target_pub;
END;
$$;

-- Call a procedure with CALL (not SELECT!):
CALL transfer_title_to_publisher('BU1032', '1389', '0736');
```

**Step 4 — Use a DO block for a one-time data migration task:**

```sql
-- Equivalent to an ad-hoc T-SQL migration script
DO $$
DECLARE
    v_rec     RECORD;
    v_count   INTEGER := 0;
BEGIN
    -- Standardize title types: set any UNDECIDED type to 'UNASSIGNED'
    -- and report which titles were updated
    FOR v_rec IN
        SELECT title_id, title, type
        FROM titles
        WHERE TRIM(type) = 'UNDECIDED'
    LOOP
        UPDATE titles
        SET    type = 'UNASSIGNED  '   -- CHAR(12), pad to length
        WHERE  title_id = v_rec.title_id;
        v_count := v_count + 1;
    END LOOP;

    RAISE NOTICE 'Standardized % title records', v_count;
END;
$$;
```

**Step 5 — List all functions in the public schema (equivalent to sys.procedures in SQL Server):**

```sql
SELECT routine_name, routine_type, data_type
FROM information_schema.routines
WHERE routine_schema = 'public'
ORDER BY routine_name;

-- Or using pg_proc for more details:
SELECT p.proname   AS function_name,
       pg_get_function_result(p.oid) AS return_type,
       l.lanname   AS language
FROM pg_proc p
JOIN pg_namespace n ON n.oid = p.pronamespace
JOIN pg_language  l ON l.oid = p.prolang
WHERE n.nspname = 'public'
ORDER BY p.proname;
```

<p style="border-bottom: 1px solid lightgrey;"></p>

<p><img style="margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/owl.png"><b>For Further Study</b></p>

- [PostgreSQL Documentation — PL/pgSQL](https://www.postgresql.org/docs/current/plpgsql.html)
- [PostgreSQL Documentation — SQL Functions](https://www.postgresql.org/docs/current/sql-createfunction.html)
- [PostgreSQL Documentation — Stored Procedures](https://www.postgresql.org/docs/current/sql-createprocedure.html)
- [PostgreSQL Documentation — RETURNING Clause](https://www.postgresql.org/docs/current/dml-returning.html)
- [PostgreSQL Documentation — String Functions](https://www.postgresql.org/docs/current/functions-string.html)
- [PostgreSQL Documentation — Date/Time Functions](https://www.postgresql.org/docs/current/functions-datetime.html)
- [PostgreSQL Documentation — Window Functions](https://www.postgresql.org/docs/current/tutorial-window.html)
- [PostgreSQL Documentation — Error Codes](https://www.postgresql.org/docs/current/errcodes-appendix.html)
- [PostgreSQL by Example](https://github.com/boringcollege/postgres-by-example)

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/geopin.png"><b>Next Steps</b></p>

Next, continue to <a href="04_-_Indexes_and_Performance.md" target="_blank"><i>Module 04 – Indexes and Performance</i></a>.
