<img width="150" style="float: right; margin: 0px 15px 15px 0px;" src="../graphics/logo.png">

# Workshop: Data Literacy

#### <i>Using Data To Make Intelligent Decisions</i>

<p style="border-bottom: 1px solid lightgrey;"></p>

<img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/textbubble.png?raw=true"> <h2>2 - Find and Trust Data</h2>

| Minutes | What happens |
|---|---|
| 0 to 9 | Lecture: where data comes from, and what makes a source authoritative |
| 9 to 17 | Activity 1: Build a Source Log |
| 17 to 26 | Lecture: how to verify data, and the red flags to watch for |
| 26 to 37 | Activity 2: Why Do the Reports Disagree? |
| 37 to 40 | Skeptic's checkpoint: who benefits? |

> **Starting here?** You need the Lantern Peak case files (the `case-data` folder), in particular `sources/source_notes.md` and the `raw` folder. If you skipped the earlier modules, all you need to know is this: Lantern Peak Supply Co. is a fictional online retailer of camping and hiking gear, its leadership team is deciding where to spend $150,000 next year, and a table's *grain* is what one row of it means.

<p style="border-bottom: 1px solid lightgrey;"></p>

Once you can read the letters, you need something worth reading. In Module 01 you learned what data is. Now you'll learn where it comes from and, more importantly, whether to believe it. People tend to skip this step because it feels slower than analysis. It's also the step that decides whether everything after it is worth doing.

<img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/pencil2.png?raw=true"> <h2>2.1 Finding and Identifying Sources</h2>

Every number you use started somewhere. Someone measured something, a system recorded a transaction, or a person typed an answer into a form. Your job is to trace the number back to that origin.

**Primary and secondary sources.** A *primary* source is where the data was first captured: the order system that recorded the purchase, the survey you ran yourself, the sensor that took the reading. A *secondary* source is someone else's summary or analysis of primary data, such as a trade report, a vendor brochure, or a news article. Neither kind is automatically better. Primary data is closer to what really happened. Secondary data is often broader, and it can give you comparisons you could never collect yourself. What matters is knowing which one you're holding.

**Internal and external sources.** Data from inside your organization comes with an owner you can call. External data (from a government agency, a trade group, a vendor) comes with a publisher whose motives you have to figure out for yourself.

**Authoritative data.** Within an organization, the *authoritative* source for a question is the one everyone has agreed gives *the* answer. A source earns that status when it has these traits:

- It sits as close as possible to the *system of record*, the place where the fact is first captured and maintained.
- It has an *owner* who is accountable for it (and often a *steward* who looks after its quality day to day).
- Its definitions are written down, so "revenue" or "customer" means one thing.
- It has a known refresh schedule and a way to track changes.
- You can find it again. (A *data catalog* is the usual tool for that, and a shared source log is a good start.)

Lantern Peak's finance team owns the monthly revenue report, so for "how much revenue did we recognize?" that report is the authoritative source. The order system is authoritative for something else: what customers asked to buy, and when. Notice how the question picks the source.

**Finding data you don't own.** Start with the people who produce it. National statistics offices, regulators, standards bodies, universities, and open-data portals (such as [data.gov](https://www.data.gov/) for US government data) publish primary data and document how they collected it. Use more than one search engine, and don't skip your local or university library, where a research librarian can find things the open web hides. When you find a number, follow it back to its publisher, past the page that quoted it.

**A caution about AI assistants.** An assistant can suggest where to look, and it can explain what a dataset probably contains. It can also invent a plausible-sounding report, with a convincing title and a link that goes nowhere. Treat anything it tells you as a lead. Only the source itself, opened and read, counts as a source.

**Keep a log.** Write down every source you use, and the ones you rejected too: who produced it, what it measures, when you got it, and how to get it again. You'll thank yourself in a month, and so will anyone who has to check your work.

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/point1.png?raw=true"><b>Activity 1: Build a Source Log</b></p>

Lantern Peak's leadership team has been quoting numbers from five different places. You'll log each source and decide how far to trust it.

<p><img style="margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/checkmark.png?raw=true"><b>Steps</b></p>

**Hands-on:**

1. Open `case-data/sources/source_notes.md`. It describes Sources A through E.
2. Copy the source log template at the bottom into a spreadsheet or a note.
3. For each source, fill in who produced it, what it measures, why it exists, whether it is primary or secondary, and what it covers.
4. Give each source a trust rating (high, medium, or low) and write one sentence explaining why. Don't worry about being right. Worry about being able to defend your rating.
5. Pick the source you would use for each question: *"How much revenue did we recognize in 2025?"* and *"Is paid social worth more budget?"* Is there any source you'd use for both?

**Leader's view:** Think of the last number someone showed you in a board deck. Ask for its source log: the source, the owner, the date, and the definition. A good answer arrives in a minute. If the answer is "it's in a spreadsheet someone made," your next question is "who owns that spreadsheet?"

