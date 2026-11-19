![](https://github.com/BuckWoody/PresentationsAndBlogs/blob/master/graphics/logo.png?raw=true)

# Workshop: PostgreSQL for the SQL Server Database Professional

#### <i>A SQL Server to PostgreSQL Skilling</i>

<p style="border-bottom: 1px solid lightgrey;"></p>

<img style="float: left; margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/textbubble.png"> <h2>00 – Pre-Requisites - Linux</h2>

Use this guide to prepare a Linux workstation. Install the course tools before attending; the workshop switches between graphical clients and command-line tools.

## PostgreSQL 17

Install PostgreSQL 17 using the instructions for your Linux distribution:

- [PostgreSQL downloads for Linux](https://www.postgresql.org/download/linux/)

Follow the distribution's instructions to start the PostgreSQL service and make `psql` available in your shell. PostgreSQL package names, service commands, and installation paths vary by distribution.

## SQL Server reference database

SQL Server 2022 on Linux is supported only on the distributions listed in Microsoft's installation guidance. Follow the [SQL Server on Linux installation instructions](https://learn.microsoft.com/en-us/sql/linux/install-upgrade/setup?view=sql-server-ver16).

If your distribution is not supported, use the [container setup](00-pre-requisites-container.md) or an existing SQL Server instance. SSMS is a Windows application; use DBeaver for a graphical client on Linux.

## Graphical client

Install [DBeaver Community](https://dbeaver.io/download/) for the side-by-side SQL Server and PostgreSQL exercises.

## Create the sample databases

Use the course scripts to create the reference and PostgreSQL sample databases:

- [SQL Server pubs script](pubs-tsql.md)
- [PostgreSQL pubs script](pubs-pgsql.md)

Follow the connection and database-creation steps in the [main prerequisites](00-pre-requisites.md), adapting the client commands and paths to your distribution.

<p style="border-bottom: 1px solid lightgrey;"></p>

Next, continue to <a href="01-introduction-and-overview.md" target="_blank"><i>Module 01 – Introduction and Overview</i></a>.
