"""
Builds a small ILLUSTRATIVE extract for the optional "Go further" activities.

Adventure Works Cycles is a fictitious bicycle maker that began as a Microsoft sample company.
Everything in this extract is invented for teaching. It is NOT the Microsoft sample database, and it
carries no real financial figures (the company profile itself says no financial statements exist).
It follows the company profile: two sales channels (Internet and Reseller), 10 territories in 3 regions,
a July 1 to June 30 fiscal year, and a case window of May 31, 2011 to June 30, 2014.

Run:  python3 build_aw_extract.py          (Python 3.9 or later and numpy)
Writes aw_extract.sqlite, the CSV files, and ../../facilitator/aw_answer_key.md
"""
import csv
import datetime as dt
import os
import sqlite3

import numpy as np

# The modules quote numbers from the files this script produced. numpy does not promise the same random
# numbers across releases, so a rebuild with another version can change the data and break those numbers.
BUILT_WITH_NUMPY = "2.5.4"
if np.__version__ != BUILT_WITH_NUMPY:
    print("WARNING: these files were built with numpy %s and you have %s. A rebuild may produce different data, "
          "so re-check every number in the modules against the new answer key before publishing." % (BUILT_WITH_NUMPY, np.__version__))

HERE = os.path.dirname(os.path.abspath(__file__))
FAC = os.path.join(HERE, "..", "..", "facilitator")
rng = np.random.default_rng(20110531)

START, END = dt.date(2011, 5, 31), dt.date(2014, 6, 30)
NDAYS = (END - START).days + 1


def fiscal_year(d):
    return d.year + 1 if d.month >= 7 else d.year  # FY ends June 30


# -------------------------------------------------------------- territories
TERRITORIES = [(1, "Canada", "North America"), (2, "Central", "North America"), (3, "Northeast", "North America"),
               (4, "Northwest", "North America"), (5, "Southeast", "North America"), (6, "Southwest", "North America"),
               (7, "France", "Europe"), (8, "Germany", "Europe"), (9, "United Kingdom", "Europe"), (10, "Pacific", "Pacific")]
TERR_W = np.array([.08, .05, .07, .14, .06, .20, .09, .09, .10, .12])
TERR_W = TERR_W / TERR_W.sum()

# ----------------------------------------------------------------- products
CATALOG = {
    ("Bikes", "Mountain Bikes"): (1100, 3400, .62, ["Ridgeback 200", "Ridgeback 400", "Ridgeback 600"]),
    ("Bikes", "Road Bikes"): (900, 3300, .64, ["Roadster 100", "Roadster 300", "Roadster 500"]),
    ("Bikes", "Touring Bikes"): (1300, 2900, .63, ["Wayfarer 300", "Wayfarer 500", "Wayfarer 700"]),
    ("Components", "Wheels"): (90, 480, .58, ["Trail Wheel", "Road Wheel", "Carbon Wheel"]),
    ("Components", "Handlebars"): (25, 140, .55, ["Flat Bar", "Drop Bar", "Riser Bar"]),
    ("Components", "Brakes"): (30, 160, .56, ["Rim Brake Set", "Disc Brake Set", "Hydraulic Brake Set"]),
    ("Components", "Saddles"): (30, 120, .52, ["Comfort Saddle", "Sport Saddle", "Race Saddle"]),
    ("Components", "Pedals"): (20, 110, .53, ["Platform Pedals", "Clipless Pedals", "Touring Pedals"]),
    ("Clothing", "Jerseys"): (35, 85, .48, ["Short-Sleeve Jersey", "Long-Sleeve Jersey", "Race Jersey"]),
    ("Clothing", "Shorts"): (40, 90, .47, ["Basic Shorts", "Padded Shorts", "Bib Shorts"]),
    ("Clothing", "Gloves"): (18, 50, .46, ["Half-Finger Gloves", "Full-Finger Gloves", "Winter Gloves"]),
    ("Clothing", "Socks"): (8, 20, .45, ["Mountain Socks", "Racing Socks", "Wool Socks"]),
    ("Accessories", "Helmets"): (35, 120, .42, ["Sport Helmet", "Road Helmet", "Trail Helmet"]),
    ("Accessories", "Lights"): (20, 90, .40, ["Front Light", "Rear Light", "Light Set"]),
    ("Accessories", "Locks"): (15, 65, .38, ["Cable Lock", "U-Lock", "Chain Lock"]),
    ("Accessories", "Water Bottles"): (5, 15, .36, ["Basic Bottle", "Insulated Bottle", "Race Bottle"]),
}
products, pid = [], 1
for (cat, sub), (lo, hi, ratio, names) in CATALOG.items():
    prices = np.sort(rng.uniform(lo, hi, len(names)))
    for name, price in zip(names, prices):
        price = round(float(price), 2)
        products.append(dict(product_id=pid, product_name=name, category=cat, subcategory=sub, list_price=price,
                             standard_cost=round(price * float(rng.uniform(ratio - .04, ratio + .04)), 2)))
        pid += 1
