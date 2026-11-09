![Straight Path Solutions](assets/logo.png)

# Adventure Works Cycles: company profile

*A fictitious multinational bicycle manufacturer, used as the case company for the course and presentation materials in this repository.*

## Snapshot

| | |
|---|---|
| Company | Adventure Works Cycles (fictitious) |
| Industry | Bicycle manufacturing and sales |
| What it sells | Metal and composite bicycles, plus components, clothing, and accessories |
| Sales channels | Internet (direct to consumer) and Reseller (business partners and stores) |
| Catalog | About 500 products (504) in 4 categories and 37 subcategories |
| Customers | About 20,000, both individuals and stores |
| Order volume | About 31,000 sales orders (31,465), averaging about 4 line items each |
| Employees | Nearly 300 |
| Markets | 10 sales territories in 3 regions: North America, Europe, and Pacific |
| Fiscal year | July 1 to June 30 |
| Case data window | May 31, 2011 to June 30, 2014 (fiscal years 2012 to 2014) |
| Management KPIs | Revenue, growth in customer base, product gross profit margin, and financial efficiency |

## Company overview

Adventure Works Cycles makes and sells metal and composite bicycles, along with the components, clothing, and accessories that go with them. It serves individual consumers directly through the Internet and sells through business partners and stores in a reseller channel. It buys from a network of vendors, runs its own manufacturing, and employs nearly 300 people.

The company is fictitious. It is the long-running sample company behind the SQL Server and Microsoft Fabric sample databases, so it is well documented and familiar to many practitioners. Throughout this repository the company is treated as a going concern with current data.

## Products

- **Range:** four categories (bikes, components, clothing, and accessories), 37 subcategories, and about 500 products.
- **Lines and classes:** road, mountain, touring, and standard lines, in high, medium, and low classes.
- **Pricing and cost:** every product carries a list price and a standard cost, and the company keeps the history of both.
- **Global catalog:** product descriptions exist in six languages (Arabic, Chinese (Traditional), English, French, Hebrew, and Thai).
- **Customer voice:** customers can post product reviews.

## Customers and channels

The Internet channel sells directly to individuals. The Reseller channel sells through business partners and stores. Together they account for about 31,000 orders from about 20,000 customers.

The company records why customers buy (price, quality, reviews, the manufacturer, advertising, promotions, demo events, sponsorships, and the web) and runs promotions with their own discounts and date ranges. Customer demographics, such as income, education, occupation, and family, support segmentation.

## Geographic footprint

| Region | Territories |
|---|---|
| North America | Canada, Central, Northeast, Northwest, Southeast, Southwest |
| Europe | France, Germany, United Kingdom |
| Pacific | Pacific |

The company sells in multiple currencies and tracks daily exchange rates. Each territory reports year-to-date and prior-year sales and cost.

## Operations and supply chain

**Manufacturing.** Production runs through work orders that move across work centers, such as frame forming, frame welding, painting, subassembly, and final assembly. Bills of materials describe multi-level assemblies. Scrap is recorded with a reason, such as a wheel misalignment. Inventory is tracked by location, shelf, and bin, and every movement (a purchase, a sale, or a work order) is logged.

**Purchasing.** Each vendor carries a credit rating from 1 (superior) to 5 and a preferred-vendor flag. One product can come from several vendors, each with its own price and lead time. Purchase orders move from pending to approved or rejected, and then to complete. Several carriers and rate structures handle shipping.

## People and organization

Nearly 300 employees work in a management hierarchy across twelve departments: Engineering; Executive General and Administration; Human Resources; Information Services; Manufacturing; Production Control; Purchasing; Quality Assurance; Research and Development; Sales and Marketing; Shipping and Receiving; and Tool Design. Work is organized in day, evening, and night shifts.

Sales representatives carry quotas, bonuses, and commission rates, and their territory assignments are tracked over time. Human Resources keeps department and pay history, and candidate resumes.

## Fiscal calendar and performance measures

- **Fiscal year:** July 1 to June 30.
- **KPIs management watches:** revenue (with a goal, status, and trend), growth in the customer base, product gross profit margin, and financial efficiency.
- **Scenarios:** finance reports against actual, budget, and forecast figures.
- **Sales targets:** quotas are set for each salesperson by quarter.
- **Management views:** channel sales, direct sales, finance, a sales summary, and a warehouse view of inventory and procurement.

## Reading the numbers

This profile describes the structure and scale of the company. It contains no revenue, margin, or profit figures, because the company is fictitious and no financial statements exist for it. Where course materials need figures such as quality scores or dollar amounts, they are illustrative, and each document says so.

