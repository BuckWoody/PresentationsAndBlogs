<img width="150" style="float: right; margin: 0px 15px 15px 0px;" src="../graphics/logo.png">

# Workshop: Data Literacy

#### <i>Using Data To Make Intelligent Decisions</i>

<p style="border-bottom: 1px solid lightgrey;"></p>

<img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/textbubble.png?raw=true"> <h2>00 - Start Here</h2>

Welcome. This workshop is about one skill: using data to make better decisions. It takes about six hours, split into ten short modules, and every module can be taught or taken on its own. Take them in order and each one builds on the last, with a single fictional company following you all the way through.

| Minutes | What happens |
|---|---|
| 0 to 5 | Lecture: how the workshop is built, and the company you'll work with |
| 5 to 10 | Warm-up: eight quick questions (no grades, no pressure) |

<p style="border-bottom: 1px solid lightgrey;"></p>

<img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/pencil2.png?raw=true"> <h2>0.1 How the Workshop Builds</h2>

Think back to how you learned to read. First came the letters of the alphabet, then paper and pencil to write them, then the rules of grammar, and finally longer works where you pulled meaning out of what you read. Data literacy follows the same path.

| Reading and writing | Data literacy | Modules |
|---|---|---|
| The alphabet | Data itself: what it is, where it comes from, and whether to trust it | 01, 02 |
| Paper and pencil | The tools you use to work with data | 03 |
| Grammar | Context and relationships: what happened, how you could be fooled, and why it happened | 04, 05, 06 |
| Meaning | Looking ahead, deciding, and explaining your decision | 07, 08, 09 |

Analysis itself comes in four flavors, and each answers a different question.

| Kind of analysis | The question it answers | Module |
|---|---|---|
| Descriptive | What happened? | 04 |
| Diagnostic | Why did it happen? | 06 |
| Predictive | What is likely to happen next? | 07 |
| Prescriptive | What should we do about it? | 08 |

