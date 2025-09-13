
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
As I mentioned, I run a complete update script to keep my system up to date and secure. Some of these might require an apt install, so examine them line by line to see what you want to scrape from here.  

> This is the most dangerouse of the scripts, don't run this on your test system without understanding everything it does. Completely. You are on your own here.

```bash

#!/usr/bin/env bash
#------------------------------------------------------------------------------
# Ubuntu Maintenance Utility
#------------------------------------------------------------------------------

set -Eeuo pipefail
IFS=$'\n\t'

#------------------------------------------------------------------------------
# Metadata
#------------------------------------------------------------------------------
SCRIPT_NAME="${0##*/}"
SCRIPT_VERSION="2025.9.13"   # non-fatal apt + optional old-releases auto-fix + fd-lock release

#------------------------------------------------------------------------------
# Defaults (overridable via CLI)
# Enter Your Path for Logging
#------------------------------------------------------------------------------
LOG_FILE="${LOG_FILE:-/home/username/logs/maintain_ubuntu.log}"
VACUUM_DAYS="${VACUUM_DAYS:-1}"     # systemd journal retention in days
USE_COLOR="${USE_COLOR:-1}"
CLEAR_SCREEN="${CLEAR_SCREEN:-1}"
DRY_RUN="${DRY_RUN:-0}"
APT_OLD_RELEASES_FIX="${APT_OLD_RELEASES_FIX:-0}"  # --apt-old-releases flag

# Logging levels
LOG_LEVEL_DEBUG=10
LOG_LEVEL_INFO=20
LOG_LEVEL_WARN=30
LOG_LEVEL_ERROR=40
LOG_LEVEL_THRESHOLD="${LOG_LEVEL_THRESHOLD:-$LOG_LEVEL_INFO}"

# Locking
LOCKFILE="/tmp/${SCRIPT_NAME}.lock"
LOCK_FD=9

# sudo helper
if [[ ${EUID} -ne 0 ]]; then
  SUDO="sudo"
else
  SUDO=""
fi

#------------------------------------------------------------------------------
# Colors (console only)
#------------------------------------------------------------------------------
supports_color() { [[ -t 1 && "${USE_COLOR}" -eq 1 ]]; }
if supports_color; then
  CLR_RESET="\e[0m"; CLR_DIM="\e[2m"; CLR_BOLD="\e[1m"
  CLR_INFO="\e[38;5;33m"; CLR_WARN="\e[38;5;214m"; CLR_ERROR="\e[38;5;196m"; CLR_DEBUG="\e[38;5;244m"
  CLR_TITLE_BG="\e[43;31m"
else
  CLR_RESET=""; CLR_DIM=""; CLR_BOLD=""; CLR_INFO=""; CLR_WARN=""; CLR_ERROR=""; CLR_DEBUG=""; CLR_TITLE_BG=""
fi

#------------------------------------------------------------------------------
# Utilities
#------------------------------------------------------------------------------
usage() {
  cat <<'USAGE'
Ubuntu maintenance utility

Usage:
  maintain_ubuntu.sh [options]

Options:
  -v, --verbose            Increase verbosity to DEBUG
  -q, --quiet              Reduce verbosity to WARN+
  -n, --dry-run            Show actions without making changes
      --no-color           Disable colored console output
      --no-clear           Do not clear the terminal at start
      --log-file PATH      Set log file (default: /home/buck/logs/maintain_ubuntu.log)
      --vacuum-days N      systemd-journal retention in days (default: 1)
      --apt-old-releases   (Optional) Repoint EOL Ubuntu repos to old-releases and comment '-proposed/-backports'
  -h, --help               Show this help and exit
  -V, --version            Show version and exit

Examples:
  sudo ./maintain_ubuntu.sh
  ./maintain_ubuntu.sh -v --log-file "$HOME/logs/maintain_ubuntu.log" --vacuum-days 3
  sudo ./maintain_ubuntu.sh --apt-old-releases
USAGE
}

version() { echo "${SCRIPT_NAME} v${SCRIPT_VERSION}"; }

ensure_dir() {
  local dir="$1"
  [[ -d "$dir" ]] || mkdir -p "$dir"
}

rotate_log_if_needed() {
  local max_size=$((5 * 1024 * 1024)) # 5MB
  if [[ -f "$LOG_FILE" ]]; then
    local size
    size=$(stat -c %s "$LOG_FILE" 2>/dev/null || echo 0)
    if (( size > max_size )); then
      local ts
      ts=$(date +"%Y%m%d_%H%M%S")
      mv -- "$LOG_FILE" "${LOG_FILE}.${ts}.old" || true
    fi
  fi
}

level_to_num() {
  case "${1^^}" in
    DEBUG) echo "$LOG_LEVEL_DEBUG" ;;
    INFO)  echo "$LOG_LEVEL_INFO" ;;
    WARN|WARNING) echo "$LOG_LEVEL_WARN" ;;
    ERROR) echo "$LOG_LEVEL_ERROR" ;;
    *)     echo "$LOG_LEVEL_INFO" ;;
  esac
}

log() {
  local level="${1:-INFO}"; shift || true
  local msg="${*:-}"
  local ts lvl_num line color
  ts=$(date +"%Y-%m-%d %H:%M:%S")
  lvl_num="$(level_to_num "$level")"
  if (( lvl_num < LOG_LEVEL_THRESHOLD )); then return 0; fi
  line="[${ts}] [${level}] v${SCRIPT_VERSION} | ${msg}"
  printf "%s\n" "$line" >> "$LOG_FILE"
  case "${level^^}" in
    DEBUG) color="$CLR_DEBUG" ;; INFO) color="$CLR_INFO" ;;
    WARN|WARNING) color="$CLR_WARN" ;; ERROR) color="$CLR_ERROR" ;;
    *) color="" ;;
  esac
  printf "%b%s%b\n" "$color" "$line" "$CLR_RESET"
}

title() { printf "%b%s%b\n" "$CLR_TITLE_BG" "========== $1 ==========" "$CLR_RESET"; }
section() { title "$1"; log INFO "---- $1 ----"; }
die() { log ERROR "$*"; exit 1; }
require_cmd() { command -v "$1" >/dev/null 2>&1 || die "Required command not found: $1"; }
cmd_exists() { command -v "$1" >/dev/null 2>&1; }

# Execute commands with timing/logging & optional dry-run
run() {
  local desc="$1"; shift
  log INFO "$desc"
  if (( DRY_RUN )); then
    log DEBUG "dry-run: $*"
    printf "%b[DRY-RUN]%b %s\n" "$CLR_DIM" "$CLR_RESET" "$*"
    return 0
  fi
  local start end dur rc
  start=$(date +%s)
  if "$@"; then rc=0; else rc=$?; fi
  end=$(date +%s); dur=$(( end - start ))
  if (( rc == 0 )); then
    log INFO "${desc} [ok] (${dur}s)"
  else
    log ERROR "${desc} [rc=${rc}] (${dur}s)"
  fi
  return "$rc"
}

# Non-fatal wrapper: never propagates non-zero (so set -e won't exit)
run_nonfatal() {
  local desc="$1"; shift
  if run "$desc" "$@"; then
    return 0
  else
    log WARN "${desc} failed but continuing"
    return 0
  fi
}

#------------------------------------------------------------------------------
# Locking (FD-based; fixed release via closing FD)
#------------------------------------------------------------------------------
acquire_lock() {
  require_cmd flock
  exec {LOCK_FD}>"$LOCKFILE"
  if ! flock -n "$LOCK_FD"; then
    die "Another instance is already running. Lock: $LOCKFILE"
  fi
  log DEBUG "Acquired lock (fd=${LOCK_FD}, file=${LOCKFILE})"
}

release_lock() {
  if { true >&"$LOCK_FD"; } 2>/dev/null; then
    exec {LOCK_FD}>&- || true
    log DEBUG "Released lock FD"
  fi
  rm -f -- "$LOCKFILE" 2>/dev/null || true
}

cleanup() {
  local rc=$?
  release_lock
  if (( rc != 0 )); then
    log ERROR "Script terminated with errors (rc=${rc})"
  else
    log INFO "Script completed successfully"
  fi
  exit "$rc"
}

trap cleanup EXIT
trap 'log ERROR "Interrupted (SIGINT/SIGTERM)"; exit 130' INT TERM

#------------------------------------------------------------------------------
# APT sources auto-fix for EOL releases (optional)
#------------------------------------------------------------------------------
apt_switch_to_old_releases() {
  local ts target
  ts=$(date +"%Y%m%d_%H%M%S")
  target="http://old-releases.ubuntu.com/ubuntu"

  log INFO "Attempting to repoint APT sources to old-releases (backup kept with .bak.${ts})"
  local files=(/etc/apt/sources.list /etc/apt/sources.list.d/*.list)
  for f in "${files[@]}"; do
    [[ -f "$f" ]] || continue
    run_nonfatal "Backup $f" ${SUDO} cp -a "$f" "$f.bak.${ts}"
    # Replace archive URLs with old-releases
    run_nonfatal "Repoint $f to old-releases" \
      ${SUDO} sed -i -E 's#https?://[^[:space:]]*ubuntu\.com/ubuntu#'"$target"'#g' "$f"
    # Comment out -proposed and -backports lines
    run_nonfatal "Comment -proposed/-backports in $f" \
      ${SUDO} sed -i -E 's#^([[:space:]]*deb([[:space:]].*)?(proposed|backports)([[:space:]].*)?)#\# \1#g' "$f"
  done
}

#------------------------------------------------------------------------------
# Steps
#------------------------------------------------------------------------------
step_hostname() {
  section "Hostname & System"
  run_nonfatal "Show hostname and system info" hostnamectl
}

step_clean_packages() {
  section "Clean Packages"
  run_nonfatal "Autoremove unused packages" ${SUDO} apt-get autoremove --purge -y
  run_nonfatal "Clean apt caches"           ${SUDO} apt-get clean

  # Remove GNOME thumbnail cache for the invoking user (if sudo used)
  local user_home
  if [[ -n "${SUDO_USER:-}" ]]; then
    user_home="$(getent passwd "$SUDO_USER" | cut -d: -f6)"
  else
    user_home="${HOME:-$PWD}"
  fi
  if [[ -n "$user_home" && -d "$user_home/.cache/thumbnails" ]]; then
    run_nonfatal "Remove thumbnail cache for ${SUDO_USER:-$USER}" \
      ${SUDO:+sudo -u "$SUDO_USER"} bash -c "rm -rf '$user_home/.cache/thumbnails/'*"
  else
    log WARN "Thumbnail cache directory not found; skipping"
  fi

  # Optional: deborphan
  if cmd_exists deborphan; then
    run_nonfatal "Remove orphaned libraries (deborphan)" \
      bash -c 'deborphan | xargs -r sudo apt-get -y remove --purge'
  else
    log WARN "deborphan not installed; skipping orphan removal"
  fi

  # Journal vacuum
  if [[ "${VACUUM_DAYS}" =~ ^[0-9]+$ ]] && (( VACUUM_DAYS > 0 )); then
    run_nonfatal "Vacuum systemd journal to ${VACUUM_DAYS} day(s)" \
      ${SUDO} journalctl --vacuum-time="${VACUUM_DAYS}d"
  else
    log WARN "Invalid or zero VACUUM_DAYS='${VACUUM_DAYS}'; skipping journal vacuum"
  fi
}

step_update_packages() {
  section "Update Packages"
  if ! run "Update package index" ${SUDO} apt-get update; then
    log WARN "apt-get update failed (common on EOL releases like 'oracular'). Continuing."
    if (( APT_OLD_RELEASES_FIX )); then
      apt_switch_to_old_releases
      run_nonfatal "Retry package index update against old-releases" ${SUDO} apt-get update
    fi
  fi
}

step_upgrade_packages() {
  section "Upgrade Packages"
  # Upgrades can still fail if update was broken; keep non-fatal
  run_nonfatal "Upgrade installed packages" ${SUDO} apt-get -y upgrade
  # Optional, comment in if desired as a separate non-fatal:
  # run_nonfatal "Full upgrade (may install/remove packages)" ${SUDO} apt-get -y full-upgrade
}

step_disk_space() { section "Disk Space";  run_nonfatal "Show filesystem usage" df -h; }
step_memory()     {
  section "Memory"
  if free -h >/dev/null 2>&1; then run_nonfatal "Show memory usage" free -h
  else run_nonfatal "Show memory usage" free
  fi
}
step_uptime()     { section "Uptime & Load"; run_nonfatal "Show uptime and load averages" uptime; }
step_users()      { section "Current Users"; run_nonfatal "Show logged-in users" who; }
step_top_memory() { section "Top 5 Memory Consumers"; run_nonfatal "Show top 5 processes by memory" bash -c 'ps -eo %mem,%cpu,comm --sort=-%mem | head -n 6'; }

#------------------------------------------------------------------------------
# Argument parsing
#------------------------------------------------------------------------------
parse_args() {
  while [[ $# -gt 0 ]]; do
    case "$1" in
      -v|--verbose)        LOG_LEVEL_THRESHOLD=$LOG_LEVEL_DEBUG; shift ;;
      -q|--quiet)          LOG_LEVEL_THRESHOLD=$LOG_LEVEL_WARN; shift ;;
      -n|--dry-run)        DRY_RUN=1; shift ;;
      --no-color)          USE_COLOR=0; shift ;;
      --no-clear)          CLEAR_SCREEN=0; shift ;;
      --log-file)          [[ -n "${2:-}" ]] || die "--log-file requires a path"; LOG_FILE="$2"; shift 2 ;;
      --vacuum-days)       [[ -n "${2:-}" ]] || die "--vacuum-days requires a number"; VACUUM_DAYS="$2"; shift 2 ;;
      --apt-old-releases)  APT_OLD_RELEASES_FIX=1; shift ;;
      -h|--help)           usage; exit 0 ;;
      -V|--version)        version; exit 0 ;;
      --) shift; break ;;
      -*) die "Unknown option: $1" ;;
      *)  die "Unexpected argument: $1 (no positional args supported)" ;;
    esac
  done
}

#------------------------------------------------------------------------------
# Main
#------------------------------------------------------------------------------
main() {
  parse_args "$@"

  # Prepare logging
  umask 077
  ensure_dir "$(dirname -- "$LOG_FILE")"
  rotate_log_if_needed
  # (Append mode; no truncation)

  (( CLEAR_SCREEN )) && clear || true

  log INFO "Starting ${SCRIPT_NAME} v${SCRIPT_VERSION}"
  log DEBUG "LOG_FILE=${LOG_FILE}; VACUUM_DAYS=${VACUUM_DAYS}; DRY_RUN=${DRY_RUN}; USE_COLOR=${USE_COLOR}; APT_OLD_RELEASES_FIX=${APT_OLD_RELEASES_FIX}"

  # Acquire lock
  acquire_lock

  # Preconditions (commands presence)
  require_cmd hostnamectl
  require_cmd apt-get
  require_cmd df
  require_cmd free
  require_cmd uptime
  require_cmd who
  require_cmd ps
  require_cmd journalctl

  local total_start total_end total_dur
  total_start=$(date +%s)

  # Execute steps (all resilient)
  step_hostname
  step_clean_packages
  step_update_packages
  step_upgrade_packages
  step_disk_space
  step_memory
  step_uptime
  step_users
  step_top_memory

  total_end=$(date +%s)
  total_dur=$(( total_end - total_start ))

  printf "%b%s%b\n" "$CLR_BOLD" "✅ Maintenance Complete (with non-fatal handling) in ${total_dur}s." "$CLR_RESET"
  log INFO "Maintenance complete (non-fatal mode) in ${total_dur}s."
}

main "$@"

```
