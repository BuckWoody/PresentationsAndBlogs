![](graphics/microsoftlogo.png)

# Workshop: PostgreSQL for the SQL Server Database Professional

#### <i>A SQL Server to PostgreSQL Skilling</i>


<p style="border-bottom: 1px solid lightgrey;"></p>

<img style="float: left; margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/textbubble.png"> <h2>Module 05 – Administration and Security</h2>

*Estimated Time: 60 minutes (≈20 minutes lecture, ≈40 minutes hands-on)*

This module covers the administrative tasks that SQL Server DBAs perform daily — creating users, managing permissions, backing up and restoring databases, and monitoring server health. For each task you will see the SQL Server approach alongside the PostgreSQL equivalent.

<p style="border-bottom: 1px solid lightgrey;"></p>

<h2><img style="float: left; margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/pencil2.png">5.1 – Users, Roles, and Privileges</h2>

SQL Server has a two-layer security model: **Logins** (server-level principals that can authenticate) and **Users** (database-level principals mapped to a login). PostgreSQL has a **unified model**: there is only one type of principal called a **Role**. A role can log in (if `LOGIN` attribute is set), own objects, and be a member of other roles. This is more similar to how SQL Server's fixed server roles work than its login/user split.

**Comparison table:**

| SQL Server Concept | PostgreSQL Equivalent |
|---|---|
| Login | Role with `LOGIN` attribute |
| User (database) | Role with `LOGIN` granted access to a database via `GRANT CONNECT` |
| Role (server-level) | Role without `LOGIN` (a group role) |
| `sysadmin` fixed server role | `SUPERUSER` attribute |
| `db_owner` fixed database role | Role with `GRANT ALL PRIVILEGES ON DATABASE` |
| `db_datareader` fixed database role | Role with `GRANT SELECT ON ALL TABLES IN SCHEMA public` |
| `db_datawriter` | Role with `GRANT INSERT, UPDATE, DELETE ON ALL TABLES` |
| `GRANT EXECUTE ON PROCEDURE` | `GRANT EXECUTE ON FUNCTION` |
| Schema ownership | `ALTER SCHEMA ... OWNER TO role` |

**Creating roles and granting access:**

```sql
-- SQL Server:
-- CREATE LOGIN app_user WITH PASSWORD = 'SecurePass123!';
-- CREATE USER app_user FOR LOGIN app_user;
-- GRANT SELECT ON SCHEMA::sales TO app_user;

-- PostgreSQL Step 1: Create a login role:
CREATE ROLE app_user
    WITH LOGIN
    PASSWORD 'SecurePass123!'
    NOSUPERUSER
    NOCREATEDB
    NOCREATEROLE
    VALID UNTIL '2025-12-31';    -- No SQL Server equivalent for logins; use for accounts

-- PostgreSQL Step 2: Grant connection to the database:
GRANT CONNECT ON DATABASE adventureworks TO app_user;

-- PostgreSQL Step 3: Grant schema usage (required before table-level grants):
GRANT USAGE ON SCHEMA sales TO app_user;
GRANT USAGE ON SCHEMA person TO app_user;

-- PostgreSQL Step 4: Grant object-level permissions:
GRANT SELECT ON ALL TABLES IN SCHEMA sales   TO app_user;
GRANT SELECT ON ALL TABLES IN SCHEMA person  TO app_user;

-- Grant future tables too (SQL Server has no equivalent — you must re-grant):
ALTER DEFAULT PRIVILEGES IN SCHEMA sales
    GRANT SELECT ON TABLES TO app_user;

-- PostgreSQL Step 5: Grant execute on functions:
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA sales TO app_user;
```

**Role groups (equivalent to SQL Server database roles):**

```sql
-- Create a group role (no LOGIN):
CREATE ROLE reporting_role;

-- Grant permissions to the group:
GRANT CONNECT ON DATABASE adventureworks TO reporting_role;
GRANT USAGE   ON SCHEMA sales            TO reporting_role;
GRANT SELECT  ON ALL TABLES IN SCHEMA sales TO reporting_role;

-- Add users to the group:
GRANT reporting_role TO app_user;

-- Revoke from group:
REVOKE reporting_role FROM app_user;
```

**Row-Level Security (RLS) — PostgreSQL equivalent of SQL Server RLS:**

```sql
-- Enable RLS on a table:
ALTER TABLE sales.sales_order_header ENABLE ROW LEVEL SECURITY;

-- Create a policy (equivalent to SQL Server security predicate):
CREATE POLICY sales_policy ON sales.sales_order_header
    FOR SELECT
    USING (customer_id = current_setting('app.current_customer_id')::INTEGER);

-- Set the session variable in application code:
-- SET app.current_customer_id = '42';
-- SELECT * FROM sales.sales_order_header;  -- Returns only customer 42's orders

-- Superusers bypass RLS by default; to enforce on table owner:
ALTER TABLE sales.sales_order_header FORCE ROW LEVEL SECURITY;
```

