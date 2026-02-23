![](graphics/microsoftlogo.png)

# Workshop: PostgreSQL for the SQL Server Database Professional

#### <i>A Microsoft-style Course — SQL Server & PostgreSQL Track</i>

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
| `DATEDIFF(day, d1, d2)` | `d2::DATE - d1::DATE` or `EXTRACT(DAY FROM (d2-d1))` | See date arithmetic below |
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
SELECT first_name + ' ' + last_name AS full_name FROM person.person;

-- PostgreSQL (using ||):
SELECT first_name || ' ' || last_name AS full_name FROM person.person;

-- PostgreSQL (using CONCAT — null-safe, works in both systems):
SELECT CONCAT(first_name, ' ', last_name) AS full_name FROM person.person;
```

**Getting the last inserted identity value** is handled very differently in PostgreSQL:

```sql
-- SQL Server:
INSERT INTO orders (customer_id) VALUES (42);
SELECT SCOPE_IDENTITY();

-- PostgreSQL Option 1: RETURNING clause (preferred — atomic with the INSERT):
INSERT INTO orders (customer_id) VALUES (42)
RETURNING order_id;

-- PostgreSQL Option 2: currval() (requires sequence name, session-specific):
INSERT INTO orders (customer_id) VALUES (42);
SELECT currval(pg_get_serial_sequence('orders', 'order_id'));
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
WITH org_hierarchy AS (
    SELECT employee_id, manager_id, 1 AS level
    FROM employees WHERE manager_id IS NULL
    UNION ALL
    SELECT e.employee_id, e.manager_id, h.level + 1
    FROM employees e
    JOIN org_hierarchy h ON e.manager_id = h.employee_id
)
SELECT * FROM org_hierarchy;

-- PostgreSQL (add RECURSIVE keyword):
WITH RECURSIVE org_hierarchy AS (
    SELECT employee_id, manager_id, 1 AS level
    FROM employees WHERE manager_id IS NULL
    UNION ALL
    SELECT e.employee_id, e.manager_id, h.level + 1
    FROM employees e
    JOIN org_hierarchy h ON e.manager_id = h.employee_id
)
SELECT * FROM org_hierarchy;
```

<p style="border-bottom: 1px solid lightgrey;"></p>

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/point1.png"><b>Activity 3.1 – Translate Common T-SQL Queries to PostgreSQL</b></p>

<p><img style="margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/checkmark.png"><b>Steps</b></p>

Open psql or pgAdmin Query Tool connected to the `adventureworks` database and run each pair of queries. Observe the syntax differences.

**Step 1 — Connect to adventureworks and load sample data:**

```sql
-- Insert sample data for exercises (if not already present):
INSERT INTO person.person (person_type, first_name, last_name, email_promotion)
VALUES
    ('IN', 'Kim',     'Abercrombie',  0),
    ('IN', 'Hazem',   'Abolrous',     1),
    ('IN', 'Pilar',   'Ackerman',     2),
    ('IN', 'Frances', 'Adams',        0),
    ('IN', 'Margaret','Smith',        1),
    ('IN', 'Carla',   'Adams',        2);
```

**Step 2 — TOP vs. LIMIT:**

```sql
-- T-SQL equivalent:
-- SELECT TOP 3 first_name, last_name FROM person.person ORDER BY last_name;

-- PostgreSQL:
SELECT first_name, last_name
FROM person.person
ORDER BY last_name
LIMIT 3;

-- OFFSET (paging) — no T-SQL equivalent without ROW_NUMBER workaround:
SELECT first_name, last_name
FROM person.person
ORDER BY last_name
LIMIT 3 OFFSET 3;   -- Rows 4-6 (second page)
```

**Step 3 — String concatenation, COALESCE, and casting:**

```sql
-- Build a display name with concatenation:
SELECT first_name || ' ' || last_name       AS full_name_pipe,
       CONCAT(first_name, ' ', last_name)   AS full_name_concat,
       COALESCE(middle_name, '(none)')       AS middle_or_none,
       email_promotion::TEXT                AS promo_as_text,
       email_promotion::BOOLEAN             AS promo_as_bool
FROM person.person;
```

**Step 4 — Date functions:**

```sql
-- Insert a test order to work with dates:
INSERT INTO sales.sales_order_header
    (sales_order_number, customer_id, order_date, ship_date, subtotal, tax_amt, freight)
VALUES
    ('SO-0010', 1, '2024-01-15 09:00:00', '2024-01-22 14:00:00', 500.00, 50.00, 15.00),
    ('SO-0011', 2, '2024-03-01 11:00:00', '2024-03-08 10:00:00', 750.00, 75.00, 20.00);

