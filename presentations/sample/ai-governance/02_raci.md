![Straight Path Solutions](../assets/logo.png)

# Who decides what: RACI

**Adventure Works Cycles** | *Example document. Names are placeholders.*

R is responsible (does the work). A is accountable (decides and answers for it, exactly one per row). C is consulted (gives input before the decision). I is informed (told after).

## Who holds each hat

| Role | Held by |
|---|---|
| Decision Board | Domain owners, Data Lead, Legal Counsel (meets monthly) |
| Data Lead | Information Services Manager (the CDO hat) |
| Owner | Vice President of Sales (Sales and customer), Chief Financial Officer (Finance), Vice President of Production (Product), Purchasing Manager (Purchasing), Human Resources Manager (People) |
| Steward | Dana and Marcus (Sales), Priya (Finance), Elena (Product), Tomas (Purchasing), Grace (People) |
| Custodian | Information Services: Raj (BI team) for sales, finance, product, and purchasing data, and the operations team for HR data |
| Security or Legal | Legal Counsel, with the IT Security Lead consulted on access |

## The table

| Activity | Decision | Decision Board | Data Lead | Owner | Steward | Custodian | Security or Legal |
|---|---|---|---|---|---|---|---|
| Approve the charter and the AI standard | Use | A | R | C | C | I | C |
| Name domains, owners, and stewards | Own | A | R | C | I | I | I |
| Pick the critical data elements (CDEs) | Matter | I | A | C | R | C | C |
| Write the CDE definition | Matter | I | I | A | R | C | I |
| Set the quality threshold | Bar | I | C | A | R | C | I |
| Build and run the quality checks | Bar | I | A | I | C | R | I |
| Fix a failing CDE | Fix | I | C | A | R | R | I |
| Grant access to restricted data | Use | I | C | A | C | R | C |
| Approve a new AI use case, by risk tier * | Use | C | A | C | C | R | C |
| Publish the Coverage, Trust, and Use scorecard | All | I | A/R | C | R | C | I |

\* The Decision Board is consulted on high-risk AI use cases only.

## How it was used at Adventure Works

- Week 3: the table was reviewed with the owners. Three roles turned out to be unnamed: the steward for Order Date, the steward for Product Standard Cost, and the owner for Vendor Credit Rating. They were named in week 8.
- Week 6: the Decision Board approved the table with the charter.
- The review date is the 12-month charter review.
