"""
Builds a LEARNER EDITION of the workshop: the same modules, data, and tools, with the answers removed.

Why: the "Instructor notes" blocks in every module, and the facilitator folder, contain full answer keys.
On a public repository, anyone can read them. Publish the learner edition publicly and keep this full
version private (or on a private branch) for teaching.

Usage:   python3 tools/make_learner_edition.py OUTPUT_FOLDER

What it leaves out:
  - the facilitator folder (answer keys, design notes, link and deployment notes)
  - every collapsed "Instructor notes" block in the modules
  - the scripts that generate the data and the answer key, and the maintenance scripts

What stays: modules, data, chart images, the data workbench, and the activity "reveal" blocks that give
learners feedback on their own answers (those are part of the learning design).

It then checks that every local link and image in the learner edition still works.
"""
import os
import re
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

EXCLUDE_DIRS = {"facilitator", "__pycache__", "venv", ".git"}
EXCLUDE_FILES = {
    os.path.join("case-data", "build_case_data.py"),
    os.path.join("case-data", "make_images.py"),
    os.path.join("case-data", "adventure-works", "build_aw_extract.py"),
    os.path.join("tools", "predeploy_check.py"),
    os.path.join("tools", "check_links.py"),
    os.path.join("tools", "localize_icons.py"),
    os.path.join("tools", "make_learner_edition.py"),
    os.path.join("tools", "data-workbench", "working_copy.sqlite"),
}
INSTRUCTOR_BLOCK = re.compile(r"<details>\s*<summary><b>Instructor notes</b></summary>.*?</details>\s*", re.S)

# (file, exact text to remove or replace, replacement). Each must be found, or the script warns.
PATCHES = [
    ("modules/00-start-here.md",
     "If you're teaching this, look for the collapsed \"Instructor notes\" at the end of each module. They hold timing, a talk track, and the answer key.\n\n", ""),
    ("case-data/README.md",
     "The answer keys live in the separate `facilitator` folder. Keep that folder out of the learners' copy.\n\n", ""),
    ("case-data/README.md",
     "| `build_case_data.py` and `make_images.py` | Optional. Rebuild the data and the chart images (seeded, and identical on the same numpy version) | Instructors |\n", ""),
    ("README.md", "| `facilitator/` | Answer keys and design notes for instructors. Keep this folder out of the learners' copy |\n", ""),
    ("README.md", "| `tools/*.py` | Maintenance scripts: a pre-deployment check, a link checker, an icon localizer, and a learner-edition builder |\n", ""),
    ("README.md", ", an optional Adventure Works extract, and the scripts that rebuild it all |", ", and an optional Adventure Works extract |"),
]
PARAGRAPH_PATCHES = [  # remove whole paragraphs that start with this text
    ("case-data/README.md", "**Rebuilding the data (instructors).**"),
    ("case-data/adventure-works/README.md", "Instructors can rebuild everything"),
]


def copy_tree(out):
    for folder, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        rel_folder = os.path.relpath(folder, ROOT)
        for name in files:
            rel = os.path.normpath(os.path.join(rel_folder, name))
            if rel in EXCLUDE_FILES:
                continue
            dest = os.path.join(out, rel)
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            shutil.copy2(os.path.join(folder, name), dest)


def read(path):
    with open(path, encoding="utf-8", newline="") as f:
        return f.read()


def write(path, text):
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    out = os.path.abspath(sys.argv[1])
    if os.path.exists(out) and os.listdir(out):
        print("The output folder must be empty or not exist yet:", out)
        return 2
    os.makedirs(out, exist_ok=True)
    copy_tree(out)

    removed = 0
    for folder, _, files in os.walk(os.path.join(out, "modules")):
        for name in files:
            if name.endswith(".md"):
                path = os.path.join(folder, name)
                text = read(path)
                new, n = INSTRUCTOR_BLOCK.subn("", text)
                removed += n
                if n:
                    write(path, new)
    print("Removed %d Instructor notes blocks." % removed)

    warnings = []
    for rel, old, new in PATCHES:
        path = os.path.join(out, rel)
        text = read(path)
        if old not in text:
            warnings.append("patch text not found in %s: %r" % (rel, old[:60]))
            continue
        write(path, text.replace(old, new, 1))
    for rel, start in PARAGRAPH_PATCHES:
        path = os.path.join(out, rel)
        text = read(path)
        pattern = re.compile(r"(?:^|\n)" + re.escape(start) + r".*?(?:\n\n|\Z)", re.S)
        if not pattern.search(text):
            warnings.append("paragraph not found in %s: %r" % (rel, start))
            continue
        write(path, pattern.sub("\n", text, count=1).rstrip("\n") + "\n")

    leftovers = []
    broken = []
    for folder, _, files in os.walk(out):
        for name in files:
            if not name.endswith(".md"):
                continue
            path = os.path.join(folder, name)
            text = read(path)
            rel = os.path.relpath(path, out)
            if "Instructor notes" in text or "facilitator" in text:
                leftovers.append(rel)
            for t in re.findall(r'(?:src|href)="((?!https?:|mailto:)[^"#]+)"', text) + re.findall(r"\]\(((?!https?:|mailto:)[^)#]+)\)", text):
                if not os.path.exists(os.path.normpath(os.path.join(folder, t))):
                    broken.append("%s -> %s" % (rel, t))
    for w in warnings:
        print("WARNING:", w)
    for l in leftovers:
        print("WARNING: still mentions instructor material:", l)
    for b in broken:
        print("BROKEN LINK:", b)
    print("Learner edition written to", out)
    return 1 if (warnings or leftovers or broken) else 0


if __name__ == "__main__":
    sys.exit(main())
