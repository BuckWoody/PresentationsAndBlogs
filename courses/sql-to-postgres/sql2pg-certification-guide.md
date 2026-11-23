![](https://github.com/BuckWoody/PresentationsAndBlogs/blob/master/graphics/logo.png?raw=true)

# PostgreSQL for the SQL Server Professional: A Certification Guide

**Course Reference Document**
**Edition: November 2026**

---

## Table of Contents

- [PostgreSQL for the SQL Server Professional: A Certification Guide](#postgresql-for-the-sql-server-professional-a-certification-guide)
  - [Table of Contents](#table-of-contents)
  - [1. The Certification Landscape](#1-the-certification-landscape)
  - [2. Certifications at a Glance](#2-certifications-at-a-glance)
  - [3. Choosing a Path](#3-choosing-a-path)
  - [4. Mapping This Course to the Exams](#4-mapping-this-course-to-the-exams)
  - [5. SQL Server Habits That Cost Exam Points](#5-sql-server-habits-that-cost-exam-points)
  - [6. Study Plan](#6-study-plan)
  - [7. Study Resources](#7-study-resources)

---

## 1. The Certification Landscape

PostgreSQL has no single owner, so there is no single official certification. The PostgreSQL Global Development Group does not certify anyone -- vendors and independent certification bodies do. For a SQL Server professional used to one Microsoft path, this is the biggest adjustment.

| Concept | SQL Server | PostgreSQL | Notes |
|---|---|---|---|
| Who certifies | Microsoft, the platform owner | Vendors (EDB) and certification bodies (LPI-Japan / EDUCO) | The PostgreSQL project itself issues no certification |
| Core DBA credential | DP-300: Azure Database Administrator Associate | EDB Essentials for PostgreSQL; OSS-DB Silver | Both PostgreSQL options focus on self-managed servers |
| Advanced DBA credential | None (DP-300 is the top DBA credential) | EDB Advanced for PostgreSQL; OSS-DB Gold | Tuning, monitoring, and troubleshooting |
| Managed cloud service | DP-300 covers Azure SQL | No PostgreSQL credential from Microsoft or AWS | DP-300 does not cover Azure Database for PostgreSQL; AWS retired its Database Specialty exam in April 2024 |
| Version targeting | Role-based, updated continuously | Tied to PostgreSQL major versions | Check which version an exam targets before you study |
| Renewal | Free annual online assessment | Varies by issuer | OSS-DB certification stays active for 5 years |
| Test delivery | Pearson VUE, online or test center | OSS-DB: Pearson VUE; EDB: EDB training portal | |

---

## 2. Certifications at a Glance

| Certification | Issuer | PostgreSQL Version | Covers | Cost | Format |
|---|---|---|---|---|---|
| EDB Essentials for PostgreSQL | EDB | 18, 16, 14 | Architecture, installation, configuration, security, monitoring, backup and PITR, maintenance, moving data, replication | See EDB training portal | See EDB training portal |
| EDB Advanced for PostgreSQL | EDB | 18, 16 | Monitoring, SQL and performance tuning, benchmarking, extensions, partitioning, connection pooling, FDWs, upgrades | See EDB training portal | See EDB training portal |
| OSS-DB Silver | LPI-Japan (EDUCO outside Japan) | 12 to 14 (exam v3.0) | General knowledge, operation and management, SQL development | US$150 plus tax | 50 questions, 90 minutes, Pearson VUE |
| OSS-DB Gold | LPI-Japan (EDUCO outside Japan) | 12 to 14 (exam v3.0) | Operation and management, performance monitoring, performance tuning, troubleshooting | US$150 plus tax | 30 questions, 90 minutes, Pearson VUE |
| Google Professional Cloud Database Engineer | Google Cloud | Not version-specific | Designing, managing, migrating, and deploying Google Cloud databases | US$200 plus tax | 50 to 60 questions, 2 hours, online or test center |

**Notes:**

- EDB topics follow the outlines of EDB's matching instructor-led courses (Essentials: 4 days; Advanced: 3 days). Each course includes one exam attempt.
- EDB publishes exam pricing and format on its training portal (training.enterprisedb.com), not on its public pages. Check there before you buy.
- EDB also certifies its own products: EDB Postgres AI Database (Oracle-compatible Advanced Server), CloudNativePG (Kubernetes), High Availability, and WarehousePG. Choose the *for PostgreSQL* exams unless your shop runs those products.
- OSS-DB Silver has no prerequisites. Gold certification requires an active Silver certification.
- The Google exam covers all Google Cloud database services. PostgreSQL is one engine among several.

---

## 3. Choosing a Path

| If you... | Start with | Then | Notes |
|---|---|---|---|
| Administer self-managed PostgreSQL (VM or on-premises) | EDB Essentials for PostgreSQL | EDB Advanced for PostgreSQL | Closest match to the DBA content in this course |
| Want a credential from an independent, non-vendor body | OSS-DB Silver | OSS-DB Gold | Published objectives and sample questions; targets older versions (12 to 14) |
| Run Azure Database for PostgreSQL or Amazon RDS / Aurora | EDB Essentials for PostgreSQL | EDB Advanced for PostgreSQL | Managed services hide some admin tasks the exams test -- practice those on a VM |
| Run PostgreSQL on Google Cloud | EDB Essentials for PostgreSQL | Google Professional Cloud Database Engineer | Prove the engine first, then the platform |
| Run EDB Postgres Advanced Server (Oracle compatibility) | EDB Postgres AI Database Essentials | EDB Postgres AI Database Advanced | Same structure as the *for PostgreSQL* exams |
| Run PostgreSQL on Kubernetes | EDB Essentials for PostgreSQL | EDB Essentials for CloudNativePG | CloudNativePG assumes core PostgreSQL knowledge |

---

## 4. Mapping This Course to the Exams

Exam topics below follow EDB's published course outlines. For OSS-DB, use the [detailed objectives](https://oss-db.jp/eng_examarea) as your checklist. Rows marked *Not covered* are gaps to study from the [PostgreSQL documentation](https://www.postgresql.org/docs/current/admin.html).

| Exam Topic | Exam | Course Module | Rosetta Stone |
|---|---|---|---|
| Architecture (processes, memory, MVCC, WAL) | Essentials | [01](01-introduction-and-overview.md) (1.1) | [1](sql2pg-rosetta-stone.md#1-architecture) |
| Installation and configuration | Essentials | [01](01-introduction-and-overview.md) (1.3) | [2](sql2pg-rosetta-stone.md#2-installation-and-configuration) |
| psql and command-line tools | Essentials | [01](01-introduction-and-overview.md) | [3](sql2pg-rosetta-stone.md#3-connectivity-and-client-tools) |
| Data dictionary (system catalogs) | Essentials | [01](01-introduction-and-overview.md) | [16](sql2pg-rosetta-stone.md#16-system-catalogs-and-metadata) |
| Creating and managing databases | Essentials | [02](02-data-types-and-schema-design.md) | [1.3](sql2pg-rosetta-stone.md#1-architecture), [5.6](sql2pg-rosetta-stone.md#5-sql-language-and-syntax) |
| SQL primer | Essentials | [03](03-tsql-to-pl-pgsql.md) | [5](sql2pg-rosetta-stone.md#5-sql-language-and-syntax) |
| Database security (roles, privileges, pg_hba.conf) | Essentials | [05](05-administration-and-security.md) (5.1, 5.2) | [10](sql2pg-rosetta-stone.md#10-security-and-access-control) |
| Backup, recovery, and PITR | Essentials | [05](05-administration-and-security.md) (5.3) | [13](sql2pg-rosetta-stone.md#13-backup-and-recovery) |
| Routine maintenance (VACUUM, ANALYZE) | Essentials | [04](04-indexes-and-performance.md) (4.4) | [12](sql2pg-rosetta-stone.md#12-administration-and-maintenance) |
| Moving data (COPY, pg_dump) | Essentials | [05](05-administration-and-security.md) (5.3), [06](06-advanced-features-and-migration.md) (6.4) | [13.2](sql2pg-rosetta-stone.md#13-backup-and-recovery) |
| Replication and high availability | Essentials | [06](06-advanced-features-and-migration.md) (6.3, logical only) | [14](sql2pg-rosetta-stone.md#14-high-availability-and-replication) |
| Database monitoring | Essentials, Advanced | [05](05-administration-and-security.md) (5.4) | [12.3](sql2pg-rosetta-stone.md#12-administration-and-maintenance) |
| SQL and performance tuning | Advanced | [04](04-indexes-and-performance.md) (4.3, 4.4) | [15](sql2pg-rosetta-stone.md#15-performance-tuning-and-query-optimization) |
| Extensions | Advanced | [06](06-advanced-features-and-migration.md) (6.2) | [19.1](sql2pg-rosetta-stone.md#19-extensions-and-ecosystem) |
| Foreign Data Wrappers | Advanced | [06](06-advanced-features-and-migration.md) (6.3) | [19.2](sql2pg-rosetta-stone.md#19-extensions-and-ecosystem) |
| Table partitioning | Advanced | *Not covered* | [9](sql2pg-rosetta-stone.md#9-partitioning) |
| Connection pooling | Advanced | [01](01-introduction-and-overview.md) (overview only) | [15.5](sql2pg-rosetta-stone.md#15-performance-tuning-and-query-optimization) |
| Performance benchmarking (pgbench) | Advanced | *Not covered* | *Not covered* |
| Upgrades (pg_upgrade, logical replication) | Advanced | *Not covered* | *Not covered* |

---

## 5. SQL Server Habits That Cost Exam Points

EDB lists Linux experience as a helpful prerequisite. If you have only run PostgreSQL on Windows through a GUI, practice on Linux with psql before the exam.

| SQL Server Habit | PostgreSQL Answer | Rosetta Stone |
|---|---|---|
| Logins and users are separate objects | One object: a role. CREATE USER is CREATE ROLE ... LOGIN | [10.2](sql2pg-rosetta-stone.md#10-security-and-access-control) |
| Logins and endpoints control who connects | pg_hba.conf controls connections; the first matching line wins; reload to apply changes | [2.4](sql2pg-rosetta-stone.md#2-installation-and-configuration) |
| Change settings with sp_configure | Edit postgresql.conf or use ALTER SYSTEM; pg_settings.context tells you reload or restart | [2.2](sql2pg-rosetta-stone.md#2-installation-and-configuration) |
| Recovery model controls log retention | No recovery models; PITR needs a base backup plus archived WAL | [1.5](sql2pg-rosetta-stone.md#1-architecture), [13](sql2pg-rosetta-stone.md#13-backup-and-recovery) |
| A database backup includes its logins | pg_dump covers one database; roles and tablespaces need pg_dumpall --globals-only | [13.2](sql2pg-rosetta-stone.md#13-backup-and-recovery) |
| Updates change rows in place | Every UPDATE writes a new row version; dead rows wait for VACUUM | [1.4](sql2pg-rosetta-stone.md#1-architecture) |
| Shrink returns space to the OS | VACUUM makes space reusable; VACUUM FULL rewrites the table under an exclusive lock | [12.2](sql2pg-rosetta-stone.md#12-administration-and-maintenance) |
| Object names are case-insensitive | Unquoted names fold to lowercase; quoted names are case-sensitive | [1.3](sql2pg-rosetta-stone.md#1-architecture) |
| A clustered index keeps table order | No clustered indexes; CLUSTER reorders once and is not maintained | [7.1](sql2pg-rosetta-stone.md#7-indexing) |
| Query across databases with three-part names | Not supported; use postgres_fdw or dblink | [1.3](sql2pg-rosetta-stone.md#1-architecture) |
| SNAPSHOT is an opt-in isolation level | REPEATABLE READ is snapshot isolation; MVCC is always on | [11.2](sql2pg-rosetta-stone.md#11-transactions-and-concurrency) |
| Stored procedures do everything | Functions return values; procedures run with CALL and can COMMIT | [6.6](sql2pg-rosetta-stone.md#6-procedural-programming-t-sql-vs-plpgsql) |

---

## 6. Study Plan

1. **Choose your exam and version.** Use [Section 3](#3-choosing-a-path). This course uses PostgreSQL 17; EDB exams target 16 and 18, so read the release notes for the version you choose.
2. **Finish this course.** Complete Modules 01 to 06, then close the gaps marked *Not covered* in [Section 4](#4-mapping-this-course-to-the-exams).
3. **Build a Linux lab.** On a Linux VM or container, do every task with psql: initialize a cluster, edit pg_hba.conf, create roles, take and restore a base backup, and build a streaming replica.
4. **Read the documentation.** Work through the [Server Administration](https://www.postgresql.org/docs/current/admin.html) part of the PostgreSQL documentation for your exam's version.
5. **Drill the habits.** Review [Section 5](#5-sql-server-habits-that-cost-exam-points) until the PostgreSQL answer comes first.
6. **Practice with official material only.** OSS-DB publishes sample questions. Avoid "exam dump" sites: they violate candidate agreements and are often wrong.

---

## 7. Study Resources

| Resource | Covers | Cost |
|---|---|---|
| [PostgreSQL Documentation: Server Administration](https://www.postgresql.org/docs/current/admin.html) | Installation, configuration, authentication, roles, maintenance, backup, HA, monitoring | Free |
| [EDB Training](https://www.enterprisedb.com/training) | On-demand courses; instructor-led Essentials and Advanced courses | On-demand: free; instructor-led: contact EDB |
| [EDB Certification Exams Catalog](https://www.enterprisedb.com/training/certification-exams) | Current EDB exams and versions | -- |
| [OSS-DB Exam (English)](https://oss-db.jp/eng_exam) | Exam overview, fees, and registration | -- |
| [OSS-DB Detailed Objectives](https://oss-db.jp/eng_examarea) | Topic checklist for Silver and Gold | Free |
| [OSS-DB Sample Questions](https://oss-db.jp/eng_sample) | Practice questions | Free |
| [Postgres Professional DBA1 Course](https://edu.postgrespro.com/16/dba1-16-en/dba1_00_introduction.html) | Administration courseware (DBA1 and DBA2 available in English) | Free |
| [Google Professional Cloud Database Engineer](https://cloud.google.com/learn/certification/cloud-database-engineer) | Exam guide and learning path | Exam: US$200 |
| [Rosetta Stone](sql2pg-rosetta-stone.md) | Side-by-side SQL Server and PostgreSQL reference | Free |

---

*End of Document*

*Certification programs change often. Exam names, versions, prices, and formats in this guide were checked against each issuer's public pages in November 2026; confirm them with the issuer before you register.*

*For course materials, corrections, and updates, contact your instructor.*