-- Date arithmetic and extraction:
SELECT sales_order_number,
       order_date,
       ship_date,
       (ship_date::DATE - order_date::DATE)  AS days_to_ship,
       EXTRACT(YEAR  FROM order_date)        AS order_year,
       EXTRACT(MONTH FROM order_date)        AS order_month,
       DATE_TRUNC('month', order_date)       AS month_start,
       order_date + INTERVAL '30 days'       AS payment_due
FROM sales.sales_order_header;
```

**Step 5 — RETURNING clause (getting inserted ID):**

```sql
-- Insert and get the generated ID back atomically:
INSERT INTO person.address (address_line1, city, postal_code)
VALUES ('456 Oak Ave', 'Portland', '97201')
RETURNING address_id, address_line1, city;

-- Multi-row insert with RETURNING:
INSERT INTO person.person (person_type, first_name, last_name)
VALUES
    ('SP', 'Alex',  'Johnson'),
    ('SP', 'Maria', 'Garcia')
RETURNING business_entity_id, first_name, last_name;
```

**Step 6 — Window functions with FILTER:**

```sql
-- Standard window functions (identical to T-SQL):
SELECT first_name,
       last_name,
       email_promotion,
       ROW_NUMBER()    OVER (ORDER BY last_name, first_name)                AS row_num,
       RANK()          OVER (PARTITION BY email_promotion ORDER BY last_name) AS rank_in_group,
       COUNT(*)        OVER (PARTITION BY email_promotion)                  AS group_count,
       SUM(email_promotion) OVER (ORDER BY last_name ROWS UNBOUNDED PRECEDING) AS running_sum
FROM person.person;

-- FILTER clause on aggregates (PostgreSQL-specific, no T-SQL equivalent):
SELECT
    COUNT(*)                                      AS total_people,
    COUNT(*) FILTER (WHERE email_promotion = 0)   AS no_promo,
    COUNT(*) FILTER (WHERE email_promotion > 0)   AS some_promo,
    AVG(email_promotion)                          AS avg_promo_level
FROM person.person;
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
-- CREATE PROCEDURE dbo.usp_get_order_total
--     @customer_id INT,
--     @total       MONEY OUTPUT
-- AS BEGIN
--     SELECT @total = SUM(total_due) FROM sales.SalesOrderHeader
--     WHERE CustomerID = @customer_id;
-- END;

-- PostgreSQL FUNCTION (for scalar returns):
CREATE OR REPLACE FUNCTION sales.get_order_total(p_customer_id INTEGER)
RETURNS NUMERIC(19,4)
LANGUAGE plpgsql
AS $$
DECLARE
    v_total NUMERIC(19,4);
BEGIN
    SELECT COALESCE(SUM(subtotal + tax_amt + freight), 0)
    INTO   v_total
    FROM   sales.sales_order_header
    WHERE  customer_id = p_customer_id;

    RETURN v_total;
END;
$$;

