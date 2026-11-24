"""
Builds the Lantern Peak Supply Co. case data for the Data Literacy course.

Everything is fictitious and seeded, so the same files rebuild identically.
Run:  python3 build_case_data.py
Needs: Python 3.9 or later, numpy. SQLite ships with Python.

Outputs (written next to this script):
  lantern_clean.sqlite      cleaned tables plus supplements
  raw/                      the messy files learners clean in Modules 02 and 03
  clean_csv/                cleaned tables as CSV for spreadsheet users
  supplements/              loyalty, marketing, survey, churn pilot, Anscombe
  data_dictionary.csv       learner-facing dictionary (no type answers)
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

SEED = 20261124
rng = np.random.default_rng(SEED)
HERE = os.path.dirname(os.path.abspath(__file__))

START = dt.date(2023, 1, 1)
END = dt.date(2025, 12, 31)
NDAYS = (END - START).days + 1
LAUNCH = dt.date(2024, 7, 1)  # loyalty program launch

SEASON_BY_MONTH = {1: .80, 2: .80, 3: .90, 4: 1.0, 5: 1.10, 6: 1.25,
                   7: 1.30, 8: 1.20, 9: 1.0, 10: 1.05, 11: 1.60, 12: 1.85}
DAYS = [START + dt.timedelta(days=i) for i in range(NDAYS)]
SEASON = np.array([SEASON_BY_MONTH[d.month] for d in DAYS])
AVG_SEASON = SEASON.mean()


def day_to_date(i):
    return START + dt.timedelta(days=int(i))


def date_to_day(d):
    return (d - START).days


# ---------------------------------------------------------------- products
CATEGORIES = {
    # Names are listed from cheapest to priciest, because sorted prices are assigned in list order.
    "Shelter": (99, 399, .60, ["Camp Shade Shelter", "Trailfly Tarp 10x10", "Stormbreak Rain Fly", "Summit Bivy",
                               "Alpine Hammock Shelter", "Gearshed Canopy", "Featherlight 1P Tent",
                               "Ridgeline 2P Tent", "Ridgeline 4P Tent", "Basecamp Cabin Tent"]),
    "Sleep": (49, 249, .60, ["Camp Pillow Compact", "Summer Liner Bag", "Down Booties", "Hammock Underquilt",
                             "Cloudrest Sleeping Pad", "Airlift Pad Plus", "Quilted Trail Quilt", "Basecamp Cot",
                             "Nightfall 20F Bag", "Nightfall 0F Bag"]),
    "Packs": (39, 219, .60, ["Pack Rain Cover", "Hip Belt Pouch", "Dry Bag 10L", "Dry Bag 30L", "Camera Sling",
                             "Kid Explorer Pack", "Daybreak 20L Pack", "Trail Runner Vest", "Ridge 45L Pack",
                             "Summit 65L Pack"]),
    "Clothing": (19, 189, .45, ["Wool Hiking Socks", "Sun Hoodie", "Trail Shorts", "Merino Base Layer Top",
                                "Merino Base Layer Bottom", "Hiking Pants", "Fleece Midlayer", "Trail Rain Jacket",
                                "Insulated Puffy Jacket", "Alpine Shell"]),
    "Footwear": (69, 199, .55, ["Camp Slipper", "Trail Sandal", "Water Shoe", "Camp Sandal", "Approach Shoe",
                                "Trail Runner Low", "Trail Runner Mid", "Hiking Shoe", "Hiking Boot",
                                "Insulated Winter Boot"]),
    "Cook_Hydrate": (9, 119, .55, ["Spork Set", "Camp Mug", "Fuel Canister", "Water Filter Squeeze",
                                   "Insulated Bottle 32oz", "Hydration Bladder 2L", "Pocket Stove", "Titanium Pot Set",
                                   "Gravity Filter 4L", "Dual Burner Camp Stove"]),
}
BASE_COLORS = ["Red", "Blue", "Green", "Black", "Gray", "Orange", "Yellow", "Olive", "Brown", "Navy"]
COLOR_VARIANTS = {
    "Red": ["Red", "red", "RED", "Light Red", "auburn", "Crimson", "Brick Red"],
    "Blue": ["Blue", "blue", "Sky Blue", "Light Blue", "Cobalt"],
    "Green": ["Green", "green", "Forest Green", "Lime"],
    "Black": ["Black", "black", "Jet Black", "BLACK"],
    "Gray": ["Gray", "Grey", "grey", "Charcoal"],
    "Orange": ["Orange", "orange", "Burnt Orange", "Rust"],
    "Yellow": ["Yellow", "yellow", "Gold"],
    "Olive": ["Olive", "olive", "Olive Drab"],
    "Brown": ["Brown", "brown", "Tan", "Coffee"],
    "Navy": ["Navy", "navy", "Dark Blue"],
}

products = []
pid = 1
for cat, (lo, hi, cost_ratio, names) in CATEGORIES.items():
    prices = np.sort(rng.uniform(lo, hi, len(names)))
    for name, price in zip(names, prices):
        price = round(float(price) - 0.01, 2)
        cost = round(price * float(rng.uniform(cost_ratio - .07, cost_ratio + .07)), 2)
        color = BASE_COLORS[int(rng.integers(0, len(BASE_COLORS)))]
        products.append(dict(product_id=pid, product_name=name, category=cat,
                             list_price=price, unit_cost=cost, color=color))
        pid += 1
PROD_BY_CAT = {}
for p in products:
    PROD_BY_CAT.setdefault(p["category"], []).append(p)
CAT_WEIGHTS = {"Shelter": .08, "Sleep": .11, "Packs": .13, "Clothing": .28, "Footwear": .13, "Cook_Hydrate": .27}
CAT_LIST = list(CAT_WEIGHTS)
CAT_P = np.array([CAT_WEIGHTS[c] for c in CAT_LIST])
CAT_P = CAT_P / CAT_P.sum()
RETURN_RATE = {"Shelter": .06, "Sleep": .05, "Packs": .07, "Clothing": .15, "Footwear": .19, "Cook_Hydrate": .04}

# --------------------------------------------------------------- customers
NEW_BY_YEAR = {2023: 1800, 2024: 2300, 2025: 2800}
MIX = {2023: (.55, .30, .15), 2024: (.50, .30, .20), 2025: (.30, .20, .50)}
CHANNELS = ["organic_search", "email_referral", "paid_social"]
P_REPEAT90 = {2023: (.44, .38, .18), 2024: (.46, .40, .20), 2025: (.48, .42, .22)}
WHOLESALE_SHARE = .015
REGIONS = ["Northeast", "Southeast", "Midwest", "Southwest", "West", "Northwest"]
REGION_P = [.20, .18, .20, .12, .22, .08]
AGE_BANDS = ["18-24", "25-34", "35-44", "45-54", "55+"]
AGE_P = [.10, .30, .27, .18, .15]

month_w = {y: np.array([SEASON_BY_MONTH[m] * (1 if not (y == 2023 and m == 1) else 1) for m in range(1, 13)])
           for y in NEW_BY_YEAR}

customers = []
ENGAGE = {}
cust_orders = {}  # customer_id -> list of day offsets
SPECS = []        # (customer dict, hidden traits) built first so repeat purchase can be assigned exactly per cohort
cid = 1001
for year, n in NEW_BY_YEAR.items():
    mw = month_w[year] / month_w[year].sum()
    for _ in range(n):
        month = int(rng.choice(12, p=mw)) + 1
        last = (dt.date(year + (month == 12), (month % 12) + 1, 1) - dt.timedelta(days=1)).day
        acq = dt.date(year, month, int(rng.integers(1, last + 1)))
        wholesale = rng.random() < WHOLESALE_SHARE
        if wholesale:
            ctype, ch, k, m = "wholesale", "sales_rep", None, float(rng.lognormal(0.3, .3))
        else:
            k = int(rng.choice(3, p=MIX[year]))
            ctype, ch, m = "consumer", CHANNELS[k], float(rng.lognormal(0, .35))
        e = 1.0 if wholesale else float(rng.lognormal(0, .6))  # persistent engagement trait (hidden)
        region = REGIONS[int(rng.choice(len(REGIONS), p=REGION_P))]
        age = None if rng.random() < .08 else AGE_BANDS[int(rng.choice(len(AGE_BANDS), p=AGE_P))]
        opt_in = int(rng.random() < (.62 if ch != "sales_rep" else .9))
        cust = dict(customer_id=cid, acquired_date=acq.isoformat(), acquisition_channel=ch,
                    customer_type=ctype, region=region, age_band=age, email_opt_in=opt_in)
        customers.append(cust)
        SPECS.append(dict(cust=cust, year=year, k=k, wholesale=wholesale, m=m, e=e, acq=acq))
        ENGAGE[cid] = e
        cid += 1

# Exact repeat-within-90-days counts per cohort (year x channel), so the Module 06 effect never depends on luck.
strata = {}
for sp in SPECS:
    key = (sp["year"], "wholesale" if sp["wholesale"] else sp["k"])
    strata.setdefault(key, []).append(sp)
for (year, k), members in strata.items():
    p = .70 if k == "wholesale" else P_REPEAT90[year][k]
    n_rep = int(round(p * len(members)))
    chosen = set(rng.choice(len(members), n_rep, replace=False).tolist())
    for i, sp in enumerate(members):
        sp["repeat90"] = i in chosen

for sp in SPECS:
    cust, wholesale, m, e, acq = sp["cust"], sp["wholesale"], sp["m"], sp["e"], sp["acq"]
    a = date_to_day(acq)
    orders = [a]
    if sp["repeat90"]:
        d = a + 1 + int(min(rng.exponential(28), 88))
        if d <= NDAYS - 1:
            orders.append(d)
    late_start = a + 91
    if wholesale:
        rate = 4.0
    elif sp["repeat90"]:
        rate = 1.1 * m ** 1.5 * e ** 1.0
    else:
        rate = 0.30 * m * e ** 1.0
    if late_start <= NDAYS - 1:
        days = np.arange(late_start, NDAYS)
        p = rate / 365.0 * SEASON[days] / AVG_SEASON
        hit = days[rng.random(len(days)) < p]
        orders += hit.tolist()
    cust_orders[cust["customer_id"]] = sorted(set(orders))

# ---------------------------------------------------------- loyalty program
loyalty = []
for c in customers:
    if c["customer_type"] != "consumer":
        continue
    ods = cust_orders[c["customer_id"]]
    decision = max(date_to_day(LAUNCH), ods[0] + 90)
    if decision > NDAYS - 1:
        continue
    p_join = 1.0 / (1.0 + np.exp(-(-3.2 + 2.4 * np.log(ENGAGE[c["customer_id"]]))))
    if rng.random() < p_join:
        join = decision + int(rng.integers(0, 61))
        if join <= NDAYS - 1:
            loyalty.append(dict(customer_id=c["customer_id"], join_date=day_to_date(join).isoformat()))
            extra = []
            for d in ods:
                if d > join and rng.random() < .10:
                    e = d + 1 + int(rng.exponential(15))
                    if e <= NDAYS - 1 and e not in ods:
                        extra.append(e)
            cust_orders[c["customer_id"]] = sorted(set(ods + extra))
member_ids = {l["customer_id"] for l in loyalty}
cust_by_id = {c["customer_id"]: c for c in customers}

# ------------------------------------------------------ orders, lines, returns
all_orders = []
for cid_, ods in cust_orders.items():
    for d in ods:
        all_orders.append((d, cid_))
all_orders.sort()

orders, lines, returns_ = [], [], []
oid = 100001
rid = 1
for d, cid_ in all_orders:
    c = cust_by_id[cid_]
    wholesale = c["customer_type"] == "wholesale"
    odate = day_to_date(d)
    status = "cancelled" if rng.random() < .02 else "shipped"
    ship = None if status == "cancelled" else odate + dt.timedelta(days=int(rng.integers(3, 11) if wholesale else rng.integers(1, 5)))
    if wholesale:
        nlines = 2 + int(rng.poisson(2))
    else:
        nlines = min(5, 1 + int(rng.poisson(0.6)))
    promo_p, promo_vals = (.45, [.15, .20, .25]) if odate.month == 11 else (.30, [.10]) if odate.month == 7 else (.06, [.05, .10])
    merch = 0.0
    order_lines = []
    for ln in range(1, nlines + 1):
        cat = CAT_LIST[int(rng.choice(len(CAT_LIST), p=CAT_P))]
        prod = PROD_BY_CAT[cat][int(rng.integers(0, len(PROD_BY_CAT[cat])))]
        if wholesale:
            qty = int(rng.integers(2, 7))
            disc = .15
        else:
            qty = int(rng.choice([1, 2, 3], p=[.85, .12, .03]))
            disc = float(rng.choice(promo_vals)) if rng.random() < promo_p else 0.0
        lt = round(qty * prod["list_price"] * (1 - disc), 2)
        merch += lt
        order_lines.append(dict(order_id=oid, line_no=ln, product_id=prod["product_id"], quantity=qty,
                                unit_price=prod["list_price"], discount_pct=disc, line_total=lt, category=cat))
    merch = round(merch, 2)
    sfee = 0.0 if (wholesale or merch >= 75) else 7.95
    if wholesale:
        channel = "phone" if rng.random() < .8 else "web"
    else:
        channel = "web" if rng.random() < .70 else "app"
    orders.append(dict(order_id=oid, customer_id=cid_, order_date=odate.isoformat(),
                       ship_date=ship.isoformat() if ship else None, channel=channel, status=status,
                       shipping_fee=sfee, order_total=merch))
    for ol in order_lines:
        lines.append({k: v for k, v in ol.items() if k != "category"})
        if status == "shipped" and rng.random() < RETURN_RATE[ol["category"]]:
            rdate = ship + dt.timedelta(days=int(rng.integers(3, 31)))
            if rdate <= END:
                reason = str(rng.choice(["Did not fit", "Defective", "Not as described", "Changed mind", "Arrived late"],
                                        p=[.34, .18, .16, .27, .05]))
                returns_.append(dict(return_id=rid, order_id=oid, line_no=ol["line_no"],
                                     return_date=rdate.isoformat(), reason=reason, refund_amount=ol["line_total"]))
                rid += 1
    oid += 1

# ---------------------------------------------------- finance (separate system)
fin = {}
cancelled = {o["order_id"] for o in orders if o["status"] == "cancelled"}
ship_by_order = {o["order_id"]: o["ship_date"] for o in orders}
for ln in lines:
    if ln["order_id"] in cancelled:
        continue
    m = ship_by_order[ln["order_id"]][:7]
    fin[m] = fin.get(m, 0.0) + ln["line_total"]
for r in returns_:
    m = r["return_date"][:7]
    fin[m] = fin.get(m, 0.0) - r["refund_amount"]
finance_rows = [dict(month=m, net_revenue=round(v, 2)) for m, v in sorted(fin.items()) if m <= "2025-12"]

# ------------------------------------------------------------- marketing
monthly_orders = {}
for o in orders:
    monthly_orders[o["order_date"][:7]] = monthly_orders.get(o["order_date"][:7], 0) + 1
marketing = []
for y in (2023, 2024, 2025):
    for m in range(1, 13):
        key = f"{y}-{m:02d}"
        base_spend = {2023: 2500, 2024: 4500, 2025: 11000}[y]
        marketing.append(dict(month=key,
                              paid_social_spend=int(base_spend * float(rng.uniform(.85, 1.15))),
                              email_sends=int(24000 * SEASON_BY_MONTH[m] * (1 + (y - 2023) * .12) * float(rng.uniform(.92, 1.08))),
                              site_sessions=int(monthly_orders.get(key, 0) * float(rng.uniform(34, 40)))))

# ---------------------------------------------------------------- survey
q4_buyers = sorted({o["customer_id"] for o in orders
                    if o["order_date"] >= "2025-07-01" and cust_by_id[o["customer_id"]]["customer_type"] == "consumer"
                    and o["status"] == "shipped"})
ret_orders = {r["order_id"] for r in returns_}
cust_returned_q4 = {o["customer_id"] for o in orders if o["order_date"] >= "2025-07-01" and o["order_id"] in ret_orders}
RESP_P = {5: .155, 4: .103, 3: .021, 2: .005, 1: .0026}
survey = []
sid = 1
for c_id in q4_buyers:
    if c_id in cust_returned_q4:
        rating = int(rng.choice([1, 2, 3, 4, 5], p=[.20, .20, .22, .20, .18]))
    else:
        rating = int(rng.choice([1, 2, 3, 4, 5], p=[.07, .07, .16, .30, .40]))
    if rng.random() < RESP_P[rating] * 0.92:
        survey.append(dict(response_id=sid, customer_id=c_id, survey_date="2025-12-%02d" % int(rng.integers(1, 29)),
                           rating=rating, would_recommend=int(rating >= 4)))
        sid += 1
SURVEY_EMAILED = len(q4_buyers)

# ----------------------------------------------------------- churn pilot
pilot_ids = [int(x) for x in rng.choice([c["customer_id"] for c in customers if c["customer_type"] == "consumer"],
                                         2000, replace=False)]
actual = np.zeros(2000, dtype=int)
actual[rng.choice(2000, 100, replace=False)] = 1
pred = np.zeros(2000, dtype=int)
churners = np.where(actual == 1)[0]
keepers = np.where(actual == 0)[0]
pred[rng.choice(churners, 30, replace=False)] = 1
pred[rng.choice(keepers, 22, replace=False)] = 1
churn = [dict(customer_id=pilot_ids[i], predicted_churn=int(pred[i]), actual_churn=int(actual[i])) for i in range(2000)]

# ------------------------------------------- prepared summary tables (built by "the data team")
spend = {}
for o in orders:
    if o["status"] != "shipped":
        continue
    d_ = o["order_date"]
    rec = spend.setdefault(o["customer_id"], [0.0, 0.0, 0.0])
    if "2024-01-01" <= d_ <= "2024-06-30":
        rec[0] += o["order_total"]
    if "2025-01-01" <= d_ <= "2025-06-30":
        rec[1] += o["order_total"]
    if "2025-01-01" <= d_ <= "2025-12-31":
        rec[2] += o["order_total"]
join_by = {l_["customer_id"]: l_["join_date"] for l_ in loyalty}
spend_summary = []
for c in customers:
    if c["customer_type"] == "consumer" and c["acquired_date"] < "2025-01-01":
        r_ = spend.get(c["customer_id"], [0.0, 0.0, 0.0])
        spend_summary.append(dict(customer_id=c["customer_id"], acquired_date=c["acquired_date"],
                                  loyalty_member=int(c["customer_id"] in join_by), join_date=join_by.get(c["customer_id"]),
                                  spend_h1_2024=round(r_[0], 2), spend_h1_2025=round(r_[1], 2), spend_2025=round(r_[2], 2)))
resp_by = {s_["customer_id"]: s_["rating"] for s_ in survey}
survey_audit = [dict(customer_id=c_, responded=int(c_ in resp_by), rating=resp_by.get(c_),
                     returned_item=int(c_ in cust_returned_q4)) for c_ in q4_buyers]

# ---- repeat_cohort: consumer customers whose first shipped order fell between January 1 and September 30 of 2024 or 2025
lines_by_order = {}
for l_ in lines:
    lines_by_order.setdefault(l_["order_id"], []).append(l_)
ret_lines = {(r_["order_id"], r_["line_no"]) for r_ in returns_}
cost_by_prod = {p_["product_id"]: p_["unit_cost"] for p_ in products}
orders_by_cust = {}
for o_ in orders:
    if o_["status"] == "shipped":
        orders_by_cust.setdefault(o_["customer_id"], []).append(o_)
order_gp = {}
for o_id, ls_ in lines_by_order.items():
    order_gp[o_id] = sum(l_["line_total"] - l_["quantity"] * cost_by_prod[l_["product_id"]]
                         for l_ in ls_ if (l_["order_id"], l_["line_no"]) not in ret_lines)
order_rev_net = {}
for o_id, ls_ in lines_by_order.items():
    order_rev_net[o_id] = sum(l_["line_total"] for l_ in ls_ if (l_["order_id"], l_["line_no"]) not in ret_lines)
repeat_cohort = []
for c in customers:
    if c["customer_type"] != "consumer":
        continue
    os_ = sorted(orders_by_cust.get(c["customer_id"], []), key=lambda x: x["order_date"])
    if not os_:
        continue
    fo = dt.date.fromisoformat(os_[0]["order_date"])
    if not ((dt.date(2024, 1, 1) <= fo <= dt.date(2024, 9, 30)) or (dt.date(2025, 1, 1) <= fo <= dt.date(2025, 9, 30))):
        continue
    d90 = fo + dt.timedelta(days=90)
    d365 = fo + dt.timedelta(days=365)
    in90 = [x for x in os_ if dt.date.fromisoformat(x["order_date"]) <= d90]
    in365 = [x for x in os_ if dt.date.fromisoformat(x["order_date"]) <= d365]
    repeat_cohort.append(dict(customer_id=c["customer_id"], first_order_date=fo.isoformat(), cohort_year=fo.year,
                              acquisition_channel=c["acquisition_channel"], repeat_90=int(len(in90) > 1), orders_90d=len(in90),
                              revenue_90d=round(sum(order_rev_net[x["order_id"]] for x in in90), 2),
                              gross_profit_90d=round(sum(order_gp[x["order_id"]] for x in in90), 2),
                              gross_profit_365d=round(sum(order_gp[x["order_id"]] for x in in365), 2) if fo.year == 2024 else None))

# --------------------------------------------------------------- Anscombe
x123 = [10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5]
x4 = [8, 8, 8, 8, 8, 8, 8, 19, 8, 8, 8]
y1 = [8.04, 6.95, 7.58, 8.81, 8.33, 9.96, 7.24, 4.26, 10.84, 4.82, 5.68]
y2 = [9.14, 8.14, 8.74, 8.77, 9.26, 8.10, 6.13, 3.10, 9.13, 7.26, 4.74]
y3 = [7.46, 6.77, 12.74, 7.11, 7.81, 8.84, 6.08, 5.39, 8.15, 6.42, 5.73]
y4 = [6.58, 5.76, 7.71, 8.84, 8.47, 7.04, 5.25, 12.50, 5.56, 7.91, 6.89]
anscombe = []
for name, xs, ys in (("I", x123, y1), ("II", x123, y2), ("III", x123, y3), ("IV", x4, y4)):
    for x, y in zip(xs, ys):
        anscombe.append(dict(dataset=name, x=x, y=y))

# ===================================================================== write
def write_csv(path, rows, fields):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow({k: ("" if r.get(k) is None else r.get(k)) for k in fields})


F = {
    "customers": ["customer_id", "acquired_date", "acquisition_channel", "customer_type", "region", "age_band", "email_opt_in"],
    "products": ["product_id", "product_name", "category", "list_price", "unit_cost", "color"],
    "orders": ["order_id", "customer_id", "order_date", "ship_date", "channel", "status", "shipping_fee", "order_total"],
    "order_items": ["order_id", "line_no", "product_id", "quantity", "unit_price", "discount_pct", "line_total"],
    "returns": ["return_id", "order_id", "line_no", "return_date", "reason", "refund_amount"],
    "loyalty_members": ["customer_id", "join_date"],
    "marketing_monthly": ["month", "paid_social_spend", "email_sends", "site_sessions"],
    "survey_responses": ["response_id", "customer_id", "survey_date", "rating", "would_recommend"],
    "churn_model_scores": ["customer_id", "predicted_churn", "actual_churn"],
    "customer_spend_summary": ["customer_id", "acquired_date", "loyalty_member", "join_date", "spend_h1_2024", "spend_h1_2025", "spend_2025"],
    "survey_audit": ["customer_id", "responded", "rating", "returned_item"],
    "repeat_cohort": ["customer_id", "first_order_date", "cohort_year", "acquisition_channel", "repeat_90", "orders_90d",
                      "revenue_90d", "gross_profit_90d", "gross_profit_365d"],
}
DATA = {"customers": customers, "products": products, "orders": orders, "order_items": lines, "returns": returns_,
        "loyalty_members": loyalty, "marketing_monthly": marketing, "survey_responses": survey,
        "churn_model_scores": churn, "customer_spend_summary": spend_summary, "survey_audit": survey_audit,
        "repeat_cohort": repeat_cohort}

# clean CSVs and supplements
for t in ("customers", "products", "orders", "order_items", "returns"):
    write_csv(os.path.join(HERE, "clean_csv", f"{t}.csv"), DATA[t], F[t])
for t in ("loyalty_members", "marketing_monthly", "survey_responses", "churn_model_scores", "customer_spend_summary", "survey_audit", "repeat_cohort"):
    write_csv(os.path.join(HERE, "supplements", f"{t}.csv"), DATA[t], F[t])
write_csv(os.path.join(HERE, "supplements", "anscombe.csv"), anscombe, ["dataset", "x", "y"])

# SQLite
db_path = os.path.join(HERE, "lantern_clean.sqlite")
if os.path.exists(db_path):
    os.remove(db_path)
con = sqlite3.connect(db_path)
con.executescript("""
CREATE TABLE customers (customer_id INTEGER PRIMARY KEY, acquired_date TEXT NOT NULL, acquisition_channel TEXT NOT NULL,
  customer_type TEXT NOT NULL, region TEXT NOT NULL, age_band TEXT, email_opt_in INTEGER NOT NULL);
