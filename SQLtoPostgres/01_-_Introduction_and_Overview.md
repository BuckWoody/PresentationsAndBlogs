![](graphics/microsoftlogo.png)

# Workshop: PostgreSQL for the SQL Server Database Professional

#### <i>A SQL Server to PostgreSQL Skilling</i>


<p style="border-bottom: 1px solid lightgrey;"></p>

<img style="float: left; margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/textbubble.png"> <h2>Module 01 – Introduction and Overview</h2>

*Estimated Time: 60 minutes (≈20 minutes lecture, ≈40 minutes hands-on)*

In this module you will build a mental map of PostgreSQL by comparing it directly to SQL Server. The goal is not to make you an expert yet — it is to eliminate the "unknown unknowns" so that the rest of the day's exercises make sense. By the end of this module you will be able to connect to PostgreSQL, navigate its hierarchy of objects, and use its primary client tools.

Make sure you have completed the <a href="00_-_Pre-Requisites.md">Pre-Requisites</a> before starting this module.

<p style="border-bottom: 1px solid lightgrey;"></p>

<h2><img style="float: left; margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/pencil2.png">1.1 – How PostgreSQL Compares to SQL Server at a Glance</h2>

Both SQL Server and PostgreSQL are full ACID-compliant relational database management systems that support standard SQL, stored procedures, triggers, views, indexing, replication, and role-based security. For a working SQL Server professional, most of the concepts transfer directly — the vocabulary and the mechanics differ in important ways.

The table below is your "Rosetta Stone" for the workshop:

| Concept | SQL Server | PostgreSQL |
|---|---|---|
| Server instance | SQL Server instance (one per port, default 1433) | PostgreSQL cluster (one per port, default 5432) |
| Top-level container | Database | Database |
| Namespace within database | Schema (dbo is default) | Schema (public is default) |
| Admin superuser | `sa` | `postgres` |
| Procedural language | T-SQL | PL/pgSQL (also PL/Python, PL/Perl, etc.) |
| Interactive terminal | `sqlcmd` | `psql` |
| Primary GUI | SSMS | pgAdmin 4 |
| Execution plan tool | SSMS graphical plan / SET STATISTICS XML | `EXPLAIN` / `EXPLAIN ANALYZE` |
| Transaction log | Per-database `.ldf` file | Cluster-wide WAL (Write-Ahead Log) |
| Concurrency model | Lock-based (pessimistic by default) | MVCC (Multi-Version Concurrency Control) |
| Auto-increment column | `IDENTITY(1,1)` | `SERIAL`, `BIGSERIAL`, or `GENERATED ALWAYS AS IDENTITY` |
| Catalog tables | `sys.*` views | `pg_catalog.*` and `information_schema.*` views |
| Jobs/scheduling | SQL Server Agent | `pg_cron` extension, or OS-level cron |
| Linked servers | Linked Servers / OPENROWSET | Foreign Data Wrappers (FDW) |
| Licensing | Commercial (free Developer/Express editions) | Open source (PostgreSQL License) |

**Key Insight — The Cluster/Database/Schema hierarchy is the same:** In both systems the hierarchy is: *server instance → database → schema → object*. The word "cluster" in PostgreSQL is simply the term for what SQL Server calls an "instance." You connect to a PostgreSQL cluster on port 5432, then choose a database, exactly as you connect to a SQL Server instance and choose a database.

<h3>Process Model vs. Thread Model</h3>

One of the most important architectural differences is how each system handles client connections. SQL Server uses a **thread-based model**: a pool of OS threads managed within a single process (`sqlservr.exe`) handles all client connections. PostgreSQL uses a **process-based model**: each client connection spawns a dedicated OS process (`postgres` backend process). This means that on a system with 500 concurrent connections, PostgreSQL will have approximately 500 OS processes. The process model provides strong isolation — a crashing backend affects only that connection — but it also means connection pooling is far more critical in PostgreSQL than in SQL Server. Tools such as **PgBouncer** or **pgpool-II** are used in production PostgreSQL environments for the same reason that SQL Server's built-in connection pool is less of a concern for SQL Server developers.

