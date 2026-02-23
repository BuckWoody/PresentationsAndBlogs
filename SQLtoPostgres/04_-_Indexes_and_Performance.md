![](graphics/microsoftlogo.png)

# Workshop: PostgreSQL for the SQL Server Database Professional

#### <i>A Microsoft-style Course — SQL Server & PostgreSQL Track</i>

<p style="border-bottom: 1px solid lightgrey;"></p>

<img style="float: left; margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/textbubble.png"> <h2>Module 04 – Indexes and Performance</h2>

*Estimated Time: 60 minutes (≈20 minutes lecture, ≈40 minutes hands-on)*

This module covers PostgreSQL's index ecosystem, how to read `EXPLAIN ANALYZE` output (the equivalent of SQL Server's execution plan), how autovacuum and statistics affect query plans, and how `pg_stat_statements` gives you the equivalent of SQL Server's Query Store.

<p style="border-bottom: 1px solid lightgrey;"></p>

<h2><img style="float: left; margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/pencil2.png">4.1 – Index Types in PostgreSQL vs. SQL Server</h2>

SQL Server has two primary index categories: **clustered** (the table is the index — data rows are stored in index key order) and **nonclustered** (a separate structure with a pointer back to the heap or the clustered index). PostgreSQL has **no clustered index concept** — the table data is always stored in a heap (a collection of 8KB pages in no particular order). PostgreSQL does have a `CLUSTER` command that physically reorders the heap to match an index, but it is a one-time operation and the table drifts back to disorder with subsequent writes.

**PostgreSQL index types:**

| Index Type | SQL Server Equivalent | Best Use Cases |
|---|---|---|
| **B-tree** (default) | Clustered / nonclustered index | Equality, range, ORDER BY, LIKE 'prefix%' |
| **Hash** | (none — SQL Server uses B-tree for equality) | Equality lookups only; no range support |
| **GiST** (Generalized Search Tree) | Spatial index (geometry type) | Geometric/spatial data, full-text, ranges |
| **GIN** (Generalized Inverted Index) | Full-text index | JSONB, array containment, full-text search |
| **BRIN** (Block Range Index) | (none) | Very large tables with naturally ordered data (time-series, IoT) |
| **Partial index** | Filtered index (`WHERE` clause on index) | Indexes on a subset of rows — very powerful |
| **Expression index** | Computed column index | Index on `LOWER(email)`, `EXTRACT(YEAR FROM d)` |
| **Covering index** (`INCLUDE`) | Nonclustered index with `INCLUDE` columns | Satisfy queries from index alone (index-only scan) |

**The clustered vs. heap difference matters for performance.** In SQL Server, a clustered index seek goes directly to the data row. In PostgreSQL, an index scan must follow a pointer from the index leaf to the heap page (a "heap fetch"). For this reason, PostgreSQL has the concept of an **Index Only Scan** — when the index contains all the columns needed by the query (a covering index), PostgreSQL can return results without touching the heap. This is controlled by the **visibility map**, which is maintained by VACUUM.

**B-tree index syntax — nearly identical to SQL Server:**

```sql
-- SQL Server:
CREATE INDEX IX_Person_LastName ON Person.Person (LastName ASC);
CREATE UNIQUE INDEX UX_Sales_OrderNumber ON Sales.SalesOrderHeader (SalesOrderNumber);
CREATE INDEX IX_SOH_OrderDate_INC ON Sales.SalesOrderHeader (OrderDate)
    INCLUDE (SubTotal, TaxAmt, Freight);

-- PostgreSQL:
CREATE INDEX idx_person_last_name        ON person.person          (last_name ASC);
CREATE UNIQUE INDEX ux_sales_order_number ON sales.sales_order_header (sales_order_number);
CREATE INDEX idx_soh_order_date          ON sales.sales_order_header (order_date)
    INCLUDE (subtotal, tax_amt, freight);  -- Covering index (PostgreSQL 11+)
```

**Partial indexes** are one of PostgreSQL's most powerful features and correspond to SQL Server's filtered indexes:

```sql
-- Only index active, un-shipped orders (not the full history):
CREATE INDEX idx_soh_unshipped
    ON sales.sales_order_header (order_date)
    WHERE ship_date IS NULL;

-- This index is tiny but very fast for:
SELECT * FROM sales.sales_order_header WHERE order_date > NOW() - INTERVAL '30 days'
  AND ship_date IS NULL;
```

**Expression (functional) indexes** — index a computed expression rather than a raw column:

```sql
-- Case-insensitive search index (eliminates full table scans on LOWER() queries):
CREATE INDEX idx_person_last_name_lower
    ON person.person (LOWER(last_name));

-- Now this query uses the index:
SELECT * FROM person.person WHERE LOWER(last_name) = 'smith';

-- SQL Server equivalent: computed column + index, or a filtered index with a persisted column
```

