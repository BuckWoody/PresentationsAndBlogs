#!/usr/bin/env python3
"""
Governance Without the Gridlock: two-database demo (Live! 360 Orlando)

Zero cost, zero installs: Python 3.9+ standard library only.

THE POINT OF THE DEMO
  Two separate databases, just like a real estate:

    operational.db   The business data being governed (stand-in for your CRM,
                     warehouse, or lakehouse). The scanner opens it READ-ONLY.

    governance.db    The governance record (stand-in for Purview, OpenMetadata,
                     or a governed list): domains, critical data elements (CDEs),
                     owners, stewards, custodians, quality rules and thresholds,
                     use cases, every scan run, every result, and every issue.

  The scanner reads the first and writes only to the second. History builds up
  run after run, so you can show a trend, not just a snapshot.

COMMANDS (run in this order for the live demo)
  init              Create both databases (messy data, one CDE without a steward)
  register          Show the catalog: who is accountable for what, and the bars
  scan --label X    Score every rule, badge the CDEs, open or close issues
  fix-data          The steward and custodian clean the operational data
  assign-steward    Name the missing steward in the governance record
  history           Coverage, Trust, and Use for every run
  issues            Open issues (add --all to include closed ones)
  reset             Delete both databases and the HTML report

THREE NUMBERS
  Coverage = CDEs with owner, steward, and custodian all named
  Trust    = CDEs whose rules are all inside their thresholds
  Use      = analytics and AI use cases that rely only on certified CDEs

Each scan also writes scorecard.html. It uses Bootstrap from a CDN, or a local
bootstrap.min.css if you save one next to this script (handy when Wi-Fi is bad).
"""
import argparse
import html
import os
import random
import sqlite3
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

OPS_DB = "operational.db"
GOV_DB = "governance.db"
HTML_OUT = "scorecard.html"
CDN_CSS = "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
VALID_STATES = ["WA", "OR", "CA", "TX", "FL", "NY", "IL", "OH", "GA", "CO"]
STATE_LIST_SQL = ",".join(f"'{s}'" for s in VALID_STATES)
ROLES = ("owner", "steward", "custodian")

# ---------------------------------------------------------------------------
# Governance database schema. Think of this as a tiny catalog.
# ---------------------------------------------------------------------------
GOV_SCHEMA = """
CREATE TABLE domain (
    domain      TEXT PRIMARY KEY,
    owner_role  TEXT NOT NULL
);
CREATE TABLE cde (
    cde_id         INTEGER PRIMARY KEY,
    name           TEXT UNIQUE NOT NULL,
    definition     TEXT NOT NULL,
    domain         TEXT NOT NULL REFERENCES domain(domain),
    source_system  TEXT,
    source_table   TEXT,
    source_column  TEXT,
    classification TEXT
);
CREATE TABLE cde_role (
    cde_id      INTEGER NOT NULL REFERENCES cde(cde_id),
    role        TEXT NOT NULL CHECK (role IN ('owner','steward','custodian')),
    person      TEXT NOT NULL,
    assigned_on TEXT,
    PRIMARY KEY (cde_id, role)
);
CREATE TABLE dq_rule (
    rule_id          INTEGER PRIMARY KEY,
    cde_id           INTEGER NOT NULL REFERENCES cde(cde_id),
    dimension        TEXT NOT NULL,
    passing_rows_sql TEXT NOT NULL,
    threshold_pct    REAL NOT NULL
);
CREATE TABLE use_case (
    use_case_id INTEGER PRIMARY KEY,
    name        TEXT UNIQUE NOT NULL,
    kind        TEXT NOT NULL,
    risk_tier   TEXT NOT NULL
);
CREATE TABLE use_case_cde (
    use_case_id INTEGER NOT NULL REFERENCES use_case(use_case_id),
    cde_id      INTEGER NOT NULL REFERENCES cde(cde_id),
    PRIMARY KEY (use_case_id, cde_id)
);
CREATE TABLE scan_run (
    run_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    ran_at       TEXT NOT NULL,
    label        TEXT,
    source_db    TEXT NOT NULL,
    rows_scanned INTEGER NOT NULL,
    coverage_pct INTEGER,
    trust_pct    INTEGER,
    use_pct      INTEGER
);
CREATE TABLE scan_result (
    run_id        INTEGER NOT NULL REFERENCES scan_run(run_id),
    rule_id       INTEGER NOT NULL REFERENCES dq_rule(rule_id),
    passed_rows   INTEGER NOT NULL,
    total_rows    INTEGER NOT NULL,
    pct           REAL NOT NULL,
    threshold_pct REAL NOT NULL,
    status        TEXT NOT NULL,
    PRIMARY KEY (run_id, rule_id)
);
CREATE TABLE cde_status (
    run_id      INTEGER NOT NULL REFERENCES scan_run(run_id),
    cde_id      INTEGER NOT NULL REFERENCES cde(cde_id),
    has_people  INTEGER NOT NULL,
    all_pass    INTEGER NOT NULL,
    certified   INTEGER NOT NULL,
    reason      TEXT,
    PRIMARY KEY (run_id, cde_id)
);
CREATE TABLE issue (
    issue_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    issue_key   TEXT NOT NULL,
    cde_id      INTEGER NOT NULL REFERENCES cde(cde_id),
    description TEXT NOT NULL,
    assigned_to TEXT NOT NULL,
    opened_run  INTEGER NOT NULL,
    closed_run  INTEGER,
    status      TEXT NOT NULL
);
"""

