# Workshop: Shut The Front Door

#### <i>A Security Course from Buck Woody and David Seis</i>

<p style="border-bottom: 1px solid lightgrey;"></p>

<img style="float: left; margin: 0px 15px 15px 0px;" src="../graphics/textbubble.png"> <h2>Module 03: Security Processes and Procedures</h2>

In this module you'll cover various security processes and procedures you can use to secure your organization's environment. 

In each module you'll get more references, which you should follow up on to learn more. Also watch for links within the text - click on each one to explore that topic.

You'll cover these topics in the workshop:
<dl>
  <dt><a href="#ZeroTrust" target="_blank">3.1 - Zero Trust</a></dt>
  <dt><a href="#SelfAudit" target="_blank">3.2 - Self-Auditing</a></dt>
  <dt><a href="#Maintenance" target="_blank">3.3 - Security Maintenance</a></dt>
</dl>

<p style="border-bottom: 1px solid lightgrey;"></p>
<br>

<h2 id="ZeroTrust"><img style="float: left; margin: 0px 15px 15px 0px;" src="../graphics/pencil2.png">3.1 Zero Trust Mindset</h2>
<p>Zero trust is a security paradigm where a user or business shouldn't have any implicit trust relationships. Multiple forms of verification must be used for authentication of a user, a site, an email, a download, and other assets. This methodology can help ensure that each asset is properly secured, and each attempt by a security principal is verified.</p> 

<br>
<p><img style="float: left; margin: 0px 15px 15px 0px;" src="../graphics/point1.png"><b>Activity: Where is there trust in your computing?</b></p>
<p>Consider where you implicitly trust certain programs, vendors, technology, etc. in your environment and consider what steps could be done to help prevent vulnerability.</p>

<br>
<p><img style="float: left; margin: 0px 15px 15px 0px;" src="../graphics/checkmark.png"><b>Description</b></p>

In this activity you will evaluate the Hardware and Software trust areas on the user's system.

<br>
<p><img style="float: left; margin: 0px 15px 15px 0px;" src="../graphics/checkmark.png"><b>Steps</b></p>

Create a section in your system notes for each system you evaluate. Using the following steps, update the environment notes for each system. While this process can take a significant amount of time, it can form a baseline that allows the process to move quicker in subsequent reviews. 

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="../graphics/checkbox.png">  Any programs that exist on your computer have certain access and permissions. Identify any programs you do not use, consider which programs to keep and look into their settings for privacy and what information is stored. The same is true for websites.</p>
<p><img style="float: left; margin: 0px 15px 15px 0px;" src="../graphics/checkbox.png">  All hardware peripherals have some access to the information in your computer. Some are notorious for being untrustworthy (<a href="https://www.kaspersky.com/resource-center/threats/webcam-hacking">webcams</a>), and others have been the vector malicious actors use to gain leverage into networks (<a href="https://www.forbes.com/sites/leemathews/2020/08/31/800000-printers-vulnerable-28000-hacked/?sh=f9534d2d8a9f">printers</a>, <a href="https://www.entrepreneur.com/article/368943">fish thermometers</a>, <a href="https://www.iotforall.com/5-worst-iot-hacking-vulnerabilities">etc.</a>). You can <a href="https://www.bing.com/search?q=securing+iot+devices+at+home&form=QBLH&sp=-1&pq=securing+iot+devices+at+home&sc=1-28&qs=n&sk=&cvid=C33FB918074141EEBA10D5C354792C36">find resources here</a> for securing your IoT devices.</p>

<br>
<p style="border-bottom: 1px solid lightgrey;"></p>

<br>
<h2 id="SelfAudit"><img style="float: left; margin: 0px 15px 15px 0px;" src="../graphics/pencil2.png">3.2 Self-Auditing</h2>

