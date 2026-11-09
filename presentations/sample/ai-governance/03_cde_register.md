![Straight Path Solutions](../assets/logo.png)

# CDE register and thresholds

**Adventure Works Cycles** | Register version 1.3 | Status as of week 10 | *Example document. Scores are illustrative. Table, column, and scale facts come from the [AdventureWorks Company 360](../README.md).*

Ten critical data elements, chosen with the Data Storm test and then filtered by executive dashboards, regulated or contractual data, and planned AI use. Scale is taken from the company profile: about 500 products (504 in the catalog), about 20,000 customers, about 31,000 sales orders (31,465 order headers), and nearly 300 employees. The fiscal year runs July 1 to June 30.

## The register

| ID | CDE | Domain | Source | Rows in scope | Class | Tier | Owner | Steward | Custodian |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Customer Email | Sales and customer | Person.EmailAddress.EmailAddress, reached through Sales.Customer.PersonID | Customers (about 20,000) | Confidential | 2 | VP of Sales | Dana | Information Services (Raj) |
| 2 | Customer ID | Sales and customer | Sales.Customer.CustomerID | Customers (about 20,000) | Internal | 2 | VP of Sales | Dana | Information Services (Raj) |
| 3 | Order Total Due | Finance | Sales.SalesOrderHeader.TotalDue (computed: SubTotal + TaxAmt + Freight) | Orders (31,465) | Confidential | 1 | CFO | Priya | Information Services (Raj) |
| 4 | Order Date | Sales and customer | Sales.SalesOrderHeader.OrderDate | Orders (31,465) | Internal | 2 | VP of Sales | Marcus (named week 8) | Information Services (Raj) |
| 5 | Sales Territory | Sales and customer | Sales.SalesOrderHeader.TerritoryID, Sales.SalesTerritory.Name (10 territories) | Orders (31,465) | Internal | 2 | VP of Sales | Dana | Information Services (Raj) |
| 6 | Product List Price | Product | Production.Product.ListPrice | Products (504) | Internal | 2 | VP of Production | Elena | Information Services (Raj) |
| 7 | Product Standard Cost | Product | Production.Product.StandardCost | Products (504) | Confidential | 2 | VP of Production | Priya (named week 8) | Information Services (Raj) |
| 8 | Product Number | Product | Production.Product.ProductNumber | Products (504) | Internal | 2 | VP of Production | Elena | Information Services (Raj) |
| 9 | Employee National ID | People | HumanResources.Employee.NationalIDNumber | Employees (nearly 300) | Regulated | 1 | HR Manager | Grace | Information Services (operations) |
| 10 | Vendor Credit Rating | Purchasing | Purchasing.Vendor.CreditRating (1 to 5, where 1 is superior) | Active vendors | Confidential | 2 | Purchasing Manager (named week 8) | Tomas | Information Services (Raj) |

## What the source already enforces

Write a rule only where the source does not already enforce the property. The schema already carries several controls, which is why some CDEs below need few or no extra rules.

| Control in the source | Effect on the register |
|---|---|
| Customer ID is the primary key of Sales.Customer | Uniqueness of Customer ID is guaranteed. The rule is a check that it stays true. |
| ListPrice must be zero or higher (check constraint) | No rule for negative prices. The price rule tests price against cost. |
| SellEndDate must be on or after SellStartDate | No rule for product sell dates. |
| EmailPromotion is limited to 0, 1, or 2 (none, own, partner) | Campaign use reads this opt-in value. It is a use condition on Customer Email. |
| Order status is limited to 1 through 6 (in process to cancelled) | The revenue report excludes cancelled orders by status. |
| TotalDue is computed from SubTotal, TaxAmt, and Freight | Completeness of Order Total Due is guaranteed. The rule that matters is reconciliation. |
| User-defined types (AccountNumber, OrderNumber, Name, Phone) are reused across schemas | Format rules live in one place and carry over to every table that uses the type. |
| Schema changes are captured in dbo.DatabaseLog by a database trigger | The custodian can see when a change might break a rule. |

## Rules, bars, and results

Run 1 was in week 6, before any cleanup. Run 3 was in week 10. A bar is the lowest passing score.

