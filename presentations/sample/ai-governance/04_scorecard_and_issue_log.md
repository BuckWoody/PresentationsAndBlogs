![Straight Path Solutions](../assets/logo.png)

# Governance scorecard and issue log

**Adventure Works Cycles** | Latest run: run 3, week 10 | *Example document. All figures are illustrative.*

## The three numbers

| Measure | What it counts | Run 3 | 90-day target |
|---|---|---|---|
| Coverage | CDEs with an owner, steward, and custodian all named | **100%** (10 of 10) | 100% |
| Trust | CDEs inside every quality bar | **90%** (9 of 10) | 90% |
| Use | Analytics and AI use cases that rely only on certified CDEs | **100%** (6 of 6) | 100% |

All three 90-day targets are met. The one open item is Vendor Credit Rating, which no current use case depends on.

## The trend

| Run | When | What changed | Coverage | Trust | Use | Certified | Open issues |
|---|---|---|---|---|---|---|---|
| 1 | Week 6 | Baseline, before any cleanup | 70% | 60% | 33% | 5 of 10 | 7 |
| 2 | Week 8 | Three missing people named (steward for Order Date, steward for Product Standard Cost, owner for Vendor Credit Rating) | 100% | 60% | 33% | 6 of 10 | 4 |
| 3 | Week 10 | Data cleanup on email completeness, sales territories, and standard costs | 100% | 90% | 100% | 9 of 10 | 1 |

Run 2 is the instructive one. Naming people fixed Coverage and did nothing for Trust, and run 3 shows the reverse: the data work lifted Trust and Use. Both kinds of fix were needed.

## CDE status, run 1 against run 3

| ID | CDE | People named (run 1) | Rules pass (run 1) | Certified (run 1) | Certified (run 3) |
|---|---|---|---|---|---|
| 1 | Customer Email | Yes | No | No | Yes |
| 2 | Customer ID | Yes | Yes | Yes | Yes |
| 3 | Order Total Due | Yes | Yes | Yes | Yes |
| 4 | Order Date | **No steward** | Yes | No | Yes |
| 5 | Sales Territory | Yes | No | No | Yes |
| 6 | Product List Price | Yes | Yes | Yes | Yes |
| 7 | Product Standard Cost | **No steward** | No | No | Yes |
| 8 | Product Number | Yes | Yes | Yes | Yes |
| 9 | Employee National ID | Yes | Yes | Yes | Yes |
| 10 | Vendor Credit Rating | **No owner** | No | No | **No** |

## Use cases

| ID | Use case | Kind | Risk tier | Depends on | Run 1 | Run 3 |
|---|---|---|---|---|---|---|
| UC-01 | Weekly campaign email | Analytics | Medium | 1 | Blocked | Cleared |
| UC-02 | Customer churn model | AI | Medium | 1, 4 | Blocked | Cleared |
| UC-03 | Monthly revenue report | Analytics | High | 3, 4, 5 | Blocked | Cleared |
| UC-04 | Pricing recommendation assistant | AI | Medium | 6, 7, 8 | Blocked | Cleared |
| UC-05 | Product catalog assistant for the sales team | AI | Low | 6, 8 | Cleared | Cleared |
| UC-06 | Benefits enrollment file | Analytics | High | 9 | Cleared | Cleared |

Notes on the use cases: UC-01 sends only to customers whose marketing opt-in (EmailPromotion) allows it. UC-03 excludes cancelled orders and reports by channel (Internet and Reseller) and by fiscal period. UC-05 draws on catalog descriptions in six languages.

## Issue log

Each failing rule or missing role opens an issue, assigned to the steward (or to the owner when there is no steward). An issue closes on its own when a later run passes.

| Issue | CDE | What | Assigned to | Opened | Closed | Status |
|---|---|---|---|---|---|---|
| 1 | Customer Email | Completeness 96.4% against a 98% bar (about 720 customers without an address) | Dana | Run 1 | Run 3 | Closed |
| 2 | Sales Territory | Consistency 97.2% against a 99% bar (about 880 orders whose territory differs from the customer's) | Dana | Run 1 | Run 3 | Closed |
| 3 | Product Standard Cost | Consistency 96.5% against a 99% bar (about 18 products that differ from the cost history) | VP of Production (no steward yet) | Run 1 | Run 3 | Closed |
| 4 | Vendor Credit Rating | Reviewed rating 91.0% against a 95% bar (93.5% in run 3) | Tomas | Run 1 | | **Open** |
| 5 | Order Date | No steward assigned | VP of Sales | Run 1 | Run 2 | Closed |
| 6 | Product Standard Cost | No steward assigned | VP of Production | Run 1 | Run 2 | Closed |
| 7 | Vendor Credit Rating | No owner assigned | Unassigned | Run 1 | Run 2 | Closed |

## Next actions

1. Tomas to close the 1.5 point reviewed-rating gap on Vendor Credit Rating (owner: Purchasing Manager). Target: before the next Decision Board.
2. Dana to keep a monthly completeness check running on Customer Email, since the fix was a one-time cleanup.
3. Data Lead to bring the trend to the Decision Board, with the first win and its Return on Data range (see `07_executive_interviews_and_first_win.md`).
