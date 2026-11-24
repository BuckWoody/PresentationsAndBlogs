<img width="150" style="float: right; margin: 0px 15px 15px 0px;" src="../graphics/logo.png">

# Workshop: Data Literacy

#### <i>Using Data To Make Intelligent Decisions</i>

<p style="border-bottom: 1px solid lightgrey;"></p>

<img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/textbubble.png?raw=true"> <h2>3 - Work with Data</h2>

| Minutes | What happens |
|---|---|
| 0 to 9 | Lecture: the data work cycle, the kinds of tools, and how data is stored |
| 9 to 18 | Activity 1: Clean the Raw Files |
| 18 to 26 | Lecture: shaping, combining, and summarizing (and how joins go wrong) |
| 26 to 37 | Activity 2: Combine and Tie Out |
| 37 to 40 | Skeptic's checkpoint: check the helper |

> **Starting here?** You need the Lantern Peak case files (the `case-data` folder), especially the `raw` folder. A quick catch-up: Lantern Peak Supply Co. is a fictional online retailer of camping and hiking gear. Its finance report and its order system disagree on revenue, and the order files are messy (duplicate rows, test orders, two date formats, and inconsistent labels). If you'd rather skip ahead to a cleaned state, the `clean_csv` folder holds the result of this module's cleaning.

<p style="border-bottom: 1px solid lightgrey;"></p>

When you learned to write, you picked up a pencil and learned to form the letters. The tools you use to work with data play the same role. You can work with data using only your head, or pencil and paper, and while you're learning, that's often the best way. But sooner or later you'll want something more powerful. This module is about choosing tools well and using them carefully. Here you'll learn the moves that every tool makes, whatever the product.

<img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/pencil2.png?raw=true"> <h2>3.1 The Data Work Cycle and Its Tools</h2>

Nearly every data task follows the same loop, no matter which tool you use:

1. **Obtain** the data (and log where it came from, as you did in Module 02).
2. **Inspect** it: how many rows, what columns, what values, what's missing.
3. **Clean** it: fix the problems you found.
4. **Shape** it: filter, sort, and add the columns you need.
5. **Combine** it with other data.
6. **Summarize** it: counts, totals, averages.
7. **Document** what you did.

Two rules protect you through all seven. **Never edit the raw data.** Work on a copy, so you can always start over and so anyone can check you. And **make every change repeatable**: a formula, a query, a lookup table, or a script, never a hand edit you can't reproduce. If you can't redo it, you can't defend it.

**Kinds of tools.** Every tool you'll meet does the same three things: it connects to data, lets you model or transform it, and lets you display or share the result.

| Kind of tool | What it is | Good for | Watch out for |
|---|---|---|---|
| Spreadsheet | A grid of cells with formulas, sorting, filtering, summary tables, and charts | Exploring small to medium data, quick answers, and sharing with people who already have one | Hand edits leave no trail, formulas that copy wrong, row limits, silent date conversions |
| Query language (SQL) | Statements that ask questions of tables in a database | Large tables, combining tables, and repeatable questions | Small differences between database products (called *dialects*) |
| Programming language or notebook (Python and R are two popular examples) | Code that loads, transforms, analyzes, and charts data | Full control, repeatability, statistics, and machine learning | A steeper learning curve |
| Business intelligence (BI) or visualization tool | Software that connects to data, models it, and builds interactive reports and dashboards | Standard reports many people use from the same governed data | Definitions buried inside the tool where nobody can see them |
| AI assistant | A chat tool that writes formulas, queries and code, and explains errors | Speeding up routine work and learning syntax | Confident wrong answers, invented column names, hidden assumptions, and privacy |

Which one should you pick? If everyone who needs the result already has the same spreadsheet and the data is modest, a spreadsheet will do. If you need exact control and have the time and skill, use code. If you want standard reports on central, governed data that many people share, use a BI tool. Most analysts use several, and each one teaches you something different about the same data.

**How data sits in files.** Before any tool can read a file, it needs to know how the file is laid out.