<p style="border-bottom: 1px solid lightgrey;"></p>

<img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/pencil2.png?raw=true"> <h2>2.2 Verifying Data</h2>

After you know where data comes from, you need to check that it's sound. Start with three questions about what's in front of you:

- Is it *accurate*? Accurate data lines up with the reality of the event it describes.
- Is it *representative*? Representative data was collected so that the cases you see stand for the cases you don't. A survey answered only by delighted customers isn't representative.
- Is it *sufficient*? Sufficient data has enough support behind it (enough observations, over enough time) to carry the claim being made.

Beyond those three, data quality teams usually check six dimensions. Lantern Peak's raw files show every one of them going wrong.

| Dimension | The question | What it looks like at Lantern Peak |
|---|---|---|
| Accuracy | Does it match reality? | An order total that doesn't equal the sum of its lines |
| Completeness | Is anything missing? | Age band left blank for some customers |
| Consistency | Is it the same everywhere? | One region spelled 24 different ways |
| Timeliness | Is it current enough? | Returns still arriving for recent orders |
| Validity | Does it follow the rules? | A date written month-first in some rows and year-first in others |
| Uniqueness | Is each thing recorded once? | The same order loaded twice |

**Who, what, and why.** Three questions uncover a lot about any source of information: *Who is telling me this? What exactly are they telling me? Why are they telling me this?* If a car salesperson hands you a stack of data showing the most expensive model is the best value, you'd discount it. That has nothing to do with whether the salesperson is dishonest. The salesperson earns a living from your decision, so the data in the stack was chosen to support one answer. The same logic applies to vendors, advocacy groups, and (to be fair) your own team when a result helps their project. There is no single source of "fair and balanced" information. The goal is to get as close to the origin as you can and to know the motive of everyone in between.

**Triangulate.** When a number matters, find a second source that was produced independently. If the two agree, your confidence goes up. If they disagree, don't pick the one you like. Find out *why* they disagree, because a discrepancy is information. You're about to see a good example.

**Exceptional claims require exceptional sources.** The more surprising or convenient a claim is, the better its support needs to be. These red flags should slow you down:

- No method described, or no sample size
- A vague time period, or one that was clearly picked to flatter the result
- "Selected" or "representative" examples with no explanation of how they were selected
- Key terms (like "return" or "online sales") left undefined
- A source that profits if you believe the claim
- Money from interested parties (look at the sponsors)
- A result that is too neat or too round

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/point1.png?raw=true"><b>Activity 2: Why Do the Reports Disagree?</b></p>

Lantern Peak's finance report says the company earned about $3.97 million in net revenue from 2023 through 2025. The order system's total, as loaded, says about $4.75 million. The CFO and the head of digital each say their number is right. You'll work out who is right, and in what sense.

<p><img style="margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/checkmark.png?raw=true"><b>Steps</b></p>

**Hands-on:**

1. Open `case-data/raw/finance_monthly_revenue.csv` and total the `net_revenue` column. Then open `case-data/raw/orders_raw.csv` and total `order_total`. How big is the gap?
2. Hunt for causes in `orders_raw.csv`. Use your spreadsheet's sort, filter, and "remove duplicates" features, and the sum your spreadsheet shows for a selection. Look for:
   - rows that repeat an `order_id`,
   - rows with `customer_id` 0,
   - rows whose `status` is cancelled,
   - rows whose `ship_date` falls in 2026.
3. Open `case-data/raw/returns_raw.csv` and total `refund_amount`.
4. Build a *bridge* from the order-system total to the finance total: list each cause, its dollar amount, and the running total. **Remove the duplicate rows first.** Some of the cancelled rows are duplicate copies, and if you subtract cancelled orders before removing duplicates, you'll subtract the same orders twice. Where does your bridge land?
5. Write two sentences. Which number should the CEO quote for *revenue we earned*, and which for *demand, what customers asked to buy*?

