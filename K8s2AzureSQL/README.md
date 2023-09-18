
<img style="float: right;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/solutions-microsoft-logo-small.png">

# Creating a Kubernetes Application for Azure SQL DB

#### Buck Woody, Principal Applied Data Scientist, Microsoft 

Intro and Overview 

## Using the AdventureWorks Sample Database in a Practical Example
Edit the following:
The AdventureWorks (fictitious) company uses a database that store data about Sales and Marketing, Products, Customers and Manufacturing. It also contains a view that joins information about the 
products, such as the product name, category, price, and a brief description. 

Currently, AdventureWorks sends the product name and brief description to a marketing firm to develop a campaign to boost sales. The cost for this marketing specialist is significant, and after looking into the capabilities of Generative Pre-trained Transformers (GPT), the company is curious to know if this Artificial Intelligence (AI) could be used to create starter-text for brochures, automating the first step of the process. GPT-4 is a powerful language model that can generate coherent and creative text from complex input, or prompts. Instead of hiring a professional writer, they can use SQL Server Machine Learning Services with Microsoft Azure OpenAI to automatically generate high-quality starter ad copy based on the product description and other relevant data. This can save time and money on the marketing budget. This approach also has the added benefit of security, since the database stays local, Stored Procedures have high security granularity, and Azure OpenAI does not use the information sent for further training. 

This process works on SQL Server Machine Learning Services platforms on Windows, Linux, Containers, and Kubernetes clusters, including Virtual Machines and SQL Server Managed Instance, from version 2019.

During their research, AdventureWorks discovered that it is important to be cautious when generating text using a GPT model. It is possible that the generated text may not always be appropriate or accurate, so it is important to have a system in place for reviewing and approving any changes before they are published.

The Proof-of-Concept (PoC) for AdventureWorks involves the following requirements: 
1.	Create a Stored Procedure to accept the model of a given product.
2.	Generate marketing brochure text for that product, highlighting its features and benefits, using OpenAI's GPT-4 model. 
3.	Ensure that the generated text is safe and factual, and that it can be edited before publishing.

## Pre-Requisites
Python
az commands
SQL DB with AdventureWorksLT sample installed
 
az login
az account set --name ""Visual Studio Enterprise Subscription""
az sql server list
az sql db list bwoody-db 
 
## Create the Application
 
NOTE: https://medium.com/google-cloud/a-guide-to-deploy-flask-app-on-google-kubernetes-engine-bfbbee5c6fb#:~:text=Deploy%20to%20Flask%20app%20to%20the%20kubernetes%20cluster,deployment%20flask-app-tutorial%20%20--type%3DLoadBalancer%20--port%2080%20--target-port%208080 
 

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
