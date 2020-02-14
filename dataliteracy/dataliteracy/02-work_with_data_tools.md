<img width="150" style="float: right; margin: 0px 15px 15px 0px;" src="https://github.com/BuckWoody/presentations/blob/master/graphics/BWLogo002.png?raw=true"> 

# Workshop: Data Literacy

#### <i>Using Data To Make Intelligent Decisions</i>

<img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/textbubble.png?raw=true"> <h2>2 - Work with Data Using Various Tools</h2>

In this workshop you'll cover using data to make intelligent decisions. In each module you'll get more references, which you should follow up on to learn more. Also watch for links within the text - click on each one to explore that topic.

(<a href="https://github.com/BuckWoody/presentations/blob/master/dataliteracy/dataliteracy/00-pre-requisites.md" target="_blank">Make sure you check out the <b>Pre-Requisites</b> page before you start</a>. You'll need to complete the work there before you can proceed with the workshop.)

<p style="border-bottom: 1px solid lightgrey;"></p>

Now that you have defined your data, you need to examine it, group it, and change it to show what you want to know.

You can work with data using only your mind, or pencil and paper. In fact, while you’re learning, using basic resources like these can be optimal. But soon you will find that you need more powerful tools.

<h2><img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/pencil2.png?raw=true">2.1 Tools For Querying Data</h2>

<h3>2.1.1 Spreadsheets</h3>
You’ll use various tools to query, alter, and display the results of data. <a href="https://products.office.com/en-us/free-office-online-for-the-web">The first tool to learn more about querying and entering data is an electronic spreadsheet</a>. A spreadsheet uses a "tabular" display of data - meaning rows of data divided into columns for each heading of data. The intersection of a row and column is called a "cell", and it contains one datum, or element, or attribute. These terms are often interchangeable. 

A spreadsheet not only stores the data, but you can perform actions on the rows, columns, or cells. A cell can hold a datum, or it can hold a formula. In Excel, the formula starts with an "=" sign, followed by the function. 

Almost everyone should learn to use a spreadsheet, even for home use. There are several very good free resources for learning Excel or other spreadsheets – You'll complete some of those in the Activities section below.  

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/point1.png?raw=true"><b>Activity: Work with Excel</b></p>

In this activity you'll learn more about working with Microsoft Excel.

<p><img style="margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/checkmark.png?raw=true"><b>Steps</b></p>

- If you are new to Excel, [open this reference and complete it](https://support.office.com/en-us/article/create-a-new-workbook-ae99f19b-cecb-4aa0-92c8-7126d6212a83?wt.mc_id=otc_excel), [then complete this section](https://support.office.com/en-us/article/overview-of-formulas-in-excel-ecfdc708-9162-49e8-b993-c311f47ca173?wt.mc_id=otc_excel), and then [bookmark this reference for more training](https://support.office.com/en-us/article/excel-for-windows-training-9bc05390-e94c-46af-a5b3-d7c22f6990bb). 
- If you already know how to use Excel, [open this reference on PivotTables and complete the exercises there](https://support.office.com/en-us/article/create-a-pivottable-to-analyze-worksheet-data-a9a84538-bfe9-40a9-a8e9-f99134456576?wt.mc_id=otc_excel).

<p style="border-bottom: 1px solid lightgrey;"></p>

<h3>2.1.2 SQL</h3>
After understanding spreadsheets, you should learn more about the *Structured Query Language*, or SQL. This language has statements to Create, Read, Update and Delete (*CRUD*) data in tabular sets called Relations, or Tables. A group of tables is stored in a database, and are similar to a group of Spreadsheets. 

SQL is the language that works on a *Relational Database Management System* (RDBS) that you'll learn about in a few moments. Many companies make these engines, and they all extend or modify the basic SQL language into a "dialect". The dialect for SQL Server is Transact-SQL or T-SQL, the dialect for Oracle is PL-SQL and so on.   

The most powerful part of the SQL structure is that of *Normalization* (based on relational calculus and set theory) which allows you to split up the data into single concepts and then tie those concepts back together in new ways using a "Key" value. [You can read more about that here](https://searchdatamanagement.techtarget.com/definition/relational-database). 

Another powerful concept is that of *Integrity*. The database engine ensures that the data entered and stored is structurally correct, the Normalization ensures that tables are consistent in the way they refer to each other, and you can set properties on the columns and/or values of data to ensure they store values you desire - such as ensuring numeric fields don't allow text data.

As you work through the tutorials that follow, you should be familiar with some basic terminology:

- **Database**: A single collection of all data, managed and stored in a consistent way.
- **Relation**: A tabular store of data with a given name. This looks like a single spreadsheet, and is often called a Table.
- **Tuple**: A single collection of information, also called a Row.
- **Attribute**: A single type of data, also called a Column.
- **Query**: Statements that create, update, or delete data, as well as display data from a Database. 

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/point1.png?raw=true"><b>Activity: Work with SQL</b></p>

In this exercise, you will work with the SQL language using an on-line system. You do not need to install anything to complete these exercises.

<p><img style="margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/checkmark.png?raw=true"><b>Steps</b></p>

- Open [this reference and complete all of the lessons there](https://www.w3schools.com/sql/sql_intro.asp) from *SQL Intro* through *SQL Comments*.

<p style="border-bottom: 1px solid lightgrey;"></p>

<h3>2.1.3 The R Platform</h3>

The R Platform is a base language for working with data that can be extended using more code called *packages*. These packages contain various functions you can use in R to perform tasks on data. R has packages available for almost any domain, and has many statistical packages for descriptive and predictive analytics, like those used in Machine Learning. 

R is a *functional* programming language, which means you apply expressions or functions instead of using statements as you do in object-oriented or other program paradigms. With R you progressively work on a data object from right to left, modifying it using various functions. You can also store the results of those operations as another object, which you can further use in the code. 

R also has a broad series of packages for data visualization. You create these visualizations using code, rather than a graphical interface. You will learn more about visualization with R in a moment.

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/point1.png?raw=true"><b>Activity: Work with Data and R</b></p>

In this exercise, you will work through an online course to learn R. You do not need to install anything to complete these exercises.

<p><img style="margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/checkmark.png?raw=true"><b>Steps</b></p>

- [Open this reference, and complete lessons](https://www.codecademy.com/learn/learn-r) 1-10.

<p style="border-bottom: 1px solid lightgrey;"></p>

<h3>2.1.4 Python</h3>

The Python language allows you to write code using object-oriented and other programming paradigms, has support for thousands of libraries, many of which deal with data and Machine Learning. It is fast-becoming of of the most popular programming language for Data Science applications.

Python is guided (unofficially) by the "PEP" - the Python Enhancement Proposal - that gives [the following guidelines for writing Python code](https://pep8.org/). Reviewing that document will give you common information on writing good Python Code.

> NOTE: While reporting and visualization tools also query data, we'll treat that as a separate skill in this Workshop.

Learning Languages like SQL, R and Python will help you understand your data better. As you work with a given language, you'll find out how to explore data structures in a way you may not think about when just considering the data itself. Using more than one tool broadens that understanding even further.

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/point1.png?raw=true"><b>Activity: Learn Python</b></p>

In this exercise, you will install Python and work with it on a development system. 

> NOTE: These steps require [Python](https://www.python.org/downloads/) and [MySQL](https://dev.mysql.com/downloads/installer/) to be installed locally on your system. It's best to use a development system or Virtual Machine for this installation. 

<p><img style="margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/checkmark.png?raw=true"><b>Steps</b></p>

- Open [this reference, and follow the lessons there](https://www.w3schools.com/python/python_intro.asp) from *Python Intro* through *Python Functions*. 
- Next, [open this reference, and follow the lessons there](https://www.w3schools.com/python/python_mysql_getstarted.asp) from *MySQL Get Started* through *MySQL Join*. 

<p style="border-bottom: 1px solid lightgrey;"></p>

<h2><img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/pencil2.png?raw=true">2.2 Tools For Storing and Processing Data</h2>

Data must be stored (persisted) in order for you and others to work with it. In fact, this was one of the first uses of computers after computation machines were invented - storing the results of those computation as tabular sets of data. You should be familiar with working with all of the following types of storage. You will then move on to systems (engines) that not only store data, but provide interfaces to allow multiple users to access, modify and remove data.

<h3>2.2.1 Text Files</h3>

While you are probably familiar with text files, you may not be aware of how they are used within the data profession. Computers don't actually store text, they store numbers - so several systems were created to represent a give letter in a language as a number. The most common is the [American Standard Code for Information Interchange](https://en.wikipedia.org/wiki/ASCII#References) (ASCII), which has been extended to allow for characters not found in English by an encoding known as [Unicode](https://en.wikipedia.org/wiki/Unicode). As you work with text files in your data analysis, you will need to know which encoding is being used, because each system you use requires its own open and closing functions, along with being able to read the text.

<h4>2.2.1.1 Text File Formats</h4>

Any ASCII document can be used as data. You might have a text document containing the names of customers and sales, like this:

<pre>
Bob Smith     Lawnmower  150.00
Jane T. Doe  Hammer 12.00
Sushma Yentil Savarri Tape  3
</pre>

While you can read that yourself, it would be harder for a program to figure out how to use that data in a structured way. Each line has separate spacing, number of letters in the name, and even how the numbers should lay out. The text file needs a layout in order to use it in a data system - even something as simple a spreadsheet.

<h5>Field Delimeters and Separators</h5>

To group a "field" together, you have a few choices. One is to enclose the characters you want to keep together with a *delimiter*. A common delimiter is a quotation mark:

<pre>
"Bob Smith"     "Lawnmower"  "150.00"
"Jane T. Doe"  "Hammer" "12.00"
"Sushma Yentil Savarri" "Tape"  "3"
</pre>

But this can still lead to data consistency issues, so a text file often has a separator. One of the most common is the *,* symbol, called a *Comma-Separated Values* (CSV) file:

<pre>
"Bob Smith","Lawnmower","150.00"
"Jane T. Doe","Hammer","12.00"
"Sushma Yentil Savarri","Tape","3"
</pre>

Other common delimeters are tabs (TSV), Colons, and Fixed-Width files: 

<pre>
"Bob Smith"  "Lawnmower"  "150.00"
"Jane T. Doe"  "Hammer"  "12.00"
"Sushma Yentil Savarri"  "Tape"  "3"
</pre>

In any case, when you are working with text files in most any language or data processing system, you will need to specify the file encoding, delimiters and separators, and sometimes the line-terminator (Unix or Windows).

<h5>XML</h5>
Trying to make a text file act as intelligent data storage presents other issues than just delimiters and separators. You might want to describe the "fields" or elements, and you may want to nest the structure in a different way. In addition, every row of data in the text file might not have the same descriptions, lengths, or even elements. 

The *Extensible Markup Language* (XML) is a markup specification for a text file that defines a set of rules for representing elements in a document.  It's a simple text file, with *Tags* that enclose *Elements*. As long as you open **<>** and close **</>** a Tag, you can use any tag name, and any elements inside it that you want. 

> Technically, you need the line below to dictate to the file reader that this is a well-formed XML document, and it's common to name XML files with an .xml extension.

\<?xml version="1.0" encoding="UTF-8"?>

Although you aren't required to have a consistent "header" structure in an XML file, our example would look like this in XML:

    <salesinfo>
        <name>Bob Smith</name>  
        <item>Lawnmower</item>  
        <price>150.00</price>

        <name>Jane T. Doe</name>  
        <item>Hammer</item>  
        <price>12.00</price>

        <name>Sushma Yentil Savarri</name>  
        <item>Tape</item>  
        <price>3</price>
    </salesinfo>

Note that the spaces and arrangement of the layout of the file are immaterial. This is the same information and will process correctly: 

    <salesinfo>  <name>Bob Smith</name> <item>Lawnmower</item>  <price>150.00</price>
    <name>Jane T. Doe</name>  <item>Hammer</item>  <price>12.00</price>
    <name>Sushma Yentil Savarri</name>  <item>Tape</item>  <price>3</price> </salesinfo>

You [learn much more about XML here](https://www.w3schools.com/xml/default.asp).

<h5>Key-Value Pairs</h5>

A Key-Value pair data set takes the form of a reference to an element (like "name") and then a value that follows - no closing tag is needed. For instance: 

    {name : "Buck Woody"}

While the XML specification has some limitations for representing complex data sets, a new standard called *JavaScript Object Notation* (JSON) is quite common in programming. One of the primary features is the ability to declare an array within an element. Here's an [example JSON file from Wikipedia](https://en.wikipedia.org/wiki/JSON): 

    {
    "firstName": "John",
    "lastName": "Smith",
    "isAlive": true,
    "age": 27,
    "address": {
        "streetAddress": "21 2nd Street",
        "city": "New York",
        "state": "NY",
        "postalCode": "10021-3100"
    },
    "phoneNumbers": [
        {
        "type": "home",
        "number": "212 555-1234"
        },
        {
        "type": "office",
        "number": "646 555-4567"
        },
        {
        "type": "mobile",
        "number": "123 456-7890"
        }
    ],
    "children": [],
    "spouse": null
    }

Modern programming languages use JSON for many functions, including setting values and storing data. You can [learn more about working with JSON here](https://www.w3schools.com/js/js_json_intro.asp). 

<h3>2.2.2 Relational Database Management Systems (RDBMS)</h3>

While storing data in text is quite common (even more so in large-scale data systems like [Hadoop](https://docs.microsoft.com/en-us/azure/hdinsight/hadoop/apache-hadoop-introduction) or [Spark](https://docs.microsoft.com/en-us/azure/hdinsight/spark/apache-spark-overview) and others), it is not as space-efficient or speed efficient as working with Binary file formats. Another very important feature is that Binary files can be "locked" in a granular way to allow many users to work with the same data at one time. However, a Binary file is designed to work with software specifically designed to access it - a *Database Engine*. This is software that runs on a central computer (or set of computers) called a server as a service - it's always running, waiting for calls from client software. It then controls the access to the data in the Binary file very efficiently. 

There are generally two classifications of Database Engines: *Relational Database Management Systems* and *NoSQL* Platforms. 

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/point1.png?raw=true"><b>Activity: Understand Database Engines</b></p>

In this exercise, you will watch an instructional video on the SQL Server database engine. You do not need to install anything to complete these exercises.

<p><img style="margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/checkmark.png?raw=true"><b>Steps</b></p>

- Open [this reference and watch this 9-minute introduction](https://www.youtube.com/watch?v=bXbm0qGwgAw) to Database Engines

<p style="border-bottom: 1px solid lightgrey;"></p>

<h3>2.2.3 NoSQL and Big Data Engines</h3>

An RDBMS provides very tightly controlled data integrity and a high level of security and speed over "structured" 

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/point1.png?raw=true"><b>Activity: TODO: Activity Name</b></p>

TODO: Activity Description and tasks

<p><img style="margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/checkmark.png?raw=true"><b>Steps</b></p>

https://www.youtube.com/watch?v=uD3p_rZPBUQ

<p style="border-bottom: 1px solid lightgrey;"></p>

<h2><img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/pencil2.png?raw=true">2.3 Tools For Data Reporting</h2>

Reporting is [less about tools than about understanding how to visualize data](https://flourish.studio/2018/09/28/choosing-the-right-visualisation/), and do it correctly. Displaying the graphics of data can completely change how you understand it – after you understand basic statistics, take a look at this [article on Anscombe’s Quartet](https://eagereyes.org/criticism/anscombes-quartet) to see a startling example.

<h3>2.3.1 Visualizing Data in Excel</h3>

https://www.excel-easy.com/data-analysis/charts.html



<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/point1.png?raw=true"><b>Activity: TODO: Activity Name</b></p>

TODO: Activity Description and tasks

<p><img style="margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/checkmark.png?raw=true"><b>Steps</b></p>

TODO: Enter activity steps description with checkbox

<p style="border-bottom: 1px solid lightgrey;"></p>

<h3>2.3.2 Visualizing Data using Programming</h3>

https://www.analyticsvidhya.com/blog/2015/07/guide-data-visualization-r/

<img src="https://upload.wikimedia.org/wikipedia/en/0/0a/Gallery_of_Plotly_Graphs.png">
<br>
<a href="https://en.wikipedia.org/wiki/Plotly"><i>Plot gallery using the Plotly library in R - Source: Wikimedia</i></a>

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/point1.png?raw=true"><b>Activity: TODO: Activity Name</b></p>

TODO: Activity Description and tasks

<p><img style="margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/checkmark.png?raw=true"><b>Steps</b></p>

TODO: Enter activity steps description with checkbox

<p style="border-bottom: 1px solid lightgrey;"></p>


https://gilberttanner.com/blog/introduction-to-data-visualization-inpython

<img width="400" src="https://seaborn.pydata.org/_images/structured_heatmap.png">
<br>
<a href="https://seaborn.pydata.org/"><i>Plot gallery using the Seaborn library in Python - Source: Seaborn Project</i></a>

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/point1.png?raw=true"><b>Activity: TODO: Activity Name</b></p>

TODO: Activity Description and tasks

<p><img style="margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/checkmark.png?raw=true"><b>Steps</b></p>

TODO: Enter activity steps description with checkbox

<p style="border-bottom: 1px solid lightgrey;"></p>

<h3>2.3.3 Visualizing Data using Power BI and other Graphing Systems</h3>

https://powerbi.microsoft.com/en-us/learning/

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/point1.png?raw=true"><b>Activity: TODO: Activity Name</b></p>

TODO: Activity Description and tasks

<p><img style="margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/checkmark.png?raw=true"><b>Steps</b></p>

TODO: Enter activity steps description with checkbox

<p style="border-bottom: 1px solid lightgrey;"></p> 

Remember, *the tool you use to convey information is less important than learning to present data graphically*.

<p style="border-bottom: 1px solid lightgrey;"></p>

<p><img style="margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/owl.png?raw=true"><b>For Further Study</b></p>
<ul>
    <li>One of the few non-free resources in this series for learning: Wayne Winston’s excellent book called <a href="https://www.amazon.com/Microsoft-Analysis-Business-Modeling-Skills/dp/1509305882/ref=sr_1_1?crid=3T9RV585FOIOY&keywords=business+analysis+with+excel&qid=1578403817&sprefix=business+analysis+with+exce%2Caps%2C336&sr=8-1" target="_blank">Microsoft Excel 2019 Data Analysis and Business Modeling. There are earlier editions if you are not using 2019 as well.</a></li>
    <li>Another non-free (but very good) resource is <a href="https://www.amazon.com/Seven-Databases-Weeks-Modern-Movement/dp/1680502530/ref=sr_1_2?crid=1HQU1Z9H2Q7M0&keywords=7+databases+in+7+weeks&qid=1578404488&sprefix=7+databases%2Caps%2C189&sr=8-2" target="_blank">Seven Databases in Seven Weeks. This text will have you work with several platforms, and broaden your perspectives on database engines.</a></i>    
</ul>

<p style="border-bottom: 1px solid lightgrey;"></p>

<p><img style="margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/owl.png?raw=true"><b>Next Steps</b></p>

<a href=" " target="_blank">Now move on to the next topic: 3 - Analyzing Data In Context</a>