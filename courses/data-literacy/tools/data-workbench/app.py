"""
Data Workbench: a small local web page for browsing and editing a SQLite file.
Create, Read, Update and Delete (CRUD) on any table, working on a COPY of the database.

Run:   python app.py                      (uses ../../case-data/lantern_clean.sqlite)
       python app.py path/to/other.sqlite
Open:  http://127.0.0.1:5000

Design notes
- It edits working_copy.sqlite, never the original. "Reset" copies the original back.
- It listens on 127.0.0.1 only, so nothing outside your computer can reach it.
- Table and column names come from the database itself and are checked before use.
  Values always travel as parameters, never pasted into SQL.
- Foreign keys are switched on, so the database refuses changes that would orphan rows.
- Every change is written to a change log table (workbench_log) inside the working copy.
"""
import datetime as dt
import os
import secrets
import shutil
import sqlite3
import sys

from flask import Flask, abort, flash, redirect, render_template, request, session, url_for

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DB = os.path.join(HERE, "..", "..", "case-data", "lantern_clean.sqlite")
SOURCE_DB = os.path.abspath(
    os.environ.get("WORKBENCH_DB") or (sys.argv[1] if len(sys.argv) > 1 and __name__ == "__main__" else DEFAULT_DB)
)
WORKING_DB = os.environ.get("WORKBENCH_WORKING_DB") or os.path.join(HERE, "working_copy.sqlite")
PAGE_SIZE = 25

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)  # new every run, which is fine for a local tool


# ----------------------------------------------------------------- database
def ensure_working_copy(force=False):
    if force or not os.path.exists(WORKING_DB):
        if not os.path.exists(SOURCE_DB):
            raise FileNotFoundError("Database not found: " + SOURCE_DB)
        shutil.copyfile(SOURCE_DB, WORKING_DB)


def get_db():
    ensure_working_copy()
    conn = sqlite3.connect(WORKING_DB)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("""CREATE TABLE IF NOT EXISTS workbench_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT, at TEXT NOT NULL, table_name TEXT NOT NULL,
        action TEXT NOT NULL, row_id INTEGER, detail TEXT)""")
    return conn


def quote(name):
    return '"' + name.replace('"', '""') + '"'


def table_names(conn):
    rows = conn.execute("""SELECT name FROM sqlite_master WHERE type = 'table'
                           AND name NOT LIKE 'sqlite_%' AND name NOT LIKE 'workbench_%' ORDER BY name""")
    return [r["name"] for r in rows]


def columns_of(conn, table):
    allowed = table_names(conn)
    safe_table = next((t for t in allowed if t == table), None)
    if safe_table is None:
        abort(404)
    return conn.execute("PRAGMA table_info(%s)" % quote(safe_table)).fetchall()


def log_change(conn, table, action, row_id, detail):
    conn.execute("INSERT INTO workbench_log (at, table_name, action, row_id, detail) VALUES (?, ?, ?, ?, ?)",
                 (dt.datetime.now().isoformat(timespec="seconds"), table, action, row_id, detail))


# --------------------------------------------------------------- protection
@app.context_processor
def inject_globals():
    session.setdefault("csrf", secrets.token_hex(16))
    return {"csrf_token": session["csrf"],
            "local_bootstrap": os.path.exists(os.path.join(HERE, "static", "bootstrap.min.css")),
            "source_db": os.path.basename(SOURCE_DB)}


@app.before_request
def check_csrf():
    if request.method == "POST":
        if not session.get("csrf") or request.form.get("csrf") != session["csrf"]:
            abort(400, "The page expired. Go back, reload it, and try again.")


# ------------------------------------------------------------------- pages
@app.route("/")
def index():
    conn = get_db()
    tables = [(t, conn.execute("SELECT COUNT(*) FROM %s" % quote(t)).fetchone()[0]) for t in table_names(conn)]
    conn.close()
    return render_template("index.html", tables=tables)