<h3>MVCC vs. Lock-Based Concurrency</h3>

SQL Server's default transaction isolation level (`READ COMMITTED`) acquires shared read locks on rows as they are read and releases them when the statement completes. Readers can block writers and writers can block readers (unless `READ_COMMITTED_SNAPSHOT` is enabled at the database level).

PostgreSQL uses **Multi-Version Concurrency Control (MVCC)** by default. When a row is updated, PostgreSQL creates a *new physical version* of that row (called a "tuple") rather than overwriting the existing one. Readers always see a consistent snapshot of the data at their transaction start time, and **readers never block writers, and writers never block readers**. The tradeoff is that "dead" old row versions accumulate on disk and must be reclaimed by the **VACUUM** process — something that has no direct SQL Server equivalent and is covered in Module 05.

<h3>WAL vs. Transaction Log</h3>

SQL Server writes all changes to a per-database transaction log (`.ldf` file) before writing to data pages. PostgreSQL writes all changes to the cluster-wide **Write-Ahead Log (WAL)** before writing to data pages. The principle is identical — durability and crash recovery — but because the WAL is cluster-wide rather than per-database, PostgreSQL backup, replication, and PITR (Point-In-Time Recovery) all work at the cluster level rather than the database level.

**Practical implication:** `pg_basebackup` (the equivalent of a SQL Server full backup) backs up the entire cluster, not a single database. `pg_dump` is used to back up individual databases (covered in Module 05).

<p style="border-bottom: 1px solid lightgrey;"></p>

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/point1.png"><b>Activity 1.1 – Connect with psql and Explore the Cluster Hierarchy</b></p>

<p><img style="margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/checkmark.png"><b>Description</b></p>

In this activity you will use `psql` — PostgreSQL's command-line client — to connect to your local cluster and explore the object hierarchy. This mirrors what you would do with `sqlcmd` in SQL Server.

<p><img style="margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/checkmark.png"><b>Steps</b></p>

**Step 1 — Connect to the cluster as the postgres superuser:**

```bash
psql -U postgres -h localhost -p 5432
```

You will be prompted for the password you set during installation. A successful connection displays the `postgres=#` prompt.

**Step 2 — List all databases (equivalent to `SELECT name FROM sys.databases`):**

```sql
\l
-- or the long form:
\list
```

You should see the default databases: `postgres`, `template0`, and `template1`. The `adventureworks` database you created in pre-requisites should also appear.

**Step 3 — Connect to the adventureworks database:**

```sql
\c adventureworks
```

The prompt changes to `adventureworks=#`.

**Step 4 — List all schemas (equivalent to `SELECT * FROM sys.schemas`):**

```sql
\dn
```

You should see the schemas you created: `humanresources`, `person`, `production`, `purchasing`, `sales`, and `public`.

**Step 5 — Explore system catalog views (equivalent to `sys.*` in SQL Server):**

```sql
-- List all tables in the public schema
\dt public.*

-- List all tables in all schemas
\dt *.*

-- The SQL Server equivalent:
-- SELECT * FROM sys.tables

-- Using information_schema (portable across databases):
SELECT table_schema, table_name
FROM information_schema.tables
WHERE table_type = 'BASE TABLE'
  AND table_schema NOT IN ('pg_catalog','information_schema')
ORDER BY table_schema, table_name;
```

**Step 6 — Query the pg_catalog for server version and connection info:**

```sql
SELECT version();

SELECT current_database(),
       current_user,
       inet_server_addr(),
       inet_server_port();
```

**Step 7 — List useful psql meta-commands (there is no SSMS toolbar here!):**

```sql
\?          -- help on psql backslash commands
\h SELECT   -- help on any SQL command
\timing     -- toggle query execution time display (like SSMS status bar)
\x          -- toggle expanded output (like flipping to column output)
\e          -- open last query in your editor (uses $EDITOR env var)
\i filename -- execute a SQL file (like sqlcmd -i)
\q          -- quit
```