BY_CAT = {}
for p in products:
    BY_CAT.setdefault(p["category"], []).append(p)

# ---------------------------------------------------------------- customers
customers = []
for cid in range(1, 2601):
    store = rng.random() < .22
    customers.append(dict(customer_id=cid, customer_type="Store" if store else "Individual",
                          territory_id=int(rng.choice(10, p=TERR_W)) + 1))
INDIV = [c for c in customers if c["customer_type"] == "Individual"]
STORES = [c for c in customers if c["customer_type"] == "Store"]

# ------------------------------------------------------------------- orders
# Growth by fiscal year; seasonality peaks in spring and summer.
SEASON = {1: .8, 2: .8, 3: 1.0, 4: 1.2, 5: 1.4, 6: 1.4, 7: 1.3, 8: 1.2, 9: 1.0, 10: .9, 11: .8, 12: .9}
days = np.array([START + dt.timedelta(days=i) for i in range(NDAYS)])
growth = np.array([1.0 + .22 * (i / 365.0) for i in range(NDAYS)])
weight = np.array([SEASON[d.month] for d in days]) * growth
weight = weight / weight.sum()

orders, lines = [], []
oid = 1
N_ORDERS = 6600
order_days = np.sort(rng.choice(NDAYS, N_ORDERS, p=weight))
for di in order_days:
    d = days[di]
    reseller = rng.random() < .24
    cust = STORES[int(rng.integers(len(STORES)))] if reseller else INDIV[int(rng.integers(len(INDIV)))]
    channel = "Reseller" if reseller else "Internet"
    if reseller:
        nl = 2 + int(rng.poisson(2))
        disc_pool = [0, .05, .10, .15, .20]
    else:
        nl = 1 + int(rng.poisson(.5))
        disc_pool = [0, 0, 0, .05, .10]
    cat_p = [.30, .28, .20, .22] if reseller else [.20, .22, .30, .28]
    for ln in range(1, nl + 1):
        cat = ["Bikes", "Components", "Clothing", "Accessories"][int(rng.choice(4, p=cat_p))]
        prod = BY_CAT[cat][int(rng.integers(len(BY_CAT[cat])))]
        qty = int(rng.integers(1, 6)) if reseller else (1 if rng.random() < .85 else 2)
        disc = float(rng.choice(disc_pool))
        lines.append(dict(order_id=oid, line_no=ln, product_id=prod["product_id"], quantity=qty,
                          unit_price=prod["list_price"], discount=disc))
    orders.append(dict(order_id=oid, order_date=d.isoformat(), channel=channel, customer_id=cust["customer_id"],
                       territory_id=cust["territory_id"]))
    oid += 1

# --------------------------------------------------- territory annual targets
prod_by_id = {p["product_id"]: p for p in products}
actual = {}
for o in orders:
    fy = fiscal_year(dt.date.fromisoformat(o["order_date"]))
    actual.setdefault((o["territory_id"], fy), 0.0)
rev_by_order = {}
for l in lines:
    rev_by_order[l["order_id"]] = rev_by_order.get(l["order_id"], 0.0) + l["quantity"] * l["unit_price"] * (1 - l["discount"])
for o in orders:
    fy = fiscal_year(dt.date.fromisoformat(o["order_date"]))
    actual[(o["territory_id"], fy)] += rev_by_order[o["order_id"]]
targets = []
for (t, fy), a in sorted(actual.items()):
    if fy < 2012:
        continue
    prior = actual.get((t, fy - 1), 0.0)
    if fy == 2012:
        tgt = a * float(rng.uniform(.9, 1.1))   # first full year: no prior year to build on
    else:
        tgt = prior * float(rng.uniform(1.10, 1.30))
    targets.append(dict(territory_id=t, fiscal_year=fy, sales_target=round(tgt, 2)))

