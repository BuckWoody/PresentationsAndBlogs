# Windows System Setup

These are a few of the scripts, commands, and other environment settings I use on my Windows systems. I'm currently running Windows 11 Enterprise, which is working well with these settings. I do everything in [PowerShell](https://learn.microsoft.com/en-us/powershell/) (Core) for my system management and configuration. Also, some of these commands won't run properly unless you are in "Elevated" or "Administrator" level, so be aware of that.

This is for info and examples **only**. I explain a few things here, but if *anything* is a new term or command, highlight it and look it up. Understand what your are doing if you want to try this - and you're on your own here - test first, don't run this in production first! 

### Disclaimer, for people who need to be told this sort of thing: 

*Never trust any script, presentation, code or information including those that you find here, until you understand exactly what it does and how it will act on your systems. Always check scripts and code on a test system or Virtual Machine, not a production system. Yes, there are always multiple ways to do things, and this script, code, information, or content may not work in every situation, for everything. It’s just an example, people. All scripts on this site are performed by a professional stunt driver on a closed course. Your mileage may vary. Void where prohibited. Offer good for a limited time only. Keep out of reach of small children. Do not operate heavy machinery while using this script. If you experience blurry vision, indigestion or diarrhea during the operation of this script, see a physician immediately*

If you want to suggest something here, add an [Issue](https://docs.github.com/en/issues/tracking-your-work-with-issues/creating-an-issue) referencing this page and what you want to mention. If I like it, I'll put it here. I'll not close the Issue unless it's a bug you've found, that way you can see what other people do that I didn't include. 

# Configure Powershell Environment

I like interesting prompts and so on. I also use [Windows Terminal](https://apps.microsoft.com/detail/9N0DX20HK701?launch=true&mode=full&referrer=bingwebsearch&ocid=bingwebsearch&hl=en-us&gl=US), which is really useful. My prompt looks like this (I blanked out my domain name in this graphic, it shows if you use this script:)

![My PowerShell Prompt, which has embedded graphics](../graphics/tempsnip.png)

Here's how I configured my main profile in PowerShell:

<pre> notepad $profile </pre>

Then I entered this text in the file it creates: 

<pre>
function prompt {

    $host.ui.RawUI.WindowTitle = "Current Folder: $pwd"
    $CmdPromptUser = [Security.Principal.WindowsIdentity]::GetCurrent();
    $IsAdmin = (New-Object Security.Principal.WindowsPrincipal ([Security.Principal.WindowsIdentity]::GetCurrent())).IsInRole([Security.Principal.WindowsBuiltinRole]::Administrator)

    Write-Host ""
    Write-Host "`u{1F9D9} $($CmdPromptUser.Name.split("\")[1]) " -ForegroundColor Green -NoNewline
    Write-host ($(if ($IsAdmin) { '(as admin) ' } else { '' })) -ForegroundColor Red -NoNewLine
    Write-Host "on `u{1F4BB}" $env:COMPUTERNAME"."$env:USERDNSDOMAIN

    Write-Host "`u{1F4C1} $pwd"  -ForegroundColor Yellow 
    return "`u{25B6} "
} 
</pre>

## Install Choco from PowerShell

Package Managers are tools that help you install/configure/uninstall software from the command-line. 
I primarily use [winget](https://learn.microsoft.com/en-us/windows/package-manager/winget/) for that, since it's built into the latest Windows releases, but I really like the [chocolatey](https://chocolatey.org/) package manager for other things. Here's how I installed that on my system:

<pre>
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
</pre>

# Install PSWindowsUpdate

I keep my system up to date from the command line in PowerShell, and to completely do that I want to get the Windows Updates as well. I do that with a PowerShell module called [PSWindowsUpdate](https://woshub.com/pswindowsupdate-module/)

<pre>
Set-ExecutionPolicy -ExecutionPolicy Unrestricted
Install-Module -Name PSWindowsUpdate -Force
Add-WUServiceManager -ServiceID 7971f918-a847-4430-9279-4a52d1efe18d
</pre>

# Put Windows 11 Full Context Menu back in Explorer

With all apologies to the Windows team (who are AWESOME), I like having the full menu available when  I right-click an item in the File Explorer in Windows. Again, do this at your own risk.

**[Back up your registry if you try this on a test system! You should be doing that anyway. Click here to learn more.](https://support.microsoft.com/en-us/topic/how-to-back-up-and-restore-the-registry-in-windows-855140ad-e318-2a13-2829-d428a2ab0692)**

<pre>
reg.exe add "HKCU\Software\Classes\CLSID\{86ca1aa0-34aa-4e8b-a509-50c905bae2a2}\InprocServer32" /f /ve
</pre>

# Update Windows from Command Line 

As I mentioned, I run a complete update script to keep my system up to date and secure. I also do things like making sure the time is sync'd first (super important), find out the drive space, do some cleanup, and show my network status. 

> This is the most dangerouse of the scripts, don't run this on your test system without understanding everything it does. Completely. You are on your own here.

<pre>
$host.ui.RawUI.WindowTitle = "Synchronizing Clock..."
net start w32time
w32tm /resync

$host.ui.RawUI.WindowTitle = "Beginning update with Choco..."
Write-Host "Running Choco Upgrade"
choco upgrade all --confirm

$host.ui.RawUI.WindowTitle = "Beginning update with Winget..."
Write-Host "Running Winget Upgrade"
winget upgrade --all 

$host.ui.RawUI.WindowTitle = "Beginning update with PSWindowsUpgrade..."
Write-Host "Running PSWindowsUpgrade"
get-windowsupdate
install-windowsupdate -acceptall | Format-Table -Property Result, Title, Description -wrap

$host.ui.RawUI.WindowTitle = "Beginning File Cleanup with CleanMgr..."
Write-Host "Running CleanMgr"
Start-Process -FilePath CleanMgr.exe -ArgumentList '/sagerun:1' ##-WindowStyle Hidden

$host.ui.RawUI.WindowTitle = "Checking Logs for Errors..."
Get-EventLog -LogName System -EntryType Error | Out-GridView -Title "Windows System Log Error List"
Get-EventLog -LogName Application -EntryType Error  | Out-GridView -Title "Windows Application Log Error List"
Get-EventLog -LogName Security -EntryType Error | Out-GridView -Title "Windows Security Log Error List"

$host.ui.RawUI.WindowTitle = "Complete. System Information:"

Write-Host "Drives: "
Get-Volume | sort-object Size

Write-Host "Network: " 
Get-NetIPConfiguration | format-table -autosize -Property InterfaceDescription, IPv4Address

Write-Host "GB of Memory om this system: " 
(Get-CimInstance Win32_PhysicalMemory | Measure-Object -Property capacity -Sum).sum /1gb
</pre>

## So what's your deal?

Like these? Am I doing something wrong or that I could do better? Hit me up in the "Issues" tab there at the top of the page. Be complete, not just "You're wrong". :) 
