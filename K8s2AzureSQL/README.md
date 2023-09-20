
<img style="float: right;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/solutions-microsoft-logo-small.png">

# Creating a Kubernetes Application for Azure SQL DB

#### Buck Woody, Principal Applied Data Scientist, Microsoft 

Modern application development has several challenges. From selecting a "stack" of front-end through data storage and processing from several competing standards, through ensuring the highest levels of security and performance, developers are required to ensure the application scales and performs well and is supportable on multiple platforms. For that last requirement, bundling up the application into Container technologies such as Docker and deploying multiple Containers onto the Kubernetes platform is now de rigueur in application development.  

In this example, we'll explore using Python, Docker Containers, and Kubernetes - all running on the Microsoft Azure platform. Using Kubernetes means that you also have the flexibility of using local enviroments or even other clouds for a seamless and consistent deployment of your application, and allows for multi-cloud deployments for even higher resiliency. We'll also use Microsoft Azure SQL DB for a service-based, scalable, highly resilient and secure environment for the data storage and processing. In fact, in many cases, other applications are often using Microsoft Azure SQL DB already, and this sample application can be used to curther leverage and enrich that data.  

This example is fairly comprehensive in scope, but uses the simplest applications, databases and deployments to illustrate the process. You can adapt this sample to be far more robust, even including leveraging the latest technologies for the returned data. 

## Using the AdventureWorksLT Sample Database in a Practical Example

The AdventureWorks (fictitious) company uses a database that stores data about Sales and Marketing, Products, Customers and Manufacturing. It also contains views and stored procedures that join information about the products, such as the product name, category, price, and a brief description. 

The AdventureWorks Development team wants to create a Proof-of-Concept (PoC) that returns data from a View in the AdventureWorksLT database, and show the result in a web interface. Using this PoC, the Development team will create a more scalable snd multi-cloud ready application for the Sales team. They have selected the Microsoft Azure platform for all aspects of deployment. The PoC is using the following elements:

- A Python application using the Flask package for headless web deployment.
- Docker Containers for code and environment isolation, stored in a private registry so that the entire company can re-use the application Containers in future projects, saving time and money. 
- Kubernetes for ease of deployment and scale, and to avoid platform lock-in.
- Microsoft Azure SQL DB for selection of size, performance, scale, auto-management and backup, in addition to Relational data storage and processing at the highest security level.  

In this article we'll explain the process for creating the entire Proof-of-Concept project. The general steps for creating the application are:

1. Set up pre-requisites
2. Write the application
3. Create a Docker Container to deploy the application and test
4. Create an Azure Container Service (ACS) Registry and load the Container to the ACS Registry
5. Create the Azure Kubernetes Service (AKS) environment
6. Deploy the application Container from the ACS Registry to AKS and test the application
7. Clean up

> Throughout this article, there are several values you should replace, as listed below. Ensure that you consistently replace these values for each step.

- *ReplaceWith_AzureSubscriptionName*: Replace this value with the name of the Azure subscription name you have. 
- *ReplaceWith_PoCResourceGroupName*: Replace this value with the name of the resource group you would like to create. 
- *ReplaceWith_AzureSQLDBServerName*: Replace this value with the name of the Azure SQL Database Server you create using the Azure Portal.
- *ReplaceWith_AzureSQLDBSQLServerLoginName*: Replace this value with the vaue of the SQL Server User Name you create in the Azure Portal.
- *ReplaceWith_AzureSQLDBSQLServerLoginPassword*: Replace this value with the vaue of the SQL Server User Password you create in the Azure Portal.
- *ReplaceWith_AzureSQLDBDatabaseName*: Replace this value with the name of the Azure SQL Database you create using the Azure Portal.
- *ReplaceWith_AzureContainerRegistryName*: Replace this value with the name of the Azure Container Registry you would like to create.
- *ReplaceWith_AzureKubernetesServiceName*: Replace this value with the name of the Azure Kubernetes Service you would like to create.

## Pre-Requisites
The developers at AdventureWorks use a mix of Windows, Linux, and Apple systems for development, so they are using Visual Studio Code as their environment and git for the source control, both of which which run cross-platform. 

For the PoC, The team requires the following pre-requisites:

