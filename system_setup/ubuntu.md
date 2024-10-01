
# Linux System Setup

These are a few of the scripts, commands, and other environment settings I use on my Linux systems. I'm currently running Ubuntu Dev release, which is working well with these settings. Some of these commands won't run properly unless you are in "sudo" or "su" level, so be aware of that.

This is for info and examples **only**. I explain a few things here, but if *anything* is a new term or command, highlight it and look it up. Understand what your are doing if you want to try this - and you're on your own here - test first, don't run this in production first! 

### Disclaimer, for people who need to be told this sort of thing: 

*Never trust any script, presentation, code or information including those that you find here, until you understand exactly what it does and how it will act on your systems. Always check scripts and code on a test system or Virtual Machine, not a production system. Yes, there are always multiple ways to do things, and this script, code, information, or content may not work in every situation, for everything. It’s just an example, people. All scripts on this site are performed by a professional stunt driver on a closed course. Your mileage may vary. Void where prohibited. Offer good for a limited time only. Keep out of reach of small children. Do not operate heavy machinery while using this script. If you experience blurry vision, indigestion or diarrhea during the operation of this script, see a physician immediately*

If you want to suggest something here, add an [Issue](https://docs.github.com/en/issues/tracking-your-work-with-issues/creating-an-issue) referencing this page and what you want to mention. If I like it, I'll put it here. I'll not close the Issue unless it's a bug you've found, that way you can see what other people do that I didn't include. 

# Install localpurge 

<pre> 
sudo apt-get install localepurge 
</pre>

# Update Ubuntu
As I mentioned, I run a complete update script to keep my system up to date and secure. I also do things like making sure the time is sync'd first (super important), find out the drive space, do some cleanup, and show my network status. 

> This is the most dangerouse of the scripts, don't run this on your test system without understanding everything it does. Completely. You are on your own here.

<pre> 
#!/bin/bash

clear

# Detailed Logging and Versioning
script_version="2.0"  # Increment this when making changes
log_file="/var/log/maintain_ubuntu.log"
log_message() {
    local timestamp=$(date +"%Y-%m-%d %H:%M:%S")
    local level="$1"  # INFO, WARNING, ERROR
    shift
    echo "[$timestamp] [$level] [v$script_version] $*" | tee -a "$log_file"
}

# On systems where I stream my Calibre Library, I have to do a bit of maintenance here...
# echo -e "\e[31;43m***** CLEAN AND START CALIBRE *****\e[0m"
# rm /mymedia/calibre/delete.log
# calibre-server --daemonize /mymedia/calibre --log /mymedia/calibre/delete.log --enable-local-write /mymedia/calibre
# echo ""

# -Hostname information:
echo -e "\e[31;43m***** Hostname *****\e[0m"
hostnamectl
echo ""

echo -e "\e[31;43m***** Check Evening Shutdown from Cron Job *****\e[0m"
cat ./evening.log
echo ""

echo -e "\e[31;43m***** Start Containers *****\e[0m"
~/scripts/containerstart.sh
echo ""

echo -e "\e[31;43m***** Clean Packages *****\e[0m"
sudo apt autoremove --purge -y
sudo apt clean
sudo rm -rf ~/.cache/thumbnails/*
sudo deborphan | xargs sudo apt-get -y remove --purge
sudo journalctl --vacuum-time=1d
echo ""

echo -e "\e[31;43m***** Update Packages *****\e[0m"
log_message "INFO" "Upgrading packages"
sudo apt update
echo ""

echo -e "\e[31;43m***** Upgrade Packages *****\e[0m"
sudo apt upgrade -y
echo ""

echo -e "\e[31;43m***** Release Upgrade *****\e[0m"
sudo do-release-upgrade
echo ""

# -File system disk space usage:
echo -e "\e[31;43m***** Disk Space *****\e[0m"
df -h
echo ""

# -Free and used memory in the system:
echo -e "\e[31;43m ***** Memory Space *****\e[0m"
free
echo ""

# -System uptime and load:
echo -e "\e[31;43m***** Uptime and Load *****\e[0m"
uptime

echo ""

# -Logged-in users:
echo -e "\e[31;43m***** Current Users *****\e[0m"
who
echo ""

# -Top 5 processes as far as memory usage is concerned
echo -e "\e[31;43m***** Top 5 Memory *****\e[0m"
ps -eo %mem,%cpu,comm --sort=-%mem | head -n 6
echo ""

echo -e "\e[31;43m***** Containers Status *****\e[0m"
~/scripts/containerstatus.sh
echo ""

echo -e "\e[1;32mMaintenance Complete.\e[0m"


</pre>
