![Straight Path Solutions](../assets/logo.png)

# AI usage standard

**Adventure Works Cycles** | A child of the data governance charter | Version 1.0 | *Example document*

The AI standard reuses what the charter already built: classification, domains, stewards, and CDEs. There is no second binder. One page of rules, one register, one intake form.

## 1. Which data may go to which tool

| Data class | Approved enterprise assistant | Approved internal system | Public consumer tool |
|---|---|---|---|
| Public | Allowed | Allowed | Allowed |
| Internal | Allowed | Allowed | Not allowed |
| Confidential | Review first | Allowed | Not allowed |
| Regulated | Review first | Review first | Not allowed |

Review first means steward sign-off and logging. At Adventure Works, regulated data includes Employee National ID and credit card numbers (Sales.CreditCard), which are masked at the source and excluded from AI use, and login credentials (Person.Password), which are never used. Confidential data includes Customer Email, customer demographics, and Product Standard Cost.

## 2. Risk tiers

| Tier | Typical use | What it takes to approve |
|---|---|---|
| Low | Internal drafting and summarizing | Register the use case. The Data Lead approves. |
| Medium | Customer-facing output or decision support | Intake form, test results, and owner sign-off. The Data Lead approves. |
| High | Decisions about people, credit, or safety | Full intake, human oversight plan, Legal review, Decision Board consulted. The Data Lead approves. |

## 3. The core rule

Only certified CDEs feed analytics or AI that makes or supports a decision. A use case whose CDEs are not all certified stays blocked, and the scorecard shows it as blocked until they are.

## 4. Access rules for AI tools

AI tools inherit the access of the person using them, and never more.

- Territory-based row-level security on Sales.SalesOrderHeader (filtered by TerritoryID) applies to any assistant that reads order data.
- Credit card numbers (Sales.CreditCard.CardNumber) are masked for anyone without a need to see them, and no AI tool receives them.
- XML and binary content, such as product photos, engineering documents, job candidate resumes, and marketing catalog descriptions, is inventoried before an AI tool reads it. Job candidate resumes (HumanResources.JobCandidate.Resume) are out of scope for AI use in version 1.

## 5. AI use-case register

| ID | Use case | Owner | Tier | Data classes | CDEs used | Tool | Status | Review |
|---|---|---|---|---|---|---|---|---|
| UC-02 | Customer churn model | VP of Sales | Medium | Confidential, Internal | 1, 4 | Approved internal system | Approved, week 10 | 6 months |
| UC-04 | Pricing recommendation assistant | VP of Sales | Medium | Confidential, Internal | 6, 7, 8 | Approved internal system | Approved, week 10, with a condition | 6 months |
| UC-05 | Product catalog assistant for the sales team | VP of Production | Low | Internal | 6, 8 | Approved enterprise assistant | Approved, week 7 | 12 months |

UC-02 and UC-04 were blocked at runs 1 and 2 because Customer Email and Product Standard Cost were not certified. They were approved only after run 3 cleared them.

Two conditions came with the approvals. The churn model (UC-02) leaves out the personal attributes exposed by Sales.vPersonDemographics (birth date, marital status, gender, yearly income, children, education, and occupation) in version 1, until Legal Counsel and the owner review them. The product catalog assistant (UC-05) answers only from the marketing catalog descriptions, which exist in six languages.

## 6. Approved grounding sources

Assistants answer from sources the Data Lead has approved, and they cite them. The register of approved sources is short on purpose.

| ID | Source | Class | Owner | Approved for | Review |
|---|---|---|---|---|---|
| GS-01 | [AdventureWorks Company 360](../README.md) (the repository README) | Internal | Data Lead | Questions about the company's data estate: schemas, objects, warehouse mapping, business scenarios, and governance patterns | Quarterly |

Rules for agents, taken from the operating instructions in the Company 360 itself:

1. Ground first in the approved sources, and cite every nontrivial claim.
2. List assumptions, constraints, and steps.
3. Prefer correctness over coverage, and mark uncertainty.
4. Say how to verify anything unknown instead of guessing.
5. Keep the transactional database (OLTP), the warehouse (DW), and the lightweight database (LT) distinct.

## 7. How it maps to the NIST AI Risk Management Framework

| NIST function | Adventure Works practice |
|---|---|
| Govern | The Decision Board owns the standard and approves changes |
| Map | The intake form records purpose, data, and risk tier |
| Measure | Test results are required before launch for Medium and High tiers |
| Manage | Monitoring and a review date on every register entry |

Legal Counsel will confirm the current EU AI Act timeline, since Adventure Works sells in France and Germany.

## 8. Sample intake form: UC-04 pricing recommendation assistant

| Field | Entry |
|---|---|
| Purpose | Suggest list price changes to sales managers, with the reasoning. |
| Requested by | Vice President of Sales |
| Tool | Approved internal system |
| Data used | Product List Price, Product Standard Cost, Product Number |
| Data classes | Confidential (standard cost), Internal |
| Certified CDEs only? | Yes, as of run 3. Blocked at runs 1 and 2. |
| Risk tier | Medium (decision support) |
| Tests before launch | Compare suggestions with 12 months of actual price changes. Check for suggestions below standard cost. |
| Human oversight | A sales manager and the Finance steward review any suggested change above 5%. Nothing is applied automatically. |
| Monitoring | Weekly review of suggestions accepted and rejected. |
| Approved by | Data Lead, week 10. Decision Board informed. |
| Review date | Six months after approval |
