<img width="150" style="float: right; margin: 0px 15px 15px 0px;" src="../graphics/logo.png">

# Workshop: Data Literacy

#### <i>Using Data To Make Intelligent Decisions</i>

<p style="border-bottom: 1px solid lightgrey;"></p>

<img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/textbubble.png?raw=true"> <h2>8 - Decide What to Do</h2>

| Minutes | What happens |
|---|---|
| 0 to 7 | Lecture: framing the decision |
| 7 to 15 | Activity 1: Frame the Decision |
| 15 to 24 | Lecture: options, value, break-even, and sensitivity |
| 24 to 34 | Activity 2: Score and Stress-Test |
| 34 to 40 | Lecture: deciding when you can't be sure |
| 40 to 43 | Activity 3: Stage It and Set Kill Criteria |
| 43 to 45 | Skeptic's checkpoint: who is in the room? |

> **Starting here?** You can do this module without the earlier ones, because the "case file" table in Activity 1 gives you everything the analysis found so far. You'll need a spreadsheet and the Lantern Peak case files (the `case-data` folder) if you want to check the inputs. A quick catch-up: Lantern Peak Supply Co. is a fictional online retailer of camping and hiking gear, and its leadership team has $150,000 to spend next year and has to decide where it goes.

<p style="border-bottom: 1px solid lightgrey;"></p>

This is where everything you've learned turns into a choice. *Prescriptive* analysis answers the question **what should we do?** It combines a description of the past, an explanation of why it happened, a prediction of what's coming, and a set of values and constraints, and from all of that it recommends an action. Some prescriptive tools are mathematical engines that search for the best plan under a set of limits. For most business decisions, though, the engine is a careful person with a clear frame, honest numbers, and a willingness to say how unsure they are.

<img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/pencil2.png?raw=true"> <h2>8.1 Framing the Decision</h2>

Start with the problem itself. Imagine you're in a car and you ask the driver, "Are we making good time?" The driver checks the speedometer and says yes. Later you ask, "Are we nearly there?" and the driver says yes again. Then you get dropped off at the wrong address. You asked the wrong question. The better one was, *"When will we arrive at this address?"*

You can often find the right question by asking another one: **"When we get the answer from the data, what will we do about it?"** If no answer would change what you do, you're asking the wrong question.

A well-framed decision has five parts.

- **The objective.** What are you trying to achieve, and how will you measure it?
- **The options.** Include *do nothing* and *wait and test* in the list. They're real options.
- **The constraints.** Money, time, people, rules.
- **The criteria.** How will you compare the options? (Value, risk, speed, fit with strategy.)
- **The uncertainties.** What do you not know that matters most?

Then work the problem in a sensible order:

1. State the goal as a question.
2. Break it into sub-questions.
3. Find data for each one.
4. Answer each sub-question.
5. Combine the answers into possible courses of action.
6. Score those options against your criteria and constraints.
7. Choose one, and keep the runner-up as the alternative.

**Is the decision reversible?** A decision you can undo cheaply (a two-week experiment) deserves speed. A decision you can't (signing a three-year contract) deserves more evidence. The same $150,000 can be spent as one big bet, or in stages that let you stop.

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/point1.png?raw=true"><b>Activity 1: Frame the Decision</b></p>

Here's what the analysis found. Lantern Peak's leadership team wants to know where $150,000 should go next year.

**The case file so far**

| Finding | Source |
|---|---|
| Net revenue grew 54 percent in 2025. Orders and customers grew, and the average order barely moved. | Modules 02 and 04 |
| The 90-day repeat rate for new customers fell from 38.5 to 34.7 percent, even though every channel's rate improved. The cause is mix: paid social grew to about half of new customers. | Module 06 |
| Paid social customers repeat at about 20 to 23 percent, against 40 to 47 percent for organic search and email referral. | Module 06 |
| Paid social cost about $98 for each new customer in 2025. A paid social customer earned about $115 in gross profit in the first 90 days, and about $157 over a year (2024 customers). | Modules 06 and this module |
| Loyalty members spend about twice what others do, but they were already spending about 1.5 times as much before the program. Their spending fell about 8 percent, against about 15 percent for non-members. | Module 05 |
| Email volume and revenue correlate, but that's the season. The correlation of year-over-year growth rates is about 0.10. | Module 06 |
| Revenue for January to March 2026 is forecast at roughly $450,000, with a plausible range of $390,000 to $510,000. | Module 07 |
| The vendor's churn model is 95.4 percent accurate, and "no one leaves" is 95 percent accurate. It catches 30 percent of leavers. | Module 07 |
| Clothing and footwear returns coded "did not fit" cost about $41,000 in refunds in 2025, and about $19,800 in gross profit. | This module |