# ------------------------------------------------------------------ write out
def write_csv(name, rows, fields):
    with open(os.path.join(HERE, name), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


TERR_ROWS = [dict(territory_id=t, territory_name=n, region=r) for t, n, r in TERRITORIES]
SCHEMA = {
    "sales_territory": (["territory_id", "territory_name", "region"], TERR_ROWS),
    "product": (["product_id", "product_name", "category", "subcategory", "list_price", "standard_cost"], products),
    "customer": (["customer_id", "customer_type", "territory_id"], customers),
    "sales_order": (["order_id", "order_date", "channel", "customer_id", "territory_id"], orders),
    "sales_order_line": (["order_id", "line_no", "product_id", "quantity", "unit_price", "discount"], lines),
    "territory_target": (["territory_id", "fiscal_year", "sales_target"], targets),
}
db = os.path.join(HERE, "aw_extract.sqlite")
if os.path.exists(db):
    os.remove(db)
con = sqlite3.connect(db)
con.executescript("""
CREATE TABLE sales_territory (territory_id INTEGER PRIMARY KEY, territory_name TEXT, region TEXT);
CREATE TABLE product (product_id INTEGER PRIMARY KEY, product_name TEXT, category TEXT, subcategory TEXT, list_price REAL, standard_cost REAL);
CREATE TABLE customer (customer_id INTEGER PRIMARY KEY, customer_type TEXT, territory_id INTEGER REFERENCES sales_territory(territory_id));
CREATE TABLE sales_order (order_id INTEGER PRIMARY KEY, order_date TEXT, channel TEXT, customer_id INTEGER REFERENCES customer(customer_id), territory_id INTEGER REFERENCES sales_territory(territory_id));
CREATE TABLE sales_order_line (order_id INTEGER REFERENCES sales_order(order_id), line_no INTEGER, product_id INTEGER REFERENCES product(product_id), quantity INTEGER, unit_price REAL, discount REAL, PRIMARY KEY (order_id, line_no));
CREATE TABLE territory_target (territory_id INTEGER REFERENCES sales_territory(territory_id), fiscal_year INTEGER, sales_target REAL, PRIMARY KEY (territory_id, fiscal_year));
""")
for t, (fields, rows) in SCHEMA.items():
    write_csv(t + ".csv", rows, fields)
    con.executemany("INSERT INTO %s (%s) VALUES (%s)" % (t, ",".join(fields), ",".join("?" * len(fields))),
                    [tuple(r[f] for f in fields) for r in rows])
con.commit()

# ----------------------------------------------------------------- answer key
q = lambda s: con.execute(s).fetchall()
os.makedirs(FAC, exist_ok=True)
L = ["# Adventure Works illustrative extract: answer key numbers\n",
     "Generated by build_aw_extract.py. Everything is invented for teaching and is not the Microsoft sample database.\n",
     "## Table sizes\n"]
for t in SCHEMA:
    L.append("- %s: %s rows" % (t, format(q("SELECT COUNT(*) FROM %s" % t)[0][0], ",")))
L.append("\n## Module 04 Go further: Internet and Reseller channels (descriptive)\n")
L.append("| Channel | Orders | Revenue | Average order value | Gross margin |")
L.append("|---|---:|---:|---:|---:|")
rows = q("""SELECT o.channel, COUNT(DISTINCT o.order_id),
  SUM(l.quantity*l.unit_price*(1-l.discount)),
  SUM(l.quantity*l.unit_price*(1-l.discount)) / COUNT(DISTINCT o.order_id),
  1 - SUM(l.quantity*p.standard_cost) / SUM(l.quantity*l.unit_price*(1-l.discount))
FROM sales_order o JOIN sales_order_line l USING(order_id) JOIN product p USING(product_id) GROUP BY o.channel ORDER BY o.channel""")
tot_rev = sum(r[2] for r in rows)
for ch, n, rev, aov, gm in rows:
    L.append("| %s | %s | $%s (%.0f%% of total) | $%s | %.1f%% |" % (ch, format(n, ","), format(round(rev), ","), 100 * rev / tot_rev, format(round(aov), ","), 100 * gm))
L.append("\nGross margin here is revenue after discount minus standard cost, divided by revenue. Both numbers are illustrative.")
L.append("\n## Later Go further: territory performance against target, by fiscal year\n")
L.append("| Territory | FY2012 | FY2013 | FY2014 | FY2013 vs target | FY2014 vs target |")
L.append("|---|---:|---:|---:|---:|---:|")
T = {}
for t, fy, a in q("""SELECT o.territory_id, CASE WHEN CAST(substr(o.order_date,6,2) AS INT) >= 7 THEN CAST(substr(o.order_date,1,4) AS INT)+1 ELSE CAST(substr(o.order_date,1,4) AS INT) END fy,
  SUM(l.quantity*l.unit_price*(1-l.discount)) FROM sales_order o JOIN sales_order_line l USING(order_id) GROUP BY 1,2"""):
    T[(t, fy)] = a
TG = {(r[0], r[1]): r[2] for r in q("SELECT territory_id, fiscal_year, sales_target FROM territory_target")}
for t, n, _ in TERRITORIES:
    row = [n]
    for fy in (2012, 2013, 2014):
        row.append("$%s" % format(round(T.get((t, fy), 0)), ","))
    for fy in (2013, 2014):
        row.append("%+.0f%%" % (100 * (T[(t, fy)] / TG[(t, fy)] - 1)))
    L.append("| " + " | ".join(row) + " |")
L.append("\nFiscal years run July 1 to June 30 (FY2014 is July 2013 to June 2014). FY2012 holds the May 31, 2011 stub plus the year that follows. Targets are invented.")
L.append("\n## Later Go further: product margin\n")
L.append("| Category | Revenue | Gross margin |")
L.append("|---|---:|---:|")
for cat, rev, gm in q("""SELECT p.category, SUM(l.quantity*l.unit_price*(1-l.discount)), 1 - SUM(l.quantity*p.standard_cost)/SUM(l.quantity*l.unit_price*(1-l.discount))
FROM sales_order_line l JOIN product p USING(product_id) GROUP BY 1 ORDER BY 2 DESC"""):
    L.append("| %s | $%s | %.1f%% |" % (cat, format(round(rev), ","), 100 * gm))

# ---- Module 06 Go further: drill into the territory with the biggest miss against target in FY2014
FYSQL = "CASE WHEN CAST(substr(o.order_date,6,2) AS INT) >= 7 THEN CAST(substr(o.order_date,1,4) AS INT)+1 ELSE CAST(substr(o.order_date,1,4) AS INT) END"
miss = min(((t, T[(t, 2014)] / TG[(t, 2014)] - 1) for t, _, _ in TERRITORIES), key=lambda x: x[1])
tname = [n for t, n, _ in TERRITORIES if t == miss[0]][0]
L.append("\n## Module 06 Go further: why did %s miss its FY2014 target?\n" % tname)
L.append("FY2014 revenue was %+.0f%% against target, and FY2013 had been %+.0f%% against target." % (100 * miss[1], 100 * (T[(miss[0], 2013)] / TG[(miss[0], 2013)] - 1)))
L.append("\n| Fiscal year | Channel | Orders | Revenue | Average order value |")
L.append("|---|---|---:|---:|---:|")
for fy, ch, n, rev in q("""SELECT %s fy, o.channel, COUNT(DISTINCT o.order_id), SUM(l.quantity*l.unit_price*(1-l.discount))
FROM sales_order o JOIN sales_order_line l USING(order_id) WHERE o.territory_id = %d AND fy IN (2013, 2014) GROUP BY 1, 2 ORDER BY 1, 2""" % (FYSQL, miss[0])):
    L.append("| FY%d | %s | %d | $%s | $%s |" % (fy, ch, n, format(round(rev), ","), format(round(rev / n), ",")))
big = q("""SELECT %s fy, MAX(rv) FROM (SELECT o.order_id, o.order_date, SUM(l.quantity*l.unit_price*(1-l.discount)) rv FROM sales_order o JOIN sales_order_line l USING(order_id)
 WHERE o.territory_id = %d GROUP BY o.order_id) o GROUP BY 1 HAVING fy IN (2013, 2014)""" % (FYSQL.replace("o.order_date", "o.order_date"), miss[0]))
L.append("\nLargest single order in the territory by fiscal year: " + ", ".join("FY%d $%s" % (fy, format(round(v), ",")) for fy, v in big) + ". Territory revenue is lumpy because a handful of large Reseller orders can swing a year, so a single year's miss is weak evidence of a real problem.")

# ---- Module 08 Go further: Internet channel margin by category
L.append("\n## Module 08 Go further: which category should the Internet team promote? (Internet channel only)\n")
L.append("| Category | Revenue | Gross margin dollars | Gross margin percent | Share of Internet revenue |")
L.append("|---|---:|---:|---:|---:|")
irows = q("""SELECT p.category, SUM(l.quantity*l.unit_price*(1-l.discount)) rev,
  SUM(l.quantity*l.unit_price*(1-l.discount)) - SUM(l.quantity*p.standard_cost) gm
FROM sales_order o JOIN sales_order_line l USING(order_id) JOIN product p USING(product_id)
WHERE o.channel = 'Internet' GROUP BY 1 ORDER BY gm DESC""")
itot = sum(r[1] for r in irows)
for cat, rev, gm in irows:
    L.append("| %s | $%s | $%s | %.1f%% | %.0f%% |" % (cat, format(round(rev), ","), format(round(gm), ","), 100 * gm / rev, 100 * rev / itot))
L.append("\nThe highest margin percent and the highest margin dollars are in different categories, which is the point of the exercise.")
with open(os.path.join(FAC, "aw_answer_key.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(L) + "\n")
con.close()
print("\n".join(L))
