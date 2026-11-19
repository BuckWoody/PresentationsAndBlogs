![](https://github.com/BuckWoody/PresentationsAndBlogs/blob/master/graphics/logo.png?raw=true)

# Workshop: PostgreSQL for the SQL Server Database Professional

#### <i>A SQL Server to PostgreSQL Skilling</i>

<p style="border-bottom: 1px solid lightgrey;"></p>

<img style="float: left; margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/textbubble.png"> <h2>00 – Pre-Requisites - Containers</h2>

Use this guide to run the database engines in containers. Install and start a container runtime before attending; the workshop also uses a graphical database client.

## Container runtime

Install [Docker Desktop](https://docs.docker.com/get-started/get-docker/) or Docker Engine for your host operating system. Use Linux containers and confirm that the runtime is running.

## SQL Server 2022 and PostgreSQL 17

Create one container for each database engine, following the vendors' instructions:

- [Run SQL Server 2022 in a Linux container](https://learn.microsoft.com/en-us/sql/linux/quickstart-install-connect-docker?view=sql-server-ver16)
- [Run PostgreSQL using the official Docker image](https://hub.docker.com/_/postgres) (use the `postgres:17` image)

Publish the SQL Server and PostgreSQL ports (`1433` and `5432`) to the host so the client can connect. Set strong passwords as directed by the image documentation, preserve database files with container volumes, and do not expose these database ports to untrusted networks.

## Graphical client

Install [DBeaver Community](https://dbeaver.io/download/) on the host. Connect it to the containers using `localhost`, port `1433` for SQL Server and port `5432` for PostgreSQL, along with the credentials configured for each container.

## Create the sample databases

Use the course scripts to create the reference and PostgreSQL sample databases:

- [SQL Server pubs script](pubs-tsql.md)
- [PostgreSQL pubs script](pubs-pgsql.md)

Create the `pubs` database in PostgreSQL before running its script. Follow the database-creation steps in the [main prerequisites](00-pre-requisites.md), substituting the container connection details.

<p style="border-bottom: 1px solid lightgrey;"></p>

Next, continue to <a href="01-introduction-and-overview.md" target="_blank"><i>Module 01 – Introduction and Overview</i></a>.
