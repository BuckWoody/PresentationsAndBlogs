# Workshop: Shut The Front Door

#### *A Security Course from [Buck Woody](https://aka.ms/buckwoody) and [David Seis](https://www.linkedin.com/in/davidseis/)*

<p style="border-bottom: 1px solid lightgrey;"></p>

<img style="float: left; margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/textbubble.png"> <h2>About this Workshop</h2>

Welcome to this workshop on "Shut the front door", which covers tools and processes used to bolster personal computer security for the layman and expert alike. In this workshop, you'll learn the most common threats to personal computer security and the tools and processes that can be used to mitigate these threats. The focus of this workshop is to educate technical professionals on what every person should know and do to keep themselves andothers safe in the cyber environment. You'll also get a starting checklist you can use to audit and check a computing asset. 

You'll start by understanding the most common and easily preventable vectors for computing security, moving on to the tools you can use to inventory and detect malware, and then how to educate users for better security, with a focus on how to extrapolate what you have learned to create other solutions for your organization.

This [github README.MD file](https://github.com/BuckWoody/presentations/blob/master/shut_the_front_door/README.md) explains how the workshop is laid out, what you will learn, and the technologies you will use in this solution. To download this Lab to your local computer, click the **Clone or Download** button you see at the top right side of this page. [More about that process is here](https://help.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository). 

You can view other courses and  workshops Buck and his team has created at this link - open in a new tab to find out more.](https://github.com/BuckWoody/presentations).

<p style="border-bottom: 1px solid lightgrey;"></p>

<img style="float: left; margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/checkmark.png"> <h3>Learning Objectives</h3>

In this workshop you'll learn:
<br>

- How to identify the primary causes of security breaches (user error, vulnerable systems, and loss of credentials)
- The "tools of the trade" to identify the primary issues (MS Security Center, MS Map Tool, and a brief overview of other options)
- Processes that you can follow to help secure systems at work and home (Strong passwords, replacing defaults, computer hygiene and habits to avoid phishing and malware downloading)

The goal of this workshop is to train technical professionals to secure their organization's computing assets from the most common security threats and issues. The technical professional can then use this information to form their own materials to assist end-users. 

The concepts and skills taught in this workshop form the starting points for:

- Technical Professionals tasked with administration of a computing network
- Technical Professionals tasked with securing computing assets
- End-Users with a degree of technical skill that want to assist others in securing computing assets


<p style="border-bottom: 1px solid lightgrey;"></p>
<img style="float: left; margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/building1.png"> <h2>Business Applications of this Workshop</h2>

Businesses require secure systems at the edge of their networks, and the front-lines of this area is the end-user. However, many end-users are so busy with their daily work that they do not take the proper steps to behave in a secure fashion with computing assets. This course provides the technical professionals tasked with securing the organization from viri, malware, and ransomware to brief the users on proper security behaviors and also gives them a checklist and a set of tools to check each system to maintain that posture. 


<p style="border-bottom: 1px solid lightgrey;"></p>

<img style="float: left; margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/listcheck.png"> <h2>Technologies used in this Workshop</h2>

The solution includes the following technologies - although you are not limited to these, they form the basis of the workshop. At the end of the workshop you will learn how to extrapolate these components into other solutions. You will cover these at an overview level, with references to much deeper training provided.

 <table style="tr:nth-child(even) {background-color: #f2f2f2;}; text-align: left; display: table; border-collapse: collapse; border-spacing: 2px; border-color: gray;">

  <tr><th style="background-color: #1b20a1; color: white;">Technology</th> <th style="background-color: #1b20a1; color: white;">Description</th></tr>

  <tr><td><i>Microsoft Windows</i></td><td> While the behaviors and general processes for security apply to all operating systems, the focus of this course is on the Microsoft Windows operating system. </td></tr>

</table>

<p style="border-bottom: 1px solid lightgrey;"></p>

<img style="float: left; margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/owl.png"> <h2>Before Taking this Workshop</h2>

You'll need a local system that you are able to install software on. The workshop demonstrations use Microsoft Windows as an operating system and all examples use Windows for the workshop. Optionally, you can use a Microsoft Azure Virtual Machine (VM) to install the software on and work with the solution.

This workshop expects that you understand basic computing concepts, and how to install and configure Microsoft Windows on a computing device. 

If you are new to these, here are a few references you can complete prior to class:

-  [Windows 10 Free e-book](https://www.filecritic.com/windows10-free-ebook-filecritic.pdf)
-  [Windows 10 Security](https://www.microsoft.com/en-us/windows/comprehensive-security)

<img style="float: left; margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/bulletlist.png"> <h3>Setup</h3>

You will only need a web browser and a note-taking software or paper/pen. You can perform the steps you see in the software area on your local system, but be aware that this does install software on your system. You can perform all audit actions (with no changes) without affecting your system. 

> NOTE: All systems should be backed up prior to making any changes; this ensures the system can be restored to the current state. If there is no backup available, take one now, otherwise you can simply listen during the class and make no changes to the computer. No changes should be made if there is not a current backup. 

<p style="border-bottom: 1px solid lightgrey;"></p>

<img style="float: left; margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/bookpencil.png"> <h2>Workshop Modules</h2>

This is a modular workshop, and in each section, you'll learn concepts, technologies and processes to help you complete the solution.

<table style="tr:nth-child(even) {background-color: #f2f2f2;}; text-align: left; display: table; border-collapse: collapse; border-spacing: 5px; border-color: gray;">

<tr><td style="background-color: AliceBlue; color: black;"><b>Module</b></td><td style="background-color: AliceBlue; color: black;"><b>Topics</b></td></tr>

<tr><td><a href="https://github.com/BuckWoody/presentations/blob/master/shut_the_front_door/shut_the_front_door/Module01.md" target="_blank"> 01 - Common Security Breaches </a></td><td> This module covers the most common security breach avenues, and how criminals use them to infiltrate your systems.</td></tr>

<tr><td style="background-color: AliceBlue; color: black;"><a href="https://github.com/BuckWoody/presentations/blob/master/shut_the_front_door/shut_the_front_door/Module02.md" target="_blank"> 02 - Basic Security Tools</a> </td><td td style="background-color: AliceBlue; color: black;"> In this Module you'll learn free and commerical tools you can use to investigate, mitigate and prevent the most common security violations. </td></tr>

<tr><td><a href="https://github.com/BuckWoody/presentations/blob/master/shut_the_front_door/shut_the_front_door/Module03.md" target="_blank"> 03 - Security Processes and Procedures </a></td><td> In this module you'll learn how to create a "security mindset" that will use the knowledge about security risks and the tools you can use to prevent the most common security breaches.</td></tr>

<tr><td style="background-color: AliceBlue; color: black;"><a href="https://github.com/BuckWoody/presentations/blob/master/shut_the_front_door/shut_the_front_door/SecurityAuditChecklist-Edge.md" target="_blank"> Security Audit Checklist</a> </td><td td style="background-color: AliceBlue; color: black;"> Use this Checklist as a starting point for your Security Audits. </td></tr>

</table>

<p style="border-bottom: 1px solid lightgrey;"></p>

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/geopin.png"><b>Next Steps</b></p>

Next, Continue to <a href="https://github.com/BuckWoody/presentations/blob/master/shut_the_front_door/shut_the_front_door/00%20-%20Pre-Requisites.md" target="_blank"><i> Pre-Requisites</i></a>

# Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us the rights to use your contribution. For details, visit https://cla.opensource.microsoft.com. Changes are submitted via comments, multiple-committers are not allowed. 

When you submit a pull request, a CLA bot will automatically determine whether you need to provide a CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the instructions provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

# Legal Notices

### License
Buck Woody and David Seis and any other contributors grant you a license to the documentation and other content in this repository under the [Creative Commons Attribution 4.0 International Public License](https://creativecommons.org/licenses/by/4.0/legalcode), see [the LICENSE file](https://github.com/MicrosoftDocs/mslearn-tailspin-spacegame-web/blob/master/LICENSE), and grant you a license to any code in the repository under [the MIT License](https://opensource.org/licenses/MIT), see the [LICENSE-CODE file](https://github.com/MicrosoftDocs/mslearn-tailspin-spacegame-web/blob/master/LICENSE-CODE).

Microsoft, Windows, Microsoft Azure and/or other Microsoft and Non-Microsoft products and services referenced in the documentation may be either trademarks or registered trademarks of Microsoft in the United States and/or other countries.

The licenses for this project do not grant you rights to use any Microsoft or other company names, logos, or other trademarks.
Microsoft's general trademark guidelines can be found at http://go.microsoft.com/fwlink/?LinkID=254653.

Privacy information can be found at https://privacy.microsoft.com/en-us/

Microsoft and any contributors reserve all other rights, whether under their respective copyrights, patents,
or trademarks, whether by implication, estoppel or otherwise.
