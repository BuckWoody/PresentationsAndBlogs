# Security Audit Checklist

#### <i>From the Security Course <a href="https://github.com/BuckWoody/presentations/tree/master/shut_the_front_door">"Shut the Front Door"</a> by Buck Woody and David Seis</i>

<p style="border-bottom: 1px solid lightgrey;"></p>

<img style="float: left; margin: 0px 15px 15px 0px;" src="../graphics/textbubble.png"> <h2>Edge Security Audit Checklist</h2>

A Security Audit is an important tool to ensure each area of your system is secure. This checklist covers the "Edge" systems and users - those that are the end-users of your network. This audit should be performed on each system and for each user of your system. 
>Ensure the user has a complete backup of their data before making any changes.
Here are a few basic areas you should cover in a Security Audit:
<dl>

  <dt><a href="#UserBriefing" target="_blank">01 - User Briefing<dt>
  <dt><a href="#AssetInventory" target="_blank">02 - Hardware and Software Asset Inventory<dt>
  <dt><a href="#Updates" target="_blank">03 - Patches and Updates<dt>
  <dt><a href="#Scans" target="_blank">04 - Virus and Malware Scans<dt>
  <dt><a href="#Ports" target="_blank">05 - Firewalls and Ports<dt>
  <dt><a href="#Web" target="_blank">06 - Browser, E-Mail and Internet-Facing Assets<dt>

</dl>
<p style="border-bottom: 1px solid lightgrey;"></p>




<h2 id="UserBriefing"><img style="float: left; margin: 0px 15px 15px 0px;" src="../graphics/pencil2.png">01 - User Briefing</h2>
The most common security vector is social engineering or compromising a user account. You should begin your security audit by sitting with the user (in-person or online, individually or in a group) and walk them through your organization's security policy, and reinforce their understanding of the security vectors they are responsible for. 
<br>
<p><img style="float: left; margin: 0px 15px 15px 0px;" src="../graphics/point1.png"><b>Activity: Checklist for User Briefing</b></p>

>The following items are a base-level of briefing for each system user. You should enhance this list with additional requirements based on your environment and your organization's security policies:
<p><img style="margin: 0px 15px 15px 0px;" src="../graphics/checkbox.png">  Point out location of organization's security policy, and verify signature.</p>
<p><img style="margin: 0px 15px 15px 0px;" src="../graphics/checkbox.png">  Brief the user on the most common threats to individuals and businesses (Loss of Credentials, Vulnerable Systems, and User Error)</p>
<p><img style="margin: 0px 15px 15px 0px;" src="../graphics/checkbox.png">  Brief the user on hygiene practices such as removing unused software and apps, using strong and unique passwords and authenticator-based MFA, correcting default passwords on all network devices, visiting trusted sites (including reviewing cookies, cross-site scripting, and javascript).</p>
<p><img style="margin: 0px 15px 15px 0px;" src="../graphics/checkbox.png">  Explain the most common phishing vectors (phone call, email, text, mistyped addresses), and the payloads (corrupted links, fake forms or websites to collect sensitive or saleable data, offering refunds, offering freebies or limited time only offers, IRS, amazon purchase, virus removal, family member in trouble, boss needs gift cards or for you to click a link or provide information immediately).</p>
<p><img style="margin: 0px 15px 15px 0px;" src="../graphics/checkbox.png">  Explain the different breaches of large companies and visited <a href="https://haveibeenpwned.com/" target="_blank">Have I been pwned?</a> to see if their account information has been leaked in any breaches. Reiterating the importance of unique passwords.</p>
<p><img style="margin: 0px 15px 15px 0px;" src="../graphics/checkbox.png">  Explain the different tactics used to get malware onto computers such as free software or media downloads, corrupted links and files in email and other messaging apps, untrustworthy sites running javascript, weak network controls, clicking on popups or malicious ads - even on trustworthy sites, and using social engineering to have people forward corrupted links and images.</p>
<p><img style="margin: 0px 15px 15px 0px;" src="../graphics/checkbox.png">  Explain the contact information for follow up questions and incident reporting.</p>
<p style="border-bottom: 1px solid lightgrey;"></p>




