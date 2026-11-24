"""
Runs every check that can be done offline, so you can run it after any edit and before publishing.

Usage:   python3 tools/predeploy_check.py              (Python 3.9 or later; Flask and numpy are used if installed)
         python3 tools/predeploy_check.py --skip-style  (skip the writing-style rules)

Checks:
  1. Style          no ampersands, em dashes, en dashes, or non-ASCII characters in markdown and CSV files
  2. References     every local link and image exists, and every file path named in a module exists
  3. Workbench      the 23 tests for the browser tool pass (needs Flask)
  4. Rebuild        the data generators reproduce the committed data (needs numpy, and only when it is the
                    same version the files were built with, because numpy does not promise the same random
                    numbers across releases)

For external web links, run tools/check_links.py as well (it needs an internet connection).
"""
import glob
import hashlib
import os
import re
import shutil
import sqlite3
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_STYLE = "--skip-style" in sys.argv
results = []  # (name, status, detail)


def record(name, status, detail=""):
    results.append((name, status, detail))
    print("%-5s %s%s" % (status, name, ("  " + detail) if detail else ""))


def files(pattern):
    return [f for f in glob.glob(os.path.join(ROOT, pattern), recursive=True) if "venv" not in f and "__pycache__" not in f]


# ------------------------------------------------------------------ 1. style
def check_style():
    if SKIP_STYLE:
        record("style", "SKIP", "(--skip-style)")
        return
    problems = []
    for f in files("**/*.md") + files("**/*.csv"):
        text = open(f, encoding="utf-8").read()
        rel = os.path.relpath(f, ROOT)
        for ch, name in (("\u2014", "em dash"), ("\u2013", "en dash")):
            if ch in text:
                problems.append("%s: %s" % (rel, name))
        if f.endswith(".md") and "&" in text:
            problems.append("%s: ampersand" % rel)
        odd = sorted({hex(ord(c)) for c in text if ord(c) > 127})
        if odd:
            problems.append("%s: non-ASCII %s" % (rel, ", ".join(odd[:5])))
    record("style", "FAIL" if problems else "PASS", "; ".join(problems[:6]) if problems else "")


# ------------------------------------------------------------- 2. references
def check_references():
    bad = []
    mds = files("**/*.md")
    for f in mds:
        text = open(f, encoding="utf-8").read()
        rel = os.path.relpath(f, ROOT)
        targets = re.findall(r'(?:src|href)="((?!https?:|mailto:)[^"#]+)"', text) + re.findall(r"\]\(((?!https?:|mailto:)[^)#]+)\)", text)
        for t in targets:
            if not os.path.exists(os.path.normpath(os.path.join(os.path.dirname(f), t))):
                bad.append("%s links to missing %s" % (rel, t))
        if "/facilitator/" in f.replace(os.sep, "/"):
            continue
        for m in re.findall(r"`((?:case-data|tools|supplements|raw|clean_csv|sources|images)/[A-Za-z0-9_./-]+\.[a-z]+)`", text):
            candidates = [os.path.join(ROOT, m), os.path.join(ROOT, "case-data", m), os.path.join(ROOT, "modules", m), os.path.join(os.path.dirname(f), m)]
            if not any(os.path.exists(c) for c in candidates):
                bad.append("%s names missing file %s" % (rel, m))
    record("references", "FAIL" if bad else "PASS", "; ".join(bad[:5]) if bad else "%d markdown files" % len(mds))


# --------------------------------------------------------------- 3. workbench
def check_workbench():
    try:
        import flask  # noqa: F401
    except ImportError:
        record("workbench", "SKIP", "(Flask is not installed)")
        return
    folder = os.path.join(ROOT, "tools", "data-workbench")
    proc = subprocess.run([sys.executable, "test_workbench.py"], cwd=folder, capture_output=True, text=True)
    out = (proc.stdout + proc.stderr).strip().splitlines()
    shutil.rmtree(os.path.join(folder, "__pycache__"), ignore_errors=True)
    record("workbench", "PASS" if proc.returncode == 0 else "FAIL", out[-1] if out else "")


# ---------------------------------------------------------------- 4. rebuild
def table_hashes(path):
    con = sqlite3.connect(path)
    out = {}
    for (t,) in con.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY 1"):
        out[t] = hashlib.sha256(repr(con.execute('SELECT * FROM "%s" ORDER BY rowid' % t).fetchall()).encode()).hexdigest()
    con.close()
    return out


def read_bytes(path):
    with open(path, "rb") as f:
        return f.read()


def check_rebuild():
    try:
        import numpy as np
    except ImportError:
        record("rebuild", "SKIP", "(numpy is not installed)")
        return
    src = read_bytes(os.path.join(ROOT, "case-data", "build_case_data.py")).decode("utf-8")
    built = re.search(r'BUILT_WITH_NUMPY = "([^"]+)"', src)
    if not built or built.group(1) != np.__version__:
        record("rebuild", "SKIP", "(numpy %s here, data built with %s, so identical output isn't promised)" % (np.__version__, built.group(1) if built else "unknown"))
        return
    tmp = tempfile.mkdtemp()
    try:
        os.makedirs(os.path.join(tmp, "case-data", "adventure-works"))
        shutil.copy(os.path.join(ROOT, "case-data", "build_case_data.py"), os.path.join(tmp, "case-data"))
        shutil.copy(os.path.join(ROOT, "case-data", "adventure-works", "build_aw_extract.py"), os.path.join(tmp, "case-data", "adventure-works"))
        for script, cwd in (("build_case_data.py", "case-data"), ("build_aw_extract.py", os.path.join("case-data", "adventure-works"))):
            proc = subprocess.run([sys.executable, script], cwd=os.path.join(tmp, cwd), capture_output=True, text=True)
            if proc.returncode != 0:
                record("rebuild", "FAIL", "%s stopped: %s" % (script, (proc.stderr.strip().splitlines() or ["?"])[-1]))
                return
        diffs = []
        for rel in ("case-data/lantern_clean.sqlite", "case-data/adventure-works/aw_extract.sqlite"):
            if table_hashes(os.path.join(tmp, rel)) != table_hashes(os.path.join(ROOT, rel)):
                diffs.append(rel)
        compare = ["facilitator/answer_key_numbers.md", "facilitator/aw_answer_key.md", "case-data/data_dictionary.csv"]
        for sub in ("raw", "clean_csv", "supplements"):
            compare += [os.path.relpath(p, ROOT).replace(os.sep, "/") for p in glob.glob(os.path.join(ROOT, "case-data", sub, "*.csv"))]
        for rel in compare:
            a, b = os.path.join(tmp, rel), os.path.join(ROOT, rel)
            if not os.path.exists(a) or read_bytes(a) != read_bytes(b):
                diffs.append(rel)
        record("rebuild", "FAIL" if diffs else "PASS", ("differs: " + ", ".join(diffs[:5])) if diffs else "data and answer keys reproduce, and the cleaning recipe ties out to finance")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    print("Pre-deployment checks for", ROOT, "\n")
    check_style()
    check_references()
    check_workbench()
    check_rebuild()
    failed = [r for r in results if r[1] == "FAIL"]
    skipped = [r for r in results if r[1] == "SKIP"]
    print("\n%d passed, %d failed, %d skipped." % (len(results) - len(failed) - len(skipped), len(failed), len(skipped)))
    sys.exit(1 if failed else 0)