# ---------------------------------------------------------------------------
# Seed content for the governance database (the register).
# ---------------------------------------------------------------------------
SEED_DOMAINS = [("Sales", "VP of Sales"), ("Finance", "CFO")]

# (cde_id, name, definition, domain, column, classification, owner, steward, custodian)
SEED_CDES = [
    (1, "Customer Email", "Primary email address used to contact the customer.",
     "Sales", "email", "Confidential", "VP of Sales", "Dana (Sales Ops)", "Raj (BI Team)"),
    (2, "Customer State", "Two-letter US state code of the billing address.",
     "Finance", "state", "Internal", "CFO", "Priya (Billing)", "Raj (BI Team)"),
    # Deliberately no steward: clean data still cannot earn the Certified badge.
    (3, "Signup Date", "Date the customer account was created. Cannot be in the future.",
     "Sales", "signup_date", "Internal", "VP of Sales", None, "Raj (BI Team)"),
]

# (cde_id, dimension, SQL that counts PASSING rows in operational.db, threshold percent)
SEED_RULES = [
    (1, "Completeness", "SELECT COUNT(*) FROM customers WHERE email IS NOT NULL AND TRIM(email) <> ''", 98.0),
    (1, "Validity", "SELECT COUNT(*) FROM customers WHERE email LIKE '_%@_%._%' AND email NOT LIKE '% %'", 97.0),
    (1, "Uniqueness", "SELECT COUNT(*) FROM (SELECT email FROM customers WHERE email IS NOT NULL GROUP BY LOWER(email) HAVING COUNT(*) = 1)", 99.0),
    (2, "Validity", f"SELECT COUNT(*) FROM customers WHERE state IN ({STATE_LIST_SQL})", 99.0),
    (3, "Timeliness", "SELECT COUNT(*) FROM customers WHERE signup_date <= DATE('now')", 100.0),
]

# (name, kind, risk tier, [CDE ids it depends on])
SEED_USE_CASES = [
    ("Weekly campaign email", "Analytics", "Medium", [1]),
    ("Churn prediction model", "AI", "Medium", [1, 3]),
    ("Billing tax run", "Analytics", "High", [2]),
]


# ---------------------------------------------------------------------------
# Connections
# ---------------------------------------------------------------------------
def open_gov():
    if not Path(GOV_DB).exists():
        sys.exit(f"{GOV_DB} not found. Run:  python governance_demo.py init")
    con = sqlite3.connect(GOV_DB)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys = ON")
    return con


