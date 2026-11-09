![Straight Path Solutions](../assets/logo.png)

# Executive interviews, goals, and the first win

**Adventure Works Cycles** | Weeks 1 to 2 (Ask), with the first win measured in week 10 | *Example document. Answers, hours, and dollar figures are invented for illustration.*

## 1. The five interview questions

Six executives answered the same five questions, which keeps the answers comparable.

1. **Value aspiration.** Where will our advantage come from: running leaner, or creating new revenue from data?
2. **Decision gap.** What single trusted insight would change how you lead next quarter?
3. **Data Storm.** Which three business functions must be back within an hour after a disruption?
4. **AI and trust.** How do we balance AI speed against privacy and trust?
5. **Return on Data.** What would a return on our data estate mean to you?

## 2. What we heard

| Executive | Value aspiration | Decision gap | Data Storm | AI and trust | Return on Data |
|---|---|---|---|---|---|
| Chief Executive Officer | Leaner first, then new revenue | One view of revenue by territory and channel | Orders, product and price lookups, payroll | Move carefully, with one owner for each tool | Margin we can explain |
| VP of Sales | New revenue from Internet and Reseller customers | An accurate customer count and contact list | Order intake and fulfillment | Wants a churn model, worried about email quality | Fewer failed campaigns |
| Chief Financial Officer | Leaner | Month-end close in five days | Order intake and fulfillment, because orders feed the financials | Nothing that touches financial reporting without review | Hours saved at close |
| VP of Production | Leaner | Which products earn their cost | Product and price lookups | Pricing help, if costs are right | Fewer pricing corrections |
| Purchasing Manager | Leaner | Which vendors carry risk | Vendor ordering | Cautious | Fewer surprises from vendors |
| Human Resources Manager | Leaner | Accurate payroll and benefits files | Payroll | Strict on employee data | No data incidents |

## 3. The Data Storm test

Each executive named the functions that must return within an hour. Tallied across all six, order intake and fulfillment was named three times, product and price lookups twice, and payroll twice, so those became the three. Vendor ordering was named once. The data each of the three depends on:

| Function | Data it needs first |
|---|---|
| Order intake and fulfillment | Customer ID, Order Date, Order Total Due, Sales Territory |
| Product and price lookups | Product Number, Product List Price, Product Standard Cost |
| Payroll | Employee National ID |

Three more filters added candidates: data on executive dashboards (Order Total Due, Sales Territory), regulated or contractual data (Employee National ID and Customer Email, which is subject to marketing opt-in rules), and data planned for AI (Customer Email, Product List Price, Product Standard Cost). Vendor Credit Rating was added from the Purchasing Manager's interview about vendor risk. The result was ten CDEs, listed in `03_cde_register.md`.

### The executive KPIs behind the CDEs

The Adventure Works cube carries four executive KPIs. Three of them rest directly on CDEs in the register.

| Executive KPI | CDEs behind it |
|---|---|
| Revenue | Order Total Due, Order Date, Sales Territory |
| Growth in Customer Base | Customer ID, Order Date |
| Product Gross Profit Margin | Product List Price, Product Standard Cost, Product Number |
| Financial Efficiency | Budget scenarios in the warehouse. Not yet in the register, so it is a candidate for the next 90 days. |

## 4. Consolidated business-to-data goals

| Goal | Raised by | Data it depends on |
|---|---|---|
| G1. Close the month in five days | Chief Financial Officer | Order Total Due, Order Date, Sales Territory |
| G2. One accurate customer count and contact list | VP of Sales | Customer ID, Customer Email |
| G3. Price products with confidence | VP of Production, VP of Sales | Product List Price, Product Standard Cost, Product Number |
| G4. Keep payroll and benefits data correct and safe | Human Resources Manager | Employee National ID |
| G5. Know vendor risk before we buy | Purchasing Manager | Vendor Credit Rating |
| G6. Use AI without surprising anyone | Chief Executive Officer | The AI matrix, the intake form, certified CDEs |

## 5. Gap analysis

| Goal | Recommendation | Effort | Priority |
|---|---|---|---|
| G1. Close in five days | Certify the monthly revenue report | Medium | High |
| G2. Customer count and contacts | Certify the customer CDEs and remove duplicates | Low | High |
| G3. Price with confidence | Certify price and cost, then add the pricing assistant | Medium | Medium |
| G4. Payroll and benefits | Access review for restricted data | Medium | High |
| G5. Vendor risk | Close the credit rating gap | Low | Medium |
| G6. AI without surprises | Publish the AI matrix and intake form | Low | High |

## 6. Candidate wins

Each candidate is placed by effort and business value, the same way as the quadrant slide in the talk.

| # | Candidate win | Quadrant |
|---|---|---|
| 1 | Name stewards for the top 10 CDEs | Tactical quick win |
| 6 | Remove duplicate customer records | Tactical quick win |
| 2 | **Certify the monthly revenue report** | Strategic priority |
| 3 | Daily quality checks on customer data | Strategic priority |
| 7 | Access review for restricted data | Strategic priority |
| 4 | AI assistant on certified product data | Transformational |
| 5 | Enterprise catalog and lineage | Transformational |
| 8 | Real-time quality monitoring | Transformational |

**Chosen win:** certify the monthly revenue report (candidate 2). It uses data Adventure Works already has, and the Chief Financial Officer signs the budget.

## 7. The first win as a range

Hours saved each month on manual reconciliation of order totals and territories at close. Five finance analysts gave estimates: 20, 28, 35, 42, and 60 hours. By the Rule of Five, there is a 93.75% chance that the median of the full population falls between the smallest and largest of five random estimates, so the range is a usable measurement.

| | Low | Expected | High |
|---|---|---|---|
| Hours saved per month | 20 | 35 | 60 |
| Hours saved per year | 240 | 420 | 720 |
| Value at $85 an hour | $20,400 | $35,700 | $61,200 |
| Cost to deliver (80 hours at $100, no new tools) | $8,000 | $8,000 | $8,000 |
| Return on Data: (gain minus cost) divided by cost | 155% | 346% | 665% |

The hourly rates and the cost of effort are assumptions. What we do not yet know is how much of the saving holds after the next quarter's data changes, which is why the range is shown, and why the plan repeats the measurement at the next review.