| Format | What it looks like | Things to know |
|---|---|---|
| Delimited text (CSV, TSV) | One row per line, with values separated by commas or tabs | You must know the delimiter, whether there's a header row, how quotes work, and the *encoding* (UTF-8 is the usual choice today, and plain ASCII is a subset of it) |
| Fixed-width text | Every field takes a set number of characters | Compact, but you need the layout document to read it |
| JSON | Nested names and values, such as `{"name": "Lantern Peak", "regions": ["Northeast", "West"]}` | Flexible, and the standard way most web services exchange data |
| XML | Data wrapped in opening and closing tags | Verbose but self-describing |
| Database file or engine | A binary file managed by software | Fast, shared by many users, and protected by rules |

A *database engine* is software that runs as a service and manages access to data for many users at once. There are two broad families. A *relational* database (such as SQLite, the free, single-file engine this workshop uses) stores data in tables joined by keys and enforces rules about what's allowed, which is called *integrity*. A *NoSQL* ("not only SQL") database gives up some of that structure to handle huge or irregular data across many machines. The main kinds are document, key-value, column, and graph databases, and some of them relax consistency, which means a read might not see the very latest write. For most business analysis you'll meet relational databases first.

Whatever the engine, you'll do four things to data: **C**reate it, **R**ead it, **U**pdate it, and **D**elete it (together, *CRUD*). The database's job is to let you do those four things while protecting the data from mistakes.

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/point1.png?raw=true"><b>Optional Try It: See CRUD and Integrity in a Browser (5 minutes)</b></p>

The `tools/data-workbench` folder holds a small web page that runs on your own computer and lets you change a *copy* of the Lantern Peak database. It needs Python (see its README for the setup). It's not required for the workshop, but it makes integrity visible.

**Steps:**

1. Start the workbench and open the `customers` table.
2. **Create:** add a new customer. Leave `customer_id` blank so the database numbers it for you.
3. **Update:** edit your new customer's region. Open the Change log and find your edit.
4. **Delete (refused):** try to delete customer 1001. The database says no. Why? (Look at the `orders` table.)
5. **Delete (allowed):** delete the customer you created. Why does that one work?
6. Click Reset copy to put everything back.

**Leader's view:** In a real system, who is allowed to create, update, and delete which records? When something changes, can your team tell you who changed it and when? The change log shows what a good answer looks like.

<p style="border-bottom: 1px solid lightgrey;"></p>

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/point1.png?raw=true"><b>Activity 1: Clean the Raw Files</b></p>

In Module 02 you learned that Lantern Peak's order system was loaded twice, holds test orders, and mixes date formats. Now you'll fix the raw files (on a copy) and keep a log of every change.

<p><img style="margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/checkmark.png?raw=true"><b>Steps</b></p>

**Hands-on:**

1. Copy the `raw` folder to a working folder. You won't touch the originals.
2. **Customers.** Open `customers_raw.csv` and standardize three columns. `region` has 24 spellings for six real regions. `email_opt_in` has eight spellings of yes and no, and should become 1 or 0. `age_band` marks a missing value five different ways, and should use one. A *lookup table* (raw spelling in one column, clean value in the next) works well, because it's reusable and it documents your decisions.
3. **Orders.** Open `orders_raw.csv` and handle four things, *in this order*:
   - remove the duplicate rows (keep one row per `order_id`),
   - remove the test orders (`customer_id` of 0),
   - set the cancelled orders aside, but keep them in a separate list,
   - fix the dates in the oldest rows. Orders from January through March 2023 use month/day/year (03/01/2023 means March 1). Convert them to year-month-day (2023-03-01).
4. Run a sanity check on dates. Order numbers rise over time, so sort by `order_id` and confirm that the dates rise with them.
5. Keep a **cleaning log** with one line per issue: what was wrong, how you found it, how many rows it touched, the rule you applied, and the effect on the data.

