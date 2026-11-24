<img width="150" style="float: right; margin: 0px 15px 15px 0px;" src="../graphics/logo.png">

# Workshop: Data Literacy

#### <i>Using Data To Make Intelligent Decisions</i>

<p style="border-bottom: 1px solid lightgrey;"></p>

<img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/textbubble.png?raw=true"> <h2>7 - Look Ahead</h2>

| Minutes | What happens |
|---|---|
| 0 to 8 | Lecture: forecasting with trend, season, and honest error |
| 8 to 17 | Activity 1: Forecast the Quarter |
| 17 to 26 | Lecture: predicting categories, and what a model's "accuracy" really means |
| 26 to 34 | Activity 2: Judge the Churn Claim |
| 34 to 39 | Lecture: how predictions mislead |
| 39 to 43 | Activity 3: Spot the Flaw |
| 43 to 45 | Skeptic's checkpoint: false precision |

> **Starting here?** You need the Lantern Peak case files (the `case-data` folder), in particular `raw/finance_monthly_revenue.csv` and `supplements/churn_model_scores.csv`. A quick catch-up: Lantern Peak Supply Co. is a fictional online retailer of camping and hiking gear. Its leadership team is planning next year, and a vendor has pitched a churn-prediction service that it says is "95 percent accurate." You should be comfortable with percent change, seasonality (Module 04), and the base rate idea from Module 05.

<p style="border-bottom: 1px solid lightgrey;"></p>

So far you've looked backward. *Predictive* analysis looks forward, and it answers the question **what is likely to happen?** It does that by finding patterns in the past and assuming they'll continue, at least roughly. That assumption is where most of the trouble lives, so this module is as much about what predictions *can't* tell you as about how to make them.

Keep one idea in mind all the way through: **a prediction is an estimate.** It can be useful and it can be wrong, so an honest prediction always comes with a sense of how wrong it might be.

<img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/pencil2.png?raw=true"> <h2>7.1 Forecasting a Number</h2>

