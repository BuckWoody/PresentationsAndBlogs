---

title: "AdventureWorks Company 360"
owner: "Buck Woody"
purpose: "Deep, citable grounding for LLMs and humans on AdventureWorks OLTP/DW/OLAP samples: variants, objects, business scenarios, OLTP→DW mappings, SSAS/SSRS artifacts, governance, and ready-to-run examples."
scope: "AdventureWorks OLTP, DW, LT, SSAS (multidimensional/tabular) materials, SSRS samples, and Azure/Fabric options across SQL Server 2005→2025; emphasizes authoritative sources, reproducible installs, and full object-level documentation."
audience: "SQL Server practitioners, architects, trainers, and LLM agents using AdventureWorks for demos, workshops, and reasoning."
status: "Enhanced – v3.1"
last_updated: "2026-11-09"
version: "v3.1"
tags: ["domain:data", "platform:sql-server", "topic:adventureworks", "samples", "ssas", "ssrs", "olap", "dw", "fabric", "azure", "governance", "workloads"]
related_pages: ["Data Engineering", "Data Analysis", "Data Governance", "AI Governance"]

---

![Straight Path Solutions](assets/logo.png)

# AdventureWorks Company 360

This repository is the working library for the fictitious Adventure Works Cycles. This README is the **Company 360**: one citable description of the company and its data estate, covering the database variants, schemas and objects, business scenarios, the OLTP to warehouse mapping, reporting, installation, and governance patterns. Everything in the folders beneath it uses this document as its source of company facts, and cites it by section number (sections 1 to 18, and Appendices A to D).

## How this repository is organized

```
/
+-- README.md          This Company 360
+-- assets/            Shared images, such as the logo
+-- ai-governance/     Workload: data governance and AI usage for Adventure Works
```

