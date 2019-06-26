USE sqltoazure;
GO

-- Create Main Entities
DROP TABLE IF EXISTS Problem;
GO
CREATE TABLE Problem (
ProblemID INT IDENTITY PRIMARY KEY
, ProblemName NVARCHAR(150)
, ProblemDescription NVARCHAR(MAX)
);
GO

DROP TABLE IF EXISTS Solution;
GO
CREATE TABLE Solution (
SolutionID INT IDENTITY PRIMARY KEY
, SolutionName NVARCHAR(150)
, SolutionDescription NVARCHAR(MAX)
);
GO

DROP TABLE IF EXISTS AzureService;
GO
CREATE TABLE AzureService (
AzureServiceID INT IDENTITY PRIMARY KEY
, ServiceName NVARCHAR(150)
, ServiceDescription NVARCHAR(MAX)
) 
GO

DROP TABLE IF EXISTS ItemReference;
GO
CREATE TABLE ItemReference (
ItemReferenceID INT IDENTITY PRIMARY KEY
, ItemReferenceName NVARCHAR(150)
, ItemReferenceType NVARCHAR(50)
, ItemReferenceLocation NVARCHAR(150)
, ItemReferenceDescription NVARCHAR(MAX)
);
GO

DROP TABLE IF EXISTS ItemProperty;
GO
CREATE TABLE ItemProperty (
ItemPropertyID INT IDENTITY PRIMARY KEY
, ItemPropertyType NVARCHAR(100)
, ItemPropertyName NVARCHAR(150)
, ItemPropertyDescription NVARCHAR(MAX)
);
GO

-- Create Joins
DROP TABLE IF EXISTS ProblemToSolution;
GO
CREATE TABLE ProblemToSolution (
ProblemToSolutionID INT IDENTITY PRIMARY KEY 
, FromItem INT
, ToItem INT
, Strength NVARCHAR(50)
);

DROP TABLE IF EXISTS SolutionToService;
GO
CREATE TABLE SolutionToService (
SolutionToServiceID INT IDENTITY PRIMARY KEY 
, FromItem INT
, ToItem INT
, Complexity NVARCHAR(50)
, MonthlyEstimatedCost NVARCHAR(50)
);

-- Fill tables
INSERT INTO Problem (ProblemName, ProblemDescription ) 
VALUES ('Copy Data Automatically', 'We want to copy certain data elements to an external location for use by others, securely.')
GO

INSERT INTO Solution (SolutionName, SolutionDescription ) 
VALUES ('SQL Replication to Azure VM', 'Use SQL Server Replication to copy data to an Azure Virtual Machine.')
GO 

INSERT INTO AzureService (ServiceName, ServiceDescription ) 
VALUES ('Virtual Machines', 'Windows or Linux Virtual Machine')
GO 

INSERT INTO ItemReference (ItemReferenceName, ItemReferenceType, ItemReferenceLocation, ItemReferenceDescription) 
VALUES ('Windows Virtual Machines Documentation', 'Official Documentation', 'https://docs.microsoft.com/en-us/azure/virtual-machines/windows/', 'Official Documentation for Windows Virtual Machines')
,('Linux Virtual Machines Documentation', 'Official Documentation', 'https://docs.microsoft.com/en-us/azure/virtual-machines/linux/', 'Official Documentation for Linux Virtual Machines');
GO 

INSERT INTO ItemReference (ItemReferenceName, ItemReferenceType, ItemReferenceLocation, ItemReferenceDescription) 
VALUES ('SQL Server Replication to Azure', 'Official Documentation', 'https://docs.microsoft.com/en-us/sql/relational-databases/replication/sql-server-replication?view=sql-server-2017', 'Official Documentation for SQL Server Replication');
GO

-- Joins
INSERT INTO ProblemToSolution (FromItem, ToItem, Strength) 
VALUES (
(SELECT ProblemID FROM Problem WHERE ProblemName = 'Copy Data Automatically')
, (SELECT SolutionID FROM [Solution] WHERE SolutionName = 'SQL Replication to Azure VM')
, 'High');
GO

INSERT INTO SolutionToService (FromItem, ToItem, Complexity, MonthlyEstimatedCost) 
VALUES (
(SELECT AzureServiceID FROM AzureService WHERE ServiceName = 'Virtual Machines')
, (SELECT SolutionID FROM [Solution] WHERE SolutionName = 'SQL Replication to Azure VM')
, 'Low'
, 'Low');
GO 

-- Queries
SELECT Problem.ProblemName, Solution.SolutionName
FROM Problem
INNER JOIN ProblemToSolution ON Problem.ProblemID  = ProblemToSolution.FromItem
INNER JOIN Solution ON SolutionID = ProblemToSolution.ToItem


/* 

https://www.red-gate.com/simple-talk/sql/sql-development/sql-server-graph-databases-part-1-introduction/
https://azure.microsoft.com/en-us/services/ 
INSERT INTO SolutionToService ($from_id, $to_id, Complexity, Cost)
VALUES (
(SELECT $node_id FROM AzureService WHERE ServiceName = 'Virtual Machines')
, (SELECT $node_id FROM [Solution] WHERE SolutionName = 'SQL Replication to Azure VM')
, 'Low'
, 'Low');
GO

SELECT Solution.SolutionName, AzureService.ServiceName
FROM Solution, SolutionToService, AzureService
WHERE MATCH (Solution<-(SolutionToService)-AzureService);
GO
*/