**GIN index for JSONB and full-text search:**

```sql
-- For full-text search (covered more in Module 06):
ALTER TABLE person.person ADD COLUMN search_vector TSVECTOR;

CREATE INDEX idx_person_fts ON person.person USING GIN (search_vector);

-- For JSONB columns (Module 06):
-- CREATE INDEX idx_demographics_gin ON person.person USING GIN (demographics);
```

<h3>4.2 – Concurrent Index Builds</h3>

SQL Server builds indexes with locks that can block concurrent DML (depending on edition). PostgreSQL has `CREATE INDEX CONCURRENTLY`, which builds the index without blocking reads or writes (at the cost of taking longer and using more resources):

```sql
-- Build index without blocking production traffic:
CREATE INDEX CONCURRENTLY idx_soh_customer_id
    ON sales.sales_order_header (customer_id);

-- DROP INDEX CONCURRENTLY works similarly:
DROP INDEX CONCURRENTLY idx_soh_customer_id;
```

`CREATE INDEX CONCURRENTLY` cannot be run inside a transaction block.

<p style="border-bottom: 1px solid lightgrey;"></p>

<h2><img style="float: left; margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/pencil2.png">4.3 – Reading EXPLAIN ANALYZE (the PostgreSQL Execution Plan)</h2>