(For this activity you can ignore the dates in January through March 2023, which use a different format. You'll fix them in Module 03.)

<details>
<summary><b>Fact sheet (use this if you'd rather not dig through the files yet)</b></summary>

The data team found: 190 order numbers appear twice in the file, 45 rows have a customer number of 0 and look like checkout tests, 330 rows have the status "cancelled" (a couple of them are duplicate copies), 95 rows have a ship date in 2026, and the returns file has 2,361 refunds. Use these counts to tell you where to look, and the files to find the dollar amounts.

</details>

**Leader's view:** Your team hands you the bridge below. Your job is to judge it. For each step, decide whether it's a *data error* (something to fix) or a *definition difference* (something to document). Then ask: which steps can the order system's owner fix, and which one needs a rule agreed between finance and digital?

<details>
<summary><b>The bridge your team sends you (hands-on learners: finish your own first)</b></summary>

| Step | Amount | Running total |
|---|---:|---:|
| Order system total, all rows as loaded | $4,748,146.75 | $4,748,146.75 |
| Less: duplicate rows from a second load of the file | $56,646.70 | $4,691,500.05 |
| Less: test orders placed by the store team | $210,023.79 | $4,481,476.26 |
| Less: cancelled orders | $89,970.57 | $4,391,505.69 |
| Less: orders that shipped in January 2026 (finance reports through December) | $29,969.82 | $4,361,535.87 |
| Less: refunds for returned items | $396,072.43 | $3,965,463.44 |
| Finance report total | $3,965,463.44 | |

</details>

<p style="border-bottom: 1px solid lightgrey;"></p>

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/point1.png?raw=true"><b>Skeptic's Checkpoint: Who Benefits?</b></p>

Back to `sources/source_notes.md` and Source C, the vendor handout that says paid social earns "3x return on ad spend." Take two minutes and answer these:

1. Name three red flags in that claim (use the list in 2.2).
2. Source D, the trade group's press release, mentions that the same vendor is one of its sponsors. Does that prove the press release is wrong? What does it change about how you use it?

You aren't looking for a verdict on the vendor. You're building the habit of asking *who benefits if I believe this?* before you ask *is it true?*

<details>
<summary><b>Instructor notes</b></summary>

**Timing (40 minutes).** Lecture 2.1 for 9 minutes, Activity 1 for 8, lecture 2.2 for 9, Activity 2 for 11, checkpoint for 3. If you run long, shorten the lecture on finding external data and let learners read it afterward.

**Talk track.**
- Open with "a fact is only as good as where it came from." Ask the room where the last number they used in a meeting originated.
- Make the point that the *question* chooses the authoritative source. Finance is authoritative for recognized revenue, and the order system is authoritative for demand. Neither report is wrong.
- Use the car-salesperson example, and then turn it around: your own team's dashboard has the same problem when it makes someone's project look good.
- Walk the six quality dimensions as a table and tell learners they'll fix three of them in Module 03.

**Answer key, Activity 1 (suggested ratings, accept well-reasoned alternatives).**

| Source | Primary or secondary | Suggested trust | Reason |
|---|---|---|---|
| A: Finance report | Primary (the finance system's own record) | High for recognized revenue | Named owner, reviewed, clear definition (ship date, net of refunds) |
| B: Order system export | Primary | High for demand, after cleaning | Closest to the system of record, but loaded twice, holds test orders, and mixes two date formats |
| C: Vendor one-pager | Secondary | Low | Seller of the product, no sample size, period, or definition, "selected" results |
| D: Trade group release | Secondary | Low to medium | Self-reported, 31 of 40 members, "online sales" undefined, sponsored by the vendor in Source C, members are mostly physical retailers so it may not describe an online-first company like Lantern Peak |
| E: Satisfaction survey | Primary (a survey the company ran) | Medium for what respondents think, low for "all customers" | Voluntary replies, about 9 percent response (foreshadows Module 05) |

For the question "How much revenue did we recognize in 2025?" the answer is Source A. For "Is paid social worth more budget?" no single source is enough. Source C is a sales pitch, Source D is irrelevant to one company's channel economics, and the real answer sits in Lantern Peak's own data, which learners will analyze in Modules 06 and 08.

**Answer key, Activity 2.** The bridge above is the answer, and it ties to the cent. Order matters because duplicates overlap with cancelled orders. Total of `finance_monthly_revenue.csv`: $3,965,463.44. Total `order_total` in `orders_raw.csv` as loaded: $4,748,146.75. Duplicates and test orders are *data errors* (fix them). Cancelled orders, the January 2026 shipments, and refunds are *definition differences* (document them). The order system is right for demand, finance is right for recognized revenue, and the leadership team needs both numbers labeled.

**Answer key, Checkpoint.** Red flags in Source C: no number of clients, no time period, "selected" results with no selection rule, "return" undefined, and the vendor sells the thing being praised. A shared sponsor doesn't prove Source D is wrong, but it changes how much weight to give it. Treat it as a claim to verify and not as independent support.

**Common pitfalls.** Learners subtract cancelled orders before removing duplicates and overshoot by a small amount. Learners include the January to March 2023 dates and get confused by the format. Both are covered in the activity text. Some learners will want to "fix" the bridge by editing the raw file. Remind them that you never edit raw data, a rule Module 03 turns into practice.

**If you need to cut time.** Hands-on learners can skip step 1 and begin from the fact sheet.

</details>

<p style="border-bottom: 1px solid lightgrey;"></p>

<p><img style="margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/owl.png?raw=true"><b>For Further Study</b></p>
<ul>
 <li><a href="https://www.data.gov/" target="_blank">data.gov: US government open data</a> (look at how each dataset documents its source and method)</li>
 <li>Your local or university library's research guides on evaluating sources</li>
</ul>

<p style="border-bottom: 1px solid lightgrey;"></p>

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/geopin.png?raw=true"><b>Next Steps</b></p>

Next, continue to <a href="03-work-with-data.md"><i>Module 03 - Work with Data</i></a>.
