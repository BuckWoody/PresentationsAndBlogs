# Install Choco from PowerShell
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Install PSWindowsUpdate
Set-ExecutionPolicy -ExecutionPolicy Unrestricted
Install-Module -Name PSWindowsUpdate -Force
Add-WUServiceManager -ServiceID 7971f918-a847-4430-9279-4a52d1efe18d

# Put Windows 11 Full Context Menu back in Explorer
reg.exe add "HKCU\Software\Classes\CLSID\{86ca1aa0-34aa-4e8b-a509-50c905bae2a2}\InprocServer32" /f /ve

Start Plex Server:
start "C:\Program Files\Plex\Plex Media Server\Plex Media Server.exe"


# Configure Powershell Environment

<pre> notepad $profile </pre>

Then enter: 

<pre>
function prompt {

    $host.ui.RawUI.WindowTitle = "Current Folder: $pwd"
    $CmdPromptUser = [Security.Principal.WindowsIdentity]::GetCurrent();
    $IsAdmin = (New-Object Security.Principal.WindowsPrincipal ([Security.Principal.WindowsIdentity]::GetCurrent())).IsInRole([Security.Principal.WindowsBuiltinRole]::Administrator)

    Write-Host ""
    Write-Host "`u{1F9D9} $($CmdPromptUser.Name.split("\")[1]) " -ForegroundColor Green -NoNewline
    Write-host ($(if ($IsAdmin) { '(as admin) ' } else { '' })) -ForegroundColor Red -NoNewLine
    Write-Host "on `u{1F4BB}" $env:COMPUTERNAME"."$env:USERDNSDOMAIN

    Write-Host "`u{1F4C1} $pwd"  -ForegroundColor Yellow ``
    return "`u{25B6} "
} 
</pre>

# Update Windows from Command Line 
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

Get-Volume

