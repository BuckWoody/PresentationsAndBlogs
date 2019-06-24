USE sqltoazure;
GO

-- Create Nodes
DROP TABLE IF EXISTS AzureService;
GO
CREATE TABLE AzureService (
AzureServiceID INT IDENTITY PRIMARY KEY
, ServiceName NVARCHAR(150)
, ServiceDescription NVARCHAR(MAX)
) AS NODE;
GO
DROP TABLE IF EXISTS ItemReference;
GO
CREATE TABLE ItemReference (
ItemReferenceID INT IDENTITY PRIMARY KEY
, ItemReferenceName NVARCHAR(150)
, ItemReferenceType NVARCHAR(50)
, ItemReferenceLocation NVARCHAR(150)
, ItemReferenceDescription NVARCHAR(MAX)
) AS NODE;
GO

DROP TABLE IF EXISTS ItemProperty;
GO
CREATE TABLE ItemProperty (
ItemPropertyID INT IDENTITY PRIMARY KEY
, ItemPropertyType NVARCHAR(100)
, ItemPropertyName NVARCHAR(150)
, ItemPropertyDescription NVARCHAR(MAX)
) AS NODE;
GO

DROP TABLE IF EXISTS Solution;
GO
CREATE TABLE Solution (
SolutionID INT IDENTITY PRIMARY KEY
, SolutionName NVARCHAR(150)
, SolutionDescription NVARCHAR(MAX)
) AS NODE;
GO

-- Create Edges
DROP TABLE IF EXISTS SolutionToService;
GO
CREATE TABLE SolutionToService (
Complexity NVARCHAR(100)
, Cost NVARCHAR(50)
) AS EDGE;

-- Fill tables
INSERT INTO AzureService (ServiceName, ServiceDescription ) 
VALUES ('Virtual Machines', 'Windows or Linux Virtual Machine')
GO 
INSERT INTO ItemReference (ItemReferenceName, ItemReferenceType, ItemReferenceLocation, ItemReferenceDescription) 
VALUES ('Windows Virtual Machines Documentation', 'Official Documentation', 'https://docs.microsoft.com/en-us/azure/virtual-machines/windows/', 'Official Documentation for Windows Virtual Machines')
,('Linux Virtual Machines Documentation', 'Official Documentation', 'https://docs.microsoft.com/en-us/azure/virtual-machines/linux/', 'Official Documentation for Linux Virtual Machines');
GO 

INSERT INTO Solution (SolutionName, SolutionDescription ) 
VALUES ('SQL Replication to Azure VM', 'Use SQL Server Replication to copy data to an Azure Virtual Machine.')
GO 
INSERT INTO ItemReference (ItemReferenceName, ItemReferenceType, ItemReferenceLocation, ItemReferenceDescription) 
VALUES ('SQL Server Replication to Azure', 'Official Documentation', 'https://docs.microsoft.com/en-us/sql/relational-databases/replication/sql-server-replication?view=sql-server-2017', 'Official Documentation for SQL Server Replication');
GO

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

/* 

https://www.red-gate.com/simple-talk/sql/sql-development/sql-server-graph-databases-part-1-introduction/
https://azure.microsoft.com/en-us/services/ 



INSERT INTO Posts ($from_id, $to_id) VALUES (
    (SELECT $node_id FROM FishLover WHERE FishLoverID = 1), 
    (SELECT $node_id FROM FishPost WHERE PostID = 3));

SELECT fl.Username, fs.CommonName, fs.ScientificName
  FROM FishLover fl INNER JOIN Likes lk
      ON fl.$node_id = lk.$from_id
    INNER JOIN FishSpecies fs
      ON lk.$to_id = fs.$node_id;

SELECT Lover.Username, Species.CommonName, Species.ScientificName
FROM FishLover Lover, Likes, FishSpecies Species
WHERE MATCH(Lover-(Likes)->Species);

*/
