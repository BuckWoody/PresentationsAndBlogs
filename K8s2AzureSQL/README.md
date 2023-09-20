
<img style="float: right;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/solutions-microsoft-logo-small.png">

# Creating a Kubernetes Application for Azure SQL DB

#### Buck Woody, Principal Applied Data Scientist, Microsoft 

Modern application development has several challenges. From selecting a "stack" of front-end through data storage and processing from several competing standards, through ensuring the highest levels of security and performance, developers are required to ensure the application scales and performs well and is supportable on multiple platforms. For that last requirement, bundling up the application into Container technologies such as Docker and deploying multiple Containers onto the Kubernetes platform is now de rigueur in application development.  

In this example, we'll explore using Python, Docker Containers, and Kubernetes - all running on the Microsoft Azure platform. Using Kubernetes means that you also have the flexibility of using local enviroments or even other clouds for a seamless and consistent deployment of your application, and allows for multi-cloud deployments for even higher resiliency. We'll also use Microsoft Azure SQL Database for a service-based, scalable, highly resilient and secure environment for the data storage and processing. In fact, in many cases, other applications are often using Microsoft Azure SQL Database already, and this sample application can be used to further leverage and enrich that data.  

This example is fairly comprehensive in scope, but uses the simplest application, database and deployment to illustrate the process. You can adapt this sample to be far more robust, even including leveraging the latest technologies for the returned data. It's a useful learning tool to create a pattern for other applications.

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

> Throughout this article, there are several values you should replace, as listed below. Ensure that you consistently replace these values for each step. You might want to open a text editor and drop these values in to set the correct values as you work though the Proof-of-Concept project:

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

> **Important Security Considerations:** For clarity and simplicity, this application is using a configuration file that is read from Python. Since the code will deploy with the container, the connection information may be able to derive from the contents. You should carefully consider the various methods of working with security, connections, and secrets and determine the best level and mechanism you should use for your application. You have multiple options of working with secret information such as connection strings and the like, and the list below shows a few of those options. Always pick the highest level of security, and even multiple levels to ensure your application is secure.

