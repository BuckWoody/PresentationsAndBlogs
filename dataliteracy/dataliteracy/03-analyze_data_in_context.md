<img width="150" style="float: right; margin: 0px 15px 15px 0px;" src="https://github.com/BuckWoody/presentations/blob/master/graphics/BWLogo002.png?raw=true"> 

# Workshop: Data Literacy

#### <i>Using Data To Make Intelligent Decisions</i>

<img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/textbubble.png?raw=true"> <h2>3 - Analyze Data In Context</h2>

In this workshop you'll cover using data to make intelligent decisions. In each module you'll get more references, which you should follow up on to learn more. Also watch for links within the text - click on each one to explore that topic.

(<a href="https://github.com/BuckWoody/presentations/blob/master/dataliteracy/dataliteracy/00-pre-requisites.md" target="_blank">Make sure you check out the <b>Pre-Requisites</b> page before you start</a>. You'll need to complete the work there before you can proceed with the workshop.)

<p style="border-bottom: 1px solid lightgrey;"></p>

Analyzing data at its simplest means looking at the data, from multiple perspectives and using multiple tools, in context. The specific process you’ll follow to analyze a given data set [largely depends on the goal of the analysis, the type of data, and the area of analysis](https://en.wikipedia.org/wiki/Analysis) (such as business, science, etc.). In general, it follows this outline:

<ol>
  <li>Gather and verify data</li>
  <li>When necessary, homogenize the data to ensure consistent comparisons and groupings</li>
  <li>Group the data into meaningful sets</li>
  <li>Examine the data using various tools and processes, in context</li>
  <li>Deriving a result from the examination</li>
  <li>Communicating and documenting the analysis, including the methods, tools and processes used in the analysis</li>
</ol>

> NOTE: In scientific and other fields, this process is augmented by adding in more components, such as creating a hypothesis (a guess of what should/could be or happen) and then performing experiments to test the hypotheses, and publishing the results for peer-review.

<h2><img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/pencil2.png?raw=true">3.1 Understanding Context</h2>

Returning to the literacy example from the first Module in this series, when you learned to read, you often encountered a word you didn’t know. When that happens, you can learn the word itself, or gain a pretty good understanding of it by understanding the other words in the sentence where it is used. This is called context.

It’s the same with data. So far in our study on Data Literacy, you’ve learned to find the sources of data and verify it. You’ve learned the types of data, and several tools you can use to manipulate it. And herein lies the biggest danger…

In many cases, people start with the tools. They spend so much time learning the tool, they don’t spend enough time locating and verifying data, or moving on to ensuring the context where it is used. Data is rarely atomic – it doesn’t often stand alone. For instance, if you read that the approval rating of a politician has gone up 10%, you might think that’s a good thing. Of course that one number doesn’t show where the approval rating stood before, what it is now, how long that took, or maybe most importantly, why.

As you learned in the last skill, this is especially pronounced in statistics – even by data professionals. Many times the average of a number is bandied about as the single measure of something – but understanding the standard deviation and other descriptive statistics quickly shows you that a single number is not to be trusted – you need other measurements to ensure you have the full picture. In fact, as you learned in Anscombe’s Quartet, sometimes the best way to get the big picture is to create a picture.

But it’s more than numerical data. As mentioned a moment ago, the situation itself around the metric provides context, as does the environment, timing, location and more. The general advice is to look around at the entire picture at each step of the analytic process. Constantly be on the lookout for something that contradicts or enforces your analysis.

The key to finding context is using multiple resources. Remember that the time, place, source and delivery methods of data can affect the meaning of data, so you should perform a thorough analysis of a topic using several sources. 

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/point1.png?raw=true"><b>Activity: Developing Context</b></p>

In this exercise, you will learn to develop context around your data. 

<p><img style="margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/checkmark.png?raw=true"><b>Steps</b></p>

- Open a new note in your favorite note-taking software.
- Select one topic you are interested in.
- Find at least three sources of data for that topic, and note their locations. 
- Next to the location of each data source, write a short paragraph defending your selection of that resource as a reliable source. If you find you cannot trust the source, write down your reason for rejecting it. 

<p style="border-bottom: 1px solid lightgrey;"></p>

<h2><img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/pencil2.png?raw=true">3.2 Being a Data Skeptic</h2>

The first step in analyzing data is to put yourself in the place of being skeptical of the data, methods, tools, and results that you will use. Be your own critic. At each step, you imagine someone saying “I don’t believe you – prove it!” Having this voice in your head will help you ensure from the start that you are being careful in your data analytic process.

And one of the best ways to do that is to understand the errors you can make in analysis. They are all logical errors, and fall into two camps: *Cognitive Biases*, and *Logical Fallacies*.

<h3>Cognitive Bias</h3>

A *Cognitive Bias* is a logical error in rationality. You'll review a list of these in a moment, and even a quick glance will show you errors you have probably seen in data analytics. Walk through each of these to understand the error, how it applies to analysis, and how to combat it in your analysis. It is useful to visit this article once every few months to refresh your understanding as you work though an analysis.

<img width="800" src="https://upload.wikimedia.org/wikipedia/commons/6/65/Cognitive_bias_codex_en.svg">
<br>
<i>Image Source: <a href="https://upload.wikimedia.org/wikipedia/commons/6/65/Cognitive_bias_codex_en.svg">Wikimedia Commons</i></a>
<br>

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/point1.png?raw=true"><b>Activity: Review Cognitive Biases</b></p>

In this exercise you will evaluate various Cognitive Biases and detail how they can affect your data analysis.

<p><img style="margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/checkmark.png?raw=true"><b>Steps</b></p>

- Open [this resource in a new tab](https://en.wikipedia.org/wiki/List_of_cognitive_biases#Decision-making,_belief,_and_behavioral_biases).
- Review the list, and select three biases you think you may have committed recently.
- Click on each of those, and in your notes explain a mitigation to those biases you can take.

<p style="border-bottom: 1px solid lightgrey;"></p>

<h3>Logical Fallacies</h3>

The next step after you have worked to eliminate as much bias as you can from your data and assumptions is to examine the conclusions you come to. A *Logical Fallacy* is also a logical error, but in this case it involves reasoning, argument or proof. Once again there’s another list to study, and the list that follows will help you to do that. It’s actually a bit overwhelming, and that’s why many people don’t take the time to do it.

However, understanding these fallacies will keep you from the major errors you can make in creating a conclusion from data.
<br>

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/point1.png?raw=true"><b>Activity: Recognize a Logical Fallacy</b></p>

In this exercise you will examine a list of Logical Fallacies, and then compare those to a claim about a topic to see if you recognize any fallacies in their conclusions.

<p><img style="margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/checkmark.png?raw=true"><b>Steps</b></p>

- In your notes, using your topic of interest, locate one article or online resource that draws a conclusion from data.
- Open [this reference in another tab](https://en.wikipedia.org/wiki/List_of_fallacies) and review the list quickly.
- Document any Logical Fallacies in the conclusions drawn in your resource. 

<p style="border-bottom: 1px solid lightgrey;"></p>

> NOTE: Time is the enemy of thorough analysis, but there is such a thing as "analysis to paralysis"

<p style="border-bottom: 1px solid lightgrey;"></p>

<p><img style="margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/owl.png?raw=true"><b>For Further Study</b></p>
<ul>
    <li><a href="https://www.criticalthinking.org/pages/defining-critical-thinking/766" target="_blank">Critical Thinking is another important skills, related to Data Literacy.</a></li>
</ul>

<p><img style="margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/owl.png?raw=true"><b>Next Steps</b></p>

<a href="https://github.com/BuckWoody/presentations/blob/master/dataliteracy/dataliteracy/04-use_data_for_intelligent_decisions.md" target="_blank">Now move on to the next topic: 4 - Use Data for Intelligent Decisions</a>