<img width="150" style="float: right; margin: 0px 15px 15px 0px;" src="../graphics/logo.png">

# Workshop: Data Literacy

#### <i>The Lantern Peak Supply Co. Case Files</i>

<p style="border-bottom: 1px solid lightgrey;"></p>

<img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/textbubble.png?raw=true"> <h2>About the Case Files</h2>

Lantern Peak Supply Co. is fictional, and so is every customer, order and number in these files. Any resemblance to a real company is a coincidence. The data covers January 1, 2023 through December 31, 2025 (a few late-December orders ship in January 2026). Amounts are in US dollars and dates use the year-month-day format (2025-03-18).

Everything here works on a plain computer with no accounts and no internet connection. A spreadsheet application opens the CSV files. The SQLite file is optional and needs a free viewer or the `sqlite3` command line.

<p style="border-bottom: 1px solid lightgrey;"></p>

<img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/pencil2.png?raw=true"> <h2>What Is Here</h2>

| Path | What it holds | Used in |
|---|---|---|
| `data_dictionary.csv` | Every field, what it means, and a real example value | Module 01 onward |
| `raw/` | The messy files as they came out of the source systems | Modules 02 and 03 |
| `clean_csv/` | The same tables after cleaning, as CSV files | Modules 01 and 04 to 08 |
| `lantern_clean.sqlite` | The cleaned tables, plus the loyalty, marketing, survey, churn and prepared summary tables, in one SQLite database | Module 03 (optional SQL) and 04 to 08 |
| `sources/` | `source_notes.md`: descriptions of the five places leadership gets its numbers | Module 02 |
| `supplements/` | Loyalty members, monthly marketing, a customer survey, a vendor's churn pilot, the four Anscombe datasets, and three prepared summary tables (`customer_spend_summary`, `survey_audit`, `repeat_cohort`) | Modules 04 to 07 |
| `adventure-works/` | An optional, invented extract of Adventure Works Cycles for "Go further" activities (read its README first) | Optional |
| `build_case_data.py` and `make_images.py` | Optional. Rebuild the data and the chart images (seeded, and identical on the same numpy version) | Instructors |

The answer keys live in the separate `facilitator` folder. Keep that folder out of the learners' copy.

**Two states of the data.** Modules 02 and 03 use the `raw` folder, which has real-world problems on purpose. From Module 04 on, everyone uses the cleaned state, so a learner who jumps straight to a later module never needs the earlier exercises. (If you're taking the full path, your own cleaning in Module 03 should end up looking like the cleaned files.)

<p style="border-bottom: 1px solid lightgrey;"></p>

<img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/pencil2.png?raw=true"> <h2>The Tables</h2>

| Table | One row is a single... | Key |
|---|---|---|
| `customers` | customer account | `customer_id` |
| `products` | catalog product | `product_id` |
| `orders` | order | `order_id` |
| `order_items` | product line within an order | `order_id` with `line_no` |
| `returns` | returned line from an order | `return_id` |
| `loyalty_members` | customer who joined the loyalty program | `customer_id` |
| `marketing_monthly` | calendar month | `month` |
| `survey_responses` | customer survey reply | `response_id` |
| `churn_model_scores` | customer scored in a vendor pilot | `customer_id` |
| `customer_spend_summary` | consumer customer acquired before 2025 (prepared by the data team) | `customer_id` |
| `survey_audit` | customer who was emailed the satisfaction survey (prepared by the data team) | `customer_id` |
| `repeat_cohort` | consumer customer whose first order fell in January to September of 2024 or 2025 (prepared by the data team) | `customer_id` |

The `raw` folder also holds `finance_monthly_revenue.csv`, a monthly revenue report from the finance system, which is a separate source from the order system.

<p style="border-bottom: 1px solid lightgrey;"></p>

<img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/pencil2.png?raw=true"> <h2>Opening the SQLite File (Optional)</h2>

SQLite is a free database engine that keeps everything in one file. Pick any SQLite viewer, or use the command line:

```
sqlite3 lantern_clean.sqlite
.tables
SELECT COUNT(*) FROM orders;
.quit
```

Module 03 walks through a handful of queries. Nobody has to use SQL to finish the workshop, because every exercise also works with the CSV files in a spreadsheet.

**Rebuilding the data (instructors).** With Python 3.9 or later and `numpy` installed, run `python3 build_case_data.py` from this folder. It recreates the database, the CSV files, the data dictionary and the facilitator answer key, and it checks that the cleaning recipe in Module 03 still ties out to the finance report to the cent. The committed files were built with numpy 2.5.4, and numpy doesn't promise the same random numbers across versions, so the modules' numbers belong to the committed files. If you rebuild with another version, the script warns you, and you should re-check the modules against the new answer key. For the chart images in `modules/images`, install `matplotlib` and run `python3 make_images.py`.

**Browsing and editing the data.** The optional `tools/data-workbench` folder holds a small local web page for creating, reading, updating and deleting rows in a copy of the database (see Module 03).

<p style="border-bottom: 1px solid lightgrey;"></p>

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/geopin.png?raw=true"><b>Next Steps</b></p>

Return to <a href="../modules/00-start-here.md"><i>Module 00 - Start Here</i></a>.