<p style="border-bottom: 1px solid lightgrey;"></p>

<h2><img style="float: left; margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/pencil2.png">1.2 – Tour of pgAdmin 4 and DBeaver</h2>

**pgAdmin 4** is the standard PostgreSQL GUI, comparable to SSMS. It is a web-application that runs locally in your browser (served by a bundled Python web server). Key differences from SSMS to know about:

- The **Query Tool** is opened per-database by right-clicking a database and choosing "Query Tool."
- **Execution plans** are shown via the Explain / Explain Analyze buttons in the toolbar — the output is a graphical tree and a table of nodes, similar to SSMS's graphical plan.
- Server-level administration (roles, tablespaces, replication) lives under the server node.
- The **Dashboard** tab shows real-time activity equivalent to SQL Server's Activity Monitor.

**DBeaver Community** is recommended for side-by-side comparison work because you can have both a SQL Server and a PostgreSQL connection open simultaneously in separate editor tabs. The SQL auto-complete is dialect-aware, and the ER diagram tool works across both platforms.

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/point1.png"><b>Activity 1.2 – Explore pgAdmin 4 and Compare with SSMS</b></p>

<p><img style="margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/checkmark.png"><b>Description</b></p>

Open pgAdmin 4 and replicate the following SQL Server SSMS tasks in pgAdmin, noting where the equivalents are.

<p><img style="margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/checkmark.png"><b>Steps</b></p>

**Step 1 — Open pgAdmin and connect to your local PostgreSQL server.**

Launch pgAdmin from the Start menu. In the Browser panel on the left, expand **Servers → PostgreSQL 17 → Databases → adventureworks**. Note the parallel structure to SSMS's Object Explorer.

**Step 2 — Open the Query Tool and run a catalog query.**

Right-click the `adventureworks` database node, choose **Query Tool**, then run:

```sql
SELECT schemaname, tablename, tableowner
FROM pg_catalog.pg_tables
WHERE schemaname NOT IN ('pg_catalog','information_schema')
ORDER BY schemaname, tablename;
```

This is equivalent to browsing the Tables node in SSMS.

**Step 3 — View the Server Dashboard.**

Click the **adventureworks** database node, then click the **Dashboard** tab at the top. You will see graphs for connections, transactions per second, and block I/O. This is pgAdmin's equivalent of SSMS Activity Monitor.