<p><img style="margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/checkmark.png?raw=true"><b>Steps</b></p>

**Hands-on:**

1. Write the goal as a *question* that a decision could answer. Check it with "what will we do about the answer?"
2. List the **constraints** (at least money and time) and the **criteria** you'll use to compare options.
3. List the **options**. Start with these four, and add any you think are missing:
   - **A.** Expand paid social with the full $150,000.
   - **B.** A $60,000 retention program aimed at existing customers (email, loyalty tuning, win-back offers).
   - **C.** A $30,000 set of fit tools (size guides and fit reviews) to cut fit-related returns in clothing and footwear.
   - **D.** Hold the money in reserve.
4. For each option, write the one thing you'd most want to know before choosing it.

**Leader's view:** Before you ever look at an analysis, check its frame. *What decision will this change? What are the options, including doing nothing? What are the constraints? What's the biggest unknown?* If the team can't say, the analysis may be answering a question nobody asked.

<p style="border-bottom: 1px solid lightgrey;"></p>

<img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/pencil2.png?raw=true"> <h2>8.2 Options, Value, Break-Even, and Sensitivity</h2>

To compare options, you need a way to put them on the same footing.

**Value.** The value of an option is its benefit minus its cost, over a time horizon you choose and state (here, twelve months). Only count what changes because of the decision. Money already spent is a *sunk cost* and doesn't belong in the comparison. What you give up by choosing one option over the next best is the *opportunity cost*.

**Incrementality.** Ask whether the benefit would have happened *anyway*. If a paid social customer would have found Lantern Peak through search a week later, the advertising didn't create that customer, so only the *incremental* share should count toward its value.

**Scenarios and expected value.** When you aren't sure of an input, don't pick one number. Pick a low, a base, and a high case, give each a probability, and compute the *expected value* (each outcome times its probability, added up). Also look at the *spread*, because two options with the same expected value can carry very different risks.

**Break-even.** Ask *what has to be true for this to pay for itself?* A break-even number often answers a question that a forecast can't. It turns "will it work?" into "do we believe it's at least this big?"

**Sensitivity.** Change one assumption at a time, and watch how much the result moves. The assumptions that move it most deserve the most evidence.

**Weighted scoring.** When some criteria aren't in dollars (how risky, how well-supported, how quickly you'd learn), give each criterion a weight, score each option from 1 to 5, and total them. The weights encode your values, so try different weights and see if the ranking holds.

**The formulas for Lantern Peak:**

- Paid social: customers acquired is the budget divided by the cost per customer. Net value is customers times (the incremental share times 12-month gross profit per customer, minus the cost per customer).
- Retention: net value is active customers times gross profit per customer times the lift in spending, minus the program cost.
- Fit tools: net value is the gross profit forgone on fit-related returns times the share of them avoided, minus the program cost.

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/point1.png?raw=true"><b>Activity 2: Score and Stress-Test</b></p>

You'll compare the options with numbers, find out what has to be true for each to pay, and see how sensitive the answer is.

**The inputs.** (From the case files, so you can check them: paid social spend and customers from `supplements/marketing_monthly.csv` and `clean_csv/customers.csv`, and profit per customer from `supplements/repeat_cohort.csv`.)

| Input | Value |
|---|---:|
| Paid social cost per new customer, 2025 | $98 |
| Paid social 365-day gross profit per customer (2024 customers) | $157 |
| Customers who ordered in 2025 | 4,551 |
| 2025 gross profit per active customer, after returns | $185 |
| Gross profit forgone on fit-related clothing and footwear returns | $19,841 |

**The scenario assumptions.** (These are invented for the exercise. Challenge them.)

| Option | Low | Base | High |
|---|---|---|---|
| **A.** Paid social, $150,000 | Cost per customer 30% higher ($127), 365-day gross profit $130, 50% of customers incremental | Cost $98, gross profit $157, 75% incremental | Cost $98, gross profit $175, 100% incremental |
| **B.** Retention, $60,000 | Spending per active customer up 2% | Up 5% | Up 8% |
| **C.** Fit tools, $30,000 | 10% of fit-related profit loss avoided | 25% avoided | 40% avoided |