A **workload** is a folder beneath the root that applies the Company 360 to one purpose. Each workload has its own README listing its files and the Company 360 sections it draws on. The list of workloads and their files is in [Workloads and assets](#workloads-and-assets) at the bottom of this page, and it grows as workloads are added.

## How to use this document

- **People:** use the numbered sections below as a reference. Start with the Overview (section 2) for the scale of the company.
- **LLM agents and Copilot:** follow the operating instructions in section 1, ground answers in this document, and cite the section you used.
- **Workload authors:** take facts from here instead of restating them, and say in your own README which sections you used.

## 1) LLM Operating Instructions

**When responding with AdventureWorks content, the LLM must:**

1. **Ground first** in this Page's **Source Library** and **References**; prefer Microsoft Learn & the official GitHub repo; cite every nontrivial claim.
2. **Preserve structure** — mirror requested headings/schemas; keep outputs skimmable.
3. **Show your work** — list **assumptions**, **constraints**, **steps**, and add T-SQL when helpful.
4. **Prefer correctness over coverage**; mark uncertainties explicitly.
5. **Use latest artifacts** — favor 2016→2025 releases and Azure/Fabric options when version-specific behavior matters.
6. **Avoid hallucinations**; if unknown, state how to verify (e.g., check object catalog, reference docs).
7. **Reuse prompts** from **Questions for Copilot** below.
8. **Version awareness** — AdventureWorks object names are stable from 2012 through 2022; the 2025 release adds FILESTREAM and additional engine feature hooks. The 2005 schema used different table names (e.g., `Person.Contact` instead of `Person.Person`).
9. **Always distinguish** OLTP (`AdventureWorks`), DW (`AdventureWorksDW`), and LT (`AdventureWorksLT`) — they are separate databases with different schemas.

---

## 2) Overview

**Adventure Works Cycles** is a fictitious multinational bicycle manufacturer used by Microsoft as the canonical SQL Server sample database family, spanning **OLTP**, **Data Warehouse (DW)**, and **OLAP (SSAS)** scenarios. It replaced the earlier *pubs* and *Northwind* samples starting with SQL Server 2005 and has been maintained continuously through **SQL Server 2025** and **Microsoft Fabric**.

Three primary database variants are shipped: **AdventureWorks (OLTP)**, **AdventureWorksDW (DW/star-schema)**, and **AdventureWorksLT (lightweight OLTP)**. The official **sql-server-samples** GitHub repository is the authoritative source for all `.bak` files and install scripts.

**Key facts about the company model:**
- Adventure Works Cycles is a large multinational manufacturing company producing and selling metal and composite bicycles.
- The company has approximately **500 products**, **20,000 customers**, and **31,000 sales orders** with an average of 4 line items each — large enough to be interesting, not unwieldy.
- The employee hierarchy has nearly **300 employees** organized in a tree managed via `hierarchyid`.
- Sales channels are split: **Internet** (direct-to-consumer) and **Reseller** (through business partners/stores), which is why the DW has separate `FactInternetSales` and `FactResellerSales` tables.
- The fictional fiscal year runs **July 1 – June 30**, which matters for time-intelligence demos.
- Adventure Works operates in multiple **territories** and **currencies**, enabling multi-currency and geospatial analysis demos.

**Schema stability note:** AdventureWorks has not seen significant object-level changes since the 2012 version. Differences between versions are primarily the **database name** (e.g., `AdventureWorks2019`, `AdventureWorks2022`) and the **compatibility level**. The 2025 release adds FILESTREAM-based storage changes. Always verify the target version compatibility level when demonstrating version-specific engine features.

---

## 3) Source Library (Authoritative — keep handy)

| Source | URL | Notes |
|---|---|---|
| AdventureWorks install & versions (Learn) | https://learn.microsoft.com/en-us/sql/samples/adventureworks-install-configure?view=sql-server-ver17 | Direct `.bak` download links for OLTP, DW, LT from 2008R2→2025 and Azure/Fabric deployment guidance |
| Official samples repo (GitHub) | https://github.com/microsoft/sql-server-samples/tree/master/samples/databases/adventure-works | Install scripts, README, version notes, 2025 feature changes |
| GitHub release tag (all .bak files) | https://github.com/Microsoft/sql-server-samples/releases/tag/adventureworks | Canonical download location for all AdventureWorks `.bak` files |
| SQL samples landing page (Learn) | https://learn.microsoft.com/en-us/sql/samples/sql-samples-where-are?view=sql-server-ver17 | Where to find AdventureWorks and WideWorldImporters |
| SSAS Multidimensional tutorial | https://learn.microsoft.com/en-us/analysis-services/multidimensional-tutorial/multidimensional-modeling-adventure-works-tutorial?view=asallproducts-allversions | End-to-end cube modeling (dimensions, cubes, M2M, KPIs, actions, perspectives, translations) |
| SSAS tutorial source (GitHub) | https://github.com/MicrosoftDocs/bi-shared-docs | Tutorial markdown source |
| Analysis Services samples (Learn) | https://learn.microsoft.com/en-us/analysis-services/analysis-services-samples?view=sql-analysis-services-2025 | Current SSAS guidance & sample project links |
| AdventureWorksDW data dictionary (Dataedo) | https://dataedo.com/samples/html/Data_warehouse/doc/AdventureWorksDW_4/home.html | Browseable DW fact/dim table documentation |
| AdventureWorks OLTP table catalog (Dataedo) | https://dataedo.com/samples/html/AdventureWorks/doc/AdventureWorks_2/tables.html | Enumerated OLTP tables with column descriptions |
| AdventureWorks full data dictionary (PDF) | https://banbao991.github.io/resources/DB/AdventureWorks.pdf | Table descriptions, column metadata, FK/PK information |
| In-Memory OLTP sample (Learn) | https://learn.microsoft.com/en-us/sql/relational-databases/in-memory-oltp/sample-database-for-in-memory-oltp?view=sql-server-ver17 | Hekaton migration scripts and workload driver |
| Data API builder sample (GitHub) | https://github.com/Azure-Samples/dab-adventureworks-lt | REST + GraphQL on AdventureWorksLT |
| AdventureWorks for Postgres (GitHub) | https://github.com/lorint/AdventureWorks-for-Postgres | OLTP schema ported to PostgreSQL |
| Fabric: Load AdventureWorksLT (Learn) | https://learn.microsoft.com/en-us/fabric/database/sql/load-adventureworks-sample-data | One-click sample load in Microsoft Fabric SQL Database |
| SSRS sample reports (Database Journal) | https://www.databasejournal.com/ms-sql/taking-advantage-of-sample-reporting-services-reports/ | Classic SSRS sample set walkthrough |
| SSRS community refresh (sqlpowered) | https://sqlpowered.com/reporting-services-samples-for-adventureworks2017/ | AdventureWorks 2017 SSRS report set |
| GitHub location change notice | https://techcommunity.microsoft.com/blog/sqlserver/new-github-location-for-adventureworks/385728 | Moved from CodePlex to GitHub |
| SSAS multidimensional .abf backups | https://github.com/Microsoft/sql-server-samples/releases/tag/adventureworks-analysis-services | Adventure Works cube `.abf` backup files (Enterprise + Standard; Tabular 1200) |
| Install for SQL Server 2025 (MSSQLTips) | https://www.mssqltips.com/sqlservertip/11463/install-the-adventureworks-database-for-sql-server/ | Step-by-step for SQL Server 2025 CTP, compatibility level 170 |

---

## 4) Variants & Data Sources (What exists, when to use)

### A. OLTP — `AdventureWorks` / `AdventureWorks20xx`

**Purpose:** Full transactional workload covering **Person, HumanResources, Production, Purchasing, Sales**; realistic FK constraints, UDTs, XML columns, binary media, and sample FILESTREAM content (2025).

**Schema count:** 5 business schemas + `dbo` utilities = **~71 tables, 20 views, 10 stored procedures, 11 UDFs**, 1 database-level DDL trigger (2012+).

**When to use:**
- T-SQL training: joins, CTEs, recursive BOM, window functions, PIVOT/UNPIVOT
- Schema design demos: normalization, FK patterns, UDTs, check constraints
- Indexing labs: covering indexes, filtered indexes, columnstore
- Transaction management: TRY/CATCH, nested transactions, error logging
- XML and binary data: `Production.Document`, `Production.ProductPhoto`, `HumanResources.JobCandidate.Resume`
- Performance tuning: Query Store demos (2016+), execution plan analysis, statistics management
- In-Memory OLTP: migrate selected tables to memory-optimized (Hekaton) with natively compiled procs

**Notable data characteristics:**
- Order data spans **May 31, 2011 through June 30, 2014** (fiscal years 2012–2014 for query-range demos)
- Products span 4 categories: **Bikes, Components, Clothing, Accessories**
- Territories cover North America, Europe, and Pacific regions
- Multi-currency support via `Sales.CurrencyRate`

**Get it:** `.bak` files per SQL Server version (2008 R2→2025) or install scripts from GitHub (`oltp-install-script` folder). License: MIT.

---

### B. Data Warehouse — `AdventureWorksDW` / `AdventureWorksDW20xx`

**Purpose:** Star-schema DW for OLAP, reporting, and BI tooling demonstrations. Pre-populated with denormalized fact and dimension tables aligned to the OLTP source.

**When to use:** SSAS cube modeling (multidimensional and tabular), MDX/DAX labs, SSRS matrix reports, Power BI connectivity, KPI/perspective demos, time intelligence (fiscal + calendar), promotions analysis, currency conversion, call center analysis, survey analysis.

**Schema:** All objects are in the `dbo` schema (no schema-qualified business groupings like OLTP).

**Full Table Inventory:**

*Dimension Tables (16):*

| Table | Purpose |
|---|---|
| `DimAccount` | Chart of accounts for finance scenarios; parent-child hierarchy |
| `DimCurrency` | ISO currency codes and names |
| `DimCustomer` | Customer demographics, geography FK, SCD Type 1 (no history) |
| `DimDate` | Date spine with 14+ attributes: calendar/fiscal year/quarter/month/week, day-of-week, flags for holidays and working days |
| `DimDepartmentGroup` | HR department group hierarchy (parent-child) |
| `DimEmployee` | Employee dimension with HR attributes; SCD Type 1 |
| `DimGeography` | Geographic hierarchy: City → State/Province → Country/Region → Sales Territory |
| `DimOrganization` | Organizational hierarchy for finance scenarios; currency FK |
| `DimProduct` | Full product attributes: name, color, size, weight, list price, standard cost, model, subcategory, category |
| `DimProductCategory` | Product category lookup (Bikes, Components, Clothing, Accessories) |
| `DimProductSubcategory` | Product subcategory lookup; FK to `DimProductCategory` |
| `DimPromotion` | Promotions/special offers: type, discount amount, minimum/maximum quantity, date range |
| `DimReseller` | Reseller business entities: type, business type, number of employees, annual sales |
| `DimSalesReason` | Sales reason lookup: price, quality, manufacturer, review, etc. |
| `DimSalesTerritory` | Territory: group, country, region with sales targets |
| `DimScenario` | Scenario labels for finance: Actual, Budget, Forecast |

*Fact Tables (9):*

| Table | Grain | Key Measures |
|---|---|---|
| `FactInternetSales` | One row per internet sales order line | OrderQuantity, UnitPrice, UnitPriceDiscountPct, DiscountAmount, ProductStandardCost, TotalProductCost, SalesAmount, TaxAmt, Freight, ExtendedAmount, RevisionNumber |
| `FactInternetSalesReason` | Bridge: one row per sales order line × sales reason | Links `FactInternetSales` to `DimSalesReason` (many-to-many) |
| `FactResellerSales` | One row per reseller sales order line | Same measures as `FactInternetSales` plus CarrierTrackingNumber, CustomerPONumber |
| `FactSalesQuota` | One row per salesperson per quarter | SalesAmountQuota; FK to `DimEmployee`, `DimDate` (calendar quarter grain) |
| `FactFinance` | One row per account × organization × scenario × date | Amount; FK to `DimAccount`, `DimDate`, `DimOrganization`, `DimScenario` |
| `FactCallCenter` | One row per call center shift-day | Calls, Orders, AutomaticResponses, AverageTimePerIssue, ServiceGrade; FK to `DimDate` |
| `FactCurrencyRate` | One row per currency × date | AverageRate, EndOfDayRate; FK to `DimCurrency`, `DimDate` |
| `FactProductInventory` | One row per product × location × date (snapshot) | UnitsBalance, UnitCost; FK to `DimProduct`, `DimDate` |
| `FactSurveyResponse` | One row per survey response | 30+ demographic/opinion columns; FK to `DimDate`, `DimCustomer`, `DimGeography` |
| `FactAdditionalInternationalProductDescription` | International product descriptions | FK to `DimProduct`; used for multilingual demos |

**Get it:** `.bak` files aligned to engine versions, or `data-warehouse-install-script` folder on GitHub.

---

### C. Lightweight — `AdventureWorksLT`

**Purpose:** Simplified, denormalized OLTP for quickstarts, Azure/Fabric labs, and beginner SQL training. Uses the single schema `SalesLT.*` plus `dbo.*` utilities. **12 tables** vs. ~71 in the full OLTP.

**SalesLT Schema Tables (12):**

| Table | Purpose |
|---|---|
| `SalesLT.Address` | Shipping/billing addresses |
| `SalesLT.Customer` | Customers (de-normalized: name, email, phone, company in one table) |
| `SalesLT.CustomerAddress` | Junction: customer ↔ address (with AddressType) |
| `SalesLT.Product` | Products with list price, standard cost, color, size, weight, category FK |
| `SalesLT.ProductCategory` | Simplified category (no subcategory separate table) |
| `SalesLT.ProductDescription` | Product descriptions in culture-specific text |
| `SalesLT.ProductModel` | Product model name and XML catalog description |
| `SalesLT.ProductModelProductDescription` | Junction: model ↔ description ↔ culture |
| `SalesLT.SalesOrderDetail` | Order line items: product, quantity, unit price, discount |
| `SalesLT.SalesOrderHeader` | Order headers: customer, addresses, status, dates, totals |
| `dbo.BuildVersion` | Database build version info |
| `dbo.ErrorLog` | TRY/CATCH error capture table |

**SalesLT Views:**
- `SalesLT.vGetAllCategories` — recursive product category hierarchy
- `SalesLT.vProductAndDescription` — product × description × culture
- `SalesLT.vProductModelCatalogDescription` — XML-shredded catalog descriptions

**SalesLT Stored Procedures:**
- `SalesLT.uspLogError` — logs errors to `dbo.ErrorLog`
- `SalesLT.uspPrintError` — prints error messages

**SalesLT Functions:**
- `dbo.ufnGetAllCategories()` — TVF returning recursive category hierarchy
- `dbo.ufnGetCustomerInformation(@CustomerID)` — returns customer details as a table

**When to use:** Azure SQL quickstarts, REST/GraphQL via Data API builder, beginner SQL training (JOINs without complexity overload), Fabric SQL Database demos, Power Apps connectors, App Service tutorials.

**Get it / Azure:** Create Azure SQL DB with **Sample: AdventureWorksLT** from the portal; in Microsoft Fabric, select **Sample Data** on a new SQL database; or restore a `.bak` file.

---

### D. Extended / Specialized Samples

#### D1. SQL Server 2016 Extended — `AdventureWorks2016_EXT` / `AdventureWorksDW2016_EXT`

- **Purpose:** Showcases SQL Server 2016 features on the AdventureWorks schema; download size ~883 MB.
- **Features demonstrated:** JSON support (`FOR JSON`, `OPENJSON`), row-level security, dynamic data masking, temporal tables (system-versioned), stretch database (deprecated in later versions), query store basics, PolyBase stubs.
- **Use when:** teaching any 2016-era feature against a familiar schema.
- **Scripts:** Run the SQL Server 2016 feature sample scripts against this database (available in the `scripts` folder of the GitHub repo).

#### D2. In-Memory OLTP (Hekaton) Demo

- **Purpose:** Migrates selected AdventureWorks OLTP tables to **memory-optimized tables** and creates **natively compiled stored procedures**; includes a workload driver for throughput comparison.
- **Tables migrated (examples):** `Sales.SalesOrderHeader_inmem`, `Sales.SalesOrderDetail_inmem`, `Production.Product_inmem`
- **Includes:** Memory-optimized table types, hash indexes, range indexes, natively compiled procedures for order insertion.
- **Use when:** demonstrating In-Memory OLTP throughput gains, migration methodology, or explaining Hekaton architecture.
- **Source:** `learn.microsoft.com/en-us/sql/relational-databases/in-memory-oltp/sample-database-for-in-memory-oltp`

#### D3. SSAS Multidimensional — Adventure Works Cube

- **Databases:** Enterprise Edition (`.abf`) and Standard Edition (`.abf`) — two separate backups.
- **Cube name:** `Adventure Works`
- **Source data:** `AdventureWorksDW`
- **Perspectives (named subsets of the cube):** `Channel Sales`, `Direct Sales`, `Finance`, `Sales Summary`, `Warehouse`
- **Measure Groups:** Internet Sales, Reseller Sales, Sales Quotas, Sales Quotas 1, Exchange Rates, Sales Reasons, Financial Reporting, Internet Customers, Reseller Orders, Internet Orders, Mined Customers (data mining integration)
- **Translations:** Multiple language translations for dimension members and measure captions (demonstrates the Translations feature).
- **Get it:** `https://github.com/Microsoft/sql-server-samples/releases/tag/adventureworks-analysis-services`

#### D4. SSAS Tabular — AdventureWorks Tabular Model

- **Compatibility level 1200** (SQL Server 2016 model)
- **Source data:** `AdventureWorksDW`
- **Includes:** Sales, Customer, Product, Date, and Territory tables; DAX calculated columns and measures; row-level security roles.
- **Get it:** `adventure-works-tabular-model-1200-full-database-backup.zip` from the Analysis Services release tag.

#### D5. Docker / Container Images

- Community scripts exist to restore AdventureWorks into SQL Server Linux containers for portable labs.
- Pattern: Pull `mcr.microsoft.com/mssql/server:20xx-latest`, copy `.bak`, execute `RESTORE DATABASE`.
- Docker Compose examples exist in community repositories (e.g., AdventureWorks-for-Postgres also provides Docker Compose).

#### D6. Microsoft Fabric SQL Database

- `AdventureWorksLT` is natively available as a one-click **Sample Data** load in Fabric SQL Database.
- After load, the `SalesLT` schema is present and ready to query via T-SQL, Power BI Direct Lake, or REST.

---

## 5) OLTP Schemas & Canonical Objects (ERD-level Detail)

AdventureWorks uses schema-qualified naming to group business areas. The `dbo` schema holds cross-cutting utilities.

### Schema: `dbo` (Utilities)

**Tables:**
- `AWBuildVersion` — Tracks the current version number of the sample database install.
- `DatabaseLog` — Audit table for DDL events captured by trigger `ddlDatabaseTriggerLog`; columns: DatabaseLogID, PostTime, DatabaseUser, Event, Schema, Object, TSQL, XmlEvent.
- `ErrorLog` — Errors caught by `CATCH` blocks; populated by `dbo.uspLogError`; columns: ErrorLogID, ErrorTime, UserName, ErrorNumber, ErrorSeverity, ErrorState, ErrorProcedure, ErrorLine, ErrorMessage.

**User-Defined Types (UDTs) — `dbo` schema:**
- `AccountNumber` — nvarchar(15), NOT NULL
- `Flag` — bit, NOT NULL
- `Name` — nvarchar(50), NOT NULL
- `NameStyle` — bit, NOT NULL
- `OrderNumber` — nvarchar(25), NOT NULL
- `Phone` — nvarchar(25), NOT NULL

These UDTs are used pervasively to standardize semantics across schemas — an important data quality teaching point.

---

### Schema: `Person` (Identity & Contact)

**Business purpose:** Manages all human/organizational identity data. Central to the system — nearly every other schema references `Person.Person` or `Person.BusinessEntity`.

**Tables:**

| Table | Key Columns | Purpose |
|---|---|---|
| `Person.BusinessEntity` | BusinessEntityID (PK), rowguid, ModifiedDate | Root identity record; all persons, vendors, and stores inherit from this |
| `Person.Person` | BusinessEntityID (FK/PK), PersonType, NameStyle, Title, FirstName, MiddleName, LastName, Suffix, EmailPromotion, AdditionalContactInfo (XML), Demographics (XML) | Core person record; PersonType: EM=Employee, SP=SalesPerson, IN=Individual Customer, VC=Vendor Contact, GC=General Contact, SC=Store Contact |
| `Person.Address` | AddressID (PK), AddressLine1, AddressLine2, City, StateProvinceID (FK), PostalCode, SpatialLocation (geography), rowguid | Physical addresses; `SpatialLocation` is `geography` type for spatial demos |
| `Person.AddressType` | AddressTypeID (PK), Name, rowguid | Lookup: Billing, Home, Main Office, Primary, Shipping, Archive |
| `Person.BusinessEntityAddress` | BusinessEntityID+AddressID+AddressTypeID (composite PK) | Junction: entity ↔ address ↔ address type |
| `Person.BusinessEntityContact` | BusinessEntityID+PersonID+ContactTypeID (composite PK) | Junction: entity ↔ contact person ↔ contact type |
| `Person.ContactType` | ContactTypeID (PK), Name | Lookup: Accounting Manager, Assistant Sales Agent, Order Administrator, Owner, Purchase Manager, etc. |
| `Person.CountryRegion` | CountryRegionCode (PK), Name | ISO country codes and names |
| `Person.EmailAddress` | BusinessEntityID+EmailAddressID (composite PK), EmailAddress, rowguid | One-to-many email addresses per person |
| `Person.Password` | BusinessEntityID (PK), PasswordHash, PasswordSalt, rowguid | Hashed password credentials (demonstrates secure storage patterns) |
| `Person.PersonPhone` | BusinessEntityID+PhoneNumber+PhoneNumberTypeID (composite PK) | One-to-many phone numbers per person |
| `Person.PhoneNumberType` | PhoneNumberTypeID (PK), Name | Lookup: Cell, Home, Work |
| `Person.StateProvince` | StateProvinceID (PK), StateProvinceCode, CountryRegionCode (FK), IsOnlyStateProvinceFlag, Name, TerritoryID (FK), rowguid | State/province lookup with territory assignment |

**Views:**
- `Person.vAdditionalContactInfo` — XML-shredded view of the `AdditionalContactInfo` column
- `Person.vStateProvinceCountryRegion` — Joins StateProvince to CountryRegion for cleaner display

---

### Schema: `HumanResources` (Employee Management)

**Business purpose:** Full employee lifecycle — hiring, org placement, pay, scheduling.

**Tables:**

| Table | Key Columns | Purpose |
|---|---|---|
| `HumanResources.Department` | DepartmentID (PK), Name, GroupName | Lookup of departments by group (Engineering, Executive General and Administration, Human Resources, Information Services, Manufacturing, Production Control, Purchasing, Quality Assurance, Research and Development, Sales and Marketing, Shipping and Receiving, Tool Design) |
| `HumanResources.Employee` | BusinessEntityID (FK/PK), NationalIDNumber, LoginID, OrganizationNode (hierarchyid), OrganizationLevel (computed), JobTitle, BirthDate, MaritalStatus, Gender, HireDate, SalariedFlag, VacationHours, SickLeaveHours, CurrentFlag, rowguid | Core employee record; **`OrganizationNode` (hierarchyid)** is the canonical demo for hierarchyid usage; `OrganizationLevel` is a computed column |
| `HumanResources.EmployeeDepartmentHistory` | BusinessEntityID+DepartmentID+ShiftID+StartDate (composite PK), EndDate | Tracks department/shift assignments over time — SCD Type 2 demo source |
| `HumanResources.EmployeePayHistory` | BusinessEntityID+RateChangeDate (composite PK), Rate, PayFrequency | Salary change history — SCD Type 2 demo source |
| `HumanResources.JobCandidate` | JobCandidateID (PK), BusinessEntityID (FK, nullable), Resume (XML) | Unstructured HR data; `Resume` column is `xml` type — XML querying demos |
| `HumanResources.Shift` | ShiftID (PK), Name, StartTime, EndTime | Lookup: Day, Evening, Night shifts |

**Views:**
- `HumanResources.vEmployee` — Full employee contact information
- `HumanResources.vEmployeeDepartment` — Current department assignments
- `HumanResources.vEmployeeDepartmentHistory` — Historical department assignments (SCD history)
- `HumanResources.vJobCandidate` — Basic job candidate info
- `HumanResources.vJobCandidateEducation` — XML-shredded education data from Resume
- `HumanResources.vJobCandidateEmployment` — XML-shredded employment history from Resume

---

### Schema: `Production` (Manufacturing & Catalog)

**Business purpose:** Product catalog, bill of materials, manufacturing operations, quality, and inventory.

**Tables:**

| Table | Key Columns | Purpose |
|---|---|---|
| `Production.BillOfMaterials` | BillOfMaterialsID (PK), ProductAssemblyID (FK, nullable), ComponentID (FK), StartDate, EndDate, UnitMeasureCode, BOMLevel, PerAssemblyQty | Recursive BOM; `BOMLevel` allows multi-level assembly queries; NULL `ProductAssemblyID` = top-level component |
| `Production.Culture` | CultureID (PK), Name | Languages for product descriptions: Arabic, Chinese (Traditional), English, French, Hebrew, Thai |
| `Production.Document` | DocumentNode (hierarchyid, PK), DocumentLevel (computed), Title, Owner (FK→Employee), FolderFlag, FileName, FileExtension, Revision, ChangeNumber, Status, DocumentSummary, Document (varbinary(max)), rowguid | Product/engineering documents; FILESTREAM-backed in 2025 edition |
| `Production.Illustration` | IllustrationID (PK), Diagram (xml) | Bicycle assembly diagrams stored as XML SVG |
| `Production.Location` | LocationID (PK), Name, CostRate, Availability | Manufacturing locations/work centers (e.g., Frame Forming, Frame Welding, Painting, Subassembly, Final Assembly) |
| `Production.Product` | ProductID (PK), Name, ProductNumber, MakeFlag, FinishedGoodsFlag, Color, SafetyStockLevel, ReorderPoint, StandardCost, ListPrice, Size, SizeUnitMeasureCode, WeightUnitMeasureCode, Weight, DaysToManufacture, ProductLine, Class, Style, ProductSubcategoryID (FK), ProductModelID (FK), SellStartDate, SellEndDate, DiscontinuedDate, rowguid | Core product table; 504 products; ProductLine: R=Road, M=Mountain, T=Touring, S=Standard; Class: H=High, M=Medium, L=Low |
| `Production.ProductCategory` | ProductCategoryID (PK), Name, rowguid | Top-level: Bikes, Components, Clothing, Accessories |
| `Production.ProductCostHistory` | ProductID+StartDate (composite PK), EndDate, StandardCost | Cost change history — useful for SCD and trend analysis |
| `Production.ProductDescription` | ProductDescriptionID (PK), Description, rowguid | Multilingual product descriptions |
| `Production.ProductDocument` | ProductID+DocumentNode (composite PK), ModifiedDate | Junction: product ↔ supporting document |
| `Production.ProductInventory` | ProductID+LocationID (composite PK), Shelf, Bin, Quantity, rowguid | Current inventory levels by location/shelf/bin |
| `Production.ProductListPriceHistory` | ProductID+StartDate (composite PK), EndDate, ListPrice | List price change history — trend/SCD demos |
| `Production.ProductModel` | ProductModelID (PK), Name, CatalogDescription (xml), Instructions (xml), rowguid | Product model groups; `CatalogDescription` is XML with product marketing content; `Instructions` is XML with manufacturing steps |
| `Production.ProductModelIllustration` | ProductModelID+IllustrationID (composite PK) | Junction: model ↔ assembly diagram |
| `Production.ProductModelProductDescriptionCulture` | ProductModelID+ProductDescriptionID+CultureID (composite PK) | Junction: model ↔ description ↔ culture (multilingual descriptions) |
| `Production.ProductPhoto` | ProductPhotoID (PK), ThumbNailPhoto (varbinary(max)), ThumbnailPhotoFileName, LargePhoto (varbinary(max)), LargePhotoFileName | Product images stored as binary — binary/FILESTREAM governance demo |
| `Production.ProductProductPhoto` | ProductID+ProductPhotoID (composite PK), Primary | Junction: product ↔ photo |
| `Production.ProductReview` | ProductReviewID (PK), ProductID (FK), ReviewerName, ReviewDate, EmailAddress, Rating, Comments | Customer product reviews; full-text search demo target |
| `Production.ProductSubcategory` | ProductSubcategoryID (PK), ProductCategoryID (FK), Name, rowguid | 37 subcategories under 4 parent categories |
| `Production.ScrapReason` | ScrapReasonID (PK), Name | Quality/manufacturing scrap reasons lookup (e.g., Wheel Misalignment, Trim Length Too Long) |
| `Production.TransactionHistory` | TransactionID (PK), ProductID (FK), ReferenceOrderID, ReferenceOrderLineID, TransactionDate, TransactionType, Quantity, ActualCost, ModifiedDate | All inventory transactions; TransactionType: P=Purchase Order, S=Sales Order, W=Work Order |
| `Production.TransactionHistoryArchive` | Same as above | Archived older transactions; partitioning/archiving demo |
| `Production.UnitMeasure` | UnitMeasureCode (PK), Name | Lookup: BX (Box), DZ (Dozen), EA (Each), FT (Foot), G (Gram), GL (Gallon), HR (Hour), IN (Inch), KG (Kilogram), L (Liter), LB (Pound), MG (Milligram), ML (Milliliter), OZ (Ounce), QT (Quart), SET (Set) |
| `Production.WorkOrder` | WorkOrderID (PK), ProductID (FK), OrderQty, StockedQty (computed), ScrappedQty, StartDate, EndDate, DueDate, ScrapReasonID (FK) | Manufacturing work orders |
| `Production.WorkOrderRouting` | WorkOrderID+ProductID+OperationSequence (composite PK), LocationID (FK), ScheduledStartDate, ScheduledEndDate, ActualStartDate, ActualEndDate, ActualResourceHrs, PlannedCost, ActualCost | Routing steps per work order per location |

**Views:**
- `Production.vProductAndDescription` — Product with localized description (culture-joined)
- `Production.vProductModelCatalogDescription` — XML-shredded marketing catalog data
- `Production.vProductModelInstructions` — XML-shredded manufacturing instructions

---

### Schema: `Purchasing` (Procurement & Vendors)

**Business purpose:** Vendor management and procure-to-pay workflow.

**Tables:**

| Table | Key Columns | Purpose |
|---|---|---|
| `Purchasing.ProductVendor` | ProductID+BusinessEntityID (composite PK), AverageLeadTime, StandardPrice, LastReceiptCost, LastReceiptDate, MinOrderQty, MaxOrderQty, OnOrderQty, UnitMeasureCode (FK) | Products-to-vendor catalog with pricing and lead times |
| `Purchasing.PurchaseOrderDetail` | PurchaseOrderID+PurchaseOrderDetailID (composite PK), DueDate, OrderQty, ProductID (FK), UnitPrice, LineTotal (computed), ReceivedQty, RejectedQty, StockedQty (computed) | Line items for purchase orders |
| `Purchasing.PurchaseOrderHeader` | PurchaseOrderID (PK), RevisionNumber, Status, EmployeeID (FK), VendorID (FK), ShipMethodID (FK), OrderDate, ShipDate, SubTotal, TaxAmt, Freight, TotalDue (computed) | Purchase order headers; Status: 1=Pending, 2=Approved, 3=Rejected, 4=Complete |
| `Purchasing.ShipMethod` | ShipMethodID (PK), Name, ShipBase, ShipRate | Shipping carriers and rates (e.g., CARGO TRANSPORT 5, OVERNIGHT J-FAST, XRQ-TRUCK GROUND) |
| `Purchasing.Vendor` | BusinessEntityID (FK/PK), AccountNumber, Name, CreditRating, PreferredVendorStatus, ActiveFlag, PurchasingWebServiceURL, ModifiedDate | Vendor master; CreditRating 1–5 (1=Superior); PreferredVendorStatus flag |

**Views:**
- `Purchasing.vVendorWithAddresses` — Vendor with all associated addresses
- `Purchasing.vVendorWithContacts` — Vendor with all associated contact persons

---

### Schema: `Sales` (Orders, Customers & Selling)

**Business purpose:** Full order-to-cash workflow, customer management, territory management, and pricing/promotions.

**Tables:**

| Table | Key Columns | Purpose |
|---|---|---|
| `Sales.CountryRegionCurrency` | CountryRegionCode+CurrencyCode (composite PK) | Country-to-currency mapping (one-to-many countries per currency) |
| `Sales.CreditCard` | CreditCardID (PK), CardType, CardNumber (masked), ExpMonth, ExpYear | Credit card records; demonstrates PII masking patterns |
| `Sales.Currency` | CurrencyCode (PK), Name | ISO 4217 currency codes |
| `Sales.CurrencyRate` | CurrencyRateID (PK), CurrencyRateDate, FromCurrencyCode (FK), ToCurrencyCode (FK), AverageRate, EndOfDayRate | Daily currency exchange rates; ~13,532 rows |
| `Sales.Customer` | CustomerID (PK), PersonID (FK, nullable), StoreID (FK, nullable), TerritoryID (FK), AccountNumber (computed), rowguid | Central customer record; PersonID populated for individual customers, StoreID for store customers |
| `Sales.PersonCreditCard` | BusinessEntityID+CreditCardID (composite PK) | Junction: person ↔ credit card |
| `Sales.SalesOrderDetail` | SalesOrderID+SalesOrderDetailID (composite PK), CarrierTrackingNumber, OrderQty, ProductID (FK), SpecialOfferID (FK), UnitPrice, UnitPriceDiscount, LineTotal (computed), rowguid | Order line items; ~121,317 rows |
| `Sales.SalesOrderHeader` | SalesOrderID (PK), RevisionNumber, OrderDate, DueDate, ShipDate, Status, OnlineOrderFlag, SalesOrderNumber (computed), PurchaseOrderNumber, AccountNumber, CustomerID (FK), SalesPersonID (FK), TerritoryID (FK), BillToAddressID (FK), ShipToAddressID (FK), ShipMethodID (FK), CreditCardID (FK), CreditCardApprovalCode, CurrencyRateID (FK), SubTotal, TaxAmt, Freight, TotalDue (computed), Comment, rowguid | Order headers; ~31,465 rows; `OnlineOrderFlag=1` = Internet channel, `0` = Reseller channel |
| `Sales.SalesOrderHeaderSalesReason` | SalesOrderID+SalesReasonID (composite PK) | Junction: order ↔ reason (one order can have multiple reasons) — many-to-many demo |
| `Sales.SalesPerson` | BusinessEntityID (FK/PK), TerritoryID (FK), SalesQuota, Bonus, CommissionPct, SalesYTD, SalesLastYear, rowguid | Sales reps with quota/commission; base for sales performance analysis |
| `Sales.SalesPersonQuotaHistory` | BusinessEntityID+QuotaDate (composite PK), SalesQuota | Quota change history per rep per period |
| `Sales.SalesReason` | SalesReasonID (PK), Name, ReasonType | Why customers bought: Price, Quality, Review, Manufacturer, Advertisement, On Promotion, Demo Event, Sponsorship, TV Advertisement, Magazine Advertisement, Web, Other |
| `Sales.SalesTaxRate` | SalesTaxRateID (PK), StateProvinceID (FK), TaxType, TaxRate, Name | Tax rates by state/type |
| `Sales.SalesTerritory` | TerritoryID (PK), Name, CountryRegionCode (FK), `Group`, SalesYTD, SalesLastYear, CostYTD, CostLastYear, rowguid | 10 territories (Canada, Central, France, Germany, Northeast, Northwest, Pacific, Southeast, Southwest, United Kingdom) |
| `Sales.SalesTerritoryHistory` | BusinessEntityID+TerritoryID+StartDate (composite PK), EndDate | Tracks territory assignments for reps over time (SCD source) |
| `Sales.ShoppingCartItem` | ShoppingCartItemID (PK), ShoppingCartID, Quantity, ProductID (FK), DateCreated | Shopping cart (web) items; used for abandoned cart / session demos |
| `Sales.SpecialOffer` | SpecialOfferID (PK), Description, DiscountPct, Type, Category, StartDate, EndDate, MinQty, MaxQty, rowguid | Promotions and special offers catalog |
| `Sales.SpecialOfferProduct` | SpecialOfferID+ProductID (composite PK), rowguid | Junction: promotion ↔ eligible product |
| `Sales.Store` | BusinessEntityID (FK/PK), Name, SalesPersonID (FK), Demographics (xml), rowguid | Retail stores (resellers); `Demographics` XML stores store attributes like AnnualSales, AnnualRevenue, BankName, BusinessType |

**Views:**
- `Sales.vIndividualCustomer` — Individual customers with demographics and contact info
- `Sales.vPersonDemographics` — XML-shredded demographics (TotalPurchaseYTD, DateFirstPurchase, BirthDate, MaritalStatus, YearlyIncome, Gender, TotalChildren, NumberChildrenAtHome, Education, Occupation, HomeOwnerFlag, NumberCarsOwned, CommuteDistance, Region, Age, BuyingGroup)
- `Sales.vSalesPerson` — Sales rep with territory and contact info
- `Sales.vSalesPersonSalesByFiscalYears` — Crosstab of sales per rep per fiscal year (PIVOT demo)
- `Sales.vStoreWithAddresses` — Store with all addresses
- `Sales.vStoreWithContacts` — Store with all contacts
- `Sales.vStoreWithDemographics` — XML-shredded store demographics

---

## 6) OLTP Stored Procedures (10) — Detail

| Schema.Procedure | Parameters | Purpose |
|---|---|---|
| `dbo.uspGetBillOfMaterials` | `@StartProductID int, @CheckDate datetime` | Recursive CTE to retrieve full multi-level BOM for a product as of a date |
| `dbo.uspGetEmployeeManagers` | `@BusinessEntityID int` | Recursive CTE via `hierarchyid` to return the management chain above an employee |
| `dbo.uspGetManagerEmployees` | `@BusinessEntityID int` | Recursive CTE to return all direct and indirect reports under a manager |
| `dbo.uspGetWhereUsedProductID` | `@StartProductID int, @CheckDate datetime` | Where-used query: find all assemblies that use a given component as of a date |
| `dbo.uspLogError` | `@ErrorLogID int OUTPUT` | Captures error details inside a CATCH block and inserts into `dbo.ErrorLog` |
| `dbo.uspPrintError` | (none) | Prints error details to the Messages window from inside a CATCH block |
| `dbo.uspSearchCandidateResumes` | `@searchString nvarchar(1000), @useInflectional bit, @useThesaurus bit, @language int` | Full-text search against `HumanResources.JobCandidate.Resume` XML |
| `HumanResources.uspUpdateEmployeeHireInfo` | `@BusinessEntityID int, @JobTitle nvarchar(50), @HireDate datetime, @RateChangeDate datetime, @Rate money, @PayFrequency tinyint, @CurrentFlag bit` | Updates Employee, adds PayHistory record; uses explicit transaction |
| `HumanResources.uspUpdateEmployeeLogin` | `@BusinessEntityID int, @OrganizationNode hierarchyid, @LoginID nvarchar(256), @JobTitle nvarchar(50), @HireDate datetime, @CurrentFlag bit` | Updates login and org placement |
| `HumanResources.uspUpdateEmployeePersonalInfo` | `@BusinessEntityID int, @NationalIDNumber nvarchar(15), @BirthDate datetime, @MaritalStatus nchar(1), @Gender nchar(1)` | Updates personal demographics |

---

## 7) OLTP User-Defined Functions (11) — Detail

| Function | Type | Returns | Purpose |
|---|---|---|---|
| `dbo.ufnGetAccountingEndDate()` | Scalar | `datetime` | Returns the last date of the current accounting period |
| `dbo.ufnGetAccountingStartDate()` | Scalar | `datetime` | Returns the first date of the current accounting period |
| `dbo.ufnGetContactInformation(@PersonID)` | TVF | Table | Returns person info (name, job title, business entity type) from multiple schemas |
| `dbo.ufnGetDocumentStatusText(@Status)` | Scalar | `nvarchar(16)` | Converts status tinyint to text (0=Pending Approval, 1=Approved, 2=Obsolete) |
| `dbo.ufnGetProductDealerPrice(@ProductID, @OrderDate)` | Scalar | `money` | Returns the dealer price for a product on an order date |
| `dbo.ufnGetProductListPrice(@ProductID, @OrderDate)` | Scalar | `money` | Returns the list price for a product on a given date from price history |
| `dbo.ufnGetProductStandardCost(@ProductID, @OrderDate)` | Scalar | `money` | Returns the standard cost for a product on a given date from cost history |
| `dbo.ufnGetPurchaseOrderStatusText(@Status)` | Scalar | `nvarchar(15)` | Converts PO status tinyint to text (1=Pending, 2=Approved, 3=Rejected, 4=Complete) |
| `dbo.ufnGetSalesOrderStatusText(@Status)` | Scalar | `nvarchar(15)` | Converts SO status tinyint to text (1=In process, 2=Approved, 3=Backordered, 4=Rejected, 5=Shipped, 6=Cancelled) |
| `dbo.ufnGetStock(@ProductID)` | Scalar | `int` | Returns current total stock quantity across all locations for a product |
| `dbo.ufnLeadingZeros(@Value)` | Scalar | `varchar(8)` | Zero-pads an integer to 8 characters (used in computed columns like `SalesOrderNumber`) |

---

## 8) Business Scenarios (What to Demo & Why)

### A. Sales & Marketing

**Internet vs. Reseller Channel Analysis**
- Compare `OnlineOrderFlag=1` (Internet) vs `=0` (Reseller) orders in `Sales.SalesOrderHeader`.
- OLTP data maps directly to `FactInternetSales` and `FactResellerSales` in the DW.
- Use cases: channel profitability, average order value, order frequency by channel.

**Customer Segmentation**
- `Sales.vPersonDemographics` exposes XML-shredded data: income bands, education, occupation, commute distance, buying group.
- Use for: RFM analysis, demographic targeting, cohort analysis.
- DW: `DimCustomer` has `CommuteDistance`, `EnglishEducation`, `EnglishOccupation`, `YearlyIncome`, `TotalChildren`, `HouseOwnerFlag`, `NumberCarsOwned` for OLAP slicing.

**Sales Reason / Campaign Attribution**
- `Sales.SalesOrderHeaderSalesReason` is a many-to-many bridge between orders and reasons.
- Demonstrates M2M relationship modeling in both OLTP (bridge table) and DW (`FactInternetSalesReason` bridge fact).
- In the SSAS cube, this is the canonical **many-to-many dimension relationship** tutorial example.

**Territory Performance**
- 10 territories with YTD/LY comparison columns in `Sales.SalesTerritory`.
- `Sales.vSalesPersonSalesByFiscalYears` is a PIVOT demo showing rep × year matrix.

**Promotions Effectiveness**
- `Sales.SpecialOffer` + `Sales.SpecialOfferProduct` + `Sales.SalesOrderDetail` join chain.
- DW: `DimPromotion` dimension with `FactInternetSales`.

---

### B. Product & Catalog Management

**Product Hierarchy**
- 4 categories → 37 subcategories → 504 products → product models → multilingual descriptions.
- `Production.ProductCategory` → `Production.ProductSubcategory` → `Production.Product` → `Production.ProductModel` → `Production.ProductModelProductDescriptionCulture` → `Production.ProductDescription` (by culture).
- DW: `DimProductCategory` → `DimProductSubcategory` → `DimProduct` (flattened hierarchy).

**Price and Cost History**
- `Production.ProductListPriceHistory` and `Production.ProductCostHistory` are canonical SCD Type 2 source tables.
- Use for: margin trend analysis, effective price/cost lookup (point-in-time queries), ETL SCD demos.
- UDFs `ufnGetProductListPrice` and `ufnGetProductStandardCost` encapsulate the date-effective lookup logic.

**Multilingual Catalog**
- `Production.Culture` has 6 languages; `Production.ProductModelProductDescriptionCulture` is the junction.
- SSAS: demonstrates the `Translations` feature at dimension member and caption level.

**Bill of Materials (BOM)**
- `Production.BillOfMaterials` is a self-referencing table with BOMLevel and PerAssemblyQty.
- `dbo.uspGetBillOfMaterials` and `dbo.uspGetWhereUsedProductID` use recursive CTEs.
- Use for: T-SQL recursion teaching, manufacturing cost roll-up, where-used analysis.

---

### C. Purchasing & Vendor Management

**Procure-to-Pay Pipeline**
- `Purchasing.Vendor` → `Purchasing.ProductVendor` → `Purchasing.PurchaseOrderHeader` → `Purchasing.PurchaseOrderDetail`.
- Reports: vendor spend analysis, preferred vs. non-preferred vendor comparison, lead time analysis.
- `PurchaseOrderHeader.Status` enum (1–4) demonstrates status-tracking pattern.

**Multi-Vendor Sourcing**
- `Purchasing.ProductVendor` is a many-to-many bridge: one product can have multiple vendors, each with their own price and lead time.
- Use for: procurement analytics, vendor benchmarking, supply risk analysis.

---

### D. Manufacturing & Inventory

**Work Order Lifecycle**
- `Production.WorkOrder` → `Production.WorkOrderRouting` (by location/operation sequence).
- ScrapReasonID joins to `Production.ScrapReason` for quality reporting.
- Dates: ScheduledStart/End vs. ActualStart/End for on-time delivery analysis.

**Inventory Snapshot**
- `Production.ProductInventory` tracks Quantity by Product × Location × Shelf/Bin.
- DW: `FactProductInventory` is a periodic snapshot fact table — different grain from transaction facts.
- `dbo.ufnGetStock` aggregates inventory across locations for a product.

**Transaction History**
- `Production.TransactionHistory` records all inventory movements (P=Purchase, S=Sale, W=Work Order).
- `Production.TransactionHistoryArchive` is the same schema — used for partitioning, archiving, and data lifecycle demos.

---

### E. Human Resources

**Organizational Hierarchy**
- `HumanResources.Employee.OrganizationNode` is `hierarchyid` — the go-to teaching demo for this data type.
- `dbo.uspGetEmployeeManagers` and `dbo.uspGetManagerEmployees` traverse the tree.
- Report uses: org chart visualization, span-of-control analysis, roll-up reporting by level.

**HR History / SCD**
- `HumanResources.EmployeeDepartmentHistory` and `HumanResources.EmployeePayHistory` are natural SCD Type 2 source tables.
- Use for: as-of queries, point-in-time HR reporting, ETL SCD processing demos.

**Unstructured Data (XML Resumes)**
- `HumanResources.JobCandidate.Resume` is `xml` — demonstrates XML indexing, `value()`, `exist()`, `nodes()`.
- `HumanResources.vJobCandidateEducation` and `vJobCandidateEmployment` are pre-built XML-shredding views.
- `dbo.uspSearchCandidateResumes` demonstrates full-text search over XML.

---

## 9) OLAP, DW & Analysis Services — Deep Dive

### A. ETL / OLTP → DW Mapping (Complete Cheat Sheet)

| DW Object | Source OLTP Tables | Key Transform Notes |
|---|---|---|
| `DimCustomer` | `Sales.Customer`, `Person.Person`, `Sales.vPersonDemographics`, `Person.Address`, `Sales.SalesTerritory` | Demographics XML is shredded; SCD Type 1 (overwrites) |
| `DimDate` | Generated date spine (no OLTP source) | 14+ date attributes computed; fiscal year July–June; used by all fact tables |
| `DimEmployee` | `HumanResources.Employee`, `Person.Person`, `HumanResources.Department` | SalesPerson subset also feeds SalesPerson dim in cube |
| `DimGeography` | `Person.Address`, `Person.StateProvince`, `Person.CountryRegion`, `Sales.SalesTerritory` | Hierarchy: City→State→Country→Territory |
| `DimOrganization` | `HumanResources.Department`, `HumanResources.EmployeeDepartmentHistory` | Parent-child hierarchy for finance |
| `DimProduct` | `Production.Product`, `Production.ProductSubcategory`, `Production.ProductCategory`, `Production.ProductModel`, `Production.ProductDescription` | Flattened hierarchy; English description only by default |
| `DimProductCategory` | `Production.ProductCategory` | Lookup |
| `DimProductSubcategory` | `Production.ProductSubcategory` | Lookup |
| `DimPromotion` | `Sales.SpecialOffer` | Includes No Discount as default member |
| `DimReseller` | `Sales.Store`, `Person.BusinessEntity`, `Person.Address` | Store-type customers only |
| `DimSalesReason` | `Sales.SalesReason` | Lookup |
| `DimSalesTerritory` | `Sales.SalesTerritory` | 10 territories + NA for unassigned |
| `DimScenario` | Hard-coded: Actual, Budget, Forecast | — |
| `FactInternetSales` | `Sales.SalesOrderHeader` (OnlineOrderFlag=1), `Sales.SalesOrderDetail`, with lookups to multiple dims | Degenerate dims: SalesOrderNumber, SalesOrderLineNumber; surrogate key lookups via ETL |
| `FactInternetSalesReason` | `Sales.SalesOrderHeaderSalesReason`, `Sales.SalesOrderDetail` | Bridge fact resolving M2M between FactInternetSales and DimSalesReason |
| `FactResellerSales` | `Sales.SalesOrderHeader` (OnlineOrderFlag=0), `Sales.SalesOrderDetail` | Same as InternetSales but joins to DimReseller instead of DimCustomer |
| `FactSalesQuota` | `Sales.SalesPersonQuotaHistory` | Quarterly grain; requires date rollup from order-level to quarter-level |
| `FactFinance` | Derived from `HumanResources` budget data | Finance scenario data; requires Scenario, Organization, Account dimensions |
| `FactCallCenter` | Synthetic/derived | Models a call center with shift-level data |
| `FactCurrencyRate` | `Sales.CurrencyRate` | Daily exchange rates for multi-currency analysis |
| `FactProductInventory` | `Production.ProductInventory`, `Production.TransactionHistory` | Periodic snapshot grain |
| `FactSurveyResponse` | Synthetic customer survey data | Demographic opinion data for market basket/segmentation demos |

---

### B. SSAS Multidimensional Cube — Detail

**Cube Name:** `Adventure Works` (and sub-cubes via Perspectives)

**Measure Groups and Key Measures:**

| Measure Group | Key Measures | Primary Fact Table |
|---|---|---|
| Internet Sales | Sales Amount, Order Quantity, Extended Amount, Discount Amount, Unit Price, Total Product Cost, Tax Amount, Freight | `FactInternetSales` |
| Reseller Sales | Sales Amount, Order Quantity, Extended Amount, Discount Amount, Unit Price, Total Product Cost, Tax Amount, Freight | `FactResellerSales` |
| Sales Quotas | Sales Amount Quota | `FactSalesQuota` |
| Exchange Rates | Average Rate, End of Day Rate | `FactCurrencyRate` |
| Sales Reasons | (bridge; no standalone measures) | `FactInternetSalesReason` |
| Financial Reporting | Amount | `FactFinance` |
| Internet Customers | Distinct Count of Internet Customers | `FactInternetSales` |
| Internet Orders | Distinct Count of Internet Orders | `FactInternetSales` |
| Reseller Orders | Distinct Count of Reseller Orders | `FactResellerSales` |
| Call Center | Calls, Orders, Automatic Responses | `FactCallCenter` |
| Inventory | Units Balance, Unit Cost | `FactProductInventory` |

**Calculated Measures (MDX, selected examples):**
- `[Measures].[Internet Gross Profit]` = `[Internet Revenue] - [Internet Total Product Cost]`
- `[Measures].[Internet Gross Profit Margin]` = `[Internet Gross Profit] / [Internet Revenue]`
- `[Measures].[Reseller Gross Profit]` = `[Reseller Revenue] - [Reseller Total Product Cost]`
- `[Measures].[Total Sales Amount]` = `[Internet Sales Amount] + [Reseller Sales Amount]`
- Various time intelligence: YTD, LY, YOY growth, rolling 12-month, prior period comparisons

**Dimensions in the Cube:**
- `Customer` (hierarchy: Country → State-Province → City → Postal Code → Customer)
- `Date` (hierarchies: Calendar (Year→Semester→Quarter→Month→Date), Fiscal (Year→Semester→Quarter→Month→Date), Calendar Week (Year→Week), ISO Week (Year→Week))
- `Delivery Date` (role-playing dimension from DimDate)
- `Due Date` (role-playing dimension from DimDate)
- `Employee` (hierarchy: Employees (org tree via parent-child))
- `Geography` (hierarchy: Country → State-Province → City → Postal Code)
- `Internet Sales Order Details` (degenerate dimension)
- `Organization` (parent-child hierarchy for finance scenarios)
- `Product` (hierarchies: Product Categories → Subcategories → Products, Product Model Lines (by ProductLine code))
- `Promotion` (hierarchy: Promotion Category → Promotion)
- `Reseller` (hierarchy: Reseller Type → Reseller)
- `Reseller Sales Order Details` (degenerate dimension)
- `Sales Channel` (Internet vs. Reseller)
- `Sales Reason` (hierarchy: Sales Reason Type → Sales Reason)
- `Sales Summary Order Details` (degenerate dimension)
| `Sales Territory` (hierarchy: Country Group → Country → Region)
- `Scenario` (Actual, Budget, Forecast — for finance)
- `Ship Date` (role-playing dimension from DimDate)
- `Source Currency` (for exchange rate scenarios)

**KPIs (Key Performance Indicators):**
- Revenue (with goal, status, and trend indicators)
- Growth in Customer Base
- Product Gross Profit Margin
- Financial Efficiency

**Actions:**
- Drillthrough to detail rows
- URL actions (e.g., launch product page)
- Report actions (launch SSRS reports from cube browsing)

**Perspectives:**
- `Channel Sales` — Internet Sales + Reseller Sales combined view
- `Direct Sales` — Internet-only subset
- `Finance` — Finance reporting measure group focus
- `Sales Summary` — Simplified top-level view for management
- `Warehouse` — Inventory and procurement focus

**Translations:** Dimension captions and member names translated to multiple languages — teaches the SSAS Translations feature.

---

### C. SSAS Tabular Model

**Model Name:** `AdventureWorks Tabular Model SQL 2012` (varies by version)
**Compatibility Level:** 1200 (SQL Server 2016+)
**Source:** `AdventureWorksDW`

**Tables imported (selected):**
- `DimCustomer`, `DimDate`, `DimEmployee`, `DimGeography`, `DimProduct`, `DimProductCategory`, `DimProductSubcategory`, `DimPromotion`, `DimReseller`, `DimSalesReason`, `DimSalesTerritory`
- `FactInternetSales`, `FactInternetSalesReason`, `FactResellerSales`, `FactSalesQuota`

**DAX Measures (selected):**
- `Internet Total Sales := SUM(FactInternetSales[SalesAmount])`
- `Reseller Total Sales := SUM(FactResellerSales[SalesAmount])`
- `Total Sales := [Internet Total Sales] + [Reseller Total Sales]`
- `Internet Previous Year Sales := CALCULATE([Internet Total Sales], PREVIOUSYEAR('DimDate'[FullDateAlternateKey]))`
- `Internet Year Over Year Growth := ([Internet Total Sales] - [Internet Previous Year Sales]) / [Internet Previous Year Sales]`
- `Internet Gross Profit := [Internet Total Sales] - SUM(FactInternetSales[TotalProductCost])`

**Row-Level Security Roles:** Defined by sales territory; demonstrates DAX-based RLS.

---

### D. Data Mining (Historic — SQL Server 2005–2017)

These labs are available in documentation up through SQL Server 2017 and use `AdventureWorksDW` as the source:

| Mining Scenario | Algorithm | Business Question |
|---|---|---|
| Targeted Mailing | Decision Trees / Naïve Bayes | Which customers are likely bike buyers? |
| Market Basket | Association Rules | Which products are bought together? |
| Forecasting | Time Series (ARIMA/ARTXP) | Predict future sales amounts |
| Sequence Clustering | Sequence Clustering | What purchase sequences lead to repeat buying? |
| Customer Profiling | Clustering | Identify natural customer segments |

> **Note:** SQL Server Data Mining is deprecated as of SQL Server 2017 (announced for removal). Azure Machine Learning or Synapse Analytics with Python/R are the current replacement path.

---

## 10) Reporting — SSRS

### A. Classic Sample Report Set

The historic AdventureWorks SSRS sample reports (shipped with SQL Server 2005–2012) include:

| Report Name | Type | Data Source | Key Features |
|---|---|---|---|
| Company Sales | Matrix/Chart | `AdventureWorksDW` OLAP | Year-over-year sales by product category and territory; MDX-based |
| Employee Sales Summary | Tablix with Grouping | `AdventureWorksDW` | Sales by territory and sales person; drill-down |
| Product Catalog | Subreport | `AdventureWorks` OLTP | Category → Subcategory → Product listing with images |
| Product Line Sales | Chart | `AdventureWorksDW` | Stacked bar by product line |
| Sales Order Detail | Tablix | `AdventureWorks` OLTP | Single order detail; parameterized by SalesOrderID |
| Sales Reason Comparisons | Matrix | `AdventureWorksDW` | Multi-select parameter for sales reasons |
| Store Contacts | Tablix | `AdventureWorks` OLTP | Store listing with contacts; demonstrates subreports |
| Territory Sales Drilldown | Matrix with Drillthrough | `AdventureWorksDW` | Territory → salesperson drillthrough; OLAP source |

### B. Report Techniques Demonstrated
- **Parameters:** Single-select, multi-select, cascading parameters
- **Drillthrough:** From summary matrix to detail report
- **Drill-down:** Expand/collapse row groups inline
- **Subreports:** Embedded child reports
- **Chart types:** Bar, column, pie, line, combination
- **Data sources:** Relational T-SQL and OLAP MDX in the same report set
- **Shared datasets:** Reusable queries across reports
- **Report Server Catalog reports:** System reports showing deployed item metadata

### C. Community/Modern Versions
- `AdventureWorks2017` SSRS report solution available at community repositories (sqlpowered.com).
- Power BI Desktop can connect to AdventureWorksDW natively for equivalent visualizations.

---

## 11) Installation & Setup (Complete Reference)

### A. Restore from Backup (Recommended)

```sql
USE [master];
GO
RESTORE DATABASE [AdventureWorks2022]
FROM DISK = N'C:\Program Files\Microsoft SQL Server\MSSQL16.MSSQLSERVER\MSSQL\Backup\AdventureWorks2022.bak'
WITH FILE = 1, NOUNLOAD, STATS = 5;
GO
-- Optionally update compatibility level for the version you are running:
-- ALTER DATABASE AdventureWorks2022 SET COMPATIBILITY_LEVEL = 160; -- SQL Server 2022
-- ALTER DATABASE AdventureWorks2022 SET COMPATIBILITY_LEVEL = 170; -- SQL Server 2025
```

**Default backup path patterns:**
- SQL Server 2022: `C:\Program Files\Microsoft SQL Server\MSSQL16.MSSQLSERVER\MSSQL\Backup\`
- SQL Server 2025: `C:\Program Files\Microsoft SQL Server\MSSQL17.MSSQLSERVER\MSSQL\Backup\`

### B. Install from Scripts (GitHub)

Installs at the current instance compatibility level — preferred for SQL Server 2025 demos.

```powershell
# Download oltp-install-script.zip from GitHub releases and extract
# Set SqlSamplesSourceDataPath to extracted CSV folder
# Run instawdb.sql via SQLCMD:
sqlcmd -S . -i instawdb.sql
```

### C. Azure SQL Database (AdventureWorksLT)

1. Go to `aka.ms/azuresqlhub` → Create Azure SQL Database
2. On **Additional settings** tab → **Data source: Sample**
3. The portal automatically creates `AdventureWorksLT`
4. Alternatively: restore an OLTP `.bak` to Azure SQL Managed Instance or use SSMS's "Deploy Database to Azure SQL" wizard

### D. Microsoft Fabric SQL Database (AdventureWorksLT)

1. Create a new SQL database in Fabric workspace
2. On the database home page → **Sample Data** button
3. The `SalesLT` schema is loaded automatically

### E. SSAS Cubes (.abf Restore)

```
-- In SSMS connected to Analysis Services instance:
-- Right-click Databases → Restore... → Browse to .abf file
-- Or use PowerShell:
Restore-ASDatabase -restorefile "adventure-works-multidimensional-model-full.abf" `
  -name "Adventure Works DW" -Server "localhost"
```

### F. Docker / Container

```bash
docker run -e "ACCEPT_EULA=Y" -e "SA_PASSWORD=YourStrong!Passw0rd" \
  -p 1433:1433 --name sql2022 \
  -d mcr.microsoft.com/mssql/server:2022-latest

# Copy .bak into container and restore:
docker cp AdventureWorks2022.bak sql2022:/var/opt/mssql/backup/
docker exec -it sql2022 /opt/mssql-tools/bin/sqlcmd -S localhost -U SA -P 'YourStrong!Passw0rd' \
  -Q "RESTORE DATABASE [AdventureWorks] FROM DISK='/var/opt/mssql/backup/AdventureWorks2022.bak' \
      WITH MOVE 'AdventureWorks2017' TO '/var/opt/mssql/data/AdventureWorks.mdf', \
           MOVE 'AdventureWorks2017_log' TO '/var/opt/mssql/data/AdventureWorks_log.ldf'"
```

### G. Version Compatibility Level Reference

| Database Name | Default Compat Level | SQL Server Version |
|---|---|---|
| AdventureWorks2008R2 | 100 | SQL Server 2008 R2 |
| AdventureWorks2012 | 110 | SQL Server 2012 |
| AdventureWorks2014 | 120 | SQL Server 2014 |
| AdventureWorks2016 | 130 | SQL Server 2016 |
| AdventureWorks2017 | 140 | SQL Server 2017 |
| AdventureWorks2019 | 150 | SQL Server 2019 |
| AdventureWorks2022 | 160 | SQL Server 2022 |
| AdventureWorks2025 | 170 | SQL Server 2025 |

---

## 12) Governance, Patterns & Teaching Notes

### A. Audit & Error Logging Pattern
- `dbo.DatabaseLog` captures DDL changes via trigger `ddlDatabaseTriggerLog` — demos on change auditing.
- `dbo.ErrorLog` is populated by `dbo.uspLogError` inside CATCH blocks — the canonical TRY/CATCH demo.
- Teaching point: always instrument production code with both patterns.

### B. User-Defined Types (UDTs) as Data Quality Contracts
- `AccountNumber`, `OrderNumber`, `Flag`, `Name`, `NameStyle`, `Phone` are defined once and reused across schemas.
- Teaching point: UDTs enforce domain constraints at the type level, not just table level; changes propagate automatically.
- Governance discussion: UDTs add migration complexity (ALTER requires type recreation + column rebuild) — a real trade-off.

### C. Binary and XML Data Governance
- `Production.ProductPhoto` stores images as `varbinary(max)` — leads to discussions about externalization to blob storage vs. in-database storage.
- `Production.Document` is FILESTREAM-backed in the 2025 release — demonstrates the FILESTREAM governance model.
- `HumanResources.JobCandidate.Resume` and `Production.ProductModel.Instructions` are `xml` typed — demonstrates XML schema collection, indexing (`PRIMARY XML INDEX`, `SECONDARY XML INDEX`), and query patterns.
- `Sales.Store.Demographics` and `Person.Person.Demographics` are `xml` typed — unstructured demographic data.

### D. Computed Columns
- `SalesOrderHeader.SalesOrderNumber` = `dbo.ufnLeadingZeros(SalesOrderID)` — surrogate-key-to-business-key pattern.
- `SalesOrderHeader.TotalDue` = `SubTotal + TaxAmt + Freight` — persistence and indexability discussion.
- `HumanResources.Employee.OrganizationLevel` = `OrganizationNode.GetLevel()` — hierarchyid method demo.
- `PurchaseOrderHeader.TotalDue` = `SubTotal + TaxAmt + Freight`

### E. Row GUID Columns
- Most tables include a `rowguid uniqueidentifier ROWGUIDCOL DEFAULT NEWSEQUENTIALID()` column — supports replication, merge replication, and change data capture demos.
- Teaching point: NEWSEQUENTIALID() avoids page fragmentation vs. NEWID().

### F. 2016 Feature Hooks (`_EXT` variant)
- **Row-Level Security (RLS):** Sales data filtered by TerritoryID based on login.
- **Dynamic Data Masking (DDM):** Credit card numbers and personal data masked for non-privileged users.
- **Temporal Tables:** `Sales.SalesOrderHeader` converted to system-versioned temporal with history table.
- **JSON:** Order data serializable/deserializable with `FOR JSON` / `OPENJSON`.
- **Stretch Database (deprecated):** Cold transaction history stretched to Azure — architecture discussion.

### G. SQL Server 2025 Feature Hooks
- **FILESTREAM storage:** `Production.Document` uses FILESTREAM for large binary document files.
- **Compatibility level 170:** Required for new T-SQL functions (e.g., `REGEXP_LIKE`).
- **Query Store enabled by default:** Immediate plan capture on install.
- **Accelerated Database Recovery (ADR):** Enabled by default — faster recovery demos.
- **Optimized Locking:** Enabled by default — concurrency improvement demos.

---

## 13) Example Queries

> **Tip:** Substitute `AdventureWorks` for your versioned name (e.g., `AdventureWorks2022`). Use `USE AdventureWorks2022; GO` before all queries.

### A) Recursive BOM — All Levels for a Parent Product

```sql
-- Find all components (at all levels) for a given top-level assembly
DECLARE @AssemblyID int = 749; -- Road-150 Red, 62

WITH Parts AS (
    SELECT b.ProductAssemblyID, b.ComponentID, b.PerAssemblyQty,
           b.EndDate, 0 AS ComponentLevel
    FROM Production.BillOfMaterials AS b
    WHERE b.ProductAssemblyID = @AssemblyID AND b.EndDate IS NULL
    UNION ALL
    SELECT bom.ProductAssemblyID, bom.ComponentID, p.PerAssemblyQty,
           bom.EndDate, ComponentLevel + 1
    FROM Production.BillOfMaterials AS bom
    JOIN Parts AS p ON bom.ProductAssemblyID = p.ComponentID
    WHERE bom.EndDate IS NULL
)
SELECT p.ComponentLevel, pr.Name AS ComponentName,
       p.ComponentID, p.PerAssemblyQty
FROM Parts AS p
JOIN Production.Product AS pr ON p.ComponentID = pr.ProductID
ORDER BY p.ComponentLevel, pr.Name;
```

### B) Internet vs. Reseller Sales by Fiscal Year

```sql
-- Fiscal year starts July 1; compare channels by year
SELECT
    CASE WHEN MONTH(soh.OrderDate) >= 7
         THEN YEAR(soh.OrderDate)
         ELSE YEAR(soh.OrderDate) - 1
    END AS FiscalYear,
    SUM(CASE WHEN soh.OnlineOrderFlag = 1 THEN sod.LineTotal ELSE 0 END)
        AS InternetSales,
    SUM(CASE WHEN soh.OnlineOrderFlag = 0 THEN sod.LineTotal ELSE 0 END)
        AS ResellerSales,
    COUNT(DISTINCT CASE WHEN soh.OnlineOrderFlag = 1
                        THEN soh.SalesOrderID END)
        AS InternetOrders,
    COUNT(DISTINCT CASE WHEN soh.OnlineOrderFlag = 0
                        THEN soh.SalesOrderID END)
        AS ResellerOrders
FROM Sales.SalesOrderHeader AS soh
JOIN Sales.SalesOrderDetail  AS sod ON soh.SalesOrderID = sod.SalesOrderID
GROUP BY
    CASE WHEN MONTH(soh.OrderDate) >= 7
         THEN YEAR(soh.OrderDate)
         ELSE YEAR(soh.OrderDate) - 1
    END
ORDER BY FiscalYear;
```

### C) Vendor Cost Benchmark with Window Functions

```sql
-- Vendor spend with rank by total purchase amount
SELECT
    v.Name                           AS Vendor,
    v.CreditRating,
    SUM(poh.TotalDue)                AS TotalPurchase,
    AVG(poh.TotalDue)                AS AvgPurchase,
    COUNT(poh.PurchaseOrderID)       AS OrderCount,
    RANK() OVER (ORDER BY SUM(poh.TotalDue) DESC)
                                     AS SpendRank
FROM Purchasing.Vendor AS v
JOIN Purchasing.PurchaseOrderHeader AS poh ON v.BusinessEntityID = poh.VendorID
GROUP BY v.Name, v.CreditRating
ORDER BY TotalPurchase DESC;
```

### D) Product Catalog Hierarchy with Price/Cost

```sql
SELECT
    pc.Name   AS Category,
    psc.Name  AS Subcategory,
    pm.Name   AS Model,
    p.Name    AS Product,
    p.ProductNumber,
    p.Color,
    p.ListPrice,
    p.StandardCost,
    CAST(p.ListPrice - p.StandardCost AS decimal(10,2)) AS GrossMargin,
    CAST(CASE WHEN p.ListPrice > 0
              THEN (p.ListPrice - p.StandardCost) / p.ListPrice * 100
              ELSE NULL END AS decimal(5,2))             AS MarginPct
FROM Production.Product AS p
LEFT JOIN Production.ProductSubcategory AS psc
    ON psc.ProductSubcategoryID = p.ProductSubcategoryID
LEFT JOIN Production.ProductCategory AS pc
    ON pc.ProductCategoryID = psc.ProductCategoryID
LEFT JOIN Production.ProductModel AS pm
    ON pm.ProductModelID = p.ProductModelID
WHERE p.FinishedGoodsFlag = 1
ORDER BY pc.Name, psc.Name, pm.Name, p.Name;
```

### E) Employee Org Chart with HierarchyID

```sql
-- All employees under a given manager (including indirect reports)
DECLARE @ManagerID int = 6; -- David Bradley, Marketing Manager example

SELECT
    e2.LoginID,
    p.FirstName + ' ' + p.LastName AS EmployeeName,
    e2.JobTitle,
    e2.OrganizationNode.ToString()  AS OrgPath,
    e2.OrganizationLevel
FROM HumanResources.Employee AS e1
JOIN HumanResources.Employee AS e2
    ON e2.OrganizationNode.IsDescendantOf(e1.OrganizationNode) = 1
JOIN Person.Person AS p
    ON p.BusinessEntityID = e2.BusinessEntityID
WHERE e1.BusinessEntityID = @ManagerID
  AND e2.BusinessEntityID <> e1.BusinessEntityID
ORDER BY e2.OrganizationNode;
```

### F) SalesLT — Customer with Orders (AdventureWorksLT)

```sql
-- For use in AdventureWorksLT / Azure SQL / Fabric
SELECT
    c.CustomerID,
    c.FirstName + ' ' + c.LastName AS Customer,
    c.CompanyName,
    COUNT(soh.SalesOrderID)         AS OrderCount,
    SUM(soh.TotalDue)               AS TotalRevenue,
    MAX(soh.OrderDate)              AS LastOrderDate
FROM SalesLT.Customer AS c
LEFT JOIN SalesLT.SalesOrderHeader AS soh ON c.CustomerID = soh.CustomerID
GROUP BY c.CustomerID, c.FirstName, c.LastName, c.CompanyName
ORDER BY TotalRevenue DESC;
```

### G) DW — Top Products by Internet Sales (AdventureWorksDW)

```sql
-- Use in AdventureWorksDW
SELECT TOP 20
    dp.EnglishProductName                       AS Product,
    dpc.EnglishProductCategoryName              AS Category,
    dpsc.EnglishProductSubcategoryName          AS Subcategory,
    SUM(f.SalesAmount)                          AS TotalSales,
    SUM(f.OrderQuantity)                        AS TotalUnits,
    SUM(f.SalesAmount) / NULLIF(SUM(f.OrderQuantity), 0) AS AvgUnitPrice,
    SUM(f.SalesAmount - f.TotalProductCost)     AS GrossProfit
FROM dbo.FactInternetSales AS f
JOIN dbo.DimProduct AS dp ON f.ProductKey = dp.ProductKey
LEFT JOIN dbo.DimProductSubcategory AS dpsc
    ON dp.ProductSubcategoryKey = dpsc.ProductSubcategoryKey
LEFT JOIN dbo.DimProductCategory AS dpc
    ON dpsc.ProductCategoryKey = dpc.ProductCategoryKey
GROUP BY dp.EnglishProductName, dpc.EnglishProductCategoryName,
         dpsc.EnglishProductSubcategoryName
ORDER BY TotalSales DESC;
```

### H) MDX — Internet Sales by Territory and Year

```mdx
-- Execute against Adventure Works SSAS Multidimensional cube
SELECT
  NON EMPTY
    { [Measures].[Internet Sales Amount],
      [Measures].[Internet Order Count],
      [Measures].[Internet Gross Profit Margin] }
  ON COLUMNS,
  NON EMPTY
    { [Sales Territory].[Sales Territory Group].[Sales Territory Group].MEMBERS }
  * { [Date].[Calendar Year].[Calendar Year].MEMBERS }
  ON ROWS
FROM [Adventure Works]
WHERE ([Sales Channel].[Sales Channel].&[Internet])
```

### I) Query Store Plan Forcing Demo (SQL Server 2016+)

```sql
-- Capture queries in Query Store
ALTER DATABASE AdventureWorks2022 SET QUERY_STORE = ON;
ALTER DATABASE AdventureWorks2022 SET QUERY_STORE CLEAR;

-- Find top regressed queries
SELECT TOP 10
    q.query_id,
    qt.query_sql_text,
    rs.avg_duration       AS avg_duration_microseconds,
    rs.count_executions,
    p.plan_id
FROM sys.query_store_query AS q
JOIN sys.query_store_query_text AS qt
    ON q.query_text_id = qt.query_text_id
JOIN sys.query_store_plan AS p ON q.query_id = p.query_id
JOIN sys.query_store_runtime_stats AS rs ON p.plan_id = rs.plan_id
ORDER BY rs.avg_duration DESC;

-- Force a plan (replace IDs with actual values from above)
EXEC sys.sp_query_store_force_plan @query_id = 42, @plan_id = 100;
```

### J) In-Memory OLTP — Verify Memory-Optimized Objects

```sql
-- After loading the In-Memory OLTP sample database
SELECT name, type_desc, durability_desc
FROM sys.tables
WHERE is_memory_optimized = 1
ORDER BY name;

-- Check native stored procedures
SELECT name, type_desc
FROM sys.objects
WHERE type = 'PC'  -- PC = CLR/native compiled procedure
ORDER BY name;
```

---

## 14) Performance & Indexing Teaching Points

### A. Clustered Index Patterns
- Most tables use an integer surrogate PK as the clustered index — optimal for DW lookups.
- `HumanResources.Employee.OrganizationNode` (hierarchyid) is an interesting alternative for depth-first traversal.
- Composite PK tables (junction tables like `Sales.SalesOrderHeaderSalesReason`) have composite clustered indexes.

### B. Common Non-Clustered Index Patterns
- Foreign key columns are generally **not** automatically indexed — a deliberate teaching gap: demonstrate the value of FK indexes on `Sales.SalesOrderDetail.ProductID`, etc.
- Filtered indexes: Demonstrate with `Production.Product` WHERE `FinishedGoodsFlag=1` or `SellEndDate IS NULL`.
- Covering indexes: Demonstrate on `Sales.SalesOrderHeader` for date-range + territory queries.
- Columnstore indexes: Demonstrate on `Production.TransactionHistory` or `Sales.SalesOrderDetail` for aggregation queries.

### C. Partitioning Candidates
- `Sales.SalesOrderHeader` partitioned by `OrderDate` year — range partitioning demo.
- `Production.TransactionHistory` → `Production.TransactionHistoryArchive` swap demo using partition switching.

### D. Statistics
- Use AdventureWorks with auto-update statistics disabled to demonstrate stale stats and plan degradation.
- Query Store makes this very visible in 2016+.

---

## 15) Version History & Schema Changes

| SQL Server Version | Key Changes to AdventureWorks |
|---|---|
| 2005 | Original release. `Person.Contact` table; `Sales.Individual` and `Sales.StoreContact` exist; ~70 DML triggers; no `BusinessEntity` abstraction |
| 2008 | Minor refinements; moved to CodePlex download |
| 2008 R2 | Minimal changes; first version on current download path |
| 2012 | **Major refactor**: `Person.Contact` → `Person.Person`; `Person.BusinessEntity` added as root; `Sales.Individual` removed; trigger count reduced to 1 DDL trigger; `Person.PersonPhone`, `Person.EmailAddress` normalized; schema is now stable through 2022 |
| 2014 | Name-only change (AdventureWorks2014); compat level 120 |
| 2016 | Name change + compat 130; **2016_EXT** variant adds temporal tables, RLS, DDM, JSON, Stretch |
| 2017 | Name change + compat 140; no schema changes |
| 2019 | Name change + compat 150; no schema changes |
| 2022 | Name change + compat 160; no schema changes |
| 2025 | **FILESTREAM added** to `Production.Document`; compat 170; enables Query Store/ADR/Optimized Locking by default; install script creates at current instance compat level |

---

## 16) Cross-References (Teach with Contrasts)

| Sample DB | Introduced | Design Philosophy | Best Use |
|---|---|---|---|
| **pubs** | SQL Server 6.5 | Simple, small (books/authors/titles); no schemas | Legacy training only |
| **Northwind** | SQL Server 7.0 | Small (orders/products); no schemas | Legacy training only; AdventureWorks is the replacement |
| **AdventureWorks OLTP** | SQL Server 2005 | Complex, multi-schema, realistic enterprise OLTP | T-SQL training, schema design, indexing, XML, hierarchies |
| **AdventureWorksDW** | SQL Server 2005 | Star schema, Kimball-style DW | SSAS modeling, SSRS, DW design, ETL demos |
| **AdventureWorksLT** | SQL Server 2005 | Simplified, denormalized; Azure-friendly | Azure quickstarts, beginner SQL, app development |
| **WideWorldImporters** | SQL Server 2016 | Modern feature showcase: temporal, JSON, spatial, columnstore, In-Memory | SQL Server 2016+ feature demos; more current than AdventureWorks |
| **WideWorldImportersDW** | SQL Server 2016 | Modern DW with columnstore | Modern DW with 2016+ engine features |

> **Migration note:** The original documentation for AdventureWorks (SQL Server 2005) explicitly includes "AdventureWorks to Northwind Table Comparison" and "AdventureWorks to pubs Table Comparison" cross-reference documents in the SQL Server 2008 Books Online, helping instructors migrating from legacy samples.

---

## 17) Questions for Copilot (Prompt Library)

Use these verbatim or adapt as needed:

1. **"Enumerate all objects that store XML or varbinary(max) and propose governance (indexing, retention, externalization) trade-offs."**
2. **"Produce a complete OLTP→DW mapping table for Internet/Reseller Sales with source columns, target columns, keys, degenerate dims, and SCD treatment."**
3. **"Design a set of SSRS reports (matrix, tablix, drillthrough) using Sales and Production — include dataset queries and parameters."**
4. **"Walk me through building a Multidimensional SSAS cube on AdventureWorksDW step-by-step, including a many-to-many relationship for Sales Reasons and a KPI for Gross Profit Margin."**
5. **"Set up an Azure SQL DB with AdventureWorksLT and expose it via Data API builder (REST + GraphQL endpoints for Customer and SalesOrderHeader)."**
6. **"Demonstrate Query Store insights on AdventureWorks2022: capture, identify regressed plans, compare plans, and force a plan."**
7. **"Run the In-Memory OLTP sample workload on AdventureWorks and chart throughput vs. disk-based tables using DMVs."**
8. **"Write a recursive CTE to enumerate the full Bill of Materials for product ID 749, showing all levels and cumulative quantities."**
9. **"Show all SCD Type 2 source tables in AdventureWorks OLTP and demonstrate how they map to slowly changing dimensions in AdventureWorksDW."**
10. **"Generate an MDX query against the Adventure Works cube that shows Internet Gross Profit Margin by Product Category and Calendar Quarter, filtered to North America."**
11. **"Demonstrate hierarchyid usage in HumanResources.Employee: find all reports under a given manager using both IsDescendantOf and a recursive CTE approach, and compare execution plans."**
12. **"Model an SSAS Tabular solution on AdventureWorksDW using DAX, including a time intelligence measure for YOY Internet Sales growth and row-level security by sales territory."**
13. **"Propose a partitioning strategy for Production.TransactionHistory and Sales.SalesOrderDetail, including partition function, partition scheme, and a partition-switch archiving demo."**
14. **"Write T-SQL to shred the XML from Production.ProductModel.CatalogDescription and return a normalized result set with product features."**
15. **"Demonstrate dynamic data masking on Sales.CreditCard.CardNumber and row-level security on Sales.SalesOrderHeader filtered by TerritoryID for a given user."**

---

## 18) References (Curated)

- **AdventureWorks install & versions (Learn).** <https://learn.microsoft.com/en-us/sql/samples/adventureworks-install-configure?view=sql-server-ver17>
- **GitHub – sql-server-samples (Adventure Works).** <https://github.com/microsoft/sql-server-samples/tree/master/samples/databases/adventure-works>
- **GitHub – All AdventureWorks releases (.bak downloads).** <https://github.com/Microsoft/sql-server-samples/releases/tag/adventureworks>
- **GitHub – Analysis Services releases (.abf downloads).** <https://github.com/Microsoft/sql-server-samples/releases/tag/adventureworks-analysis-services>
- **SQL samples – Where are they? (Learn).** <https://learn.microsoft.com/en-us/sql/samples/sql-samples-where-are?view=sql-server-ver17>
- **SSAS Multidimensional Tutorial (Learn).** <https://learn.microsoft.com/en-us/analysis-services/multidimensional-tutorial/multidimensional-modeling-adventure-works-tutorial?view=asallproducts-allversions>
- **Analysis Services samples (Learn).** <https://learn.microsoft.com/en-us/analysis-services/analysis-services-samples?view=sql-analysis-services-2025>
- **AdventureWorksDW data dictionary (Dataedo).** <https://dataedo.com/samples/html/Data_warehouse/doc/AdventureWorksDW_4/home.html>
- **AdventureWorks OLTP table catalog (Dataedo).** <https://dataedo.com/samples/html/AdventureWorks/doc/AdventureWorks_2/tables.html>
- **AdventureWorks full data dictionary (PDF, Banbao).** <https://banbao991.github.io/resources/DB/AdventureWorks.pdf>
- **AdventureWorks documentation (dbdesc mirror).** <https://dbdesc.com/output_samples/htmlbrowse_AdventureWorks.html>
- **In-Memory OLTP sample (Learn).** <https://learn.microsoft.com/en-us/sql/relational-databases/in-memory-oltp/sample-database-for-in-memory-oltp?view=sql-server-ver17>
- **Fabric – Load AdventureWorksLT (Learn).** <https://learn.microsoft.com/en-us/fabric/database/sql/load-adventureworks-sample-data>
- **Data API builder sample (GitHub).** <https://github.com/Azure-Samples/dab-adventureworks-lt>
- **AdventureWorks for Postgres (GitHub).** <https://github.com/lorint/AdventureWorks-for-Postgres>
- **SSRS sample reports (Database Journal).** <https://www.databasejournal.com/ms-sql/taking-advantage-of-sample-reporting-services-reports/>
- **SSRS community refresh AdventureWorks2017 (sqlpowered).** <https://sqlpowered.com/reporting-services-samples-for-adventureworks2017/>
- **Install AdventureWorks for SQL Server 2025 (MSSQLTips).** <https://www.mssqltips.com/sqlservertip/11463/install-the-adventureworks-database-for-sql-server/>
- **Release/hosting move notes (Tech Community).** <https://techcommunity.microsoft.com/blog/sqlserver/new-github-location-for-adventureworks/385728>
- **DAX for multidimensional models (Learn).** <https://learn.microsoft.com/en-us/analysis-services/multidimensional-models/dax-for-multidimensional-models?view=asallproducts-allversions>
- **Key concepts in MDX (Learn).** <https://learn.microsoft.com/en-us/analysis-services/multidimensional-models/mdx/key-concepts-in-mdx-analysis-services?view=asallproducts-allversions>
- **AdventureWorks Sample OLTP Database – SQL Server 2008 Books Online (Learn).** <https://learn.microsoft.com/en-us/previous-versions/sql/sql-server-2008/ms124659(v=sql.100)>
- **SQL Server Reference Guide – AdventureWorks (InformIT).** <https://www.informit.com/articles/article.aspx?p=31359&seqNum=286>
- **SQL Server Reference Guide – AdventureWorks Derivatives (InformIT).** <https://www.informit.com/articles/article.aspx?p=31359&seqNum=287>

---

---

## Appendix A) Full Object Inventory — AdventureWorks OLTP

> **Scope & sources.** This inventory lists **tables, views, stored procedures, functions, and triggers** for the canonical AdventureWorks **OLTP** sample. The tables, views, procedures, and functions reflect the **2012–2022** family (stable through 2022+ in object names). The database-level trigger reflects 2012+; a **legacy SQL Server 2005 trigger list** is also provided for historical completeness.

### A. Tables (71)

`AWBuildVersion`; `DatabaseLog`; `ErrorLog`; `HumanResources.Department`; `HumanResources.Employee`; `HumanResources.EmployeeDepartmentHistory`; `HumanResources.EmployeePayHistory`; `HumanResources.JobCandidate`; `HumanResources.Shift`; `Person.Address`; `Person.AddressType`; `Person.BusinessEntity`; `Person.BusinessEntityAddress`; `Person.BusinessEntityContact`; `Person.ContactType`; `Person.CountryRegion`; `Person.EmailAddress`; `Person.Password`; `Person.Person`; `Person.PersonPhone`; `Person.PhoneNumberType`; `Person.StateProvince`; `Production.BillOfMaterials`; `Production.Culture`; `Production.Document`; `Production.Illustration`; `Production.Location`; `Production.Product`; `Production.ProductCategory`; `Production.ProductCostHistory`; `Production.ProductDescription`; `Production.ProductDocument`; `Production.ProductInventory`; `Production.ProductListPriceHistory`; `Production.ProductModel`; `Production.ProductModelIllustration`; `Production.ProductModelProductDescriptionCulture`; `Production.ProductPhoto`; `Production.ProductProductPhoto`; `Production.ProductReview`; `Production.ProductSubcategory`; `Production.ScrapReason`; `Production.TransactionHistory`; `Production.TransactionHistoryArchive`; `Production.UnitMeasure`; `Production.WorkOrder`; `Production.WorkOrderRouting`; `Purchasing.ProductVendor`; `Purchasing.PurchaseOrderDetail`; `Purchasing.PurchaseOrderHeader`; `Purchasing.ShipMethod`; `Purchasing.Vendor`; `Sales.CountryRegionCurrency`; `Sales.CreditCard`; `Sales.Currency`; `Sales.CurrencyRate`; `Sales.Customer`; `Sales.PersonCreditCard`; `Sales.SalesOrderDetail`; `Sales.SalesOrderHeader`; `Sales.SalesOrderHeaderSalesReason`; `Sales.SalesPerson`; `Sales.SalesPersonQuotaHistory`; `Sales.SalesReason`; `Sales.SalesTaxRate`; `Sales.SalesTerritory`; `Sales.SalesTerritoryHistory`; `Sales.ShoppingCartItem`; `Sales.SpecialOffer`; `Sales.SpecialOfferProduct`; `Sales.Store`

### B. Views (20)

`HumanResources.vEmployee`; `HumanResources.vEmployeeDepartment`; `HumanResources.vEmployeeDepartmentHistory`; `HumanResources.vJobCandidate`; `HumanResources.vJobCandidateEducation`; `HumanResources.vJobCandidateEmployment`; `Person.vAdditionalContactInfo`; `Person.vStateProvinceCountryRegion`; `Production.vProductAndDescription`; `Production.vProductModelCatalogDescription`; `Production.vProductModelInstructions`; `Purchasing.vVendorWithAddresses`; `Purchasing.vVendorWithContacts`; `Sales.vIndividualCustomer`; `Sales.vPersonDemographics`; `Sales.vSalesPerson`; `Sales.vSalesPersonSalesByFiscalYears`; `Sales.vStoreWithAddresses`; `Sales.vStoreWithContacts`; `Sales.vStoreWithDemographics`

### C. Stored Procedures (10)

**dbo:** `uspGetBillOfMaterials`; `uspGetEmployeeManagers`; `uspGetManagerEmployees`; `uspGetWhereUsedProductID`; `uspLogError`; `uspPrintError`; `uspSearchCandidateResumes`
**HumanResources:** `uspUpdateEmployeeHireInfo`; `uspUpdateEmployeeLogin`; `uspUpdateEmployeePersonalInfo`

### D. User-Defined Functions (11)

**dbo:** `ufnGetAccountingEndDate`; `ufnGetAccountingStartDate`; `ufnGetContactInformation`; `ufnGetDocumentStatusText`; `ufnGetProductDealerPrice`; `ufnGetProductListPrice`; `ufnGetProductStandardCost`; `ufnGetPurchaseOrderStatusText`; `ufnGetSalesOrderStatusText`; `ufnGetStock`; `ufnLeadingZeros`

### E. Triggers

#### E1. Database-Level Trigger (2012+ Family)

- **`ddlDatabaseTriggerLog`** — Audits DDL events (CREATE, ALTER, DROP) into `dbo.DatabaseLog`; fires on `DDL_DATABASE_LEVEL_EVENTS`.

#### E2. Legacy DML Triggers (SQL Server 2005 AdventureWorks OLTP)

> These object names reflect the **2005** schema (e.g., `Person.Contact`, `Sales.Individual`, `Sales.StoreContact`). Use for historical reference when working with 2005 documentation, books, or legacy samples.

`dbo.uAWBuildVersion`; `ddlDatabaseTriggerLog`; `HumanResources.dEmployee`; `HumanResources.uDepartment`; `HumanResources.uEmployee`; `HumanResources.uEmployeeAddress`; `HumanResources.uEmployeeDepartmentHistory`; `HumanResources.uEmployeePayHistory`; `HumanResources.uJobCandidate`; `HumanResources.uShift`; `Person.uAddress`; `Person.uAddressType`; `Person.uContact`; `Person.uContactType`; `Person.uCountryRegion`; `Person.uStateProvince`; `Production.iWorkOrder`; `Production.uBillOfMaterials`; `Production.uCulture`; `Production.uDocument`; `Production.uIllustration`; `Production.uLocation`; `Production.uProduct`; `Production.uProductCategory`; `Production.uProductCostHistory`; `Production.uProductDescription`; `Production.uProductDocument`; `Production.uProductInventory`; `Production.uProductListPriceHistory`; `Production.uProductModel`; `Production.uProductModelIllustration`; `Production.uProductModelProductDescriptionCulture`; `Production.uProductPhoto`; `Production.uProductProductPhoto`; `Production.uProductReview`; `Production.uProductSubcategory`; `Production.uScrapReason`; `Production.uTransactionHistory`; `Production.uTransactionHistoryArchive`; `Production.uUnitMeasure`; `Production.uWorkOrder`; `Production.uWorkOrderRouting`; `Purchasing.dVendor`; `Purchasing.iPurchaseOrderDetail`; `Purchasing.uProductVendor`; `Purchasing.uPurchaseOrderDetail`; `Purchasing.uPurchaseOrderHeader`; `Purchasing.uShipMethod`; `Purchasing.uVendor`; `Purchasing.uVendorAddress`; `Purchasing.uVendorContact`; `Sales.iduSalesOrderDetail`; `Sales.iStore`; `Sales.iuIndividual`; `Sales.uContactCreditCard`; `Sales.uCountryRegionCurrency`; `Sales.uCreditCard`; `Sales.uCurrency`; `Sales.uCurrencyRate`; `Sales.uCustomer`; `Sales.uCustomerAddress`; `Sales.uSalesOrderHeader`; `Sales.uSalesOrderHeaderSalesReason`; `Sales.uSalesPerson`; `Sales.uSalesPersonQuotaHistory`; `Sales.uSalesReason`; `Sales.uSalesTaxRate`; `Sales.uSalesTerritory`; `Sales.uSalesTerritoryHistory`; `Sales.uShoppingCartItem`; `Sales.uSpecialOffer`; `Sales.uSpecialOfferProduct`; `Sales.uStore`; `Sales.uStoreContact`

> **Note on counts.** Community-generated catalogs for the 2012+ family enumerate **Tables ≈71, Views ≈20, Procedures 10, Functions 11**; the 2005 schema shows **Triggers ≈70** across schemas, whereas 2012+ consolidates to a single database-level DDL trigger. Always verify in your instance with `SELECT name, type_desc, schema_id FROM sys.objects WHERE type IN ('U','V','P','FN','TF','IF','TR') ORDER BY type, name`.

---

## Appendix B) AdventureWorksDW Full Table Inventory

### Dimension Tables (16)

`dbo.DimAccount`; `dbo.DimCurrency`; `dbo.DimCustomer`; `dbo.DimDate`; `dbo.DimDepartmentGroup`; `dbo.DimEmployee`; `dbo.DimGeography`; `dbo.DimOrganization`; `dbo.DimProduct`; `dbo.DimProductCategory`; `dbo.DimProductSubcategory`; `dbo.DimPromotion`; `dbo.DimReseller`; `dbo.DimSalesReason`; `dbo.DimSalesTerritory`; `dbo.DimScenario`

### Fact Tables (9)

`dbo.FactAdditionalInternationalProductDescription`; `dbo.FactCallCenter`; `dbo.FactCurrencyRate`; `dbo.FactFinance`; `dbo.FactInternetSales`; `dbo.FactInternetSalesReason`; `dbo.FactProductInventory`; `dbo.FactResellerSales`; `dbo.FactSalesQuota`; `dbo.FactSurveyResponse`

### Subject Area Groupings (for SSAS Measure Group Design)

| Subject Area | Fact Table(s) | Key Dimensions |
|---|---|---|
| Internet Sales | `FactInternetSales`, `FactInternetSalesReason` | DimCustomer, DimProduct, DimDate, DimSalesTerritory, DimPromotion, DimSalesReason, DimCurrency |
| Reseller Sales | `FactResellerSales` | DimReseller, DimProduct, DimDate, DimSalesTerritory, DimPromotion, DimEmployee, DimCurrency |
| Sales Quotas | `FactSalesQuota` | DimEmployee, DimDate |
| Finance | `FactFinance` | DimAccount, DimDate, DimOrganization, DimScenario |
| Call Center | `FactCallCenter` | DimDate |
| Inventory | `FactProductInventory` | DimProduct, DimDate |
| Surveys | `FactSurveyResponse` | DimDate, DimCustomer, DimGeography |
| Currency Rates | `FactCurrencyRate` | DimCurrency, DimDate |

---

## Appendix C) AdventureWorksLT Full Table Inventory

### Tables (12)

`dbo.BuildVersion`; `dbo.ErrorLog`; `SalesLT.Address`; `SalesLT.Customer`; `SalesLT.CustomerAddress`; `SalesLT.Product`; `SalesLT.ProductCategory`; `SalesLT.ProductDescription`; `SalesLT.ProductModel`; `SalesLT.ProductModelProductDescription`; `SalesLT.SalesOrderDetail`; `SalesLT.SalesOrderHeader`

### Views (3)

`SalesLT.vGetAllCategories`; `SalesLT.vProductAndDescription`; `SalesLT.vProductModelCatalogDescription`

### Stored Procedures (2)

`SalesLT.uspLogError`; `SalesLT.uspPrintError`

### Functions (2)

`dbo.ufnGetAllCategories`; `dbo.ufnGetCustomerInformation`

---

## Appendix D) Key Business Rules & Constraints (Selected)

| Object | Constraint / Rule | Teaching Purpose |
|---|---|---|
| `Production.Product.SellEndDate` | Must be >= SellStartDate | Date range validation pattern |
| `Production.Product.ListPrice` | >= 0 | Non-negative price constraint |
| `Production.BillOfMaterials` | ComponentID != ProductAssemblyID | Prevent self-referencing BOM loop |
| `Sales.SalesOrderHeader.Status` | 1–6 (In process→Cancelled) | Enum/check constraint pattern |
| `Purchasing.PurchaseOrderHeader.Status` | 1–4 (Pending→Complete) | Enum/check constraint pattern |
| `Sales.SpecialOffer.EndDate` | >= StartDate | Date range validation |
| `Sales.SalesTaxRate.TaxType` | 1=state, 2=county, 3=state+county | Coded enum with named values |
| `HumanResources.Employee.Gender` | M or F | Single-char coded enum |
| `HumanResources.Employee.MaritalStatus` | S or M | Single-char coded enum |
| `Person.Person.EmailPromotion` | 0,1,2 (none, own, partner) | Marketing opt-in coded enum |
| `Production.Document.Status` | 1=Pending, 2=Approved, 3=Obsolete | Document lifecycle enum |
| `Person.Person.PersonType` | EM, IN, SC, SP, VC, GC | Role-based person type classification |
| `Sales.SalesTerritory.Group` | North America, Europe, Pacific | Regional grouping |

---

## Workloads and assets

This section grows as workloads are added. Each workload lives in its own folder beneath this README. Links will be added after the repository is published.

### Workload: AI governance

**Folder:** `ai-governance/`. A complete governance operating model for Adventure Works Cycles, from the "Governance Without the Gridlock" session: a charter, a RACI, a register of critical data elements, a scorecard, an AI usage standard, meeting agendas, executive interview results, and a 90-day plan.

| File name | Folder | What it is |
|---|---|---|
| [README.md](https://placeholder) | ai-governance | Index for the workload: the files, the Company 360 sections each one draws on, the numbers that tie the documents together, and assumptions to check. |
| [01_charter.md](https://placeholder) | ai-governance | The two-page data governance charter, filled in: intent, the Five Decisions, domain map, meetings, CDE rules, AI use, measures, and review. |
| [02_raci.md](https://placeholder) | ai-governance | Who decides what, as a RACI table, with the people who hold each role. |
| [03_cde_register.md](https://placeholder) | ai-governance | The register of ten critical data elements: sources, owners, stewards, quality rules, bars, and results, plus one full CDE card. |
| [04_scorecard_and_issue_log.md](https://placeholder) | ai-governance | Coverage, Trust, and Use across three runs, CDE and use-case status, and the issue log. |
| [05_ai_standard.md](https://placeholder) | ai-governance | The AI usage standard: data class to tool matrix, risk tiers, access rules, use-case register, approved grounding sources, and a sample intake form. |
| [06_meeting_agendas.md](https://placeholder) | ai-governance | Decision Board and Steward Huddle agendas, with sample decisions. |
| [07_executive_interviews_and_first_win.md](https://placeholder) | ai-governance | Executive interview summary, the Data Storm result, executive KPIs, business-to-data goals, candidate wins, and a Return on Data range. |
| [08_ninety_day_plan.md](https://placeholder) | ai-governance | The 13-week plan with status at week 10, and the next 90 days. |

### Shared assets

| File name | Folder | What it is |
|---|---|---|
| [logo.png](https://placeholder) | assets | The Straight Path Solutions logo, used at the top of the documents. |

### Adding a workload

1. Create a folder beneath the repository root, named for the workload in lowercase with hyphens.
2. Add a README.md to the folder that lists its files and the Company 360 sections they draw on.
3. Add a subsection and a table here, with one row per file.

---

*End of document: AdventureWorks Company 360 v3.1*