CREATE TABLE products (product_id INTEGER PRIMARY KEY, product_name TEXT NOT NULL, category TEXT NOT NULL,
  list_price REAL NOT NULL, unit_cost REAL NOT NULL, color TEXT NOT NULL);
CREATE TABLE orders (order_id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL REFERENCES customers(customer_id),
  order_date TEXT NOT NULL, ship_date TEXT, channel TEXT NOT NULL, status TEXT NOT NULL, shipping_fee REAL NOT NULL,
  order_total REAL NOT NULL);
CREATE TABLE order_items (order_id INTEGER NOT NULL REFERENCES orders(order_id), line_no INTEGER NOT NULL,
  product_id INTEGER NOT NULL REFERENCES products(product_id), quantity INTEGER NOT NULL, unit_price REAL NOT NULL,
  discount_pct REAL NOT NULL, line_total REAL NOT NULL, PRIMARY KEY (order_id, line_no));
CREATE TABLE returns (return_id INTEGER PRIMARY KEY, order_id INTEGER NOT NULL, line_no INTEGER NOT NULL,
  return_date TEXT NOT NULL, reason TEXT NOT NULL, refund_amount REAL NOT NULL);
CREATE TABLE loyalty_members (customer_id INTEGER PRIMARY KEY REFERENCES customers(customer_id), join_date TEXT NOT NULL);
CREATE TABLE marketing_monthly (month TEXT PRIMARY KEY, paid_social_spend INTEGER, email_sends INTEGER, site_sessions INTEGER);
CREATE TABLE survey_responses (response_id INTEGER PRIMARY KEY, customer_id INTEGER, survey_date TEXT, rating INTEGER, would_recommend INTEGER);
CREATE TABLE churn_model_scores (customer_id INTEGER PRIMARY KEY, predicted_churn INTEGER, actual_churn INTEGER);
CREATE TABLE customer_spend_summary (customer_id INTEGER PRIMARY KEY, acquired_date TEXT, loyalty_member INTEGER, join_date TEXT,
  spend_h1_2024 REAL, spend_h1_2025 REAL, spend_2025 REAL);
