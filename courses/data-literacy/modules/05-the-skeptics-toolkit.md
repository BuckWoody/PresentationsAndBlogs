<img width="150" style="float: right; margin: 0px 15px 15px 0px;" src="../graphics/logo.png">

# Workshop: Data Literacy

#### <i>Using Data To Make Intelligent Decisions</i>

<p style="border-bottom: 1px solid lightgrey;"></p>

<img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/textbubble.png?raw=true"> <h2>5 - The Skeptic's Toolkit</h2>

| Minutes | What happens |
|---|---|
| 0 to 7 | Lecture: why smart people get fooled, and what actually helps |
| 7 to 13 | Activity 1: Name the Trap |
| 13 to 22 | Lecture: a field guide to the traps, by stage of analysis |
| 22 to 31 | Activity 2: Audit Two Claims |
| 31 to 35 | Checkpoint: your checklist and a premortem |

> **Starting here?** You need the Lantern Peak case files (the `case-data` folder), in particular `supplements/customer_spend_summary.csv` and `supplements/survey_audit.csv`. A quick catch-up: Lantern Peak Supply Co. is a fictional online retailer of camping and hiking gear, and its leadership team has been repeating four claims in meetings (about the loyalty program, customer satisfaction, the average order, and email). Your job in this module is to audit them. You need to know what an average, a rate, and a percentage point are (Module 04), and what a sample is.

<p style="border-bottom: 1px solid lightgrey;"></p>

You've learned to read data, and now it's time for the rules that keep your reading honest. Every grammar teaches you how a sentence works, and it also teaches you how a sentence breaks. This module is about how analysis breaks. It sits in the middle of the workshop on purpose, because you now have enough skill to be dangerous (you can compute and chart things), and not yet enough practice to know when you're fooling yourself.

The first step in any analysis is to become your own toughest critic. At each step, imagine someone leaning over your shoulder saying, *"I don't believe you. Prove it."* If you can hear that voice, you'll catch most of your own errors before anyone else does.

<img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/pencil2.png?raw=true"> <h2>5.1 Why Smart People Get Fooled</h2>

Mistakes in analysis come from three places, and it helps to keep them apart.

- **Cognitive biases** are patterns in how people judge and decide. The mind relies on shortcuts that usually work and sometimes mislead. Everyone has them, including experts, and including you.
- **Logical fallacies** are errors in the reasoning of an argument. The facts may be perfectly fine, but the conclusion doesn't follow from them.
- **Data traps** are problems in how data was collected, measured, or summarized. They can mislead you even when your thinking is flawless.

**What actually helps.** It would be nice if reading a list of biases cured them. Mostly it doesn't, and early training programs that simply told people about biases had little effect. The more encouraging news is what came later. In a set of experiments, [a short interactive game that gave players practice and personal feedback](https://openaccess.city.ac.uk/id/eprint/12324) reduced biased judgments by roughly 30 percent right away, and by more than 20 percent two months later. An instructional video helped too, though less. A [follow-up field study](https://www.psychologicalscience.org/news/minds-business/debiasing-your-decisions.html) with business students found that training cut the habit of testing only for confirming evidence, in a real business decision, by about 29 percent. The lesson for this module is to **practice with feedback**, so you'll spend most of your time here naming traps in realistic claims and checking your answers, and not memorizing definitions.

One more caution. Psychology has had a hard few years replicating some famous findings, so the field guide below sticks to patterns that have held up well, or that are plain arithmetic.

**The checks that work.** Whatever the trap, the defenses look alike. Think of them as decision hygiene, habits you apply every time.

1. **Write down your hypothesis and what would change your mind, before you look at the data.**
2. **Look for evidence against your idea.** Ask what the opposite conclusion would need to be true.
3. **Ask "compared to what?"** Every number needs a baseline.
4. **Ask who is missing.** Who isn't in this data, and why?
5. **Run a premortem.** Imagine it's a year from now and the decision failed. Write down why. (The psychologist Gary Klein popularized this one.)
6. **Get a second pair of eyes.** Ask someone to try to break your analysis.
7. **Show your work** so others can reproduce it.
8. **Check the denominators and the definitions.**

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/point1.png?raw=true"><b>Activity 1: Name the Trap</b></p>

You haven't seen the field guide yet, and that's the point. Using only your instincts, name what's wrong with each statement and what check you'd run. Commit to an answer *before* you open the reveal below, because the feedback is what trains you.

