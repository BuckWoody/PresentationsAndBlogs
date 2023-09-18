
<img style="float: right;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/solutions-microsoft-logo-small.png">

# Creating a Kubernetes Application for Azure SQL DB

#### Buck Woody, Principal Applied Data Scientist, Microsoft 

Modern application development has several challenges. From selecting a "stack" of front-end through data storage and processing from several competing standards, through ensuring the highest levels of security and performance, developers are required to ensure the application scales and performs well and is supportable on multiple platforms. For that last requirement, bundling up the application into Container technologies such as Docker and deploying multiple Containers onto the Kubernetes platform is now de rigueur in application development.  

In this example, we'll explore using Python, Docker Containers, and Kubernetes - all running on the Microsoft Azure platform. Using Kubernetes means that you also have the flexibility of using local enviroments or even other clouds for a seamless and consistent deployment of your application, and allows for multi-cloud deployments for even higher resiliency. We'll also use Microsoft Azure SQL DB for a service-based, scalable, highly resilient and secure environment for the data storage and processing. In fact, in many cases, other applications are often using Microsoft Azure SQL DB already, and this sample application can be used to curther leverage and enrich that data.  

This example is fairly comprehensive in scope, but uses the simplest applications, databases and deployments to illustrate the process. You can adapt this sample to be far more robust, even including leveraging the latest technologies for the returned data. 

## Using the AdventureWorksLT Sample Database in a Practical Example

The AdventureWorks (fictitious) company uses a database that stores data about Sales and Marketing, Products, Customers and Manufacturing. It also contains views and stored procedures that join information about the products, such as the product name, category, price, and a brief description. 

The AdventureWorks Development team wants to create a Proof-of-Concept (PoC) that returns data from a View in the AdventureWorksLT database, and show the result in a web interface. Using this PoC, the Development team will create a more scalable snd multi-cloud ready application for the Sales team. They have selected the Microsoft Azure platform for all aspects of deployment. The PoC is using the following elements:

1.	A Python application using the Flask package for headless web deployment.
2.	Docker Containers for code and environment isolation, stored in a private registry so that the entire company can re-use the application Containers in future projects, saving time and money. 
3.	Kubernetes for ease of deployment and scale, and to avoid platform lock-in.

## Pre-Requisites

> [You can find all of the code assets for this sample at this location.]()


**Python, pip, and packages**

**Microsoft Azure SQL DB with AdventureWorksLT sample installed**
 
**The Microsoft Azure az CLI tool**

az login
az account set --name ""Visual Studio Enterprise Subscription""
az sql server list
az sql db list bwoody-db 
 
## Create the Application
 


> Important Security Considerations
For clarity and simplicity, this application is using a configuration file that is read from Python. Since the code will deploy with the container, the connection information may be able to derive from the contents. You should carefully consider the various methods of working with security, connections, and secrets and determine the best level and mechanism you should use for your application. [You can learn more about Azure SQL DB security here.](https://learn.microsoft.com/en-us/azure/security/fundamentals/database-security-checklist) 
- Python secrets
- Docker security
- Kubernetes secrets
- Microsoft Entra - https://learn.microsoft.com/en-us/azure/active-directory-b2c/configure-authentication-sample-python-web-app 

## Deploy the Application to a Docker Container
docker build -t flask2sql .
docker run -d -p 5000:5000 -t flask2sql
http://localhost:5000
 
## Create the Microsoft Assets for the Container Deployment

```
az group create --name bwoodyflask2sqlrg --location eastus
```
 
Create Container registry: 
https://learn.microsoft.com/en-us/azure/aks/tutorial-kubernetes-prepare-acr?tabs=azure-cli

```
az acr create --resource-group bwoodyflask2sqlrg --name bwoodyflask2sqlacr --sku Standard
az acr update -n bwoodyflask2sqlacr --admin-enabled true
az acr update --name bwoodyflask2sqlacr --anonymous-pull-enabled
az acr login --name bwoodyflask2sqlacr
```

docker images
az acr list --resource-group bwoodyflask2sqlrg --query "[].{acrLoginServer:loginServer}" --output table
docker tag flask2sql bwoodyflask2sqlacr.azurecr.io/azure-flask2sql:v1
docker images
 
docker push bwoodyflask2sqlacr.azurecr.io/azure-flask2sql:v1
az acr repository list --name bwoodyflask2sqlacr --output table
 
 
## Deploy to Kubernetes: 
https://learn.microsoft.com/en-us/azure/aks/tutorial-kubernetes-deploy-cluster?tabs=azure-cli
 
az aks create --resource-group bwoodyflask2sqlrg --name bwoodyflask2sqlaks --node-count 2 --generate-ssh-keys --attach-acr bwoodyflask2sqlacr
 
az aks install-cli
az aks get-credentials --resource-group bwoodyflask2sqlrg --name bwoodyflask2sqlaks
kubectl get nodes
 
az acr list --resource-group bwoodyflask2sqlrg --query "[].{acrLoginServer:loginServer}" --output table
 
kubectl apply -f flask2sql.yaml
kubectl get service flask2sql --watch
 
// Find a way to expose the port
 
 
## Clean Up
az group delete -n bwoodyflask2sqlrg -y
copy c:\users\bwoody\.kube\config c:\users\bwoody\.kube\config.old
del c:\users\bwoody\.kube\config
 
# Learn More
- What is SQL Server Machine Learning Services with Python and R? https://learn.microsoft.com/en-us/sql/machine-learning/sql-server-machine-learning-services?view=sql-server-ver16 