**Check yourself:** after cleaning you should have 15,859 orders, of which 328 are cancelled and 15,531 are shipped. (If your spreadsheet shows a date as a real date value, check it on a row where the day is 12 or less, such as 03/01/2023. Some spreadsheets guess the day and month order from your computer's regional settings. If yours does, import that column as text.)

**Leader's view:** Ask your team for the cleaning log behind any dataset that feeds an important report. "What did you change, how many rows did it touch, and who approved the rules?" A good answer is a table. "We cleaned it" is not an answer. Then ask which cleaning decisions change a number the business cares about.

<p style="border-bottom: 1px solid lightgrey;"></p>

<img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/pencil2.png?raw=true"> <h2>3.2 Shaping, Combining, and Summarizing</h2>

Clean data is a starting point. To answer a question, you'll usually reshape it, bring other data in, and boil it down.

**Shape.** *Filter* to the rows you want, *sort* them, and *derive* new columns from existing ones (for example, the month of a date, or a margin from a price and a cost). You can also change a column's *type*, such as text to number.

**Combine.** There are two main ways to bring data together.

- *Stacking* adds the rows of one table under another when they share the same layout.
- *Joining* adds columns by matching a key. In a spreadsheet you'd do that with a lookup. In a database, it's a *join*. A join that keeps every row of the first table, even when there's no match, is called a *left* join. A join that keeps only matches is an *inner* join.

Joins have a classic failure. If the key you match on isn't unique on one side, each matching row gets repeated, and your totals inflate. People call that a *fan-out*. Lantern Peak has one waiting for you: the duplicate order rows would double-count their order lines if you joined them to the line items. The habit that catches it is simple. **Count the rows and total the amounts before the join, and again after.** If a total changes when it shouldn't, stop and find out why.

**Summarize.** To summarize, you *group* rows and *aggregate* a measure for each group: count, sum, average, minimum, or maximum. Spreadsheets call the tool a pivot table or summary table, and databases call it a GROUP BY. Remember the grain from Module 01. When you summarize orders by month, you change the grain from one row per order to one row per month, so you've changed what a row means.

**Check your work by tying out.** Whenever you can, compare a total you built to a total someone else trusts, and explain every difference. That is the fastest way to find out whether your cleaning and combining were right.

**AI assistants as a helper.** An assistant is quite good at writing the formula or the query for a step you've already worked out, and at explaining an error message. Give it your *data dictionary* (the column names and what they mean) and a few made-up example rows, and keep your real data out of it, especially if the data is confidential or customer-related. Then test what it gives you, the same way you'd test a new colleague's work: run it on cases where you already know the answer.

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/point1.png?raw=true"><b>Activity 2: Combine and Tie Out</b></p>

You'll rebuild the finance team's monthly net revenue from the order and returns files, and see whether your numbers match theirs.

<p><img style="margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/checkmark.png?raw=true"><b>Steps</b></p>

**Hands-on:**

1. Start from your cleaned shipped orders. (If you didn't finish Activity 1, use `clean_csv/orders.csv` and keep only the rows where `status` is shipped.) Add a column for the *ship month* (year and month of `ship_date`), and total `order_total` by ship month.
2. Open `raw/returns_raw.csv`. Add a column for the *return month* (year and month of `return_date`), and total `refund_amount` by return month.
3. Combine the two: for each month, net revenue is shipped total minus refunds. Leave out any month after December 2025.
4. Compare your 36 monthly totals with `raw/finance_monthly_revenue.csv`. What is the largest difference? If a month is off, which kind of problem is the likely cause (dates, duplicates, or cancelled orders)?
5. **Stretch (the fan-out):** join the *uncleaned* `orders_raw.csv` to `order_items_raw.csv` on `order_id`, and compare the total `line_total` before and after the join. By how much did it inflate, and why?

**Leader's view:** Ask your team to show you the *tie-out* for your most important report: which trusted total does it match, how closely, and what explains any gap? A good answer sounds like "We match finance to the cent in all 36 months." A gap with no explanation is a reason to keep asking.

<details>
<summary><b>Optional: the SQLite path (for anyone who wants to try SQL)</b></summary>

SQLite is a free, single-file database. You can use its command-line shell (`sqlite3`) or any SQLite viewer. These commands load the raw files into a new database and repeat Activities 1 and 2 with SQL. Run them from the `case-data` folder.

When SQLite imports a CSV file it creates every column as text, so the queries below use `CAST` to turn text into numbers where it matters.

```
sqlite3 work.sqlite
.mode csv
.import raw/orders_raw.csv orders_raw
.import raw/order_items_raw.csv order_items_raw
.import raw/returns_raw.csv returns_raw
.import raw/customers_raw.csv customers_raw
.import raw/finance_monthly_revenue.csv finance_monthly_revenue
```

**Inspect.** Rows against distinct order numbers (you should see 16,094 and 15,904):

```sql
SELECT COUNT(*), COUNT(DISTINCT order_id) FROM orders_raw;
```

**Clean the orders.** `DISTINCT` removes exact duplicate rows, the `WHERE` drops test and cancelled orders, and the `CASE` converts the month/day/year dates:

```sql
CREATE VIEW orders_clean AS
SELECT DISTINCT
  order_id, customer_id,
  CASE WHEN order_date LIKE '%/%'
       THEN substr(order_date, 7, 4) || '-' || substr(order_date, 1, 2) || '-' || substr(order_date, 4, 2)
       ELSE order_date END AS order_date,
  CASE WHEN ship_date LIKE '%/%'
       THEN substr(ship_date, 7, 4) || '-' || substr(ship_date, 1, 2) || '-' || substr(ship_date, 4, 2)
       ELSE ship_date END AS ship_date,
  channel, status,
  CAST(shipping_fee AS REAL) AS shipping_fee,
  CAST(order_total AS REAL) AS order_total
FROM orders_raw
WHERE customer_id <> '0' AND status <> 'cancelled';
```

**Clean the regions.** This maps all 24 spellings onto six values, and flags any spelling it doesn't recognize:

```sql
SELECT
  CASE replace(replace(replace(lower(trim(region)), ' ', ''), '.', ''), '-', '')
    WHEN 'ne' THEN 'Northeast' WHEN 'northeast' THEN 'Northeast'
    WHEN 'se' THEN 'Southeast' WHEN 'southeast' THEN 'Southeast'
    WHEN 'mw' THEN 'Midwest'   WHEN 'midwest'   THEN 'Midwest'
    WHEN 'sw' THEN 'Southwest' WHEN 'southwest' THEN 'Southwest'
    WHEN 'w'  THEN 'West'      WHEN 'west'      THEN 'West'  WHEN 'western' THEN 'West'
    WHEN 'nw' THEN 'Northwest' WHEN 'northwest' THEN 'Northwest' WHEN 'pacificnw' THEN 'Northwest'
    ELSE 'CHECK ME: ' || region
  END AS region_clean,
  COUNT(*) AS customers
FROM customers_raw
GROUP BY 1
ORDER BY 1;
```

**Tie out.** Net revenue by month, then a comparison with finance (an empty result means every month matches to the cent):

```sql
CREATE VIEW my_net_revenue AS
WITH sales AS (
  SELECT substr(ship_date, 1, 7) AS month, SUM(order_total) AS amount
  FROM orders_clean GROUP BY 1),
refunds AS (
  SELECT substr(return_date, 1, 7) AS month, SUM(CAST(refund_amount AS REAL)) AS amount
  FROM returns_raw GROUP BY 1)
SELECT s.month, ROUND(s.amount - COALESCE(r.amount, 0), 2) AS net_revenue
FROM sales s LEFT JOIN refunds r USING (month)
WHERE s.month <= '2025-12';

SELECT f.month, f.net_revenue AS finance, m.net_revenue AS mine
FROM finance_monthly_revenue f
LEFT JOIN my_net_revenue m ON m.month = f.month
WHERE m.net_revenue IS NULL OR ABS(m.net_revenue - CAST(f.net_revenue AS REAL)) > 0.005;
```

**See the fan-out.** The first number is what the join produces, and the second is the true total of all lines. The difference is $56,646.70, the lines of the duplicated orders, counted twice:

```sql
SELECT
  (SELECT ROUND(SUM(CAST(i.line_total AS REAL)), 2)
     FROM orders_raw o JOIN order_items_raw i ON i.order_id = o.order_id) AS after_join,
  (SELECT ROUND(SUM(CAST(line_total AS REAL)), 2) FROM order_items_raw) AS true_total;
```

</details>

<p style="border-bottom: 1px solid lightgrey;"></p>

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/point1.png?raw=true"><b>Skeptic's Checkpoint: Check the Helper</b></p>

Suppose you ask an AI assistant (or a quick-talking colleague) for a formula that converts the old 2023 dates to year-month-day. It hands you one with great confidence. Before you trust it, run it on three rows whose true dates you already know:

| Raw date | Should become |
|---|---|
| 02/01/2023 | 2023-02-01 |
| 03/01/2023 | 2023-03-01 |
| 01/13/2023 | 2023-01-13 |

If the formula turns the first one into 2023-01-02, it quietly assumed day-first dates. Nothing in the answer would have warned you. The third row can only be read one way, but the first two can be read two ways, and those are the rows that catch the mistake.

**Do this now (two minutes):** Write down one "known answer" test for the last formula or query you trusted without testing. What would it have shown?

<details>
<summary><b>Instructor notes</b></summary>

**Timing (40 minutes).** Lecture 3.1 for 9 minutes, Activity 1 for 9, lecture 3.2 for 8, Activity 2 for 11, checkpoint for 3. The optional Try It (5 minutes) isn't in the 40, so run it only if everyone has Python set up, or demo it on the projector.

**Talk track.**
- Open with the pencil-and-paper analogy and the seven-step cycle. Push the two rules: never edit raw data, and make every change repeatable.
- Spend most of the tool discussion on the question "which kind of tool fits this job?" Resist any urge to demo a favorite product.
- Show the fan-out on the projector. It's the single best argument for "count and total before and after."
- On AI assistants, give learners a rule of thumb: share structure (the data dictionary), keep content (real records) private, and always test on known cases.

**Answer key, Activity 1.**
- Region: 24 spellings become 6. Email opt-in: 8 spellings become 1 or 0. Age band: 5 spellings of "missing" become one.
- Orders: 16,094 rows loaded, 15,904 distinct order numbers (190 duplicates removed), 45 test orders removed (15,859 left), 328 of those are cancelled (15,531 shipped). The dates for 400 orders from January to March 2023 are month-first.
- A common slip is to convert dates by treating the first number as the day. A good spot check is that order numbers rise with time.

**Answer key, Activity 2.** The recipe (shipped, de-duplicated, non-test orders, by ship month, minus refunds by return month, through December 2025) matches the finance report in all 36 months, to the cent. If a learner leaves out the date fix, the early 2023 months won't tie out. If they leave out the duplicate removal, every month with a duplicate will be too high. The stretch: the join produces $4,538,122.96 against a true line total of $4,481,476.26, an inflation of $56,646.70 (the lines of the 190 duplicated orders).

**Answer key, checkpoint.** The three test rows are real orders (100114, 100257 and 100039). The right answers are in the table. The usual wrong answer to the first is 2023-01-02.

**Optional Try It.** Customer 1001 has orders, so the database refuses to delete them (the `orders` table points to the customer). A new customer has no orders, so the delete works. The change log records the create, the edit (old and new values), and the delete, but not the refused delete. The README in `tools/data-workbench` covers setup.

**Common pitfalls.**
- Some spreadsheets convert text that looks like a date into a real date using the computer's regional settings, which can silently turn 03/01/2023 into the wrong day. Have learners import those columns as text.
- Learners subtract cancelled orders before removing duplicates (the order in Module 02 matters here too).
- A learner who edits the raw file loses the ability to redo the work. Reinforce the copy habit.

**If you need to cut time.** Drop the stretch step in Activity 2, or give learners the lookup table for the customer labels.

</details>

<p style="border-bottom: 1px solid lightgrey;"></p>

<p><img style="margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/owl.png?raw=true"><b>For Further Study</b></p>
<ul>
 <li><a href="https://www.sqlite.org/" target="_blank">SQLite</a> (the free, single-file database used in this workshop)</li>
 <li><a href="https://www.sqlite.org/cli.html" target="_blank">The SQLite command-line shell</a> (including the .import command)</li>
 <li>The README in <code>tools/data-workbench</code> for the optional browser tool</li>
</ul>

<p style="border-bottom: 1px solid lightgrey;"></p>

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/geopin.png?raw=true"><b>Next Steps</b></p>

Next, continue to <a href="04-see-what-happened.md"><i>Module 04 - See What Happened</i></a>.