## Questions this company invites

An analyst picking up Adventure Works would reasonably ask:

1. **Channel economics.** How do the Internet and Reseller channels compare on order value, frequency, and profitability?
2. **Territory performance.** Which territories beat their prior year, and which meet their quotas?
3. **Product economics.** Where do list price and standard cost leave the widest margin, and how have both moved over time?
4. **Customer segments.** Which customers buy most often, and which promotions and reasons for buying work best?
5. **Supply risk.** How concentrated is spending across vendors, and what do credit ratings and lead times say about risk?
6. **Operational quality.** Where does scrap occur, and does it affect on-time delivery?
7. **Workforce.** How is the organization structured, and how do quotas and pay track results?

## Key terms

| Term | Meaning |
|---|---|
| Reseller | A business partner or store that buys from the company and sells to consumers |
| Territory | A sales region with its own targets and results |
| List price | The price the company advertises for a product |
| Standard cost | The planned cost to make or buy a product |
| Gross profit margin | The share of revenue left after the product's cost |
| Quota | A sales target set for a representative for a period |
| Bill of materials | The list of parts and subassemblies needed to build a product |
| Fiscal year | The company's 12-month reporting year, here July 1 to June 30 |

## How the company's information is organized

The company's information falls into five business areas: people and contacts, human resources, production, purchasing, and sales. A reporting warehouse built from those areas supports analysis. Instructors and workload authors will find the full technical detail in the [Company 360 technical reference](reference/company-360.md).

## How this repository is organized

```
/
+-- README.md          This company profile
+-- assets/            Shared images, such as the logo
+-- reference/         Company 360 technical reference
+-- ai-governance/     Workload: data governance and AI usage for Adventure Works
```

Read this profile first. Then open a workload folder. A workload applies the company to one purpose, and its README lists its files and the parts of the technical reference it draws on. The list of workloads and files is in the next section, and it grows as workloads are added.

## Workloads and assets

This section grows as workloads are added. Each workload lives in its own folder beneath this README. Links will be added after the repository is published.

### Workload: AI governance

**Folder:** `ai-governance/`. A complete governance operating model for Adventure Works Cycles, from the "Governance Without the Gridlock" session: a charter, a RACI, a register of critical data elements, a scorecard, an AI usage standard, meeting agendas, executive interview results, and a 90-day plan.

| File name | Folder | What it is |
|---|---|---|
| [README.md](https://placeholder) | ai-governance | Index for the workload: the files, the technical reference sections each one draws on, the numbers that tie the documents together, and assumptions to check. |
| [01_charter.md](https://placeholder) | ai-governance | The two-page data governance charter, filled in: intent, the Five Decisions, domain map, meetings, CDE rules, AI use, measures, and review. |
| [02_raci.md](https://placeholder) | ai-governance | Who decides what, as a RACI table, with the people who hold each role. |
| [03_cde_register.md](https://placeholder) | ai-governance | The register of ten critical data elements: sources, owners, stewards, quality rules, bars, and results, plus one full CDE card. |
| [04_scorecard_and_issue_log.md](https://placeholder) | ai-governance | Coverage, Trust, and Use across three runs, CDE and use-case status, and the issue log. |
| [05_ai_standard.md](https://placeholder) | ai-governance | The AI usage standard: data class to tool matrix, risk tiers, access rules, use-case register, approved grounding sources, and a sample intake form. |
| [06_meeting_agendas.md](https://placeholder) | ai-governance | Decision Board and Steward Huddle agendas, with sample decisions. |
| [07_executive_interviews_and_first_win.md](https://placeholder) | ai-governance | Executive interview summary, the Data Storm result, executive KPIs, business-to-data goals, candidate wins, and a Return on Data range. |
| [08_ninety_day_plan.md](https://placeholder) | ai-governance | The 13-week plan with status at week 10, and the next 90 days. |

### Shared assets and references

| File name | Folder | What it is |
|---|---|---|
| [company-360.md](https://placeholder) | reference | The Company 360 technical reference: databases, schemas, objects, mappings, and governance patterns, for instructors, workload authors, and LLM agents. |
| [logo.png](https://placeholder) | assets | The Straight Path Solutions logo, used at the top of the documents. |

### Adding a workload

1. Create a folder beneath the repository root, named for the workload in lowercase with hyphens.
2. Add a README.md to the folder that lists its files and the parts of this profile and the technical reference that they draw on.
3. Add a subsection and a table here, with one row per file.