<h3>5.2 – pg_hba.conf: Host-Based Authentication</h3>

The `pg_hba.conf` file controls who can connect to PostgreSQL, from where, and using what authentication method. There is no equivalent single file in SQL Server — this level of control is distributed across Windows Firewall, SQL Server Configuration Manager, and SQL Server's authentication settings.

The format of each line is:
```
TYPE  DATABASE  USER  ADDRESS       METHOD
local all       all                 md5
host  all       all   127.0.0.1/32  scram-sha-256
host  all       all   0.0.0.0/0     scram-sha-256
```

- **TYPE:** `local` (Unix socket), `host` (TCP/IP), `hostssl` (SSL required), `hostnossl`
- **DATABASE:** Database name, `all`, or `sameuser`
- **USER:** Role name, `all`, or a role group with `+rolename`
- **ADDRESS:** IP address or CIDR range (only for `host` records)
- **METHOD:** `scram-sha-256` (recommended), `md5`, `trust` (no password — only for local dev!), `peer`, `cert`, `ldap`, `radius`

```sql
-- After editing pg_hba.conf, reload without restart:
SELECT pg_reload_conf();

-- Check current connections and their auth method:
SELECT usename, client_addr, auth_method
FROM pg_stat_activity
WHERE client_addr IS NOT NULL;
```

<p style="border-bottom: 1px solid lightgrey;"></p>

<h2><img style="float: left; margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/pencil2.png">5.3 – Backup and Restore</h2>

PostgreSQL has three primary backup tools — each with a different scope and use case, analogous to SQL Server's backup strategy.

| Backup Type | PostgreSQL Tool | SQL Server Equivalent |
|---|---|---|
| Logical (single database) | `pg_dump` | `BACKUP DATABASE ... TO DISK` |
| Logical (entire cluster) | `pg_dumpall` | `BACKUP DATABASE ALL` (plus system DBs) |
| Physical (entire cluster) | `pg_basebackup` | Full database backup (all databases) |
| Point-in-time recovery | WAL archiving + `pg_basebackup` | Transaction log backup chain |

**pg_dump — the everyday backup tool:**

```sql
-- Backup a single database to a custom-format archive (compressed, supports parallel restore):
pg_dump -U postgres -h localhost -d adventureworks -F c -f adventureworks.dump

-- Backup to plain SQL (readable, portable, slower to restore):
pg_dump -U postgres -h localhost -d adventureworks -F p -f adventureworks.sql

-- Backup only a specific schema:
pg_dump -U postgres -h localhost -d adventureworks -n sales -F c -f sales_schema.dump

-- Backup only specific tables:
pg_dump -U postgres -h localhost -d adventureworks -t sales.sales_order_header -F c -f orders.dump

-- Parallel dump (faster for large databases, requires directory format):
pg_dump -U postgres -h localhost -d adventureworks -F d -j 4 -f adventureworks_dir/
```

**pg_restore — restoring from custom-format archives:**

```sql
-- Restore to a new database:
createdb -U postgres adventureworks_restored
pg_restore -U postgres -h localhost -d adventureworks_restored adventureworks.dump

-- Restore only specific schemas or tables:
pg_restore -U postgres -h localhost -d adventureworks_restored -n sales adventureworks.dump

-- Parallel restore:
pg_restore -U postgres -h localhost -d adventureworks_restored -j 4 adventureworks_dir/

-- List contents of a dump file (like looking at a SQL Server backup file):
pg_restore -l adventureworks.dump
```

**pg_basebackup — physical cluster backup:**

```sql
-- Windows Command Prompt:
pg_basebackup -U postgres -h localhost -D C:\PGBackup\base -P -Xs -R
```

Flags: `-D` = destination directory, `-P` = show progress, `-Xs` = include WAL via streaming, `-R` = write `recovery.conf` for standby setup.

**Point-In-Time Recovery (PITR):**

Configure WAL archiving in `postgresql.conf`:

```ini
wal_level = replica
archive_mode = on
archive_command = 'copy "%p" "C:\\WALArchive\\%f"'   # Windows
# archive_command = 'cp %p /var/lib/pgsql/wal_archive/%f'  # Linux
```

To recover to a point in time: take a base backup, configure `recovery.conf` (or `postgresql.conf` in PostgreSQL 12+) with a `recovery_target_time`, then start PostgreSQL with the restored base backup. This is conceptually identical to SQL Server's log chain restore.

<p style="border-bottom: 1px solid lightgrey;"></p>

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/point1.png"><b>Activity 5.1 – Create Roles and Manage Permissions</b></p>

