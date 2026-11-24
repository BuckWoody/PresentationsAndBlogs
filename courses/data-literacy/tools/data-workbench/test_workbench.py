"""
Quick end-to-end check of the Data Workbench (run: python test_workbench.py).
Uses a temporary working copy, so nothing in your real files changes.
"""
import importlib
import os
import re
import sqlite3
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
tmp = tempfile.mkdtemp()
os.environ["WORKBENCH_DB"] = os.path.join(HERE, "..", "..", "case-data", "lantern_clean.sqlite")
os.environ["WORKBENCH_WORKING_DB"] = os.path.join(tmp, "working_copy.sqlite")
app_module = importlib.import_module("app")
app = app_module.app
app.config["TESTING"] = True


def token(client, url="/"):
    html = client.get(url).get_data(as_text=True)
    return re.search(r'name="csrf" value="([0-9a-f]+)"', html).group(1)


def count(sql, params=()):
    con = sqlite3.connect(os.environ["WORKBENCH_WORKING_DB"])
    n = con.execute(sql, params).fetchone()[0]
    con.close()
    return n


ok = 0
def check(label, condition):
    global ok
    assert condition, "FAILED: " + label
    ok += 1
    print("pass:", label)


with app.test_client() as c:
    # Read
    r = c.get("/")
    check("home page lists tables", r.status_code == 200 and "customers" in r.get_data(as_text=True))
    check("workbench_log is hidden from the table list", "workbench_log" not in r.get_data(as_text=True))
    r = c.get("/table/customers")
    check("table page shows 25 rows per page", r.get_data(as_text=True).count(">Edit<") == 25)
    r = c.get("/table/customers?q=Northeast&sort=customer_id&dir=desc")
    check("search and sort work", r.status_code == 200 and "Northeast" in r.get_data(as_text=True))
    check("unknown table gives 404", c.get("/table/nope").status_code == 404)
    r = c.get("/table/customers?sort=customer_id;DROP TABLE customers")
    check("a hostile sort value is ignored", r.status_code == 200 and count("SELECT COUNT(*) FROM customers") == 6900)
    r = c.get("/table/customers?q=' OR 1=1 --")
    check("a hostile search value is just text", r.status_code == 200 and count("SELECT COUNT(*) FROM customers") == 6900)

    # CSRF
    r = c.post("/table/customers/delete/1001")
    check("a POST without the token is refused", r.status_code == 400)

    # Create
    t = token(c, "/table/customers/add")
    r = c.post("/table/customers/add", data={"csrf": t, "customer_id": "", "acquired_date": "2025-12-31",
               "acquisition_channel": "organic_search", "customer_type": "consumer", "region": "West",
               "age_band": "", "email_opt_in": "1"})
    check("add a customer redirects", r.status_code == 302)
    check("the new customer exists with the next id", count("SELECT COUNT(*) FROM customers WHERE customer_id = 7901") == 1)
    check("blank age_band is stored as NULL", count("SELECT COUNT(*) FROM customers WHERE customer_id = 7901 AND age_band IS NULL") == 1)
    r = c.post("/table/customers/add", data={"csrf": t, "acquired_date": "2025-12-31", "email_opt_in": "yes"})
    check("bad input is reported, not stored", b"must be a number" in r.data and count("SELECT COUNT(*) FROM customers") == 6901)
    r = c.post("/table/customers/add", data={"csrf": t})
    check("missing required fields are reported", b"is required" in r.data)

    # Update
    rowid = count("SELECT rowid FROM customers WHERE customer_id = 7901")
    r = c.post("/table/customers/edit/%d" % rowid, data={"csrf": t, "acquired_date": "2025-12-30", "acquisition_channel": "paid_social",
               "customer_type": "consumer", "region": "Midwest", "age_band": "25-34", "email_opt_in": "0"})
    check("edit redirects", r.status_code == 302)
    check("the edit was saved", count("SELECT COUNT(*) FROM customers WHERE customer_id = 7901 AND region = 'Midwest' AND email_opt_in = 0") == 1)
    check("the key cannot be changed through the form", count("SELECT COUNT(*) FROM customers WHERE customer_id = 7901") == 1)

    # Delete, refused by the database
    r = c.post("/table/customers/delete/1001", data={"csrf": t}, follow_redirects=True)
    check("deleting a customer who has orders is refused", b"refused the delete" in r.data and count("SELECT COUNT(*) FROM customers WHERE customer_id = 1001") == 1)
    check("a refused delete is not logged as a delete", count("SELECT COUNT(*) FROM workbench_log WHERE action = 'delete'") == 0)

    # Delete, allowed
    r = c.post("/table/customers/delete/%d" % rowid, data={"csrf": t})
    check("deleting a customer with no orders works", r.status_code == 302 and count("SELECT COUNT(*) FROM customers WHERE customer_id = 7901") == 0)

    # Log
    r = c.get("/log")
    check("the change log records create, update and delete",
          all(w.encode() in r.data for w in ("create", "update", "delete")))
    check("the log keeps the old and new value of an edit", b"Midwest" in r.data and b"West to Midwest" in r.data)

    # Reset
    c.post("/table/customers/delete/%d" % count("SELECT rowid FROM customers ORDER BY customer_id DESC LIMIT 1"), data={"csrf": t})
    r = c.post("/reset", data={"csrf": t})
    c.get("/log")  # the log table is recreated on the next page load
    check("reset restores the original", r.status_code == 302 and count("SELECT COUNT(*) FROM customers") == 6900
          and count("SELECT COUNT(*) FROM workbench_log") == 0)

# the original database was never touched
src = sqlite3.connect(os.environ["WORKBENCH_DB"])
check("the original database is unchanged", src.execute("SELECT COUNT(*) FROM customers").fetchone()[0] == 6900
      and src.execute("SELECT COUNT(*) FROM sqlite_master WHERE name = 'workbench_log'").fetchone()[0] == 0)
src.close()
print("\nAll %d checks passed." % ok)