def open_ops(read_only=True):
    if not Path(OPS_DB).exists():
        sys.exit(f"{OPS_DB} not found. Run:  python governance_demo.py init")
    if read_only:
        uri = Path(OPS_DB).resolve().as_uri() + "?mode=ro"
        return sqlite3.connect(uri, uri=True)
    return sqlite3.connect(OPS_DB)


# ---------------------------------------------------------------------------
# init: build both databases
# ---------------------------------------------------------------------------
def build_operational(rows=500):
    random.seed(42)  # same messy data every run
    con = sqlite3.connect(OPS_DB)
    con.execute("CREATE TABLE customers (customer_id INTEGER PRIMARY KEY, email TEXT, state TEXT, signup_date TEXT)")
    for i in range(1, rows + 1):
        email = f"user{i}@example.com"
        state = random.choice(VALID_STATES)
        signup = (date.today() - timedelta(days=random.randint(1, 1500))).isoformat()
        roll = random.random()
        if roll < 0.06:
            email = None                          # missing
        elif roll < 0.11:
            email = f"user{i}example.com"         # no @ sign
        elif roll < 0.15:
            email = f"user{i - 1}@example.com"    # duplicate of the prior row
        if random.random() < 0.04:
            state = random.choice(["Wash.", "ca", "XX", "Texas"])   # nonstandard
        if random.random() < 0.02:
            signup = (date.today() + timedelta(days=random.randint(5, 90))).isoformat()  # future
        con.execute("INSERT INTO customers VALUES (?,?,?,?)", (i, email, state, signup))
    con.commit()
    con.close()


def build_governance():
    con = sqlite3.connect(GOV_DB)
    con.executescript(GOV_SCHEMA)
    today = date.today().isoformat()
    con.executemany("INSERT INTO domain VALUES (?,?)", SEED_DOMAINS)
    for cid, name, definition, domain, col, cls, owner, steward, custodian in SEED_CDES:
        con.execute("INSERT INTO cde VALUES (?,?,?,?,?,?,?,?)",
                    (cid, name, definition, domain, "Operational CRM", "customers", col, cls))
        for role, person in (("owner", owner), ("steward", steward), ("custodian", custodian)):
            if person:
                con.execute("INSERT INTO cde_role VALUES (?,?,?,?)", (cid, role, person, today))
    con.executemany("INSERT INTO dq_rule (cde_id, dimension, passing_rows_sql, threshold_pct) VALUES (?,?,?,?)", SEED_RULES)
    for name, kind, tier, deps in SEED_USE_CASES:
        uid = con.execute("INSERT INTO use_case (name, kind, risk_tier) VALUES (?,?,?)", (name, kind, tier)).lastrowid
        con.executemany("INSERT INTO use_case_cde VALUES (?,?)", [(uid, d) for d in deps])
    con.commit()
    con.close()


def cmd_init(args):
    exists = [p for p in (OPS_DB, GOV_DB) if Path(p).exists()]
    if exists and not args.force:
        sys.exit(f"Already exists: {', '.join(exists)}. Use --force to rebuild, or run 'reset'.")
    for p in (OPS_DB, GOV_DB, HTML_OUT):
        if Path(p).exists():
            os.remove(p)
    build_operational()
    build_governance()
    print(f"Created {OPS_DB}  (business data: 500 customer rows, with defects)")
    print(f"Created {GOV_DB}  (governance record: domains, CDEs, roles, rules, use cases)")
    print("Next: python governance_demo.py register")


# ---------------------------------------------------------------------------
# register: show the catalog
# ---------------------------------------------------------------------------
def roles_for(gov, cde_id):
    return {r["role"]: r["person"] for r in
            gov.execute("SELECT role, person FROM cde_role WHERE cde_id = ?", (cde_id,))}


