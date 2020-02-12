<img width="150" style="float: right; margin: 0px 15px 15px 0px;" src="https://github.com/BuckWoody/presentations/blob/master/graphics/BWLogo002.png?raw=true"> 

# Workshop: Data Literacy

#### <i>Using Data To Make Intelligent Decisions</i>

<img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/textbubble.png?raw=true"> <h2>1 - Find Authoritative Data</h2>

In this workshop you'll cover using data to make intelligent decisions. In each module you'll get more references, which you should follow up on to learn more. Also watch for links within the text - click on each one to explore that topic.

(<a href="https://github.com/BuckWoody/presentations/blob/master/dataliteracy/dataliteracy/00-pre-requisites.md" target="_blank">Make sure you check out the <b>Pre-Requisites</b> page before you start</a>. You'll need to complete the work there before you can proceed with the workshop.)

<p style="border-bottom: 1px solid lightgrey;"></p>

Learning Data Literacy skills is similar to the way you learned the skills you have in literacy with your language.

To read and write, you learned the basic building blocks of your language – *the letters of the alphabet*. These form the atomic units of literacy. With Data Literacy, you’ll learn about *Data* as the atomic unit.

Next you learned to work with various tools, such as *paper and pencil*, to write those letters. This is similar to the tools you’ll use for writing and reading data such as *programming or other interfaces*.

From there you learned the rules of *grammar*. This is similar to learning how one data element affects another, using *context and relationships*.

And finally you were introduced to longer and more complex works of writing, and you derived *meaning from your reading*. This is similar to how you will *interpret data to make intelligent decisions*.

In this Module you'll learn more about finding and using authoritative data. Before you do that, we need to define what data is.

<h2><img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/pencil2.png?raw=true">1.1 Defining Data</h2>

Let’s start at the beginning: What is Data? [Webster’s defines data as “factual information (such as measurements or statistics) used as a basis for reasoning, discussion, or calculation”](https://www.merriam-webster.com/dictionary/data). Essentially, data is one or more facts.

So *Facts* make *Data*, data makes *Information*, recalling that information makes *Knowledge*, and correctly applied knowledge makes *Wisdom* – and the whole point of Data Literacy is helping you making *wise decisions*.

<p style="border-bottom: 1px solid lightgrey;"></p>

<h2><img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/pencil2.png?raw=true">1.2 General Data Types</h2>

There are two general types of data you will work with: *Quantitative* and *Qualitative* (sometimes called *Categorical*) data. [A longer explanation of these types is here](http://www.differencebetween.net/science/difference-between-qualitative-and-quantitative-observation/), but in general, quantitative data is *numeric*, and qualitative data describes an *attribute*.

Therefore:

**1** apple, **25** votes, **15** cars = **Quantitative** Data

**Red** apple, **University-age** voters, **Blue** cars = **Qualitative** Data

You’ll use formulas, aggregations and more on quantitative data, and you’ll describe those sets of data using qualitative data.

You can also analyze qualitative data, or use it to get numbers – for instance, you can see the names of students in a class (qualitative), and then count the names (quantitative). This distinction is important because you want to ensure you perform the proper analysis on the appropriate type of data.

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/point1.png?raw=true"><b>Activity: Setting Up Quantitative and Qualitative Data</b></p>

In this exercise you will work through a mental exercise of breaking down one type of data to another.


<p><img style="margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/checkmark.png?raw=true"><b>Steps</b></p>

You need to analyze the number of customers who have clicked on a web page for a particular clothing article, but the colors are marked as "red", "light red", "auburn" and other subjective terms. What are some of the ways you could standardize the data for more in-depth numerical analysis?

<p style="border-bottom: 1px solid lightgrey;"></p>

<h2><img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/pencil2.png?raw=true">1.3 Source Identification</h2>

The next skill to learn is how to *find* the data you need. [Start with a basic understanding of how to do research](https://www.skillsyouneed.com/learn/research-methods.html). Create your own log of the data sources you use. Take your time on this step, it is pivotal to the rest of your work with data.

To find sources of data you didn’t collect yourself, [a quick web search will open up a lot of data sources](https://infogram.com/blog/free-data-sources/), but make sure you [understand the difference between Primary and Secondary data sources](http://www.businessdictionary.com/definition/primary-data.html) as you use them.

Don’t rely on one search result, or even one search engine. Check out the [advanced search features on Google](https://support.google.com/websearch/answer/134479?hl=en), [Bing](https://fossbytes.com/advanced-bing-search-tips-and-tricks/), [Yahoo](https://search.yahoo.com/web/advanced), [StartPage](https://www.startpage.com/en/?&hmb=1), [Yandex](https://yandex.com/), [Ask.com](https://www.ask.com/), [DuckDuckGo](https://duckduckgo.com/), [WolframAlpha](https://www.wolframalpha.com/) and more. And even though the web contains lots of data, it doesn’t have everything. [Visit your local library](https://publiclibraries.com/) and know how to [leverage the Research section](https://libraryguides.binghamton.edu/libraryresearch) - use the [libraries at colleges and schools](http://www.top10onlineuniversities.org/50-incredible-free-university-libraries-online.html) as well.

If you find a discrepancy between a data set, find out why. [And always document your sources](https://docs.microsoft.com/en-us/azure/data-catalog/data-catalog-how-to-documentation), even the ones you don't use immediately.

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/point1.png?raw=true"><b>Activity: Locate data about a topic</b></p>

In this exercise you will locate data that may not be in your field of expertise. You will ensure you have enough data to check against multiple verifications.

<p><img style="margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/checkmark.png?raw=true"><b>Steps</b></p>

- Locate the unit sales of lipstick in the U.S. for this year, and compare it to the unit sales in 1947.
- Were you able to locate data for each of these requests? 
- How many sources did you use? Did they agree? If not, what do you think could account for the discrepancy, and how would you report that in your analysis?

<p style="border-bottom: 1px solid lightgrey;"></p>

<h2><img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/pencil2.png?raw=true">1.4 Data Verification</h2>

After you know where to find data, you need to insure that it is valid – [accurate](https://www.whydoscientists.org/accuracy-precision-errors-statistics/), [representative](https://www.investopedia.com/terms/r/representative-sample.asp), and [sufficient](https://www.statisticshowto.datasciencecentral.com/sufficient-statistic/).

*Accurate* data aligns closest to the actual reality of the observation or event.

*Representative* data means that the observation and collection method took into account the most possibilities were covered.

*Sufficient* data means that the data point (such as a sum or average) has enough support to represent what it purports to.

There are three basic questions you should ask when you find information:

- Who is telling me this
- What are they telling me about this
- Why are they telling me this

Asking these simple questions can uncover a lot of issues with a data source. If you listen to a salesperson about a buying a car, you’ll find their data heavily supports the decision to buy the car. Knowing that it’s a salesperson giving you the data, knowing that they make their living off of selling you a car, and knowing they want you to buy the most expensive car will help you properly evaluate the data you have.

It’s actually the same for most any data – not just qualitative data but quantitative as well. There is no single source of “fair and balanced” information – you’ll have to drive all the way back to the source to find out the truth, or at least the closest approximation to the truth that you can.

In short, it’s best to be a [data skeptic](https://www.oreilly.com/ideas/on-being-a-data-skeptic).

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/point1.png?raw=true"><b>Activity: Exceptional claims require exceptional sources</b></p>

Data Verification means that you have done due-diligence and documented your research from reliable sources. But in some cases, the data shows "red flags". This is called "Exceptional claims require exceptional sources". In this exercise you will identify those "red flags".

<p><img style="margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/checkmark.png?raw=true"><b>Steps</b></p>

- Name three "red flags" that would cause you to doubt a given dataset.
- What are some of the ways you can deal with this type of data?

<p style="border-bottom: 1px solid lightgrey;"></p>

<p><img style="margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/owl.png?raw=true"><b>For Further Study</b></p>
<ul>
    <li><a href="https://www.usgs.gov/products/data-and-tools/data-management/data-dictionaries" target="_blank">Government guide to data dictionary</a></li>
</ul>

<p style="border-bottom: 1px solid lightgrey;"></p>

<p><img style="margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/owl.png?raw=true"><b>Next Steps</b></p>

<a href="https://github.com/BuckWoody/presentations/blob/master/dataliteracy/dataliteracy/02-work_with_data_tools.md" target="_blank">Now move on to the next topic: 2 - Work With Data Using Various Tools</a>