@app.route("/table/<table>")
def show_table(table):
    conn = get_db()
    allowed_tables = table_names(conn)
    if table not in allowed_tables:
        abort(404)
    cols = columns_of(conn, table)
    names = [c["name"] for c in cols]
    sort = request.args.get("sort", "")
    direction = "DESC" if request.args.get("dir") == "desc" else "ASC"
    search = request.args.get("q", "").strip()
    page = max(1, request.args.get("page", 1, type=int))

    where, params = "", []
    if search:
        where = " WHERE " + " OR ".join("CAST(%s AS TEXT) LIKE ?" % quote(n) for n in names)
        params = ["%" + search + "%"] * len(names)
    order = " ORDER BY %s %s" % (quote(sort), direction) if sort in names else ""
    total = conn.execute("SELECT COUNT(*) FROM %s%s" % (quote(table), where), params).fetchone()[0]
    pages = max(1, -(-total // PAGE_SIZE))
    page = min(page, pages)
    rows = conn.execute("SELECT rowid AS __rowid__, * FROM %s%s%s LIMIT ? OFFSET ?" % (quote(table), where, order),
                        params + [PAGE_SIZE, (page - 1) * PAGE_SIZE]).fetchall()
    conn.close()
    return render_template("table.html", table=table, names=names, rows=rows, total=total, page=page, pages=pages,
                           sort=sort, direction=direction.lower(), search=search)


def read_form(cols, adding):
    """Turn form text into typed values. Returns (values dict, list of error messages)."""
    values, errors = {}, []
    for c in cols:
        name, ctype = c["name"], (c["type"] or "").upper()
        is_auto_key = c["pk"] == 1 and ctype == "INTEGER"
        if not adding and c["pk"]:
            continue  # keys are read-only when editing, so references never break
        raw = request.form.get(name, "").strip()
        if raw == "":
            if adding and is_auto_key:
                continue  # let the database number it
            if c["notnull"] and c["dflt_value"] is None:
                errors.append("%s is required." % name)
            values[name] = None
            continue
        try:
            if "INT" in ctype:
                values[name] = int(raw)
            elif ctype in ("REAL", "FLOAT", "DOUBLE", "NUMERIC"):
                values[name] = float(raw)
            else:
                values[name] = raw
        except ValueError:
            errors.append("%s must be a number." % name)
    return values, errors


@app.route("/table/<table>/add", methods=("GET", "POST"))
def add_row(table):
    conn = get_db()
    cols = columns_of(conn, table)
    allowed_columns = {c["name"] for c in cols}
    if request.method == "POST":
        values, errors = read_form(cols, adding=True)
        if not errors:
            try:
                names = list(values)
                if any(n not in allowed_columns for n in names):
                    abort(400)
                cur = conn.execute("INSERT INTO %s (%s) VALUES (%s)" % (
                    quote(table), ", ".join(quote(n) for n in names), ", ".join("?" * len(names))),
                    [values[n] for n in names])
                log_change(conn, table, "create", cur.lastrowid, ", ".join("%s=%s" % (n, values[n]) for n in names))
                conn.commit()
                conn.close()
                flash("Row added.", "success")
                return redirect(url_for("show_table", table=table))
            except sqlite3.DatabaseError as e:
                errors.append("The database refused the new row: %s" % e)
        for e in errors:
            flash(e, "danger")
        form = request.form
    else:
        form = {}
    conn.close()
    return render_template("form.html", table=table, cols=cols, form=form, row=None, adding=True)
    table = next((t for t in table_names(conn) if t == table), None)
    if table is None:
        conn.close()
        abort(404)


@app.route("/table/<table>/edit/<int:rowid>", methods=("GET", "POST"))
def edit_row(table, rowid):
    conn = get_db()
    allowed = table_names(conn)
    safe_table = next((t for t in allowed if t == table), None)
    if safe_table is None:
        conn.close()
        abort(404)
    cols = columns_of(conn, safe_table)
    row = conn.execute("SELECT rowid AS __rowid__, * FROM %s WHERE rowid = ?" % quote(safe_table), (rowid,)).fetchone()
    if row is None:
        conn.close()
        abort(404)
    if request.method == "POST":
        values, errors = read_form(cols, adding=False)
        if not errors and values:
            try:
                changes = ["%s: %s to %s" % (n, row[n], values[n]) for n in values if row[n] != values[n]]
                conn.execute("UPDATE %s SET %s WHERE rowid = ?" % (
                    quote(safe_table), ", ".join("%s = ?" % quote(n) for n in values)), list(values.values()) + [rowid])
                log_change(conn, safe_table, "update", rowid, "; ".join(changes) or "no change")
                conn.commit()
                conn.close()
                flash("Row updated.", "success")
                return redirect(url_for("show_table", table=safe_table))
            except sqlite3.DatabaseError as e:
                errors.append("The database refused the change: %s" % e)
        for e in errors:
            flash(e, "danger")
    conn.close()
    return render_template("form.html", table=safe_table, cols=cols, form=request.form if request.method == "POST" else {},
                           row=row, adding=False)


@app.route("/table/<table>/delete/<int:rowid>", methods=("POST",))
def delete_row(table, rowid):
    conn = get_db()
    allowed = table_names(conn)
    safe_table = next((t for t in allowed if t == table), None)
    if safe_table is None:
        conn.close()
        abort(404)
    row = conn.execute("SELECT * FROM %s WHERE rowid = ?" % quote(safe_table), (rowid,)).fetchone()
    if row is None:
        conn.close()
        abort(404)
    try:
        conn.execute("DELETE FROM %s WHERE rowid = ?" % quote(safe_table), (rowid,))
        log_change(conn, safe_table, "delete", rowid, ", ".join("%s=%s" % (k, row[k]) for k in row.keys()))
        conn.commit()
        flash("Row deleted.", "success")
    except sqlite3.IntegrityError as e:
        conn.rollback()
        flash("The database refused the delete (%s). Other rows still point to this one." % e, "danger")
    conn.close()
    return redirect(url_for("show_table", table=safe_table))


@app.route("/log")
def change_log():
    conn = get_db()
    rows = conn.execute("SELECT * FROM workbench_log ORDER BY id DESC LIMIT 200").fetchall()
    conn.close()
    return render_template("log.html", rows=rows)


@app.route("/reset", methods=("POST",))
def reset():
    ensure_working_copy(force=True)
    flash("Working copy reset to the original database.", "success")
    return redirect(url_for("index"))


if __name__ == "__main__":
    ensure_working_copy()
    print("Source database :", SOURCE_DB)
    print("Working copy    :", WORKING_DB)
    print("Open http://127.0.0.1:5000 in your browser. Press Ctrl+C to stop.")
    app.run(host="127.0.0.1", port=5000, debug=False)