def cmd_register(args):
    gov = open_gov()
    print(f"\nGovernance register  ({GOV_DB})\n" + "=" * 66)
    for c in gov.execute("SELECT * FROM cde ORDER BY cde_id"):
        roles = roles_for(gov, c["cde_id"])
        print(f"\n{c['name']}  [{c['domain']}, {c['classification']}]")
        print(f"  Means:      {c['definition']}")
        print(f"  Lives in:   {c['source_system']} / {c['source_table']}.{c['source_column']}")
        print("  People:     " + " | ".join(f"{r.title()}: {roles.get(r, 'NONE')}" for r in ROLES))
        for r in gov.execute("SELECT dimension, threshold_pct FROM dq_rule WHERE cde_id = ? ORDER BY rule_id", (c["cde_id"],)):
            print(f"  Bar:        {r['dimension']} at {r['threshold_pct']}% or better")
    print("\nUse cases and the CDEs they depend on")
    for u in gov.execute("SELECT * FROM use_case ORDER BY use_case_id"):
        deps = [r["name"] for r in gov.execute(
            "SELECT c.name FROM use_case_cde x JOIN cde c ON c.cde_id = x.cde_id WHERE x.use_case_id = ? ORDER BY c.cde_id",
            (u["use_case_id"],))]
        print(f"  {u['name']} ({u['kind']}, {u['risk_tier']} risk): {', '.join(deps)}")
    print()


# ---------------------------------------------------------------------------
# scan: score rules, badge CDEs, roll up three numbers, open and close issues
# ---------------------------------------------------------------------------
def sync_issue(gov, key, cde_id, failing, description, assigned_to, run_id):
    """Open an issue when something fails and none is open. Close it when it clears."""
    open_issue = gov.execute("SELECT issue_id FROM issue WHERE issue_key = ? AND status = 'open'", (key,)).fetchone()
    if failing and not open_issue:
        gov.execute("INSERT INTO issue (issue_key, cde_id, description, assigned_to, opened_run, status) VALUES (?,?,?,?,?, 'open')",
                    (key, cde_id, description, assigned_to, run_id))
    elif not failing and open_issue:
        gov.execute("UPDATE issue SET status = 'closed', closed_run = ? WHERE issue_id = ?", (run_id, open_issue["issue_id"]))


def cmd_scan(args):
    gov = open_gov()
    ops = open_ops(read_only=True)   # the scanner cannot change the business data
    total = ops.execute("SELECT COUNT(*) FROM customers").fetchone()[0]
    run_id = gov.execute("INSERT INTO scan_run (ran_at, label, source_db, rows_scanned) VALUES (?,?,?,?)",
                         (datetime.now().isoformat(timespec="seconds"), args.label or "", OPS_DB, total)).lastrowid

    cdes = gov.execute("SELECT * FROM cde ORDER BY cde_id").fetchall()
    certified_ids, n_people, n_pass = set(), 0, 0
    for c in cdes:
        roles = roles_for(gov, c["cde_id"])
        missing = [r for r in ROLES if r not in roles]
        has_people = not missing
        all_pass = True
        for rule in gov.execute("SELECT * FROM dq_rule WHERE cde_id = ? ORDER BY rule_id", (c["cde_id"],)).fetchall():
            passed = ops.execute(rule["passing_rows_sql"]).fetchone()[0]
            pct = round(100.0 * passed / total, 1)
            ok = pct >= rule["threshold_pct"]
            all_pass &= ok
            gov.execute("INSERT INTO scan_result VALUES (?,?,?,?,?,?,?)",
                        (run_id, rule["rule_id"], passed, total, pct, rule["threshold_pct"], "PASS" if ok else "FAIL"))
            owner_of_fix = roles.get("steward") or roles.get("owner") or "UNASSIGNED"
            sync_issue(gov, f"rule:{rule['rule_id']}", c["cde_id"], not ok,
                       f"{c['name']} {rule['dimension']}: {pct}% against {rule['threshold_pct']}% bar",
                       owner_of_fix, run_id)
        for role in ROLES:   # a missing accountable person is an issue too
            sync_issue(gov, f"role:{c['cde_id']}:{role}", c["cde_id"], role in missing,
                       f"{c['name']} has no {role} assigned", roles.get("owner") or "UNASSIGNED", run_id)
        certified = all_pass and has_people
        reason = "" if certified else ("Missing an accountable person" if not has_people else "Below quality threshold")
        gov.execute("INSERT INTO cde_status VALUES (?,?,?,?,?,?)",
                    (run_id, c["cde_id"], int(has_people), int(all_pass), int(certified), reason))
        n_people += has_people
        n_pass += all_pass
        if certified:
            certified_ids.add(c["cde_id"])

    use_cases = gov.execute("SELECT use_case_id FROM use_case").fetchall()
    safe = 0
    for u in use_cases:
        deps = [r["cde_id"] for r in gov.execute("SELECT cde_id FROM use_case_cde WHERE use_case_id = ?", (u["use_case_id"],))]
        safe += all(d in certified_ids for d in deps)
    gov.execute("UPDATE scan_run SET coverage_pct = ?, trust_pct = ?, use_pct = ? WHERE run_id = ?",
                (round(100 * n_people / len(cdes)), round(100 * n_pass / len(cdes)),
                 round(100 * safe / len(use_cases)), run_id))
    gov.commit()

    snap = snapshot(gov, run_id)
    print_scorecard(snap)
    write_html(snap)
    print(f"Read-only scan of {OPS_DB}; results saved to {GOV_DB} as run {run_id}. Wrote {HTML_OUT}.\n")


