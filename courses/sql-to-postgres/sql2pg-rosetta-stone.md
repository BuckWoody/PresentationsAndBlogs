# PostgreSQL for the SQL Server Professional: A Rosetta Stone

**Course Reference Document**
**Edition: PostgreSQL 16 and SQL Server 2022**

---

## Table of Contents

1. [Architecture](#1-architecture)
2. [Installation and Configuration](#2-installation-and-configuration)
3. [Connectivity and Client Tools](#3-connectivity-and-client-tools)
4. [Data Types](#4-data-types)
5. [SQL Language and Syntax](#5-sql-language-and-syntax)
6. [Procedural Programming: T-SQL vs PL/pgSQL](#6-procedural-programming-t-sql-vs-plpgsql)
7. [Indexing](#7-indexing)
8. [Views, Materialized Views, and CTEs](#8-views-materialized-views-and-ctes)
9. [Partitioning](#9-partitioning)
10. [Security and Access Control](#10-security-and-access-control)
11. [Transactions and Concurrency](#11-transactions-and-concurrency)
12. [Administration and Maintenance](#12-administration-and-maintenance)
13. [Backup and Recovery](#13-backup-and-recovery)
14. [High Availability and Replication](#14-high-availability-and-replication)
15. [Performance Tuning and Query Optimization](#15-performance-tuning-and-query-optimization)
16. [System Catalogs and Metadata](#16-system-catalogs-and-metadata)
17. [JSON and Semi-Structured Data](#17-json-and-semi-structured-data)
18. [Full-Text Search](#18-full-text-search)
19. [Extensions and Ecosystem](#19-extensions-and-ecosystem)
20. [Operational Patterns and Anti-Patterns](#20-operational-patterns-and-anti-patterns)

---

## 1. Architecture

### 1.1 Process Model

| Concept | SQL Server | PostgreSQL | Notes |
|---|---|---|---|
| Process model | Threaded (single process, many threads) | Multi-process (one process per connection) | Fundamental architectural difference |
| Main service process | sqlservr.exe | postmaster | The postmaster is the supervisor process |
| Worker process per connection | Thread within sqlservr.exe | Backend process (postgres) | Each PG connection spawns a new OS process |
| Background workers | Internal threads (lazy writer, log writer, etc.) | Background worker processes (autovacuum, WAL writer, checkpointer, etc.) | Both support background parallelism |
| Connection overhead | Lower per-connection overhead due to threads | Higher per-connection overhead due to forking | This is why connection pooling is essential in PG |
| Shared memory | Buffer pool managed within process | Shared memory segments (shared_buffers, etc.) | PG uses POSIX shared memory by default |

### 1.2 Storage Architecture

| Concept | SQL Server | PostgreSQL | Notes |
|---|---|---|---|
| Data file unit | Page (8 KB) | Page (8 KB, default) | Both default to 8 KB pages; PG can be compiled with 4/16/32 KB |
| Extent | 8 pages (64 KB) -- uniform or mixed | No direct equivalent | PG uses free space map (FSM) and visibility map (VM) instead |
| Data file extension | .mdf, .ndf | No named extension; base/OID/relfilenode | PG uses numbered files under the data directory |
| Log file | .ldf (sequential, circular) | WAL files (pg_wal directory, 16 MB segments by default) | Both are write-ahead logs; PG WAL is append-only segments |
| File groups | File groups (PRIMARY, user-defined) | Tablespaces | PG tablespaces map to OS directories |
| tempdb equivalent | tempdb (shared, pre-allocated) | pg_temp schema per session | PG temp tables/objects are per-session in a shared temp tablespace |
| Row versioning store | Version store in tempdb | In-table (dead tuples, MVCC via heap) | PG stores old row versions inline in the heap -- major design difference |
| Fill factor | Fill factor on indexes | Fill factor on tables and indexes | Both support configuring free space per page |
| Page splits | B-tree page splits move rows | B-tree page splits; heap pages fill up with dead tuples | PG heap never physically reorganizes on UPDATE -- it writes a new tuple |

### 1.3 Database and Instance Hierarchy

| Concept | SQL Server | PostgreSQL | Notes |
|---|---|---|---|
| Top-level unit | Instance | Cluster (database cluster) | A PG "cluster" is one postmaster managing one data directory |
| Logical database | Database | Database | Both support multiple databases per instance/cluster |
| Namespace within database | Schema | Schema | Both support schemas; PG search_path controls resolution |
| Cross-database query | Three-part name: db.schema.table | Not supported natively (use dblink or foreign data wrappers) | Major limitation of PG; cross-db requires extension |
| Cross-server query | Linked Server | Foreign Data Wrapper (FDW) | PG's FDW is standards-based (SQL/MED); very flexible |
| Default schema | dbo | public | PG uses search_path to find objects across schemas |
| System databases | master, msdb, model, tempdb | postgres, template0, template1 | postgres is for admin connections; template0/template1 are templates |
| Template database | model | template1 | New databases are cloned from template1 by default |
| Clean template | No direct equivalent | template0 | template0 cannot be connected to; guaranteed clean state |
| Object naming | [schema].[object] with brackets for reserved words | "schema"."object" with double quotes | PG is case-sensitive for quoted identifiers; unquoted folds to lowercase |

### 1.4 MVCC (Multi-Version Concurrency Control)

This is one of the most important architectural differences. SQL Server uses a pessimistic locking model by default with an optional optimistic model using the version store in tempdb. PostgreSQL uses MVCC exclusively and always has.

| Concept | SQL Server | PostgreSQL | Notes |
|---|---|---|---|
| Concurrency model | Lock-based by default; RCSI/SI optional | MVCC always | PG readers never block writers; writers never block readers |
| Row version storage | tempdb version store (with RCSI/SI) | Inline in heap (dead tuples) | PG stores old versions in the same table data files |
| Transaction ID | Internal integer | xmin and xmax columns on every row | Every PG row has hidden system columns tracking visibility |
| Visibility columns | Not user-visible | xmin, xmax, ctid, tableoid are user-accessible | SELECT xmin, xmax, ctid, * FROM mytable; -- works in PG |
| Dead tuple cleanup | Version store automatically reclaimed | VACUUM required to reclaim dead tuple space | This is why VACUUM is critical in PG but has no SQL Server equivalent |
| Transaction ID wraparound | Not a concern | XID wraparound is a real operational risk | PG XID is a 32-bit integer; must VACUUM to prevent wraparound |
| Snapshot isolation | SET TRANSACTION ISOLATION LEVEL SNAPSHOT | Default behavior of REPEATABLE READ | PG's REPEATABLE READ is actually snapshot isolation |

### 1.5 Write-Ahead Logging (WAL)

| Concept | SQL Server | PostgreSQL | Notes |
|---|---|---|---|
| Log name | Transaction Log (.ldf) | Write-Ahead Log (WAL) in pg_wal/ | Same concept, different implementation |
| Log record unit | Log Record | WAL Record | Both are byte sequences describing changes |
| Log file size | Grows dynamically (pre-allocated VLFs) | Fixed 16 MB segment files (configurable at initdb) | PG segment size set once at cluster creation; default 16 MB |
| Log archiving | Log Shipping / Backup Log | archive_command / pg_receivewal | PG archives WAL segments to a directory or command |
| Log sequence number | LSN (Log Sequence Number) | LSN (Log Sequence Number) | Both use LSNs; PG LSNs are displayed as XX/XXXXXXXX hex |
| Checkpoint | Checkpoint (full/indirect) | Checkpoint | Both flush dirty pages and advance the redo point |
| Checkpoint frequency | Recovery interval / indirect checkpoint | checkpoint_timeout and max_wal_size | PG checkpoint triggered by time or WAL volume |
| Log recovery mode | SIMPLE / BULK_LOGGED / FULL | N/A (WAL always retained based on wal_keep_size or slots) | PG does not have recovery models; WAL is always full |
| Forced log write | CHECKPOINT statement | CHECKPOINT statement | Works the same way in both |

---

## 2. Installation and Configuration

### 2.1 Service Management

| Task | SQL Server | PostgreSQL | Notes |
|---|---|---|---|
| Start service (Windows) | net start MSSQLSERVER / SQL Server Configuration Manager | net start postgresql-x64-16 / pg_ctl start | PG on Windows uses the same service infrastructure |
| Start service (Linux) | systemctl start mssql-server | systemctl start postgresql-16 | Both support systemd on modern Linux |
| Initialize data directory | Handled by installer | initdb -D /var/lib/postgresql/16/main | Must be run as the postgres OS user |
| Service account | MSSQLSERVER service account | postgres OS user | PG runs as the postgres OS user by default |
| Data directory | Configured during install (typically C:\Program Files\Microsoft SQL Server\...) | PGDATA environment variable (e.g., /var/lib/postgresql/16/main) | PGDATA is the central concept in PG |
| Listen address | Configured in SQL Server Configuration Manager | listen_addresses in postgresql.conf | Set to '*' to listen on all interfaces |
| Default port | 1433 | 5432 | Both are well-known ports |
| Named instances | Supported (INSTANCE_NAME) | One cluster per port (use different ports) | PG has no "named instance" concept; use separate port numbers |
| Multiple instances | Supported with named instances | One postmaster per data directory / port | Run separate postmaster processes on different ports |

### 2.2 Configuration Files

PostgreSQL uses flat text configuration files. SQL Server uses a mix of registry settings, startup parameters, and sp_configure.

| Configuration Element | SQL Server | PostgreSQL | Location / Notes |
|---|---|---|---|
| Main config file | Registry and startup parameters | postgresql.conf | Located in PGDATA directory |
| Server startup parameters | SQL Server Configuration Manager | postgresql.conf | Editable as text; requires reload or restart |
| Host-based auth (login rules) | Not applicable -- SQL logins or Windows auth | pg_hba.conf | Controls WHO can connect FROM WHERE using WHICH method |
| Authentication ident map | Not applicable | pg_ident.conf | Maps OS usernames to PG usernames for ident/peer auth |
| Recovery configuration | N/A | postgresql.conf (recovery_* params), standby.signal, recovery.signal | Modern PG (12+) merged recovery.conf into postgresql.conf |
| Applying config changes | Many require restart; some dynamic via sp_configure | pg_reload_conf() or SELECT pg_reload_conf(); or SIGHUP | Many PG params reload without restart; some require restart |
| View current settings | sys.configurations | pg_settings (system view) | SELECT name, setting, unit FROM pg_settings; |
| Show a specific setting | EXEC sp_configure 'max degree of parallelism' | SHOW max_connections; or SELECT current_setting('work_mem'); | |
| Change a setting dynamically | EXEC sp_configure / RECONFIGURE | SET work_mem = '256MB'; (session) or ALTER SYSTEM SET work_mem='256MB'; | ALTER SYSTEM writes to postgresql.auto.conf |
| Session-level setting | SET options | SET config_param = value; | Both scoped to session |
| Configuration file override | N/A | postgresql.auto.conf (written by ALTER SYSTEM) | Auto.conf takes precedence over postgresql.conf; do not edit manually |

### 2.3 Key Configuration Parameters

| Parameter | SQL Server Equivalent | PostgreSQL Parameter | Recommended Starting Point |
|---|---|---|---|
| Memory for data caching | max server memory | shared_buffers | 25% of total RAM |
| Memory for sort/hash per query | No direct per-query equivalent | work_mem | 4-16 MB default; multiply by max_connections for total potential usage |
| Memory for maintenance ops | Sort memory for index builds | maintenance_work_mem | 64-256 MB; affects VACUUM, CREATE INDEX, etc. |
| Max concurrent connections | max connections | max_connections | Consider pgBouncer for connection pooling |
| Write-ahead log level | N/A (always logs everything) | wal_level | minimal, replica, or logical -- must be at least replica for replication |
| Checkpointing | recovery interval | checkpoint_timeout / max_wal_size | 5min / 1GB defaults; tune for write workloads |
| Effective cache size hint | N/A | effective_cache_size | Set to approx. 75% of total RAM; planner hint only, not allocation |
| Parallel query workers | MAXDOP | max_parallel_workers_per_gather | 0 = disabled; PG parallel query since version 10 |
| Random page cost | Not tunable per se | random_page_cost | Set to 1.1 on SSD, 4.0 on spinning disk; affects index vs. seq scan |
| Autovacuum | No equivalent | autovacuum = on | Never disable autovacuum in production |
| Statistics target | Statistics sample rate | default_statistics_target | 100 default; increase for skewed distributions |
| Log slow queries | Extended Events / Profiler | log_min_duration_statement | Set to 1000 for logging queries over 1 second |
| Log query plans | Actual execution plan via GUI | auto_explain extension | Logs actual plans for slow queries automatically |

### 2.4 pg_hba.conf -- Authentication Configuration

This file has no equivalent in SQL Server. It is the access control list for the PostgreSQL connection layer.

```
# TYPE  DATABASE  USER    ADDRESS         METHOD
local   all       all                     peer        # Unix socket connections, OS user = PG user
host    all       all     127.0.0.1/32    scram-sha-256
host    all       all     ::1/128         scram-sha-256
host    mydb      myuser  10.0.0.0/8      scram-sha-256
hostssl all       all     0.0.0.0/0       scram-sha-256
```

Authentication methods include: trust, reject, peer, ident, password, md5, scram-sha-256, gss, sspi, ldap, radius, cert.

The equivalent in SQL Server is a combination of SQL Server login authentication (SQL auth or Windows auth), the firewall, and login triggers. In PostgreSQL, pg_hba.conf does all of this in one place.

---

## 3. Connectivity and Client Tools

### 3.1 Client Tools Comparison

| Tool / Purpose | SQL Server | PostgreSQL | Notes |
|---|---|---|---|
| Primary GUI tool | SQL Server Management Studio (SSMS) | pgAdmin 4, DBeaver, DataGrip | No single dominant GUI; pgAdmin 4 is the official tool |
| Command-line client | sqlcmd | psql | psql is extremely capable; heavily used in practice |
| Scripting / automation | sqlcmd, PowerShell (dbatools) | psql, pg_dump, pg_restore, pgAdmin scripts | |
| Performance monitoring GUI | Activity Monitor, SSMS Reports | pgAdmin Dashboard, pg_activity (CLI), Datadog, etc. | No built-in equivalent to SSMS performance dashboards |
| Query plan display | Estimated/Actual Execution Plan in SSMS | EXPLAIN / EXPLAIN (ANALYZE, BUFFERS) in psql or pgAdmin | |
| Index advisor | Database Engine Tuning Advisor | No built-in; pg_qualstats + HypoPG extension | Third-party tools like pganalyze fill this gap |
| Profiler / trace | SQL Server Profiler, Extended Events | pg_stat_statements, auto_explain, pgBadger | No real-time session trace like Profiler; use pg_stat_statements |
| ODBC driver | SQL Server Native Client / ODBC Driver | PostgreSQL ODBC driver (psqlODBC) | Both are ODBC-compliant |
| .NET driver | Microsoft.Data.SqlClient | Npgsql | Npgsql is mature and high performance |
| Python driver | pyodbc / pymssql | psycopg2 / psycopg3 (asyncpg for async) | psycopg2 is the standard; psycopg3 is the modern replacement |
| Java driver | SQL Server JDBC | PostgreSQL JDBC (pgjdbc) | |
| ORM support | Entity Framework Core, Hibernate | Same ORMs support PG via their PG providers | Full ORM support across all major frameworks |

### 3.2 psql Essentials for the SQL Server Professional

psql is the command-line client. It uses backslash metacommands that have no equivalent in sqlcmd but are very powerful.

| Task | sqlcmd | psql | Notes |
|---|---|---|---|
| Connect to server | sqlcmd -S server -U user -P pass -d db | psql -h host -U user -d dbname | Environment vars: PGHOST, PGUSER, PGDATABASE, PGPASSWORD |
| Run a script file | sqlcmd -i script.sql | psql -f script.sql | |
| Run inline SQL | sqlcmd -Q "SELECT 1" | psql -c "SELECT 1" | |
| List databases | SELECT name FROM sys.databases | \l or \list | |
| List tables | SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES | \dt or \dt schema.* | \dt+ shows size and description |
| List all objects | N/A (use SSMS) | \d | Shows tables, views, sequences |
| Describe a table | sp_help tablename | \d tablename or \d+ tablename | \d+ includes storage and description |
| List schemas | SELECT name FROM sys.schemas | \dn | |
| List indexes | sys.indexes | \di | |
| List functions | sys.objects where type='FN' | \df | |
| List users/roles | sys.server_principals | \du | |
| Toggle output format | N/A | \x (expanded), \t (tuples only) | \x is like pivoting the output vertically |
| Time a query | SET STATISTICS TIME ON | \timing on | Both display elapsed time |
| Set output to file | sqlcmd -o output.txt | \o output.txt | |
| Edit current query | N/A | \e (opens $EDITOR) | Very useful for long queries |
| Previous command | Up arrow in sqlcmd | Up arrow or \g (re-execute) | psql keeps a history file |
| Show current settings | N/A | \conninfo | Displays current connection details |
| Execute and quit | GO (batch terminator) | \q or \quit | GO is a batch separator, not SQL |
| Transaction control | BEGIN / COMMIT / ROLLBACK | BEGIN / COMMIT / ROLLBACK | PG auto-wraps psql statements in transactions unless -c is used |
| Password file | N/A (use Windows auth or -P) | ~/.pgpass file | Format: hostname:port:database:username:password |

### 3.3 Connection Strings

**SQL Server:**
```
Server=myserver;Database=mydb;User Id=myuser;Password=mypassword;
```

**PostgreSQL:**
```
Host=myserver;Database=mydb;Username=myuser;Password=mypassword;Port=5432;
```

**PostgreSQL URI format (also supported):**
```
postgresql://myuser:mypassword@myserver:5432/mydb
```

**PostgreSQL connection string with SSL:**
```
Host=myserver;Database=mydb;Username=myuser;Password=mypassword;SSL Mode=Require;
```

---

## 4. Data Types

### 4.1 Numeric Types

| SQL Server Type | PostgreSQL Equivalent | Notes |
|---|---|---|
| TINYINT (0-255, 1 byte) | SMALLINT (or use CHECK constraint) | PG has no unsigned integer types; use SMALLINT with CHECK |
| SMALLINT (2 bytes) | SMALLINT | Identical |
| INT / INTEGER (4 bytes) | INTEGER or INT | Identical |
| BIGINT (8 bytes) | BIGINT | Identical |
| DECIMAL(p,s) / NUMERIC(p,s) | NUMERIC(p,s) or DECIMAL(p,s) | Identical behavior; arbitrary precision |
| FLOAT(n) | DOUBLE PRECISION or REAL | FLOAT in PG is an alias for DOUBLE PRECISION |
| REAL (4 bytes) | REAL | Identical |
| MONEY | NUMERIC(19,4) | PG has no MONEY type per se; use NUMERIC. Avoid PG's "money" type due to locale issues |
| SMALLMONEY | NUMERIC(10,4) | Same recommendation |
| BIT | BOOLEAN | SQL Server BIT stores 0/1; PG BOOLEAN stores true/false |
| Auto-increment (IDENTITY) | SERIAL / BIGSERIAL / SMALLSERIAL or GENERATED ALWAYS AS IDENTITY | SERIAL is legacy shorthand; prefer GENERATED ALWAYS AS IDENTITY (SQL standard) |

**Auto-increment examples:**

SQL Server:
```sql
CREATE TABLE orders (
    order_id INT IDENTITY(1,1) PRIMARY KEY,
    order_date DATE
);
```

PostgreSQL (legacy SERIAL):
```sql
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    order_date DATE
);
```

PostgreSQL (preferred -- SQL Standard):
```sql
CREATE TABLE orders (
    order_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    order_date DATE
);
```

### 4.2 String / Character Types

| SQL Server Type | PostgreSQL Equivalent | Notes |
|---|---|---|
| CHAR(n) | CHAR(n) or CHARACTER(n) | Fixed-length, space-padded; identical behavior |
| VARCHAR(n) | VARCHAR(n) or CHARACTER VARYING(n) | Variable length; identical |
| VARCHAR(MAX) | TEXT | PG TEXT is unlimited length; no VARCHAR(MAX) syntax |
| NCHAR(n) | CHAR(n) | PG is always Unicode (UTF-8); no separate N-prefixed types |
| NVARCHAR(n) | VARCHAR(n) | PG does not distinguish Unicode vs. non-Unicode types |
| NVARCHAR(MAX) | TEXT | Same as above |
| SYSNAME | NAME | PG NAME type is 63 bytes; used for identifiers internally |
| XML | XML | Both support XML; PG XML type has basic validation |
| UNIQUEIDENTIFIER | UUID | PG UUID is a native type; formatted as xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx |
| STRING_SPLIT (function) | string_to_array() or regexp_split_to_table() | Not a type, but a common pattern |
| Collation (per column or db) | COLLATE clause | COLLATE clause; PG also supports ICU collations since v10 |
| Case-insensitive comparison | Collation-based (e.g., SQL_Latin1_General_CP1_CI_AS) | citext extension or ILIKE operator or LOWER() | PG default is case-sensitive; citext is the cleanest solution |
| String concatenation | + operator | \|\| operator | CONCAT() function works in both; be careful with NULLs and + in SQL Server |

### 4.3 Date and Time Types

| SQL Server Type | PostgreSQL Equivalent | Notes |
|---|---|---|
| DATE | DATE | Identical; YYYY-MM-DD |
| TIME(n) | TIME(n) or TIME WITH TIME ZONE (TIMETZ) | TIMETZ is allowed but rarely recommended |
| DATETIME | TIMESTAMP | DATETIME has 3ms precision; TIMESTAMP has microsecond precision |
| DATETIME2(n) | TIMESTAMP(n) | Very similar; TIMESTAMP(6) is microsecond precision |
| DATETIMEOFFSET | TIMESTAMP WITH TIME ZONE (TIMESTAMPTZ) | TIMESTAMPTZ stores in UTC and converts on display; DATETIMEOFFSET stores the offset |
| SMALLDATETIME | TIMESTAMP(0) | No exact equivalent; use TIMESTAMP with reduced precision |
| Current date/time | GETDATE() or SYSDATETIME() | NOW() or CURRENT_TIMESTAMP | NOW() returns TIMESTAMPTZ; LOCALTIMESTAMP returns TIMESTAMP |
| UTC current time | GETUTCDATE() or SYSUTCDATETIME() | NOW() AT TIME ZONE 'UTC' or CURRENT_TIMESTAMP (already UTC in TIMESTAMPTZ) | |
| Date arithmetic | DATEADD(day, 7, mydate) | mydate + INTERVAL '7 days' or mydate + 7 | PG interval arithmetic is very expressive |
| Date difference | DATEDIFF(day, start, end) | end - start (returns INTEGER for dates) or AGE(end, start) | |
| Date parts | DATEPART(year, mydate), YEAR() | EXTRACT(year FROM mydate) or DATE_PART('year', mydate) | |
| Format date as string | FORMAT(mydate, 'yyyy-MM-dd') | TO_CHAR(mydate, 'YYYY-MM-DD') | TO_CHAR is the workhorse for date formatting in PG |
| Parse string to date | CONVERT(DATE, '2024-01-15') | TO_DATE('2024-01-15', 'YYYY-MM-DD') or '2024-01-15'::DATE | |
| Infinity | N/A | 'infinity'::TIMESTAMP and '-infinity'::TIMESTAMP | PG supports temporal infinity values |

### 4.4 Binary Types

| SQL Server Type | PostgreSQL Equivalent | Notes |
|---|---|---|
| BINARY(n) | BYTEA | PG BYTEA is variable-length binary; no fixed-length binary |
| VARBINARY(n) | BYTEA | All binary in PG is BYTEA |
| VARBINARY(MAX) | BYTEA | No size limit distinction; all is BYTEA |
| IMAGE (deprecated) | BYTEA | |
| Store large binary externally | FILESTREAM | Large Object (lo) API or external storage | PG lo stores in pg_largeobject system table |

### 4.5 PostgreSQL-Specific Types (No SQL Server Equivalent)

These types are powerful and frequently used. SQL Server professionals should learn them.

| PostgreSQL Type | Description | Example Usage |
|---|---|---|
| JSONB | Binary JSON (indexed, parsed) | Storing schemaless documents; very common in modern PG apps |
| JSON | Text JSON (stored as-is) | Use JSONB instead in almost all cases |
| ARRAY | Native arrays of any type | INT[], TEXT[], etc. -- column can hold multiple values |
| HSTORE | Key-value text pairs | Extension; largely superseded by JSONB |
| INET | IPv4 or IPv6 address | Includes network operators and functions |
| CIDR | Network address (host portion must be zero) | Useful for storing network ranges |
| MACADDR | MAC address | Stored as 6-byte hardware address |
| TSVECTOR | Text search vector | Used for full-text search |
| TSQUERY | Text search query | Used for full-text search |
| RANGE types | int4range, tsrange, daterange, etc. | Ranges with inclusion/exclusion; support overlap operators |
| MULTIRANGE types | int4multirange, etc. (PG 14+) | Multiple non-contiguous ranges in one value |
| POINT, LINE, LSEG, BOX, CIRCLE, POLYGON | Geometric types | Native geometry without PostGIS for simple cases |
| INTERVAL | Time span | INTERVAL '1 year 3 months 7 days' |
| BIT(n), BIT VARYING(n) | Bit strings | Not the same as BOOLEAN |
| ENUM | User-defined ordered list of labels | CREATE TYPE mood AS ENUM ('sad', 'ok', 'happy') |
| COMPOSITE type | Row type | Can store a complete row as a column value |
| OID | Object identifier | Internal PG system identifier; rarely used in application code |
| MONEY | Currency with locale | Avoid; use NUMERIC instead due to locale-sensitivity issues |
| XML | XML document | Basic XML support; use for XML data |
| UUID | Universally Unique Identifier | gen_random_uuid() built-in since PG 13 |

### 4.6 Type Casting

| Operation | SQL Server | PostgreSQL | Notes |
|---|---|---|---|
| Explicit cast | CAST(value AS type) or CONVERT(type, value) | CAST(value AS type) or value::type | The :: operator is PG-specific shorthand; very common |
| Implicit cast | Often happens automatically | More strict; often requires explicit cast | PG will not silently convert VARCHAR to INT |
| String to integer | CAST('123' AS INT) | '123'::INTEGER or CAST('123' AS INTEGER) | |
| Integer to string | CAST(123 AS VARCHAR) | 123::TEXT or CAST(123 AS TEXT) | |
| Timestamp to date | CAST(myts AS DATE) | myts::DATE | |

---

## 5. SQL Language and Syntax

### 5.1 Core SELECT Differences

| Feature | SQL Server | PostgreSQL | Notes |
|---|---|---|---|
| Case sensitivity (strings) | Case-insensitive by default (collation-dependent) | Case-sensitive by default | This trips up many SQL Server professionals |
| Identifier quoting | [square brackets] or "double quotes" | "double quotes" only | PG uses standard SQL double-quote quoting |
| Identifier case folding | Identifiers are case-insensitive | Unquoted identifiers fold to lowercase | CREATE TABLE MyTable and mytable are the same object in PG |
| SELECT without FROM | SELECT 1, GETDATE() | SELECT 1, NOW() | PG does not require FROM for constant expressions |
| TOP n rows | SELECT TOP 10 * FROM t | SELECT * FROM t LIMIT 10 | |
| TOP with percent | SELECT TOP 10 PERCENT * FROM t | No direct equivalent; calculate manually | |
| Paging / Offset | OFFSET x ROWS FETCH NEXT y ROWS ONLY (SQL Server 2012+) or older TOP / ROW_NUMBER() | LIMIT y OFFSET x | LIMIT/OFFSET is simpler; OFFSET/FETCH also works in PG (SQL standard) |
| INTO (select into table) | SELECT * INTO newtable FROM src | CREATE TABLE newtable AS SELECT * FROM src | |
| Table hints | WITH (NOLOCK), WITH (HOLDLOCK) | No hints; use isolation levels | PG MVCC eliminates the need for NOLOCK |
| Query hints | OPTION (MAXDOP 1), OPTION (RECOMPILE) | No query hints in standard SQL; use config params | PG has no equivalent to OPTION clause |
| Force index | WITH (INDEX(idx_name)) | No direct equivalent; pg_hint_plan extension | pg_hint_plan is a third-party extension |
| Wildcard | % and _ for LIKE | % and _ for LIKE (same) | PG also supports SIMILAR TO and full regex with ~ |
| Regular expression | LIKE only (no native regex) | ~ (match), ~* (case-insensitive), !~ (not match) | PG has native POSIX regex operators |
| String comparison | Case-insensitive by default | Case-sensitive by default | Use ILIKE for case-insensitive pattern matching in PG |
| NULL handling | IS NULL / IS NOT NULL, ISNULL(), COALESCE() | IS NULL / IS NOT NULL, COALESCE() | PG has no ISNULL() function; use COALESCE() |
| NVL / ISNULL | ISNULL(a, b) | COALESCE(a, b) or a IS NOT DISTINCT FROM b | COALESCE works in both |
| NULL equality | NULL != NULL (use IS NULL) | NULL IS DISTINCT FROM NULL is true | IS NOT DISTINCT FROM is useful for nullable comparisons |
| EXCEPT | EXCEPT | EXCEPT | Same behavior |
| INTERSECT | INTERSECT | INTERSECT | Same behavior |
| PIVOT | PIVOT ... FOR ... IN | crosstab() function via tablefunc extension | PG has no native PIVOT; use conditional aggregation or crosstab |
| FOR XML | FOR XML RAW / AUTO / EXPLICIT / PATH | xmlagg(), xmlelement(), xmlforest() | Different syntax; PG uses standard SQL/XML functions |
| FOR JSON | FOR JSON PATH / AUTO | row_to_json(), json_agg(), jsonb_build_object() | |

### 5.2 Joins

| Join Type | SQL Server | PostgreSQL | Notes |
|---|---|---|---|
| INNER JOIN | INNER JOIN or JOIN | INNER JOIN or JOIN | Identical |
| LEFT OUTER JOIN | LEFT JOIN | LEFT JOIN | Identical |
| RIGHT OUTER JOIN | RIGHT JOIN | RIGHT JOIN | Identical |
| FULL OUTER JOIN | FULL OUTER JOIN | FULL OUTER JOIN | Identical |
| CROSS JOIN | CROSS JOIN | CROSS JOIN | Identical |
| SELF JOIN | Table alias technique | Table alias technique | Identical |
| NATURAL JOIN | Not supported | NATURAL JOIN | Joins on all columns with same name; use with caution |
| LATERAL JOIN | CROSS APPLY / OUTER APPLY | CROSS JOIN LATERAL / LEFT JOIN LATERAL | LATERAL allows subquery to reference outer query row |
| APPLY operator | CROSS APPLY, OUTER APPLY | CROSS JOIN LATERAL, LEFT JOIN LATERAL | LATERAL is the SQL standard; very powerful in PG |

### 5.3 Aggregates and Grouping

| Feature | SQL Server | PostgreSQL | Notes |
|---|---|---|---|
| Standard aggregates | SUM, COUNT, AVG, MIN, MAX | SUM, COUNT, AVG, MIN, MAX | Identical |
| COUNT(DISTINCT col) | COUNT(DISTINCT col) | COUNT(DISTINCT col) | Identical |
| STRING_AGG | STRING_AGG(col, ',') SQL Server 2017+ | STRING_AGG(col, ',') | Identical; PG also has array_agg() |
| Array aggregation | N/A | ARRAY_AGG(col) | Returns a native array |
| JSON aggregation | FOR JSON PATH | JSON_AGG(col) or JSONB_AGG(col) | |
| Aggregate into string | FOR XML PATH('') hack or STRING_AGG | STRING_AGG(col, ',') | |
| HAVING | HAVING | HAVING | Identical |
| ROLLUP | GROUP BY ROLLUP(...) | GROUP BY ROLLUP(...) | Identical |
| CUBE | GROUP BY CUBE(...) | GROUP BY CUBE(...) | Identical |
| GROUPING SETS | GROUP BY GROUPING SETS(...) | GROUP BY GROUPING SETS(...) | Identical |
| GROUPING() function | GROUPING() | GROUPING() | Identical |
| DISTINCT ON | Not supported | SELECT DISTINCT ON (col) * FROM t ORDER BY col, other | Very powerful; returns first row per distinct value |
| Filter within aggregate | N/A (use CASE) | FILTER (WHERE condition) | SELECT COUNT(*) FILTER (WHERE status='active') FROM t |
| Ordered-set aggregates | PERCENTILE_CONT, PERCENTILE_DISC | PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY col) | Identical SQL standard syntax |
| Hypothetical-set aggregates | RANK() (as a function of a hypothetical value) | RANK(val) WITHIN GROUP (ORDER BY col) | Less common; PG supports the full SQL standard |
| Statistics aggregates | N/A | CORR(), COVAR_POP(), REGR_* functions | PG includes statistical aggregate functions |

### 5.4 Window Functions

Both platforms support window functions, and the syntax is largely identical. Key differences are noted.

| Feature | SQL Server | PostgreSQL | Notes |
|---|---|---|---|
| Basic window function | OVER (PARTITION BY col ORDER BY col) | OVER (PARTITION BY col ORDER BY col) | Identical |
| ROW_NUMBER | ROW_NUMBER() OVER (...) | ROW_NUMBER() OVER (...) | Identical |
| RANK / DENSE_RANK | RANK() / DENSE_RANK() OVER (...) | RANK() / DENSE_RANK() OVER (...) | Identical |
| NTILE | NTILE(n) OVER (...) | NTILE(n) OVER (...) | Identical |
| LAG / LEAD | LAG(col, offset, default) | LAG(col, offset, default) | Identical |
| FIRST_VALUE / LAST_VALUE | FIRST_VALUE / LAST_VALUE OVER (...) | FIRST_VALUE / LAST_VALUE OVER (...) | Identical |
| NTH_VALUE | Not supported | NTH_VALUE(col, n) OVER (...) | PG extension beyond SQL Server |
| Frame specification | ROWS / RANGE BETWEEN ... | ROWS / RANGE / GROUPS BETWEEN ... | PG adds GROUPS mode (group of peer rows) |
| Named window | Not supported | WINDOW w AS (PARTITION BY col) ... OVER w | Reuse window definition with named WINDOW clause |
| Window on aggregate | SUM(col) OVER (PARTITION BY ...) | SUM(col) OVER (PARTITION BY ...) | Identical |
| Running total | SUM(col) OVER (ORDER BY id ROWS UNBOUNDED PRECEDING) | SUM(col) OVER (ORDER BY id) | PG default frame is RANGE UNBOUNDED PRECEDING when ORDER BY used |

### 5.5 DML Statements

| Operation | SQL Server | PostgreSQL | Notes |
|---|---|---|---|
| INSERT | INSERT INTO t (cols) VALUES (...) | INSERT INTO t (cols) VALUES (...) | Identical |
| Multi-row INSERT | INSERT INTO t VALUES (...), (...), (...) | INSERT INTO t VALUES (...), (...), (...) | Both support multi-row INSERT |
| INSERT ... SELECT | INSERT INTO t SELECT ... | INSERT INTO t SELECT ... | Identical |
| OUTPUT clause | INSERT ... OUTPUT INSERTED.id | INSERT ... RETURNING id | RETURNING is the PG equivalent of OUTPUT |
| UPDATE | UPDATE t SET col = val WHERE ... | UPDATE t SET col = val WHERE ... | Identical |
| UPDATE from join | UPDATE t SET col = s.val FROM src s WHERE t.id = s.id | UPDATE t SET col = s.val FROM src s WHERE t.id = s.id | Identical (PG supports FROM in UPDATE) |
| UPDATE with OUTPUT | UPDATE t SET ... OUTPUT DELETED.*, INSERTED.* | UPDATE t SET ... RETURNING * | RETURNING returns the new values by default |
| DELETE | DELETE FROM t WHERE ... | DELETE FROM t WHERE ... | Identical |
| DELETE with OUTPUT | DELETE FROM t OUTPUT DELETED.* WHERE ... | DELETE FROM t WHERE ... RETURNING * | |
| TRUNCATE | TRUNCATE TABLE t | TRUNCATE TABLE t | PG TRUNCATE can also RESTART IDENTITY and CASCADE |
| MERGE | MERGE target USING source ON ... WHEN MATCHED ... | INSERT ... ON CONFLICT DO UPDATE (upsert) or full MERGE (PG 15+) | PG 15 added standard MERGE; ON CONFLICT is the idiomatic upsert |
| Upsert pattern | MERGE statement | INSERT ... ON CONFLICT (col) DO UPDATE SET ... | |
| Upsert ignore | MERGE / TRY-CATCH | INSERT ... ON CONFLICT DO NOTHING | |
| Bulk insert | BULK INSERT / bcp | COPY command | COPY is very fast; psql \copy works over the client connection |

### 5.6 DDL Statements

| Operation | SQL Server | PostgreSQL | Notes |
|---|---|---|---|
| Create table | CREATE TABLE | CREATE TABLE | Very similar; PG has more type options |
| Temporary table | CREATE TABLE #tmp | CREATE TEMP TABLE tmp or CREATE TEMPORARY TABLE tmp | PG temp tables are session-scoped and visible only to that session |
| Global temp table | CREATE TABLE ##globaltmp | No direct equivalent | Share data via regular tables or unlogged tables |
| Unlogged table | N/A | CREATE UNLOGGED TABLE | Faster (no WAL overhead); data lost on crash; good for staging |
| Table with OIDs | N/A (legacy) | Legacy; OIDs not added by default since PG 12 | Historical artifact; ignore unless maintaining old code |
| Add column | ALTER TABLE t ADD col TYPE | ALTER TABLE t ADD COLUMN col TYPE | COLUMN keyword is optional in both |
| Drop column | ALTER TABLE t DROP COLUMN col | ALTER TABLE t DROP COLUMN col | Identical; PG supports CASCADE to drop dependent objects |
| Rename column | sp_rename or ALTER TABLE ... | ALTER TABLE t RENAME COLUMN old TO new | |
| Change column type | ALTER TABLE t ALTER COLUMN col TYPE | ALTER TABLE t ALTER COLUMN col TYPE new_type | PG may require USING clause to convert data |
| Computed column | col AS (expression) [PERSISTED] | GENERATED ALWAYS AS (expression) STORED | PG only supports STORED (physically written); no virtual computed columns |
| Default value | DEFAULT constraint | DEFAULT expression | Identical concept; PG defaults can be arbitrary expressions |
| Add constraint | ALTER TABLE t ADD CONSTRAINT | ALTER TABLE t ADD CONSTRAINT | Identical |
| Check constraint | CHECK (expression) | CHECK (expression) | Identical; PG checks are only enforced on INSERT and UPDATE, not ALTER |
| NOT VALID constraint | N/A | ADD CONSTRAINT ... NOT VALID | Add constraint without checking existing rows; validate later |
| Validate constraint | N/A | VALIDATE CONSTRAINT constraint_name | Validates NOT VALID constraint with less locking |
| CREATE INDEX CONCURRENTLY | CREATE INDEX WITH (ONLINE=ON) | CREATE INDEX CONCURRENTLY | PG CONCURRENTLY takes longer but does not block writes |
| DROP INDEX CONCURRENTLY | ALTER INDEX ... DISABLE or DROP INDEX | DROP INDEX CONCURRENTLY | |
| Rename object | sp_rename | ALTER TABLE / INDEX / SEQUENCE / VIEW ... RENAME TO | PG has ALTER ... RENAME TO for most objects |
| CREATE SCHEMA | CREATE SCHEMA | CREATE SCHEMA | Identical |
| Schema authorization | CREATE SCHEMA AUTHORIZATION user | CREATE SCHEMA schemaname AUTHORIZATION rolename | |
| IF EXISTS / IF NOT EXISTS | IF EXISTS / IF NOT EXISTS | IF EXISTS / IF NOT EXISTS | PG supports these on most DDL statements |

---

## 6. Procedural Programming: T-SQL vs PL/pgSQL

### 6.1 Language Overview

| Concept | SQL Server | PostgreSQL | Notes |
|---|---|---|---|
| Procedural language | T-SQL (Transact-SQL) | PL/pgSQL (default), plus PL/Python, PL/Perl, PL/Tcl, PL/V8 (JavaScript), PL/R, etc. | PG is multi-language; PL/pgSQL is the primary choice |
| Stored procedures | CREATE PROCEDURE | CREATE PROCEDURE (PG 11+) | Pre-PG 11, use functions; procedures added in PG 11 |
| Functions | CREATE FUNCTION | CREATE FUNCTION | PG functions are more powerful; they return values |
| Function return type | Must be typed | Must be typed | PG functions must declare return type |
| Void function | N/A (use procedure) | RETURNS VOID | PG functions can return nothing with RETURNS VOID |
| Set-returning function | Table-valued function | RETURNS TABLE or RETURNS SETOF | PG SRFs return multiple rows |
| Inline TVF | Inline TVF (single SELECT) | SQL language function (RETURNS TABLE AS $$ SELECT ... $$) | Inline functions are inlined by the planner in both |
| Multi-statement TVF | Multi-statement TVF | PL/pgSQL function with RETURNS TABLE | |
| Trigger functions | Trigger stored procedure | Trigger function (must return TRIGGER) | PG trigger functions are separate from the trigger definition |
| Anonymous code block | N/A (use temp proc or EXEC) | DO $$ BEGIN ... END $$; | DO blocks execute anonymous PL/pgSQL inline |
| Dollar quoting | N/A | $$ ... $$ or $tag$ ... $tag$ | Avoids escaping single quotes in function bodies |
| Language declaration | N/A (T-SQL is implicit) | LANGUAGE plpgsql (required) | Must declare the language in CREATE FUNCTION/PROCEDURE |
| Transaction in procedure | Supported | Supported (PG 11+); not in functions | PG functions run within the caller's transaction; procedures can COMMIT/ROLLBACK |
| Exception handling | BEGIN TRY ... END TRY / BEGIN CATCH ... END CATCH | BEGIN ... EXCEPTION WHEN ... THEN ... END | PG uses EXCEPTION block within BEGIN...END |
| RAISERROR | RAISERROR(...) or THROW | RAISE EXCEPTION '...' or RAISE NOTICE '...' | PG RAISE has levels: DEBUG, LOG, NOTICE, WARNING, EXCEPTION |
| User-defined error codes | RAISERROR with custom msg ID | RAISE EXCEPTION ... ERRCODE 'P0001' | PG uses SQLSTATE codes; 'P0001' through 'P9999' are user-defined |
| PRINT statement | PRINT 'message' | RAISE NOTICE 'message' | |

### 6.2 Variable Declaration and Assignment

**SQL Server (T-SQL):**
```sql
DECLARE @myvar INT = 10;
DECLARE @mystr VARCHAR(100);
SET @mystr = 'hello';
SELECT @myvar = COUNT(*) FROM mytable;  -- Assign from query
```

**PostgreSQL (PL/pgSQL):**
```sql
DECLARE
    myvar INTEGER := 10;
    mystr TEXT;
    mycount INTEGER;
BEGIN
    mystr := 'hello';
    SELECT COUNT(*) INTO mycount FROM mytable;
    -- or: mycount := (SELECT COUNT(*) FROM mytable);
END;
```

Key differences:
- PG variables do not use the @ prefix
- PG uses := for assignment (or = in the DECLARE section for defaults)
- PG DECLARE block is separate from the BEGIN...END block
- PG uses SELECT INTO to assign from queries (different meaning than SQL Server's SELECT INTO)

### 6.3 Control Flow

| Construct | SQL Server (T-SQL) | PostgreSQL (PL/pgSQL) | Notes |
|---|---|---|---|
| IF / ELSE | IF condition BEGIN ... END ELSE BEGIN ... END | IF condition THEN ... ELSE ... END IF; | PG uses THEN and END IF; no BEGIN/END for blocks |
| CASE expression | CASE WHEN ... THEN ... END | CASE WHEN ... THEN ... END | Identical (SQL standard) |
| WHILE loop | WHILE condition BEGIN ... END | WHILE condition LOOP ... END LOOP; | |
| FOR loop (integer) | Workaround with WHILE | FOR i IN 1..10 LOOP ... END LOOP; | PG has native integer FOR loops |
| FOR loop (query) | CURSOR or set-based | FOR rec IN SELECT * FROM t LOOP ... END LOOP; | PG FOR loops can iterate over query results directly |
| FOREACH (array) | N/A | FOREACH elem IN ARRAY myarray LOOP ... END LOOP; | PG can iterate over array elements |
| BREAK | BREAK | EXIT; | Exit current loop |
| CONTINUE | CONTINUE | CONTINUE; | Skip to next iteration |
| EXIT WHEN | N/A | EXIT WHEN condition; | Conditional loop exit |
| GOTO | GOTO label (discouraged) | Not supported | PG has no GOTO |
| RETURN | RETURN value | RETURN value; (functions) or RETURN; (procedures) | |
| RETURN NEXT | N/A | RETURN NEXT value; | Appends a row to the result set in SRF functions |
| RETURN QUERY | N/A | RETURN QUERY SELECT ...; | Returns a full query result from a SRF function |
| EXECUTE (dynamic SQL) | EXEC sp_executesql @sql, @params, @val | EXECUTE sql_string USING param1, param2; | PG EXECUTE for dynamic SQL uses positional parameters |

### 6.4 Cursors

Cursors work in PG but the preferred pattern is set-based or FOR-loop iteration. Explicit cursors are shown here for reference.

**SQL Server:**
```sql
DECLARE myCursor CURSOR FOR SELECT id, name FROM customers;
OPEN myCursor;
FETCH NEXT FROM myCursor INTO @id, @name;
WHILE @@FETCH_STATUS = 0 BEGIN
    -- process row
    FETCH NEXT FROM myCursor INTO @id, @name;
END
CLOSE myCursor;
DEALLOCATE myCursor;
```

**PostgreSQL:**
```sql
DECLARE
    myCursor CURSOR FOR SELECT id, name FROM customers;
    v_id INTEGER;
    v_name TEXT;
BEGIN
    OPEN myCursor;
    LOOP
        FETCH myCursor INTO v_id, v_name;
        EXIT WHEN NOT FOUND;
        -- process row
    END LOOP;
    CLOSE myCursor;
END;
```

**PostgreSQL preferred pattern (implicit cursor with FOR loop):**
```sql
BEGIN
    FOR rec IN SELECT id, name FROM customers LOOP
        -- rec.id and rec.name are available
        RAISE NOTICE 'Customer: %', rec.name;
    END LOOP;
END;
```

### 6.5 Error Handling

**SQL Server:**
```sql
BEGIN TRY
    INSERT INTO orders (customer_id, amount) VALUES (1, 100.00);
    COMMIT;
END TRY
BEGIN CATCH
    DECLARE @msg NVARCHAR(4000) = ERROR_MESSAGE();
    DECLARE @sev INT = ERROR_SEVERITY();
    ROLLBACK;
    RAISERROR(@msg, @sev, 1);
END CATCH;
```

**PostgreSQL:**
```sql
BEGIN
    INSERT INTO orders (customer_id, amount) VALUES (1, 100.00);
EXCEPTION
    WHEN unique_violation THEN
        RAISE NOTICE 'Duplicate order detected';
    WHEN foreign_key_violation THEN
        RAISE EXCEPTION 'Invalid customer ID';
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Unexpected error: %', SQLERRM;
END;
```

Named PG exception conditions include: unique_violation, foreign_key_violation, not_null_violation, check_violation, division_by_zero, deadlock_detected, serialization_failure, and many others from the pg_exception_table.

### 6.6 Stored Procedures vs Functions

This is a critical distinction in PostgreSQL. Before version 11, PostgreSQL had only functions. Procedures were added in PG 11.

| Feature | SQL Server Procedure | PG Procedure (11+) | PG Function |
|---|---|---|---|
| Returns a value | OUTPUT parameters or result sets | OUTPUT parameters only | RETURNS clause (required) |
| Returns a result set | Yes (implicit result sets) | Not directly | RETURNS TABLE or RETURNS SETOF |
| Transaction control | Yes (COMMIT, ROLLBACK, SAVE) | Yes (COMMIT, ROLLBACK) | No; runs in caller's transaction |
| Called with | EXEC procname | CALL procname(...) | SELECT funcname(...) or in an expression |
| Can be used in SELECT | No | No | Yes |
| Can be used in triggers | No | No | Yes (triggers call functions) |
| Created with | CREATE PROCEDURE | CREATE PROCEDURE | CREATE FUNCTION |

**PG Function Example (returns a scalar):**
```sql
CREATE OR REPLACE FUNCTION get_customer_balance(p_customer_id INTEGER)
RETURNS NUMERIC AS $$
DECLARE
    v_balance NUMERIC;
BEGIN
    SELECT COALESCE(SUM(amount), 0)
    INTO v_balance
    FROM orders
    WHERE customer_id = p_customer_id
      AND status = 'unpaid';
    RETURN v_balance;
END;
$$ LANGUAGE plpgsql;

-- Usage:
SELECT get_customer_balance(42);
```

**PG Function Example (returns a table):**
```sql
CREATE OR REPLACE FUNCTION get_active_customers(p_min_orders INTEGER)
RETURNS TABLE(customer_id INTEGER, customer_name TEXT, order_count BIGINT) AS $$
BEGIN
    RETURN QUERY
    SELECT c.id, c.name, COUNT(o.id)
    FROM customers c
    LEFT JOIN orders o ON o.customer_id = c.id
    GROUP BY c.id, c.name
    HAVING COUNT(o.id) >= p_min_orders;
END;
$$ LANGUAGE plpgsql;

-- Usage:
SELECT * FROM get_active_customers(5);
```

**PG Trigger Function Example:**
```sql
CREATE OR REPLACE FUNCTION trg_audit_orders()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO order_audit (order_id, action, changed_at)
        VALUES (NEW.id, 'INSERT', NOW());
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO order_audit (order_id, action, changed_at)
        VALUES (NEW.id, 'UPDATE', NOW());
    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO order_audit (order_id, action, changed_at)
        VALUES (OLD.id, 'DELETE', NOW());
    END IF;
    RETURN NEW;  -- For DELETE triggers, return OLD
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER audit_orders
AFTER INSERT OR UPDATE OR DELETE ON orders
FOR EACH ROW EXECUTE FUNCTION trg_audit_orders();
```

In SQL Server, the trigger code IS the stored procedure. In PG, you create a function first, then attach it to the trigger.

### 6.7 Dynamic SQL

| Feature | SQL Server | PostgreSQL | Notes |
|---|---|---|---|
| Execute dynamic string | EXEC (@sql) or EXEC sp_executesql | EXECUTE sql_string | |
| Parameterized dynamic SQL | sp_executesql with @params, @values | EXECUTE sql_string USING param1, param2 | PG USING clause prevents SQL injection |
| Dynamic SQL parameters | @p1, @p2 (named) | $1, $2 (positional) | PG uses positional parameters |
| Build dynamic identifier | QUOTENAME(name) | quote_ident(name) | Both safely quote identifiers |
| Build dynamic literal | QUOTENAME(val, '''') | quote_literal(val) or format('%L', val) | PG format() is very useful for dynamic SQL |
| Dynamic SQL in functions | Supported | Supported via EXECUTE | |

**PG Dynamic SQL Example:**
```sql
CREATE OR REPLACE FUNCTION get_table_count(p_schema TEXT, p_table TEXT)
RETURNS BIGINT AS $$
DECLARE
    v_count BIGINT;
    v_sql TEXT;
BEGIN
    v_sql := format('SELECT COUNT(*) FROM %I.%I', p_schema, p_table);
    EXECUTE v_sql INTO v_count;
    RETURN v_count;
END;
$$ LANGUAGE plpgsql;
```

The %I format specifier in format() is equivalent to quote_ident() -- it safely quotes an identifier. The %L specifier quotes a literal value.

---

## 7. Indexing

### 7.1 Index Types

| Index Type | SQL Server | PostgreSQL | Notes |
|---|---|---|---|
| Clustered index | CLUSTERED (table ordered by index key) | No equivalent | PG has no clustered index concept; heap is always unordered |
| Re-order table by index | N/A (use clustered index) | CLUSTER tablename USING indexname | PG CLUSTER physically reorders the heap once; not maintained |
| Heap (no clustered index) | Heap table (no clustered index) | All tables are heaps | PG tables are always heaps; no clustered index alternative |
| Non-clustered index | NONCLUSTERED | All indexes (B-tree is default) | All PG indexes are non-clustered in SQL Server terminology |
| B-tree index | Default index type | CREATE INDEX (default B-tree) | B-tree is the workhorse in both |
| Hash index | Not supported as persistent | CREATE INDEX USING HASH | PG hash indexes are WAL-logged since PG 10; good for equality only |
| Bitmap index | Not available | Not available (but used internally by query executor) | PG executor uses bitmap scans on B-tree indexes; no explicit bitmap index creation |
| GiST index | Full-text / spatial only | CREATE INDEX USING GIST | Generalized Search Tree; used for ranges, geometry, full-text, nearest-neighbor |
| SP-GiST index | N/A | CREATE INDEX USING SPGIST | Space-partitioned GiST; for non-balanced trees (quad-tree, k-d tree) |
| GIN index | Full-text search index | CREATE INDEX USING GIN | Generalized Inverted Index; for JSONB, arrays, full-text |
| BRIN index | N/A | CREATE INDEX USING BRIN | Block Range Index; tiny, fast for naturally ordered data (timestamps, sequences) |
| Filtered/partial index | CREATE INDEX ... WHERE condition | CREATE INDEX ... WHERE condition | Identical concept; indexes only qualifying rows |
| Covering index (INCLUDE) | CREATE INDEX ... INCLUDE (cols) | CREATE INDEX ... INCLUDE (cols) | Identical; include non-key columns in index leaf pages |
| Composite index | CREATE INDEX ON t (col1, col2) | CREATE INDEX ON t (col1, col2) | Identical |
| Unique index | CREATE UNIQUE INDEX | CREATE UNIQUE INDEX | Identical |
| Function-based index | Computed column + index | CREATE INDEX ON t (lower(col)) | PG allows indexes directly on expressions |
| Index on expression | Not directly; use computed column | CREATE INDEX ON t (EXTRACT(year FROM created_at)) | Very powerful PG feature |
| Descending index | Supported | CREATE INDEX ON t (col DESC) | Identical |
| Null ordering in index | Not configurable | NULLS FIRST / NULLS LAST | CREATE INDEX ON t (col DESC NULLS LAST) |
| Online index create | CREATE INDEX WITH (ONLINE=ON) | CREATE INDEX CONCURRENTLY | PG CONCURRENTLY is non-blocking for reads and writes |
| Online index rebuild | ALTER INDEX ... REBUILD WITH (ONLINE=ON) | REINDEX CONCURRENTLY | PG 12+ supports concurrent reindex |
| Index rebuild | ALTER INDEX ... REBUILD | REINDEX INDEX indexname | |
| Index reorganize | ALTER INDEX ... REORGANIZE | No direct equivalent; use VACUUM FULL or pg_repack | VACUUM in PG does not reorganize; pg_repack does |
| Index disable | ALTER INDEX ... DISABLE | DROP INDEX (no disable concept) | PG has no disabled index state; drop and recreate |
| View index statistics | sys.dm_db_index_usage_stats | pg_stat_user_indexes, pg_statio_user_indexes | |
| Index fragmentation | sys.dm_db_index_physical_stats | pgstattuple extension | |
| Fill factor | CREATE INDEX WITH (FILLFACTOR=80) | CREATE INDEX WITH (FILLFACTOR=80) | Identical; leaves space for future inserts |
| Statistics on index | Created automatically | Created automatically | Auto-update controlled by autovacuum |

### 7.2 Index Access Methods (PG-Specific)

Understanding when to use each PG index type:

| Index Type | Best For | Example Use Case |
|---|---|---|
| B-tree (default) | Equality, range, sorting, LIKE 'prefix%' | Most columns; the default choice |
| Hash | Equality only (=) | UUID lookups where range queries never happen |
| GIN | Multi-element containment (@>), JSONB keys, arrays, full-text | WHERE jsonb_col @> '{"status":"active"}' |
| GiST | Ranges, geometric, nearest-neighbor (KNN) | WHERE daterange_col && '[2024-01-01,2024-12-31]' |
| SP-GiST | Non-overlapping data (IP addresses, phone number trees) | Hierarchical or point data |
| BRIN | Very large tables with correlated physical order | Timeseries, log tables with sequential timestamps |

### 7.3 Index Usage and Query Plans

**SQL Server:** Use SSMS to view graphical execution plans, or:
```sql
SET STATISTICS IO ON;
SET STATISTICS TIME ON;
-- or
SELECT * FROM sys.dm_exec_query_stats;
```

**PostgreSQL:** Use EXPLAIN and EXPLAIN ANALYZE:
```sql
EXPLAIN SELECT * FROM orders WHERE customer_id = 42;
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT) SELECT * FROM orders WHERE customer_id = 42;
EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON) SELECT * FROM orders WHERE customer_id = 42;
```

Key PG plan nodes and their SQL Server equivalents:

| PostgreSQL Plan Node | SQL Server Equivalent | Notes |
|---|---|---|
| Seq Scan | Table Scan | Full table scan; not always bad |
| Index Scan | Index Seek + Key Lookup | Uses index, fetches heap rows |
| Index Only Scan | Covering Index Seek | All needed columns in index; no heap access |
| Bitmap Index Scan + Bitmap Heap Scan | Index Seek (for OR conditions) | Collects TIDs from index, then fetches heap in order |
| Nested Loop | Nested Loops | Outer row drives inner lookup |
| Hash Join | Hash Match | Build hash table from smaller input |
| Merge Join | Merge Join | Both inputs sorted |
| Sort | Sort | Explicit sort step |
| Hash Aggregate | Hash Match (aggregate mode) | Group by using hash |
| Materialize | Spool | Materializes subquery result |
| Gather / Gather Merge | Parallelism icons | Parallel worker coordination |

---

## 8. Views, Materialized Views, and CTEs

### 8.1 Views

| Feature | SQL Server | PostgreSQL | Notes |
|---|---|---|---|
| Create view | CREATE VIEW | CREATE VIEW | Identical |
| Replace view | ALTER VIEW or CREATE OR REPLACE VIEW | CREATE OR REPLACE VIEW | PG requires same column names and types for replacement |
| Updatable view | Auto-updatable if meets criteria | Auto-updatable if meets criteria | Both have rules for when a view is auto-updatable |
| View with CHECK OPTION | WITH CHECK OPTION | WITH CHECK OPTION | Prevents updates that would make rows invisible through the view |
| Indexed view | CREATE UNIQUE CLUSTERED INDEX ON view | MATERIALIZED VIEW | Different concepts; use materialized view in PG |
| Schema binding | WITH SCHEMABINDING | No equivalent | PG does not lock down dependent objects on views |

### 8.2 Materialized Views

SQL Server has "indexed views" which are similar but not the same. PostgreSQL materialized views are explicit and require manual or scheduled refresh.

| Feature | SQL Server Indexed View | PostgreSQL Materialized View | Notes |
|---|---|---|---|
| Create | CREATE VIEW ... WITH SCHEMABINDING + CREATE UNIQUE CLUSTERED INDEX | CREATE MATERIALIZED VIEW mv AS SELECT ... | PG syntax is simpler and more explicit |
| Auto-update | Yes (maintained automatically by DML) | No; must call REFRESH MATERIALIZED VIEW | Major difference; PG MVs are static until refreshed |
| Non-blocking refresh | N/A | REFRESH MATERIALIZED VIEW CONCURRENTLY | CONCURRENTLY allows reads during refresh; requires unique index |
| Blocking refresh | N/A | REFRESH MATERIALIZED VIEW mvname | Faster but locks the view during refresh |
| Index on MV | Automatic (clustered) | CREATE INDEX ON mv (col) | PG MVs can be indexed like regular tables |
| Query rewrite | Yes (optimizer may use indexed view automatically) | No automatic rewrite | Optimizer does not automatically use PG MVs; must query MV explicitly |
| pg_cron for scheduling | SQL Server Agent Job | pg_cron extension or external scheduler | Schedule REFRESH calls with pg_cron |

**PostgreSQL Materialized View Example:**
```sql
CREATE MATERIALIZED VIEW mv_monthly_sales AS
SELECT
    DATE_TRUNC('month', order_date) AS month,
    SUM(amount) AS total_sales,
    COUNT(*) AS order_count
FROM orders
WHERE status = 'completed'
GROUP BY 1;

CREATE UNIQUE INDEX ON mv_monthly_sales (month);

-- Refresh without blocking reads:
REFRESH MATERIALIZED VIEW CONCURRENTLY mv_monthly_sales;
```

### 8.3 Common Table Expressions (CTEs)

| Feature | SQL Server | PostgreSQL | Notes |
|---|---|---|---|
| CTE syntax | WITH cte AS (SELECT ...) SELECT ... | WITH cte AS (SELECT ...) SELECT ... | Identical |
| Multiple CTEs | WITH cte1 AS (...), cte2 AS (...) SELECT ... | WITH cte1 AS (...), cte2 AS (...) SELECT ... | Identical |
| Recursive CTE | WITH RECURSIVE or just WITH (auto-detects) | WITH RECURSIVE cte AS (...) | PG requires explicit RECURSIVE keyword |
| CTE materialization | Optimizer may inline or materialize | Historically always materialized (optimization fence); PG 12 changed this | PG 12+ CTEs are inlined by default unless MATERIALIZED is specified |
| Force CTE materialization | Not possible (optimizer decides) | WITH cte AS MATERIALIZED (SELECT ...) | Forces the CTE to be executed once |
| Prevent CTE materialization | Not possible | WITH cte AS NOT MATERIALIZED (SELECT ...) | Forces inlining (optimizer default since PG 12) |
| CTE for DML | CTEs can contain INSERT/UPDATE/DELETE with OUTPUT | CTEs can contain INSERT/UPDATE/DELETE with RETURNING | Very useful for chained DML |

**PG CTE with DML Example:**
```sql
WITH moved_rows AS (
    DELETE FROM orders_staging
    WHERE created_at < NOW() - INTERVAL '30 days'
    RETURNING *
)
INSERT INTO orders_archive
SELECT * FROM moved_rows;
```

**Recursive CTE (identical in both platforms, but RECURSIVE keyword required in PG):**
```sql
-- SQL Server:
WITH EmployeeHierarchy AS (
    SELECT id, name, manager_id, 0 AS level FROM employees WHERE manager_id IS NULL
    UNION ALL
    SELECT e.id, e.name, e.manager_id, h.level + 1
    FROM employees e JOIN EmployeeHierarchy h ON e.manager_id = h.id
)
SELECT * FROM EmployeeHierarchy;

-- PostgreSQL (add RECURSIVE keyword):
WITH RECURSIVE EmployeeHierarchy AS (
    SELECT id, name, manager_id, 0 AS level FROM employees WHERE manager_id IS NULL
    UNION ALL
    SELECT e.id, e.name, e.manager_id, h.level + 1
    FROM employees e JOIN EmployeeHierarchy h ON e.manager_id = h.id
)
SELECT * FROM EmployeeHierarchy;
```

---

## 9. Partitioning

### 9.1 Partitioning Concepts

| Concept | SQL Server | PostgreSQL | Notes |
|---|---|---|---|
| Table partitioning | Partition Function and Scheme | Declarative partitioning (PG 10+) | PG 10+ added native declarative partitioning |
| Partition types | Range (by partition function) | RANGE, LIST, HASH | PG supports three partition strategies |
| Create partitioned table | CREATE TABLE with partition scheme | CREATE TABLE ... PARTITION BY RANGE (col) | Different syntax but similar concept |
| Create partition | Happens automatically via scheme | CREATE TABLE child PARTITION OF parent FOR VALUES FROM (...) TO (...) | Each partition is a real child table in PG |
| Partition pruning | Automatic (based on partition elimination) | Automatic (constraint_exclusion or partition_pruning) | Both exclude irrelevant partitions at query time |
| Partition on expression | Not directly | PARTITION BY RANGE (DATE_TRUNC('month', created_at)) | PG can partition by expression |
| Sub-partitioning | Supported | Supported | Each partition can itself be partitioned |
| Partition switching | ALTER TABLE ... SWITCH PARTITION ... TO ... | ATTACH PARTITION / DETACH PARTITION | PG DETACH/ATTACH is the equivalent of partition switching |
| Online partition management | Partition switching is fast metadata-only | DETACH PARTITION CONCURRENTLY (PG 14+) | PG 14 allows non-blocking detach |
| Default partition | No equivalent | CREATE TABLE p_default PARTITION OF parent DEFAULT | Catches rows that do not match any other partition |
| Unique indexes across partitions | Possible (with partition key in index) | Unique constraints must include partition key | PG unique indexes on partitioned tables must include the partition key |
| Foreign keys to partitioned table | Supported | Supported (PG 12+) | |
| Triggers on partitioned table | Table-level triggers | Triggers defined on parent apply to all partitions | |
| Row counts per partition | sys.partitions | pg_stat_user_tables (filter by parent OID) | |

**PostgreSQL Partitioned Table Example:**
```sql
-- Create the parent partitioned table
CREATE TABLE orders (
    order_id BIGINT NOT NULL,
    customer_id INTEGER NOT NULL,
    order_date DATE NOT NULL,
    amount NUMERIC(12,2) NOT NULL
) PARTITION BY RANGE (order_date);

-- Create partitions
CREATE TABLE orders_2024_q1 PARTITION OF orders
    FOR VALUES FROM ('2024-01-01') TO ('2024-04-01');

CREATE TABLE orders_2024_q2 PARTITION OF orders
    FOR VALUES FROM ('2024-04-01') TO ('2024-07-01');

-- Create a default partition for anything outside defined ranges
CREATE TABLE orders_default PARTITION OF orders DEFAULT;

-- Index on partition key (automatically created on child tables)
CREATE INDEX ON orders (order_date);

-- Detach a partition for archiving (non-blocking in PG 14+)
ALTER TABLE orders DETACH PARTITION orders_2024_q1 CONCURRENTLY;
```

---

## 10. Security and Access Control

### 10.1 Authentication vs Authorization

| Concept | SQL Server | PostgreSQL | Notes |
|---|---|---|---|
| Authentication | SQL login or Windows/AD auth | Password, peer, ident, GSSAPI, LDAP, SCRAM-SHA-256, cert, etc. | PG auth configured in pg_hba.conf |
| Authorization | Database user permissions | Role permissions | Both use a user-permission model; PG uses roles |
| Login (server-level) | SQL Server Login (sys.server_principals) | Role with LOGIN privilege | PG does not distinguish logins from users; it uses roles |
| Database user | Database User (must be mapped to login) | Same role (no separate mapping needed) | In PG, one role can connect to any database it has CONNECT privilege on |
| Role concept | Server roles (sysadmin, etc.) and database roles | Single role concept with LOGIN, SUPERUSER, etc. attributes | PG roles are unified; attributes control capabilities |
| Superuser | sysadmin server role | SUPERUSER attribute | CREATE ROLE myuser WITH SUPERUSER LOGIN PASSWORD '...'; |
| Create database | dbcreator server role | CREATEDB attribute | |
| Create role | securityadmin server role | CREATEROLE attribute | |
| Group roles | Database roles | Roles without LOGIN | Roles can be members of other roles in both |
| Grant to role | GRANT ... TO role | GRANT ... TO role | Identical concept |
| Inherit permissions | Automatic for database roles | INHERIT attribute on role (default) | NOINHERIT means member must SET ROLE to access granted permissions |
| Default permissions | dbo has many defaults | No default permissions except public | PG public schema had wide-open permissions pre-PG 15; PG 15 changed defaults |

### 10.2 Role Management

| Task | SQL Server | PostgreSQL | Notes |
|---|---|---|---|
| Create login/user | CREATE LOGIN / CREATE USER | CREATE ROLE name WITH LOGIN PASSWORD '...' | |
| Create group role | CREATE ROLE | CREATE ROLE groupname (no LOGIN) | Roles without LOGIN are group roles |
| Grant role membership | ALTER ROLE role ADD MEMBER user | GRANT grouprole TO memberrole | |
| Revoke role membership | ALTER ROLE role DROP MEMBER user | REVOKE grouprole FROM memberrole | |
| Set current role | EXECUTE AS | SET ROLE rolename | Switch to another role you are a member of |
| Revert role | REVERT | RESET ROLE | |
| Drop user | DROP USER | DROP ROLE | Cannot drop a role that owns objects or has active grants |
| Password management | ALTER LOGIN ... WITH PASSWORD | ALTER ROLE rolename WITH PASSWORD '...' | |
| Connection limit | N/A (max connections global) | CONNECTIONLIMIT n on CREATE ROLE | |
| Validity period | N/A | VALID UNTIL 'timestamp' | PG roles can expire |
| List roles | sys.server_principals, sys.database_principals | \du in psql or SELECT * FROM pg_roles; | |

### 10.3 Object Permissions

| Permission | SQL Server | PostgreSQL | Notes |
|---|---|---|---|
| Grant SELECT | GRANT SELECT ON table TO user | GRANT SELECT ON TABLE tablename TO rolename | |
| Grant all | GRANT ALL ON table TO user | GRANT ALL ON TABLE tablename TO rolename | |
| Grant schema-wide | GRANT SELECT ON SCHEMA::s TO user | GRANT SELECT ON ALL TABLES IN SCHEMA s TO rolename | |
| Future objects | N/A; must grant again | ALTER DEFAULT PRIVILEGES IN SCHEMA s GRANT SELECT ON TABLES TO rolename | Very useful; applies to future objects |
| Column-level permissions | GRANT SELECT (col) ON table TO user | GRANT SELECT (col) ON TABLE t TO rolename | Both support column-level grants |
| Revoke | REVOKE | REVOKE | Identical concept |
| DENY | DENY (takes precedence over GRANT) | No DENY; revoke instead | PG has no DENY; remove grants with REVOKE |
| Permission check | fn_my_permissions() | has_table_privilege(), has_schema_privilege(), etc. | PG has per-object-type privilege check functions |
| GRANT OPTION | WITH GRANT OPTION | WITH GRANT OPTION | Both allow the grantee to re-grant the privilege |
| Ownership | dbo owns objects by default | Creating role owns the object | Change ownership with ALTER TABLE ... OWNER TO rolename |
| Transfer ownership | ALTER AUTHORIZATION ON object TO user | ALTER TABLE t OWNER TO newowner | Or ALTER SCHEMA s OWNER TO ..., etc. |
| Row-level security | Row-Level Security (RLS) with security policies | Row-Level Security (RLS) with CREATE POLICY | Very similar concept; PG syntax is slightly different |

### 10.4 Row-Level Security (RLS)

Both platforms support RLS. The concept is identical but syntax differs.

**SQL Server:**
```sql
CREATE SCHEMA Security;
GO
CREATE FUNCTION Security.fn_securitypredicate(@SalesRep AS NVARCHAR(50))
    RETURNS TABLE WITH SCHEMABINDING AS
    RETURN SELECT 1 AS fn_result WHERE @SalesRep = USER_NAME();
GO
CREATE SECURITY POLICY SalesFilter
ADD FILTER PREDICATE Security.fn_securitypredicate(SalesRep)
ON dbo.Orders WITH (STATE = ON);
```

**PostgreSQL:**
```sql
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;

CREATE POLICY orders_isolation_policy ON orders
    USING (sales_rep = current_user);

-- Or with separate INSERT/UPDATE/DELETE policies:
CREATE POLICY orders_select_policy ON orders
    FOR SELECT USING (sales_rep = current_user);

CREATE POLICY orders_insert_policy ON orders
    FOR INSERT WITH CHECK (sales_rep = current_user);
```

---

## 11. Transactions and Concurrency

### 11.1 Transaction Control

| Feature | SQL Server | PostgreSQL | Notes |
|---|---|---|---|
| Begin transaction | BEGIN TRANSACTION or BEGIN TRAN | BEGIN or START TRANSACTION | |
| Commit | COMMIT or COMMIT TRANSACTION | COMMIT or COMMIT TRANSACTION | |
| Rollback | ROLLBACK or ROLLBACK TRANSACTION | ROLLBACK or ROLLBACK TRANSACTION | |
| Savepoint | SAVE TRANSACTION savepointname | SAVEPOINT savepointname | |
| Rollback to savepoint | ROLLBACK TRANSACTION savepointname | ROLLBACK TO SAVEPOINT savepointname | |
| Release savepoint | N/A | RELEASE SAVEPOINT savepointname | |
| Autocommit | On by default (each statement auto-commits) | On by default in psql -c mode; psql wraps in transaction | PG in psql wraps multi-statement sessions implicitly |
| Implicit transaction | SET IMPLICIT_TRANSACTIONS ON | Default in most drivers; each statement is its own transaction | |
| Transaction in function | Runs in caller's transaction | Functions run in caller's transaction; cannot COMMIT | Only PG procedures can issue COMMIT |
| DDL in transaction | DDL is auto-committed | DDL is fully transactional | Major difference: PG allows rollback of CREATE TABLE, DROP TABLE, etc. |
| @@TRANCOUNT equivalent | @@TRANCOUNT | No direct equivalent; use exception handling | PG does not expose nested transaction depth easily |
| Distributed transactions | MSDTC | N/A natively; use postgres_fdw with two-phase commit | PG 2PC exists but is rarely used and complex |
| Two-phase commit | MSDTC-managed | PREPARE TRANSACTION / COMMIT PREPARED | Low-level mechanism; application-managed |

**PostgreSQL Transactional DDL Example:**
```sql
BEGIN;
CREATE TABLE new_feature_table (id SERIAL PRIMARY KEY, name TEXT);
ALTER TABLE orders ADD COLUMN priority INTEGER DEFAULT 0;
-- If something goes wrong:
ROLLBACK;
-- This undoes both DDL statements -- impossible in SQL Server
```

### 11.2 Isolation Levels

| Isolation Level | SQL Server | PostgreSQL | Key Behavior |
|---|---|---|---|
| READ UNCOMMITTED | Supported; dirty reads possible | ALLOWED (SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED) but behaves as READ COMMITTED | PG MVCC means dirty reads are impossible; level is accepted but upgraded |
| READ COMMITTED | Default | Default | Both: statement sees committed data as of statement start |
| REPEATABLE READ | Supported; uses row locks | Supported; uses MVCC snapshot (no phantom reads either) | PG REPEATABLE READ is actually snapshot isolation; prevents phantoms too |
| SNAPSHOT | Supported (RCSI/SI must be enabled) | Default behavior of REPEATABLE READ | PG does not have a separate SNAPSHOT level |
| SERIALIZABLE | Supported (predicate locking) | Supported (Serializable Snapshot Isolation -- SSI) | PG SSI uses optimistic approach; may get serialization failure errors |
| Default level | READ COMMITTED | READ COMMITTED | Same default |
| NOLOCK hint | WITH (NOLOCK) -- dirty read | No equivalent needed | PG MVCC eliminates need for NOLOCK; readers never block |
| Serialization failure | Deadlock or blocking | ERROR: could not serialize access due to concurrent update | In SERIALIZABLE, PG may return SQLSTATE 40001; retry the transaction |

### 11.3 Locking

| Lock Type | SQL Server | PostgreSQL | Notes |
|---|---|---|---|
| Table lock | LOCK TABLE (via hints) | LOCK TABLE tablename IN mode MODE | PG has explicit LOCK TABLE command |
| Row lock | Automatic via DML | Automatic via DML; SELECT FOR UPDATE | |
| Advisory lock | Not available | pg_advisory_lock(key) / pg_advisory_unlock(key) | Application-level cooperative locks; very useful for job control |
| SELECT for update | WITH (UPDLOCK, ROWLOCK) hint | SELECT ... FOR UPDATE | Locks selected rows against concurrent update |
| Skip locked rows | N/A natively | SELECT ... FOR UPDATE SKIP LOCKED | Excellent for queue table patterns |
| Lock waiting | Waits indefinitely by default | Waits indefinitely by default | Both can use lock timeout |
| Lock timeout | SET LOCK_TIMEOUT 5000 | SET lock_timeout = '5s' | Both abort the statement if lock cannot be acquired in time |
| Deadlock detection | Automatic | Automatic | Both detect and resolve deadlocks; one transaction is chosen as victim |
| Deadlock info | sys.dm_exec_requests, Extended Events | DETAIL in ERROR message, pg_locks view | |
| Lock monitoring | sys.dm_exec_requests, sys.dm_os_waiting_tasks | pg_locks, pg_stat_activity | |
| Blocked queries | sys.dm_exec_requests (wait_type) | pg_stat_activity (wait_event) | |
| View locks | sys.dm_tran_locks | SELECT * FROM pg_locks; | |
| Statement timeout | N/A (use QUERY_GOVERNOR_COST_LIMIT) | SET statement_timeout = '30s' | Kills the statement if it runs longer than the specified time |

---

## 12. Administration and Maintenance

### 12.1 Database Maintenance Operations

| Operation | SQL Server | PostgreSQL | Notes |
|---|---|---|---|
| Equivalent of DBCC CHECKDB | DBCC CHECKDB | pg_dump --file=/dev/null (logical check) or amcheck extension | No exact equivalent; amcheck checks B-tree integrity; no comprehensive checker |
| Rebuild indexes | ALTER INDEX ALL ON t REBUILD | REINDEX TABLE tablename or REINDEX DATABASE dbname | |
| Online index rebuild | REBUILD WITH (ONLINE=ON) | REINDEX ... CONCURRENTLY | |
| Update statistics | UPDATE STATISTICS or sp_updatestats | ANALYZE or VACUUM ANALYZE | |
| Auto-update statistics | Auto stats update (enabled by default) | autovacuum runs ANALYZE automatically | |
| Reclaim space | No manual step needed (page reuse) | VACUUM tablename | Reclaims space from dead tuples for reuse |
| Defragment / reclaim and compact | DBCC SHRINKFILE or REBUILD | VACUUM FULL tablename or pg_repack | VACUUM FULL rewrites the entire table and requires exclusive lock |
| Shrink database | DBCC SHRINKDATABASE | No equivalent | PG never has a growing data file that needs shrinking in the same way |
| Page verification | Page checksums (enabled by default in new DBs) | Page checksums (enabled at initdb time with -k) | Enable at cluster creation: initdb -k |
| Monitoring bloat | Not a concern (version store in tempdb) | pgstattuple extension; pg_bloat_check | Dead tuple accumulation is a PG-specific concern |

### 12.2 VACUUM -- The Most Critical PG Administration Concept

There is no SQL Server equivalent to VACUUM. This is the most important administration concept for SQL Server professionals to understand when moving to PostgreSQL.

| VACUUM Operation | Purpose | SQL Server Analogy |
|---|---|---|
| VACUUM tablename | Marks dead tuples as reusable; updates FSM and VM; advances XID horizon | Roughly like page reuse, but it is explicit in PG |
| VACUUM ANALYZE tablename | VACUUM plus updates statistics | UPDATE STATISTICS (partial analogy) |
| VACUUM FULL tablename | Rewrites table, reclaims space to OS; requires exclusive lock | DBCC SHRINKFILE + REBUILD |
| VACUUM FREEZE tablename | Sets all row XIDs to frozen; prevents XID wraparound | No equivalent |
| AUTOVACUUM | Background process that runs VACUUM and ANALYZE automatically | Closest to auto-stats update + background page cleanup |

**Autovacuum Tuning Parameters:**

```
autovacuum = on                           # Never disable
autovacuum_vacuum_threshold = 50          # Minimum rows changed before vacuum
autovacuum_vacuum_scale_factor = 0.2      # % of table rows changed to trigger vacuum
autovacuum_analyze_threshold = 50         # Minimum rows changed before analyze
autovacuum_analyze_scale_factor = 0.1     # % of table rows changed to trigger analyze
autovacuum_vacuum_cost_delay = 2ms        # Throttling delay (lower = more aggressive)
autovacuum_max_workers = 3               # Number of autovacuum worker processes
```

For large and high-churn tables, override autovacuum settings at the table level:
```sql
ALTER TABLE orders SET (
    autovacuum_vacuum_scale_factor = 0.01,   -- Vacuum after 1% change instead of 20%
    autovacuum_analyze_scale_factor = 0.005  -- Analyze after 0.5% change
);
```

### 12.3 Monitoring and Diagnostics

| What to Monitor | SQL Server | PostgreSQL | Notes |
|---|---|---|---|
| Active sessions | sys.dm_exec_sessions | pg_stat_activity | SELECT pid, usename, state, query, wait_event FROM pg_stat_activity; |
| Blocking queries | sys.dm_exec_requests (blocking_session_id) | pg_stat_activity + pg_locks join | |
| Wait events | sys.dm_os_wait_stats | pg_stat_activity.wait_event / wait_event_type | |
| Slow queries | Extended Events, Query Store | pg_stat_statements, auto_explain | pg_stat_statements is the primary tool |
| Table access stats | sys.dm_db_index_usage_stats | pg_stat_user_tables | seq_scan, idx_scan, n_dead_tup, last_vacuum, etc. |
| Index usage | sys.dm_db_index_usage_stats | pg_stat_user_indexes | idx_scan count; zero = candidate for removal |
| Table sizes | sys.dm_db_partition_stats | pg_relation_size(), pg_table_size(), pg_total_relation_size() | |
| Database size | sys.master_files | SELECT pg_size_pretty(pg_database_size('mydb')); | |
| Buffer cache hit ratio | sys.dm_os_buffer_descriptors | pg_statio_user_tables (heap_blks_hit / heap_blks_read) | |
| Replication lag | sys.dm_hadr_database_replica_states | pg_stat_replication (primary side) | SELECT * FROM pg_stat_replication; |
| Autovacuum activity | N/A | pg_stat_user_tables (last_autovacuum, n_dead_tup) | |
| Table bloat | N/A | pgstattuple(), pgstattuple extension | |
| Kill a session | KILL session_id | SELECT pg_terminate_backend(pid); | pg_cancel_backend(pid) sends SIGINT (cancel query); pg_terminate_backend kills the connection |
| Cancel a query | In SSMS, click stop | SELECT pg_cancel_backend(pid); | Less disruptive than terminate |
| Long-running transactions | sys.dm_tran_active_transactions | SELECT * FROM pg_stat_activity WHERE state = 'idle in transaction'; | Idle-in-transaction connections hold locks; investigate and kill |

### 12.4 SQL Server Agent Equivalent

| Feature | SQL Server | PostgreSQL | Notes |
|---|---|---|---|
| Scheduled jobs | SQL Server Agent | pg_cron extension | pg_cron is a background worker that runs SQL on a cron schedule |
| One-time jobs | SQL Server Agent (one-time) | No built-in; use OS cron + psql | |
| Job alerting | SQL Server Agent Alerts | No built-in; use external monitoring (Grafana, PagerDuty, etc.) | |
| Event-driven jobs | SQL Server Agent Alerts + WMI | Triggers + pg_notify + LISTEN | PG pub/sub can drive event-based processing |
| Database Mail | Database Mail | No built-in; use external scripts or pg_notify + application layer | |

---

## 13. Backup and Recovery

### 13.1 Backup Methods

| Backup Type | SQL Server | PostgreSQL | Notes |
|---|---|---|---|
| Full backup | BACKUP DATABASE | pg_dump (logical) or pg_basebackup (physical) | PG has two fundamentally different backup approaches |
| Logical backup | N/A (BCP export is logical) | pg_dump / pg_dumpall | Produces SQL or custom binary format; platform-portable |
| Physical backup | BACKUP DATABASE (file-based) | pg_basebackup | Copies physical data files; requires WAL archiving for PITR |
| Differential backup | BACKUP DATABASE ... WITH DIFFERENTIAL | No direct equivalent | Use pg_basebackup + WAL archiving for equivalent functionality |
| Log backup | BACKUP LOG | WAL archiving (archive_command) | Archive each WAL segment for PITR capability |
| Incremental backup | Third-party or differential | pg_basebackup --checkpoint=fast + WAL or third-party (pgBackRest, Barman) | pgBackRest supports true incremental backups |
| Backup to file | BACKUP TO DISK | pg_dump -Fc -f file.dump or pg_basebackup -D /path | |
| Backup to S3/cloud | Third-party or SQL Server backup to URL | pgBackRest, Barman, wal-g | pgBackRest and wal-g are the primary open-source solutions |
| Point-in-time recovery | WITH STOPAT in RESTORE | pg_basebackup + WAL archive + recovery_target_time | PG PITR requires physical backup + archived WAL |
| Online backup | Hot backup with VSS | pg_basebackup (always online) | PG basebackup is always online; no need for special modes |
| Backup compression | BACKUP WITH COMPRESSION | pg_dump -Fc (custom format is compressed) | |
| Parallel backup | N/A | pg_dump -j n (jobs parameter) | pg_dump -j uses multiple workers for parallel schema/data dump |
| Parallel restore | N/A | pg_restore -j n | |

### 13.2 pg_dump Formats

| Format | Flag | Description | When to Use |
|---|---|---|---|
| Plain SQL | -Fp or default | Plain text SQL script | For reading or selective restore; not recommended for large DBs |
| Custom | -Fc | Compressed binary; supports selective restore | Best practice for most backups |
| Directory | -Fd | Directory with one file per table; supports parallel | Large databases; use with pg_restore -j |
| Tar | -Ft | Tar archive | Less common; similar to directory format |

**Common pg_dump and pg_restore Commands:**

```bash
# Full database backup (custom format):
pg_dump -h myserver -U myuser -Fc -f mydb.dump mydb

# Restore:
pg_restore -h myserver -U myuser -d mydb -Fc mydb.dump

# Parallel restore (4 workers):
pg_restore -h myserver -U myuser -d mydb -j 4 -Fc mydb.dump

# Schema only:
pg_dump -h myserver -U myuser -Fc --schema-only -f schema.dump mydb

# Data only:
pg_dump -h myserver -U myuser -Fc --data-only -f data.dump mydb

# Specific table:
pg_dump -h myserver -U myuser -Fc -t public.orders -f orders.dump mydb

# All databases (includes roles and tablespaces):
pg_dumpall -h myserver -U myuser -f alldatabases.sql

# Physical backup with WAL streaming:
pg_basebackup -h myserver -U replication_user -D /backup/base -Ft -z -P --wal-method=stream
```

### 13.3 Recovery Configuration

**PostgreSQL Point-in-Time Recovery (PITR):**

```ini
# postgresql.conf (on the server where WAL was generated):
archive_mode = on
archive_command = 'cp %p /mnt/wal_archive/%f'

# Recovery: create recovery.signal in PGDATA (PG 12+)
# Then set in postgresql.conf:
restore_command = 'cp /mnt/wal_archive/%f %p'
recovery_target_time = '2024-06-15 14:30:00'
recovery_target_action = 'promote'   -- promote | pause | shutdown
```

**SQL Server PITR:**
```sql
RESTORE DATABASE mydb FROM DISK = 'C:\backup\mydb_full.bak' WITH NORECOVERY;
RESTORE LOG mydb FROM DISK = 'C:\backup\mydb_log.bak' WITH NORECOVERY;
RESTORE LOG mydb FROM DISK = 'C:\backup\mydb_log2.bak'
    WITH STOPAT = '2024-06-15 14:30:00', RECOVERY;
```

---

## 14. High Availability and Replication

### 14.1 HA Options Overview

| Solution | SQL Server Equivalent | PostgreSQL Option | Notes |
|---|---|---|---|
| Synchronous replication | Always On AG (synchronous) | Streaming replication with synchronous_standby_names | Data must be committed on standby before primary acknowledges |
| Asynchronous replication | Always On AG (asynchronous) or Log Shipping | Streaming replication (default) | Most common PG replication setup |
| Automatic failover | Always On AG with WSFC | Patroni, Repmgr, or cloud-managed (RDS, CloudSQL, etc.) | PG has no built-in automatic failover; needs orchestrator |
| Read replicas | Always On AG (readable secondaries) | Hot Standby (HS) on streaming replicas | PG replicas are readable by default when hot_standby = on |
| Logical replication | Transactional replication | Logical replication (PG 10+) | Replicates data changes at the logical row level; cross-version compatible |
| Multi-master | Not in core product (AG is single primary) | BDR (Bi-Directional Replication) -- third party | pglogical and BDR from EDB for multi-master |
| Shared disk | Failover Cluster Instance (FCI) | Pacemaker + Corosync + DRBD | PG can run on shared storage with Pacemaker |
| Connection pooler | N/A (SQL Server handles connection natively) | PgBouncer (most common), Pgpool-II | Essential for PG in high-connection environments |

### 14.2 Streaming Replication Configuration

Streaming replication in PostgreSQL replicates WAL from a primary to one or more standby servers.

**Primary server configuration (postgresql.conf):**
```ini
wal_level = replica               # Minimum for replication
max_wal_senders = 10              # How many replica connections allowed
wal_keep_size = 1GB               # Keep this much WAL for replicas that fall behind
hot_standby = on                  # Allow reads on standbys
synchronous_standby_names = ''    # Empty = async; set to standby name for sync
```

**Primary server (pg_hba.conf):**
```
host replication replication_user 10.0.0.0/8 scram-sha-256
```

**Standby setup:**
```bash
pg_basebackup -h primary_host -U replication_user -D $PGDATA -P -R
# -R creates standby.signal and basic connection settings in postgresql.auto.conf
```

**Standby (postgresql.conf or postgresql.auto.conf):**
```ini
primary_conninfo = 'host=primary_host port=5432 user=replication_user password=secret'
hot_standby = on
```

**Monitoring replication (on primary):**
```sql
SELECT client_addr, state, sent_lsn, write_lsn, flush_lsn, replay_lsn,
       write_lag, flush_lag, replay_lag, sync_state
FROM pg_stat_replication;
```

### 14.3 Logical Replication

Logical replication replicates specific tables, allows cross-version replication, and can filter by table.

| Feature | SQL Server Transactional Replication | PostgreSQL Logical Replication | Notes |
|---|---|---|---|
| Unit of replication | Article (table, filtered) | Publication (set of tables) | |
| Subscriber | Subscriber database | Subscription | |
| Publisher | Publisher | Publisher (with logical WAL decoding) | |
| Filter rows | Horizontal filtering | Row filter on publication (PG 15+) | |
| Filter columns | Vertical filtering | Column list on publication (PG 15+) | |
| DDL replication | Supported | Not automatic; DDL must be applied manually | Major limitation of PG logical replication |
| Initial snapshot | Snapshot publication | Initial data copy during subscription setup | |
| Conflict resolution | Last writer wins or custom resolvers | Subscriber wins (errors on conflict by default) | Must handle conflicts manually in PG |

**Setting up logical replication:**

**Publisher (postgresql.conf):**
```ini
wal_level = logical
```

**Publisher (create publication):**
```sql
CREATE PUBLICATION my_pub FOR TABLE orders, customers;
-- Or for all tables:
CREATE PUBLICATION my_pub FOR ALL TABLES;
```

**Subscriber:**
```sql
CREATE SUBSCRIPTION my_sub
CONNECTION 'host=publisher_host dbname=mydb user=replication_user password=secret'
PUBLICATION my_pub;
```

---

## 15. Performance Tuning and Query Optimization

### 15.1 Query Plan Analysis

Understanding execution plans is as important in PG as in SQL Server, but the tools are different.

**EXPLAIN syntax:**
```sql
-- Estimated plan only (no execution):
EXPLAIN SELECT * FROM orders WHERE customer_id = 42;

-- Actual plan with runtime statistics:
EXPLAIN (ANALYZE) SELECT * FROM orders WHERE customer_id = 42;

-- Full details including buffer statistics:
EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM orders WHERE customer_id = 42;

-- All options:
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT, VERBOSE, TIMING, SUMMARY)
    SELECT * FROM orders WHERE customer_id = 42;

-- JSON format (for programmatic processing):
EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)
    SELECT * FROM orders WHERE customer_id = 42;
```

**Reading EXPLAIN output:**

```
Nested Loop  (cost=0.43..1250.32 rows=100 width=48) (actual time=0.082..3.211 rows=87 loops=1)
  ->  Index Scan using orders_pkey on orders  (cost=0.43..8.45 rows=1 width=40) (actual time=0.050..0.051 rows=1 loops=87)
        Index Cond: (id = 42)
  ->  Seq Scan on order_items  (cost=0.00..450.00 rows=100 width=8) (actual time=0.020..1.100 rows=87 loops=87)
        Filter: (order_id = orders.id)
Buffers: shared hit=1234 read=56
Planning Time: 0.342 ms
Execution Time: 3.850 ms
```

cost=start..total: Estimated cost units (not milliseconds).
actual time=first_row_ms..last_row_ms rows=actual_rows loops=iterations.
Buffers: shared hit = from buffer cache; read = from disk.

### 15.2 Statistics and the Query Planner

| Concept | SQL Server | PostgreSQL | Notes |
|---|---|---|---|
| Column statistics | Statistics objects (histograms, density vectors) | pg_statistic / pg_stats (histograms, MCV lists, correlation) | Both use histograms and most-common-value lists |
| Update statistics | UPDATE STATISTICS or sp_updatestats | ANALYZE tablename | |
| Statistics target | N/A per column (sample rate is global) | default_statistics_target (100 default) or per column | ALTER TABLE t ALTER COLUMN c SET STATISTICS 500; |
| Multi-column statistics | Statistics on multiple columns | CREATE STATISTICS name ON (col1, col2) FROM t | PG CREATE STATISTICS for dependencies, ndistinct, MCV |
| Expression statistics | Computed column + statistics | Statistics auto-gathered for indexed expressions | |
| View statistics | sys.dm_db_stats_histogram | SELECT * FROM pg_stats WHERE tablename='t'; | |
| Cardinality estimator | 70/120/150 CE versions (compat level) | Single CE; improved per major version | |
| Parameter sniffing | Common problem in SQL Server | PREPARE / EXECUTE plan caching can have similar issues | PG uses generic vs. custom plans; custom plans chosen when estimated benefit |
| Plan cache | sys.dm_exec_cached_plans | pg_prepared_statements (explicit); internal plan cache per session | PG plan caching is per-session for prepared statements |
| Plan stability | USE PLAN hint | No direct equivalent; pg_hint_plan extension | |
| Enable/disable operators | SET STATISTICS PROFILE ON hints | SET enable_seqscan = off; SET enable_hashjoin = off; etc. | PG GUC params to disable plan operators for testing |

### 15.3 Key Performance GUC Parameters

```ini
# Planner cost parameters (tune to your storage):
seq_page_cost = 1.0              # Cost of reading a sequential disk page
random_page_cost = 4.0           # Cost of random disk access; set to 1.1 for SSD
cpu_tuple_cost = 0.01            # Cost of processing a row
cpu_index_tuple_cost = 0.005     # Cost of processing an index entry
cpu_operator_cost = 0.0025       # Cost of applying an operator

# Memory for sorting and hashing (per sort/hash operation, can multiply):
work_mem = 16MB                  # Increase for complex queries; watch total memory usage

# Tells planner how much of the OS cache to expect:
effective_cache_size = 12GB      # Set to ~75% of total RAM

# Parallelism:
max_parallel_workers = 8
max_parallel_workers_per_gather = 4
parallel_tuple_cost = 0.1
parallel_setup_cost = 1000.0
min_parallel_table_scan_size = 8MB

# JIT compilation (PG 11+):
jit = on                         # Enable JIT for long-running analytical queries
jit_above_cost = 100000          # Only use JIT for expensive queries
```

### 15.4 Common Performance Patterns

**Identifying slow queries (pg_stat_statements):**
```sql
-- Enable in postgresql.conf:
-- shared_preload_libraries = 'pg_stat_statements'

CREATE EXTENSION pg_stat_statements;

-- Top 10 slowest queries by total time:
SELECT
    round(total_exec_time::numeric, 2) AS total_ms,
    calls,
    round((total_exec_time / calls)::numeric, 2) AS avg_ms,
    round(stddev_exec_time::numeric, 2) AS stddev_ms,
    rows,
    query
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 10;
```

**Finding bloated tables:**
```sql
SELECT
    schemaname,
    tablename,
    n_dead_tup,
    n_live_tup,
    round(n_dead_tup * 100.0 / NULLIF(n_live_tup + n_dead_tup, 0), 2) AS dead_pct,
    last_autovacuum,
    last_autoanalyze
FROM pg_stat_user_tables
WHERE n_dead_tup > 10000
ORDER BY n_dead_tup DESC;
```

**Finding unused indexes:**
```sql
SELECT
    schemaname,
    tablename,
    indexname,
    idx_scan,
    pg_size_pretty(pg_relation_size(indexrelid)) AS index_size
FROM pg_stat_user_indexes
WHERE idx_scan = 0
  AND schemaname NOT IN ('pg_catalog', 'pg_toast')
ORDER BY pg_relation_size(indexrelid) DESC;
```

**Identifying blocking queries:**
```sql
SELECT
    blocked.pid AS blocked_pid,
    blocked.query AS blocked_query,
    blocking.pid AS blocking_pid,
    blocking.query AS blocking_query,
    now() - blocked.query_start AS blocked_duration
FROM pg_stat_activity AS blocked
JOIN pg_locks AS blocked_locks ON blocked.pid = blocked_locks.pid
JOIN pg_locks AS blocking_locks ON blocking_locks.granted
    AND blocked_locks.locktype = blocking_locks.locktype
    AND blocked_locks.relation IS NOT DISTINCT FROM blocking_locks.relation
    AND blocking_locks.pid != blocked_locks.pid
JOIN pg_stat_activity AS blocking ON blocking_locks.pid = blocking.pid
WHERE NOT blocked_locks.granted;
```

### 15.5 Connection Pooling with PgBouncer

SQL Server handles many connections natively without a pooler. PostgreSQL's process-per-connection model requires a pooler for high-connection workloads.

| PgBouncer Mode | Description | SQL Server Analogy | Use Case |
|---|---|---|---|
| Session pooling | One server connection per client session | No analogy (SQL Server does this natively for threads) | Long-lived connections; transparent to applications |
| Transaction pooling | Server connection held only during a transaction | Closest to how SQL Server manages internal resources | Most common production mode; applications must not use session-level state |
| Statement pooling | Server connection held only for one statement | Not applicable | Rare; incompatible with multi-statement transactions |

**pgbouncer.ini example:**
```ini
[databases]
mydb = host=127.0.0.1 port=5432 dbname=mydb

[pgbouncer]
pool_mode = transaction
listen_port = 6432
listen_addr = *
auth_type = scram-sha-256
auth_file = /etc/pgbouncer/userlist.txt
max_client_conn = 1000
default_pool_size = 25
min_pool_size = 5
reserve_pool_size = 5
```

---

## 16. System Catalogs and Metadata

### 16.1 Information Schema vs System Catalogs

PostgreSQL supports the SQL standard information_schema as well as its own pg_catalog (pg_*) views. The pg_catalog views are more complete and performant.

| SQL Server View | PostgreSQL Equivalent | Notes |
|---|---|---|
| sys.databases | pg_database | SELECT datname, encoding, datcollate FROM pg_database; |
| sys.schemas | pg_namespace | SELECT nspname FROM pg_namespace; |
| sys.tables | pg_class WHERE relkind='r' | relkind: r=table, v=view, m=materialized view, i=index, S=sequence |
| sys.columns | pg_attribute | SELECT attname, atttypid::regtype FROM pg_attribute WHERE attrelid='mytable'::regclass; |
| sys.indexes | pg_index + pg_class | |
| sys.index_columns | pg_index (indkey array) | Use generate_subscripts or unnest to expand key columns |
| sys.foreign_keys | pg_constraint WHERE contype='f' | contype: p=PK, u=unique, f=FK, c=check |
| sys.check_constraints | pg_constraint WHERE contype='c' | |
| sys.key_constraints | pg_constraint WHERE contype IN ('p','u') | |
| sys.triggers | pg_trigger | |
| sys.views | pg_class WHERE relkind='v' | |
| sys.procedures | pg_proc | Functions and procedures; prokind: f=function, p=procedure, a=aggregate, w=window |
| sys.parameters | pg_proc (proargnames, proargtypes) | Arguments are arrays on pg_proc; must unnest |
| sys.types | pg_type | |
| sys.server_principals | pg_roles | SELECT rolname, rolsuper, rolcreatedb, rolcreaterole FROM pg_roles; |
| sys.database_principals | pg_roles (same) | PG does not separate server-level from database-level users |
| sys.permissions | pg_auth_members, information_schema.role_table_grants | |
| INFORMATION_SCHEMA.TABLES | information_schema.tables | Standard; exists in both |
| INFORMATION_SCHEMA.COLUMNS | information_schema.columns | Standard; exists in both |
| sys.dm_exec_sessions | pg_stat_activity | SELECT pid, usename, application_name, state, query FROM pg_stat_activity; |
| sys.dm_exec_requests | pg_stat_activity (state='active') | |
| sys.dm_os_wait_stats | pg_stat_bgwriter, pg_stat_activity.wait_event | |
| sys.dm_db_index_usage_stats | pg_stat_user_indexes | |
| sys.dm_db_partition_stats | pg_stat_user_tables | n_live_tup, n_dead_tup, seq_scan, idx_scan |
| sys.dm_io_virtual_file_stats | pg_statio_user_tables, pg_statio_user_indexes | heap_blks_read, heap_blks_hit, idx_blks_read, idx_blks_hit |
| sys.configurations | pg_settings | SELECT name, setting, unit, category FROM pg_settings; |
| sys.messages | pg_catalog.pg_description | Object comments stored in pg_description |
| sys.extended_properties | pg_description (COMMENT ON ...) | COMMENT ON TABLE mytable IS 'This table stores orders'; |

### 16.2 Useful Metadata Queries

**List all tables with sizes:**
```sql
SELECT
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS total_size,
    pg_size_pretty(pg_relation_size(schemaname||'.'||tablename)) AS table_size,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)
                   - pg_relation_size(schemaname||'.'||tablename)) AS index_size
FROM pg_tables
WHERE schemaname NOT IN ('pg_catalog','information_schema')
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

**List all indexes with definition:**
```sql
SELECT
    schemaname,
    tablename,
    indexname,
    indexdef,
    pg_size_pretty(pg_relation_size(indexrelid)) AS index_size
FROM pg_indexes
JOIN pg_stat_user_indexes USING (schemaname, tablename, indexname)
WHERE schemaname = 'public'
ORDER BY pg_relation_size(indexrelid) DESC;
```

**Object dependencies (what does my object depend on):**
```sql
SELECT
    dep.classid::regclass AS object_class,
    dep.objid::regclass AS object_name,
    ref.classid::regclass AS depends_on_class,
    ref.objid::regclass AS depends_on_name
FROM pg_depend dep
JOIN pg_depend ref ON dep.objid = ref.objid
WHERE dep.deptype = 'n';  -- 'n' = normal dependency
```

---

## 17. JSON and Semi-Structured Data

### 17.1 JSON Data Types

PostgreSQL has two JSON types. Use JSONB almost always.

| Feature | SQL Server | PostgreSQL JSON | PostgreSQL JSONB | Notes |
|---|---|---|---|---|
| Storage | Stored as NVARCHAR | Stored as exact text | Stored as parsed binary | JSONB is parsed once on insert |
| Indexing | Full-text index on JSON cols | Not indexable | GIN and B-tree indexable | JSONB indexes are extremely powerful |
| Key ordering | N/A | Preserved | Not preserved | Keys sorted in JSONB |
| Duplicate keys | Allowed | Allowed | Last value wins | |
| White space | N/A | Preserved | Removed | |
| Performance | Parses on each access | Parses on each access | Parsed once; fast access | JSONB wins for read-heavy workloads |

### 17.2 JSON Operators and Functions

| Operation | SQL Server | PostgreSQL | Notes |
|---|---|---|---|
| Extract field (text) | JSON_VALUE(col, '$.key') | col->>'key' | Returns text |
| Extract field (JSON) | JSON_QUERY(col, '$.key') | col->'key' | Returns JSON/JSONB |
| Path navigation | JSON_VALUE(col, '$.a.b.c') | col#>>'{a,b,c}' | Nested path access |
| Check key exists | ISJSON(col) and manual check | col ? 'key' | The ? operator checks key existence |
| Check path exists | N/A | col @> '{"key": null}' | Containment check |
| Containment | N/A | col @> '{"status":"active"}'::jsonb | Does JSONB contain this sub-document? |
| Key array check | N/A | col ?| ARRAY['key1','key2'] | Any of these keys exist? |
| Key array all | N/A | col ?and ARRAY['key1','key2'] | All of these keys exist? |
| Modify JSON | JSON_MODIFY(col, '$.key', val) | jsonb_set(col, '{key}', '"value"') | Returns modified JSONB |
| Delete key | N/A | col - 'key' | The - operator removes a key |
| Delete by path | N/A | col #- '{a,b}' | Removes nested key |
| Convert to JSON | FOR JSON AUTO | to_json(row) or row_to_json(t.*) | |
| Array to JSON | N/A | to_json(ARRAY[1,2,3]) | |
| JSON to rows | OPENJSON() | jsonb_each(), jsonb_array_elements() | Expand JSON to relational rows |
| JSON array elements | OPENJSON() | jsonb_array_elements(col) | Returns one row per array element |
| Build JSON object | JSON_OBJECT() (SQL Server 2022) | jsonb_build_object('k1',v1,'k2',v2) | |
| Build JSON array | JSON_ARRAY() (SQL Server 2022) | jsonb_build_array(v1,v2,v3) | |
| Aggregate to JSON | FOR JSON | jsonb_agg(expression) | |
| Parse JSON path | N/A | jsonb_path_query(col, '$.items[*].name') | SQL/JSON path language (PG 12+) |

**JSONB Indexing Examples:**
```sql
-- GIN index for general JSONB containment queries:
CREATE INDEX idx_orders_data_gin ON orders USING GIN (data);

-- Targeted B-tree index on a specific JSON key:
CREATE INDEX idx_orders_status ON orders ((data->>'status'));

-- Query using containment (uses GIN index):
SELECT * FROM orders WHERE data @> '{"status": "active", "region": "US"}';

-- Query using extracted key (uses B-tree index):
SELECT * FROM orders WHERE data->>'status' = 'active';
```

---

## 18. Full-Text Search

### 18.1 Full-Text Search Comparison

| Feature | SQL Server | PostgreSQL | Notes |
|---|---|---|---|
| Index type | Full-text catalog and index | GIN index on TSVECTOR column | PG FTS is built in; no separate catalog |
| Vector type | Internal (not user-visible) | TSVECTOR | PG text search vectors are a native data type |
| Query type | Internal | TSQUERY | PG text search queries are a native data type |
| Create searchable doc | CONTAINS / FREETEXT | to_tsvector('english', col) | Converts text to a lexeme vector |
| Search query | CONTAINS(col, 'word') | to_tsquery('english', 'word') or plainto_tsquery() | |
| Phrase search | CONTAINS(col, '"exact phrase"') | phraseto_tsquery('english', 'exact phrase') | |
| Rank results | Automatic ranking with CONTAINSTABLE | ts_rank(tsvector, tsquery) or ts_rank_cd() | |
| Highlight results | N/A | ts_headline(text, tsquery) | Returns text with matching terms highlighted |
| Language support | Via language packs | Via pg dictionaries | |
| Stop words | Configured in full-text catalog | Language dictionary (e.g., english.stop) | |
| Stemming | Language-based stemming | Language-based stemming via snowball | |
| Synonyms | Thesaurus in full-text catalog | Thesaurus dictionary in FTS config | |
| Multiple columns | Full-text index on multiple columns | Concatenate with to_tsvector and store in generated column | |

**PostgreSQL Full-Text Search Example:**
```sql
-- Add a tsvector column for FTS:
ALTER TABLE articles ADD COLUMN fts_vector TSVECTOR
    GENERATED ALWAYS AS (
        to_tsvector('english', coalesce(title,'') || ' ' || coalesce(body,''))
    ) STORED;

-- Create a GIN index on the FTS vector:
CREATE INDEX idx_articles_fts ON articles USING GIN (fts_vector);

-- Search:
SELECT title, ts_rank(fts_vector, query) AS rank
FROM articles, to_tsquery('english', 'postgresql and performance') AS query
WHERE fts_vector @@ query
ORDER BY rank DESC;

-- Headline (snippet with highlights):
SELECT ts_headline('english', body, to_tsquery('postgresql and performance'))
FROM articles WHERE fts_vector @@ to_tsquery('english', 'postgresql and performance');
```

---

## 19. Extensions and Ecosystem

### 19.1 Key PostgreSQL Extensions

One of PG's greatest strengths is its extension ecosystem. These are community and commercial extensions that add major capabilities.

| Extension | Purpose | SQL Server Equivalent | Notes |
|---|---|---|---|
| pg_stat_statements | Query performance statistics | Query Store | Must-have for production; tracks all query execution stats |
| auto_explain | Log slow query plans automatically | Extended Events plan capture | Add to shared_preload_libraries |
| pgBouncer | Connection pooler | Built into SQL Server | External process; not a PG extension per se |
| PostGIS | Full spatial/GIS capabilities | SQL Server Spatial (geometry/geography types) | Industry-standard spatial for PostgreSQL |
| TimescaleDB | Time-series data at scale | N/A (use columnstore indexes manually) | Extension or separate product; automatic time-based partitioning |
| Citus | Horizontal sharding and distributed SQL | Not available in core SQL Server | Distributes tables across worker nodes |
| pgvector | Vector similarity search for AI/ML workloads | N/A | Enables embedding storage and similarity search |
| pg_partman | Automated partition management | Custom SQL Agent scripts | Creates and maintains time-based partitions automatically |
| pg_cron | In-database job scheduler | SQL Server Agent | Runs SQL on a cron schedule |
| pglogical | Advanced logical replication | Transactional replication | BDR is built on pglogical for multi-master |
| HypoPG | Hypothetical indexes (what-if analysis) | Database Engine Tuning Advisor | Test if an index would help without creating it |
| pg_qualstats | Track predicate statistics for index advisor | Database Engine Tuning Advisor | Works with HypoPG for index recommendations |
| amcheck | Verify B-tree index integrity | DBCC CHECKDB (partially) | Checks index structural integrity |
| pgstattuple | Table and index bloat statistics | sys.dm_db_index_physical_stats | |
| tablefunc | crosstab (PIVOT equivalent) | PIVOT operator | SELECT * FROM crosstab(...) AS ... |
| fuzzystrmatch | Fuzzy string matching (soundex, levenshtein, metaphone) | SOUNDEX() function | Levenshtein distance for fuzzy matching |
| pg_trgm | Trigram similarity for fuzzy search and LIKE acceleration | No equivalent | CREATE INDEX USING GIN (col gin_trgm_ops) for fast LIKE '%pattern%' |
| uuid-ossp | UUID generation functions | NEWID() function | gen_random_uuid() built-in since PG 13 |
| hstore | Key-value storage | N/A (use JSON) | Largely superseded by JSONB |
| citext | Case-insensitive text type | Case-insensitive collation | Avoids LOWER() everywhere for case-insensitive fields |
| earthdistance | Earth-surface distance calculations | SQL Server Spatial | Simpler than PostGIS for basic geo distance |
| pg_prewarm | Warm the buffer cache after restart | Indirect via DBCC PINTABLE (deprecated) | Load table into shared_buffers proactively |
| lo | Large Object management | FILESTREAM (partial) | For storing large binary objects in the database |
| dblink | Cross-database queries | Linked Server | Connect to another PG database for ad-hoc queries |
| postgres_fdw | Foreign Data Wrapper for PostgreSQL | Linked Server | Federate queries across PG instances |
| file_fdw | Read CSV/text files as a table | BULK INSERT / OPENROWSET | SELECT * FROM a table backed by a CSV file |
| oracle_fdw | Foreign Data Wrapper for Oracle | Linked Server to Oracle | Query Oracle tables from PG |
| wal2json | WAL decoding to JSON (CDC) | Change Data Capture (CDC) or Change Tracking | Outputs row changes as JSON via logical decoding |
| pgaudit | Detailed audit logging | SQL Server Audit | Logs DDL and DML operations for compliance |

**Installing and using an extension:**
```sql
-- Extensions are installed per-database:
CREATE EXTENSION pg_stat_statements;
CREATE EXTENSION postgis;
CREATE EXTENSION pg_trgm;

-- List installed extensions:
SELECT name, default_version, installed_version, comment
FROM pg_available_extensions
WHERE installed_version IS NOT NULL;

-- Drop an extension:
DROP EXTENSION pg_trgm;
```

### 19.2 Foreign Data Wrappers (FDW)

FDW is the PG equivalent of SQL Server Linked Servers, but more standards-based and flexible.

```sql
-- postgres_fdw example (link to another PG database):
CREATE EXTENSION postgres_fdw;

CREATE SERVER remote_server
    FOREIGN DATA WRAPPER postgres_fdw
    OPTIONS (host 'remote.host.com', port '5432', dbname 'remotedb');

CREATE USER MAPPING FOR CURRENT_USER
    SERVER remote_server
    OPTIONS (user 'remote_user', password 'secret');

-- Import schema from remote server:
IMPORT FOREIGN SCHEMA public
    FROM SERVER remote_server
    INTO local_schema;

-- Or create an individual foreign table:
CREATE FOREIGN TABLE remote_orders (
    order_id INTEGER,
    customer_id INTEGER,
    amount NUMERIC
)
SERVER remote_server
OPTIONS (schema_name 'public', table_name 'orders');

-- Query it like a local table:
SELECT * FROM remote_orders WHERE amount > 1000;
```

---

## 20. Operational Patterns and Anti-Patterns

### 20.1 SQL Server Habits to Unlearn

| SQL Server Habit | Why It Does Not Apply in PostgreSQL | PostgreSQL Best Practice |
|---|---|---|
| Using WITH (NOLOCK) everywhere | PG MVCC means readers never block writers; dirty reads are impossible | Remove all NOLOCK hints; trust MVCC |
| Fear of SELECT on production | NOLOCK is not needed; reads do not block | Use standard SELECT; MVCC handles concurrency |
| Clustered index on every table | PG has no clustered index; all tables are heaps | Define a good primary key; BRIN indexes for time-ordered data |
| Relying on IDENTITY always going up | PG sequences can have gaps (rollback, crash) | Design for gaps in sequence values; never treat sequence as gapless |
| Using VARCHAR(MAX) for everything | PG TEXT has no size limit; use TEXT | Use TEXT instead of VARCHAR(MAX); VARCHAR(n) when you want enforcement |
| Using N-prefixed types (NVARCHAR) | PG is always UTF-8 Unicode | Use TEXT or VARCHAR; N prefixes do not exist |
| Disabling AUTO UPDATE STATISTICS | Auto-update stats prevents bad plans | Never disable autovacuum or auto-analyze in PG |
| Using SELECT INTO for temp tables | PG uses CREATE TEMP TABLE or CREATE TABLE AS | Use CREATE TEMP TABLE or CREATE TABLE AS SELECT |
| Using @@ROWCOUNT | @@ROWCOUNT after DML | Use GET DIAGNOSTICS row_count = ROW_COUNT; in PL/pgSQL |
| Heavy use of cursors | Cursors are slow in both; PG FOR loops are better | Use set-based SQL; use PG FOR rec IN SELECT ... LOOP |
| Using TOP without ORDER BY | Non-deterministic in both | Always pair LIMIT with ORDER BY for reproducible results |
| Ignoring connection count | SQL Server threads are cheap; PG processes are not | Use PgBouncer; design for fewer, longer-lived connections |
| Ignoring table bloat | SQL Server reclaims space automatically | Monitor n_dead_tup; tune autovacuum for high-churn tables |
| Assuming DDL is not transactional | In SQL Server, DDL is auto-committed | In PG, DDL is fully transactional; use this to your advantage |
| Using square bracket quoting | [mytable] is SQL Server-specific | Use "double quotes" or (preferably) avoid reserved words |
| Mixing GETDATE() and SYSDATETIME() | Use NOW() or CURRENT_TIMESTAMP in PG | PG NOW() returns TIMESTAMPTZ; LOCALTIMESTAMP returns TIMESTAMP |
| Relying on implicit type coercion | SQL Server silently converts types often | PG is stricter; add explicit casts (::) when needed |
| Using three-part names for cross-db | db.schema.table is PG-unsupported | Use postgres_fdw or move data to the same database |
| PRINT for debugging | PG uses RAISE NOTICE | RAISE NOTICE 'value is: %', myvar; |

### 20.2 PostgreSQL Best Practices for SQL Server Professionals

| Practice | Recommendation | Explanation |
|---|---|---|
| Always use TIMESTAMPTZ | Use TIMESTAMP WITH TIME ZONE instead of TIMESTAMP | TIMESTAMPTZ stores in UTC and converts to local time on display; avoids timezone bugs |
| Use RETURNING instead of OUTPUT | INSERT/UPDATE/DELETE ... RETURNING * | PG RETURNING is the equivalent of SQL Server OUTPUT clause |
| Prefer GEN_RANDOM_UUID() over sequences for distributed IDs | gen_random_uuid() is built-in since PG 13 | UUIDs avoid sequence hot spots in distributed inserts |
| Use partial indexes aggressively | CREATE INDEX ... WHERE status='active' | Very low overhead; dramatically speeds up filtered queries |
| Use EXPLAIN ANALYZE with BUFFERS | Always include BUFFERS for real diagnosis | Shows cache hits vs. disk reads; essential for tuning |
| Set statement_timeout and lock_timeout | Prevent runaway queries and lock waits | SET statement_timeout = '30s'; in connection or role default |
| Monitor pg_stat_activity for idle-in-transaction | Idle-in-transaction sessions hold locks and prevent VACUUM | Alert and kill sessions WHERE state = 'idle in transaction' AND duration > 5 minutes |
| Enable pg_stat_statements in shared_preload_libraries | Must be loaded at server startup | Most important tool for query performance analysis in PG |
| Use COPY for bulk loads instead of INSERT | COPY is 10-100x faster than row-by-row INSERT | The equivalent of BULK INSERT; works with CSV and binary formats |
| Set per-table autovacuum for large or high-churn tables | Default autovacuum thresholds are too high for large tables | ALTER TABLE t SET (autovacuum_vacuum_scale_factor=0.01) |
| Keep transaction duration short | Long transactions block VACUUM and cause bloat | Avoid idle-in-transaction; commit as soon as possible |
| Use LISTEN/NOTIFY for async messaging | pg_notify(channel, payload) + LISTEN channel | Lightweight pub/sub for event-driven architectures |
| Use advisory locks for distributed job control | pg_advisory_lock(hashtext('job_name')) | Prevents multiple workers running the same job |
| Prefer JSONB over JSON | JSONB is parsed, indexed, and queryable | JSONB is the right choice in essentially every scenario |
| Add comments to all objects | COMMENT ON TABLE t IS 'description' | Stored in pg_description; visible in pgAdmin and \d+ output |

---

## Appendix A: Quick Reference -- Most Common Translations

| Task | SQL Server | PostgreSQL |
|---|---|---|
| Get current date/time | GETDATE() | NOW() or CURRENT_TIMESTAMP |
| Get current date | CAST(GETDATE() AS DATE) | CURRENT_DATE |
| Get current UTC time | GETUTCDATE() | NOW() AT TIME ZONE 'UTC' |
| String length | LEN(str) | LENGTH(str) or CHAR_LENGTH(str) |
| Substring | SUBSTRING(str, start, len) | SUBSTRING(str FROM start FOR len) or SUBSTR(str, start, len) |
| String position | CHARINDEX(find, str) | POSITION(find IN str) or STRPOS(str, find) |
| Uppercase | UPPER(str) | UPPER(str) |
| Lowercase | LOWER(str) | LOWER(str) |
| Trim whitespace | LTRIM(RTRIM(str)) | TRIM(str) or LTRIM(str) / RTRIM(str) |
| Pad left | RIGHT('00000' + CAST(n AS VARCHAR), 5) | LPAD(n::TEXT, 5, '0') |
| Pad right | N/A simple function | RPAD(str, 5, ' ') |
| Replace in string | REPLACE(str, old, new) | REPLACE(str, old, new) |
| Split string | STRING_SPLIT(str, ',') | STRING_TO_TABLE(str, ',') (PG 16) or regexp_split_to_table() |
| Convert to string | CAST(n AS VARCHAR) or STR(n) | n::TEXT or CAST(n AS TEXT) |
| Null coalescence | ISNULL(a, b) or COALESCE(a,b) | COALESCE(a, b) |
| Conditional expression | CASE WHEN ... THEN ... END | CASE WHEN ... THEN ... END |
| Row number | ROW_NUMBER() OVER (...) | ROW_NUMBER() OVER (...) |
| Top N rows | SELECT TOP 10 * FROM t | SELECT * FROM t LIMIT 10 |
| Random rows | SELECT TOP 10 * FROM t ORDER BY NEWID() | SELECT * FROM t ORDER BY RANDOM() LIMIT 10 |
| Absolute value | ABS(n) | ABS(n) |
| Round | ROUND(n, decimals) | ROUND(n, decimals) |
| Floor | FLOOR(n) | FLOOR(n) |
| Ceiling | CEILING(n) | CEIL(n) or CEILING(n) |
| Modulo | n % m | n % m or MOD(n, m) |
| Power | POWER(n, exp) | POWER(n, exp) or n ^ exp |
| Check if table exists | OBJECT_ID('tablename') IS NOT NULL | to_regclass('schema.tablename') IS NOT NULL |
| Create if not exists | IF NOT EXISTS (SELECT...) CREATE TABLE ... | CREATE TABLE IF NOT EXISTS ... |
| Drop if exists | DROP TABLE IF EXISTS t | DROP TABLE IF EXISTS t |
| List databases | SELECT name FROM sys.databases | SELECT datname FROM pg_database |
| Current database | DB_NAME() | CURRENT_DATABASE() |
| Current user | SUSER_NAME() or SYSTEM_USER | CURRENT_USER |
| Current schema | SCHEMA_NAME() | CURRENT_SCHEMA() |
| Object definition | sp_helptext or sys.sql_modules | pg_get_viewdef(), pg_get_functiondef(), \d+ in psql |
| Escape single quote | '' (double single quote) | '' (double single quote) or $$ dollar quoting $$ |
| Generate UUID | NEWID() | gen_random_uuid() |
| Hash value | HASHBYTES('SHA2_256', str) | digest(str, 'sha256') via pgcrypto extension |
| Encode to base64 | N/A natively | encode(data::BYTEA, 'base64') |
| Regex match | Not available (LIKE only) | str ~ 'pattern' (case-sensitive) or str ~* 'pattern' (case-insensitive) |

---

## Appendix B: pg_hba.conf Authentication Methods Reference

| Method | Description | When to Use |
|---|---|---|
| trust | Allow connection without password | Local development only; never in production |
| reject | Unconditionally reject | Block specific hosts or users |
| peer | OS username must match PG username | Local Unix socket connections; CLI tools |
| ident | Like peer but for TCP (uses ident server) | Rare; requires ident server on client host |
| password | Plain text password (insecure) | Never; use scram-sha-256 instead |
| md5 | MD5-hashed password | Legacy; prefer scram-sha-256 |
| scram-sha-256 | Secure challenge-response auth | Production standard (PG 10+) |
| gss | Kerberos/GSSAPI (Windows AD integration) | Windows/Active Directory environments |
| sspi | Windows SSPI (Windows only) | Windows-only; similar to GSSAPI |
| ldap | Authenticate via LDAP server | Enterprise directory integration |
| radius | RADIUS server authentication | Enterprise network auth |
| cert | Client SSL certificate | Highest security; mutual TLS |

---

## Appendix C: Error Code Reference (SQLSTATE)

| Category | SQL Server Error | PostgreSQL SQLSTATE | PG Exception Name |
|---|---|---|---|
| Duplicate key | 2627, 2601 | 23505 | unique_violation |
| Foreign key violation | 547 | 23503 | foreign_key_violation |
| Not null violation | 515 | 23502 | not_null_violation |
| Check constraint violation | 547 | 23514 | check_violation |
| Deadlock | 1205 | 40P01 | deadlock_detected |
| Serialization failure | 1205 (different) | 40001 | serialization_failure |
| Division by zero | 8134 | 22012 | division_by_zero |
| Invalid text representation | N/A | 22P02 | invalid_text_representation |
| Numeric overflow | 8115 | 22003 | numeric_value_out_of_range |
| Insufficient privilege | 229 | 42501 | insufficient_privilege |
| Undefined table | 208 | 42P01 | undefined_table |
| Undefined column | 207 | 42703 | undefined_column |
| Undefined function | N/A | 42883 | undefined_function |
| Syntax error | 102 | 42601 | syntax_error |
| Too many connections | 17810 | 53300 | too_many_connections |
| Out of memory | 701 | 53200 | out_of_memory |
| Disk full | 1105 | 53100 | disk_full |
| Transaction rollback | 3609 | 40000 | transaction_rollback |
| Lock timeout | 1222 | 55P03 | lock_not_available |

---

*End of Document*

*This document covers PostgreSQL 16 and SQL Server 2022. Many features have version-specific availability; always consult official documentation for your specific version.*

*For course materials, corrections, and updates, contact your instructor.*