<p><img style="margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/checkmark.png?raw=true"><b>Steps</b></p>

**Hands-on:** For each statement, write down (a) what's wrong or risky about it, and (b) one question or check you'd use.

1. "Our best customers are the 4,000 who are still active, so let's study them to learn why customers stay."
2. "Ninety-four percent of the people who answered our survey are satisfied, so our customers love us."
3. "Email sends and monthly revenue rise and fall together, so email drives sales."
4. "The vendor says its churn model is 95 percent accurate. (Only 5 percent of our customers leave.)"
5. "We were sure paid social was working, so we pulled every chart that showed it was."
6. "We've already spent $40,000 on this campaign, so we have to see it through."
7. "Everyone in the meeting agreed once the CEO said it was obvious."
8. "Repeat purchasing is down overall, so every channel must be getting worse."
9. "The AI assistant told me 2025 revenue grew 61 percent, and it sounded very sure."

**Leader's view:** Read the statements and mark the three you've heard in your own organization. Then pick one and write the question you'd ask the person who said it.

<details>
<summary><b>Reveal the answers (after you've committed to yours)</b></summary>

| # | The trap | The check |
|---|---|---|
| 1 | Survivorship bias: you're only looking at the customers who stayed, so the reasons people leave are invisible | Include the customers who left and compare |
| 2 | Non-response bias: people who answer a survey are often the happiest or angriest ones | Ask what share answered, and whether responders resemble everyone |
| 3 | Confounding: the holiday season raises both email volume and sales | Remove the season, or compare like months with like months |
| 4 | Base rate neglect: if only 5 percent leave, "predict nobody leaves" is 95 percent accurate too | Ask what a do-nothing guess would score |
| 5 | Confirmation bias: you searched for support and discarded the rest | Write down what would change your mind, then go looking for it |
| 6 | Sunk cost fallacy: past spending can't be recovered, so it shouldn't drive the choice | Ask "if we were starting today, would we choose this?" |
| 7 | Groupthink and appeal to authority: agreement followed rank | Collect independent opinions before the discussion, junior people first |
| 8 | Simpson's paradox: a trend in the whole can reverse inside the groups (you'll see this in Module 06) | Look at the groups and the total |
| 9 | Automation bias: a fluent, confident answer feels more reliable than it is | Verify against a source you trust (finance's report says 54 percent) |

</details>

<p style="border-bottom: 1px solid lightgrey;"></p>

<img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/pencil2.png?raw=true"> <h2>5.2 A Field Guide, by Stage of Analysis</h2>

There are hundreds of named biases and fallacies, which is far too many to use at your desk. This guide keeps seventeen, grouped by the stage of work where each one strikes hardest, so you know what to watch for *right now*.

**When you're sourcing data (Modules 02 and 03)**

| Trap | What it is | The check |
|---|---|---|
| Selection bias | The records you have aren't like the ones you don't | Who is missing? |
| Survivorship bias | You study only what survived (customers who stayed, projects that finished) | Include the ones that dropped out |
| Non-response bias | The people who answer differ from the people who don't | Compare responders with the full list on something you already know |
| Definition drift | The way something is measured or defined changes over time or between teams | Write down the definition and the date it applies to |

**When you're describing data (Module 04)**

| Trap | What it is | The check |
|---|---|---|
| Cherry-picking | Choosing the time window or subset that flatters the result | Show the full period, and say why you picked yours |
| Anchoring and framing | The first number you see, or the way a number is worded, sways your judgment | Restate the result a second way (points and percent) |
| Base rate neglect | Ignoring how common something is to begin with | Ask what a do-nothing guess would score |

**When you're diagnosing (Module 06)**

| Trap | What it is | The check |
|---|---|---|
| Confirmation bias | You seek and favor evidence that supports what you already believe | Write down what would change your mind, then look for it |
| Confounding (correlation is not causation) | A third factor drives two things that move together, and "after, therefore because" is a common version | What else changed? Compare like with like |
| Simpson's paradox | A pattern in the groups reverses when you combine them | Look at the groups and the total |
| Multiple comparisons | Slice data enough ways and a pattern will appear by chance (the "sharpshooter" paints the target after firing) | Decide the question first, and test the pattern on fresh data |
| Regression to the mean | An extreme result tends to look less extreme next time on its own | Be wary of "it improved after we acted" when you acted on a bad stretch |

**When you're predicting (Module 07)**

| Trap | What it is | The check |
|---|---|---|
| Overfitting | A model that memorized the noise of the past | Test it on data it hasn't seen |
| Overconfidence (planning fallacy) | Ranges that are too narrow and schedules that are too rosy | Give ranges, and track forecasts against what happened |
| Automation bias | Trusting an output because it came from a machine or sounded fluent | Verify against a trusted source, and ask how it could be wrong |

**When you're deciding (Module 08)**

| Trap | What it is | The check |
|---|---|---|
| Sunk cost fallacy | Letting past spending, which can't be recovered, drive the next choice | If we were starting today, would we choose this? |
| Groupthink and appeal to authority | Agreement follows rank or the room's mood | Gather independent views first, and hear the most junior person first |

**A word on AI assistants.** They add a wrinkle to every row above. An assistant produces fluent, confident text whether or not it's right, and it can invent numbers, sources, and column names. Fluency feels like authority. So treat its output as a draft from a fast, untested colleague: ask where a number came from, check it against something you trust, and test it on cases where you know the answer (the "check the helper" habit from Module 03).

If you want to go deeper than seventeen, [Wikipedia's list of cognitive biases](https://en.wikipedia.org/wiki/List_of_cognitive_biases), its [list of fallacies](https://en.wikipedia.org/wiki/List_of_fallacies), and the [Cognitive Bias Codex](https://upload.wikimedia.org/wikipedia/commons/6/65/Cognitive_bias_codex_en.svg) are good references, and the codex is worth a look every few months. Treat them as dictionaries, though, and not as a place to learn habits.

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/point1.png?raw=true"><b>Activity 2: Audit Two Claims</b></p>

Two of the leadership team's favorite claims are about to meet the data. The data team has prepared two summary tables for you.

<p><img style="margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/checkmark.png?raw=true"><b>Steps</b></p>

**Hands-on:**

**Claim 1: "Loyalty members spend twice as much as everyone else, so the program works."** The program launched on July 1, 2024.

1. Open `supplements/customer_spend_summary.csv`. (One row is a consumer customer acquired before 2025.) Compute the average `spend_2025` for members (`loyalty_member` = 1) and for non-members. What's the ratio?
2. Which trap or traps could apply?
3. Run a check that uses time. Keep only customers acquired before 2024-01-01. Compare the average `spend_h1_2024` (January through June 2024, *before the program existed*) for those who later joined with those who didn't. What do you find?
4. What does that say about the claim? (If you have time, compare the change from `spend_h1_2024` to `spend_h1_2025` for each group.)

**Claim 2: "Ninety-four percent of our customers are satisfied."**

1. Open `supplements/survey_audit.csv`. (One row is a customer who was emailed the survey.) What share of them responded (`responded` = 1)?
2. Compare the share who returned an item (`returned_item` = 1) among responders and among non-responders. What do you see, and what does it suggest about who answered?
3. Rewrite the claim so it's honest about what the data shows.

(Claim 3, "the average order is $283," you settled in Module 04. Claim 4, "email drives sales," you'll take on in Module 06.)

**Leader's view:** For any "our program works" claim, ask for the *before* comparison: how did the people who joined behave before they joined? For any survey number, ask for the response rate and a comparison of responders with everyone. The honest rewrites are below.

<details>
<summary><b>The honest versions of the claims</b></summary>

**Claim 1.** "Loyalty members spend about twice as much as non-members. But the people who joined were already spending about 1.5 times as much before the program launched, so most of the gap was there from the start. Members' spending fell less than non-members' over the same period, which hints at a modest benefit, but this comparison can't prove it."

**Claim 2.** "Of the roughly 9 percent of customers who answered the survey, 94 percent said they were satisfied. The people who answered were about half as likely to have returned an item as the people who didn't, so the satisfaction of all customers is probably lower than 94 percent."

</details>

<p style="border-bottom: 1px solid lightgrey;"></p>

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/point1.png?raw=true"><b>Checkpoint: Your Checklist and a Premortem</b></p>

Two short tasks, four minutes in all.

1. **Build your card (two minutes).** From the eight checks in 5.1, circle the five you'll use every time you share a number. Write them on a card or in a note. Scale your effort to the stakes: a quick check for a casual question, and a premortem and a second reviewer for a decision that costs real money. (Time is the enemy of thorough analysis, but there is such a thing as analysis paralysis. Match the rigor to the risk.)
2. **Run a premortem (two minutes).** It's late next year. Lantern Peak spent its $150,000, and it turned out badly. Write down three reasons why. Keep them. In Module 08 you'll see whether your decision survives them.

<details>
<summary><b>Instructor notes</b></summary>

**Timing (35 minutes).** Lecture 5.1 for 7 minutes, Activity 1 for 6, lecture 5.2 for 9, Activity 2 for 9, checkpoint for 4. If you run short, do Claim 1 in Activity 2 and assign Claim 2 as homework.

**Why this module is built the way it is.** Early training that mainly described biases had little success, and later studies found that practice with personalized feedback (games most of all, and videos to a lesser degree) worked better. So run Activity 1 as a quick-fire round. Have each learner write an answer, then reveal one row at a time and let people score themselves. Do the practice *before* the field guide, then let the guide organize what they've just felt.

**Talk track.**
- Say early and often that everyone has these habits, including you. The goal is to build team habits. Avoid accusing individuals. Use "the data" and "the claim" as the subject.
- In 5.1, spend your time on the eight checks. They're the part learners will use on Monday.
- Be honest that some famous psychology results haven't replicated, and say that's why the guide is short. It models the skepticism you're teaching.
- In 5.2, don't read the tables out. Pick the three traps that match your audience (finance learners tend to love base rates and sunk costs, and operations learners tend to love survivorship and definition drift).

**Answer key, Activity 1.** The table in the reveal is the answer key. Accept any defensible variant. Several statements have more than one trap (statement 3 involves confounding and a possible "after, therefore because" fallacy, and statement 7 involves authority and groupthink). The point is to name a reasonable trap and a concrete check.

**Answer key, Activity 2.**
- Claim 1, step 1: members average $336.60 in 2025 (322 customers) against $168.28 for non-members (3,718 customers), a ratio of 2.00.
- Claim 1, step 3: among customers acquired before 2024, members who later joined averaged $116.83 in January to June 2024 (149 customers), against $77.08 for non-members. Ratio about 1.5. The members were already better customers before the program existed (self-selection).
- Claim 1, step 4: for the same customers in January to June 2025, members averaged $107.05 and non-members $65.65. Between the two half-years, members' spending changed by about minus 8 percent and non-members' by about minus 15 percent. The gap widened a little, so there may be a modest program effect, but most of the headline difference is who joined. A proper test would compare similar customers, ideally with a randomly assigned control group.
- Claim 2, step 1: 3,155 customers were emailed, and 283 responded (9.0 percent).
- Claim 2, step 2: 8.8 percent of responders returned an item, against 17.8 percent of non-responders. Responders were about half as likely to have returned something, so they skew toward happier customers.
- Of the 283 responders, 266 rated 4 or 5 (94.0 percent).

**Common pitfalls.** Learners compare members with non-members using `spend_2025` only and stop. Prompt them with "what did these people look like before the program?" Learners include customers acquired in 2024 in the pre-launch comparison (they weren't customers for all of January to June 2024). Remind them to filter on `acquired_date`.

**If you need to cut time.** Run Activity 1 with only statements 1 through 6, and skip the premortem task (it returns in Module 08).

</details>

<p style="border-bottom: 1px solid lightgrey;"></p>

<p><img style="margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/owl.png?raw=true"><b>For Further Study</b></p>
<ul>
 <li><a href="https://openaccess.city.ac.uk/id/eprint/12324" target="_blank">Morewedge and colleagues: Debiasing decisions, improved decision making with a single training intervention</a></li>
 <li><a href="https://www.psychologicalscience.org/news/minds-business/debiasing-your-decisions.html" target="_blank">Association for Psychological Science: Debiasing Your Decisions</a></li>
 <li><a href="https://en.wikipedia.org/wiki/List_of_cognitive_biases" target="_blank">List of cognitive biases</a> and <a href="https://en.wikipedia.org/wiki/List_of_fallacies" target="_blank">list of fallacies</a></li>
 <li><a href="https://www.criticalthinking.org/pages/defining-critical-thinking/766" target="_blank">Critical thinking</a>, a closely related skill</li>
 <li>Books worth your time: <i>Thinking, Fast and Slow</i> (Kahneman) and <i>Noise</i> (Kahneman, Sibony and Sunstein), which covers decision hygiene</li>
</ul>

<p style="border-bottom: 1px solid lightgrey;"></p>

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/geopin.png?raw=true"><b>Next Steps</b></p>

Next, continue to <a href="06-find-out-why.md"><i>Module 06 - Find Out Why</i></a>.