**Step 4 — View current sessions (equivalent to SQL Server's sp_who2).**

In the Query Tool, run:

```sql
SELECT pid,
       usename,
       application_name,
       client_addr,
       state,
       query_start,
       left(query, 80) AS current_query
FROM pg_stat_activity
WHERE state <> 'idle'
ORDER BY query_start;
```

The `pg_stat_activity` view is PostgreSQL's equivalent of `sys.dm_exec_sessions` + `sys.dm_exec_requests`.

**Step 5 — Review the SSMS-to-pgAdmin equivalence table:**

| SSMS Task | pgAdmin Equivalent |
|---|---|
| Object Explorer | Browser panel |
| Query Editor | Query Tool (per-database) |
| Activity Monitor | Dashboard tab |
| Database Properties | Right-click database → Properties |
| New Login | Right-click Login/Group Roles → Create |
| Backup database | Right-click database → Backup |
| Table Designer | Table → Properties, or script DDL |
| Execution Plan | Explain / Explain Analyze toolbar button |

<p style="border-bottom: 1px solid lightgrey;"></p>

<h2><img style="float: left; margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/pencil2.png">1.3 – PostgreSQL Configuration Files</h2>

SQL Server configuration is managed primarily through SQL Server Configuration Manager and `sp_configure`. In PostgreSQL, configuration lives in two key text files inside the data directory:

**`postgresql.conf`** — The main parameter file. Equivalent to SQL Server's sp_configure settings. Important parameters you will encounter during the workshop:

```
# Memory
shared_buffers = 256MB          # SQL Server equivalent: max server memory (but much smaller)
work_mem = 4MB                  # Per-sort-or-hash memory — very different from SQL Server
effective_cache_size = 1GB      # Planner hint for OS cache

# Connections
max_connections = 100           # SQL Server manages this via thread pool dynamically

# Write-Ahead Log
wal_level = replica             # Enables streaming replication
max_wal_size = 1GB

# Query Planner
random_page_cost = 4.0          # Lower for SSD: set to 1.1
```

**`pg_hba.conf`** — The Host-Based Authentication file. Controls *who* can connect, from *where*, and *how* they authenticate. There is no direct SQL Server equivalent — this level of granularity is handled by SQL Server's firewall rules + login security combined. This file is covered in detail in Module 05.

You can query and change most parameters at runtime without a restart:

```sql
-- Show a configuration value (like sp_configure)
SHOW shared_buffers;
SHOW all;   -- Show all configuration parameters

-- Change a parameter for the current session
SET work_mem = '64MB';

-- Change a parameter permanently (writes to postgresql.conf, requires reload)
ALTER SYSTEM SET shared_buffers = '512MB';
SELECT pg_reload_conf();   -- Reload config without restart (for most parameters)
```

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/point1.png"><b>Activity 1.3 – Explore PostgreSQL Configuration</b></p>

<p><img style="margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/checkmark.png"><b>Steps</b></p>

**Step 1 — Find the data directory and config file locations:**

```sql
-- In psql or pgAdmin Query Tool:
SHOW data_directory;
SHOW config_file;
SHOW hba_file;
```

Open the `postgresql.conf` file in a text editor to inspect it. Note that it is heavily commented — the default values are shown next to each parameter name.

**Step 2 — Query the current parameter settings via SQL:**

```sql
SELECT name, setting, unit, short_desc
FROM pg_settings
WHERE name IN (
    'shared_buffers',
    'work_mem',
    'max_connections',
    'effective_cache_size',
    'random_page_cost',
    'wal_level',
    'log_min_duration_statement'
)
ORDER BY name;
```

The `pg_settings` view is the PostgreSQL equivalent of `sys.configurations`.

**Step 3 — Enable query logging for slow queries (equivalent to SQL Server Profiler's duration filter):**

```sql
-- Log any query taking longer than 1 second
ALTER SYSTEM SET log_min_duration_statement = 1000;  -- milliseconds
SELECT pg_reload_conf();

-- Verify:
SHOW log_min_duration_statement;
```

This writes slow queries to the PostgreSQL log file in the `log` subdirectory of your data directory.

<p style="border-bottom: 1px solid lightgrey;"></p>

<p><img style="margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/owl.png"><b>For Further Study</b></p>

- [PostgreSQL Documentation — Architecture](https://www.postgresql.org/docs/current/overview.html)
- [PostgreSQL Documentation — psql Reference](https://www.postgresql.org/docs/current/app-psql.html)
- [PostgreSQL Documentation — Server Configuration](https://www.postgresql.org/docs/current/runtime-config.html)
- [pgAdmin 4 Documentation](https://www.pgadmin.org/docs/pgadmin4/latest/)
- [EDB Blog — SQL Server vs. PostgreSQL Comparison](https://www.enterprisedb.com/blog/microsoft-sql-server-mssql-vs-postgresql-comparison-details-what-differences)
- [SQLpassion — Top 5 Differences Between SQL Server and PostgreSQL](https://www.sqlpassion.at/archive/2024/10/09/the-top-5-key-differences-between-sql-server-and-postgresql/)
- [Microsoft Learn — Azure Database for PostgreSQL Overview](https://learn.microsoft.com/en-us/azure/postgresql/)
- [PgBouncer — Connection Pooling for PostgreSQL](https://www.pgbouncer.org/)
- [DBeaver Community Edition](https://dbeaver.io/)

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/geopin.png"><b>Next Steps</b></p>

Next, continue to <a href="02_-_Data_Types_and_Schema_Design.md" target="_blank"><i>Module 02 – Data Types and Schema Design</i></a>.