<h2 id="AssetInventory"><img style="float: left; margin: 0px 15px 15px 0px;" src="../graphics/pencil2.png">02 - Hardware and Software Asset Inventory</h2>
The second most common vector is the exploitation of a vulnerable system. You should continue your security audit by guiding the user through your organizations security and acceptable use policies, and reinforce their understanding of the software and hardware they are responsible for.
<br>
<p><img style="float: left; margin: 0px 15px 15px 0px;" src="../graphics/point1.png"><b>Activity: Checklist for Hardware and Software Asset Inventory</p>

>The following items are a base-level of briefing for each system user. You should enhance this list with additional requirements based on your environment and your organization's security and acceptable use policies:
<p><img style="margin: 0px 15px 15px 0px;" src="../graphics/checkbox.png">  Collect and review Hardware Inventory using the <a href="https://support.microsoft.com/en-us/topic/description-of-microsoft-system-information-msinfo32-exe-tool-10d335d8-5834-90b4-8452-42c58e61f9fc">System Information function</a> in Windows</p>
<p><img style="margin: 0px 15px 15px 0px;" src="../graphics/checkbox.png">  Collect and review Software Inventory using the <a href="https://devblogs.microsoft.com/scripting/use-powershell-to-find-installed-software/">PowerShell Tool</a> in Windows</b></p>
<p><img style="margin: 0px 15px 15px 0px;" src="../graphics/checkbox.png">  Brief the user on removing unused programs.</p>
<p><img style="margin: 0px 15px 15px 0px;" src="../graphics/checkbox.png">  Breif the user on how to check the author of programs and the keys to identifying malicious programs and removing them.</p>
<p><img style="margin: 0px 15px 15px 0px;" src="../graphics/checkbox.png">  Explain that any software that allows a user to do things that are illegal (pirating) will likely cause a compromise.</p>
<p><img style="margin: 0px 15px 15px 0px;" src="../graphics/checkbox.png">  Catalogue and brief the user on peripheral security (Printers, Phones, cameras and microphones).</p>
<p style="border-bottom: 1px solid lightgrey;"></p>




<h2 id="Updates"><img style="float: left; margin: 0px 15px 15px 0px;" src="../graphics/pencil2.png">03 - Patches and Updates</h2>
To protect systems, companies regularly publish updates to software and hardware. You should continue your security audit by guiding the user through the updating process, and reinforce their understanding of the process and necessity of maintaining and up-to-date system.
<br>
<p><img style="float: left; margin: 0px 15px 15px 0px;" src="../graphics/point1.png"><b>Activity: Checklist for Patches and Updates</b></p>

>The following items are a base-level of briefing for each system user. You should enhance this list with additional requirements and processes based on your environment and your organizations security policy:
<p><img style="margin: 0px 15px 15px 0px;" src="../graphics/checkbox.png">  Explain <a href="https://support.microsoft.com/en-us/windows/windows-update-faq-8a903416-6f45-0718-f5c7-375e92dddeb2">Windows Update</a>, and apply approrpiate pending updates. Note that this tool update the Windows operating system, and if selected, any programs that Microsoft provides or those that register with the service. Some applications may not use this feature, so you should use the software list you created earlier to ensure proper updates for each application.</p>
<p><img style="margin: 0px 15px 15px 0px;" src="../graphics/checkbox.png">  Use <a href="https://support.microsoft.com/en-us/windows/update-drivers-in-windows-10-ec62f46c-ff14-c91d-eead-d7126dc1f7b6">device manager</a> to check for the latest and upd to date device drivers. </p>
<p style="border-bottom: 1px solid lightgrey;"></p>




<h2 id="Scans"><img style="float: left; margin: 0px 15px 15px 0px;" src="../graphics/pencil2.png">04 - Virus and Malware Scans</h2>
Not all attacks are immediately visible. You should continue your security audit by guiding the user through a virus and malware check of the system, and reinforcing their understanding of the different types of malware and their purpose.
<br>
<p><img style="float: left; margin: 0px 15px 15px 0px;" src="../graphics/point1.png"><b>Activity: Checklist for Virus and Malware Scans</b></p>
  