Use probabilities of 25 percent for Low, 50 percent for Base, and 25 percent for High. Option D, holding the reserve, is worth $0 in every scenario.

<p><img style="margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/checkmark.png?raw=true"><b>Steps</b></p>

**Hands-on:**

1. **Break-even.** Work out (a) the share of paid social customers that must be incremental for the advertising to pay back within a year (cost per customer divided by 365-day gross profit), (b) the lift in spending a $60,000 retention program needs, as a share of total gross profit (the program cost divided by active customers times gross profit per customer), and (c) whether fit tools can pay back even if they eliminated every fit-related return.
2. **Scenarios.** Fill in a table of net value for Options A, B, and C in the Low, Base, and High cases. Then compute each option's expected value and its chance of losing money.
3. **Score.** Score options A, B, C, and D from 1 to 5 on four criteria: *expected net value* (weight 40 percent), *downside risk* (25 percent, with a higher score meaning less to lose), *strength of the evidence* (20 percent), and *speed to learn* (15 percent). Compute the weighted totals. Then change the weights (try giving downside risk only 10 percent and expected value 50 percent). Does the ranking change?
4. **Sensitivity.** For Option A, hold everything at Base and vary one assumption at a time: incrementality (50, 75, and 100 percent), cost per customer (30 percent higher and lower), and 365-day gross profit ($130 and $175). Which assumption swings the result the most?
5. **Design Option E.** Using what you found, design a *staged* option that spends part of the money to learn what you most need to know. Score it too.

**Leader's view:** Open the results below and read them as a decision-maker. *Which option has the best expected value? Which has the biggest possible loss? What single number would you most like to know before committing, and what's the cheapest way to find out?*

<details>
<summary><b>The scenario results (check your work, or read them as a leader)</b></summary>

| Option | Low | Base | High | Expected value | Chance of losing money |
|---|---:|---:|---:|---:|---:|
| A: expand paid social ($150,000) | -$73,398 | $30,343 | $118,106 | $26,348 | 25% |
| B: retention program ($60,000) | -$43,198 | -$17,996 | $7,206 | -$17,996 | 75% |
| C: fit tools ($30,000) | -$28,016 | -$25,040 | -$22,064 | -$25,040 | 100% |
| D: hold in reserve | $0 | $0 | $0 | $0 | 0% |

**Break-evens.** Paid social needs about 62 percent of its customers to be incremental. The retention program needs about a 7.1 percent lift in spending. Fit tools can recover at most $19,841, which is less than their $30,000 cost, so they can't pay back on returns alone.

</details>

<p style="border-bottom: 1px solid lightgrey;"></p>

<img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/pencil2.png?raw=true"> <h2>8.3 Deciding When You Can't Be Sure</h2>

You'll rarely have enough information to be certain, and waiting for certainty is itself a decision. Here are some ways to act well anyway.

**Buy information when the stakes are high and the uncertainty is large.** If one unknown (here, how many paid social customers are truly new) can swing the result by $100,000, a small experiment that settles it can be worth more than any option it delays. Commit a small amount first, measure, and then decide whether to scale. Set the rule *before* you start (the *kill criteria*): "If the result is below X by day Y, we stop."

**Use a decision loop.** Colonel John Boyd, a US Air Force fighter pilot, developed the OODA loop (*Observe, Orient, Decide, Act*) from his study of air combat, where [decisions have to be made quickly under pressure](https://www.maxwell.af.mil/News/Display/Article/420819/). It's often retold as "the faster loop always wins," and that's an oversimplification. The part worth borrowing is *orientation*: how you interpret what you observe, shaped by your experience, your biases, and your model of the situation. You've spent this workshop improving the first two steps, observing (Modules 02 through 04) and orienting (Modules 05 through 07). The loop repeats. Each action creates new observations, which is why a staged decision fits it so well.

**Respect real constraints, and push on them.** There is never enough time to analyze everything. Some decisions have to be made in days. Do the best you can with the time and money you have, and push back on the limits when the stakes justify it.

**Beware paralysis.** Aim for a decision that's good enough, well reasoned, and on time.

**Keep people in the loop.** Prescriptive tools (optimization engines, recommendation systems, automated pricing or offers) can embed bias, treat groups unfairly, or use personal data in ways people wouldn't accept. Ask who is affected, how the recommendation was produced, and who is accountable. An AI assistant can help you build options and check your arithmetic. The decision, and the responsibility for it, stays with a person.

**Apply the skeptic's habits.** Ask what you'd do if you were starting today (that sets aside sunk costs). Collect views independently before the group discusses. Run the premortem you wrote in Module 05.

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/point1.png?raw=true"><b>Activity 3: Stage It and Set Kill Criteria</b></p>

Turn your Option E into a plan someone could follow, and test it against your premortem.

<p><img style="margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/checkmark.png?raw=true"><b>Steps</b></p>

**Hands-on:**

1. Reread the three reasons you wrote in the Module 05 premortem. (If you skipped it, write three ways this decision could fail.) Does your Option E guard against each one?
2. Write the staged plan in four lines: *what you'll spend first, what you'll measure, how you'll compare (what's the control?), and what result tells you to stop or to scale.*
3. State your kill criteria with a number in them.