CREATE TABLE survey_audit (customer_id INTEGER PRIMARY KEY, responded INTEGER, rating INTEGER, returned_item INTEGER);
CREATE TABLE repeat_cohort (customer_id INTEGER PRIMARY KEY, first_order_date TEXT, cohort_year INTEGER, acquisition_channel TEXT,
  repeat_90 INTEGER, orders_90d INTEGER, revenue_90d REAL, gross_profit_90d REAL, gross_profit_365d REAL);
""")
for t, rows in DATA.items():
    cols = F[t]
    con.executemany(f"INSERT INTO {t} ({','.join(cols)}) VALUES ({','.join('?' * len(cols))})",
                    [tuple(r.get(c) for c in cols) for r in rows])
con.commit()
con.close()

# ----------------------------------------------------------------- RAW files
RAW = os.path.join(HERE, "raw")
REGION_VARIANTS = {"Northeast": ["NE", "north east", "N.E.", "Northeast "], "Southeast": ["SE", "south east", "S.E."],
                   "Midwest": ["MW", "Mid-West", "mid west"], "Southwest": ["SW", "south west"],
                   "West": ["W", "west", "Western"], "Northwest": ["NW", "north west", "Pacific NW"]}
raw_customers = []
for c in customers:
    r = dict(c)
    if rng.random() < .30:
        r["region"] = str(rng.choice(REGION_VARIANTS[c["region"]]))
    if c["age_band"] is None:
        r["age_band"] = str(rng.choice(["", "unknown", "N/A", "n/a", "-"]))
    r["email_opt_in"] = str(rng.choice(["Y", "yes", "1", "TRUE"] if c["email_opt_in"] else ["N", "no", "0", "FALSE"]))
    raw_customers.append(r)
write_csv(os.path.join(RAW, "customers_raw.csv"), raw_customers, F["customers"])

raw_products = []
for p in products:
    r = dict(p)
    r["color"] = str(rng.choice(COLOR_VARIANTS[p["color"]]))
    if rng.random() < .25:
        r["list_price"] = f"${p['list_price']:.2f}"
    if rng.random() < .15:
        r["category"] = r["category"].lower() if rng.random() < .5 else r["category"] + " "
    raw_products.append(r)
write_csv(os.path.join(RAW, "products_raw.csv"), raw_products, F["products"])


def us_date(iso):
    if not iso:
        return iso
    y, m, d = iso.split("-")
    return f"{m}/{d}/{y}"


raw_orders = []
legacy_rows = 0
for o in orders:
    r = dict(o)
    if o["order_date"] < "2023-04-01":  # legacy system migration used US-style dates
        r["order_date"] = us_date(o["order_date"])
        r["ship_date"] = us_date(o["ship_date"])
        legacy_rows += 1
    raw_orders.append(r)
n_dups = int(round(len(orders) * .012))
dup_idx = rng.choice(len(raw_orders), n_dups, replace=False)
dups = [dict(raw_orders[int(i)]) for i in dup_idx]
tests = []
for k in range(45):
    d = day_to_date(int(rng.integers(0, NDAYS)))
    tests.append(dict(order_id=900001 + k, customer_id=0, order_date=d.isoformat(),
                      ship_date=(d + dt.timedelta(days=2)).isoformat(), channel="web", status="shipped",
                      shipping_fee=0.0, order_total=float(rng.choice([1.00, 9999.99]))))
raw_all = raw_orders + dups + tests
write_csv(os.path.join(RAW, "orders_raw.csv"), raw_all, F["orders"])
write_csv(os.path.join(RAW, "order_items_raw.csv"), lines, F["order_items"])
raw_returns = []
for r in returns_:
    rr = dict(r)
    if rng.random() < .25:
        rr["reason"] = str(rng.choice([r["reason"].lower(), r["reason"].upper(), r["reason"] + " "]))
    raw_returns.append(rr)
write_csv(os.path.join(RAW, "returns_raw.csv"), raw_returns, F["returns"])
write_csv(os.path.join(RAW, "finance_monthly_revenue.csv"), finance_rows, ["month", "net_revenue"])

# --------------------------------------------------------- data dictionary
DICT = [
    ("customers", "customer_id", "Unique number for each customer account", "1001"),
    ("customers", "acquired_date", "Date of the customer's first order", "2024-03-18"),
    ("customers", "acquisition_channel", "Marketing source that brought the customer in", "paid_social"),
    ("customers", "customer_type", "Individual shopper (consumer) or business buyer (wholesale)", "consumer"),
    ("customers", "region", "Sales region of the customer's address", "Northeast"),
    ("customers", "age_band", "Age range the customer chose, if they chose one", "25-34"),
    ("customers", "email_opt_in", "Whether the customer agreed to receive marketing email (1 yes, 0 no)", "1"),
    ("products", "product_id", "Unique number for each product", "14"),
    ("products", "product_name", "Name shown in the catalog", "Ridge 45L Pack"),
    ("products", "category", "Product family", "Packs"),
    ("products", "list_price", "Advertised price in US dollars", "189.99"),
    ("products", "unit_cost", "What the product costs the company in US dollars", "104.50"),
    ("products", "color", "Color shown in the catalog", "Olive"),
    ("orders", "order_id", "Unique number for each order", "100245"),
    ("orders", "customer_id", "The customer who placed the order", "1020"),
    ("orders", "order_date", "Date the order was placed", "2024-05-02"),
    ("orders", "ship_date", "Date the order left the warehouse (blank if cancelled)", "2024-05-04"),
    ("orders", "channel", "How the order was placed", "web"),
    ("orders", "status", "shipped or cancelled", "shipped"),
    ("orders", "shipping_fee", "Shipping charged to the customer in US dollars", "7.95"),
    ("orders", "order_total", "Merchandise total of the order in US dollars, before shipping", "212.40"),
    ("order_items", "order_id", "The order this line belongs to", "100245"),
    ("order_items", "line_no", "Position of the line within its order (1, 2, 3 ...)", "2"),
    ("order_items", "product_id", "The product on this line", "14"),
    ("order_items", "quantity", "Number of units on this line", "1"),
    ("order_items", "unit_price", "Price per unit before discount", "189.99"),
    ("order_items", "discount_pct", "Promotion discount as a fraction (0.15 is 15 percent)", "0.15"),
    ("order_items", "line_total", "quantity times unit_price after discount", "161.49"),
    ("returns", "return_id", "Unique number for each return", "310"),
    ("returns", "order_id", "The order the item came from", "100245"),
    ("returns", "line_no", "The line within that order that was returned", "2"),
    ("returns", "return_date", "Date the return was received", "2024-05-19"),
    ("returns", "reason", "Reason the customer gave", "Did not fit"),
    ("returns", "refund_amount", "Amount refunded in US dollars", "161.49"),
    ("loyalty_members", "customer_id", "Customer who joined the loyalty program", "1022"),
    ("loyalty_members", "join_date", "Date the customer joined (program launched 2024-07-01)", "2024-08-09"),
    ("marketing_monthly", "month", "Calendar month (YYYY-MM)", "2025-03"),
    ("marketing_monthly", "paid_social_spend", "Paid social advertising spend in US dollars", "10800"),
    ("marketing_monthly", "email_sends", "Marketing emails sent in the month", "29000"),
    ("marketing_monthly", "site_sessions", "Website visits in the month", "36500"),
    ("survey_responses", "response_id", "Unique number for each survey response", "12"),
    ("survey_responses", "customer_id", "The customer who responded", "2310"),
    ("survey_responses", "survey_date", "Date of the response", "2025-12-04"),
    ("survey_responses", "rating", "Satisfaction from 1 (very unhappy) to 5 (very happy)", "5"),
    ("survey_responses", "would_recommend", "1 if the customer would recommend the company", "1"),
    ("churn_model_scores", "customer_id", "Customer scored in the vendor pilot", "1450"),
    ("churn_model_scores", "predicted_churn", "Vendor model prediction (1 means predicted to leave)", "0"),
    ("churn_model_scores", "actual_churn", "What happened in the next 6 months (1 means the customer left)", "0"),
    ("customer_spend_summary", "customer_id", "Consumer customer acquired before 2025", "1"),
    ("customer_spend_summary", "acquired_date", "Date of the customer's first order", "1"),
    ("customer_spend_summary", "loyalty_member", "1 if the customer ever joined the loyalty program", "1"),
    ("customer_spend_summary", "join_date", "Date the customer joined (blank if not a member)", "1"),
    ("customer_spend_summary", "spend_h1_2024", "Shipped order_total from January 1 to June 30, 2024, before the program launched", "1"),
    ("customer_spend_summary", "spend_h1_2025", "Shipped order_total from January 1 to June 30, 2025", "1"),
    ("customer_spend_summary", "spend_2025", "Shipped order_total for calendar 2025", "1"),
    ("survey_audit", "customer_id", "Customer emailed the satisfaction survey (bought July to December 2025)", "1"),
    ("survey_audit", "responded", "1 if the customer answered the survey", "1"),
    ("survey_audit", "rating", "Survey rating from 1 to 5 (blank if the customer did not respond)", "1"),
    ("survey_audit", "returned_item", "1 if the customer returned something from an order placed July to December 2025", "1"),
    ("repeat_cohort", "customer_id", "Consumer customer whose first shipped order fell between January 1 and September 30 of 2024 or 2025", "1"),
    ("repeat_cohort", "first_order_date", "Date of the customer's first shipped order", "1"),
    ("repeat_cohort", "cohort_year", "Year of the first order (2024 or 2025)", "1"),
    ("repeat_cohort", "acquisition_channel", "Marketing source that brought the customer in", "1"),
    ("repeat_cohort", "repeat_90", "1 if the customer placed a second shipped order within 90 days after the first", "1"),
    ("repeat_cohort", "orders_90d", "Shipped orders within 90 days of the first order, including the first", "1"),
    ("repeat_cohort", "revenue_90d", "Merchandise revenue in those orders, after removing returned lines", "1"),
    ("repeat_cohort", "gross_profit_90d", "Revenue minus product cost in those orders, after removing returned lines", "1"),
    ("repeat_cohort", "gross_profit_365d", "The same measure over 365 days (blank for 2025 customers, who don't have a full year yet)", "1"),
]
# Every example value in the dictionary is taken from a real row, so learners can find it in the files.
lines_by_order = {}
for l_ in lines:
    lines_by_order.setdefault(l_["order_id"], []).append(l_)
pcat = {p_["product_id"]: p_ for p_ in products}
ex_order = next(o_ for o_ in orders if o_["order_date"].startswith("2024-05") and o_["status"] == "shipped"
                and len(lines_by_order[o_["order_id"]]) == 1
                and pcat[lines_by_order[o_["order_id"]][0]["product_id"]]["category"] == "Packs"
                and lines_by_order[o_["order_id"]][0]["quantity"] == 1
                and lines_by_order[o_["order_id"]][0]["discount_pct"] == 0)
ex_line = lines_by_order[ex_order["order_id"]][0]
ex_rows = {"customers": cust_by_id[ex_order["customer_id"]], "products": pcat[ex_line["product_id"]],
           "orders": ex_order, "order_items": ex_line, "returns": returns_[0], "loyalty_members": loyalty[0],
           "marketing_monthly": next(m_ for m_ in marketing if m_["month"] == "2025-03"),
           "survey_responses": survey[0], "churn_model_scores": churn[0],
           "customer_spend_summary": next(r_ for r_ in spend_summary if r_["loyalty_member"] == 1),
           "survey_audit": next(r_ for r_ in survey_audit if r_["responded"] == 1),
           "repeat_cohort": next(r_ for r_ in repeat_cohort if r_["cohort_year"] == 2024 and r_["repeat_90"] == 1)}
def fmt(v):
    return "" if v is None else str(v)
write_csv(os.path.join(HERE, "data_dictionary.csv"),
          [dict(table=t, column=c, description=d, example_value=fmt(ex_rows[t][c])) for t, c, d, e in DICT],
          ["table", "column", "description", "example_value"])

# ------------------------------------------------------------- self-checks
con = sqlite3.connect(db_path)
q = lambda sql: con.execute(sql).fetchall()
print("rows:", {t: q(f"SELECT COUNT(*) FROM {t}")[0][0] for t in DATA})
print("raw order rows:", len(raw_all), "dups:", n_dups, "tests:", len(tests), "legacy-date rows:", legacy_rows)
print("repeat90 by year/channel (first orders Jan-Sep):")
rows = q("""
WITH first AS (SELECT customer_id, MIN(order_date) fo FROM orders WHERE status='shipped' GROUP BY customer_id),
f2 AS (SELECT f.customer_id, f.fo, c.acquisition_channel ch, substr(f.fo,1,4) yr,
  (SELECT COUNT(*) FROM orders o WHERE o.customer_id=f.customer_id AND o.order_date>f.fo
     AND o.order_date<=date(f.fo,'+90 day') AND o.status='shipped') n2
  FROM first f JOIN customers c USING(customer_id)
  WHERE substr(f.fo,6,2) BETWEEN '01' AND '09' AND f.fo>='2024-01-01')
