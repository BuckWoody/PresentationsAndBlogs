<img width="150" style="float: right; margin: 0px 15px 15px 0px;" src="../graphics/logo.png">

# Workshop: Data Literacy

#### <i>Using Data To Make Intelligent Decisions</i>

<p style="border-bottom: 1px solid lightgrey;"></p>

<img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/textbubble.png?raw=true"> <h2>6 - Find Out Why</h2>

| Minutes | What happens |
|---|---|
| 0 to 7 | Lecture: from "what happened" to "why," and how to drill down |
| 7 to 14 | Activity 1: Drill Down |
| 14 to 23 | Lecture: mix, rates, and Simpson's paradox |
| 23 to 32 | Activity 2: Mix or Rate? |
| 32 to 38 | Lecture: correlation, causation, and how to tell the difference |
| 38 to 43 | Activity 3: Does Email Drive Sales? |
| 43 to 45 | Skeptic's checkpoint: after, therefore because? |

> **Starting here?** You need the Lantern Peak case files (the `case-data` folder), in particular `supplements/repeat_cohort.csv`, `supplements/marketing_monthly.csv`, and `raw/finance_monthly_revenue.csv`. A quick catch-up: Lantern Peak Supply Co. is a fictional online retailer of camping and hiking gear. Its leadership team has noticed that fewer new customers come back for a second purchase, and wants to know why before deciding where to spend $150,000. You'll need to be comfortable with rates, percentage points, and the skeptic's habits from Module 05 (write your hypotheses down first, ask what else changed).

<p style="border-bottom: 1px solid lightgrey;"></p>

In Module 04 you learned to say what happened. Now you ask the harder question: **why?** *Diagnostic* analysis is detective work. You look at a result, form some explanations, and test each against the evidence. It's also the first place where the skeptic's toolkit from Module 05 earns its keep, because the temptation to grab the first plausible story is strongest right here.

<img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/pencil2.png?raw=true"> <h2>6.1 From What to Why</h2>

Good diagnostic work usually follows this path:

1. **Confirm the change is real.** Before you explain a drop, make sure it's bigger than ordinary wobble (more on that in a moment).
2. **Write down your hypotheses first.** List the plausible explanations *before* you slice the data. If you slice first and explain afterward, you'll find a story in whatever the slices show.
3. **Drill down.** Break the total into parts (by channel, product, region, time) and see where the change lives.
4. **Compare.** Put like beside like: segments, time periods, and *cohorts* (groups of customers who started at the same time or in the same way, followed for the same length of time).
5. **Decompose the change.** Work out how much of it comes from each part.
6. **Ask what else changed.** Something that moved at the same time is a suspect, but not yet a cause.

Two simple tools help you organize the hunt. The **five whys** means asking "why?" of each answer until you reach something you can act on. An **issue tree** splits a question into branches that don't overlap and together cover every possibility. For a falling repeat rate, the top split is clean: either *people within each group are repeating less*, or *the mix of groups has changed*. The data will tell you which.

**Variation versus signal.** Any measure wobbles from period to period just because different customers happen to show up. Before you explain a change, ask if it's larger than that natural wobble. A common rule of thumb for a rate is the *margin of error*: about 1.96 times the square root of p(1 minus p) divided by n, where p is the rate and n is the number of people behind it. With 1,000 customers and a 40 percent rate, the margin is about plus or minus 3 points. A change smaller than that could easily be luck. And remember that a large sample can make a tiny difference "statistically significant," so also ask whether the change is big enough to *matter*.

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/point1.png?raw=true"><b>Activity 1: Drill Down</b></p>

The CEO says fewer new customers are coming back. You'll check that, and then start looking for reasons.

<p><img style="margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/checkmark.png?raw=true"><b>Steps</b></p>

**Hands-on:**

1. Open `case-data/supplements/repeat_cohort.csv`. (One row is a consumer customer whose first order fell between January 1 and September 30 of 2024 or 2025, so every customer has a full 90 days to come back. The column `repeat_90` is 1 if they placed a second order within 90 days.) Compute the repeat rate and the number of customers for each `cohort_year`.
2. Work out each rate's 95 percent margin of error (1.96 times the square root of p(1 minus p) divided by n). Do the two ranges overlap? Then check the difference itself: its margin is 1.96 times the square root of the two squared standard errors added together. Is the drop bigger than that margin?
3. Before you slice any further, write down three possible explanations for the drop.
4. Now drill down: compute the number of customers and the repeat rate for each `acquisition_channel` in each year, and each channel's share of the year's new customers. What do you see?

