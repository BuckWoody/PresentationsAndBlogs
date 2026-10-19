#!/usr/bin/env python3
"""
Governance Without the Gridlock: CDE scorecard demo (Live! 360 Orlando)

Zero cost, zero installs: Python 3.9+ standard library only (sqlite3, html).

What it shows, in about six minutes:
  1. A tiny critical data element (CDE) register: definition, owner, steward,
     custodian, and quality thresholds.
  2. Quality rules written as plain SQL, scored against the data.
  3. A "Cleared for use" check: a CDE earns the Certified badge only when it has
     a definition, three named people, and every rule inside its threshold.
  4. Three numbers for the whole program: Coverage, Trust, and Use.
       Coverage = CDEs with owner, steward, and custodian all named
       Trust    = CDEs whose rules are all inside threshold
       Use      = analytics and AI use cases that rely only on certified CDEs

Run it twice:
    python governance_scorecard_demo.py               # messy data, mostly red
    python governance_scorecard_demo.py --remediated  # after cleanup and naming a steward

Open scorecard.html in a browser afterward. By default it loads Bootstrap from a
CDN. For offline use, save bootstrap.min.css in the same folder as this script
and the page will use that local copy automatically.
"""
import argparse
import html
import os
import random
import sqlite3
from datetime import date, timedelta

# ---------------------------------------------------------------------------
# 1. The CDE register. In real life this lives in a catalog (Purview, OpenMetadata)
#    or a governed list. Here it is plain Python so the room can read it.
# ---------------------------------------------------------------------------
CDE_REGISTER = [
    {
        "cde": "Customer Email",
        "definition": "Primary email address used to contact the customer.",
        "domain": "Sales",
        "owner": "VP of Sales",
        "steward": "Dana (Sales Ops)",
        "custodian": "Raj (BI Team)",
        "rules": [
            # (rule name, SQL that counts rows that PASS, threshold percent)
            ("Completeness", "SELECT COUNT(*) FROM customers WHERE email IS NOT NULL AND TRIM(email) <> ''", 98.0),
            ("Validity", "SELECT COUNT(*) FROM customers WHERE email LIKE '_%@_%._%' AND email NOT LIKE '% %'", 97.0),
            ("Uniqueness", "SELECT COUNT(*) FROM (SELECT email FROM customers WHERE email IS NOT NULL GROUP BY LOWER(email) HAVING COUNT(*) = 1)", 99.0),
        ],
    },
    {
        "cde": "Customer State",
        "definition": "Two-letter US state code of the billing address.",
        "domain": "Finance",
        "owner": "CFO",
        "steward": "Priya (Billing)",
        "custodian": "Raj (BI Team)",
        "rules": [
            ("Validity", "SELECT COUNT(*) FROM customers WHERE state IN ('WA','OR','CA','TX','FL','NY','IL','OH','GA','CO')", 99.0),
        ],
    },
    {
        "cde": "Signup Date",
        "definition": "Date the customer account was created. Cannot be in the future.",
        "domain": "Sales",
        "owner": "VP of Sales",
        "steward": "",  # deliberately empty: no steward, no badge
        "custodian": "Raj (BI Team)",
        "rules": [
            ("Timeliness", "SELECT COUNT(*) FROM customers WHERE signup_date <= DATE('now')", 100.0),
        ],
    },
]

# Analytics and AI use cases, each listing the CDEs it depends on.
USE_CASES = [
    ("Weekly campaign email", ["Customer Email"]),
    ("Churn prediction model", ["Customer Email", "Signup Date"]),
    ("Billing tax run", ["Customer State"]),
]


# ---------------------------------------------------------------------------
# 2. Sample data with seeded defects (or the remediated version).
# ---------------------------------------------------------------------------
def build_database(remediated: bool, rows: int = 500) -> sqlite3.Connection:
    random.seed(42)
    con = sqlite3.connect(":memory:")
    con.execute("CREATE TABLE customers (customer_id INTEGER, email TEXT, state TEXT, signup_date TEXT)")
    states = ["WA", "OR", "CA", "TX", "FL", "NY", "IL", "OH", "GA", "CO"]
    for i in range(1, rows + 1):
        email = f"user{i}@example.com"
        state = random.choice(states)
        signup = (date.today() - timedelta(days=random.randint(1, 1500))).isoformat()
        if not remediated:
            roll = random.random()
            if roll < 0.06:
                email = None                        # missing email
            elif roll < 0.11:
                email = f"user{i}example.com"       # no @ sign
            elif roll < 0.15:
                email = f"user{i - 1}@example.com"  # duplicate of the prior row
            if random.random() < 0.04:
                state = random.choice(["Wash.", "ca", "XX", "Texas"])  # nonstandard codes
            if random.random() < 0.02:
                signup = (date.today() + timedelta(days=random.randint(5, 90))).isoformat()
        con.execute("INSERT INTO customers VALUES (?,?,?,?)", (i, email, state, signup))
    return con


# ---------------------------------------------------------------------------
# 3. Score every rule, decide the badge, then roll up Coverage, Trust, and Use.
# ---------------------------------------------------------------------------
def score(con: sqlite3.Connection):
    total = con.execute("SELECT COUNT(*) FROM customers").fetchone()[0]
    results = []
    for cde in CDE_REGISTER:
        rule_rows, all_pass = [], True
        for name, sql, threshold in cde["rules"]:
            passed = con.execute(sql).fetchone()[0]
            pct = round(100.0 * passed / total, 1)
            ok = pct >= threshold
            all_pass &= ok
            rule_rows.append({"rule": name, "pct": pct, "threshold": threshold, "ok": ok})
        results.append({**cde, "rule_rows": rule_rows, "all_pass": all_pass})
    finalize(results)
    return total, results


