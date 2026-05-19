![](graphics/microsoftlogo.png)

# Workshop: PostgreSQL for the SQL Server Database Professional

#### <i>A SQL Server to PostgreSQL Skilling</i>

<p style="border-bottom: 1px solid lightgrey;"></p>

<img style="float: left; margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/textbubble.png"> <h2>00 – Pre-Requisites</h2>

The **PostgreSQL for the SQL Server Database Professional** workshop is taught using the components listed below. You should install and configure each section *before* attending the workshop — there will not be time to complete setup during class.

*All examples in this workshop use Microsoft Windows as the base operating system. PostgreSQL runs natively on Windows, Linux, and macOS; the hands-on exercises will work on any platform, but screenshots and path examples reference Windows.*

(**Note:** You will find a series of winget commands below if you want a command-line scripted installation)

<p style="border-bottom: 1px solid lightgrey;"></p>

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/point1.png"><b>Activity 1: Install SQL Server 2022 Developer Edition (Windows)</b></p>

SQL Server 2022 Developer Edition is free for development and testing. You will use it as the reference platform for side-by-side comparisons throughout the workshop.

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/checkbox.png"><b>Step 1 – Download and Install SQL Server 2022 Developer Edition</b></p>

Follow the official Microsoft instructions to download and install SQL Server 2022 Developer Edition on Windows:

- [Download SQL Server 2022 Developer Edition](https://www.microsoft.com/en-us/sql-server/sql-server-downloads)
- [SQL Server Installation Guide (Windows)](https://learn.microsoft.com/en-us/sql/database-engine/install-windows/install-sql-server?view=sql-server-ver16)

During installation, select the **Database Engine Services** feature at minimum. Accept the default instance name (`MSSQLSERVER`) or note the instance name you choose — you will reference it throughout the workshop.

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/checkbox.png"><b>Step 2 – Install SQL Server Management Studio (SSMS)</b></p>

Install the latest version of SSMS for use as a reference tool throughout the workshop:

- [Download SSMS](https://learn.microsoft.com/en-us/sql/ssms/download-sql-server-management-studio-ssms)

<p style="border-bottom: 1px solid lightgrey;"></p>
<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/point1.png"><b>Activity 2: Install PostgreSQL on Windows</b></p>

The recommended installer for Windows is the EnterpriseDB (EDB) interactive installer, which includes PostgreSQL, pgAdmin 4, the Stack Builder utility, and command-line tools.

- [Download PostgreSQL for Windows (EDB Installer)](https://www.postgresql.org/download/windows/)
- [Official PostgreSQL Windows Installation Guide](https://www.postgresql.org/docs/current/install-windows.html)

During installation:

- Set the **data directory** to a dedicated drive/folder (e.g., `C:\PostgreSQL\17\data`).
- Set a strong password for the `postgres` superuser — **remember this password**, you will need it throughout the workshop.
- Accept the default port **5432**.
- Accept the default locale.

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/point1.png"><b>Activity 3: Install DBeaver Community Edition</b></p>

DBeaver Community is a free, cross-database IDE that supports both SQL Server and PostgreSQL. During the workshop you will use it to compare the two platforms side by side.

- [Download DBeaver Community for Windows](https://dbeaver.io/download/)

<p style="border-bottom: 1px solid lightgrey;"></p>

**WINGET Alternative Installation:**
You can also use the Windows Package Manager called "winget" to install software. The commands for all of the previous packages are:
```
winget install Microsoft.SQLServer.2022.Developer
winget install --id=Microsoft.SQLServerManagementStudio -e
winget install --id=PostgreSQL.PostgreSQL.17 -e
winget install --id=DBeaver.DBeaver.Community -e
```
<p style="border-bottom: 1px solid lightgrey;"></p>


<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/point1.png"><b>Activity 4 – Verify the Installation with psql</b></p>

*Note: Unlike SQL Server, a PostgreSQL installation is called a **cluster** and runs as a single Windows Service (`postgresql-x64-17` or similar). A single cluster can host many databases.*

Open a PowerShell window. Add the PostgreSQL `bin` directory to your PATH (e.g., `C:\Program Files\PostgreSQL\17\bin`)

```powershell
# Run in an elevated PowerShell session
$pgBin = "C:\Program Files\PostgreSQL\17\bin"
[Environment]::SetEnvironmentVariable(
    "Path",
    [Environment]::GetEnvironmentVariable("Path","Machine") + ";$pgBin",
    "Machine"
)
```
Exit your terminal and start it back again. Then connect:

```bat
psql --version
pg_dump --version
psql -U postgres -h localhost
```

You will be prompted for the password you set during installation (postgres if you did the winget install). If you see the `postgres=#` prompt, PostgreSQL is running correctly. Type `\q` to exit.

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/point1.png"><b>Activity 5 – Verify pgAdmin 4 Launches</b></p>

pgAdmin 4 is included with the EDB installer. Launch it from the Start menu. Connect to the local PostgreSQL server using the `postgres` superuser credentials. You should see the server tree on the left with your new cluster.

<p style="border-bottom: 1px solid lightgrey;"></p>


<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/point1.png"><b>Activity 6 – Restore the AdventureWorks2022 Sample Database</b></p>

The workshop exercises use the pubs sample database as the SQL Server reference database.

- Navigate to this resource and copy the script into memory.
- Open SQL Server Management Studio and connect to the "master" database.
- Right-click the *master* database and select *New Query*
- Press CTRL-V to paste the pubs database script.
- Run the query using the F5 key.

<p style="border-bottom: 1px solid lightgrey;"></p>

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/point1.png"><b>Activity 7: Create the Workshop Sample Database in PostgreSQL</b></p>

The workshop uses the pubs database ported to PostgreSQL. Run the following commands in psql to create the workshop database and sample schema:

Open DBeaver, create two database connections — one for SQL Server and one for PostgreSQL. DBeaver will prompt you to download the required JDBC drivers automatically on first connection.

- *SQL Server connection string example:* `jdbc:sqlserver://localhost:1433;databaseName=pubs`
- *PostgreSQL connection string example:* `jdbc:postgresql://localhost:5432/postgres`

- Navigate to this resource and copy the script into memory.
- In DBeaver, right-click the Server name and select *Create Database*
- Type the name *pubs* and create the database
- Left-click the *Databases* node and select *Refresh*. You should see the *pubs* database listed. 
- Left-click the *pubs* database and press *CTRL-ALT-ENTER* to enter a new query file.
- Press CTRL-V to paste the pubs database script from above.
- Run the query using the third small red arrow at the left side the query window - hover over it so that it says "Run Script" before you click it.

<p style="border-bottom: 1px solid lightgrey;"></p>

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/point1.png"><b>(Optional) Set Up Azure Database for PostgreSQL Flexible Server</b></p>

Module 06 demonstrates cloud-managed PostgreSQL. If you want to follow along with the Azure sections, create a Flexible Server instance before the workshop.

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/checkbox.png"><b>Step 1 – Create an Azure Account</b></p>

You need a Microsoft Azure account. Use one of the following options:

- **Free Account (12 months + $200 credit):** [https://azure.microsoft.com/en-us/free/](https://azure.microsoft.com/en-us/free/)
- **MSDN/Visual Studio Subscriber Credit:** [https://azure.microsoft.com/en-us/pricing/member-offers/credit-for-visual-studio-subscribers/](https://azure.microsoft.com/en-us/pricing/member-offers/credit-for-visual-studio-subscribers/)
- **Pay-as-you-go:** [https://azure.microsoft.com/en-us/pricing/purchase-options/pay-as-you-go/](https://azure.microsoft.com/en-us/pricing/purchase-options/pay-as-you-go/)

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/checkbox.png"><b>Step 2 – Create Azure Database for PostgreSQL – Flexible Server</b></p>

Follow the quickstart to create a Flexible Server instance in the Azure Portal:

- [Quickstart: Create Azure Database for PostgreSQL – Flexible Server](https://learn.microsoft.com/en-us/azure/postgresql/flexible-server/quickstart-create-server-portal)

Choose the **Burstable B1ms** tier for workshop purposes to minimize cost. **Turn off the server when not in use** from the Azure Portal to avoid charges.

<p style="border-bottom: 1px solid lightgrey;"></p>


<p style="border-bottom: 1px solid lightgrey;"></p>

<p><img style="margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/owl.png"><b>For Further Study</b></p>

- [PostgreSQL Downloads Page](https://www.postgresql.org/download/)
- [EDB Interactive Installer for Windows](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads)
- [pgAdmin 4 Documentation](https://www.pgadmin.org/docs/)
- [psql Command Reference](https://www.postgresql.org/docs/current/app-psql.html)
- [Azure Database for PostgreSQL – Flexible Server Documentation](https://learn.microsoft.com/en-us/azure/postgresql/flexible-server/)
- [SQL Server 2022 Installation Guide](https://learn.microsoft.com/en-us/sql/database-engine/install-windows/install-sql-server)

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/geopin.png"><b>Next Steps</b></p>

Next, continue to <a href="01_-_Introduction_and_Overview.md" target="_blank"><i>Module 01 – Introduction and Overview</i></a>.
