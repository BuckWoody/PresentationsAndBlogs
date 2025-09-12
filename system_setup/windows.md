# Windows System Setup

These are a few of the scripts, commands, and other environment settings I use on my Windows systems. I'm currently running Windows 11 Enterprise, which is working well with these settings. I do everything in [PowerShell](https://learn.microsoft.com/en-us/powershell/) (Core) for my system management and configuration. Also, some of these commands won't run properly unless you are in "Elevated" or "Administrator" level, so be aware of that.

This is for info and examples **only**. I explain a few things here, but if *anything* is a new term or command, highlight it and look it up. Understand what your are doing if you want to try this - and you're on your own here - test first, don't run this in production first! I highly [recommend using the Windows Sandbox feature](https://learn.microsoft.com/en-us/windows/security/application-security/application-isolation/windows-sandbox/) to test things if you are running Windows 11.

### Disclaimer, for people who need to be told this sort of thing: 

*Never trust any script, presentation, code or information including those that you find here, until you understand exactly what it does and how it will act on your systems. Always check scripts and code on a test system or Virtual Machine, not a production system. Yes, there are always multiple ways to do things, and this script, code, information, or content may not work in every situation, for everything. It’s just an example, people. All scripts on this site are performed by a professional stunt driver on a closed course. Your mileage may vary. Void where prohibited. Offer good for a limited time only. Keep out of reach of small children. Do not operate heavy machinery while using this script. If you experience blurry vision, indigestion or diarrhea during the operation of this script, see a physician immediately*

If you want to suggest something here, add an [Issue](https://docs.github.com/en/issues/tracking-your-work-with-issues/creating-an-issue) referencing this page and what you want to mention. If I like it, I'll put it here. I'll not close the Issue unless it's a bug you've found, that way you can see what other people do that I didn't include. 

# Windows System Maintenance Checklist

1. **Create a System Restore Point**
   - Open **Control Panel** > **System and Security** > **System**.
   - Click **System protection** on the left.
   - Click **Create** and follow the prompts to create a restore point.
   - Note: The script below can do this, [but you have to edit your registry first. Use at your own risk](https://www.thewindowsclub.com/how-to-schedule-system-restore-points-in-windows-10).

2. **Back Up Your Files**
   - Use either the command line [**ROBOCOPY**](https://lazyadmin.nl/it/robocopy-ultimate-guide/) or [use an option listed here](https://support.microsoft.com/en-us/windows/choose-a-backup-solution-in-windows-10-31495e5d-370e-3631-c773-44de4301e070).

3. **Backup BitLocker Keys**
   - Open **Control Panel** > **System and Security** > **BitLocker Drive Encryption**.
   - Click **Manage BitLocker**.
   - Select **Back up your recovery key** and choose a safe location to save the key (e.g., USB drive, Microsoft account, or print it).

4. **Update Windows**
   - Go to **Settings** > **Update & Security** > **Windows Update**.
   - Click **Check for updates** and install any available updates.
   - (See below if you want a comand-line way to do this)

5. **Run a Virus Scan**
   - Open **Windows Security** from the Start menu.
   - Go to **Virus & threat protection**.
   - Click **Quick scan** or **Full scan** to check for malware.

6. **Check for System File Integrity**
   - Open **Command Prompt** as an administrator.
   - Type `sfc /scannow` and press **Enter**.
   - Wait for the scan to complete and follow any instructions provided.

7. **Check Disk for Errors**
   - Open **File Explorer** and right-click on the drive you want to check.
   - Select **Properties** > **Tools** > **Check** under Error checking.
   - Follow the prompts to scan and repair the drive if necessary.

8. **Clean Up Disk Space**
   - Open **Disk Cleanup** by typing it in the Start menu search bar.
   - Select the drive you want to clean up and click **OK**.
   - Check the boxes for the types of files you want to delete and click **OK**.

9. **Defragment and Optimize Drives**
   - Open **Defragment and Optimize Drives** by typing it in the Start menu search bar.
   - Select the drive you want to optimize and click **Optimize**.

10. **Review Startup Programs**
    - Open **Task Manager** by pressing **Ctrl + Shift + Esc**.
    - Go to the **Startup** tab.
    - Disable any unnecessary programs that start with Windows.

# Initial Setup - Configure Powershell Environment

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

## Maintenance - Install Choco from PowerShell

Package Managers are tools that help you install/configure/uninstall software from the command-line. 
I primarily use [winget](https://learn.microsoft.com/en-us/windows/package-manager/winget/) for that, since it's built into the latest Windows releases, but I really like the [chocolatey](https://chocolatey.org/) package manager for other things. Here's how I installed that on my system:

<pre>
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
</pre>

# Maintenance - Install PSWindowsUpdate

I keep my system up to date from the command line in PowerShell, and to completely do that I want to get the Windows Updates as well. I do that with a PowerShell module called [PSWindowsUpdate](https://woshub.com/pswindowsupdate-module/)

<pre>
Set-ExecutionPolicy -ExecutionPolicy Unrestricted
Install-Module -Name PSWindowsUpdate -Force
Add-WUServiceManager -ServiceID 7971f918-a847-4430-9279-4a52d1efe18d
</pre>

# Update Windows from Command Line 

As I mentioned, I run a complete update script to keep my system up to date and secure. I also do things like making sure the time is sync'd first (super important), find out the drive space, do some cleanup, and show my network status. 

> This is the most dangerous of the scripts, don't run this on your test system without understanding everything it does. Completely. You are on your own here.

```powershell
<#
.BOF - updateme.ps1

.DESCRIPTION
Windows 11 System Maintenance (Buck Woody, version 09.12.2025)

Performs maintenance tasks: 
    - Logs each section to Windows Application log.
    - Makes a Wi-Fi connect if both connected and wifi enabled
    - clock sync
    - Defender scan
    - updates via Chocolatey/Winget/PSWindowsUpdate
    - WSL update
    - disk cleanup 
    - log review
    - Displays system info.

Requires: 
    - Chocolately
    - PSCalendar
    - PSWindowsUpdate
#>

[CmdletBinding(SupportsShouldProcess)]
param(
    [string]$WifiSSID = 'YourWifiSID',
    [string]$WifiProfileName = 'YourWifiProfileName',
    [string]$WifiInterface = 'Wi-Fi',
    [switch]$ForceClearEventLogs,
    [switch]$SkipWifi,
    [switch]$SkipCalendar
)

# --- Config ---
$EventSource = 'Updateme.Script'
$EventLogName = 'Application'
$Evt = @{
    SectionStart = 1000
    SectionOK    = 1001
    SectionWarn  = 1002
    SectionErr   = 1003
}

# --- Functions ---
function Ensure-Admin {
    # Ensures the script is running with admin rights; if not, relaunches as admin 
    $id = [Security.Principal.WindowsIdentity]::GetCurrent()
    $p  = New-Object Security.Principal.WindowsPrincipal($id)
    if (-not $p.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
        Write-Host "Elevation required. Relaunching as Administrator..."
        $psi = New-Object System.Diagnostics.ProcessStartInfo
        $psi.FileName = (Get-Process -Id $PID).Path
        $args = @()
        if ($PSCommandPath) { $args += '-File', "`"$PSCommandPath`"" }
        if ($MyInvocation.UnboundArguments) { $args += $MyInvocation.UnboundArguments }
        $psi.Arguments = $args -join ' '
        $psi.Verb = 'runas'
        [Diagnostics.Process]::Start($psi) | Out-Null
        exit
    }
}

function Ensure-EventSource {
    # Ensures the event source exists; if not, creates it
    if (-not [System.Diagnostics.EventLog]::SourceExists($EventSource)) {
        New-EventLog -LogName $EventLogName -Source $EventSource
    }
}

function Set-WindowTitle {
    # Sets the console window title if running interactively
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string]$Title
    )
    try {
        $host.UI.RawUI.WindowTitle = $Title
    } catch {
        # Non-interactive host; ignore
    }
}

function Write-AppLog {
    <#
    .SYNOPSIS
        Writes a line to console and (best-effort) to Windows Application log.
    .PARAMETER Message
        The text to log.
    .PARAMETER Level
        Information | Warning | Error
    .PARAMETER EventId
        Integer event id to write.
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string]$Message,

        [ValidateSet('Information','Warning','Error')]
        [string]$Level = 'Information',

        [int]$EventId = $script:Evt_SectionOK  # assumes you've defined this earlier
    )

    # Console echo (avoid "$Level: ..." parsing issue)
    Write-Host ("{0}: {1}" -f $Level, $Message)

    # Event log write (best effort)
    try {
        if ([System.Diagnostics.EventLog]::SourceExists($script:EventSource)) {
            $entryType = [System.Diagnostics.EventLogEntryType]::$Level
            Write-EventLog -LogName $script:EventLogName `
                           -Source  $script:EventSource `
                           -EventId $EventId `
                           -EntryType $entryType `
                           -Message $Message
        }
    } catch {
        # swallow to keep maintenance flow resilient
    }
}