Each one is harder than the one before, each depends on the one before, and each gives you a fresh way to be wrong. That last point is why Module 05 (The Skeptic's Toolkit) sits in the middle of the workshop, and why every module closes with a two-minute skeptic's checkpoint.

<p style="border-bottom: 1px solid lightgrey;"></p>

<img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/pencil2.png?raw=true"> <h2>0.2 Three Ways to Use This Workshop</h2>

- **The full path.** Take Modules 01 through 09 in order, about six hours with breaks on top. Exercises use the output of the exercises before them, so you finish with a complete decision.
- **A single module.** Each module opens with a "Starting here?" box that tells you what you need and gives you the data in the state the module expects. You never have to go back.
- **The leader's view.** Every activity comes in two versions. The hands-on version has you do the work. The leader's view tells you what to ask your team for and what a good answer sounds like, so you can steer the work without running the software yourself.

If you're teaching this, look for the collapsed "Instructor notes" at the end of each module. They hold timing, a talk track, and the answer key.

<p style="border-bottom: 1px solid lightgrey;"></p>

<img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/pencil2.png?raw=true"> <h2>0.3 What You Need</h2>

- **A spreadsheet application.** Any one will do, desktop or browser-based.
- **A plain text editor.** The one already on your computer is fine.
- **The case files.** The `case-data` folder that comes with this workshop.
- **Optional: SQLite.** A free database engine that keeps everything in a single file, plus any viewer that can open that file. Module 03 shows you how. Nobody has to write SQL to finish the workshop.

Everything runs on your own computer, and the workshop itself needs no accounts or cloud services. (The reading links at the end of each module point to the web, of course.)

A word about AI assistants, since they now show up in everyday analysis work. Modules 03, 05 and 07 look at using one as a helper and at checking its work. If you use one, pick a tool your organization has approved (a locally run model is best), and never paste confidential data into a tool you haven't cleared for it.

<p style="border-bottom: 1px solid lightgrey;"></p>

<img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/pencil2.png?raw=true"> <h2>0.4 Meet Lantern Peak Supply Co.</h2>

Lantern Peak Supply Co. is a fictional online retailer of camping and hiking gear: tents, sleeping bags, packs, clothing, footwear, and cook-and-hydrate gear. It opened its online store in January 2023, sells mostly to individual shoppers, and supplies a small number of wholesale accounts (outfitters and outdoor clubs). You'll work with about three years of its records, roughly 6,900 customers and 15,900 orders.

Here is the situation. It's early 2026. Net revenue grew about 54 percent in 2025, which sounds wonderful, but the CEO has noticed that fewer new customers are coming back for a second purchase. The loyalty program is getting a lot of credit, a vendor has pitched a churn-prediction service, and there's $150,000 available for next year. The leadership team wants to know where it should go.

That is your question, and every module gets you one step closer to answering it.

| Module | What you'll do with Lantern Peak |
|---|---|
| 01 Data Basics | Learn the fields and tables, and decide what each row means |
| 02 Find and Trust Data | Work out why two reports show different revenue |
| 03 Work with Data | Clean and combine the messy raw files |
| 04 See What Happened | Summarize and chart orders, returns, and repeat buying |
| 05 The Skeptic's Toolkit | Audit four claims the leadership team has been repeating |
| 06 Find Out Why | Explain why repeat purchasing slipped |
| 07 Look Ahead | Forecast next quarter and test a vendor's accuracy claim |
| 08 Decide What to Do | Score the options for the $150,000 |
| 09 Explain, Act, Learn | Write the decision brief and plan the post-mortem |

**About Adventure Works Cycles (optional).** Several modules end with a "Go further" activity set at Adventure Works Cycles, a well-known fictitious bicycle maker that began as a Microsoft sample company and has been expanded for these materials. You never need it to finish the workshop. If you'd like the background first, [the company profile is here](https://tinyurl.com/bw-sample).

<p style="border-bottom: 1px solid lightgrey;"></p>

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/point1.png?raw=true"><b>Activity: Warm-Up</b></p>

Eight quick questions to see where you're starting. Nothing here is graded. It only helps you decide where to go fast and where to slow down.

<p><img style="margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/checkmark.png?raw=true"><b>Steps</b></p>

**Hands-on:** Jot a short answer to each question, then open the answers.

1. A report says "the average salary here is $82,000." Name one thing you'd want to know before relying on that number.
2. Weekly units sold went from 120 to 150. By what percentage did sales rise?
3. A column chart's vertical axis starts at 95 instead of 0. What does that do to how the differences look?
4. Ten homes sell on one street. Nine go for about $300,000 and one mansion goes for $4 million. Which gives a better sense of a typical sale, the mean or the median?
5. One survey shows 60 percent satisfied (6 of 10 people). Another shows 55 percent satisfied (550 of 1,000). Which number deserves more trust, and why?
6. A company emails 1,000 customers a survey. Eighty reply, and 72 say they're happy. The headline reads "90 percent of customers are happy." What's wrong with that?
7. Ice cream sales and sunburns both rise in July. Does ice cream cause sunburn? What else could explain both?
8. Someone hands you a striking number with no source. Which three questions do you ask?

**Leader's view:** Read the questions as a checklist for any report that lands on your desk. If you can't say what a good answer to each one looks like, that tells you where to spend your time in this workshop.

<details>
<summary><b>Open the answers</b></summary>

1. Which "average" it is (mean or median), how many people it covers, which people were included, how spread out the salaries are, and who produced the number and why.
2. 25 percent ((150 - 120) / 120).
3. The differences look much bigger than they are. A truncated axis exaggerates small gaps.
4. The median. The mean is $670,000, a price that none of the ten homes actually sold for.
5. The second one. Six of ten people could easily be a different story with another ten people. Larger samples settle down.
6. Only 8 percent replied, and people who answer a survey are often the ones who feel strongly (usually the happiest ones). The 90 percent describes the respondents, and you can't safely stretch it to everyone.
7. No. Hot, sunny weather drives both. When two things rise together, look for a third factor behind them before you claim one causes the other.
8. Who is telling me this? What exactly are they telling me? Why are they telling me this?

</details>

**Reading your results.** Got seven or eight? You can move quickly through Modules 01 and 02 and spend your time later. Four to six? The full path is a good fit. Three or fewer? Take the full path and keep the refresher links below close. There is no passing grade.

<p style="border-bottom: 1px solid lightgrey;"></p>

<p><img style="margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/owl.png?raw=true"><b>For Further Study (optional refreshers)</b></p>
<ul>
 <li><a href="https://www.khanacademy.org/math" target="_blank">Khan Academy: Math</a> (percentages, ratios, and everyday numeracy)</li>
 <li><a href="https://www.khanacademy.org/math/statistics-probability" target="_blank">Khan Academy: Statistics and probability</a> (the one subject most adults who analyze data are missing; take your time with it)</li>
</ul>

<details>
<summary><b>Instructor notes</b></summary>

**Timing (10 minutes).** Lecture 5, warm-up 5.

**Talk track.**
- Open with the reading analogy and the two tables in 0.1. Spend most of your time on the four kinds of analysis, because learners will keep returning to that ladder.
- Introduce Lantern Peak in two minutes. Name the three things the leadership team is arguing about (repeat buying, the loyalty program, the churn vendor). Learners will meet each one again.
- Mention the three paths in 0.2 so people know they can jump in anywhere later.

**Running the warm-up.** Ask for a show of hands or a quick poll for each question, then reveal the answer. Keep it light. With executives or mixed groups, call it a warm-up and invite stories ("Has anyone seen a chart like question 3?"). Skip scoring aloud.

**Before the session.** Confirm every learner can open a CSV in a spreadsheet. If you'll use the optional SQLite exercises in Module 03, confirm a viewer is installed. Keep the `facilitator` folder (answer keys) out of the learners' copy.

**Common questions.**
- "Do I need to know SQL?" No. It appears in Module 03 as an optional hands-on path.
- "Can we use our own data?" Yes, after the workshop. Use Lantern Peak first so everyone shares the same ground truth.

</details>

<p style="border-bottom: 1px solid lightgrey;"></p>

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/geopin.png?raw=true"><b>Next Steps</b></p>

Next, continue to <a href="01-data-basics.md"><i>Module 01 - Data Basics</i></a>.
