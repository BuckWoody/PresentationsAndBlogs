<img width="150" style="float: right; margin: 0px 15px 15px 0px;" src="graphics/logo.png">

# Workshop: Data Literacy

#### <i>Using Data To Make Intelligent Decisions</i>

<p style="border-bottom: 1px solid lightgrey;"></p>

<img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/textbubble.png?raw=true"> <h2>About this Workshop</h2>

Welcome to this workshop on *Data Literacy: Using Data To Make Intelligent Decisions*. In about six hours, you'll learn how to find data you can trust, work with it, describe what happened, find out why, look ahead, decide what to do, and explain your decision so that others can act on it and check your work.

You'll follow one fictional company, Lantern Peak Supply Co., from a messy pile of files to a defensible decision about where to spend $150,000. Every module can be taught or taken on its own, and taken in order each one builds on the last.

This README explains how the workshop is laid out, what you'll learn, and what you'll need.

<p style="border-bottom: 1px solid lightgrey;"></p>

<img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/checkmark.png?raw=true"> <h3>Learning Objectives</h3>

In this workshop you'll learn how to:
<br>

- Find, verify, and document the most authoritative data
- Work with data using any tool: clean it, combine it, summarize it, and check your work
- Describe what happened, using the right measures and honest charts
- Diagnose why it happened, and tell a real cause from a coincidence
- Predict what's likely to happen next, and judge a prediction (or a vendor's claim) fairly
- Decide what to do under uncertainty, using value, break-even, and staged decisions
- Recognize the biases, fallacies, and data traps that fool smart people
- Explain a decision clearly, and learn from what happens next

<p style="border-bottom: 1px solid lightgrey;"></p>

<img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/building1.png?raw=true"> <h2>Business Applications of this Workshop</h2>

Businesses need a high level of data literacy in every role, from the newest analyst to the executive team. It's usually assumed these skills were picked up in school, but many were given little time there, and people are left to fill in the gaps on their own.

This workshop gives you a practical method and a set of habits. The four kinds of analysis (descriptive, diagnostic, predictive, and prescriptive) are taught in order, each one resting on the one before, and a section on biases and data traps sits in the middle because every kind of analysis can mislead you. Each activity comes in two versions: a hands-on version, and a leader's view that shows what to ask your team for and what a good answer looks like.

<p style="border-bottom: 1px solid lightgrey;"></p>

<img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/listcheck.png?raw=true"> <h2>Tools Used in this Workshop</h2>

The workshop teaches how to use tools well, and it uses no product in particular. Any tool in each row will do.

<table style="text-align: left; border-collapse: collapse;">
 <tr><th style="background-color: #1b20a1; color: white;">Kind of tool</th><th style="background-color: #1b20a1; color: white;">How it's used</th></tr>
 <tr><td><i>A spreadsheet</i></td><td>Every activity can be done in a spreadsheet application, desktop or browser-based.</td></tr>
 <tr><td>SQLite and SQL</td><td>An optional path. SQLite is a free, single-file database, and SQL is the standard query language. Nothing has to be installed on a server.</td></tr>
 <tr><td><i>A browser-based data workbench</i></td><td>An optional small Python and Flask web page (included) that lets you create, read, update, and delete rows in a copy of the database, so you can see what a database allows and refuses.</td></tr>
 <tr><td>BI, notebooks, and programming languages</td><td>Described and compared in Module 03, so you can choose well. No installs are required.</td></tr>
 <tr><td><i>AI assistants</i></td><td>Used as a helper in several modules, with habits for checking their work. The workshop recommends approved, local tools and never sharing confidential data.</td></tr>
</table>

<p style="border-bottom: 1px solid lightgrey;"></p>

<img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/owl.png?raw=true"> <h2>Before Taking this Workshop</h2>

You need a computer with a spreadsheet application and a plain text editor. Nothing else is required. All of the data is included in the `case-data` folder, and everything runs on your own machine with no accounts or cloud services.

There's no separate prerequisites page. Module 00 has an eight-question warm-up that helps you decide where to move quickly and where to slow down, with a few optional refreshers.

<p style="border-bottom: 1px solid lightgrey;"></p>

<img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/education1.png?raw=true"> <h2>Workshop Details</h2>

<table style="border-collapse: collapse; border-spacing: 5px;">
 <tr><td style="background-color: Cornsilk; padding: 5px;">Primary Audience:</td><td style="background-color: Cornsilk; padding: 5px;">Business and technical professionals, from entry level to executives</td></tr>
 <tr><td>Secondary Audience:</td><td>Students who want to learn how data is used to make decisions</td></tr>
 <tr><td style="background-color: Cornsilk; padding: 5px;">Level:</td><td style="background-color: Cornsilk; padding: 5px;">100-300</td></tr>
 <tr><td>Type:</td><td>In person, or self-paced from GitHub</td></tr>
 <tr><td style="background-color: Cornsilk; padding: 5px;">Length:</td><td style="background-color: Cornsilk; padding: 5px;">About 6 hours (360 minutes), plus breaks</td></tr>