function Invoke-Step {
    # Sets the window title, logs start, runs the script block, logs success or failure
    param([string]$Name,[scriptblock]$Script)
    Set-WindowTitle $Name
    Write-AppLog "$Name - Running..." 'Information' $Evt.SectionStart
    try {
        & $Script
        Write-AppLog "$Name - OK" 'Information' $Evt.SectionOK
    } catch {
        Write-AppLog "$Name - ERROR: $($_.Exception.Message)" 'Error' $Evt.SectionErr
    }
}

# --- Maintenance Tasks ---
function Show-Calendar {
    # Displays calendar if PSCalendar is available - if not, you should install it
    if ($SkipCalendar) { return }
    if (Get-Command Get-Calendar -ErrorAction SilentlyContinue) {
        Get-Calendar
    } else {
        Write-AppLog "PSCalendar not available, skipping" 'Warning' $Evt.SectionWarn
    }
}

function Connect-Wifi {
    # Connects to specified Wi-Fi SSID/profile/interface if not skipped. Change the name to your wifi profile.
    param($SSID,$Profile,$Interface)
    if ($SkipWifi) { return }
    & netsh wlan connect ssid=$SSID name=$Profile interface=$Interface
}

function Sync-Clock {
    # Syncs the system clock
    net start w32time | Out-Null
    w32tm /resync | Out-Null
}