def snapshot(gov, run_id):
    run = gov.execute("SELECT * FROM scan_run WHERE run_id = ?", (run_id,)).fetchone()
    cdes = []
    for c in gov.execute("SELECT * FROM cde ORDER BY cde_id"):
        st = gov.execute("SELECT * FROM cde_status WHERE run_id = ? AND cde_id = ?", (run_id, c["cde_id"])).fetchone()
        rules = gov.execute(
            "SELECT d.dimension, r.pct, r.threshold_pct, r.status FROM scan_result r "
            "JOIN dq_rule d ON d.rule_id = r.rule_id WHERE r.run_id = ? AND d.cde_id = ? ORDER BY d.rule_id",
            (run_id, c["cde_id"])).fetchall()
        cdes.append({"cde": c, "roles": roles_for(gov, c["cde_id"]), "status": st, "rules": rules})
    uses = []
    for u in gov.execute("SELECT * FROM use_case ORDER BY use_case_id"):
        deps = gov.execute(
            "SELECT c.name, s.certified FROM use_case_cde x JOIN cde c ON c.cde_id = x.cde_id "
            "JOIN cde_status s ON s.cde_id = c.cde_id AND s.run_id = ? WHERE x.use_case_id = ? ORDER BY c.cde_id",
            (run_id, u["use_case_id"])).fetchall()
        uses.append({"use": u, "deps": [d["name"] for d in deps], "safe": all(d["certified"] for d in deps)})
    issues = gov.execute("SELECT i.*, c.name AS cde_name FROM issue i JOIN cde c ON c.cde_id = i.cde_id "
                         "WHERE i.status = 'open' ORDER BY i.issue_id").fetchall()
    history = gov.execute("SELECT * FROM scan_run ORDER BY run_id").fetchall()
    return {"run": run, "cdes": cdes, "uses": uses, "issues": issues, "history": history}


