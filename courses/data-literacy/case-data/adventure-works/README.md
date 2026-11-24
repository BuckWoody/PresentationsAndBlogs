<img width="150" style="float: right; margin: 0px 15px 15px 0px;" src="../../graphics/logo.png">

# Workshop: Data Literacy

#### <i>Adventure Works Cycles: Illustrative Extract (Optional)</i>

<p style="border-bottom: 1px solid lightgrey;"></p>

Several modules end with an optional "Go further" activity set at Adventure Works Cycles, the well-known fictitious bicycle maker that began as a Microsoft sample company and has been expanded for these materials. [The company profile is here](https://tinyurl.com/bw-sample).

**Please read this first.** The files in this folder are a small, **invented** extract made for teaching. They aren't the Microsoft sample databases, and none of the amounts are real or taken from a financial statement (the company profile itself says no financial statements exist for the company). The extract follows the profile's structure: two sales channels (Internet and Reseller), ten territories in three regions, a July 1 to June 30 fiscal year, and a case window of May 31, 2011 to June 30, 2014. It has about 48 products where the real catalog has about 500, and about 6,600 orders where the full sample has about 31,000.

You never need this extract to finish the workshop.

| File | One row is a single... | Key |
|---|---|---|
| `sales_territory.csv` | territory | `territory_id` |
| `product.csv` | product (with list price and standard cost) | `product_id` |
| `customer.csv` | customer (an individual or a store) | `customer_id` |
| `sales_order.csv` | order, in the Internet or Reseller channel | `order_id` |
| `sales_order_line.csv` | product line within an order | `order_id` with `line_no` |
| `territory_target.csv` | sales target for a territory in a fiscal year | `territory_id` with `fiscal_year` |

`aw_extract.sqlite` holds the same six tables in one SQLite file. Revenue for a line is `quantity * unit_price * (1 - discount)`. Gross margin is revenue minus `quantity * standard_cost`, divided by revenue.

Instructors can rebuild everything with `python3 build_aw_extract.py` (Python 3.9 or later and `numpy`, ideally the version noted in the script, because numpy doesn't promise the same random numbers across versions). It also writes `aw_answer_key.md` into the `facilitator` folder.
