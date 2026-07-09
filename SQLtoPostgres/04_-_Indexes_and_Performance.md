![](graphics/microsoftlogo.png)

# Workshop: PostgreSQL for the SQL Server Database Professional

#### <i>A SQL Server to PostgreSQL Skilling</i>


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
| **Expression index** | Computed column index | Index on `LOWER(au_lname)`, `EXTRACT(YEAR FROM pubdate)` |
| **Covering index** (`INCLUDE`) | Nonclustered index with `INCLUDE` columns | Satisfy queries from index alone (index-only scan) |

**The clustered vs. heap difference matters for performance.** In SQL Server, a clustered index seek goes directly to the data row. In PostgreSQL, an index scan must follow a pointer from the index leaf to the heap page (a "heap fetch"). For this reason, PostgreSQL has the concept of an **Index Only Scan** — when the index contains all the columns needed by the query (a covering index), PostgreSQL can return results without touching the heap. This is controlled by the **visibility map**, which is maintained by VACUUM.

**B-tree index syntax — nearly identical to SQL Server:**

```sql
-- SQL Server:
CREATE INDEX IX_Author_LastName ON dbo.authors (au_lname ASC);
CREATE UNIQUE INDEX UX_Publisher_Name ON dbo.publishers (pub_name);
CREATE INDEX IX_Titles_PubDate ON dbo.titles (pubdate)
    INCLUDE (price, ytd_sales);

-- PostgreSQL:
CREATE INDEX idx_authors_lname         ON authors    (au_lname ASC);
CREATE UNIQUE INDEX ux_publishers_name ON publishers (pub_name);
CREATE INDEX idx_titles_pubdate        ON titles     (pubdate)
    INCLUDE (price, ytd_sales);   -- Covering index (PostgreSQL 11+)
```

**Partial indexes** are one of PostgreSQL's most powerful features and correspond to SQL Server's filtered indexes:

```sql
-- Only index authors not yet under contract (not the full author list):
CREATE INDEX idx_authors_no_contract
    ON authors (au_lname)
    WHERE contract = 0;

-- This index is tiny but very fast for:
SELECT * FROM authors WHERE au_lname > 'M' AND contract = 0;
```

**Expression (functional) indexes** — index a computed expression rather than a raw column:

```sql
-- Case-insensitive search index (eliminates full table scans on LOWER() queries):
CREATE INDEX idx_authors_lname_lower
    ON authors (LOWER(au_lname));

-- Now this query uses the index:
SELECT * FROM authors WHERE LOWER(au_lname) = 'smith';

-- SQL Server equivalent: computed column + index, or a filtered index with a persisted column
```

**GIN index for JSONB and full-text search:**

```sql
-- For full-text search (covered more in Module 06):
ALTER TABLE titles ADD COLUMN search_vector TSVECTOR;

CREATE INDEX idx_titles_fts ON titles USING GIN (search_vector);

-- For JSONB columns (Module 06):
-- CREATE INDEX idx_pub_info_gin ON pub_info USING GIN (pr_info_json);
```

<h3>4.2 – Concurrent Index Builds</h3>

SQL Server builds indexes with locks that can block concurrent DML (depending on edition). PostgreSQL has `CREATE INDEX CONCURRENTLY`, which builds the index without blocking reads or writes (at the cost of taking longer and using more resources):

> Note: Each of the following steps should be run individually. If you run UPDATE and SELECT from `pg_stat_user_tables` as a batch, the dead rows may not show up in the results. It's best-practice to run the UPDATE first, then separately run the stats query.

```sql
-- Build index without blocking production traffic:
CREATE INDEX CONCURRENTLY idx_employee_pub_id
    ON employee (pub_id);

-- DROP INDEX CONCURRENTLY works similarly:
DROP INDEX CONCURRENTLY idx_employee_pub_id;
```

`CREATE INDEX CONCURRENTLY` cannot be run inside a transaction block.

<p style="border-bottom: 1px solid lightgrey;"></p>

<h2><img style="float: left; margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/pencil2.png">4.3 – Reading EXPLAIN ANALYZE (the PostgreSQL Execution Plan)</h2>

