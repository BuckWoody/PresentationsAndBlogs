<img width="150" style="float: right; margin: 0px 15px 15px 0px;" src="../graphics/logo.png">

# Workshop: Data Literacy

#### <i>Using Data To Make Intelligent Decisions</i>

<p style="border-bottom: 1px solid lightgrey;"></p>

<img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/textbubble.png?raw=true"> <h2>1 - Data Basics</h2>

| Minutes | What happens |
|---|---|
| 0 to 9 | Lecture: what data is, and the kinds of data you'll meet |
| 9 to 16 | Activity 1: Know Your Fields |
| 16 to 23 | Lecture: how data is organized (tables, keys, and the data dictionary) |
| 23 to 28 | Activity 2: What Does One Row Mean? |
| 28 to 30 | Skeptic's checkpoint: definitions and units |

> **Starting here?** You don't need anything from the other modules. Open the Lantern Peak case files (the `case-data` folder) and keep `data_dictionary.csv`, the `clean_csv` folder and the `raw` folder handy. If you skipped Module 00, here is the setup: Lantern Peak Supply Co. is a fictional online retailer of camping and hiking gear, and you're helping its leadership team decide where to spend next year's $150,000.

<p style="border-bottom: 1px solid lightgrey;"></p>

When you learned to read, you started with the letters of the alphabet. They're small, they don't mean much alone, and everything else gets built from them. Data has an alphabet too, and this module is where you learn it. Before you can find data, trust it, or analyze it, you need to know what it is, what kinds there are, and how it's laid out.

<img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/pencil2.png?raw=true"> <h2>1.1 Defining Data</h2>

Let's start at the beginning: what is data? [Merriam-Webster](https://www.merriam-webster.com/dictionary/data) describes it as factual information, such as measurements or statistics, that you use as a basis for reasoning, discussion, or calculation. Put simply, data is one or more facts that someone wrote down.

Facts become data when you record them. Data becomes information when you put it in context. Information becomes knowledge when you absorb it and can apply it, and knowledge applied well becomes wisdom. Wisdom is the point of this whole workshop, because wise decisions are what data literacy is for.

| Level | What it looks like at Lantern Peak |
|---|---|
| Fact | A customer bought a brown Kid Explorer Pack on May 3, 2024. |
| Data | The fact, recorded as a row: order 103999, product 26, quantity 1, date 2024-05-03. |
| Information | Orders in May ran above April, which fits the start of camping season. |
| Knowledge | Demand climbs from spring into summer and peaks in November and December. |
| Wisdom | Order inventory and schedule staff early for the holiday peak, and don't judge a January slump against December. |

<p style="border-bottom: 1px solid lightgrey;"></p>

<img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/pencil2.png?raw=true"> <h2>1.2 Kinds of Data</h2>

Two general types of data come up constantly: *quantitative* and *qualitative* (sometimes called *categorical*). Quantitative data is numeric. Qualitative data describes an attribute.

**1** order, **$138.97**, **3** tents = quantitative.
**Brown** pack, **Southwest** region, **shipped** status = qualitative.

You'll use arithmetic on the quantitative data and use the qualitative data to describe and group it. You can also cross over. The names of the regions are qualitative, but if you count the customers in each one, you've produced numbers. That distinction matters because the kind of data decides which analysis makes sense, and the wrong analysis gives you confident nonsense.

Inside those two types, data sits on one of four *scales*. The scale tells you what you can safely do with it.

| Scale | What it tells you | Lantern Peak example | Safe to do |
|---|---|---|---|
| Nominal | A name or label, with no order | region, color, order status | Count, group, compare for "same or different" |
| Ordinal | An order, but the gaps between steps aren't equal | satisfaction rating (1 to 5), age band | Rank, find the middle; be careful with averages |
| Interval | Equal gaps, but the zero is arbitrary | order date, temperature in degrees | Subtract to get differences |
| Ratio | Equal gaps and a true zero | order total, quantity, days between orders | Everything above, plus add, average and form ratios |

One trap deserves its own warning. Some numbers are really labels. A `customer_id` or a ZIP code looks numeric, but it's a name that happens to use digits. A spreadsheet will happily average customer IDs for you, and the answer means nothing at all.

Most of this workshop uses *structured* data, the rows-and-columns kind. A lot of the world's data is *unstructured*, like survey comments, emails, and photos, and some sits in between (*semi-structured*, like JSON and XML files). You'll touch on those in Module 03.

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/point1.png?raw=true"><b>Activity 1: Know Your Fields</b></p>