<p><img style="margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/checkmark.png"><b>Steps</b></p>

**Step 1 — Create roles for the AdventureWorks application:**

```sql
-- Connect as postgres superuser
\c adventureworks postgres

-- Create an application read-only role:
CREATE ROLE aw_readonly;
GRANT CONNECT ON DATABASE adventureworks TO aw_readonly;
GRANT USAGE   ON SCHEMA person, sales, production, humanresources, purchasing TO aw_readonly;
GRANT SELECT  ON ALL TABLES IN SCHEMA person, sales, production, humanresources, purchasing
    TO aw_readonly;

-- Create a reporting user that uses the read-only role:
CREATE ROLE report_user
    WITH LOGIN PASSWORD 'ReportPass1!';
GRANT aw_readonly TO report_user;

-- Create an application write role:
CREATE ROLE aw_appwrite;
GRANT CONNECT ON DATABASE adventureworks TO aw_appwrite;
GRANT USAGE   ON SCHEMA sales, person TO aw_appwrite;
GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA sales, person TO aw_appwrite;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA sales, person TO aw_appwrite;

-- Create an application user:
CREATE ROLE app_user
    WITH LOGIN PASSWORD 'AppPass1!';
GRANT aw_appwrite TO app_user;
```

**Step 2 — Test the roles:**

```sql
-- Connect as the report user and verify read access:
\c adventureworks report_user

SELECT COUNT(*) FROM person.person;         -- Should succeed
SELECT COUNT(*) FROM sales.sales_order_header; -- Should succeed

-- Try to write (should fail with permission denied):
INSERT INTO person.person (person_type, first_name, last_name)
VALUES ('IN', 'Test', 'User');              -- Should FAIL

-- Reconnect as postgres:
\c adventureworks postgres
```

**Step 3 — Inspect role memberships (equivalent to sys.database_role_members):**

```sql
SELECT r.rolname                   AS role_name,
       m.rolname                   AS member_name,
       gr.rolname                  AS granted_by
FROM pg_auth_members am
JOIN pg_roles r  ON r.oid = am.roleid
JOIN pg_roles m  ON m.oid = am.member
JOIN pg_roles gr ON gr.oid = am.grantor
ORDER BY r.rolname;

-- List all roles and their attributes:
\du
-- or:
SELECT rolname, rolsuper, rolcreatedb, rolcreaterole, rolcanlogin, rolvaliduntil
FROM pg_roles
ORDER BY rolname;
```

**Step 4 — Check object-level permissions:**

```sql
-- Table-level permissions (equivalent to fn_dbpermissions in SQL Server):
SELECT grantee,
       table_schema,
       table_name,
       privilege_type
FROM information_schema.role_table_grants
WHERE table_schema IN ('sales', 'person')
ORDER BY table_schema, table_name, grantee;
```

<p style="border-bottom: 1px solid lightgrey;"></p>

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/point1.png"><b>Activity 5.2 – Backup and Restore</b></p>

<p><img style="margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/checkmark.png"><b>Steps</b></p>

**Step 1 — Create a backup with pg_dump:**

Open a Command Prompt (not psql) and run:

```bat
REM Create a backup directory
mkdir C:\PGBackup

REM Backup the adventureworks database in custom format
pg_dump -U postgres -h localhost -d adventureworks -F c -f C:\PGBackup\adventureworks.dump

REM Backup in plain SQL format as well:
pg_dump -U postgres -h localhost -d adventureworks -F p -f C:\PGBackup\adventureworks.sql

REM List the contents of the dump (equivalent to viewing a SQL Server backup set):
pg_restore -l C:\PGBackup\adventureworks.dump
```

**Step 2 — Restore to a new database:**

```bat
REM Create the target database
createdb -U postgres -h localhost adventureworks_test

REM Restore the backup
pg_restore -U postgres -h localhost -d adventureworks_test C:\PGBackup\adventureworks.dump
```

Verify the restore in psql:

```sql
\c adventureworks_test
\dt sales.*
SELECT COUNT(*) FROM sales.sales_order_header;
```

**Step 3 — Schema-only backup (equivalent to scripting the database in SSMS):**

```bat
REM Schema only — no data:
pg_dump -U postgres -h localhost -d adventureworks --schema-only -F p -f C:\PGBackup\adventureworks_schema.sql

REM Data only — no DDL:
pg_dump -U postgres -h localhost -d adventureworks --data-only -F p -f C:\PGBackup\adventureworks_data.sql
```

**Step 4 — Monitor active connections and block/terminate them (equivalent to kill spid in SQL Server):**

