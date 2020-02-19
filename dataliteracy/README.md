<img width="150" style="float: right; margin: 0px 15px 15px 0px;" src="https://github.com/BuckWoody/presentations/blob/master/graphics/BWLogo002.png?raw=true"> 

# Workshop: Data Literacy

#### <i>Using Data To Make Intelligent Decisions</i>

<p style="border-bottom: 1px solid lightgrey;"></p>

<img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/textbubble.png?raw=true"> <h2>About this Workshop</h2>

Welcome to this workshop on *Data Literacy - Using Data To Make Intelligent Decisions*. In this workshop, you'll learn how to apply a rigorous analysis process and work with various data tools to make good decisions from authoritative data. 

You'll start by developing skills to find the most authoritative data, understand and use data tools including spreadsheets, databases, and programming languages, analyze the data in context, and use the data for intelligent decisions. 

This README.MD file explains how the workshop is laid out, what you will learn, and the technologies you will use in this solution.

(You can view all of the [source files for this workshop on this [github](https://lab.github.com/githubtraining/introduction-to-github) site, along with other presentations and workshops. Open this link in a new tab to find out more.](https://github.com/BuckWoody/presentations))

<p style="border-bottom: 1px solid lightgrey;"></p>

<img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/checkmark.png?raw=true"> <h3>Learning Objectives</h3>

In this workshop you'll learn how to:
<br>

- Find and source the most authoritative data
- Work with data tools
- Analyze data in context
- Create analytic results from data

<p style="border-bottom: 1px solid lightgrey;"></p>

<img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/building1.png?raw=true"> <h2>Business Applications of this Workshop</h2>

Businesses require a high level of data literacy in every role within an organization, and it is assumed these skills are gained in primary or secondary education. However, many of these skills are not given the proper amount of time or consideration during this phase of training, and students are often left to fill in the gaps on their own. 

This workshop provides a prescriptive methodology and references to learn the basics and go much deeper into each of the data literacy topics than primary education provides, and allows a modular approach to learning. You're able to move through the workshop quickly over areas you already know, and take your time on the areas you need to know more about. 

<p style="border-bottom: 1px solid lightgrey;"></p>

<img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/listcheck.png?raw=true"> <h2>Technologies used in this Workshop</h2>

The solution includes the following technologies - although you are not limited to these, they form the basis of the workshop. At the end of the workshop you will learn how to extrapolate these components into other solutions. You will cover these at an overview level, with references to much deeper training provided.

 <table style="tr:nth-child(even) {background-color: #f2f2f2;}; text-align: left; display: table; border-collapse: collapse; border-spacing: 2px; border-color: gray;">

  <tr><th style="background-color: #1b20a1; color: white;">Technology</th> <th style="background-color: #1b20a1; color: white;">Description</th></tr>

  <tr><td><i>Spreadsheets</i></td><td>Understanding tabular data manipulation and reporting is best done using an electronic spreadsheet - you'll use one in this workshop to create, edit, and explore data, and you'll learn to create reports with a spreadsheet.</td></tr>
  <tr><td>The SQL Programming Language</td><td>The Structured Query Language provides an effective query system to manipulate data and is used in many applications.</td></tr>
  <tr><td><i>The R Platform</i></td><td>The R Programming Language and Platform is a data-first programming language based around functions, and has many libraries for working in almost any data domain. It is also used in Data Science applications.</td></tr>
  <tr><td>The Python Programming Language</td><td>The Python programming language is fast becoming a default data programming language, with many packages and functions available for almost any data domain. It is also highly used in Data Science projects.</td></tr>
  <tr><td><i>Relational Database Management Systems</i></td><td>Spreadsheets and other tools are often "single-seat" based data storage systems, designed for use by one person at a time. They also do not process data, but merely hold the data and allow you to perform functions on them. A Relational Database Management System is an engine that runs on a remote system allowing multiple users to access, update and delete tabular data in a consistent, high-performing process.</td></tr>
  <tr><td>NoSQL Database Platforms</td><td>Extremely large amounts of data processing can cause issues with a purely tabular, or relational structure. Multiple systems have evolved to solve the data access at scale problem, known collectively as "Not Only SQL" (NoSQL) platforms.</td></tr>
  <tr><td><i>Data Science Tools and Platforms</i></td><td>Data Science is an umbrella term used to describe the tools, methods and processes to create predictions, clusters and other forms of prescriptive analysis over data.</td></tr>

</table>

<p style="border-bottom: 1px solid lightgrey;"></p>

<img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/owl.png?raw=true"> <h2>Before Taking this Workshop</h2>

You'll need a local system that you are able to install software on. The workshop demonstrations use Microsoft Windows as an operating system and all examples use Microsoft Windows for the workshop. Optionally, you can use a Microsoft Azure Virtual Machine (VM) to install the software on and work with the solution.

You must have a high-school equivalent or higher educational background in multiple topics for this Workshop. If you do not, you can <a href="https://github.com/BuckWoody/presentations/blob/master/dataliteracy/dataliteracy/00-pre-requisites.md" target="_blank">access the pre-requisites reference for links to assist you in learning those topics</a>. 

<img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/bulletlist.png?raw=true"> <h3>Setup</h3>

<a href="https://github.com/BuckWoody/presentations/blob/master/dataliteracy/dataliteracy/00-pre-requisites.md" target="_blank">A full pre-requisites document is located here</a>. These instructions should be completed before the workshop starts, since you will not have time to cover these in class. 

You will need a personal computer to complete the exercises, or you can use a Virtual Machine if you like. 
<i>Remember to turn off any Virtual Machines from the Azure Portal if you use one when not taking the class so that you do incur charges (shutting down the machine in the VM itself is not sufficient)</i>.

<p style="border-bottom: 1px solid lightgrey;"></p>

<img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/education1.png?raw=true"> <h2>Workshop Details</h2>

This workshop uses various data technologies and languages, with a focus on creating decisions from data using various architectures and implementations, development languages and platforms.

<table style="tr:nth-child(even) {background-color: #f2f2f2;}; text-align: left; display: table; border-collapse: collapse; border-spacing: 5px; border-color: gray;">

  <tr><td style="background-color: Cornsilk; color: black; padding: 5px 5px;">Primary Audience:</td><td style="background-color: Cornsilk; color: black; padding: 5px 5px;">Professionals tasked with data analysis</td></tr>
  <tr><td>Secondary Audience:</td><td> Students new to the data analysis discipline who wish to learn more about the processes and tools use in that field</td></tr>
  <tr><td style="background-color: Cornsilk; color: black; padding: 5px 5px;">Level: </td><td style="background-color: Cornsilk; color: black; padding: 5px 5px0;"> 200-400 </td></tr>
  <tr><td>Type:</td><td>In-Person, or from github</td></tr>
  <tr><td style="background-color: Cornsilk; color: black; padding: 5px 5px;">Length: </td><td style="background-color: Cornsilk; color: black; padding: 5px 5px;">4-8</td></tr>

</table>

<p style="border-bottom: 1px solid lightgrey;"></p>

<img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/pinmap.png?raw=true"> <h2>Related Workshops</h2>

 - [Data Literacy Training and Certification](https://dataliteracy.com/)

<p style="border-bottom: 1px solid lightgrey;"></p>

<img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/bookpencil.png?raw=true"> <h2>Workshop Modules</h2>

This is a modular workshop, and in each section, you'll learn concepts, technologies and processes to help you complete the solution.

<table style="tr:nth-child(even) {background-color: #f2f2f2;}; text-align: left; display: table; border-collapse: collapse; border-spacing: 5px; border-color: gray;">

  <tr><td style="background-color: AliceBlue; color: black;"><b>Module</b></td><td style="background-color: AliceBlue; color: black;"><b>Topics</b></td></tr>

  <tr><td><a href="https://github.com/BuckWoody/presentations/blob/master/dataliteracy/dataliteracy/01-find_authoritative_data.md" target="_blank">01 - Find Authoritative Data </a></td><td> In this Module you'll learn more about finding data sources and using the most authoritative data in your analysis.</td></tr>
  <tr><td style="background-color: AliceBlue; color: black;"><a href="https://github.com/BuckWoody/presentations/blob/master/dataliteracy/dataliteracy/02-work_with_data_tools.md" target="_blank">02 - Work with Data Tools</a> </td><td td style="background-color: AliceBlue; color: black;"> You can work with data using only your mind, or pencil and paper. In fact, while you’re learning, using basic resources like these can be optimal. But soon you will find that you need more powerful tools. This module - the longest and most complicated topic - will cover the major tools from the simple to the complex.</td></tr>
  <tr><td><a href="https://github.com/BuckWoody/presentations/blob/master/dataliteracy/dataliteracy/03-analyze_data_in_context.md" target="_blank">03 - Analyze Data In Context </a></td><td> Analyzing data at its simplest means looking at the data, from multiple perspectives and using multiple tools, in context. The specific process you’ll follow to analyze a given data set largely depends on the goal of the analysis, the type of data, and the area of analysis (such as business, science, etc.). This Module covers that process.</td></tr>
  <tr><td style="background-color: AliceBlue; color: black;"><a href="https://github.com/BuckWoody/presentations/blob/master/dataliteracy/dataliteracy/04-use_data_for_intelligent_decisions.md" target="_blank">04 - Use Data for Intelligent Decisions</a> </td><td td style="background-color: AliceBlue; color: black;"> Applying your analysis to creating intelligent decisions is the goal of data literacy. This module covers that process, and explains how to take your analysis and form a course of action.</td></tr>  

</table>

<p style="border-bottom: 1px solid lightgrey;"></p>

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/geopin.png?raw=true"><b>Next Steps</b></p>

Next, Continue to <a href="https://github.com/BuckWoody/presentations/blob/master/dataliteracy/dataliteracy/00-pre-requisites.md" target="_blank"><i> Pre-Requisites</i></a>