def print_scorecard(s):
    run = s["run"]
    tag = f" [{run['label']}]" if run["label"] else ""
    print(f"\nScorecard, run {run['run_id']}{tag}  ({run['rows_scanned']} rows)\n" + "=" * 66)
    for item in s["cdes"]:
        c, st, roles = item["cde"], item["status"], item["roles"]
        badge = "CERTIFIED" if st["certified"] else f"NOT CERTIFIED ({st['reason']})"
        print(f"\n{c['name']}  [{c['domain']}]  {badge}")
        print("  " + " | ".join(f"{r.title()}: {roles.get(r, 'NONE')}" for r in ROLES))
        for r in item["rules"]:
            print(f"  {r['status']}  {r['dimension']:<13} {r['pct']:>5}%  (bar {r['threshold_pct']}%)")
    print("\nUse cases")
    for u in s["uses"]:
        print(f"  {'CLEARED' if u['safe'] else 'BLOCKED'}  {u['use']['name']} ({u['use']['kind']}, {u['use']['risk_tier']} risk)")
    print("\n" + "=" * 66)
    print(f"Coverage {run['coverage_pct']}%   Trust {run['trust_pct']}%   Use {run['use_pct']}%   "
          f"Open issues: {len(s['issues'])}\n")


# ---------------------------------------------------------------------------
# fix-data and assign-steward: the two different kinds of fix
# ---------------------------------------------------------------------------
def cmd_fix_data(args):
    """Steward and custodian clean the business data. (Writes to operational.db.)"""
    con = open_ops(read_only=False)
    fixes = [
        ("Replace missing or malformed emails",
         "UPDATE customers SET email = 'cust' || customer_id || '@example.com' "
         "WHERE email IS NULL OR TRIM(email) = '' OR email NOT LIKE '_%@_%._%' OR email LIKE '% %'"),
        ("Re-key duplicate emails (keep the first record)",
         "UPDATE customers SET email = 'cust' || customer_id || '@example.com' "
         "WHERE customer_id NOT IN (SELECT MIN(customer_id) FROM customers GROUP BY LOWER(email))"),
        ("Standardize state codes",
         "UPDATE customers SET state = CASE state WHEN 'Wash.' THEN 'WA' WHEN 'ca' THEN 'CA' "
         f"WHEN 'Texas' THEN 'TX' ELSE 'CA' END WHERE state NOT IN ({STATE_LIST_SQL})"),
        ("Correct future-dated signups",
         "UPDATE customers SET signup_date = DATE('now') WHERE signup_date > DATE('now')"),
    ]
    print(f"\nCleaning {OPS_DB} (this is the business data, not the catalog)")
    for label, sql in fixes:
        n = con.execute(sql).rowcount
        print(f"  {n:>4} rows  {label}")
    con.commit()
    con.close()
    print("\nNext: python governance_demo.py scan --label \"data fixed\"\n")


def cmd_assign_steward(args):
    """Name a person in the governance record. (Writes to governance.db only.)"""
    gov = open_gov()
    row = gov.execute("SELECT cde_id FROM cde WHERE name = ?", (args.cde,)).fetchone()
    if not row:
        sys.exit(f"No CDE named '{args.cde}'. Run 'register' to see the names.")
    gov.execute("INSERT OR REPLACE INTO cde_role VALUES (?,?,?,?)",
                (row["cde_id"], args.role, args.person, date.today().isoformat()))
    gov.commit()
    print(f"\n{args.person} is now the {args.role} for {args.cde} (recorded in {GOV_DB}).")
    print("Next: python governance_demo.py scan --label \"steward named\"\n")


# ---------------------------------------------------------------------------
# history and issues
# ---------------------------------------------------------------------------
def cmd_history(args):
    gov = open_gov()
    print(f"\nScan history  ({GOV_DB})\n" + "=" * 78)
    print(f"{'Run':<4} {'When':<20} {'Label':<18} {'Coverage':>9} {'Trust':>7} {'Use':>6} {'Certified':>10}")
    for r in gov.execute("SELECT * FROM scan_run ORDER BY run_id"):
        cert = gov.execute("SELECT SUM(certified) AS n, COUNT(*) AS t FROM cde_status WHERE run_id = ?", (r["run_id"],)).fetchone()
        print(f"{r['run_id']:<4} {r['ran_at']:<20} {r['label'][:18]:<18} {str(r['coverage_pct']) + '%':>9} "
              f"{str(r['trust_pct']) + '%':>7} {str(r['use_pct']) + '%':>6} {str(cert['n']) + ' of ' + str(cert['t']):>10}")
    print()


