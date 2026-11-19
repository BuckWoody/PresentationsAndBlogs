![](https://github.com/BuckWoody/PresentationsAndBlogs/blob/master/graphics/logo.png?raw=true)

# Workshop: PostgreSQL for the SQL Server Database Professional

#### <i>A SQL Server to PostgreSQL Skilling</i>

<p style="border-bottom: 1px solid lightgrey;"></p>

<img style="float: left; margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/textbubble.png"> <h2>00 – Pre-Requisites - Cloud Platform</h2>

This guide covers the optional, managed PostgreSQL environment used for the cloud examples. You will need an Azure subscription and a local client to connect to the server.

## Azure Database for PostgreSQL – Flexible Server

Create a Flexible Server by following the [Azure portal quickstart](https://learn.microsoft.com/en-us/azure/postgresql/flexible-server/quickstart-create-server-portal). Choose PostgreSQL 17 and a compute tier appropriate for your workshop; review current pricing before provisioning.

Configure networking to allow connections only from your client or private network. Keep the server name, database, username, and password available for DBeaver. Install [DBeaver Community](https://dbeaver.io/download/) on your workstation and connect using the server's hostname and port `5432`.

Create the `pubs` database and run the [PostgreSQL pubs script](pubs-pgsql.md) in it. The script and database-creation steps are also described in the [main prerequisites](00-pre-requisites.md).

> Flexible Server is a managed PostgreSQL service, not SQL Server. For the SQL Server comparison exercises, use a separate SQL Server instance prepared with the [Linux](00-pre-requisites-linux.md) or [container](00-pre-requisites-container.md) guide, or another SQL Server instance you can access.

Review Azure's current pricing and stop or delete resources when they are no longer needed. Storage and other resources may continue to incur charges even when a server is stopped.

<p style="border-bottom: 1px solid lightgrey;"></p>

Next, continue to <a href="01-introduction-and-overview.md" target="_blank"><i>Module 01 – Introduction and Overview</i></a>.
