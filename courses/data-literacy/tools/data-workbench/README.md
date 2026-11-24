<img width="150" style="float: right; margin: 0px 15px 15px 0px;" src="../../graphics/logo.png">

# Workshop: Data Literacy

#### <i>Data Workbench: Create, Read, Update and Delete in Your Browser</i>

<p style="border-bottom: 1px solid lightgrey;"></p>

The Data Workbench is a small web page that runs on your own computer and lets you browse and edit any SQLite file. Module 03 uses it as an optional activity, so you can see what a database does when you change data (and what it refuses to do).

It is built with Flask (a small Python web framework), SQLite, and Bootstrap for the look and feel.

<img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/pencil2.png?raw=true"> <h2>Run It</h2>

You need Python 3.9 or later. From this folder:

```
python3 -m venv venv
source venv/bin/activate        (on Windows: venv\Scripts\activate)
pip install -r requirements.txt
python app.py
```

Then open `http://127.0.0.1:5000` in your browser. Press Ctrl+C in the terminal to stop it.

By default it opens the Lantern Peak database (`../../case-data/lantern_clean.sqlite`). To open a different SQLite file, add its path: `python app.py path/to/your.sqlite`.

<img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/pencil2.png?raw=true"> <h2>What It Does</h2>

- **Read:** lists every table, with search across all columns, sorting, and paging.
- **Create:** adds a row. Leave a key blank and the database numbers it for you.
- **Update:** edits a row. Key columns are read-only so references can't break.
- **Delete:** removes a row, after a confirmation prompt.
- **Change log:** every create, update, and delete is recorded, including the old and new values of an edit.
- **Reset copy:** throws away your changes and starts again from the original.

<img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/pencil2.png?raw=true"> <h2>Built-In Safety</h2>

- It edits a **copy** (`working_copy.sqlite`), never your original file.
- It listens on `127.0.0.1` only, so nothing outside your computer can reach it.
- Table and column names come from the database itself and are checked before use, and every value travels as a parameter. (The included `test_workbench.py` tries hostile input to confirm this.)
- Foreign keys are switched on. Try deleting a customer who has orders and the database says no.
- Forms carry a one-time token, and debug mode is off.

This is a learning tool. Don't point it at a production database, and don't expose it on a network.

<img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/pencil2.png?raw=true"> <h2>Working Offline</h2>

By default the page loads Bootstrap's stylesheet from a public content delivery network. The tool works without it (the page just looks plain). To keep everything local, download `bootstrap.min.css` from the Bootstrap project and save it in the `static` folder. The page uses the local copy automatically.

<img style="float: left; margin: 0px 15px 15px 0px;" src="https://github.com/microsoft/sqlworkshops/blob/master/graphics/pencil2.png?raw=true"> <h2>Check That It Works</h2>

```
python test_workbench.py
```

It runs 23 checks against a temporary copy (create, read, update, delete, refused deletes, hostile input, expired forms, and reset) and prints "All 23 checks passed" when everything is fine.