def cmd_issues(args):
    gov = open_gov()
    where = "" if args.all else "WHERE i.status = 'open'"
    rows = gov.execute(f"SELECT i.*, c.name AS cde_name FROM issue i JOIN cde c ON c.cde_id = i.cde_id {where} ORDER BY i.issue_id").fetchall()
    print(f"\n{'All' if args.all else 'Open'} issues  ({GOV_DB})\n" + "=" * 78)
    if not rows:
        print("None.\n")
        return
    for i in rows:
        closed = f", closed in run {i['closed_run']}" if i["closed_run"] else ""
        print(f"#{i['issue_id']:<3} {i['status'].upper():<6} assigned to {i['assigned_to']:<18} "
              f"opened run {i['opened_run']}{closed}\n     {i['description']}")
    print()


def cmd_reset(args):
    for p in (OPS_DB, GOV_DB, HTML_OUT):
        if Path(p).exists():
            os.remove(p)
            print(f"Removed {p}")
    print("Clean slate. Run: python governance_demo.py init\n")


# ---------------------------------------------------------------------------
# HTML scorecard
# ---------------------------------------------------------------------------
def write_html(s):
    e = html.escape
    css = "bootstrap.min.css" if Path("bootstrap.min.css").exists() else CDN_CSS
    run = s["run"]

    def tile(label, value, hint):
        tone = "success" if value >= 80 else ("warning" if value >= 50 else "danger")
        return (f"<div class='col-md-4'><div class='card text-center border-{tone}'><div class='card-body'>"
                f"<div class='display-5 text-{tone}'>{value}%</div><div class='fw-bold'>{label}</div>"
                f"<div class='small text-muted'>{hint}</div></div></div></div>")

    tiles = (tile("Coverage", run["coverage_pct"], "CDEs with owner, steward, and custodian named")
             + tile("Trust", run["trust_pct"], "CDEs inside every quality threshold")
             + tile("Use", run["use_pct"], "Use cases running only on certified CDEs"))

    cards = []
    for item in s["cdes"]:
        c, st, roles = item["cde"], item["status"], item["roles"]
        tone = "success" if st["certified"] else "danger"
        badge = "Certified" if st["certified"] else f"Not certified: {e(st['reason'])}"
        rule_rows = "".join(
            f"<tr><td>{e(r['dimension'])}</td><td>{r['pct']}%</td><td>{r['threshold_pct']}%</td>"
            f"<td><span class='badge text-bg-{'success' if r['status'] == 'PASS' else 'danger'}'>{r['status'].title()}</span></td></tr>"
            for r in item["rules"])
        people = "".join(f"<li><strong>{r.title()}:</strong> {e(roles.get(r, 'None assigned'))}</li>" for r in ROLES)
        cards.append(f"""<div class="col-md-4"><div class="card h-100 border-{tone}">
          <div class="card-header d-flex justify-content-between align-items-center">
            <strong>{e(c['name'])}</strong><span class="badge text-bg-{tone}">{badge}</span></div>
          <div class="card-body"><p class="small text-muted">{e(c['definition'])}</p>
            <p class="small mb-1"><strong>{e(c['domain'])}</strong> domain, {e(c['classification'])}</p>
            <ul class="list-unstyled small">{people}</ul>
            <table class="table table-sm"><thead><tr><th>Rule</th><th>Score</th><th>Bar</th><th></th></tr></thead>
            <tbody>{rule_rows}</tbody></table></div></div></div>""")

    uses = "".join(
        f"<tr><td>{e(u['use']['name'])}</td><td>{e(u['use']['kind'])}</td><td>{e(u['use']['risk_tier'])}</td>"
        f"<td>{e(', '.join(u['deps']))}</td>"
        f"<td><span class='badge text-bg-{'success' if u['safe'] else 'danger'}'>{'Cleared' if u['safe'] else 'Blocked'}</span></td></tr>"
        for u in s["uses"])

    def bar(v):
        tone = "success" if v >= 80 else ("warning" if v >= 50 else "danger")
        return (f"<div class='progress' style='min-width:110px'><div class='progress-bar bg-{tone}' "
                f"style='width:{v}%'>{v}%</div></div>")

    hist = "".join(
        f"<tr><td>{r['run_id']}</td><td>{e(r['ran_at'])}</td><td>{e(r['label'] or '')}</td>"
        f"<td>{bar(r['coverage_pct'])}</td><td>{bar(r['trust_pct'])}</td><td>{bar(r['use_pct'])}</td></tr>"
        for r in s["history"])

    issues = "".join(
        f"<tr><td>#{i['issue_id']}</td><td>{e(i['cde_name'])}</td><td>{e(i['description'])}</td>"
        f"<td>{e(i['assigned_to'])}</td><td>{i['opened_run']}</td></tr>"
        for i in s["issues"]) or "<tr><td colspan='5' class='text-success'>No open issues.</td></tr>"

    page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Governance Scorecard</title><link href="{css}" rel="stylesheet"></head>