function Defender-QuickScan {
    # Runs a quick scan with Windows Defender
    $mp = Get-ChildItem "$env:ProgramData\Microsoft\Windows Defender\Platform" -Recurse -Filter MpCmdRun.exe -ErrorAction SilentlyContinue |
          Sort-Object LastWriteTime -Descending | Select-Object -First 1 -ExpandProperty FullName
    if (-not $mp) { $mp = "$env:ProgramFiles\Windows Defender\MpCmdRun.exe" }
    if (Test-Path $mp) { & $mp -Scan -ScanType 1 } else { Write-AppLog "Defender not found; skipping" 'Warning' }
}

function Upgrade-Choco {
    # Upgrades all installed Chocolatey packages
    if (Get-Command choco -ErrorAction SilentlyContinue) { choco upgrade all -y } else { Write-AppLog "Chocolatey not found" 'Warning' }
}

function Upgrade-Winget {
    # Upgrades all installed Winget packages
    if (Get-Command winget -ErrorAction SilentlyContinue) { winget upgrade --all --silent } else { Write-AppLog "Winget not found" 'Warning' }
}

function Upgrade-PSWindowsUpdate {
    # Upgrades Windows via PSWindowsUpdate module. You should install it first.
    try {
        if (-not (Get-Module PSWindowsUpdate -ListAvailable)) {
            Install-Module PSWindowsUpdate -Scope CurrentUser -Force
        }
        Import-Module PSWindowsUpdate
        $updates = Get-WindowsUpdate
        if ($updates) { Install-WindowsUpdate -AcceptAll -IgnoreReboot } else { Write-AppLog "No Windows Updates" }
    } catch {
        Write-AppLog "PSWindowsUpdate failed: $($_.Exception.Message)" 'Warning'
    }
}

function Update-WSL {
    # Updates Windows Subsystem for Linux if installed
    if (Get-Command wsl -ErrorAction SilentlyContinue) { wsl --update } else { Write-AppLog "WSL not found" 'Warning' }
}

