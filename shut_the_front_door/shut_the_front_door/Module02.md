# Workshop: Shut The Front Door

#### <i>A Security Course from Buck Woody and David Seis</i>

<p style="border-bottom: 1px solid lightgrey;"></p>

<img style="float: left; margin: 0px 15px 15px 0px;" src="../graphics/textbubble.png"> <h2>Module 02: Basic Security Tools</h2>

In this workshop you'll cover using the basic security tools avaliable, and recommended for using in monitoring and protecting your systems. 

In each module you'll get more references, which you should follow up on to learn more. Also watch for links within the text - click on each one to explore that topic.

You'll cover these topics in this Module of the workshop:
<dl>
  <dt><a href="url" target="_blank">2.1 - Windows Update</a></dt>
  <dt><a href="url" target="_blank">2.2 - Windows Security</a></dt>
  <dt><a href="url" target="_blank">2.3 - Windows Map Tool</a></dt>
</dl>

<br>
<p style="border-bottom: 1px solid lightgrey;"></p>

<br>
<h2><img style="float: left; margin: 0px 15px 15px 0px;" src="../graphics/pencil2.png">2.1 Windows Update</h2>

<p>Maintaining an updated system is important for avoiding many security vulnerabilities, and is one of the simplest and yet most often overlooked security vectors. In the Microsoft Windows operating system, the "System Update" tool is responsible for assessing the current state of the computer and updating it for performance, capability, and security aspects. You can make various changes to the behavior of the frequency, source, and application of these patches. For software from Microsoft, the System Update can also check patches for those deployments as well if desired.</p>

> NOTE: Your organization may have a central policy, method or process for updating the operating system and any software installed on workstations. Ensure that you are not violating any of those polcies or processes prior to continuing. 

