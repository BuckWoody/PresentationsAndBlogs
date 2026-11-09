![Straight Path Solutions](../assets/logo.png)

# Workload: AI governance for Adventure Works Cycles

*Part of the [AdventureWorks Company 360](../README.md) repository. All names, scores, dates, and dollar figures in this folder are illustrative.*

This workload is a complete set of governance working papers for the fictitious Adventure Works Cycles: a charter, a RACI, a register of critical data elements, a scorecard, an AI usage standard, meeting agendas, executive interview results, and a 90-day plan. It comes from the session "Governance Without the Gridlock" (Live! 360 Orlando 2026), and it uses the Company 360 in the root of this repository as its single source of company facts.

## What is in this folder

| File | What it is | Company 360 sections it draws on | Related talk slides |
|---|---|---|---|
| [01_charter.md](01_charter.md) | The two-page data governance charter, filled in | 2, 5 | 6 to 9, 15, 16 |
| [02_raci.md](02_raci.md) | Who decides what, with names for each role | 2, 5 | 7, 9 |
| [03_cde_register.md](03_cde_register.md) | The CDE register, rules and bars, and one full CDE card | 5, 9, 12, Appendix D | 11 to 13 |
| [04_scorecard_and_issue_log.md](04_scorecard_and_issue_log.md) | Coverage, Trust, and Use across three runs, plus the issue log | 2, 5, 8 | 10, 14 |
| [05_ai_standard.md](05_ai_standard.md) | AI use matrix, risk tiers, access rules, use-case register, approved grounding sources, and a sample intake form | 1, 5, 12 | 15 to 17 |
| [06_meeting_agendas.md](06_meeting_agendas.md) | Decision Board and Steward Huddle agendas, with sample decisions | 2 | 9 |
| [07_executive_interviews_and_first_win.md](07_executive_interviews_and_first_win.md) | Interview summary, Data Storm result, executive KPIs, goals, candidate wins, and a Return on Data range | 2, 8, 9 | 11, 20, 21 |
| [08_ninety_day_plan.md](08_ninety_day_plan.md) | The 13-week plan with status at week 10 | 2 | 20 |

## One story across all the documents

The numbers tie together, so the papers read as one engagement.

| Run | When | Coverage | Trust | Use | Certified CDEs | Open issues |
|---|---|---|---|---|---|---|
| 1 | Week 6 | 70% | 60% | 33% | 5 of 10 | 7 |
| 2 | Week 8 | 100% | 60% | 33% | 6 of 10 | 4 |
| 3 | Week 10 | 100% | 90% | 100% | 9 of 10 | 1 |

## Assumptions to check

1. **Facts about the company** (scale, channels, territories, fiscal year, schemas, and column names) come from the Company 360. Where a rule would test something the schema already enforces, such as a primary key or a check constraint, the register says so and the rule tests a different property.
2. **Order data dates.** The sample's orders span May 31, 2011 to June 30, 2014. The engagement treats the data as current, so dates in these documents are shown by week number.
3. **The people.** Owners are shown by title, because the Company 360 gives no executive names. Steward and custodian names (Dana, Priya, Marcus, Elena, Tomas, Grace, and Raj) are placeholders.
4. **The numbers.** Quality scores, issue counts, and the dollar figures in the Return on Data example are illustrative assumptions. Scale figures (504 products, 31,465 orders, and so on) are from the Company 360.
5. **Finance.** The Company 360 has no Finance schema. The Finance domain here is a reporting domain built on order totals in the Sales schema, with the warehouse (including the FactFinance budget scenarios) as its reporting layer.