```sql
\c adventureworks postgres

-- View active connections:
SELECT pid, usename, application_name, state, query_start,
       LEFT(query, 60) AS query
FROM pg_stat_activity
WHERE datname = 'adventureworks'
ORDER BY query_start;

-- Terminate a specific connection (equivalent to KILL spid):
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE datname = 'adventureworks'
  AND usename = 'report_user'
  AND state = 'idle';

-- Cancel a running query (like sending a cancel to a process — softer than terminate):
SELECT pg_cancel_backend(<pid>);
```

**Step 5 — Clean up the test database:**

```sql
\c postgres

-- You cannot drop a database while connected to it (same as SQL Server)
DROP DATABASE adventureworks_test;
```

<p style="border-bottom: 1px solid lightgrey;"></p>

<h2><img style="float: left; margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/pencil2.png">5.4 – Monitoring with pg_stat Views</h2>

PostgreSQL exposes rich monitoring information through a family of `pg_stat_*` catalog views. These are the equivalent of SQL Server's Dynamic Management Views (`sys.dm_*`).

| pg_stat View | SQL Server Equivalent |
|---|---|
| `pg_stat_activity` | `sys.dm_exec_sessions` + `sys.dm_exec_requests` |
| `pg_stat_user_tables` | `sys.dm_db_index_usage_stats` + `sys.dm_db_table_space_usage` |
| `pg_stat_user_indexes` | `sys.dm_db_index_usage_stats` |
| `pg_stat_bgwriter` | Performance Monitor: checkpoint/buffer counters |
| `pg_stat_replication` | `sys.dm_hadr_log_send_queue` / Always On DMVs |
| `pg_locks` | `sys.dm_tran_locks` |
| `pg_stat_statements` | Query Store / `sys.dm_exec_query_stats` |
| `pg_statio_user_tables` | Buffer pool hit ratio counters |

```sql
-- Check for blocking queries (equivalent to sys.dm_exec_requests with blocking_session_id):
SELECT blocked.pid                    AS blocked_pid,
       blocked.query                  AS blocked_query,
       blocking.pid                   AS blocking_pid,
       blocking.query                 AS blocking_query
FROM pg_stat_activity blocked
JOIN pg_stat_activity blocking
    ON blocking.pid = ANY(pg_blocking_pids(blocked.pid))
WHERE cardinality(pg_blocking_pids(blocked.pid)) > 0;

-- Buffer cache hit ratio (target > 99% in a well-tuned system):
SELECT SUM(heap_blks_hit)  AS buffer_hits,
       SUM(heap_blks_read) AS disk_reads,
       ROUND(
           100.0 * SUM(heap_blks_hit)
               / NULLIF(SUM(heap_blks_hit) + SUM(heap_blks_read), 0),
           2
       ) AS hit_ratio_pct
FROM pg_statio_user_tables;

-- Current lock waits:
SELECT l.pid, l.locktype, l.relation::regclass AS table_name,
       l.mode, l.granted
FROM pg_locks l
JOIN pg_stat_activity a ON a.pid = l.pid
WHERE NOT l.granted
ORDER BY l.pid;
```

<p style="border-bottom: 1px solid lightgrey;"></p>

<p><img style="margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/owl.png"><b>For Further Study</b></p>

- [PostgreSQL Documentation — Client Authentication (pg_hba.conf)](https://www.postgresql.org/docs/current/client-authentication.html)
- [PostgreSQL Documentation — Database Roles](https://www.postgresql.org/docs/current/user-manag.html)
- [PostgreSQL Documentation — Privilege System](https://www.postgresql.org/docs/current/ddl-priv.html)
- [PostgreSQL Documentation — Row Level Security](https://www.postgresql.org/docs/current/ddl-rowsecurity.html)
- [PostgreSQL Documentation — pg_dump](https://www.postgresql.org/docs/current/app-pgdump.html)
- [PostgreSQL Documentation — pg_restore](https://www.postgresql.org/docs/current/app-pgrestore.html)
- [PostgreSQL Documentation — Continuous Archiving and PITR](https://www.postgresql.org/docs/current/continuous-archiving.html)
- [PostgreSQL Documentation — Monitoring Database Activity](https://www.postgresql.org/docs/current/monitoring-stats.html)
- [PostgreSQL Documentation — Routine Vacuuming](https://www.postgresql.org/docs/current/routine-vacuuming.html)
- [Crunchy Data — PostgreSQL Security Best Practices](https://www.crunchydata.com/blog/postgres-security-best-practices)
- [pgBackRest — Advanced PostgreSQL Backup Tool](https://pgbackrest.org/)
- [Barman — Backup and Recovery Manager for PostgreSQL](https://pgbarman.org/)

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/geopin.png"><b>Next Steps</b></p>

Next, continue to <a href="06_-_Advanced_Features_and_Migration.md" target="_blank"><i>Module 06 – Advanced Features and Migration</i></a>.