SELECT yr, ch, COUNT(*), ROUND(AVG(n2>0)*100,1) FROM f2 GROUP BY yr, ch ORDER BY yr, ch""")
for r in rows:
    print("  ", r)
print(" overall:", q("""
WITH first AS (SELECT customer_id, MIN(order_date) fo FROM orders WHERE status='shipped' GROUP BY customer_id),
f2 AS (SELECT f.customer_id, substr(f.fo,1,4) yr,
  (SELECT COUNT(*) FROM orders o WHERE o.customer_id=f.customer_id AND o.order_date>f.fo
     AND o.order_date<=date(f.fo,'+90 day') AND o.status='shipped') n2
  FROM first f WHERE substr(f.fo,6,2) BETWEEN '01' AND '09' AND f.fo>='2024-01-01')
SELECT yr, COUNT(*), ROUND(AVG(n2>0)*100,1) FROM f2 GROUP BY yr"""))
vals = sorted(r[0] for r in q("SELECT order_total FROM orders WHERE status='shipped'"))
print("order_total mean %.2f median %.2f max %.2f" % (np.mean(vals), np.median(vals), max(vals)))
print("revenue by year (order_date, shipped):", q("SELECT substr(order_date,1,4), ROUND(SUM(order_total)) FROM orders WHERE status='shipped' GROUP BY 1"))
print("loyalty members:", len(loyalty))
print("H1-2024 spend/customer, customers acquired before 2024, members vs non:", q("""
SELECT CASE WHEN l.customer_id IS NULL THEN 'non' ELSE 'member' END g, COUNT(DISTINCT c.customer_id),
 ROUND(SUM(o.order_total)*1.0/COUNT(DISTINCT c.customer_id),1)