- [You can learn more about Azure SQL DB security here.](https://learn.microsoft.com/en-us/azure/security/fundamentals/database-security-checklist) 
- [Another method to work with secrets in Python is to use the python-secrets library. More here.](https://pypi.org/project/python-secrets/)Python secrets
- [Docker security and secrets are discussed here.](https://docs.docker.com/engine/swarm/secrets/)
- [Kubernetes secrets are discussed here.](https://kubernetes.io/docs/concepts/configuration/secret/)
- [You can also learn more about Microsoft Entra, formerly Azure Active Directory authentication here.](https://learn.microsoft.com/en-us/azure/active-directory-b2c/configure-authentication-sample-python-web-app)

The team next wrote the PoC application and called it *app.py*. You can see the self-documented code here:

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

<img src="https://github.com/BuckWoody/PresentationsAndBlogs/blob/master/K8s2AzureSQL/graphics/FlaskReturn01.png?raw=true" alt="drawing" width="800"/>

## Deploy the Application to a Docker Container
A Container is a reserved, protected space in a computing system that provides isolation and encapsulation. To create one, you use a Manifest file, which is simply a text file describing the binaries and code you wish to contain. Using a Container Runtime (such as Docker), you can then create a binary Image that has all of the files you want to run and reference. From there, you can "run" the binary image, and that is called a Container, which you can reference as if it were a full computing system. It's a smaller, simpler way to abstract your application runtimes and environment than using a full Virtual Machine. [You can learn more about Containers and Docker here.](https://learn.microsoft.com/en-us/dotnet/architecture/microservices/container-docker-introduction/docker-defined)

The team started with a DockerFile (the Manifest) that layers the elements of what the team wants to use. They start with a base Python image that already has the pyodbc
libraries installed, and then they run all commands necessary to contain the program and config file in the previous step. 

You can see the self-annotated Dockerfile here:

```
# syntax=docker/dockerfile:1

# Start with a Container binary that already has Python and pyodbc installed
FROM laudio/pyodbc

# Create a Working directory for the application
WORKDIR /flask2sql

# Install the other two libraries that are required - this could also be done in a "requirements file"
RUN pip install Flask
RUN pip install configparser

# Copy all of the code from the current directory into the WORKDIR
COPY . .

# Once the container starts, run the application, and open all TCP/IP ports 
CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0"]
```

With that file in place, the team dropped to a command-prompt in the coding directory and ran the following code to create the binary Image from the Manifest, and then another command to start the Container: 

```
docker build -t flask2sql .
docker run -d -p 5000:5000 -t flask2sql
```

Once again, the team tests the http://localhost:5000 link to ensure the Container can access the database, and they see the following return:

<img src="https://github.com/BuckWoody/PresentationsAndBlogs/blob/master/K8s2AzureSQL/graphics/FlaskReturn01.png?raw=true" alt="drawing" width="800"/>

## Deploy the Image to a Docker Registry
The Container is now working, but is only available on the developer's machine. The Development team would like to make this application Image available to the rest of the company, and then on to Kubernetes for production deployment. 

The storage area for Container Images is called a *repository*, and there can be both public and private repositories for Container Images. In fact, AdvenureWorks used a public Image for the Python environment in their Dockerfile. 

The team would like to control access to the Image, and rather than putting it on the web they decide they would like to host it themselves, but in Microsoft Azure where they have full control over security and access. [You can read more about Microsoft Azure Container Registry here.](https://learn.microsoft.com/en-us/azure/aks/tutorial-kubernetes-prepare-acr?tabs=azure-cli
)

Returning to the command-line, the Development team uses the *az CLI* utility to add a Container registry service, enable an administration account, set it to anonymous "pulls" during the testing phase, and set a log in context to the registry:

```
az acr create --resource-group ReplaceWith_PoCResourceGroupName --name ReplaceWith_AzureContainerRegistryName --sku Standard
az acr update -n ReplaceWith_AzureContainerRegistryName --admin-enabled true
az acr update --name ReplaceWith_AzureContainerRegistryName --anonymous-pull-enabled
az acr login --name ReplaceWith_AzureContainerRegistryName
```

This context will be used in subsequent steps. 

## Tag the local Docker Image to prepare it for uploading
The next step is to send the local application Container Image to the Azure Container Registry (ACR) service so that it is available in the cloud. Returning to the command-line, the team uses the Docker commands to list the Images on the machine, then the *az CLI* utility to list the Images in the ACR service. They then use the Docker command to "tag" the Image with the destination name of the ACR they created in the previous step, and to set a version number for proper DevOps. They then list the local Image information again to ensure the tag applied correctly:   

```
docker images
az acr list --resource-group ReplaceWith_PoCResourceGroupName --query "[].{acrLoginServer:loginServer}" --output table
docker tag flask2sql ReplaceWith_AzureContainerRegistryName.azurecr.io/azure-flask2sql:v1
docker images
```

With the code written and tested, the Dockerfile, Image and Container run and tested, the ACR service set up, and all tags applied, the team can upload the Image to the ACR service. They use the Docker "push" command to send the file, and then the *az CLI* utility to ensure the Image was loaded: 

```
docker push ReplaceWith_AzureContainerRegistryName.azurecr.io/azure-flask2sql:v1
az acr repository list --name ReplaceWith_AzureContainerRegistryName --output table
```
 
## Deploy to Kubernetes 
The team could simply run Containers and deploy the application to on-premises and in-cloud environments. However, they would like to add multiple copies of the application for scale and availability, add other Containers performing different tasks, and add monitoring and instrumentation to the entire solution. 

To group Containers togehter into a complete solution, the team decided to use Kubernetes. Kubernetes runs on-premises, and in all major cloud platforms. Microsoft Azure has a complete managed enviroment for Kubernetes, called the Azure Kubernetes Service (AKS). [You can learn more about AKS here.](https://learn.microsoft.com/en-us/training/paths/intro-to-kubernetes-on-azure/)

Using the *az CLI* utility, the team adds AKS to the Resource Group they created earlier. They add two "nodes" or computing enviroments for resiliency in the testing phase, they automatically generate SSH Keys for access to the environment, and then they attach the ACR service they created in the prevous steps so that the AKS "cluster" can locate the images they want to use for the deployment: 

```
az aks create --resource-group ReplaceWith_PoCResourceGroupName --name ReplaceWith_AzureKubernetesServiceName --node-count 2 --generate-ssh-keys --attach-acr ReplaceWith_AzureContainerRegistryName
```

Kubernetes uses a command-line tool to access and control a cluster, called *kubectl*. The team uses the *az CLI* utility to download the *kubectl* tool and install it:

```
az aks install-cli
```
Since they have a connection to AKS at the moment, they can ask it to send the SSH keys for connection to be used when they execute the *kubectl* utility:

```
az aks get-credentials --resource-group ReplaceWith_PoCResourceGroupName --name ReplaceWith_AzureKubernetesServiceName
```

These keys are stored [in a file called *.config* in the user's directory](https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/). With that security context set, the team uses the "get nodes" command using the *kubectl* utility to show the nodes in the cluster:

```
kubectl get nodes
```

Now the team uses the *az CLI* tool to list the Images in the ACR service:

```
az acr list --resource-group ReplaceWith_PoCResourceGroupName --query "[].{acrLoginServer:loginServer}" --output table
```
 
Now they can build the Mainfest that Kubernetes uses to control the deployment. This is a text file stored in a *yaml* format. Here is the annotated text in the *flask2sql.yaml* file:

```
apiVersion: apps/v1
# The type of commands that will be sent, along with the name of the deployment
kind: Deployment
metadata:
  name: flask2sql
# This section sets the general specifications for the application
spec:
  replicas: 1
  selector:
    matchLabels:
      app: flask2sql
  strategy:
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 1
  minReadySeconds: 5 
  template:
    metadata:
      labels:
        app: flask2sql
    spec:
      nodeSelector:
        "kubernetes.io/os": linux
# This section sets the location of the Image(s) in the deployment, and where to find them 
      containers:
      - name: flask2sql
        image:  bwoodyflask2sqlacr.azurecr.io/azure-flask2sql:v1
# Recall that the Flask application uses (by default) TCIP/IP port 5000 for access. This line tells Kubernetes that this "pod" uses that address.
        ports:
        - containerPort: 5000
---
apiVersion: v1
# This is the front-end of the application access, called a "Load Balancer"
kind: Service
metadata:
  name: flask2sql
spec:
  type: LoadBalancer
# this final step then sets the outside exposed port of the service to TCP/IP port 80, but maps it internally to the app's port of 5000
  ports:
  - protocol: TCP
    port: 80
    targetPort: 5000
  selector:
    app: flask2sql
```

With that file defined, the team can deploy the application to the running AKS cluster. That's done with the *apply* command in the *kubectl* utility, which as you recall still has a security context to the cluster. Then the *get service* command is sent to watch the cluster as it is being built. 

```
kubectl apply -f flask2sql.yaml
kubectl get service flask2sql --watch
```

After a few moments, the "watch" command will return an external IP address. At that point the team presses CTRL-C to break the watch command, and records the external IP address of the load balancer.


## Test the Application

Using the IP Address (Endpoint) they obtained in the last step, the team checks to ensure the same output as the local application and the Docker Container:

<img src="https://github.com/BuckWoody/PresentationsAndBlogs/blob/master/K8s2AzureSQL/graphics/FlaskReturn01.png?raw=true" alt="drawing" width="800"/>

## Coding Assets

[You can find all of the code assets for this sample at this location.](https://github.com/BuckWoody/PresentationsAndBlogs/tree/master/K8s2AzureSQL/code). Here's what they do:

- **app.py** - The Python application that performs a simple SELECT from an Azure SQL Database 
- **config.ini** - A text file with connection information to the Azure SQL Database
- **Dockerfile** - The manifest for the Docker Image creation
- **flask2sql.yaml** - The manifest for the Kubernetes deplpyment

In addition, the *az CLI* utility commands may make additional files such as the key for the application and other information in your application directory.

## Clean Up
With the application created, edtied, documented and tested, the team can now "tear down" the application. By keeping everything in a single resource group in Microsoft Azure, it's a simple matter of deleting the resource group using the *az CLI* utility: 

```
az group delete -n ReplaceWith_PoCResourceGroupName -y
```

> Note: If you created your Azure SQL Database in another rewource group and you no longer need it, you can use the Microsoft Azure Portal to delete that resource.

The team member leading the PoC project uses Microsoft Windows as her workstation, and wants to retain the secrets file from Kubernets but wants to remove it from the system as the active location. She simply copies the file to a *config.old" text file and then deletes it:

```
copy c:\users\ReplaceWith_YourUserName\.kube\config c:\users\ReplaceWith_YourUserName\.kube\config.old
del c:\users\ReplaceWith_YourUserName\.kube\config
```

# Learn More
- What is SQL Server Machine Learning Services with Python and R? https://learn.microsoft.com/en-us/sql/machine-learning/sql-server-machine-learning-services?view=sql-server-ver16 