-- Call it:
SELECT sales.get_order_total(1);
```

**Important:** In PostgreSQL, stored procedures (`CREATE PROCEDURE`) cannot return result sets in the same way SQL Server procedures can. To return a result set, you write a **function** using `RETURNS TABLE(...)` or `RETURNS SETOF record`. Procedures are used for transactions and side effects; functions are used for returning data.

```sql
-- Function returning a table (equivalent to a SQL Server SP that does SELECT):
CREATE OR REPLACE FUNCTION sales.get_orders_for_customer(p_customer_id INTEGER)
RETURNS TABLE (
    order_id   INTEGER,
    order_date TIMESTAMP,
    total      NUMERIC(19,4)
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT sales_order_id,
           order_date,
           (subtotal + tax_amt + freight)
    FROM   sales.sales_order_header
    WHERE  customer_id = p_customer_id
    ORDER BY order_date;
END;
$$;

-- Call like a table:
SELECT * FROM sales.get_orders_for_customer(1);
```

**Error handling:**

```sql
CREATE OR REPLACE FUNCTION sales.safe_insert_order(
    p_customer_id     INTEGER,
    p_order_number    VARCHAR(25),
    p_subtotal        NUMERIC(19,4)
)
RETURNS INTEGER
LANGUAGE plpgsql
AS $$
DECLARE
    v_new_id  INTEGER;
BEGIN
    INSERT INTO sales.sales_order_header
        (customer_id, sales_order_number, subtotal, tax_amt, freight)
    VALUES
        (p_customer_id, p_order_number, p_subtotal, p_subtotal * 0.1, 15.00)
    RETURNING sales_order_id INTO v_new_id;

    RETURN v_new_id;

EXCEPTION
    WHEN unique_violation THEN
        RAISE NOTICE 'Order number % already exists', p_order_number;
        RETURN -1;
    WHEN foreign_key_violation THEN
        RAISE EXCEPTION 'Customer ID % does not exist', p_customer_id;
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
CREATE OR REPLACE FUNCTION sales.get_order_total(p_customer_id INTEGER)
RETURNS NUMERIC(19,4)
LANGUAGE plpgsql
AS $$
DECLARE
    v_total NUMERIC(19,4);
BEGIN
    SELECT COALESCE(SUM(subtotal + tax_amt + freight), 0)
    INTO   v_total
    FROM   sales.sales_order_header
    WHERE  customer_id = p_customer_id;
    RETURN v_total;
END;
$$;

-- Call with an existing customer:
SELECT sales.get_order_total(1);
SELECT sales.get_order_total(999);   -- Customer that doesn't exist — returns 0 due to COALESCE
```

**Step 2 — Create the table-returning function:**

```sql
CREATE OR REPLACE FUNCTION sales.get_orders_for_customer(p_customer_id INTEGER)
RETURNS TABLE (
    order_id   INTEGER,
    order_date TIMESTAMP,
    total      NUMERIC(19,4)
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT sales_order_id,
           order_date,
           (subtotal + tax_amt + freight)
    FROM   sales.sales_order_header
    WHERE  customer_id = p_customer_id
    ORDER BY order_date;
END;
$$;

SELECT * FROM sales.get_orders_for_customer(1);
SELECT * FROM sales.get_orders_for_customer(2);
```

**Step 3 — Create a PostgreSQL PROCEDURE with transaction control:**

```sql
-- Procedures in PostgreSQL (11+) support COMMIT/ROLLBACK inside them
-- This is something SQL Server procedures also support
CREATE OR REPLACE PROCEDURE sales.transfer_order(
    p_source_customer INTEGER,
    p_target_customer INTEGER,
    p_order_id        INTEGER
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Update the customer on the order
    UPDATE sales.sales_order_header
    SET    customer_id = p_target_customer,
           modified_date = NOW()
    WHERE  sales_order_id = p_order_id
      AND  customer_id    = p_source_customer;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Order % not found for customer %', p_order_id, p_source_customer;
    END IF;

    RAISE NOTICE 'Order % transferred from customer % to customer %',
        p_order_id, p_source_customer, p_target_customer;
END;
$$;

-- Call a procedure with CALL (not SELECT!):
CALL sales.transfer_order(1, 2, 1);
```

**Step 4 — Use a DO block for a one-time data migration task:**

```sql
-- Equivalent to an ad-hoc T-SQL migration script
DO $$
DECLARE
    v_rec     RECORD;
    v_count   INTEGER := 0;
BEGIN
    -- Standardize email_promotion values: set any value > 2 to 2
    FOR v_rec IN
        SELECT business_entity_id, email_promotion
        FROM person.person
        WHERE email_promotion > 2
    LOOP
        UPDATE person.person
        SET    email_promotion = 2
        WHERE  business_entity_id = v_rec.business_entity_id;
        v_count := v_count + 1;
    END LOOP;

    RAISE NOTICE 'Standardized % records', v_count;
END;
$$;
```

**Step 5 — List all functions in the sales schema (equivalent to sys.procedures in SQL Server):**

```sql
SELECT routine_name, routine_type, data_type
FROM information_schema.routines
WHERE routine_schema = 'sales'
ORDER BY routine_name;

-- Or using pg_proc for more details:
SELECT p.proname   AS function_name,
       pg_get_function_result(p.oid) AS return_type,
       l.lanname   AS language
FROM pg_proc p
JOIN pg_namespace n ON n.oid = p.pronamespace
JOIN pg_language  l ON l.oid = p.prolang
WHERE n.nspname = 'sales'
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
- [EDB Blog — T-SQL to PL/pgSQL Migration Guide](https://www.enterprisedb.com/blog/how-migrate-sql-server-postgresql)
- [Use the Pipes — PostgreSQL for SQL Server DBAs](https://use-the-index-luke.com/sql/postgresql-for-sql-server-dbas)

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/geopin.png"><b>Next Steps</b></p>

Next, continue to <a href="04_-_Indexes_and_Performance.md" target="_blank"><i>Module 04 – Indexes and Performance</i></a>.