Lantern Peak's data dictionary lists every field in the company's tables. In this activity you'll decide what kind of data each field holds, and then tackle a messy-labels problem that shows up in nearly every real dataset.

<p><img style="margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/checkmark.png?raw=true"><b>Steps</b></p>

**Hands-on:**

1. Open `case-data/data_dictionary.csv` in your spreadsheet application.
2. For each of these ten fields, write down whether it's quantitative or qualitative, and which of the four scales it sits on: `customers.customer_id`, `customers.acquired_date`, `customers.region`, `customers.age_band`, `orders.order_total`, `orders.status`, `order_items.quantity`, `order_items.discount_pct`, `survey_responses.rating`, `products.color`.
3. Which of the ten would a spreadsheet let you average even though you shouldn't?
4. Now the messy-labels problem. Open `case-data/raw/products_raw.csv` and list the different values you find in the `color` column (sorting or filtering helps). Group them into a short list of standard colors. Which values were hard to place (is "auburn" red? is "Dark Blue" navy or blue?), and what rule did you use for each judgment call? Write the rule down.

**Leader's view:** Pick any three fields from the data dictionary and ask your team, "Could I add these up, average them, or only count them?" A good answer names the scale and the kind of arithmetic that is safe. A vague answer is your cue to ask for the definition.

<p style="border-bottom: 1px solid lightgrey;"></p>

<img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/pencil2.png?raw=true"> <h2>1.3 How Data Is Organized</h2>

Structured data lives in *tables*. A table is a set of *rows* (also called records) and *columns* (also called fields or attributes). Where a row and column meet is a *cell*, and it holds a single value, which some people call a *datum*. You'll hear all of these terms used interchangeably, so don't let the vocabulary trip you up.

Tables rarely stand alone. Lantern Peak keeps customers in one table and orders in another, and a *key* connects them. Each customer has a `customer_id`, and each order carries the `customer_id` of whoever placed it. Follow the key and you can find everything one customer bought. A spreadsheet can do this with lookups, and a database does it with joins (more on both in Module 03).