More information on the [Microsoft Update utility is here](https://docs.microsoft.com/en-us/windows/deployment/update/waas-wu-settings). You should understand the settings it has, and how it affects a system before you run it. 

<br>
<p><img style="float: left; margin: 0px 15px 15px 0px;" src="../graphics/point1.png"><b>Activity: Update a Windows System</b></p>
<br>

<p>In this Activity you will check the settings for Windows Update, and use it to identify any pending updates and to apply them.</p>

> NOTE: Do NOT apply any changes to a system that does not have a current backup. While updates are generally safe, there are circumstances where an update to a driver or DLL can damage a functional system. Making changes without a backup can permanently damage a system, or render it unable to boot. If you are uncertain about the backup status of the workstation you are using for this course, use the steps below only as a review - do not proceed without a backup.

<br>
<p><img style="float: left; margin: 0px 15px 15px 0px;" src="../graphics/checkmark.png"><b>Description</b></p>

<p>In this step you will use Windows Update to maintain a secure system.</p>

<br>
<p><img style="float: left; margin: 0px 15px 15px 0px;" src="../graphics/checkmark.png"><b>Steps</b></p>

<br>
<p><img style="float: left; margin: 0px 15px 15px 0px;" src="../graphics/checkbox.png"> Press the Winodws key to open the search function. Type "Windows Update" and open the Settings app that checks for updates.</p>  
<p><img style="float: left; margin: 0px 15px 15px 0px;" src="../graphics/checkbox.png"> Click the option to <i>"Search for Updates"</i>.</p>
<p><img style="float: left; margin: 0px 15px 15px 0px;" src="../graphics/checkbox.png"> In the case of pending updates or the message saying all updates are current it is good practice to apply updates and then re-search for updates, just in case.</p>
<p><img style="float: left; margin: 0px 15px 15px 0px;" src="../graphics/checkbox.png"> In the case of an error, follow the steps </a href="https://support.microsoft.com/en-us/sbs/windows/fix-windows-update-errors-18b693b5-7818-5825-8a7e-2a4a37d6d787"> in this Microsoft Support article to correct them</a>.</p>

<br>
<p style="border-bottom: 1px solid lightgrey;"></p>

<h2><img style="float: left; margin: 0px 15px 15px 0px;" src="../graphics/pencil2.png">2.2 Windows Security</h2>

The Windows Security application can help ensure your computer is protected from many vulnerabilities. The following areas are covered in this tool:

- Virus and threat protection: Information and access to antivirus ransomware protection settings and notifications, including Controlled folder access, and sign-in to Microsoft OneDrive.
- Account protection: Information and access to sign-in and account protection settings.
- Firewall and network protection: Information and access to firewall settings, including Windows Defender Firewall.
- Application and browser control: Controls Windows Defender SmartScreen settings and Exploit protection mitigations.
- Device security: Provides access to built-in device security settings.
- Device performance and health: Information about drivers, storage space, and general Windows Update issues.
- Family options: Includes access to parental controls along with tips and information for keeping kids safe online.

> NOTE: Do NOT apply any changes to a system that does not have a current backup. While updates are generally safe, there are circumstances where an update to a driver or DLL can damage a functional system. Making changes without a backup can permanently damage a system, or render it unable to boot. If you are uncertain about the backup status of the workstation you are using for this course, use the steps below only as a review - do not proceed without a backup. Your organiation may have a different system to perform these functions, so follow those requirements, processes and instructions if they are in place.

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="../graphics/point1.png"><b>Activity: Windows Security Configuration</b></p>

<p>Configuring Windows Security eanbles features such as virus scanning, account protection, firewall and network, browsing, and device security.</p>

<br>
<p><img style="margin: 0px 15px 15px 0px;" src="../graphics/checkmark.png"><b>Description</b></p>
<p>The steps that follow will configure virus and threat protection on your system.</p>

<p><img style="margin: 0px 15px 15px 0px;" src="../graphics/checkmark.png"><b>Steps</b></p>
<p><img style="float: left; margin: 0px 15px 15px 0px;" src="../graphics/checkbox.png">  Press the Windows key to start the search function, and type <i>"Windows Security"</i>.</p>
<p><img style="float: left; margin: 0px 15px 15px 0px;" src="../graphics/checkbox.png">  Click Virus & Threat Protection.</p>
<p><img style="float: left; margin: 0px 15px 15px 0px;" src="../graphics/checkbox.png">  Ensure the Virus & threat protection updates are current is important for blocking up-to-date malware.</p>
<p><img style="float: left; margin: 0px 15px 15px 0px;" src="../graphics/checkbox.png">  Check the Virus and threat protection settings to ensure real-time protection is on, as well as tamper protection, cloud delivered protection and automatic sample submission.</p>
<p><img style="float: left; margin: 0px 15px 15px 0px;" src="../graphics/checkbox.png">  Run a full scan to check the health of your device.</p>

<p><img style="margin: 0px 15px 15px 0px;" src="../graphics/checkmark.png"><b>Description</b></p>
<p>In this activity you will configure account protection.</p>

<p><img style="margin: 0px 15px 15px 0px;" src="../graphics/checkmark.png"><b>Steps</b></p>
<p><img style="float: left; margin: 0px 15px 15px 0px;" src="../graphics/checkbox.png">  Click <i>Account Protection</i></p>
<p><img style="float: left; margin: 0px 15px 15px 0px;" src="../graphics/checkbox.png">  Using Windows Hello or another Multi-factor Authentication (security key, biometrics, etc.) will help protect your device and account. <a href="https://docs.microsoft.com/en-us/windows/security/threat-protection/windows-defender-security-center/wdsc-account-protection">Review this feature here</a>.</p>

<p><img style="margin: 0px 15px 15px 0px;" src="../graphics/checkmark.png"><b>Description</b></p>
<p>In this step you will configure firewall and network protection.</p>

<p><img style="margin: 0px 15px 15px 0px;" src="../graphics/checkmark.png"><b>Steps</b></p>
<p><img style="float: left; margin: 0px 15px 15px 0px;" src="../graphics/checkbox.png">  Click Firewall & Network Protection</p>
<p><img style="float: left; margin: 0px 15px 15px 0px;" src="../graphics/checkbox.png">  Turn the firewall on if it is not already (and there is not 3rd party firewall enabled.)</p>
<p><img style="float: left; margin: 0px 15px 15px 0px;" src="../graphics/checkbox.png">  Watch <A href="https://www.microsoft.com/en-us/videoplayer/embed/RE3Fq1Y">This video from Microsoft</a> to help understand the role of the firewall. </p>

<p><img style="margin: 0px 15px 15px 0px;" src="../graphics/checkmark.png"><b>Description</b></p>
<p>In this step you will configure applicationa and browser control.</p>

<p><img style="margin: 0px 15px 15px 0px;" src="../graphics/checkmark.png"><b>Steps</b></p>
<p><img style="float: left; margin: 0px 15px 15px 0px;" src="../graphics/checkbox.png">  Click App & Browser Control</p>
<p><img style="float: left; margin: 0px 15px 15px 0px;" src="../graphics/checkbox.png">  Ensure reputation-based protections are all enabled.</p>
<p><img style="float: left; margin: 0px 15px 15px 0px;" src="../graphics/checkbox.png">  Ensure Exploit protection settings are all "On" by Default (except image randomization)</p>
<p><img style="float: left; margin: 0px 15px 15px 0px;" src="../graphics/checkbox.png">  Consider using Microsoft's Defender Appllication guard and With edge for a very secure browsing environment. </p>

<p><img style="margin: 0px 15px 15px 0px;" src="../graphics/checkmark.png"><b>Description</b></p>
<p>In this step you will configure device security settings.</p>

<p><img style="margin: 0px 15px 15px 0px;" src="../graphics/checkmark.png"><b>Steps</b></p>
<p><img style="float: left; margin: 0px 15px 15px 0px;" src="../graphics/checkbox.png">  Click <i>Device Security</i></p>
<p><img style="float: left; margin: 0px 15px 15px 0px;" src="../graphics/checkbox.png">  If your device has the appropriate hardware you have choices outlined in <a href="https://www.microsoft.com/en-us/videoplayer/embed/RE4qLzU">this video</a></p>

<p><img style="margin: 0px 15px 15px 0px;" src="../graphics/checkmark.png"><b>Description</b></p>
<p>In this activity you can check the your device's health and get an overview.</p>

<p><img style="margin: 0px 15px 15px 0px;" src="../graphics/checkmark.png"><b>Steps</b></p>
<p><img style="float: left; margin: 0px 15px 15px 0px;" src="../graphics/checkbox.png">  Click Device performance and health - check to see if there are any issues and then watch <a href="https://www.microsoft.com/en-us/videoplayer/embed/RE3F7Sk">this video</a></p>

<br>
<p style="border-bottom: 1px solid lightgrey;"></p>

<h2><img style="float: left; margin: 0px 15px 15px 0px;" src="../graphics/pencil2.png">2.3 Windows MAP Tool</h2>
<p>The Microsoft Assessment and Planning (MAP) Toolkit can be used to get an inventory of one or more systems on your network. It creates reports that you can use for more than a single system.</p>

> NOTE: You may need Domain or Local system administrator rights to perform this scan, so ensure you coordinate this tool with your organization's IT Team. 

<p><img style="float: left; margin: 0px 15px 15px 0px;" src="../graphics/point1.png"><b>Activity: Read the example reports</b></p>
The MAP toolkit is useful in hardware and software inventorying as well as systems upgrading. Using this tool will help in a variety of ways.

<p><img style="margin: 0px 15px 15px 0px;" src="../graphics/checkmark.png"><b>Description</b></p>
Run the MAP tool or review the different example reports run through the MAP tool to see what benefit it could be in your situation.

<p><img style="margin: 0px 15px 15px 0px;" src="../graphics/checkmark.png"><b>Steps</b></p>
<p><img style="float: left; margin: 0px 15px 15px 0px;" src="../graphics/checkbox.png">  Go to <a href="https://social.technet.microsoft.com/wiki/contents/articles/1640.microsoft-assessment-and-planning-map-toolkit-getting-started.aspx#GSG">this link</a> to read about the setup, use, and interpretation of the MAP toolkit reports. 
<p><img style="float: left; margin: 0px 15px 15px 0px;" src="../graphics/checkbox.png">  (OPTIONAL: download the map toolkit and review the example reports to see the possibilities.)</p>

<br>
<p style="border-bottom: 1px solid lightgrey;"></p>

<br>
<p><img style="margin: 0px 15px 15px 0px;" src="../graphics/owl.png"><b>For Further Study</b></p>
<ul>
    <li><a href="https://community.windows.com/en-us/videos/windows-security-the-dashboard-for-device-protections/e_Z2bk7Cp1g?from=search" target="_blank">Windows Security: The dashboard for device protections</a></li>
    <li><a href="https://community.windows.com/en-us/videos/keep-your-pc-more-secure-with-windows-security-updates/YmIitr4eJ8E?from=search" target="_blank">Keep your PC more secure with Windows Security Updates</a></li>
    <li><a href="https://community.windows.com/en-us/videos/device-security-security-that-comes-built-into-your-device/fadv4TuMOnc?from=search" target="_blank">Device security: Security that comes built into your device</a></li>
    <li><a href="https://community.windows.com/en-us/videos/meet-marcus-security-made-simple-with-windows-10-in-s-mode/VvAPQTtd-M8?from=search" target="_blank">Meet Marcus: Security made simple with Windows 10 in S mode</a></li>
    <li><a href="https://community.windows.com/en-us/videos/windows-defender-team-make-security-easier/vuduNkegxb8?from=search" target="_blank">Windows Defender team: Make security easier</a></li>
    <li><a href="https://community.windows.com/en-us/videos/firewall-network-protections-keep-unwanted-online-traffic-out/pfyyc9XdT5M?from=search" target="_blank">Firewall & network protections: Keep unwanted online traffic out</a></li>
    <li><a href="https://community.windows.com/en-us/videos/app-browser-control-add-protection-and-online-security/4kyb3u8AVpg?from=search" target="_blank">App & browser control: Add protection and online security</a></li>
    <li><a href="https://community.windows.com/en-us/videos/virus-threat-protection-keep-defender-antivirus-at-full-strength/s5ezErDI_IM?from=search" target="_blank">Virus & threat protection: Keep Defender antivirus at full strength</a></li>
</ul>

Next, Continue to <a href="https://github.com/BuckWoody/presentations/blob/master/shut_the_front_door/shut_the_front_door/Module03.md" target="_blank"><i>Module 03: Security Processes and Procedures</i></a>.
