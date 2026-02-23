![](graphics/microsoftlogo.png)

# Workshop: PostgreSQL for the SQL Server Database Professional

#### <i>SQL Server to PostgreSQL Skilling</i>

<p style="border-bottom: 1px solid lightgrey;"></p>

<img style="float: left; margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/textbubble.png"> <h2>About this Workshop</h2>

Welcome to this one-day workshop on *PostgreSQL for the SQL Server Database Professional*. In this workshop, you'll learn how to apply your existing SQL Server knowledge to become productive with PostgreSQL quickly — understanding where the two platforms are similar, where they differ fundamentally, and how to translate your skills across both.

The focus of this workshop is to give experienced SQL Server professionals a guided, hands-on path to PostgreSQL competency in a single day, covering architecture, query language, development patterns, indexing, administration, and advanced features.

You'll start by understanding how the PostgreSQL engine differs from SQL Server at an architectural level, then progress through data types, T-SQL-to-PL/pgSQL translation, index strategies and query tuning, administration and security, and finally advanced features and migration tooling — with a focus on how to extrapolate what you have learned into production workloads at your organization.

This [github README.MD file](https://lab.github.com/githubtraining/introduction-to-github) explains how the workshop is laid out, what you will learn, and the technologies you will use. To download this workshop to your local computer, click the **Clone or Download** button at the top right of this page. [More about that process is here](https://help.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository).

<p style="border-bottom: 1px solid lightgrey;"></p>

<img style="float: left; margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/checkmark.png"> <h3>Learning Objectives</h3>

In this workshop you'll learn:
<br>

- How PostgreSQL's architecture (process model, MVCC, WAL, cluster vs. database) differs from SQL Server's and what that means for day-to-day work
- How to map SQL Server data types, schema objects, and DDL patterns to their PostgreSQL equivalents
- How to translate T-SQL stored procedures, functions, and scripts into PL/pgSQL, handling syntax, error handling, and control-flow differences
- How PostgreSQL's rich index ecosystem (B-tree, GIN, GiST, BRIN, partial, expression) compares to SQL Server indexes, and how to read and tune `EXPLAIN ANALYZE` output
- How to perform common DBA tasks in PostgreSQL: user/role management, backup and restore with `pg_dump`/`pg_basebackup`, VACUUM, and monitoring with `pg_stat_*` views
- How to leverage PostgreSQL-specific advanced features including JSONB, extensions (PostGIS, pg_trgm, pgvector), Foreign Data Wrappers, and migration tooling

The goal of this workshop is to train SQL Server professionals — DBAs, developers, and architects — who need to support, design, or migrate to PostgreSQL workloads.

The concepts and skills taught in this workshop form the starting points for:

- **Database Administrators and Architects** who are evaluating or migrating workloads from SQL Server to PostgreSQL (on-premises or cloud managed services such as Azure Database for PostgreSQL, Amazon RDS, or Google Cloud SQL).
- **Application Developers** who write T-SQL today and need to understand PL/pgSQL, connection drivers, and PostgreSQL-specific query patterns.
- **Data Engineers** who work across mixed-platform environments and need to bridge SQL Server and PostgreSQL for data pipelines and ELT workflows.

<p style="border-bottom: 1px solid lightgrey;"></p>

<img style="float: left; margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/building1.png"> <h2>Business Applications of this Workshop</h2>

Businesses increasingly require open-source database expertise alongside commercial platforms. PostgreSQL has become the most popular open-source relational database for new application development, and many organizations are migrating existing SQL Server workloads to PostgreSQL to reduce licensing costs, gain cloud portability, and leverage its rich extension ecosystem. Teams that already understand SQL Server can reduce the time to PostgreSQL competency dramatically by learning the platform through direct, side-by-side comparison.

Industry examples where this cross-platform expertise matters include financial services firms reducing per-core licensing spend, SaaS companies choosing PostgreSQL for multi-cloud portability, healthcare organizations adopting PostgreSQL for compliance cost reduction, and e-commerce platforms leveraging PostgreSQL's JSONB and PostGIS capabilities.

<p style="border-bottom: 1px solid lightgrey;"></p>

<img style="float: left; margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/listcheck.png"> <h2>Technologies used in this Workshop</h2>

<table style="tr:nth-child(even) {background-color: #f2f2f2;}; text-align: left; display: table; border-collapse: collapse; border-spacing: 2px; border-color: gray;">

  <tr><th style="background-color: #1b20a1; color: white;">Technology</th> <th style="background-color: #1b20a1; color: white;">Description</th></tr>

  <tr><td><i>PostgreSQL 16/17</i></td><td>The open-source object-relational database engine at the center of this workshop</td></tr>
  <tr><td><i>psql</i></td><td>PostgreSQL's native interactive terminal — the counterpart to sqlcmd</td></tr>
  <tr><td><i>pgAdmin 4</i></td><td>Cross-platform GUI administration tool for PostgreSQL, comparable to SSMS</td></tr>
  <tr><td><i>DBeaver Community</i></td><td>Universal database IDE that supports both SQL Server and PostgreSQL side-by-side</td></tr>
  <tr><td>Microsoft SQL Server 2022 (Developer Edition)</td><td>Used as the reference platform for side-by-side comparisons throughout the workshop</td></tr>
  <tr><td>Azure Database for PostgreSQL (Flexible Server)</td><td>Microsoft's managed PostgreSQL service — used to demonstrate cloud deployment differences</td></tr>
  <tr><td><i>pg_dump / pg_restore / pg_basebackup</i></td><td>PostgreSQL's native backup and restore utilities</td></tr>

</table>

<p style="border-bottom: 1px solid lightgrey;"></p>

<img style="float: left; margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/owl.png"> <h2>Before Taking this Workshop</h2>

You'll need a local system on which you can install software. The workshop demonstrations use Microsoft Windows as the operating system; all examples use Windows. Optionally, you can use a Microsoft Azure Virtual Machine (VM).

You must have a Microsoft Azure account with the ability to create assets if you wish to use Azure Database for PostgreSQL for the cloud portions of this workshop.

This workshop expects that you understand:

- Core relational database concepts (tables, indexes, joins, transactions, ACID)
- T-SQL at a working level (SELECT, DML, DDL, stored procedures, basic functions)
- SQL Server architecture concepts (databases, instances, logins, jobs, backups)

If you are new to SQL Server or relational databases, complete these references before attending:

- [T-SQL Fundamentals (Microsoft Learn)](https://learn.microsoft.com/en-us/training/paths/get-started-querying-with-transact-sql/)
- [SQL Server Administration Fundamentals (Microsoft Learn)](https://learn.microsoft.com/en-us/training/paths/sql-server-2022/)
- [PostgreSQL Tutorial (Official)](https://www.postgresql.org/docs/current/tutorial.html)


<img style="float: left; margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/bulletlist.png"> <h3>Setup</h3>

<a href="00_-_Pre-Requisites.md" target="_blank">A full pre-requisites document is located here</a>. These instructions should be completed **before** the workshop starts, since you will not have time to cover these in class. *Remember to turn off any Azure Virtual Machines from the Azure Portal when not taking the class so that you do not incur charges (shutting down the machine in the VM itself is not sufficient).*

<p style="border-bottom: 1px solid lightgrey;"></p>

<img style="float: left; margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/education1.png"> <h2>Workshop Details</h2>

This workshop uses PostgreSQL 16/17 and SQL Server 2022 Developer Edition for all comparisons and exercises, with a focus on hands-on translation of existing SQL Server skills.

<table style="tr:nth-child(even) {background-color: #f2f2f2;}; text-align: left; display: table; border-collapse: collapse; border-spacing: 5px; border-color: gray;">

  <tr><td style="background-color: Cornsilk; color: black; padding: 5px 5px;">Primary Audience:</td><td style="background-color: Cornsilk; color: black; padding: 5px 5px;">SQL Server DBAs and Developers who need to support or migrate to PostgreSQL workloads</td></tr>
  <tr><td>Secondary Audience:</td><td>Data Engineers and Solution Architects evaluating PostgreSQL for new projects</td></tr>
  <tr><td style="background-color: Cornsilk; color: black; padding: 5px 5px;">Level:</td><td style="background-color: Cornsilk; color: black; padding: 5px 5px;">200 (Intermediate — prior SQL Server experience required)</td></tr>
  <tr><td>Type:</td><td>In-Person or self-paced from GitHub</td></tr>
  <tr><td style="background-color: Cornsilk; color: black; padding: 5px 5px;">Length:</td><td style="background-color: Cornsilk; color: black; padding: 5px 5px;">6 hours (one module per hour)</td></tr>

</table>

<p style="border-bottom: 1px solid lightgrey;"></p>

<img style="float: left; margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/pinmap.png"> <h2>Related Workshops and Resources</h2>

- [Microsoft SQL Server Workshop Series](https://microsoft.github.io/sqlworkshops/)
- [Azure Database for PostgreSQL Documentation](https://learn.microsoft.com/en-us/azure/postgresql/)
- [PostgreSQL Official Documentation](https://www.postgresql.org/docs/)
- [EDB Migration Portal (SQL Server to PostgreSQL)](https://www.enterprisedb.com/products/migration-portal)

<p style="border-bottom: 1px solid lightgrey;"></p>

<img style="float: left; margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/bookpencil.png"> <h2>Workshop Modules</h2>

This is a modular workshop. In each section you'll learn concepts, technologies, and processes to help you complete the solution.

<table style="tr:nth-child(even) {background-color: #f2f2f2;}; text-align: left; display: table; border-collapse: collapse; border-spacing: 5px; border-color: gray;">

  <tr><td style="background-color: AliceBlue; color: black;"><b>Module</b></td><td style="background-color: AliceBlue; color: black;"><b>Topics</b></td></tr>

  <tr><td><a href="01_-_Introduction_and_Overview.md" target="_blank">01 – Introduction and Overview</a></td><td>Architecture comparison (process model, MVCC vs. locking, WAL vs. T-Log, cluster/database/schema hierarchy), installation, and client tools (psql, pgAdmin, DBeaver)</td></tr>

  <tr><td style="background-color: AliceBlue; color: black;"><a href="02_-_Data_Types_and_Schema_Design.md" target="_blank">02 – Data Types and Schema Design</a></td><td>SQL Server-to-PostgreSQL type mapping, DDL differences (sequences vs. IDENTITY, schemas, constraints), and loading the sample database</td></tr>

  <tr><td><a href="03_-_TSQL_to_PL_pgSQL.md" target="_blank">03 – T-SQL to PL/pgSQL</a></td><td>Query syntax differences (TOP vs. LIMIT, ISNULL vs. COALESCE, string functions, CTEs, window functions), writing stored procedures and functions in PL/pgSQL, error handling, and DO blocks</td></tr>

  <tr><td style="background-color: AliceBlue; color: black;"><a href="04_-_Indexes_and_Performance.md" target="_blank">04 – Indexes and Performance</a></td><td>Index types (B-tree, GIN, GiST, BRIN, partial, expression), reading EXPLAIN ANALYZE vs. SQL Server execution plans, autovacuum and statistics, and the Query Store vs. pg_stat_statements</td></tr>

  <tr><td><a href="05_-_Administration_and_Security.md" target="_blank">05 – Administration and Security</a></td><td>Roles and privileges (vs. SQL Server logins/users), pg_hba.conf, backup and restore (pg_dump, pg_restore, pg_basebackup), point-in-time recovery, VACUUM/ANALYZE, and monitoring with pg_stat_* views</td></tr>

  <tr><td style="background-color: AliceBlue; color: black;"><a href="06_-_Advanced_Features_and_Migration.md" target="_blank">06 – Advanced Features and Migration</a></td><td>JSONB and document storage, extensions (PostGIS, pg_trgm, pgvector, pg_partman), Foreign Data Wrappers, logical replication, and migration tooling (pgLoader, AWS SCT, EDB Migration Portal)</td></tr>

</table>

<p style="border-bottom: 1px solid lightgrey;"></p>

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/geopin.png"><b>Next Steps</b></p>

Next, continue to <a href="00_-_Pre-Requisites.md" target="_blank"><i>Pre-Requisites</i></a>.

---

# Contributing

This project welcomes contributions and suggestions. Most contributions require you to agree to a Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us the rights to use your contribution. For details, visit https://cla.opensource.microsoft.com.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

# Legal Notices

### License
Microsoft and any contributors grant you a license to the Microsoft documentation and other content in this repository under the [Creative Commons Attribution 4.0 International Public License](https://creativecommons.org/licenses/by/4.0/legalcode), see [the LICENSE file](https://github.com/MicrosoftDocs/mslearn-tailspin-spacegame-web/blob/master/LICENSE), and grant you a license to any code in the repository under [the MIT License](https://opensource.org/licenses/MIT), see the [LICENSE-CODE file](https://github.com/MicrosoftDocs/mslearn-tailspin-spacegame-web/blob/master/LICENSE-CODE).

Microsoft, Windows, Microsoft Azure and/or other Microsoft products and services referenced in the documentation may be either trademarks or registered trademarks of Microsoft in the United States and/or other countries. The licenses for this project do not grant you rights to use any Microsoft names, logos, or trademarks. Microsoft's general trademark guidelines can be found at http://go.microsoft.com/fwlink/?LinkID=254653.

Privacy information can be found at https://privacy.microsoft.com/en-us/

Microsoft and any contributors reserve all other rights, whether under their respective copyrights, patents, or trademarks, whether by implication, estoppel or otherwise.