Every table should come with a description of itself. That description is *metadata*, which is simply data about data, and the usual way to keep it is a *data dictionary*. A good one tells you what each field means, what type of data it holds, the units, the allowed values, and who owns it. [The U.S. Geological Survey has a short guide](https://www.usgs.gov/data-management/data-dictionaries) to what belongs in one. If a dataset arrives without a dictionary, ask for one before you analyze anything.

The single most useful question you can ask of any table is this: *what does one row mean?* People call that the *grain* of the table. Lantern Peak's tables each have a different grain.

| Table | One row is a single... |
|---|---|
| customers | customer account |
| orders | order |
| order_items | product line within an order |
| returns | returned line from an order |
| products | product in the catalog |

Grain matters because counting rows only answers your question if the rows are what you're counting. Count the rows in `order_items` and call that the number of orders, and you'll overstate orders by roughly 70 percent, because most orders have more than one line.

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/point1.png?raw=true"><b>Activity 2: What Does One Row Mean?</b></p>

You'll predict the grain of each Lantern Peak table, and then check your prediction by counting.

<p><img style="margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/checkmark.png?raw=true"><b>Steps</b></p>

**Hands-on:**

1. Open the five files in `case-data/clean_csv`: `customers`, `products`, `orders`, `order_items` and `returns`.
2. For each file, finish the sentence "One row is a single ____." Use the data dictionary to make your prediction first.
3. Check yourself. Count the rows in each file (most spreadsheets show this in the status bar). Then count the *distinct* values of its key: `customer_id` for customers, `order_id` for orders, `return_id` for returns, and both `order_id` and `line_no` together for order_items. Do the counts match your prediction?
4. Work out the average number of lines per order (the rows in `order_items` divided by the rows in `orders`).

**Leader's view:** Ask your team, "In the table behind our most-used dashboard, what does one row mean? If we count the rows, what are we counting?" A good answer is one plain sentence. A hesitant answer tells you the dashboard may be counting something you didn't intend.

<p style="border-bottom: 1px solid lightgrey;"></p>

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/point1.png?raw=true"><b>Skeptic's Checkpoint: Definitions and Units</b></p>

Two questions will save you more trouble than any formula. *What exactly is being counted? In what units?*

In 1999, NASA lost the Mars Climate Orbiter, a spacecraft that cost around $125 million. One team's software produced thruster data in imperial units (pound-seconds) and the navigation team's software expected metric units (newton-seconds). The arithmetic on each side was fine. The two sides just assumed different units for the same numbers, and small errors piled up over nine months of flight. [NASA's Jet Propulsion Laboratory announced the likely cause here](https://www.jpl.nasa.gov/news/mars-climate-orbiter-team-finds-likely-cause-of-loss/), and [the official investigation report is here](https://llis.nasa.gov/llis_lib/pdf/1009464main1_0641-mr.pdf).

Your own organization probably has a version of this. Lantern Peak's `order_total` leaves out shipping and tax, for instance, and "customer" could mean a person, an account, or a household.

**Do this now (one minute):** Write down two different things your own organization could mean by the word "customer." If you came up with two, you've just found the first place a report could mislead you.

<details>
<summary><b>Instructor notes</b></summary>

**Timing (30 minutes).** Lecture 1.1 and 1.2 for 9 minutes, Activity 1 for 7, lecture 1.3 for 7, Activity 2 for 5, checkpoint for 2. If you run long, move step 4 of Activity 1 (the color labels) to a take-home.

**Talk track.**
- Anchor everything in the reading analogy: this module is the alphabet.
- Walk the Lantern Peak knowledge ladder slowly. Learners remember "fact, data, information, knowledge, wisdom" when it's tied to one order.
- For the scales, ask the room which scale a satisfaction rating of 1 to 5 sits on, then ask if "3.8 stars" is a meaningful thing to report. Expect a good argument. Ordinal averages are common and defensible in some settings, but the gaps between steps aren't guaranteed to be equal.
- Make the customer_id point with a joke if you like: it's the one average no one should ever compute.

**Answer key, Activity 1.**
- customer_id: qualitative (a label), nominal. acquired_date: interval. region: nominal. age_band: ordinal. order_total: quantitative, ratio. status: nominal. quantity: ratio (a count). discount_pct: ratio. rating: ordinal. color: nominal.
- Step 3: customer_id (and arguably rating, depending on your stance on ordinal averages).
- Step 4: `products_raw.csv` holds 30 different spellings for 10 base colors. Expect real disagreement over overlaps such as Dark Blue (Navy or Blue), Gold (Yellow or Orange), and Charcoal (Gray or Black). The point isn't a single right answer. The point is a written rule. The cleaned catalog, in `clean_csv/products.csv`, uses the ten base colors.

**Answer key, Activity 2.**

| File | Rows | Distinct key values | Grain |
|---|---:|---:|---|
| customers | 6,900 | 6,900 | one customer account |
| products | 60 | 60 | one catalog product |
| orders | 15,859 | 15,859 | one order |
| order_items | 26,864 | 26,864 (order_id with line_no) | one product line within an order |
| returns | 2,361 | 2,361 | one returned line |

Average lines per order: 26,864 / 15,859 is about 1.69. Counting `order_items` rows as orders overstates orders by about 69 percent.

**Leader's view tip.** Executives usually enjoy the "what does one row mean?" question. Suggest they try it in their very next dashboard review.

**Looking ahead.** In Module 02 learners will discover that the *raw* `orders_raw.csv` does not behave this well (it has more rows than distinct order IDs). If anyone asks why the clean files here have no such problem, tell them to hold the thought.

</details>

<p style="border-bottom: 1px solid lightgrey;"></p>

<p><img style="margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/owl.png?raw=true"><b>For Further Study</b></p>
<ul>
 <li><a href="https://www.usgs.gov/data-management/data-dictionaries" target="_blank">USGS: What's in a Data Dictionary?</a></li>
 <li><a href="https://www.jpl.nasa.gov/news/mars-climate-orbiter-team-finds-likely-cause-of-loss/" target="_blank">NASA JPL: Mars Climate Orbiter team finds likely cause of loss</a></li>
 <li><a href="https://llis.nasa.gov/llis_lib/pdf/1009464main1_0641-mr.pdf" target="_blank">NASA Mishap Investigation Board: Phase I report</a> (a PDF)</li>
 <li><a href="https://spectrum.ieee.org/why-the-mars-probe-went-off-course" target="_blank">IEEE Spectrum: why the Mars probe went off course</a> (the story involved more than a units mix-up)</li>
 <li><a href="https://www.khanacademy.org/math/statistics-probability" target="_blank">Khan Academy: Statistics and probability</a> (a good companion to the scales in 1.2)</li>
</ul>

<p style="border-bottom: 1px solid lightgrey;"></p>

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/geopin.png?raw=true"><b>Next Steps</b></p>

Next, continue to <a href="02-find-and-trust-data.md"><i>Module 02 - Find and Trust Data</i></a>.
