# Session 7 lab — Object-relational mappers

The same database as sessions 3 to 5, read through Python classes. You map the
`trips` table, run three queries you have already written in SQL, make the ORM
send a hundred and one statements where two would do, and, optionally, change the
schema with a migration.

## Setup

From the repository root:

```bash
uv sync
docker compose up -d --build
```

This session uses two new packages, SQLAlchemy and Alembic. They are already in
`pyproject.toml`, put there with

```bash
uv add sqlalchemy alembic "psycopg[binary]"
```

so you do not run that line yourself. `uv sync` installs them on your laptop, and
`--build` adds them to the notebook image, which takes a minute the first time.
There is no new container and no new data.

Then open **<http://localhost:8888/lab?token=labs>** and click into
`session-07/notebook.ipynb`. Its first cell checks that last week's tables are
still in the database, and loads them if not.

## The files

| File | What |
|---|---|
| `notebook.ipynb` | Parts A, B and C |
| `models.py` | The tables as classes. You complete `Trip` in part A |
| `query_counter.py` | Counts the statements an engine sends, for part B |
| `alembic.ini`, `alembic/` | Migrations, for part C. Already set up, with two revisions |

## The parts

| Part | What |
|---|---|
| A | Complete the `Trip` class, run three queries, compare the SQL they send |
| B | Count the statements a loop sends, then make it two |
| C | *Optional.* Add a column with a migration, then take it back |

## Running alembic

Part C runs `alembic` from notebook cells. It has to run in the notebook
container: the database's host name, `postgres`, does not exist on your laptop.
To use a terminal instead, open one in JupyterLab (*File &rarr; New &rarr;
Terminal*), then

```bash
cd /app/labs/session-07
alembic history
```

## If you break the database

Run `reset_database()` in a notebook cell. It rebuilds and reloads everything in
about 20 seconds, and records the database as being at the second revision again.

If `models.py` has a column the database does not, every query on that class
fails. Either apply the revision that adds it (`alembic upgrade head`) or remove it
from the class.