- **Python, pip, and packages** - The development team has chosen the [Python programming language](https://learn.microsoft.com/en-us/training/paths/beginner-python/) as the standard for this web-based application. Currently they are using version 3.12, but any version supporting the PoC required packages is acceptable. [You can download the Python language version 3.9 here.](https://www.python.org/downloads/release/python-390/)
- The team is using the *pyodbc package* for database access. [You can find the pyodbc package here with the *pip* commands to install it.](https://pypi.org/project/pyodbc/). You may also need the [Microsoft ODBC Driver software](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver16) if you do not have it installed.
- The team is using the *ConfigParser package* for controlling and setting configuration variables. [You can find the configparser package here with the *pip* commands to install it.](https://pypi.org/project/configparser/)
- The team is using the *Flask package* for a web interface for the application. [You can find the Flask library here.](https://flask.palletsprojects.com/en/2.3.x/installation/)

**The Microsoft Azure az CLI tool**
Next, the team installed the Azure *AZ CLI* tool. This cross-platform tool allows a command-line and scripted approach to the PoC, so that they can repeat the steps as they make changes and improvements. [You can find the installation for the AZ CLI tool here.](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli)

With that tool set up, the team used it to log in to their Azure subscription, and set the subscription name they used for the PoC. They then ensured the Azure SQL DB server and database is accessible to the subscription:


```
az login
az account set --name "ReplaceWith_AzureSubscriptionName"
az sql server list
az sql db list ReplaceWith_AzureSQLDBDatabaseName 
``` 

**Create a Microsoft Azure Resource Group (RG) to hold the entire PoC**
A [Microsoft Azure Resource Group](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/manage-resource-groups-portal#what-is-a-resource-group) is a logical container that holds related resources for an Azure solution. Generally, resources that share the same lifecycle are added to the same resource group so you can easily deploy, update, and delete them as a group. The resource group stores metadata about the resources, and you can specify a location for the resource group.

Resource groups can be created and managed using the Azure portal or the AZ CLI. They can also be used to group related resources for an application and divide them into groups for production and nonproduction, or any other organizational structure you prefer.

<img src="https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/media/manage-resource-groups-portal/manage-resource-groups-list-groups.png" alt="drawing" width="600"/>

In the snippet below, you can see the AZ command used to create a resource group in the *eastus* region of Azure:

```
az group create --name ReplaceWith_PoCResourceGroupName --location eastus
```

**Microsoft Azure SQL DB with the AdventureWorksLT sample database installed, using SQL Server Logins**
AdventureWorks has standardized on the [Microsoft SQL Server Relational Database Management System platform](https://www.microsoft.com/en-us/sql-server/), and the Development team wants to use a managed service for the database rather than installing locally. Using Azure SQL DB allows this managed service to be completely code-compatible wherever they run the SQL Server engine - on-premises, in a Container, in Linux or Windows, or even in an Internet of Things (IoT) environment. 

The team used the sample *AdventureWorksLT* database for the PoC using the same PoC Resource Group, [which you can learn to deploy here.](https://learn.microsoft.com/en-us/azure/azure-sql/database/single-database-create-quickstart?view=azuresql&tabs=azure-portal) They set a SQL Server account for login for testing, but will revisit this decision in a security review. 

<img src="https://learn.microsoft.com/en-us/azure/azure-sql/database/media/single-database-create-quickstart/additional-settings.png?view=azuresql" alt="drawing" width="600"/>

During creation, they used the [Azure Management Portal to set the Firewall for the application](https://learn.microsoft.com/en-us/azure/azure-sql/database/firewall-create-server-level-portal-quickstart?view=azuresql) to the local development machine, and changed the default you see here to **allow all Azure Services**, and also [retreived the connection credentials.](https://learn.microsoft.com/en-us/azure/azure-sql/database/azure-sql-python-quickstart?view=azuresql&tabs=windows%2Csql-auth#configure-the-local-connection-string) Note that with this approach, the database could be in another region or even a different subscription.

<img src="https://learn.microsoft.com/en-us/azure/azure-sql/database/media/single-database-create-quickstart/networking.png?view=azuresql" alt="drawing" width="600"/>
 
## Create the Application

Next, the Development team created a simple Python application that opens a connection to Azure SQL DB, and returns a list of products. This code will be replaced with much more complex functions, and may also include more than one application deployed into the Kubernetes Pods in production for a robust, manifest-driven approach to application solutions. 

The Team created a simple text file called *config.ini* to hold variables for the server connections and other information. Using the ConfigParser library they can then separate out the variables from the Python Code into a block they set to *[Connection]*:

```
[Connection]
SQL_SERVER_USERNAME = ReplaceWith_AzureSQLDBSQLServerLoginName
SQL_SERVER_ENDPOINT = ReplaceWith_AzureSQLDBServerName
SQL_SERVER_PASSWORD = ReplaceWith_AzureSQLDBSQLServerLoginPassword
SQL_SERVER_DATABASE = ReplaceWith_AzureSQLDBDatabaseName
```

> **Important Security Considerations:** For clarity and simplicity, this application is using a configuration file that is read from Python. Since the code will deploy with the container, the connection information may be able to derive from the contents. You should carefully consider the various methods of working with security, connections, and secrets and determine the best level and mechanism you should use for your application. 

- [You can learn more about Azure SQL DB security here.](https://learn.microsoft.com/en-us/azure/security/fundamentals/database-security-checklist) 
- Python secrets
- Docker security
- Kubernetes secrets
- Microsoft Entra - https://learn.microsoft.com/en-us/azure/active-directory-b2c/configure-authentication-sample-python-web-app 

The team next wrote the application and called it *app.py*. You can see the self-documented code here:

```
# Set up the libraries for the configuration and base web interfaces
import configparser
from flask import Flask
import pyodbc

# Open the configuration file
config = configparser.ConfigParser()
config.read('config.ini')

# Create the Flask Application
app = Flask(__name__)

# Create connection to Azure SQL DB using the config.ini file values
ServerName = config.get('Connection', 'SQL_SERVER_ENDPOINT')
DatabaseName = config.get('Connection', 'SQL_SERVER_DATABASE')
UserName = config.get('Connection', 'SQL_SERVER_USERNAME')
PasswordValue = config.get('Connection', 'SQL_SERVER_PASSWORD')

# Connect to Azure SQL DB using the pyodbc package
# Note: You may need to install the ODBC driver if it is not already there. You can find that at:
# https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver16#version-17
connection = pyodbc.connect(f'Driver=ODBC Driver 17 for SQL Server;Server={ServerName};Database={DatabaseName};uid={UserName};pwd={PasswordValue}')

# Create the query and set the cursor object to hold the results
cursor = connection.cursor()
cursor.execute("SELECT [ProductID], [Name], [Description] FROM [SalesLT].[vProductAndDescription] ORDER BY [Name];")

# Display the results
strContent= "<table style='border:1px solid red'>"
for row in cursor:
    strContent= strContent+ "<tr>"
    for dbItem in row:
        strContent= strContent+ "<td>" + str(dbItem) + "</td>"
    strContent= strContent+ "</tr>"
strContent= strContent+ "</table>"
connection.close()

# Set the Flask application to run on the standard ports - typically port 5000
@app.route('/')
@app.route('/home')
def home():
    return "<html><body>" + strContent + "</body></html>"

if __name__ == "__main__":
    app.run(debug=True)
```

They checked that this application runs locally, and returns a page to http://localhost:5000


## Deploy the Application to a Docker Container

```
docker build -t flask2sql .
docker run -d -p 5000:5000 -t flask2sql
http://localhost:5000
```
 
Create Container registry: 
https://learn.microsoft.com/en-us/azure/aks/tutorial-kubernetes-prepare-acr?tabs=azure-cli

```
az acr create --resource-group ReplaceWith_PoCResourceGroupName --name ReplaceWith_AzureContainerRegistryName --sku Standard
az acr update -n ReplaceWith_AzureContainerRegistryName --admin-enabled true
az acr update --name ReplaceWith_AzureContainerRegistryName --anonymous-pull-enabled
az acr login --name ReplaceWith_AzureContainerRegistryName
```

## Tag the local Docker Image to prepare it for uploading

```
docker images
az acr list --resource-group ReplaceWith_PoCResourceGroupName --query "[].{acrLoginServer:loginServer}" --output table
docker tag flask2sql ReplaceWith_AzureContainerRegistryName.azurecr.io/azure-flask2sql:v1
docker images
```

```
docker push ReplaceWith_AzureContainerRegistryName.azurecr.io/azure-flask2sql:v1
az acr repository list --name ReplaceWith_AzureContainerRegistryName --output table
```
 
## Deploy to Kubernetes: 
https://learn.microsoft.com/en-us/azure/aks/tutorial-kubernetes-deploy-cluster?tabs=azure-cli
 
```
az aks create --resource-group ReplaceWith_PoCResourceGroupName --name ReplaceWith_AzureKubernetesServiceName --node-count 2 --generate-ssh-keys --attach-acr ReplaceWith_AzureContainerRegistryName
```

```
az aks install-cli
```

```
az aks get-credentials --resource-group ReplaceWith_PoCResourceGroupName --name ReplaceWith_AzureKubernetesServiceName
```

```
kubectl get nodes
```

```
az acr list --resource-group ReplaceWith_PoCResourceGroupName --query "[].{acrLoginServer:loginServer}" --output table
```
 
```
kubectl apply -f flask2sql.yaml
kubectl get service flask2sql --watch
```
 
## Test the Application


## Coding Assets

[You can find all of the code assets for this sample at this location.](https://github.com/BuckWoody/PresentationsAndBlogs/tree/master/K8s2AzureSQL/code). Here's what they do:

- app.py
- buck3.yaml
- config.ini
- Dockerfile
- flask2sql.yaml
- requirements.txt

In addition, the az commands will make additional files such as the key for the application and other information.

## Clean Up

```
az group delete -n ReplaceWith_PoCResourceGroupName -y
copy c:\users\bwoody\.kube\config c:\users\bwoody\.kube\config.old
del c:\users\bwoody\.kube\config
```

# Learn More
- What is SQL Server Machine Learning Services with Python and R? https://learn.microsoft.com/en-us/sql/machine-learning/sql-server-machine-learning-services?view=sql-server-ver16 