FROM customers c LEFT JOIN loyalty_members l USING(customer_id)
LEFT JOIN orders o ON o.customer_id=c.customer_id AND o.status='shipped' AND o.order_date BETWEEN '2024-01-01' AND '2024-06-30'
WHERE c.acquired_date<'2024-01-01' AND c.customer_type='consumer' GROUP BY g"""))
print("H1-2025 spend/customer same group:", q("""
SELECT CASE WHEN l.customer_id IS NULL THEN 'non' ELSE 'member' END g,
 ROUND(SUM(o.order_total)*1.0/COUNT(DISTINCT c.customer_id),1)
FROM customers c LEFT JOIN loyalty_members l USING(customer_id)
LEFT JOIN orders o ON o.customer_id=c.customer_id AND o.status='shipped' AND o.order_date BETWEEN '2025-01-01' AND '2025-06-30'
WHERE c.acquired_date<'2024-01-01' AND c.customer_type='consumer' GROUP BY g"""))
print("2025 annual spend/customer members vs non (all consumers active in data):", q("""
SELECT CASE WHEN l.customer_id IS NULL THEN 'non' ELSE 'member' END g, COUNT(DISTINCT c.customer_id),
 ROUND(SUM(o.order_total)*1.0/COUNT(DISTINCT c.customer_id),1)