`EXPLAIN` shows the estimated execution plan without running the query (equivalent to SSMS's "Display Estimated Execution Plan" button). `EXPLAIN ANALYZE` runs the query and shows both estimated and actual statistics (equivalent to "Include Actual Execution Plan").

```sql
EXPLAIN SELECT * FROM authors WHERE au_lname = 'Smith';
EXPLAIN ANALYZE SELECT * FROM authors WHERE au_lname = 'Smith';
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT) SELECT * FROM authors WHERE au_lname = 'Smith';
```

**Reading the plan — key concepts:**

The plan is a tree of nodes read from **innermost (deepest) to outermost**. Each node shows:

```
Seq Scan on authors  (cost=0.00..12.50 rows=3 width=92) (actual time=0.012..0.025 rows=3 loops=1)
  Filter: ((au_lname)::text = 'Smith'::text)
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
-- The pubs authors table ships with an index on (au_lname, au_fname) called aunmind.
-- Drop it before the demo so we can observe the full sequence of plan changes
-- as we add indexes step by step. It will be recreated at the end of this activity.
DROP INDEX IF EXISTS aunmind;

-- Insert 9,999 rows of synthetic author data.
-- au_id must match the format ^\d{3}-\d{2}-\d{4}$ and be unique.
-- The formula below produces values like '000-01-0001' through '999-09-9999',
-- none of which conflict with the 23 real pubs authors (whose middle segments
-- are all >= 17, while ours are 00-09).
INSERT INTO authors (au_id, au_lname, au_fname, phone, contract)
SELECT
    LPAD((i / 10)::TEXT, 3, '0') || '-' ||
    LPAD((i % 10)::TEXT, 2, '0') || '-' ||
    LPAD(i::TEXT, 4, '0'),
    CASE (i % 10)
        WHEN 0 THEN 'Smith'   WHEN 1 THEN 'Jones'    WHEN 2 THEN 'Williams'
        WHEN 3 THEN 'Brown'   WHEN 4 THEN 'Taylor'   WHEN 5 THEN 'Wilson'
        WHEN 6 THEN 'Johnson' WHEN 7 THEN 'Davies'   WHEN 8 THEN 'Evans'
        ELSE 'Thomas'
    END,
    'FirstName_' || i::TEXT,
    'UNKNOWN',
    i % 2
FROM generate_series(1, 9999) AS s(i);
```

`generate_series()` is PostgreSQL's equivalent of a tally/numbers table. It generates a set of integers from start to stop.

**Step 2 — Check statistics and run EXPLAIN with no index:**

```sql
-- Update statistics (equivalent to UPDATE STATISTICS in SQL Server):
ANALYZE authors;

-- Check the plan for a query without an index on au_lname:
EXPLAIN ANALYZE
SELECT au_id, au_fname, au_lname
FROM authors
WHERE au_lname = 'Smith';
```

You should see a **Seq Scan** (full table scan). Note the estimated vs. actual rows.

**Step 3 — Create an index and re-check the plan:**

```sql
CREATE INDEX idx_authors_lname ON authors (au_lname);

-- Re-run the same query:
EXPLAIN ANALYZE
SELECT au_id, au_fname, au_lname
FROM authors
WHERE au_lname = 'Smith';
```

The plan should now show an **Index Scan** or **Bitmap Index Scan** depending on selectivity. Note the difference in cost and actual time.

**Step 4 — Create a covering index and observe an Index Only Scan:**

```sql
-- Drop the old index, create a covering index:
DROP INDEX idx_authors_lname;

CREATE INDEX idx_authors_lname_covering
    ON authors (au_lname) INCLUDE (au_fname, phone);

EXPLAIN ANALYZE
SELECT au_fname, au_lname, phone
FROM authors
WHERE au_lname = 'Smith';
```

You should now see an **Index Only Scan** — the query is satisfied entirely from the index without touching the heap.

**Step 5 — Create and test a partial index:**

```sql
-- Index only authors not under contract (contract = 0):
CREATE INDEX idx_authors_no_contract
    ON authors (au_lname)
    WHERE contract = 0;

EXPLAIN ANALYZE
SELECT * FROM authors
WHERE contract = 0
  AND au_lname = 'Smith';

-- Compare plan for contracted authors (partial index not used):
EXPLAIN ANALYZE
SELECT * FROM authors
WHERE contract = 1
  AND au_lname = 'Smith';
```

**Step 6 — Demonstrate expression index:**

```sql
-- Create expression index on LOWER(au_lname):
CREATE INDEX idx_authors_lname_ci ON authors (LOWER(au_lname));

-- Case-insensitive search using the expression index:
EXPLAIN ANALYZE
SELECT * FROM authors
WHERE LOWER(au_lname) = 'smith';   -- Uses index

EXPLAIN ANALYZE
SELECT * FROM authors
WHERE au_lname ILIKE 'smith';       
```
*Note:A standard B-tree expression index on LOWER(au_lname) cannot serve an ILIKE predicate. The planner does not rewrite ILIKE into a LOWER(au_lname) = … form, so this index will not be used. To index ILIKE/pattern matching you need a pg_trgm GIN/GiST index (gin_trgm_ops).*

**Step 7 — Use pgAdmin's graphical EXPLAIN:**

In pgAdmin Query Tool, paste the query from Step 3 and click the **Explain Analyze** button (depending on version, may like a bar graph next to an "E" block.). Switch between the **Graphical**, **Table**, and **Statistics** tabs. This is the closest experience to the SSMS graphical execution plan.

```sql
-- Cleanup: remove synthetic rows and restore the original pubs index
-- so subsequent modules see the standard pubs authors table.
DELETE FROM authors WHERE au_fname LIKE 'FirstName_%';
DROP INDEX IF EXISTS idx_authors_lname_covering;
DROP INDEX IF EXISTS idx_authors_no_contract;
DROP INDEX IF EXISTS idx_authors_lname_ci;
CREATE INDEX aunmind ON authors (au_lname, au_fname);
```

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
VACUUM authors;
VACUUM VERBOSE authors;    -- Shows detailed output

-- Update statistics (equivalent to UPDATE STATISTICS in SQL Server):
ANALYZE authors;

-- Both at once:
VACUUM ANALYZE authors;

-- Full vacuum — reclaims space to OS, rewrites the table, exclusive lock required:
VACUUM FULL authors;       -- Use sparingly; like DBCC SHRINKFILE but safer
```

**pg_stat_statements — the equivalent of Query Store:**

Unlike SQL Server's Query Store (enabled with a single `ALTER DATABASE` command), `pg_stat_statements` requires two separate phases: a server configuration change followed by a restart, then a per-database `CREATE EXTENSION`. Running `CREATE EXTENSION` without completing Phase 1 first produces the error `pg_stat_statements must be loaded via shared_preload_libraries`.

**Phase 1 — Server configuration (requires a PostgreSQL restart):**

First, find your `postgresql.conf` location:

```sql
-- Run this in psql or any query tool to find the config file path:
SHOW config_file;
```

Open that file in a text editor and add or update this line:

```
shared_preload_libraries = 'pg_stat_statements'
```

If `shared_preload_libraries` already exists with other values, append to it:

```
shared_preload_libraries = 'pg_stat_statements,other_existing_library'
```

Then restart PostgreSQL. On Linux with systemd:

```bash
sudo systemctl restart postgresql
```

On Windows, restart the PostgreSQL service from Services (services.msc) or:

```cmd
net stop postgresql-x64-17 && net start postgresql-x64-17
```

(Replace `postgresql-x64-17` with your installed service name.)

Verify the library loaded after restart:

```sql
SHOW shared_preload_libraries;
```

**Phase 2 — Enable in the database (run once per database, no restart needed):**

```sql
-- Enable the extension in the pubs database:
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- Confirm it is active:
SELECT * FROM pg_extension WHERE extname = 'pg_stat_statements';
```

**Querying pg_stat_statements:**

```sql
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
WHERE schemaname = 'public'
ORDER BY n_dead_tup DESC;
```

**Step 2 — Deliberately create dead rows and observe:**

```sql
-- Touch every row to create dead tuple versions
-- (self-assignment changes nothing but forces MVCC to write new row versions):
UPDATE authors SET phone = phone;

-- Check dead rows (will show before autovacuum runs):
SELECT relname, n_live_tup, n_dead_tup
FROM pg_stat_user_tables
WHERE relname = 'authors';

-- Run manual vacuum and re-check:
VACUUM authors;

SELECT relname, n_live_tup, n_dead_tup
FROM pg_stat_user_tables
WHERE relname = 'authors';
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
WHERE schemaname = 'public'
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
- [Percona — PostgreSQL Index Bloat and Vacuum](https://www.percona.com/blog/postgresql-vacuuming-to-optimize-database-performance-and-reclaim-space/)
- [Microsoft Learn — SQL Server Index Architecture](https://learn.microsoft.com/en-us/sql/relational-databases/indexes/clustered-and-nonclustered-indexes-described)

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/geopin.png"><b>Next Steps</b></p>

Next, continue to <a href="05_-_Administration_and_Security.md" target="_blank"><i>Module 05 – Administration and Security</i></a>.