**Leader's view:** Two questions turn a vague worry into an investigation: *Is this change bigger than ordinary wobble?* and *What are the three most plausible explanations, and what data would rule each one in or out?* Ask for the hypotheses in writing before the analysis starts.

<p style="border-bottom: 1px solid lightgrey;"></p>

<img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/pencil2.png?raw=true"> <h2>6.2 Mix, Rates, and Simpson's Paradox</h2>

Here is one of the most useful and most surprising ideas in diagnostic work. A total can move in the opposite direction from every one of its parts.

Take Lantern Peak's new customers. Overall, the share who place a second order within 90 days fell from 38.5 percent to 34.7 percent. Now look inside.

| Channel | 2024 customers | 2024 share | 2024 repeat rate | 2025 customers | 2025 share | 2025 repeat rate |
|---|---:|---:|---:|---:|---:|---:|
| Organic search | 730 | 49% | 45.6% | 598 | 32% | 46.8% |
| Email referral | 453 | 30% | 40.0% | 340 | 18% | 44.7% |
| Paid social | 319 | 21% | 20.1% | 915 | 49% | 23.1% |
| **All consumers** | 1,502 | 100% | **38.5%** | 1,853 | 100% | **34.7%** |

Every channel's repeat rate went *up*. The overall rate went *down*. That reversal is called *Simpson's paradox*. It happens because the groups carry different weights from year to year. Paid social customers repeat at roughly half the rate of the others, and paid social grew from about a fifth of new customers to about half. The average is dragged down by the *mix* even though each group improved.

You can put numbers on this. The overall change splits into two pieces:

- **The mix effect:** how much of the change comes from the shift in group sizes. For each group, multiply the change in its *share* by its *old* rate, and add them up.
- **The rate effect:** how much comes from each group's own change. For each group, multiply its *new* share by the change in its *rate*, and add them up.

The two effects add up to the total change. For Lantern Peak, the mix effect is about minus 6.5 points and the rate effect is about plus 2.7 points, for a total of minus 3.8 points. If the channel mix had stayed the same, the repeat rate would have *risen* to about 41 percent.

This analysis explains the *drop*. Whether paid social is a good idea is a separate question, because those customers might still be worth more than they cost. That's a decision question, and you'll come back to it in Module 08. Diagnostic analysis tells you what is driving a result and stops short of telling you what to do about it.

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/point1.png?raw=true"><b>Activity 2: Mix or Rate?</b></p>

You'll split the drop into its mix and rate pieces, then look at what each channel is worth.

<p><img style="margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/checkmark.png?raw=true"><b>Steps</b></p>

**Hands-on:**

1. Using your own channel table from Activity 1 (customers, shares, and repeat rates for each year), compute (a) the overall change in the repeat rate, (b) the mix effect, and (c) the rate effect. Do (b) and (c) add up to (a)?
2. What would the overall repeat rate in 2025 have been if the channel mix had stayed as it was in 2024? (Multiply the 2024 shares by the 2025 rates.)
3. Which channel changed most in share, and which has the lowest repeat rate? Write a one-sentence explanation of the drop that a CEO could repeat.
4. Now look at what the channels are worth. From `repeat_cohort.csv`, take the 2024 customers only (they all have a full year of history). Compute the average `gross_profit_90d` and the average `gross_profit_365d` for each channel. How do the channels compare? (Don't draw a conclusion about budgets yet. You'll do that in Module 08.)

**Leader's view:** Whenever a total moves, ask for the groups next to it: "Is anything hiding inside this number?" and "Did the mix change?" A good analyst can split a change into a mix piece and a rate piece in a few minutes. If your team can't, ask them to try.

<p style="border-bottom: 1px solid lightgrey;"></p>

<img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/pencil2.png?raw=true"> <h2>6.3 Correlation, Causation, and How to Tell the Difference</h2>

*Correlation* measures how closely two measures move together, on a scale from minus 1 (perfectly opposite) through 0 (unrelated) to plus 1 (perfectly in step). It tells you that two things move together. It doesn't tell you why.

When two measures are correlated, there are several possible reasons:

- A causes B.
- B causes A (the direction runs the other way).
- A third factor drives both (a *confounder*, such as the season, or the weather).
- Chance, especially if you've looked at many pairs.
- Selection: you're looking at a group that was chosen in a way that creates the link.

You can move from correlation toward cause in steps. Each step is harder to do and more convincing.

1. **Compare like with like.** Remove the obvious confounders (compare the same month in different years, or similar customers).
2. **Use a control group.** Watch what happened to a comparable group that didn't get the change.
3. **Run an experiment.** In an *A/B test*, you *randomly* split people into two groups, change one thing for one group, and compare the results. Random assignment evens out everything else (the season, the customer mix) on average, which is why experiments are the gold standard for cause.

A well-run A/B test fixes the question, the group, the measure, and the duration *before* it starts. It's big enough to detect the difference you care about, and nobody stops it early because the early numbers look good.

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/point1.png?raw=true"><b>Activity 3: Does Email Drive Sales?</b></p>

The marketing team says, "Email drives sales. Look at the chart: when we send more email, revenue goes up." You'll test that.

<p><img style="margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/checkmark.png?raw=true"><b>Steps</b></p>

**Hands-on:**

1. Put `email_sends` from `supplements/marketing_monthly.csv` next to the monthly `net_revenue` from `raw/finance_monthly_revenue.csv` (36 months). Draw a scatter chart and compute the correlation. How strong is it?
2. Now remove the season. For each month of 2024 and 2025, work out the growth versus the *same month a year earlier*, for both email sends and revenue (24 pairs of growth rates). Compute the correlation between those two columns. What happened?
3. What does the comparison suggest about the marketing team's claim? What third factor was behind the first correlation?
4. In four lines, design a test that *could* show whether email drives sales: who gets it, how you split them, what you measure, and how long you run it.

**Leader's view:** When someone shows you two lines that move together, ask *what else could move both?* Then ask whether the team could run a small test. Most "does X work?" questions can be settled by a well-designed experiment, and an experiment costs far less than a wrong $150,000 decision.

<p style="border-bottom: 1px solid lightgrey;"></p>

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/point1.png?raw=true"><b>Skeptic's Checkpoint: After, Therefore Because?</b></p>

Lantern Peak launched its loyalty program on July 1, 2024. Revenue in the six months after the launch was far higher than in the six months before. A leader says, "The program drove the growth." **Do this now (two minutes):** name two other things that changed around the same time. Then say what comparison would make you more confident.

<p style="border-bottom: 1px solid lightgrey;"></p>

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/point1.png?raw=true"><b>Go Further (Optional): Adventure Works Cycles</b></p>

Adventure Works' fiscal year runs from July 1 to June 30, and each territory has a sales target. In the invented extract (`case-data/adventure-works`), the **Canada** territory ended fiscal 2014 well below target, after beating it in fiscal 2013.

**Steps:**

1. Write down three hypotheses for the miss before you open any data.
2. Compare Canada's fiscal 2013 and fiscal 2014 by channel: the number of orders, the revenue, and the average order value. Where did the shortfall come from: fewer orders, smaller orders, or one channel?
3. Look at Canada's largest single orders in each year. How much could one order swing a year?
4. What would you want to know before calling this a real problem?

<details>
<summary><b>Instructor notes</b></summary>

**Timing (45 minutes).** Lecture 6.1 for 7 minutes, Activity 1 for 7, lecture 6.2 for 9, Activity 2 for 9, lecture 6.3 for 6, Activity 3 for 5, checkpoint for 2. The optional Adventure Works activity isn't in the 45.

**Talk track.**
- The detective framing works well. Tell learners the goal is a *defensible explanation*, and that certainty is rare.
- Press the "write hypotheses first" rule. Before step 4 of Activity 1, have the room call out hypotheses and write them on the board. Afterward, compare them with what the data showed. If your room guesses "customer service" or "product quality" first, that's normal, and it makes the reveal land harder, because the actual answer is mix.
- The mix versus rate split is the main event. Draw the channel table on a whiteboard, then walk through why the total fell while each part rose.
- Be explicit that the decomposition explains the *drop*, and that it doesn't judge paid social.
- For 6.3, ask the room for a time they saw a correlation mistaken for a cause. They have stories.