FROM customers c LEFT JOIN loyalty_members l USING(customer_id)
LEFT JOIN orders o ON o.customer_id=c.customer_id AND o.status='shipped' AND o.order_date BETWEEN '2025-01-01' AND '2025-12-31'
WHERE c.customer_type='consumer' AND c.acquired_date<'2025-01-01' GROUP BY g"""))
print("monthly finance sample:", finance_rows[:3], "...", finance_rows[-3:])
tot_fin = sum(r["net_revenue"] for r in finance_rows)
tot_raw = sum(float(r["order_total"]) for r in raw_all)
print("finance total %.0f | raw order_total total (all rows) %.0f" % (tot_fin, tot_raw))
print("survey emailed:", SURVEY_EMAILED, "responses:", len(survey), "response rate %.1f%%" % (100 * len(survey) / SURVEY_EMAILED),
      "satisfied (4-5) among respondents %.1f%%" % (100 * sum(1 for s in survey if s["rating"] >= 4) / len(survey)))
tp = sum(1 for c in churn if c["predicted_churn"] == 1 and c["actual_churn"] == 1)
fp = sum(1 for c in churn if c["predicted_churn"] == 1 and c["actual_churn"] == 0)
fn = sum(1 for c in churn if c["predicted_churn"] == 0 and c["actual_churn"] == 1)
tn = 2000 - tp - fp - fn
print("churn TP/FP/FN/TN", tp, fp, fn, tn, "accuracy %.3f" % ((tp + tn) / 2000), "recall %.2f precision %.2f" % (tp / (tp + fn), tp / (tp + fp)))
for name in ("I", "II", "III", "IV"):
    xs = np.array([a["x"] for a in anscombe if a["dataset"] == name], float)
    ys = np.array([a["y"] for a in anscombe if a["dataset"] == name], float)
    print("Anscombe", name, "mean x %.2f y %.2f r %.3f" % (xs.mean(), ys.mean(), np.corrcoef(xs, ys)[0, 1]))
con.close()



# ---- Module 03 tie-out: clean the raw files the way learners should, and compare with finance, month by month
def _read(path):
    with open(path, encoding="utf-8") as f_:
        return list(csv.DictReader(f_))
_o = _read(os.path.join(RAW, "orders_raw.csv"))
_seen, _clean = set(), []
for r_ in _o:
    if r_["customer_id"] == "0" or r_["status"] == "cancelled":
        continue
    if r_["order_id"] in _seen:
        continue
    _seen.add(r_["order_id"])
    _clean.append(r_)
def _iso(d_):
    if "/" in d_:
        m_, dd_, y_ = d_.split("/")
        return "%s-%s-%s" % (y_, m_, dd_)
    return d_
_net = {}
for r_ in _clean:
    k_ = _iso(r_["ship_date"])[:7]
    _net[k_] = _net.get(k_, 0.0) + float(r_["order_total"])
for r_ in _read(os.path.join(RAW, "returns_raw.csv")):
    k_ = r_["return_date"][:7]
    _net[k_] = _net.get(k_, 0.0) - float(r_["refund_amount"])
_fin = {r_["month"]: float(r_["net_revenue"]) for r_ in _read(os.path.join(RAW, "finance_monthly_revenue.csv"))}
TIE_MAX = max(abs(_net.get(m_, 0.0) - v_) for m_, v_ in _fin.items())
print("tie-out max monthly difference vs finance: $%.4f over %d months" % (TIE_MAX, len(_fin)))
assert TIE_MAX < 0.05, "cleaning recipe no longer ties to finance"

# ------------------------------------------------------------ answer key
FAC = os.path.join(os.path.dirname(HERE), "facilitator")
os.makedirs(FAC, exist_ok=True)
con = sqlite3.connect(db_path)
q = lambda sql: con.execute(sql).fetchall()
L = []
w = L.append
w("# Lantern Peak case: answer key numbers\n")
w("Generated by build_case_data.py (seed %d). Every figure below comes straight from the data, so it stays correct if you rebuild.\n" % SEED)

w("## Table sizes (clean database)\n")
for t in DATA:
    w("- %s: %s rows" % (t, format(q("SELECT COUNT(*) FROM %s" % t)[0][0], ",")))

w("\n## Planted problems in the raw files (Modules 02 and 03)\n")
ids = {}
for r in raw_all:
    ids[r["order_id"]] = ids.get(r["order_id"], 0) + 1
n_dup_ids = sum(1 for v in ids.values() if v > 1)
dup_total = sum(float(r["order_total"]) for r in dups)
test_total = sum(r["order_total"] for r in tests)
amb = sum(1 for r in raw_orders if "/" in str(r["order_date"]) and int(str(r["order_date"]).split("/")[1]) <= 12)
w("- orders_raw.csv has %s rows but %s distinct order_id values. %s order_ids appear twice (exact duplicate rows from a re-import), worth $%s." % (
    format(len(raw_all), ","), format(len(ids), ","), n_dup_ids, format(round(dup_total), ",")))
w("- %s test orders carry customer_id 0, order_id 900001 and up, and totals of $1.00 or $9,999.99 (worth $%s). They have no order_items rows." % (len(tests), format(round(test_total), ",")))
w("- %s orders placed from January to March 2023 use US-style dates (MM/DD/YYYY) in both order_date and ship_date, a leftover from a system migration. %s of them have a day number of 12 or less, so a value like 03/04/2023 can be read two ways. Only days 13 to 31 give the format away. The check: order_id values rise with time, so sort by order_id and confirm the dates rise with them." % (legacy_rows, amb))
reg_raw = sorted({r["region"] for r in raw_customers})
w("- customers_raw.csv region has %d distinct spellings for 6 real regions: %s." % (len(reg_raw), ", ".join('"%s"' % x for x in reg_raw)))
w("- customers_raw.csv age_band marks a missing value five different ways (blank, unknown, N/A, n/a, -). email_opt_in uses eight spellings of yes and no (Y, yes, 1, TRUE, N, no, 0, FALSE).")
col_raw = sorted({r["color"] for r in raw_products})
w("- products_raw.csv color has %d spellings for 10 base colors (including red variants: Red, red, RED, Light Red, auburn, Crimson, Brick Red). Some variants overlap (Dark Blue could be Navy or Blue, Gold could be Yellow or Orange), so learners must document their judgment calls. About a quarter of list_price values carry a dollar sign, and a few category labels differ in case or trailing space." % len(col_raw))
w("- returns_raw.csv reason differs in case and trailing spaces for about a quarter of rows.")
w("- Joining orders_raw to order_items without removing duplicates double counts the lines of the %s duplicated orders (a fan-out)." % n_dup_ids)

w("\n## Module 02: why finance and the order system disagree (whole period, Jan 2023 to Dec 2025)\n")
raw_total = sum(float(r["order_total"]) for r in raw_all)
canc = q("SELECT ROUND(SUM(order_total),2) FROM orders WHERE status='cancelled'")[0][0]
spill = q("SELECT ROUND(SUM(order_total),2) FROM orders WHERE status='shipped' AND ship_date>='2026-01-01'")[0][0]
refunds = q("SELECT ROUND(SUM(refund_amount),2) FROM returns")[0][0]
fin_total = sum(r["net_revenue"] for r in finance_rows)
w("| Step | Amount | Running total |")
w("|---|---:|---:|")
run = raw_total
w("| Order system total, all rows as loaded | $%s | $%s |" % (format(round(raw_total, 2), ",.2f"), format(round(run, 2), ",.2f")))
for label, amt in (("Duplicate rows from the re-import", dup_total), ("Test orders", test_total), ("Cancelled orders", canc),
                   ("Shipped in January 2026 (finance reports through December)", spill), ("Refunds for returns", refunds)):
    run -= amt
    w("| Less: %s | $%s | $%s |" % (label, format(round(amt, 2), ",.2f"), format(round(run, 2), ",.2f")))
w("| Finance report total (finance_monthly_revenue.csv) | $%s | |" % format(round(fin_total, 2), ",.2f"))
w("\nThe two totals reconcile to within a cent. Month by month they also differ because the order system counts the order date and finance counts the ship date (and the refund month).")
w("\nWhere each system is the right answer: use the order system for demand (what customers asked to buy and when). Use finance for recognized revenue (what shipped, net of refunds).")

w("\n## Module 03: cleaning the raw files and tying out to finance\n")
w("Cleaning recipe: drop exact duplicate order rows (keep one per order_id), drop test orders (customer_id 0), drop cancelled orders, convert the January to March 2023 dates from MM/DD/YYYY to year-month-day, then total order_total by the month of ship_date and subtract refund_amount by the month of return_date.")
w("- Result: the recipe matches finance_monthly_revenue.csv in every one of the %d months, with a largest difference of $%.2f." % (len(_fin), TIE_MAX))
w("- Region labels: 24 spellings collapse to 6 (Northeast, Southeast, Midwest, Southwest, West, Northwest). Missing age bands: five spellings collapse to one missing value. email_opt_in: eight spellings collapse to 1 or 0.")
w("- If a learner skips the date fix, January to March 2023 will not tie out (the ship month is misread), which is the quickest way to prove the dates matter.")
w("- Fan-out demonstration: joining orders_raw (with its %d duplicate order rows) to order_items_raw counts those orders' lines twice, adding about $%s to revenue." % (n_dup_ids, format(round(sum(sum(l_["line_total"] for l_ in lines_by_order.get(int(d_["order_id"]), [])) for d_ in dups), 2), ",.2f")))
w("\n## Module 04: describing orders\n")
vals = [r[0] for r in q("SELECT order_total FROM orders WHERE status='shipped' ORDER BY order_total")]
cons = [r[0] for r in q("SELECT o.order_total FROM orders o JOIN customers c USING(customer_id) WHERE o.status='shipped' AND c.customer_type='consumer'")]
whol = [r[0] for r in q("SELECT o.order_total FROM orders o JOIN customers c USING(customer_id) WHERE o.status='shipped' AND c.customer_type='wholesale'")]
w("- Shipped orders: %s. Mean order total $%.2f, median $%.2f, maximum $%s. The mean sits well above the median because a small number of wholesale orders pull it up." % (format(len(vals), ","), np.mean(vals), np.median(vals), format(round(max(vals), 2), ",.2f")))
w("- Consumer orders only: mean $%.2f, median $%.2f. Wholesale orders (%s of them): mean $%s, median $%s." % (np.mean(cons), np.median(cons), len(whol), format(round(np.mean(whol), 2), ",.2f"), format(round(np.median(whol), 2), ",.2f")))
w("- 25th and 75th percentile of all shipped order totals: $%.2f and $%.2f." % (np.percentile(vals, 25), np.percentile(vals, 75)))
w("- Revenue by order year (shipped orders, order_total): " + ", ".join("%s $%s" % (r[0], format(round(r[1]), ",")) for r in q("SELECT substr(order_date,1,4), SUM(order_total) FROM orders WHERE status='shipped' GROUP BY 1")) + ".")
mrev = {r["month"]: r["net_revenue"] for r in finance_rows}
yr = {y: sum(v for m, v in mrev.items() if m.startswith(str(y))) for y in (2023, 2024, 2025)}
w("- Net revenue from finance: 2023 $%s, 2024 $%s (+%.0f%%), 2025 $%s (+%.0f%%)." % (format(round(yr[2023]), ","), format(round(yr[2024]), ","), 100 * (yr[2024] / yr[2023] - 1), format(round(yr[2025]), ","), 100 * (yr[2025] / yr[2024] - 1)))
mon_share = {m: sum(v for k, v in mrev.items() if k.endswith("-%02d" % m) and k < "2026") for m in range(1, 13)}
tot = sum(mon_share.values())
w("- Seasonality (share of three-year net revenue by calendar month): " + ", ".join("%s %.1f%%" % (dt.date(2000, m, 1).strftime("%b"), 100 * mon_share[m] / tot) for m in range(1, 13)) + ". November and December carry the peak.")
rr = q("""SELECT p.category, COUNT(*), SUM(CASE WHEN r.return_id IS NOT NULL THEN 1 ELSE 0 END)
FROM order_items i JOIN orders o USING(order_id) JOIN products p USING(product_id)
LEFT JOIN returns r ON r.order_id=i.order_id AND r.line_no=i.line_no WHERE o.status='shipped' GROUP BY p.category ORDER BY 3*1.0/2 DESC""")
w("- Return rate by category (returned lines divided by shipped lines): " + ", ".join("%s %.1f%%" % (c, 100 * r / n) for c, n, r in rr) + ". Returns that have not happened yet by the end of the data are missing, so recent months understate the true rate.")

chan = q("""SELECT c.acquisition_channel, COUNT(*), ROUND(AVG(o.order_total),2) FROM orders o JOIN customers c USING(customer_id)
WHERE o.status='shipped' AND c.customer_type='consumer' GROUP BY 1 ORDER BY 1""")
w("\n### Module 04 headline numbers (Activity 1)\n")
y25 = q("SELECT COUNT(*), ROUND(SUM(order_total),2), ROUND(AVG(order_total),2), COUNT(DISTINCT customer_id) FROM orders WHERE status='shipped' AND substr(order_date,1,4)='2025'")[0]
y24 = q("SELECT COUNT(*), ROUND(SUM(order_total),2), ROUND(AVG(order_total),2), COUNT(DISTINCT customer_id) FROM orders WHERE status='shipped' AND substr(order_date,1,4)='2024'")[0]
newc = {y_: q("SELECT COUNT(*) FROM customers WHERE substr(acquired_date,1,4)='%d'" % y_)[0][0] for y_ in (2024, 2025)}
w("| Measure | 2024 | 2025 | Change |")
w("|---|---:|---:|---:|")
w("| Shipped orders (by order date) | %s | %s | %+.0f%% |" % (format(y24[0], ","), format(y25[0], ","), 100 * (y25[0] / y24[0] - 1)))
w("| Merchandise revenue (sum of order_total, shipped orders) | $%s | $%s | %+.0f%% |" % (format(round(y24[1]), ","), format(round(y25[1]), ","), 100 * (y25[1] / y24[1] - 1)))
w("| Average order value (mean) | $%.2f | $%.2f | %+.0f%% |" % (y24[2], y25[2], 100 * (y25[2] / y24[2] - 1)))
w("| Customers who ordered | %s | %s | %+.0f%% |" % (format(y24[3], ","), format(y25[3], ","), 100 * (y25[3] / y24[3] - 1)))
w("| New customers | %s | %s | %+.0f%% |" % (format(newc[2024], ","), format(newc[2025], ","), 100 * (newc[2025] / newc[2024] - 1)))
rl = q("""SELECT strftime('%Y', o.order_date), COUNT(*), SUM(CASE WHEN r.return_id IS NOT NULL THEN 1 ELSE 0 END)
FROM order_items i JOIN orders o USING(order_id) LEFT JOIN returns r ON r.order_id=i.order_id AND r.line_no=i.line_no
WHERE o.status='shipped' AND substr(o.order_date,1,4) IN ('2024','2025') GROUP BY 1""")
w("| Share of shipped lines returned (by order year, recent returns still arriving) | %.1f%% | %.1f%% | |" % (100 * rl[0][2] / rl[0][1], 100 * rl[1][2] / rl[1][1]))
w("\nNet revenue from the finance report is the figure to quote for recognized revenue (2025: $%s, up %.0f%% on 2024). The order-system figures above are merchandise demand by order date, so the two differ by design (Module 02)." % (format(round(yr[2025]), ","), 100 * (yr[2025] / yr[2024] - 1)))
w("\n### Module 04 chart exercise: average order value by acquisition channel (consumer, shipped orders)\n")
w("| Channel | Orders | Mean order value |")
w("|---|---:|---:|")
for ch_, n_, a_ in chan:
    w("| %s | %s | $%.2f |" % (ch_, format(n_, ","), a_))
lo_, hi_ = min(a_ for _, _, a_ in chan), max(a_ for _, _, a_ in chan)
w("\nThe three channels sit within $%.2f of each other (%.1f%% of the average). A bar chart whose axis starts near $%d makes that gap look enormous. Starting the axis at zero shows it is small. Module 04 includes both versions as images (modules/images)." % (hi_ - lo_, 100 * (hi_ - lo_) / np.mean([a_ for _, _, a_ in chan]), int(lo_ // 10 * 10 - 10)))
w("\n## Module 05: auditing the leadership claims\n")
mem = q("""SELECT CASE WHEN l.customer_id IS NULL THEN 'non' ELSE 'member' END g, COUNT(DISTINCT c.customer_id), ROUND(SUM(o.order_total)*1.0/COUNT(DISTINCT c.customer_id),2)
FROM customers c LEFT JOIN loyalty_members l USING(customer_id)
LEFT JOIN orders o ON o.customer_id=c.customer_id AND o.status='shipped' AND o.order_date BETWEEN '2025-01-01' AND '2025-12-31'
WHERE c.customer_type='consumer' AND c.acquired_date<'2025-01-01' GROUP BY g""")
d = {g: (n, v) for g, n, v in mem}
w("- Claim 1, \"Loyalty members spend twice as much as everyone else\": 2025 spend per customer, consumers acquired before 2025: members $%.2f (%s customers) against non-members $%.2f (%s customers), a ratio of %.2f." % (d['member'][1], d['member'][0], d['non'][1], format(d['non'][0], ","), d['member'][1] / d['non'][1]))
pre = q("""SELECT CASE WHEN l.customer_id IS NULL THEN 'non' ELSE 'member' END g, COUNT(DISTINCT c.customer_id), ROUND(SUM(o.order_total)*1.0/COUNT(DISTINCT c.customer_id),2)
FROM customers c LEFT JOIN loyalty_members l USING(customer_id)
LEFT JOIN orders o ON o.customer_id=c.customer_id AND o.status='shipped' AND o.order_date BETWEEN '2024-01-01' AND '2024-06-30'
WHERE c.customer_type='consumer' AND c.acquired_date<'2024-01-01' GROUP BY g""")
dp = {g: (n, v) for g, n, v in pre}
post = q("""SELECT CASE WHEN l.customer_id IS NULL THEN 'non' ELSE 'member' END g, ROUND(SUM(o.order_total)*1.0/COUNT(DISTINCT c.customer_id),2)
FROM customers c LEFT JOIN loyalty_members l USING(customer_id)
LEFT JOIN orders o ON o.customer_id=c.customer_id AND o.status='shipped' AND o.order_date BETWEEN '2025-01-01' AND '2025-06-30'
WHERE c.customer_type='consumer' AND c.acquired_date<'2024-01-01' GROUP BY g""")
dq = dict(post)
w("- The check: the program launched on 2024-07-01. For consumers acquired before 2024, spend per customer in January to June 2024 (before the program existed) was $%.2f for the people who later joined (%s customers) and $%.2f for everyone else, a ratio of %.2f. The members were already better customers." % (dp['member'][1], dp['member'][0], dp['non'][1], dp['member'][1] / dp['non'][1]))
w("- Same customers, January to June 2025: members $%.2f, non-members $%.2f. From the pre-launch half-year to the same half a year later, members changed %.0f%% and non-members %.0f%%. The gap between them widened only a little, so most of the headline difference is who joined, with a modest program effect on top." % (dq['member'], dq['non'], 100 * (dq['member'] / dp['member'][1] - 1), 100 * (dq['non'] / dp['non'][1] - 1)))
w("- The same result comes from supplements/customer_spend_summary.csv (pivot spend_2025 and spend_h1_2024 by loyalty_member, filter acquired_date to before 2024 for the pre-launch comparison).")
w("- Traps in Claim 1: self-selection (heavy buyers joined), comparing a group to everyone else, and no pre-period. The tell is the before-launch comparison.")
resp = len(survey)
sat = sum(1 for s_ in survey if s_["rating"] >= 4)
resp_ids = {s_["customer_id"] for s_ in survey}
ret_rate_resp = sum(1 for c_ in resp_ids if c_ in cust_returned_q4) / len(resp_ids)
ret_rate_all = sum(1 for c_ in q4_buyers if c_ in cust_returned_q4) / len(q4_buyers)
w("- Claim 2, \"94 percent of customers are satisfied\": %s customers who bought from July to December 2025 were emailed the survey, and %s answered (%.1f%% response rate). Of those, %s rated 4 or 5, which is %.1f%%. Respondents are not a random sample: only %.1f%% of respondents returned something in that period, against %.1f%% of everyone emailed. The happiest customers answered most." % (format(SURVEY_EMAILED, ","), resp, 100 * resp / SURVEY_EMAILED, sat, 100 * sat / resp, 100 * ret_rate_resp, 100 * ret_rate_all))
w("- The same result comes from supplements/survey_audit.csv (pivot returned_item by responded).")
w("- Claim 3, \"The average order is $%.0f\": it is the mean. The median is $%.0f. Say which one, and why." % (np.mean(vals), np.median(vals)))
w("- Claim 4, \"Email drives sales\" (Module 06): see the correlation note below.")

w("\n## Module 06: why did repeat purchasing slip?\n")
w("Population: consumer customers whose first shipped order fell between January 1 and September 30 of the year, so every customer has a full 90-day window. Repeat means a second shipped order within 90 days after the first.\n")
rows = q("""
WITH first AS (SELECT o.customer_id, MIN(o.order_date) fo FROM orders o WHERE o.status='shipped' GROUP BY o.customer_id),
f2 AS (SELECT f.customer_id, c.acquisition_channel ch, substr(f.fo,1,4) yr,
  (SELECT COUNT(*) FROM orders o WHERE o.customer_id=f.customer_id AND o.order_date>f.fo
     AND o.order_date<=date(f.fo,'+90 day') AND o.status='shipped') n2
  FROM first f JOIN customers c USING(customer_id)
  WHERE c.customer_type='consumer' AND substr(f.fo,6,2) BETWEEN '01' AND '09' AND f.fo>='2024-01-01')