function Run-CleanMgr {
    # Runs Disk Cleanup in silent mode with preset options
    if (Get-Command CleanMgr.exe -ErrorAction SilentlyContinue) {
        Start-Process CleanMgr.exe -ArgumentList '/sagerun:1' -Wait -WindowStyle Hidden
    } else {
        Write-AppLog "CleanMgr not found" 'Warning'
    }
}

function Show-RecentErrors {
    # Shows the most recent 50 errors from System, Application, and Security logs
    foreach ($log in 'System','Application','Security') {
        Write-Host "`nErrors in $log log:"
        Get-EventLog -LogName $log -EntryType Error -Newest 50 |
            Select-Object TimeGenerated,Source,EventID,Message
    }
}

function Show-SystemInfo {
<#
.SYNOPSIS
    Displays drive sizes and memory info in Gigabytes.
.DESCRIPTION
    - Drives: SizeGB, UsedGB, FreeGB, PercentUsed (sorted by SizeGB)
    - Memory: Physical and Virtual totals, used, free, and % used
    - All values in GB (1 GB = 1,073,741,824 bytes for drives; OS memory KB converted to GB)
#>

    try {
        # Update console title
        if (Get-Command -Name Set-WindowTitle -ErrorAction SilentlyContinue) {
            Set-WindowTitle -Title 'Complete System Information (GB)'
        }

        Write-Host "`n=== Drives (GB) ==="
        $drives = Get-CimInstance Win32_LogicalDisk -Filter "DriveType = 3" | ForEach-Object {
            $sizeGB = if ($_.Size) { [math]::Round($_.Size / 1GB, 2) } else { $null }
            $freeGB = if ($_.FreeSpace) { [math]::Round($_.FreeSpace / 1GB, 2) } else { $null }
            $usedGB = if ($sizeGB -and $freeGB) { [math]::Round($sizeGB - $freeGB, 2) } else { $null }
            $pctUsed = if ($sizeGB -gt 0) { [math]::Round(($usedGB / $sizeGB) * 100, 1) } else { $null }

            [pscustomobject]@{
                Drive       = $_.DeviceID
                Label       = $_.VolumeName
                FileSystem  = $_.FileSystem
                SizeGB      = $sizeGB
                UsedGB      = $usedGB
                FreeGB      = $freeGB
                PercentUsed = $pctUsed
            }
        }

        $drives | Sort-Object -Property SizeGB -Descending | Format-Table -AutoSize

        Write-Host "`n=== Memory (GB) ==="
        $os = Get-CimInstance Win32_OperatingSystem
        $physTotalGB = [math]::Round($os.TotalVisibleMemorySize / 1MB, 2)  # KB → GB
        $physFreeGB  = [math]::Round($os.FreePhysicalMemory / 1MB, 2)
        $physUsedGB  = [math]::Round($physTotalGB - $physFreeGB, 2)
        $physPctUsed = if ($physTotalGB -gt 0) { [math]::Round(($physUsedGB / $physTotalGB) * 100, 1) } else { $null }

        $virtTotalGB = [math]::Round($os.TotalVirtualMemorySize / 1MB, 2)
        $virtFreeGB  = [math]::Round($os.FreeVirtualMemory / 1MB, 2)
        $virtUsedGB  = [math]::Round($virtTotalGB - $virtFreeGB, 2)
        $virtPctUsed = if ($virtTotalGB -gt 0) { [math]::Round(($virtUsedGB / $virtTotalGB) * 100, 1) } else { $null }

        $procWSumGB  = [math]::Round((Get-Process | Measure-Object -Property WorkingSet64 -Sum).Sum / 1GB, 2)
        $procPagedGB = [math]::Round((Get-Process | Measure-Object -Property PagedMemorySize64 -Sum).Sum / 1GB, 2)

        $memTable = @(
            [pscustomobject]@{
                Category    = 'Physical'
                TotalGB     = $physTotalGB
                UsedGB      = $physUsedGB
                FreeGB      = $physFreeGB
                PercentUsed = $physPctUsed
            }
            [pscustomobject]@{
                Category    = 'Virtual'
                TotalGB     = $virtTotalGB
                UsedGB      = $virtUsedGB
                FreeGB      = $virtFreeGB
                PercentUsed = $virtPctUsed
            }
            [pscustomobject]@{
                Category    = 'Processes'
                TotalGB     = 'N/A'
                UsedGB      = $procWSumGB
                FreeGB      = 'N/A'
                PercentUsed = "Paged: $procPagedGB GB"
            }
        )

        $memTable | Format-Table -AutoSize

        if (Get-Command -Name Write-AppLog -ErrorAction SilentlyContinue) {
            Write-AppLog -Message "System info in GB (drives + memory) collected" -Level Information -EventId $script:Evt.SectionOK
        }
    }
    catch {
        $msg = "Show-SystemInfo failed: $($_.Exception.Message)"
        Write-Host "WARN: $msg"
        if (Get-Command -Name Write-AppLog -ErrorAction SilentlyContinue) {
            Write-AppLog -Message $msg -Level Warning -EventId $script:Evt.SectionWarn
        }
    }
}