<body class="bg-white"><div class="container py-4">
<h1 class="h3">Governance Scorecard</h1>
<p class="text-muted">Run {run['run_id']}{(' (' + e(run['label']) + ')') if run['label'] else ''}:
{run['rows_scanned']} rows read from <code>{OPS_DB}</code> (read-only). Results stored in <code>{GOV_DB}</code>.</p>
<div class="row g-3 mb-4">{tiles}</div>
<div class="row g-3 mb-4">{''.join(cards)}</div>
<h2 class="h5">Use cases</h2>
<table class="table table-sm mb-4"><thead><tr><th>Use case</th><th>Kind</th><th>Risk</th><th>Depends on</th><th></th></tr></thead><tbody>{uses}</tbody></table>
<h2 class="h5">Trend across runs</h2>
<table class="table table-sm align-middle mb-4"><thead><tr><th>Run</th><th>When</th><th>Label</th><th>Coverage</th><th>Trust</th><th>Use</th></tr></thead><tbody>{hist}</tbody></table>
<h2 class="h5">Open issues</h2>
<table class="table table-sm"><thead><tr><th>Issue</th><th>CDE</th><th>What</th><th>Assigned to</th><th>Opened in run</th></tr></thead><tbody>{issues}</tbody></table>
</div></body></html>"""
    Path(HTML_OUT).write_text(page, encoding="utf-8")


# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description="Two-database governance demo")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("init", help="create operational.db and governance.db")
    p.add_argument("--force", action="store_true", help="rebuild even if the files exist")
    p.set_defaults(fn=cmd_init)

    sub.add_parser("register", help="show the governance register").set_defaults(fn=cmd_register)

    p = sub.add_parser("scan", help="run all rules and record the results")
    p.add_argument("--label", default="", help="short name for this run, e.g. baseline")
    p.set_defaults(fn=cmd_scan)

    sub.add_parser("fix-data", help="clean the operational data").set_defaults(fn=cmd_fix_data)

    p = sub.add_parser("assign-steward", help="name a person in the governance record")
    p.add_argument("--cde", default="Signup Date")
    p.add_argument("--person", default="Marcus (Sales Ops)")
    p.add_argument("--role", default="steward", choices=ROLES)
    p.set_defaults(fn=cmd_assign_steward)

    sub.add_parser("history", help="Coverage, Trust, and Use for every run").set_defaults(fn=cmd_history)

    p = sub.add_parser("issues", help="list issues")
    p.add_argument("--all", action="store_true", help="include closed issues")
    p.set_defaults(fn=cmd_issues)

    sub.add_parser("reset", help="delete both databases and the report").set_defaults(fn=cmd_reset)

    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()