def finalize(results):
    """Badge logic lives here so the demo can rerun it after naming a steward."""
    for r in results:
        r["has_people"] = bool(r["owner"] and r["steward"] and r["custodian"])
        r["certified"] = r["all_pass"] and r["has_people"] and bool(r["definition"])
        if not r["has_people"]:
            r["reason"] = "Missing an accountable person"
        elif not r["all_pass"]:
            r["reason"] = "Below quality threshold"
        else:
            r["reason"] = ""


def rollup(results):
    n = len(results)
    certified = {r["cde"] for r in results if r["certified"]}
    coverage = round(100 * sum(r["has_people"] for r in results) / n)
    trust = round(100 * sum(r["all_pass"] for r in results) / n)
    safe = [u for u, deps in USE_CASES if all(d in certified for d in deps)]
    use = round(100 * len(safe) / len(USE_CASES))
    return {"coverage": coverage, "trust": trust, "use": use, "safe": safe}


# ---------------------------------------------------------------------------
# 4. Output: console first (works offline), then an HTML scorecard.
# ---------------------------------------------------------------------------
def print_console(total, results, summary):
    print(f"\nCDE Scorecard ({total} customer rows)\n" + "=" * 66)
    for r in results:
        badge = "CERTIFIED" if r["certified"] else f"NOT CERTIFIED ({r['reason']})"
        print(f"\n{r['cde']}  [{r['domain']}]  {badge}")
        print(f"  Owner: {r['owner'] or 'NONE'} | Steward: {r['steward'] or 'NONE'}"
              f" | Custodian: {r['custodian'] or 'NONE'}")
        for rr in r["rule_rows"]:
            mark = "PASS" if rr["ok"] else "FAIL"
            print(f"  {mark}  {rr['rule']:<13} {rr['pct']:>5}%  (threshold {rr['threshold']}%)")
    print("\n" + "=" * 66)
    print(f"Coverage {summary['coverage']}%   Trust {summary['trust']}%   Use {summary['use']}%")
    safe = ", ".join(summary["safe"]) or "none"
    print(f"Use cases cleared to run on certified data: {safe}\n")


CDN_CSS = "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"


def write_html(total, results, summary, path="scorecard.html"):
    e = html.escape
    css_href = "bootstrap.min.css" if os.path.exists("bootstrap.min.css") else CDN_CSS

    def tile(label, value, hint):
        tone = "success" if value >= 80 else ("warning" if value >= 50 else "danger")
        return (f"<div class='col-md-4'><div class='card text-center border-{tone}'><div class='card-body'>"
                f"<div class='display-5 text-{tone}'>{value}%</div><div class='fw-bold'>{label}</div>"
                f"<div class='small text-muted'>{hint}</div></div></div></div>")

    tiles = (tile("Coverage", summary["coverage"], "CDEs with owner, steward, and custodian named")
             + tile("Trust", summary["trust"], "CDEs inside every quality threshold")
             + tile("Use", summary["use"], "Use cases running only on certified CDEs"))
    cards = []
    for r in results:
        color = "success" if r["certified"] else "danger"
        badge = "Certified" if r["certified"] else f"Not certified: {e(r['reason'])}"
        rows = "".join(
            f"<tr><td>{e(rr['rule'])}</td><td>{rr['pct']}%</td><td>{rr['threshold']}%</td>"
            f"<td><span class='badge text-bg-{'success' if rr['ok'] else 'danger'}'>{'Pass' if rr['ok'] else 'Fail'}</span></td></tr>"
            for rr in r["rule_rows"]
        )
        cards.append(f"""
        <div class="col-md-4"><div class="card h-100 border-{color}">
          <div class="card-header d-flex justify-content-between align-items-center">
            <strong>{e(r['cde'])}</strong><span class="badge text-bg-{color}">{badge}</span></div>
          <div class="card-body">
            <p class="small text-muted">{e(r['definition'])}</p>
            <ul class="list-unstyled small">
              <li><strong>Domain:</strong> {e(r['domain'])}</li>
              <li><strong>Owner:</strong> {e(r['owner'] or 'None assigned')}</li>
              <li><strong>Steward:</strong> {e(r['steward'] or 'None assigned')}</li>
              <li><strong>Custodian:</strong> {e(r['custodian'] or 'None assigned')}</li>
            </ul>
            <table class="table table-sm"><thead><tr><th>Rule</th><th>Score</th><th>Target</th><th></th></tr></thead>
            <tbody>{rows}</tbody></table>
          </div></div></div>""")
    page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>CDE Scorecard</title>
<link href="{css_href}" rel="stylesheet"></head>
<body class="bg-white"><div class="container py-4">
<h1 class="h3">Critical Data Element Scorecard</h1>
<p class="text-muted">{total} customer rows scored.</p>
<div class="row g-3 mb-4">{tiles}</div>
<div class="row g-3">{''.join(cards)}</div></div></body></html>"""
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(page)
    print(f"Wrote {path}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--remediated", action="store_true", help="score the cleaned-up data")
    args = ap.parse_args()
    con = build_database(args.remediated)
    total, results = score(con)
    if args.remediated:
        # The other half of the fix: a named person. Rerun the badge logic.
        for r in results:
            if not r["steward"]:
                r["steward"] = "Marcus (Sales Ops)"
        finalize(results)
    summary = rollup(results)
    print_console(total, results, summary)
    write_html(total, results, summary)