</table>

<p style="border-bottom: 1px solid lightgrey;"></p>

<img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/pinmap.png?raw=true"> <h2>Related Workshops</h2>

- [Data Literacy Training and Certification](https://dataliteracy.com/)

<p style="border-bottom: 1px solid lightgrey;"></p>

<img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/bookpencil.png?raw=true"> <h2>Workshop Modules</h2>

This is a modular workshop. Each module opens with a "Starting here?" box, so you can begin anywhere, and each one closes with a short skeptic's checkpoint.

<table style="border-collapse: collapse;">
 <tr><td style="background-color: AliceBlue;"><b>Module</b></td><td style="background-color: AliceBlue;"><b>Minutes</b></td><td style="background-color: AliceBlue;"><b>Topics</b></td></tr>
 <tr><td><a href="modules/00-start-here.md">00 - Start Here</a></td><td>10</td><td>How the workshop builds, the four kinds of analysis, the Lantern Peak case, and a warm-up.</td></tr>
 <tr><td style="background-color: AliceBlue;"><a href="modules/01-data-basics.md">01 - Data Basics</a></td><td style="background-color: AliceBlue;">30</td><td style="background-color: AliceBlue;">What data is, the kinds and scales of data, tables, keys, and the data dictionary.</td></tr>
 <tr><td><a href="modules/02-find-and-trust-data.md">02 - Find and Trust Data</a></td><td>40</td><td>Finding sources, authoritative data, verifying it, and working out why two reports disagree.</td></tr>
 <tr><td style="background-color: AliceBlue;"><a href="modules/03-work-with-data.md">03 - Work with Data</a></td><td style="background-color: AliceBlue;">40</td><td style="background-color: AliceBlue;">The data work cycle, kinds of tools, cleaning, combining, summarizing, and tying out.</td></tr>
 <tr><td><a href="modules/04-see-what-happened.md">04 - See What Happened</a></td><td>50</td><td>Descriptive analysis: measures, the middle and the spread, and honest charts.</td></tr>
 <tr><td style="background-color: AliceBlue;"><a href="modules/05-the-skeptics-toolkit.md">05 - The Skeptic's Toolkit</a></td><td style="background-color: AliceBlue;">35</td><td style="background-color: AliceBlue;">Biases, fallacies, and data traps, practiced with feedback, and a checklist of habits.</td></tr>
 <tr><td><a href="modules/06-find-out-why.md">06 - Find Out Why</a></td><td>45</td><td>Diagnostic analysis: drilling down, mix versus rate, correlation versus cause.</td></tr>
 <tr><td style="background-color: AliceBlue;"><a href="modules/07-look-ahead.md">07 - Look Ahead</a></td><td style="background-color: AliceBlue;">45</td><td style="background-color: AliceBlue;">Predictive analysis: forecasting, judging a model, and how predictions mislead.</td></tr>
 <tr><td><a href="modules/08-decide-what-to-do.md">08 - Decide What to Do</a></td><td>45</td><td>Prescriptive analysis: framing, value and break-even, scoring, and staged decisions.</td></tr>
 <tr><td style="background-color: AliceBlue;"><a href="modules/09-explain-act-learn.md">09 - Explain, Act, Learn</a></td><td style="background-color: AliceBlue;">20</td><td style="background-color: AliceBlue;">The one-page decision brief, a decision log, and a post-mortem.</td></tr>
</table>

<p style="border-bottom: 1px solid lightgrey;"></p>

<img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/pencil2.png?raw=true"> <h2>What Is in This Repository</h2>

| Folder | What it holds |
|---|---|
| `modules/` | The ten modules, plus the chart images they use |
| `case-data/` | The Lantern Peak data (raw and cleaned), a data dictionary, source notes, an optional Adventure Works extract, and the scripts that rebuild it all |
| `tools/data-workbench/` | An optional local web page for creating, reading, updating, and deleting rows in a copy of the database |
| `tools/*.py` | Maintenance scripts: a pre-deployment check, a link checker, an icon localizer, and a learner-edition builder |
| `facilitator/` | Answer keys and design notes for instructors. Keep this folder out of the learners' copy |
| `graphics/` | The logo |

<p style="border-bottom: 1px solid lightgrey;"></p>

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/geopin.png?raw=true"><b>Next Steps</b></p>

Next, continue to <a href="modules/00-start-here.md"><i>Module 00 - Start Here</i></a>.