Secure behaviors are as important as having a secure device. Users are the first line of defense and secure environments, so giving them concrete steps they can follow is essential to ensuring a secure environment. Along with the information you learned in [Module 01](https://github.com/BuckWoody/presentations/blob/master/shut_the_front_door/shut_the_front_door/Module01.md), the following activities can assist you in creating a sense of personal responsibility for security in your organization.

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="../graphics/point1.png"><b>Activity: Cyber Hygiene Audit</b></p>

In this Activity you will review an Audit checklist with each user to identify important practices and behaviors for secure computing. Ideally you would print or display this list to the user to keep these steps top-of-mind. 

<br>
<p><img style="float: left; margin: 0px 15px 15px 0px;" src="../graphics/checkmark.png"><b>Description</b></p>

In this step you will provide each user a Security Audit Checklist they can use to evaluate their systems.

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="../graphics/checkmark.png"><b>Steps</b></p>
<p><img style="float: left; margin: 0px 15px 15px 0px;" src="../graphics/checkbox.png">  Do you have a unique credentials for all online accounts? </p>
<p><img style="float: left; margin: 0px 15px 15px 0px;" src="../graphics/checkbox.png">  How often do you change your passwords? (<a href="https://www.vericlouds.com/nist-password-guidelines-2021-challenging-traditional-password-management/#:~:text=NIST%202021%20Best%20Practices%201%20Minimum%20Password%20Length.,NIST%20guidelines.%203%20Use%20A%20Password%20Manager.%20">NIST recommends having no change requirements?)</p>
<p><img style="float: left; margin: 0px 15px 15px 0px;" src="../graphics/checkbox.png">  Are your passwords <a href="https://security.harvard.edu/use-strong-passwords">strong?</a></p>
<p><img style="float: left; margin: 0px 15px 15px 0px;" src="../graphics/checkbox.png">  Do you have a backup of your data?</p>
<p><img style="float: left; margin: 0px 15px 15px 0px;" src="../graphics/checkbox.png">  Do you allow auto-filling of web forms? (<a href="https://www.techadvisory.org/2019/01/the-dangers-of-autocomplete-passwords/">Why is this dangerous?</a>) </p>
<p><img style="float: left; margin: 0px 15px 15px 0px;" src="../graphics/checkbox.png">  Do you allow multiple users onto the admin account or do multiple users have admin privileges?</p>
<p><img style="float: left; margin: 0px 15px 15px 0px;" src="../graphics/checkbox.png">  Are you familiar with the methods scammers, fraudsters, and phishers will use to trick you? (<a href="https://www.consumer.ftc.gov/articles/how-recognize-and-avoid-phishing-scams">email, phone, text</a>, <a href="https://www.usa.gov/online-safety#item-37227">websites</a>, <a href="https://www.consumer.ftc.gov/blog/2020/10/scams-start-social-media">"friends" on social media</a>, <a href="https://www.consumer.ftc.gov/features/scam-alerts">grants, work, prizes or gifts</a>, <a href="https://www.idtheftcenter.org/dont-fall-for-a-boss-gift-card-scam/#:~:text=The%20boss%20gift%20card%20scam%20is%20so%20simple,stranger%E2%80%99s%20phone%20or%20computer%20since%20theirs%20is%20locked.">bosses requesting gift cards.</a> </p>
<p><img style="float: left; margin: 0px 15px 15px 0px;" src="../graphics/checkbox.png">  Do you have Multi-factor authentication enabled on your most sensitive accounts? (Authenticator apps from <a href="https://play.google.com/store/apps/details?id=com.azure.authenticator&hl=en_US&gl=US">Microsoft</a> and <a href="https://play.google.com/store/apps/details?id=com.google.android.apps.authenticator2&hl=en_US&gl=US">Google</a>)
<p><img style="float: left; margin: 0px 15px 15px 0px;" src="../graphics/checkbox.png">  Are you dilligent and aware enough to notice the many phony <a href="https://nordvpn.com/blog/fake-apps/">apps</a>, <a href="https://www.asecurelife.com/how-to-spot-a-fake-website/">websites</a>, and <a href="https://www.cisecurity.org/daily-tip/know-how-to-spot-fake-software/">programs</a> out there that try to get information by emulating what you were looking for?
<p><img style="float: left; margin: 0px 15px 15px 0px;" src="../graphics/checkbox.png">  Are the systems you are using past their <a href="https://www.abcservices.com/the-risks-of-end-of-life-technology/">end-of-life</a>?
<p><img style="float: left; margin: 0px 15px 15px 0px;" src="../graphics/checkbox.png">  Do you keep your systems updated and patched?</p>

<br>
<p style="border-bottom: 1px solid lightgrey;"></p>

<br>
<h2 id="Maintenance"><img style="float: left; margin: 0px 15px 15px 0px;" src="../graphics/pencil2.png">3.3 Security Maintenance</h2>

Maintenance of each system is essential for security, and should be automated as much as possible, with constant reporting and reporting reviews. In the following Activities you will review various maintenance plans and create one that works well for your environment. This will keep each system running well, and also provide a vanguard for a continious security posture.

Wherever possible, you should create and implement automation tools. These can be a series of scripts you create in PowerShell all the way to a 3rd party automation tool.

<br>
<p><img style="float: left; margin: 0px 15px 15px 0px;" src="../graphics/point1.png"><b>Activity: Develop a Computer Maintenance plan</b></p>

Regular maintenance of your devices will help ensure you are protected from many vulnerabilites from cyber threats. You should create a plan that ensures you are performing such tasks as updates, log reviews, backups and other maintenance tasks for all users. 

> NOTE: Your organization may have a comprehensive plan for maintenance of all systems on the network, so it's essential you work with all groups in IT to ensure a cohesive, connected, and comprehensive plan for maintenance of all computing and networking devices.

<br>
<p><img style="float: left; margin: 0px 15px 15px 0px;" src="../graphics/checkmark.png"><b>Description</b></p>

In this Activity you will review several resources to create your own maintenance plan.

<br>
<p><img style="float: left; margin: 0px 15px 15px 0px;" src="../graphics/checkmark.png"><b>Steps</b></p>
<p><img style="float: left; margin: 0px 15px 15px 0px;" src="../graphics/checkbox.png">  <a href="https://us.norton.com/internetsecurity-how-to-computer-maintenance.html">Norton has a general list of maintenance steps</a>, <a href="https://www.hp.com/us-en/shop/tech-takes/10-essential-computer-maintenance-tips">as does HP</a>, to get you started thinking about both the hard and soft maintenance of your computer. Review these links to develop a plan in your course notes. If you already have a plan in place, this is a good opportunity to review it for completeness and accuracy.</p>

<br>
<p><img style="margin: 0px 15px 15px 0px;" src="../graphics/owl.png"><b>For Further Study</b></p>
<ul>
    <li><a href="https://csrc.nist.gov/" target="_blank">NIST: Computer Security Resource Center.</a></li>
    <li><a href="https://docs.microsoft.com/en-us/security/" target="_blank">Microsoft Security Docmentation.</a></li>
    <li><a href="https://www.cisecurity.org/resources/" target="_blank">Center for Internet Security Resources.</a></li>
    <li><a href="https://www.fbi.gov/investigate/cyber" target="_blank">FBI Cyber Threats</a></li>
    <li><a href="https://www.dsac.gov/topics/cyber-resources" target="_blank">DSAC- Cyber resources.</a></li>
</ul>

Next, Continue to <a href="https://github.com/BuckWoody/presentations/blob/master/shut_the_front_door/shut_the_front_door/SecurityAuditChecklist-Edge.md" target="_blank"><i> Security Audit Checklist</i></a>.