**Leader's view:** For any decision that commits real money, ask, "What would make us stop?" If nobody can answer with a number and a date, the plan is a hope.

<p style="border-bottom: 1px solid lightgrey;"></p>

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/point1.png?raw=true"><b>Skeptic's Checkpoint: Who Is in the Room?</b></p>

The CEO opens the meeting by saying, "I've always believed in paid social. Let's put the whole $150,000 into it." **Do this now (two minutes):** write down how you would run the meeting so the data gets a fair hearing. Which of this module's habits would you use? (Think about the order people speak in, what you'd ask for before anyone reacts, and the break-even number.)

<p style="border-bottom: 1px solid lightgrey;"></p>

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/point1.png?raw=true"><b>Go Further (Optional): Adventure Works Cycles</b></p>

The Adventure Works Internet team can promote one product category next quarter. In the invented extract (`case-data/adventure-works`), look only at Internet-channel orders.

**Steps:**

1. For each of the four categories, compute revenue, gross margin dollars, and gross margin percent. (Revenue for a line is `quantity * unit_price * (1 - discount)`. Gross margin is revenue minus `quantity * standard_cost`.)
2. Which category has the best margin *percent*? Which has the most margin *dollars*? Why might they differ?
3. Which would you promote, and what else would you want to know first? (Think about incrementality, capacity, and how promotion might change what people buy.)

<details>
<summary><b>Instructor notes</b></summary>

**Timing (45 minutes).** Lecture 8.1 for 7 minutes, Activity 1 for 8, lecture 8.2 for 9, Activity 2 for 10, lecture 8.3 for 6, Activity 3 for 3, checkpoint for 2. The optional Adventure Works activity isn't in the 45. Activity 2 is the longest, and learners will want more time. Let them split the work (one person does A, one does B, and so on) and share.

**Talk track.**
- Open with the car story, then ask: "What decision are we making, and what will we do with the answer?"
- In 8.2, the break-even idea is the one to land. "What has to be true for this to pay?" is a more useful question than "will it work?"
- Spend a minute on incrementality, because learners often don't think about it until you do. Ask: "How many of those customers would have found us anyway?"
- In 8.3, be clear that the decision belongs to people. Prescriptive tools recommend, and a person answers for the choice.
- On OODA, correct a common misunderstanding. Boyd was a fighter pilot and the idea came from air combat. It's often reduced to "the faster loop wins," but the more interesting part is orientation. Don't spend more than a minute on it.

**Answer key, Activity 1.** Accept any well-formed goal question. A good one: "How should we allocate $150,000 over the next twelve months to maximize gross profit, given what we know about acquisition cost, repeat behavior, and uncertainty?" Constraints: $150,000, twelve months, evidence quality. Criteria: expected value, downside risk, strength of evidence, speed to learn.

