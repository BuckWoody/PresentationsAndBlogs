![Straight Path Solutions](../assets/logo.png)

# Data governance charter

**Adventure Works Cycles** | Version 1.0 | Effective 14 December 2026

*Example document. All names, figures, and dates are illustrative.*

---

## Part one: decisions

### 1. Intent

We govern data so that Finance closes the month in five days, every customer gets one accurate bill, and our AI tools use only data we trust.

### 2. The Five Decisions

| Decision | The question | Who decides | Recorded in |
|---|---|---|---|
| Matter | Which data matters most? | Data Lead decides. Stewards draft and owners are consulted. | CDE register (section 5) |
| Bar | How good is good enough? | The domain owner, for each use of the data. | CDE register (section 5) |
| Own | Who answers when the data is wrong? | Decision Board. | Domain map (section 3) |
| Use | Who may use the data, and for what, including AI? | Board sets the rules. Owners approve access. Data Lead approves AI use cases. | Classification and AI matrix (section 6) |
| Fix | What happens when it breaks? | The domain owner. | Issue log (section 4) |

### 3. Domain map

Five domains to start. Each owner is an existing executive, so there are no new titles. One person can wear two hats, and the person who sets the bar is not the only one who checks it.

| Domain | Owner (title) | Steward | Custodian team | First CDEs |
|---|---|---|---|---|
| Sales and customer | Vice President of Sales | Dana (Sales Operations), Marcus (order dates, from week 8) | Information Services, BI team (Raj) | Customer Email, Customer ID, Order Date, Sales Territory |
| Finance | Chief Financial Officer | Priya (Billing and cost accounting) | Information Services, BI team (Raj) | Order Total Due |
| Product | Vice President of Production | Elena (Production Control), Priya (standard cost, from week 8) | Information Services, BI team (Raj) | Product Number, Product List Price, Product Standard Cost |
| Purchasing | Purchasing Manager (named in week 8) | Tomas (Purchasing Analyst) | Information Services, BI team (Raj) | Vendor Credit Rating |
| People | Human Resources Manager | Grace (HR Operations) | Information Services, operations | Employee National ID |

Finance is a reporting domain. It uses order totals from the Sales schema and the budget scenarios in the warehouse, and its fiscal year runs July 1 to June 30. The Data Lead is the Information Services Manager, who wears the CDO hat. The executive sponsor is the Chief Executive Officer.

### 4. Two meetings and the issue path

| | Decision Board | Steward Huddle |
|---|---|---|
| Rhythm | Monthly, 45 minutes | Every two weeks, 20 minutes |
| Who | Domain owners, Data Lead, Legal Counsel | Stewards, custodians, Data Lead |
| Agenda | 10 min scorecard (Coverage, Trust, Use). 25 min decisions. 10 min risks and escalations. | New issues, threshold changes, handoffs. |
| Decides | Policy, domain owners, AI rules, escalated issues. | Triage and routing of issues. |

**Issue path:** 1. Anyone logs an issue. 2. The steward acknowledges it within 2 business days. 3. Steward and custodian triage and fix it. 4. If it is stuck, the domain owner decides. 5. The Decision Board sees only what escalates.

---

## Part two: rules

### 5. CDE register and thresholds

Ten CDEs across the five domains, chosen with the Data Storm test (see `07_executive_interviews_and_first_win.md`). The full register, with rules and bars, is in `03_cde_register.md`.

Thresholds follow the use. Starting points, calibrated with each owner: Tier 1 (regulatory or financial) 99% and up. Tier 2 (operational) mid to high 90s. A CDE earns the Certified badge only when it has a definition, a named owner, steward, and custodian, and every rule inside its bar.

### 6. Classification and AI use

| Data class | Approved enterprise assistant | Approved internal system | Public consumer tool |
|---|---|---|---|
| Public | Allowed | Allowed | Allowed |
| Internal | Allowed | Allowed | Not allowed |
| Confidential | Review first | Allowed | Not allowed |
| Regulated | Review first | Review first | Not allowed |

Review first means steward sign-off and logging. Risk tiers and the AI use-case register are in `05_ai_standard.md`.

**Rule:** only certified CDEs feed analytics or AI that makes or supports a decision. Every AI use case goes in the AI register with its owner, tier, data used, and review date. Useful frameworks: NIST AI RMF (Govern, Map, Measure, Manage) and, when you want an audit, ISO/IEC 42001.

### 7. Measures

| Measure | What it counts | Baseline (week 6) | 90-day target | 12-month target |
|---|---|---|---|---|
| Coverage | CDEs with an owner, steward, and custodian all named, as a share of all CDEs | 70% | 100% | 100% |
| Trust | CDEs inside every quality bar, as a share of all CDEs | 60% | 90% | 100% |
| Use | Analytics and AI use cases that rely only on certified CDEs, as a share of all use cases | 33% | 100% | 100% |

### 8. Review and approval

Review this charter every 12 months and after any major data incident. Changes go to the Decision Board and take effect on approval.

| Version | Date | Change | Approved by |
|---|---|---|---|
| 1.0 | 14 December 2026 (week 6) | Initial charter | Chief Executive Officer |
| 1.1 | Week 8 | Named the steward for Order Date, the steward for Product Standard Cost, and the owner for Vendor Credit Rating | Decision Board |

Executive sponsor: Chief Executive Officer | Data Lead: Information Services Manager