| ID | CDE | Rule | Bar | Run 1 | Run 3 | Run 3 result |
|---|---|---|---|---|---|---|
| 1 | Customer Email | Completeness (individual customers with at least one address) | 98% | 96.4% | 98.6% | Pass |
| 1 | Customer Email | Validity (well-formed address) | 97% | 98.9% | 99.1% | Pass |
| 1 | Customer Email | Uniqueness (no address shared by two people) | 99% | 99.4% | 99.5% | Pass |
| 2 | Customer ID | Completeness (every customer links to a person or a store) | 100% | 100% | 100% | Pass |
| 2 | Customer ID | Uniqueness | 100% | 100% | 100% | Pass |
| 3 | Order Total Due | Completeness | 100% | 100% | 100% | Pass |
| 3 | Order Total Due | Reconciliation (warehouse totals agree with source orders) | 99.5% | 99.7% | 99.8% | Pass |
| 4 | Order Date | Consistency (on or before ship date and due date) | 100% | 100% | 100% | Pass |
| 5 | Sales Territory | Consistency (order territory agrees with the customer's territory) | 99% | 97.2% | 99.4% | Pass |
| 6 | Product List Price | Completeness (finished goods on sale have a price) | 100% | 100% | 100% | Pass |
| 6 | Product List Price | Validity (at or above standard cost) | 99% | 99.8% | 99.8% | Pass |
| 7 | Product Standard Cost | Consistency (matches the current row in ProductCostHistory) | 99% | 96.5% | 99.2% | Pass |
| 8 | Product Number | Completeness | 100% | 100% | 100% | Pass |
| 8 | Product Number | Uniqueness | 100% | 100% | 100% | Pass |
| 9 | Employee National ID | Completeness | 100% | 100% | 100% | Pass |
| 9 | Employee National ID | Validity (format) | 100% | 100% | 100% | Pass |
| 10 | Vendor Credit Rating | Reviewed rating (active vendors whose rating came from a credit review) | 95% | 91.0% | 93.5% | **Fail** |

## What the failures meant at this scale

| CDE | Rule | Run 1 gap | Roughly how many records |
|---|---|---|---|
| Customer Email | Completeness | 1.6 points under the bar | About 720 customers without an address (3.6% of about 20,000) |
| Sales Territory | Consistency | 1.8 points under the bar | About 880 orders with a territory that differs from the customer's (2.8% of 31,465) |
| Product Standard Cost | Consistency | 2.5 points under the bar | About 18 products with a cost that differs from the cost history (3.5% of 504) |
| Vendor Credit Rating | Reviewed rating | 4.0 points under the bar | Active vendors with a default or stale rating (vendor count not in the profile) |

## Why these bars

Thresholds follow the use. Tier 1 CDEs feed financial reporting or regulated processes, so they carry the highest bars (Order Total Due and Employee National ID). Tier 2 CDEs are operational, with bars in the high 90s. The owner set each bar by asking what one bad record costs for the main use, as a range from low to high, and the Data Lead checked it against a profile of the real data so it was reachable.

Vendor Credit Rating is the one CDE still failing. Its bar is 95% because purchasing can still place an order with a rating that has not been reviewed, and the cost of a bad record is lower than for pricing or revenue data. Closing the 1.5 point gap is the work of the steward, Tomas, and it sits on the issue log.

## One full CDE card

| Field | Customer Email |
|---|---|
| Definition | Primary address used to contact an individual customer. |
| Scope | Individual customers, meaning rows in Sales.Customer where PersonID is populated. Store customers (the reseller channel) have contacts rather than a person-level address. |
| Domain and class | Sales and customer, Confidential |
| Authoritative source | Person.EmailAddress.EmailAddress (one person can have several addresses) |
| Owner | Vice President of Sales |
| Steward | Dana (Sales Operations) |
| Custodian | Information Services, BI team (Raj) |
| Rules and bars | Completeness 98%, validity 97%, uniqueness 99% |
| Use condition | Campaign sends only where Person.Person.EmailPromotion is 1 or 2 (own or partner offers). A value of 0 means no marketing email. |
| Used by | UC-01 Weekly campaign email, UC-02 Customer churn model |
| Certification history | Not certified in runs 1 and 2 (completeness below bar). Certified in run 3. |
| Review | Quarterly, by the owner and steward |

The completeness rule, written as a query against the source:

```sql
SELECT 100.0 * SUM(CASE WHEN e.BusinessEntityID IS NOT NULL THEN 1 ELSE 0 END)
       / COUNT(*) AS completeness_pct
FROM Sales.Customer AS c
LEFT JOIN (SELECT DISTINCT BusinessEntityID
           FROM Person.EmailAddress
           WHERE EmailAddress IS NOT NULL
             AND LTRIM(RTRIM(EmailAddress)) <> '') AS e
       ON e.BusinessEntityID = c.PersonID
WHERE c.PersonID IS NOT NULL;
```

## Certification checklist

A CDE earns the Certified badge only when all of these are true:

1. It has a plain-language definition.
2. It has a named owner, steward, and custodian.
3. Every rule is inside its bar on the latest run.