Predictive questions come in two flavors. *How much or how many?* asks for a number (next quarter's revenue). *Which one?* asks for a category (will this customer leave, yes or no?). We'll start with numbers.

**Data over time has structure.** From Module 04: a *trend* (the long-run direction), *seasonality* (a pattern that repeats on a calendar), and *noise* (random wiggle). A forecast has to account for the first two and accept the third.

**Always start with a simple baseline.** Fancy methods (smoothing, regression, machine learning) are only worth using if they beat a simple one. Three baselines are easy to run in any spreadsheet:

- **Flat:** assume next period looks like the average of the last few. (It ignores trend and season.)
- **Same period last year:** use last year's value for the same month. (It captures the season but ignores growth.)
- **Same period last year, times a growth factor:** last year's value for that month, multiplied by how much the business has been growing year over year. (It captures both, and it assumes the growth rate holds.)

**Backtest before you trust it.** To find out how good a method is, hide the most recent months, forecast them using only the earlier data, and compare your forecast with what really happened. That's a *backtest*. Measure the miss as a percentage of the actual value for each month, and average them (the *mean absolute percentage error*, or MAPE). It tells you how far off the method tends to be.

**Turn the error into a range.** A single number looks confident and tells you nothing about the risk. A range, such as "about $450,000, give or take 13 percent," is honest. You can also build *scenarios* ("if growth cools by half, we'd see...") to show decision-makers what depends on the assumption.

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/point1.png?raw=true"><b>Activity 1: Forecast the Quarter</b></p>

You'll forecast Lantern Peak's holiday quarter using only the data available on October 1, 2025, find out how three simple methods would have done, and then forecast the next quarter.

<p><img style="margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/checkmark.png?raw=true"><b>Steps</b></p>

**Hands-on:**

1. Open `case-data/raw/finance_monthly_revenue.csv`. Pretend it's October 1, 2025, and use only the data through September 2025. Forecast October, November, and December 2025 three ways: (a) *flat* (the average of July through September 2025), (b) *same month last year*, and (c) *same month last year times a growth factor* (the total of January through September 2025 divided by the total of January through September 2024).
2. Compare each forecast with the actual values for October through December. For each method, compute the percent error for each month, and the average error across the three.
3. Which method did best? Why did each of the others miss the way it did?
4. Now forecast January through March 2026 with the best method, using this time the growth factor from the most recent quarter (October through December 2025 divided by October through December 2024). Give a range using your backtest error. Then try a scenario where growth cools to a factor of 1.25. How much does the answer move?

**Leader's view:** When someone hands you a forecast, ask four questions. *What would a simple baseline say, and does this beat it? How far off has it been when tested on past data? What range should I plan for? Which assumption, if wrong, would change the answer most?* A good forecaster welcomes every one of them.

<p style="border-bottom: 1px solid lightgrey;"></p>

<img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/pencil2.png?raw=true"> <h2>7.2 Predicting a Category, and What "Accuracy" Means</h2>

Many predictions ask for a *yes or no*: Will this customer leave? Will this order be returned? A model scores each case, and you choose a *threshold*: above it, you call the case a "yes."

**The confusion matrix.** Once you have predictions and the real outcomes, count the four possibilities.

| | Actually happened | Actually didn't happen |
|---|---|---|
| **Predicted yes** | True positive (TP) | False positive (FP) |
| **Predicted no** | False negative (FN) | True negative (TN) |

Three measures come from those four counts:

- **Accuracy** is the share of all predictions that were right: (TP + TN) divided by everything.
- **Precision** asks, of the cases we *flagged*, what share really happened? TP divided by (TP + FP).
- **Recall** asks, of the cases that *really happened*, what share did we catch? TP divided by (TP + FN).

**The base rate trap.** When the thing you're predicting is rare, accuracy is nearly meaningless. If only 5 percent of customers leave, a "model" that predicts *nobody leaves* is 95 percent accurate and entirely useless. Always ask what a do-nothing guess would score, and judge the model against *that*. Precision and recall are usually more honest when the outcome is rare.

**Errors have different prices.** Missing a customer who is about to leave (a false negative) and sending a discount to someone who was staying anyway (a false positive) cost different amounts. A useful model is judged on what its decisions are worth as well as how often they're right.

**What machine learning is.** Instead of writing rules by hand, you show a program many examples (the *inputs*, sometimes called *features*, along with the known *outcomes*, called *labels*) and it finds patterns it can use on new cases. Everything it learns comes from the examples, including their gaps and biases. Generative AI tools, including chat assistants, are a related kind of model. They produce fluent text or images by predicting what is likely to come next, which makes them good at sounding right, and sounding right is different from being right. That's why everything else in this module applies to them too.

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/point1.png?raw=true"><b>Activity 2: Judge the Churn Claim</b></p>

A vendor says its churn model is "95 percent accurate." In a pilot, it scored 2,000 Lantern Peak customers and then waited six months to see who really left. The results are in your files.

<p><img style="margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/checkmark.png?raw=true"><b>Steps</b></p>

**Hands-on:**

1. Open `case-data/supplements/churn_model_scores.csv`. (One row is a customer. `predicted_churn` is the model's call, and `actual_churn` is what happened, where 1 means the customer left.) Count how many customers fall in each of the four boxes of the confusion matrix.
2. Compute the accuracy, the precision, and the recall.
3. What would a model that always predicts "no one leaves" score on accuracy? Compare that with the vendor's number.
4. Write three questions you'd ask the vendor before signing anything.
5. *(If you have time)* The vendor says Lantern Peak could send each flagged customer a $20 offer, and that the offer saves 25 percent of the customers who would have left. A saved customer is worth about $150 in gross profit. Work out the value of acting on the flagged customers across the 2,000 in the pilot: what you'd spend, and what you'd gain.

**Leader's view:** When a vendor quotes one accuracy figure, ask four things. *What does a do-nothing guess score? What are the precision and recall for the group we'd act on? How was it tested on customers the model never saw? What does it cost when it's wrong?* A confident vendor will have the answers ready. A vague one is telling you something.

<details>
<summary><b>Show the confusion matrix and the answers to Activity 2</b></summary>

| | Left | Stayed |
|---|---:|---:|
| **Predicted to leave** | 30 | 22 |
| **Predicted to stay** | 70 | 1,878 |

Accuracy is (30 + 1,878) divided by 2,000, which is 95.4 percent. Precision is 30 divided by 52, which is 58 percent. Recall is 30 divided by 100, which is 30 percent. A model that always says "stays" scores 1,900 out of 2,000, which is 95.0 percent, so the vendor's headline adds almost nothing. The model also misses 70 of the 100 customers who left.

For step 5: you'd spend 52 times $20, which is $1,040. The offer saves about 25 percent of the 30 real leavers you reached, which is 7.5 customers, worth about $1,125. The net gain is about $85 across 2,000 customers, close to break-even. Precision matters: 22 of the 52 offers went to people who weren't leaving.

</details>

<p style="border-bottom: 1px solid lightgrey;"></p>

<img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/pencil2.png?raw=true"> <h2>7.3 How Predictions Mislead</h2>

Beyond the base rate trap, a few other failures show up again and again.

- **Overfitting.** A model that memorizes the quirks of past data scores brilliantly on that data and badly on anything new. The defense is to hold some data back (a *test set*) that the model never sees while it's being built, and to judge it only on that.
- **Leakage.** The model is given information it wouldn't have at the moment it has to predict, such as a field that's filled in *after* the outcome. It looks like a brilliant predictor because it's cheating.
- **Drift.** The world changes, and the patterns the model learned stop holding. A model built before a pricing change, a new competitor, or a new channel mix gets worse without anyone noticing.
- **False precision.** A forecast stated to the cent suggests an accuracy it doesn't have.
- **Automation bias.** People trust a number because a system produced it. This applies to AI assistants too. They answer fluently, and they can invent a figure when they don't know. If you use one for a forecast, ask for the *method*, the *range*, and the *assumptions*, and check the result against your own simple baseline.

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/point1.png?raw=true"><b>Activity 3: Spot the Flaw</b></p>

Each of these vendor claims has a problem. Name it before you open the reveal.

<p><img style="margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/checkmark.png?raw=true"><b>Steps</b></p>

**Hands-on:** For each claim, write down what's wrong and what you'd ask.

1. "Our model predicts product returns with 99 percent accuracy on the order history we trained it on."
2. "The strongest predictor of churn in our model is whether the customer's `account_closed` flag is set."
3. "We trained the model on shopping behavior from before you opened your wholesale channel. It will predict this year's orders just as well."

**Leader's view:** Pick the claim that sounds most like something a vendor has said to you. Write the one question you'd ask in reply.

<details>
<summary><b>Reveal the answers</b></summary>

1. **Overfitting (tested on the training data).** A model always looks good on the data it learned from. Ask how it did on orders it never saw.
2. **Leakage.** An account is typically closed *after* the customer decides to leave, so the flag reveals the answer. The model couldn't use that flag at the moment it needs to make a prediction. Ask what information is actually available at prediction time.
3. **Drift.** The world changed (a new channel), so the learned patterns may no longer hold. Ask how the model was tested on recent data and how it will be monitored.

</details>

<p style="border-bottom: 1px solid lightgrey;"></p>

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/point1.png?raw=true"><b>Skeptic's Checkpoint: False Precision</b></p>

Imagine you ask an AI assistant for next quarter's revenue, and it answers: "Q1 2026 revenue will be $451,208.37." **Do this now (two minutes):** list two things that should make you doubt that answer, and rewrite it as an honest statement. (Hint: look at how far off your own backtest was, and ask what method and data the assistant used.)

<details>
<summary><b>Instructor notes</b></summary>

**Timing (45 minutes).** Lecture 7.1 for 8 minutes, Activity 1 for 9, lecture 7.2 for 9, Activity 2 for 8, lecture 7.3 for 5, Activity 3 for 4, checkpoint for 2.

**Talk track.**
- Open with "a prediction is an estimate," and come back to it. Tell learners you will keep returning to "what would the do-nothing guess say?"
- In 7.1, make the baseline discipline the point. A simple method that beats a complex one is a win. Show a slide of the three baselines before the exercise.
- In 7.2, draw the confusion matrix on a whiteboard and fill it in live from the pilot data. Ask the room to guess the model's accuracy, then reveal that "always no" scores almost the same.
- On machine learning, stay at the level of "learns patterns from examples." Don't turn it into a lecture on algorithms.
- AI assistants appear in 7.2 and 7.3 on purpose. Ask the room how many have asked an assistant for a number, and what they did with it.

**Answer key, Activity 1.**
- Growth factor for step 1(c): January to September 2025 divided by January to September 2024, about 1.58.

| Method | Oct | Nov | Dec | Average error |
|---|---:|---:|---:|---:|
| Actual | $183,257 | $250,222 | $299,207 | |
| Flat (average of Jul to Sep) | $174,844 | $174,844 | $174,844 | 25.4% |
| Same month last year | $100,861 | $170,747 | $226,068 | 33.7% |
| Same month last year times 1.58 | $159,063 | $269,277 | $356,522 | 13.3% |

- Each method fails differently. The flat forecast ignores the holiday peak. Same month last year captures the season but ignores that the company grew by more than half. The growth-adjusted forecast does best, and it's still off by double digits (about 13 percent too low in October, 8 percent too high in November, and 19 percent too high in December). The growth factor from the first nine months wasn't the growth rate in the last three.
- Step 4: the latest growth factor (October to December 2025 divided by October to December 2024) is about 1.47. Q1 2025 was $304,845, so the forecast for January to March 2026 is about $448,800. Using the backtest's average error of about 13 percent, a reasonable range is roughly $389,000 to $508,000. A cooling scenario at 1.25 gives about $381,000, which is lower than the bottom of the range, so the range isn't a worst case. (Year-over-year growth by quarter in 2025 was about 1.44, 1.62, 1.62, and 1.47, so it isn't constant, and any single factor is a judgment.)

**Answer key, Activity 2.** The matrix and answers are in the reveal. Good vendor questions: What does a do-nothing guess score? What are the precision and recall? Was it tested on customers it never saw? How was "churn" defined, and over what period? What does the vendor's own data say about the offer's success rate? What does it cost when it's wrong? What happens to the model when our channel mix changes?

**Answer key, Activity 3.** The reveal is the key. Accept any reasonable variant.

**Answer key, checkpoint.** Two reasons to doubt: it's stated to the cent, which is false precision (the backtest misses by 13 percent or more), and nobody knows its method, data, or assumptions. An honest version: "Roughly $450,000, with a plausible range of about $390,000 to $510,000, assuming year-over-year growth stays near 47 percent." The assistant's number is also close to the baseline forecast, which could be a coincidence, or could mean it's doing something similar. Ask it.

**Common pitfalls.** Learners swap precision and recall. Learners forget to use only data through September when backtesting. Learners average the percent errors with signs and let the over- and under-forecasts cancel (use absolute values). Learners accept the cooling scenario as the "worst case."

**If you need to cut time.** Skip step 5 of Activity 2, or give the numbers as a handout. Run Activity 3 as a discussion.

</details>

<p style="border-bottom: 1px solid lightgrey;"></p>

<p><img style="margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/owl.png?raw=true"><b>For Further Study</b></p>
<ul>
 <li><a href="https://otexts.com/fpp3/" target="_blank">Forecasting: Principles and Practice</a> (a free online textbook)</li>
 <li><a href="https://buckwoody.github.io/presentations/ai_ml_dl/" target="_blank">AI, machine learning, and deep learning resources</a> (from the earlier version of this workshop)</li>
 <li><a href="https://www.khanacademy.org/math/statistics-probability" target="_blank">Khan Academy: Statistics and probability</a></li>
</ul>

<p style="border-bottom: 1px solid lightgrey;"></p>

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/geopin.png?raw=true"><b>Next Steps</b></p>

Next, continue to <a href="08-decide-what-to-do.md"><i>Module 08 - Decide What to Do</i></a>.