SELECT yr, ch, COUNT(*), SUM(n2>0) FROM f2 GROUP BY yr, ch ORDER BY yr, ch""")
tot_y = {}
rep_y = {}
for y_, ch_, n_, r_ in rows:
    tot_y[y_] = tot_y.get(y_, 0) + n_
    rep_y[y_] = rep_y.get(y_, 0) + r_
w("| Channel | 2024 customers | 2024 share | 2024 repeat rate | 2025 customers | 2025 share | 2025 repeat rate |")
w("|---|---:|---:|---:|---:|---:|---:|")
by = {(y_, ch_): (n_, r_) for y_, ch_, n_, r_ in rows}
for ch_ in CHANNELS:
    a_, b_ = by[("2024", ch_)], by[("2025", ch_)]
    w("| %s | %s | %.0f%% | %.1f%% | %s | %.0f%% | %.1f%% |" % (ch_, a_[0], 100 * a_[0] / tot_y["2024"], 100 * a_[1] / a_[0], b_[0], 100 * b_[0] / tot_y["2025"], 100 * b_[1] / b_[0]))
w("| **All consumers** | %s | 100%% | **%.1f%%** | %s | 100%% | **%.1f%%** |" % (tot_y["2024"], 100 * rep_y["2024"] / tot_y["2024"], tot_y["2025"], 100 * rep_y["2025"] / tot_y["2025"]))
w("\nEvery channel's repeat rate went up while the overall rate went down. The overall rate fell because paid social, the channel with the lowest repeat rate, grew from about a fifth of new customers to about half. That is Simpson's paradox at work, a mix shift. Wholesale customers (sales_rep channel) are excluded here and analyzed separately because there are too few of them for stable rates.")
paid_sp = {y_: sum(r["paid_social_spend"] for r in marketing if r["month"].startswith(str(y_))) for y_ in (2023, 2024, 2025)}
newpaid = {y_: q("SELECT COUNT(*) FROM customers WHERE acquisition_channel='paid_social' AND substr(acquired_date,1,4)='%d'" % y_)[0][0] for y_ in (2023, 2024, 2025)}
w("- Paid social spend: 2023 $%s, 2024 $%s, 2025 $%s. Customers acquired through paid social: %s, %s, %s. Spend per paid-social customer: $%.0f, $%.0f, $%.0f." % (
    format(paid_sp[2023], ","), format(paid_sp[2024], ","), format(paid_sp[2025], ","), newpaid[2023], newpaid[2024], newpaid[2025],
    paid_sp[2023] / newpaid[2023], paid_sp[2024] / newpaid[2024], paid_sp[2025] / newpaid[2025]))
mo = {r["month"]: r for r in marketing}
months = [r["month"] for r in marketing]
em = np.array([mo[m]["email_sends"] for m in months], float)
rv = np.array([mrev.get(m, 0) for m in months], float)
mnum = np.array([int(m[5:]) for m in months])
yrs = np.array([int(m[:4]) for m in months])
def deseason(x):
    out = x.astype(float).copy()
    for y_ in (2023, 2024, 2025):          # remove each year's overall level (the growth trend)
        out[yrs == y_] = out[yrs == y_] / out[yrs == y_].mean()
    res = out.copy()
    for mm in range(1, 13):                # remove each calendar month's usual pattern (the season)
        res[mnum == mm] = out[mnum == mm] / out[mnum == mm].mean()
    return res
w("- Correlation, monthly email_sends against monthly net revenue: r = %.2f. After removing each year's overall level (growth) and each calendar month's usual pattern (the season) from both series, r = %.2f. Email volume and revenue both climb with the holiday season and with company growth. Email may still help, but this correlation does not show it." % (np.corrcoef(em, rv)[0, 1], np.corrcoef(deseason(em), deseason(rv))[0, 1]))

w("\n## Module 07: forecasting and the churn claim\n")
train = [(m, mrev[m]) for m in sorted(mrev) if m <= "2025-09"]
test = {m: mrev[m] for m in ("2025-10", "2025-11", "2025-12")}
ytd25 = sum(v for m, v in mrev.items() if "2025-01" <= m <= "2025-09")
ytd24 = sum(v for m, v in mrev.items() if "2024-01" <= m <= "2024-09")
growth = ytd25 / ytd24
def mape(f):
    return 100 * np.mean([abs(f[m] - test[m]) / test[m] for m in test])
f_naive = {m: mrev[m.replace("2025", "2024")] for m in test}
f_growth = {m: mrev[m.replace("2025", "2024")] * growth for m in test}
last3 = np.mean([mrev[m] for m in ("2025-07", "2025-08", "2025-09")])
f_flat = {m: last3 for m in test}
w("Train on January 2023 to September 2025 net revenue, forecast October to December 2025, and compare with what happened:\n")
w("| Method | Oct | Nov | Dec | Error (MAPE) |")
w("|---|---:|---:|---:|---:|")
w("| Actual | $%s | $%s | $%s | |" % tuple(format(round(test[m]), ",") for m in test))
for name, f in (("Flat: average of the last three months", f_flat), ("Seasonal naive: same month last year", f_naive), ("Seasonal naive times year-to-date growth (x%.2f)" % growth, f_growth)):
    w("| %s | $%s | $%s | $%s | %.1f%% |" % ((name,) + tuple(format(round(f[m]), ",") for m in test) + (mape(f),)))
w("\nEach simple method fails in its own way. The flat forecast ignores the holiday peak. Same-month-last-year captures the season but ignores that the company grew by more than half. Combining season and growth roughly halves the error compared with the flat forecast, and even that method misses by double digits, which is why a forecast should carry a range and not a single number.")
w("\nVendor claim: \"Our churn model is 95 percent accurate.\" The pilot file scores 2,000 customers. %d actually churned (%.1f%%)." % (sum(c["actual_churn"] for c in churn), 100 * sum(c["actual_churn"] for c in churn) / 2000))
w("- Confusion matrix: true positives %d, false positives %d, false negatives %d, true negatives %d." % (tp, fp, fn, tn))
w("- Accuracy: %.1f%%. A model that predicts \"no one leaves\" scores %.1f%%, so the vendor's 95%% adds almost nothing over doing nothing." % (100 * (tp + tn) / 2000, 100 * (2000 - 100) / 2000))
w("- Recall (share of leavers caught): %.0f%%. Precision (share of flagged customers who really leave): %.0f%%. The model misses %d of 100 leavers." % (100 * tp / (tp + fn), 100 * tp / (tp + fp), fn))

# ---------------- Module 06 additions
w("\n### Module 06 numbers (Activities 1 and 2)\n")
rc = q("SELECT cohort_year, COUNT(*), AVG(repeat_90) FROM repeat_cohort GROUP BY 1")
ci = {}
for y_, n_, p_ in rc:
    ci[y_] = (n_, p_, 1.96 * np.sqrt(p_ * (1 - p_) / n_))
w("| Year | Customers | Repeat rate | 95% margin of error | Range |")
w("|---|---:|---:|---:|---|")
for y_ in (2024, 2025):
    n_, p_, m_ = ci[y_]
    w("| %d | %s | %.1f%% | plus or minus %.1f points | %.1f%% to %.1f%% |" % (y_, format(n_, ","), 100 * p_, 100 * m_, 100 * (p_ - m_), 100 * (p_ + m_)))
se_d = float(np.sqrt(sum(p_ * (1 - p_) / n_ for n_, p_, _ in ci.values())))
w("\nThe difference is %.1f points, and the margin of error on the difference itself is plus or minus %.1f points (1.96 times a standard error of %.2f). The two yearly ranges overlap a little, but the difference is still larger than its own margin, so a drop this size is unlikely to be noise alone. Overlapping ranges are a rough screen, and the difference's own margin is the better test." % (100 * (ci[2024][1] - ci[2025][1]), 196 * se_d, 100 * se_d))
chs = q("SELECT cohort_year, acquisition_channel, COUNT(*), AVG(repeat_90) FROM repeat_cohort GROUP BY 1, 2")
tot_ = {y_: sum(r_[2] for r_ in chs if r_[0] == y_) for y_ in (2024, 2025)}
sh_ = {(r_[0], r_[1]): r_[2] / tot_[r_[0]] for r_ in chs}
rt_ = {(r_[0], r_[1]): r_[3] for r_ in chs}
cl_ = sorted({r_[1] for r_ in chs})
mix_eff = sum((sh_[(2025, c_)] - sh_[(2024, c_)]) * rt_[(2024, c_)] for c_ in cl_)
rate_eff = sum(sh_[(2025, c_)] * (rt_[(2025, c_)] - rt_[(2024, c_)]) for c_ in cl_)
same_mix = sum(sh_[(2024, c_)] * rt_[(2025, c_)] for c_ in cl_)
w("\nDecomposition of the overall change (2024 to 2025): mix effect (the shift toward paid social) %+.1f points, rate effect (each channel's own change) %+.1f points, total %+.1f points. If 2025 had kept 2024's channel mix, the overall repeat rate would have been %.1f%%, higher than 2024's %.1f%%." % (100 * mix_eff, 100 * rate_eff, 100 * (mix_eff + rate_eff), 100 * same_mix, 100 * ci[2024][1]))
w("\nHow to compute it: for each channel, multiply the change in its share of new customers by its 2024 repeat rate (mix effect), and its 2025 share by the change in its repeat rate (rate effect). The two effects add up to the total change.")
w("\n| Channel (2024 cohort, 365-day window) | Customers | Repeat rate | 90-day gross profit | 365-day gross profit |")
w("|---|---:|---:|---:|---:|")
for ch_, n_, rr_, g90, g365 in q("SELECT acquisition_channel, COUNT(*), AVG(repeat_90), AVG(gross_profit_90d), AVG(gross_profit_365d) FROM repeat_cohort WHERE cohort_year=2024 GROUP BY 1 ORDER BY 1"):
    w("| %s | %s | %.1f%% | $%.2f | $%.2f |" % (ch_, n_, 100 * rr_, g90, g365))
w("\nGross profit is merchandise revenue minus product cost, after removing returned lines. It excludes shipping, payment fees, and marketing spend.")
w("\n**Email and revenue (Activity 3).** Monthly email_sends against monthly net revenue: r = %.2f. After removing each year's overall level and each calendar month's usual pattern from both series, r = %.2f. Email volume grew modestly from year to year while revenue roughly doubled and then grew by half, so both series trend upward together as well as rising with the holiday season." % (np.corrcoef(em, rv)[0, 1], np.corrcoef(deseason(em), deseason(rv))[0, 1]))
_yo_e, _yo_r = [], []
for m_ in months:
    if m_ >= "2024-01":
        p_ = "%d%s" % (int(m_[:4]) - 1, m_[4:])
        _yo_e.append(mo[m_]["email_sends"] / mo[p_]["email_sends"] - 1)
        _yo_r.append(mrev[m_] / mrev[p_] - 1)
w("**Spreadsheet-friendly version (Activity 3):** compare each month of 2024 and 2025 with the same month a year earlier, for both series (24 pairs). The correlation between the two year-over-year growth rates is r = %.2f. Within any single year, email and revenue correlate at 0.92 to 0.97 because both follow the season, which is why the raw correlation misleads. Email sends grew about %.0f percent a year on average, while revenue grew %.0f percent." % (np.corrcoef(_yo_e, _yo_r)[0, 1], 100 * np.mean(_yo_e), 100 * np.mean(_yo_r)))

# ---------------- Module 07 additions
w("\n### Module 07 numbers (Activity 1)\n")
q4g = sum(mrev["2025-%02d" % m_] for m_ in (10, 11, 12)) / sum(mrev["2024-%02d" % m_] for m_ in (10, 11, 12))
q1_25 = sum(mrev["2025-%02d" % m_] for m_ in (1, 2, 3))
yoy = []
for y_, (a_, b_) in zip(("Q1 2025", "Q2 2025", "Q3 2025", "Q4 2025"), ((1, 3), (4, 6), (7, 9), (10, 12))):
    cur = sum(mrev["2025-%02d" % m_] for m_ in range(a_, b_ + 1))
    prev = sum(mrev["2024-%02d" % m_] for m_ in range(a_, b_ + 1))
    yoy.append("%s %.2f" % (y_, cur / prev))
w("- Year-over-year growth factor by quarter: " + ", ".join(yoy) + ". It isn't constant, so any single growth factor is a judgment.")
w("- Forecast for January to March 2026 using the same method that worked best in the backtest (same quarter last year times the latest year-over-year growth, x%.3f): $%s. Q1 2025 was $%s." % (q4g, format(round(q1_25 * q4g), ","), format(round(q1_25), ",")))
w("- With the backtest's average error of about 13 percent as a rough range: $%s to $%s. A scenario where growth cools to x1.25 gives $%s." % (format(round(q1_25 * q4g * .867), ","), format(round(q1_25 * q4g * 1.133), ","), format(round(q1_25 * 1.25), ",")))

# ---------------- Module 08 inputs and scenarios
w("\n### Module 08 inputs and scenario results\n")
cac25 = paid_sp[2025] / newpaid[2025]
g90p = q("SELECT AVG(gross_profit_90d) FROM repeat_cohort WHERE cohort_year=2025 AND acquisition_channel='paid_social'")[0][0]
g365p = q("SELECT AVG(gross_profit_365d) FROM repeat_cohort WHERE cohort_year=2024 AND acquisition_channel='paid_social'")[0][0]
gp25 = q("""SELECT SUM(i.line_total - i.quantity*p.unit_cost) FROM order_items i JOIN products p USING(product_id) JOIN orders o USING(order_id)
 LEFT JOIN returns r ON r.order_id=i.order_id AND r.line_no=i.line_no
 WHERE o.status='shipped' AND substr(o.order_date,1,4)='2025' AND r.return_id IS NULL""")[0][0]
act25 = q("SELECT COUNT(DISTINCT customer_id) FROM orders WHERE status='shipped' AND substr(order_date,1,4)='2025'")[0][0]
gpc = gp25 / act25
fit = q("""SELECT COUNT(*), SUM(r.refund_amount), SUM(r.refund_amount - i.quantity*p.unit_cost)
 FROM returns r JOIN order_items i ON i.order_id=r.order_id AND i.line_no=r.line_no JOIN products p USING(product_id) JOIN orders o ON o.order_id=r.order_id
 WHERE substr(o.order_date,1,4)='2025' AND r.reason='Did not fit' AND p.category IN ('Clothing','Footwear')""")[0]
w("| Input | Value | Where it comes from |")
w("|---|---:|---|")
w("| Paid social cost per new customer, 2025 | $%.2f | 2025 paid_social_spend ($%s) divided by customers acquired through paid social (%s) |" % (cac25, format(paid_sp[2025], ","), format(newpaid[2025], ",")))
w("| Paid social 90-day gross profit per customer, 2025 customers | $%.2f | repeat_cohort |" % g90p)
w("| Paid social 365-day gross profit per customer, 2024 customers | $%.2f | repeat_cohort |" % g365p)
w("| Break-even incrementality for paid social | %.0f%% | cost per customer divided by 365-day gross profit: the share of paid-social customers who must be new business for the spend to pay back in a year |" % (100 * cac25 / g365p))
w("| Customers who ordered in 2025 | %s | orders |" % format(act25, ","))
w("| 2025 gross profit per active customer, after returns | $%.2f | merchandise revenue minus product cost on shipped, unreturned lines, divided by active customers |" % gpc)
w("| Break-even spend lift for a $60,000 retention program | %.1f%% | 60,000 divided by (active customers times gross profit per customer) |" % (100 * 60000 / (act25 * gpc)))
w("| Clothing and footwear returns coded \"Did not fit\", 2025 orders | %d lines | returns |" % fit[0])
w("| Refunds on those returns / gross profit forgone | $%s / $%s | the most any fit program could recover, even if it eliminated every one of them |" % (format(round(fit[1]), ","), format(round(fit[2]), ",")))
w("| Loyalty evidence (Module 05) | members -8%, non-members -15% | roughly 7 points; optimistic, because members chose to join |")
def net_a(budget, cac, gp, inc):
    return budget / cac * (inc * gp - cac)
A = {"Low": net_a(150000, cac25 * 1.3, 130, .5), "Base": net_a(150000, cac25, g365p, .75), "High": net_a(150000, cac25, 175, 1.0)}
B = {k_: act25 * gpc * u_ - 60000 for k_, u_ in (("Low", .02), ("Base", .05), ("High", .08))}
C = {k_: fit[2] * u_ - 30000 for k_, u_ in (("Low", .10), ("Base", .25), ("High", .40))}
w("\nScenario assumptions (invented for the exercise, and learners should challenge them):\n")
w("- Option A, expand paid social with $150,000: Low = cost per customer 30%% higher, 365-day gross profit $130, half the customers incremental. Base = cost per customer $%.0f, 365-day gross profit $%.0f, 75%% incremental. High = cost per customer $%.0f, gross profit $175, all incremental." % (cac25, g365p, cac25))
w("- Option B, retention program costing $60,000: spend per active customer rises 2% (Low), 5% (Base), 8% (High).")
w("- Option C, fit tools costing $30,000: fit-related returns fall 10% (Low), 25% (Base), 40% (High), recovering that share of the forgone gross profit.")
w("- Probabilities: Low 25%, Base 50%, High 25%.\n")
w("| Option | Low | Base | High | Expected value | Chance of losing money |")
w("|---|---:|---:|---:|---:|---:|")
for name, d_ in (("A: expand paid social ($150,000)", A), ("B: retention program ($60,000)", B), ("C: fit tools ($30,000)", C)):
    ev = .25 * d_["Low"] + .5 * d_["Base"] + .25 * d_["High"]
    loss = sum(p_ for k_, p_ in (("Low", .25), ("Base", .5), ("High", .25)) if d_[k_] < 0)
    usd = lambda x_: ("-$" if x_ < 0 else "$") + format(round(abs(x_)), ",")
    w("| %s | %s | %s | %s | %s | %.0f%% |" % (name, usd(d_["Low"]), usd(d_["Base"]), usd(d_["High"]), usd(ev), 100 * loss))
w("| D: hold the money in reserve | $0 | $0 | $0 | $0 | 0% |")
w("\nNet values are twelve-month gross profit minus the spend. Option A has the only positive expected value and also the widest spread, and its payoff depends on a number the company hasn't measured (how many paid-social customers are truly new). That points toward a staged decision: a smaller, controlled test first.")
with open(os.path.join(FAC, "answer_key_numbers.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(L) + "\n")
con.close()
print("wrote", os.path.join(FAC, "answer_key_numbers.md"))