function Clear-AllEventLogs {
    # Clears all event logs if -ForceClearEventLogs is specified
    if (-not $ForceClearEventLogs) {
        Write-AppLog "Skipping event log clear (use -ForceClearEventLogs to enable)" 'Warning'
        return
    }
    Get-EventLog -List | ForEach-Object { Clear-EventLog $_.Log }
}

function Create-RestorePoint {
    # Creates a system restore point (requires admin)
    powershell.exe -ExecutionPolicy Bypass -Command "Checkpoint-Computer -Description 'Weekly' -RestorePointType 'MODIFY_SETTINGS'"
}

# --- Main ---
Ensure-Admin
Ensure-EventSource
clear-host
Set-WindowTitle "System Maintenance Starting"
Write-AppLog "System Maintenance Starting" 'Information'
Invoke-Step "Calendar & Wi-Fi" { Show-Calendar; Connect-Wifi $WifiSSID $WifiProfileName $WifiInterface }
Invoke-Step "Synchronizing Clock" { Sync-Clock }
Invoke-Step "Create Restore Point" { Create-RestorePoint }
Invoke-Step "Defender Scan" { Defender-QuickScan }
Invoke-Step "Chocolatey Upgrade" { Upgrade-Choco }
Invoke-Step "Winget Upgrade" { Upgrade-Winget }
Invoke-Step "Windows Update" { Upgrade-PSWindowsUpdate }
Invoke-Step "WSL Update" { Update-WSL }
Invoke-Step "Disk Cleanup" { Run-CleanMgr }
Invoke-Step "Check Logs" { Show-RecentErrors }
Invoke-Step "System Info" { Show-SystemInfo }
Invoke-Step "Clear Event Logs" { Clear-AllEventLogs }

Set-WindowTitle "Maintenance Complete"
Write-AppLog "Maintenance Complete" 'Information'

#EOF - updateme.ps1
   

```

# Configuration - Put Windows 11 Full Context Menu back in Explorer and Disable Web Searching

With all apologies to the Windows team (who are AWESOME), I like having the full menu available when  I right-click an item in the File Explorer in Windows. Again, do this at your own risk.

**[Back up your registry if you try this on a test system! You should be doing that anyway. Click here to learn more.](https://support.microsoft.com/en-us/topic/how-to-back-up-and-restore-the-registry-in-windows-855140ad-e318-2a13-2829-d428a2ab0692)**

The line after that adds a registry key to use only local search results, dramatically speeding up the Search function. 
<pre>
reg.exe add "HKCU\Software\Classes\CLSID\{86ca1aa0-34aa-4e8b-a509-50c905bae2a2}\InprocServer32" /f /ve
New-Item -Path "Registry::HKEY_CURRENT_USER\Software\Policies\Microsoft\Windows\Explorer"
New-ItemProperty -Path "HKCU:\Software\Policies\Microsoft\Windows\Explorer" -Name "Enabled" -Value "1" -PropertyType DWord
</pre>


## So what's your deal?

Like these? Am I doing something wrong or that I could do better? Hit me up in the "Issues" tab there at the top of the page. Be complete, not just "You're wrong". :) 