**Answer key, Activity 2.**
- Break-evens: paid social, $97.91 divided by $156.95, about 62 percent incremental. Retention, $60,000 divided by (4,551 times $184.59), about 7.1 percent. Fit tools can recover at most $19,841 against a $30,000 cost.
- Scenario results are in the reveal. Only A has a positive expected value ($26,348), and it also has the widest spread, from -$73,398 to +$118,106.
- Scores (a suggested answer; accept well-reasoned alternatives). With the original weights (40, 25, 20, 15 percent), A scores 3.25, B 2.60, C 2.65, D 3.60. D wins because the weights penalize downside heavily, and D has none. With lighter downside weights (50, 10, 20, 20), A scores 3.8, B 2.5, C 2.3, D 3.2, so A wins. **The matrix depends on the weights**, so show how sensitive the ranking is.
- Sensitivity for Option A (all others at Base): incrementality at 50, 75, and 100 percent gives about -$29,800, +$30,300, and +$90,500. Cost per customer 30 percent higher or lower gives about -$11,300 and +$107,600. Gross profit of $130 or $175 gives about -$600 and +$51,100. **Incrementality and cost per customer matter most**, and the company hasn't measured the first.
- Option E, a staged plan (suggested): spend about $50,000 on paid social with a controlled test (a holdout region or a time-split) to measure the incremental share, and about $15,000 on a small retention pilot with a random holdout. Hold the remaining $85,000. Scale paid social only if the measured incremental share is above 62 percent. Scores with the original weights: expected value 4, downside risk 4, evidence 4, speed to learn 5, for a total of 4.15, the highest, because it buys the information the other options lack.
- Fit tools (Option C) fail on returns alone. That doesn't prove they're a bad idea (a cheaper fix, or one with benefits beyond returns, might pay), but it shows the size of the prize before anyone spends on it. Unquantified benefits aren't zero, but they shouldn't decide silently.

**Answer key, Activity 3.** A good plan: "Spend $50,000 on paid social over 60 days, with a randomly chosen set of regions held out as a control. Measure new customers per region in each group. If the exposed regions show new customers at least 62 percent of the way to what the advertising claims, scale. If they show less, stop and move the money to the reserve." Kill criteria must contain a number and a date. Look for plans where the measure and the control are named before the spending starts.

**Answer key, checkpoint.** Good answers: ask people to write their view privately before discussion, hear the most junior person first, show the break-even number (62 percent) before anyone reacts, and ask what would change the CEO's mind. The aim is to keep the CEO's preference from becoming the anchor.

**Answer key, Go Further.**

| Category | Revenue | Gross margin dollars | Gross margin percent | Share of Internet revenue |
|---|---:|---:|---:|---:|
| Bikes | $4,026,555 | $1,411,497 | 35.1% | 91% |
| Components | $202,406 | $86,291 | 42.6% | 5% |
| Accessories | $119,220 | $71,886 | 60.3% | 3% |
| Clothing | $97,302 | $49,893 | 51.3% | 2% |

Accessories have the best margin percent and Bikes have far more margin dollars, because they're 91 percent of Internet revenue. Promoting accessories has a better percentage but a small base, so even a large lift adds few dollars. Strong follow-up questions: how much extra volume would promotion create, and is it incremental? Do accessory purchases come with bike purchases (a bundling opportunity)? Is bike inventory or capacity limited?

**Common pitfalls.** Learners treat the Base case as the forecast, and skip the spread. Learners forget the cost in the net value formula (net, not gross). Learners dismiss Option C without checking the number. Learners score with the weights they like, and don't test alternatives. Learners propose a staged plan without a control group or a kill number.

**If you need to cut time.** Have learners do steps 1 and 2 of Activity 2 only, and give the scoring and sensitivity as a handout. Do Activity 3 as a discussion.

</details>

<p style="border-bottom: 1px solid lightgrey;"></p>

<p><img style="margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/owl.png?raw=true"><b>For Further Study</b></p>
<ul>
 <li><a href="https://www.maxwell.af.mil/News/Display/Article/420819/" target="_blank">Air University: the OODA loop</a></li>
 <li><a href="https://en.wikipedia.org/wiki/OODA_loop" target="_blank">OODA loop</a> and <a href="https://en.wikipedia.org/wiki/John_Boyd_(military_strategist)" target="_blank">John Boyd</a></li>
 <li><a href="https://en.wikipedia.org/wiki/Expected_value" target="_blank">Expected value</a> and <a href="https://en.wikipedia.org/wiki/Sensitivity_analysis" target="_blank">sensitivity analysis</a></li>
 <li>Books worth your time: <i>How to Measure Anything</i> (Hubbard), which shows how to put numbers on uncertain things, and <i>Noise</i> (Kahneman, Sibony and Sunstein)</li>
</ul>

<p style="border-bottom: 1px solid lightgrey;"></p>

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/geopin.png?raw=true"><b>Next Steps</b></p>

Next, continue to <a href="09-explain-act-learn.md"><i>Module 09 - Explain, Act, Learn</i></a>.