**Answer key, Activity 1.**
- Repeat rate: 38.5 percent in 2024 (1,502 customers, plus or minus 2.5 points, a range of 36.0 to 40.9 percent) and 34.7 percent in 2025 (1,853 customers, plus or minus 2.2 points, a range of 32.5 to 36.9 percent). The ranges overlap slightly, but the drop of 3.8 points is larger than the margin on the difference (plus or minus 3.3 points), so it's very likely real and not noise. Overlapping ranges are a rough screen, and the difference's own margin is the better test.
- Plausible hypotheses: product or shipping quality got worse, more returns, new customers are different (mix), a competitor moved in, the loyalty program changed behavior. Accept any, and mark the ones the data can test.
- Channel table: see the table in 6.2 (shares: organic 49 to 32 percent, email 30 to 18 percent, paid social 21 to 49 percent).

**Answer key, Activity 2.**
- Overall change: minus 3.8 points. Mix effect: minus 6.5 points. Rate effect: plus 2.7 points. They sum to minus 3.8.
- With the 2024 mix and 2025 rates the overall rate would be 41.1 percent.
- Suggested sentence: "The repeat rate fell because half of our new customers now come from paid social, which has the lowest repeat rate. Every channel actually improved."
- Channel value (2024 customers): 90-day gross profit per customer is about $135 for email, $134 for organic, and $113 for paid social. The 365-day gross profit is about $188, $193, and $157. Paid social customers are worth less per head, but this isn't yet a verdict because the acquisition cost differs (Module 08).

**Answer key, Activity 3.**
- Step 1: correlation of about 0.82 across all 36 months. It looks strong.
- Step 2: the correlation of the year-over-year growth rates is about 0.10. Within a single year the correlation is 0.92 to 0.97, because both series follow the holiday season. Email volume grew about 11 percent a year while revenue grew 87 percent on average.
- Step 3: the season (and company growth) is the confounder. This comparison can't tell whether email has an effect.
- Step 4: a good design randomly holds back a share of eligible customers (say 10 to 20 percent) from a campaign, sends it to the rest, then compares orders per customer over the following weeks, for a duration set in advance.

**Answer key, checkpoint.** Other things that changed: the holiday season (July to December is a seasonal ramp), the expansion of paid social, and ongoing company growth that was already underway. A stronger comparison uses the same months in the previous year, or compares members with similar non-members before and after (the pre-launch check from Module 05).

**Answer key, Go Further.** Canada's FY2014 revenue was about 46 percent below target, after being about 24 percent above in FY2013. Reseller orders fell from 60 to 49 and the average Reseller order fell from about $9,700 to about $7,500. Internet orders actually rose from 123 to 137, but the average Internet order fell from about $960 to about $670. Canada's largest single order was about $38,300 in FY2013 and about $26,900 in FY2014. The territory is lumpy: a handful of large Reseller orders can swing a year, so one year's miss is weak evidence of a real problem. A good next step is to look at several years, other territories, and whether FY2013's target was set off an unusually strong year.

**Common pitfalls.** Learners compute shares incorrectly (share of the year's customers, not of the channel's). Learners forget that only 2024 customers have a full-year profit. Learners treat the Simpson's paradox result as evidence that paid social "works." Remind them that a rate and a total can both be true and that this is a diagnostic result.

**If you need to cut time.** Skip step 4 of Activity 2 (the channel value comparison), and hand out the table. Skip Activity 3 step 4 and do it as a discussion.

</details>

<p style="border-bottom: 1px solid lightgrey;"></p>

<p><img style="margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/owl.png?raw=true"><b>For Further Study</b></p>
<ul>
 <li><a href="https://en.wikipedia.org/wiki/Simpson%27s_paradox" target="_blank">Simpson's paradox</a></li>
 <li><a href="https://en.wikipedia.org/wiki/Confounding" target="_blank">Confounding</a></li>
 <li><a href="https://en.wikipedia.org/wiki/A/B_testing" target="_blank">A/B testing</a></li>
 <li><a href="https://www.khanacademy.org/math/statistics-probability" target="_blank">Khan Academy: Statistics and probability</a> (margin of error and sampling)</li>
</ul>

<p style="border-bottom: 1px solid lightgrey;"></p>

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/geopin.png?raw=true"><b>Next Steps</b></p>

Next, continue to <a href="07-look-ahead.md"><i>Module 07 - Look Ahead</i></a>.