>The following items are a base-level of briefing for each system user. You should enhance this list with additional requirements and processes based on your environment and your organizations security policy:
<p><img style="margin: 0px 15px 15px 0px;" src="../graphics/checkbox.png">  Explain and guide the user through the use of <a href="https://support.microsoft.com/en-us/windows/stay-protected-with-windows-security-2ae0363d-0ada-c064-8b56-6a39afb6a963">Windows Security</a> and run a scan.</p>
<p><img style="margin: 0px 15px 15px 0px;" src="../graphics/checkbox.png">  Run a scan for viruses and malware, following the remediation if anything is found.</p>
<p><img style="margin: 0px 15px 15px 0px;" src="../graphics/checkbox.png">  Search application list for anything untrustworthy (unauthored, no versions, unknown) - using search engines to do research on anything you are unsure of.</p>
<p><img style="margin: 0px 15px 15px 0px;" src="../graphics/checkbox.png">  Ensure <a href="https://docs.microsoft.com/en-us/windows/security/identity-protection/user-account-control/user-account-control-overview">User Account Control</a> is configured so that the user is aware of when programs are attempting to make changes.</p>
<p style="border-bottom: 1px solid lightgrey;"></p>




<h2 id="Port"><img style="float: left; margin: 0px 15px 15px 0px;" src="../graphics/pencil2.png">05 - Firewalls and Ports</h2>
Securing the perimeter. You should continue your security audit by guiding the user through a firewall check, reinforcing their understanding of the purpose of the firewall and how to ensure it as effective as possible. 
<br>
<p><img style="float: left; margin: 0px 15px 15px 0px;" src="../graphics/point1.png">Activity: Checklist for Firewalls and Ports</p>

>The following items are a base-level of briefing for each system user. You should enhance this list with additional requirements and processes based on your environment and your organizations security policy:
<p><img style="margin: 0px 15px 15px 0px;" src="../graphics/checkbox.png">  Turn the firewall on if it is not already.
<p><img style="margin: 0px 15px 15px 0px;" src="../graphics/checkbox.png">  Explain the firewall purpose and configuration.</p>
<p><img style="margin: 0px 15px 15px 0px;" src="../graphics/checkbox.png">  Guide the user through checking the firewall and any port forwarding rules required.</p>
<p><img style="margin: 0px 15px 15px 0px;" src="../graphics/checkbox.png">  Guide the user through a check of the firewall logs.</p>
<p style="border-bottom: 1px solid lightgrey;"></p>




<h2 id="Web"><img style="float: left; margin: 0px 15px 15px 0px;" src="../graphics/pencil2.png">06 - Browser, E-Mail and Internet-Facing Assets</h2>
Arguably the best, and also most dangerous, part of using a computer is when it connects to others. Finish your security audit by walking the user through safe browsing, emailing, and internet usage. 
<br>
<p><img style="float: left; margin: 0px 15px 15px 0px;" src="../graphics/point1.png"><b>Activity: Checklist for Browser, E-Mail and Internet-Facing Assets</b></p>

>The following items are a base-level of briefing for each system user. You should enhance this list with additional requirements and processes based on your environment and your organizations security policy:
<p><img style="margin: 0px 15px 15px 0px;" src="../graphics/checkbox.png">  Explain the importance of unique passwords and multifactor authentication.</p>
<p><img style="margin: 0px 15px 15px 0px;" src="../graphics/checkbox.png">  Explain the basics of phishing (email, websites, phone calls - all worsened combined with malware.)</p>
<p><img style="margin: 0px 15px 15px 0px;" src="../graphics/checkbox.png">  Guide the user in spotting malicious emails, links, attachments, and sites.</p>
<p><img style="margin: 0px 15px 15px 0px;" src="../graphics/checkbox.png">  Guide the user in <a href="https://us-cert.cisa.gov/publications/securing-your-web-browser">securing the web browser.</a> (Settings - Privacy, Permissions, Cookies.)
<p style="border-bottom: 1px solid lightgrey;"></p>




<p><img style="margin: 0px 15px 15px 0px;" src="../graphics/owl.png"><b>For Further Study</b></p>
<ul>
    <li><a href="https://nvd.nist.gov/">NIST National Vulnerability Database<a></li> 
    <li><a href="https://www.microsoft.com/en-us/videoplayer/embed/RE3Fq1Y"></a>Firewall and network protection resource video</li>
</ul>

Congratulations! You have completed this Audit - ensure you set the next schedule to complete the Audit for the Edge systems and Users at this time.