`EXPLAIN` shows the estimated execution plan without running the query (equivalent to SSMS's "Display Estimated Execution Plan" button). `EXPLAIN ANALYZE` runs the query and shows both estimated and actual statistics (equivalent to "Include Actual Execution Plan").

```sql
EXPLAIN SELECT * FROM person.person WHERE last_name = 'Smith';
EXPLAIN ANALYZE SELECT * FROM person.person WHERE last_name = 'Smith';
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT) SELECT * FROM person.person WHERE last_name = 'Smith';
```

**Reading the plan — key concepts:**

The plan is a tree of nodes read from **innermost (deepest) to outermost**. Each node shows:

```
Seq Scan on person  (cost=0.00..12.50 rows=3 width=92) (actual time=0.012..0.025 rows=3 loops=1)
  Filter: ((last_name)::text = 'Smith'::text)
  Rows Removed by Filter: 3
```

- **cost=startup_cost..total_cost** — Planner's estimate. Startup cost is cost to return the *first* row; total cost is cost to return *all* rows. These are in "cost units" (abstract, relative).
- **rows** — Planner's estimate of rows returned.
- **width** — Estimated average row width in bytes.
- **actual time=start_ms..end_ms** — Real elapsed time in milliseconds. Compare to estimated.
- **rows** (actual section) — Actual rows returned. If this differs greatly from the estimate, statistics are stale.
- **loops** — How many times this node executed (e.g., inside a nested loop join).
- **Buffers** — With `BUFFERS` option: `shared hit` = pages read from buffer cache (like SQL Server buffer pool hits); `shared read` = pages read from disk.

**Common plan node types and their SQL Server equivalents:**

| PostgreSQL Node | SQL Server Equivalent |
|---|---|
| `Seq Scan` | Table Scan |
| `Index Scan` | Clustered Index Scan or Nonclustered Index Scan + Key Lookup |
| `Index Only Scan` | Nonclustered Index Scan (no key lookup needed) |
| `Bitmap Heap Scan` + `Bitmap Index Scan` | No direct equivalent (combines multiple indexes) |
| `Nested Loop` | Nested Loops Join |
| `Hash Join` | Hash Match Join |
| `Merge Join` | Merge Join |
| `Sort` | Sort |
| `Hash Aggregate` | Hash Match Aggregate |
| `Gather` / `Gather Merge` | Parallelism (Exchange operator) |
| `Limit` | Top |
| `CTE Scan` | Lazy Table Spool (CTE) |

**Identifying plan problems — the same principles apply as in SQL Server:**

- **Row estimate mismatch:** `rows=1` estimated but `rows=50000` actual → stale statistics → run `ANALYZE tablename`.
- **Seq Scan on large table when an index exists:** Either the index is not selective enough (planner is right), or `random_page_cost` is set too high for your storage (lower it for SSD).
- **Very high `Rows Removed by Filter`:** The index is not covering the WHERE clause; add a better index.
- **Sort appearing before a Join:** May indicate missing index on join key.

<p style="border-bottom: 1px solid lightgrey;"></p>

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/point1.png"><b>Activity 4.1 – Create Indexes and Read Execution Plans</b></p>

<p><img style="margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/checkmark.png"><b>Steps</b></p>

**Step 1 — Load a larger dataset for meaningful plan analysis:**

```sql
-- Insert 10,000 rows of synthetic person data
INSERT INTO person.person (person_type, first_name, last_name, email_promotion, is_active)
SELECT
    CASE (i % 3) WHEN 0 THEN 'IN' WHEN 1 THEN 'SP' ELSE 'SC' END,
    'FirstName_' || i::TEXT,
    CASE (i % 10)
        WHEN 0 THEN 'Smith'  WHEN 1 THEN 'Jones'    WHEN 2 THEN 'Williams'
        WHEN 3 THEN 'Brown'  WHEN 4 THEN 'Taylor'   WHEN 5 THEN 'Wilson'
        WHEN 6 THEN 'Johnson' WHEN 7 THEN 'Davies'  WHEN 8 THEN 'Evans'
        ELSE 'Thomas'
    END,
    i % 3,
    (i % 5 <> 0)
FROM generate_series(1, 10000) AS s(i);
```

`generate_series()` is PostgreSQL's equivalent of a tally/numbers table. It generates a set of integers from start to stop.

**Step 2 — Check statistics and run EXPLAIN with no index:**

```sql
-- Update statistics (equivalent to UPDATE STATISTICS in SQL Server):
ANALYZE person.person;

-- Check the plan for a query without an index on last_name:
EXPLAIN ANALYZE
SELECT business_entity_id, first_name, last_name
FROM person.person
WHERE last_name = 'Smith';
```

You should see a **Seq Scan** (full table scan). Note the estimated vs. actual rows.

**Step 3 — Create an index and re-check the plan:**

```sql
CREATE INDEX idx_person_last_name ON person.person (last_name);

-- Re-run the same query:
EXPLAIN ANALYZE
SELECT business_entity_id, first_name, last_name
FROM person.person
WHERE last_name = 'Smith';
```

The plan should now show an **Index Scan** or **Bitmap Index Scan** depending on selectivity. Note the difference in cost and actual time.

**Step 4 — Create a covering index and observe an Index Only Scan:**

```sql
-- Drop the old index, create a covering index:
DROP INDEX idx_person_last_name;

CREATE INDEX idx_person_last_name_covering
    ON person.person (last_name) INCLUDE (first_name, business_entity_id);

EXPLAIN ANALYZE
SELECT business_entity_id, first_name, last_name
FROM person.person
WHERE last_name = 'Smith';
```

You should now see an **Index Only Scan** — the query is satisfied entirely from the index without touching the heap.

**Step 5 — Create and test a partial index:**

```sql
-- Index only the inactive persons (is_active = FALSE):
CREATE INDEX idx_person_inactive
    ON person.person (last_name)
    WHERE is_active = FALSE;

EXPLAIN ANALYZE
SELECT * FROM person.person
WHERE is_active = FALSE
  AND last_name = 'Smith';

-- Compare plan for active persons (partial index not used):
EXPLAIN ANALYZE
SELECT * FROM person.person
WHERE is_active = TRUE
  AND last_name = 'Smith';
```

**Step 6 — Demonstrate expression index:**

```sql
-- Create expression index on LOWER(last_name):
CREATE INDEX idx_person_last_name_ci ON person.person (LOWER(last_name));

-- Case-insensitive search using the expression index:
EXPLAIN ANALYZE
SELECT * FROM person.person
WHERE LOWER(last_name) = 'smith';   -- Uses index

EXPLAIN ANALYZE
SELECT * FROM person.person
WHERE last_name ILIKE 'smith';       -- May or may not use index (ILIKE is different)
```

**Step 7 — Use pgAdmin's graphical EXPLAIN:**

In pgAdmin Query Tool, paste the query from Step 3 and click the **Explain Analyze** button (the lightning bolt with magnifying glass). Switch between the **Graphical**, **Table**, and **Statistics** tabs. This is the closest experience to the SSMS graphical execution plan.

<p style="border-bottom: 1px solid lightgrey;"></p>

<h2><img style="float: left; margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/pencil2.png">4.4 – Autovacuum, Statistics, and pg_stat_statements</h2>

**Autovacuum** is PostgreSQL's background maintenance process. Because MVCC keeps dead row versions on disk, autovacuum reclaims that space and updates statistics. It runs automatically in the background and you should normally not need to disable it — but you must understand it to avoid table bloat and statistics drift.

Key autovacuum parameters (in `postgresql.conf`):

```sql
-- Check current autovacuum settings:
SELECT name, setting, short_desc
FROM pg_settings
WHERE name LIKE 'autovacuum%'
ORDER BY name;
```

**Manual VACUUM and ANALYZE (equivalent to SQL Server's maintenance jobs):**

```sql
-- Reclaim dead space (like shrink/reorganize — but not to shrink the file):
VACUUM person.person;
VACUUM VERBOSE person.person;    -- Shows detailed output

-- Update statistics (equivalent to UPDATE STATISTICS in SQL Server):
ANALYZE person.person;

-- Both at once:
VACUUM ANALYZE person.person;

-- Full vacuum — reclaims space to OS, rewrites the table, exclusive lock required:
VACUUM FULL person.person;       -- Use sparingly; like DBCC SHRINKFILE but safer
```

**pg_stat_statements — the equivalent of Query Store:**

Enable the extension to track query performance:

```sql
-- In postgresql.conf, add:
-- shared_preload_libraries = 'pg_stat_statements'
-- (requires a restart)

-- Then in your database:
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- Top 10 slowest queries by total execution time:
SELECT LEFT(query, 80)           AS query_snippet,
       calls,
       ROUND(total_exec_time::NUMERIC, 2) AS total_ms,
       ROUND(mean_exec_time::NUMERIC,  2) AS avg_ms,
       ROUND((100 * total_exec_time / SUM(total_exec_time) OVER ())::NUMERIC, 2) AS pct_total,
       rows
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 10;

-- Reset the statistics (like clearing Query Store):
SELECT pg_stat_statements_reset();
```

**Missing index hints — PostgreSQL equivalent:**

PostgreSQL does not have SQL Server's "Missing Index" DMV suggestions in execution plans. However, you can infer missing indexes from `pg_stat_user_tables`:

```sql
-- Tables with many sequential scans relative to index scans (candidates for indexing):
SELECT relname             AS table_name,
       seq_scan,
       seq_tup_read,
       idx_scan,
       n_live_tup         AS live_rows
FROM pg_stat_user_tables
ORDER BY seq_scan DESC
LIMIT 20;
```

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/point1.png"><b>Activity 4.2 – Investigate Statistics and Autovacuum</b></p>

<p><img style="margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/checkmark.png"><b>Steps</b></p>

**Step 1 — View table statistics and bloat:**

```sql
SELECT relname          AS table_name,
       n_live_tup       AS live_rows,
       n_dead_tup       AS dead_rows,
       last_vacuum,
       last_autovacuum,
       last_analyze,
       last_autoanalyze
FROM pg_stat_user_tables
WHERE schemaname IN ('person', 'sales')
ORDER BY n_dead_tup DESC;
```

**Step 2 — Deliberately create dead rows and observe:**

```sql
-- Create dead rows by updating every person:
UPDATE person.person SET modified_date = NOW();

-- Check dead rows (will show before autovacuum runs):
SELECT relname, n_live_tup, n_dead_tup
FROM pg_stat_user_tables
WHERE relname = 'person';

-- Run manual vacuum and re-check:
VACUUM person.person;

SELECT relname, n_live_tup, n_dead_tup
FROM pg_stat_user_tables
WHERE relname = 'person';
```

**Step 3 — Check index usage statistics:**

```sql
-- Index usage report (equivalent to sys.dm_db_index_usage_stats in SQL Server):
SELECT schemaname,
       relname          AS table_name,
       indexrelname     AS index_name,
       idx_scan         AS index_scans,
       idx_tup_read     AS rows_read,
       idx_tup_fetch    AS rows_fetched
FROM pg_stat_user_indexes
WHERE schemaname IN ('person', 'sales')
ORDER BY idx_scan DESC;
```

Indexes with zero `idx_scan` are candidates for removal (just like SQL Server's unused index DMV).

<p style="border-bottom: 1px solid lightgrey;"></p>

<p><img style="margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/owl.png"><b>For Further Study</b></p>

- [PostgreSQL Documentation — Index Types](https://www.postgresql.org/docs/current/indexes-types.html)
- [PostgreSQL Documentation — EXPLAIN](https://www.postgresql.org/docs/current/sql-explain.html)
- [PostgreSQL Documentation — Using EXPLAIN](https://www.postgresql.org/docs/current/using-explain.html)
- [PostgreSQL Documentation — VACUUM](https://www.postgresql.org/docs/current/sql-vacuum.html)
- [PostgreSQL Documentation — pg_stat_statements](https://www.postgresql.org/docs/current/pgstatstatements.html)
- [PostgreSQL Documentation — Autovacuum](https://www.postgresql.org/docs/current/routine-vacuuming.html)
- [Use The Index, Luke — PostgreSQL Index Guide](https://use-the-index-luke.com/)
- [Explain.dalibo.com — Graphical EXPLAIN ANALYZE Visualizer](https://explain.dalibo.com/)
- [pgMustard — EXPLAIN ANALYZE Advisor](https://www.pgmustard.com/)
- [Percona — PostgreSQL Index Bloat and Vacuum](https://www.percona.com/blog/postgresql-bloat-autovacuum-and-vacuum/)
- [Microsoft Learn — SQL Server Index Architecture](https://learn.microsoft.com/en-us/sql/relational-databases/indexes/clustered-and-nonclustered-indexes-described)

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/geopin.png"><b>Next Steps</b></p>

Next, continue to <a href="05_-_Administration_and_Security.md" target="_blank"><i>Module 05 – Administration and Security</i></a>.
