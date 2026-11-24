"""
Optional: removes the workshop's dependency on icons hosted in the microsoft/sqlworkshops repository.

The modules show small icons (a pencil, a checkmark, an owl and so on) that are loaded from
    https://github.com/microsoft/sqlworkshops/blob/master/graphics/<name>.png?raw=true
This script copies those icons into graphics/icons/ in THIS repository and rewrites every markdown
file to point at the local copies, using a relative path that works from each file's own folder.

Usage (run from anywhere; needs Python 3.9 or later and an internet connection for the download):
    python3 tools/localize_icons.py --download     download the icons, then rewrite the links
    python3 tools/localize_icons.py                rewrite the links (icons must already be in graphics/icons)
    python3 tools/localize_icons.py --dry-run      show what would change, and change nothing

It is safe to run more than once. It will not rewrite anything if an icon is missing, so you never
end up with broken images.
"""
import os
import re
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ICON_DIR = os.path.join(ROOT, "graphics", "icons")
PATTERN = re.compile(r"https://github\.com/microsoft/sqlworkshops/blob/master/graphics/([A-Za-z0-9_]+\.png)\?raw=true")
RAW = "https://raw.githubusercontent.com/microsoft/sqlworkshops/master/graphics/%s"


def markdown_files():
    for folder, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in (".git", "venv", "__pycache__")]
        for name in files:
            if name.endswith(".md"):
                yield os.path.join(folder, name)


def main():
    download = "--download" in sys.argv
    dry = "--dry-run" in sys.argv
    found = {}
    for path in markdown_files():
        with open(path, encoding="utf-8") as f:
            text = f.read()
        names = set(PATTERN.findall(text))
        if names:
            found[path] = names
    icons = sorted({n for names in found.values() for n in names})
    if not icons:
        print("No hotlinked icons found. Nothing to do.")
        return 0
    print("Found %d distinct icons used in %d files." % (len(icons), len(found)))

    if download and not dry:
        os.makedirs(ICON_DIR, exist_ok=True)
        for name in icons:
            target = os.path.join(ICON_DIR, name)
            if os.path.exists(target):
                continue
            try:
                with urllib.request.urlopen(RAW % name, timeout=30) as r, open(target, "wb") as out:
                    out.write(r.read())
                print("downloaded", name)
            except Exception as e:  # network down, blocked, or the file moved
                print("could not download %s: %s" % (name, e))

    missing = [n for n in icons if not os.path.exists(os.path.join(ICON_DIR, n))]
    if missing and not dry:
        print("\nStopping without changing any file. Missing from graphics/icons: " + ", ".join(missing))
        print("Download them (run with --download, or save them by hand) and run this again.")
        return 1

    for path, names in sorted(found.items()):
        rel_dir = os.path.relpath(ICON_DIR, os.path.dirname(path)).replace(os.sep, "/")
        if dry:
            print("would rewrite %d icon links in %s" % (len(names), os.path.relpath(path, ROOT)))
            continue
        with open(path, encoding="utf-8") as f:
            text = f.read()
        text = PATTERN.sub(lambda m: "%s/%s" % (rel_dir, m.group(1)), text)
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(text)
    if not dry:
        print("\nDone. All icon links now point to graphics/icons/.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
