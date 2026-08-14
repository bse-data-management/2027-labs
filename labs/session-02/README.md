# Session 2 lab — Data storage systems

One month of NYC yellow taxi trips (the first million rows), stored four ways,
plus PostgreSQL and Redis in Docker.

You will not write any SQL. Every query is already written — you run cells, read
numbers, and fill in the table at the top of the notebook.

## Setup

From the repository root:

```bash
uv sync
uv run python scripts/download_nyc_taxi.py
docker compose up -d
```

Then open **<http://localhost:8888>** and click into `session-02/lab.ipynb`.

The notebook runs inside Docker, next to the databases — there is no kernel to
choose and no connection to configure. What you type is saved to your own
`labs/` folder.

The download is ~50 MB and writes ~750 MB to `data/nyc-taxi/`; nothing after it
needs internet. It is safe to re-run — it skips what it has already produced.
Tight on disk or RAM? Prefix it with `ROW_CAP=250000`.

### Prefer VS Code to the browser?

Open `labs/session-02/lab.ipynb`, then **Select Kernel** (top right) &rarr;
*Existing Jupyter Server…* &rarr; enter `http://localhost:8888` &rarr; pick
*Python 3*. Leave the password prompt empty. The code still runs in the
container; VS Code is only the editor.

For import autocompletion as well, install the **Dev Containers** extension and
run *Dev Containers: Attach to Running Container…* &rarr; `2027-labs-jupyter-1`,
then open `/app/labs/session-02/lab.ipynb` there.

When you are done: `docker compose down`.

## The three parts

| Part | What | Where |
|---|---|---|
| A | Four files, three questions: bytes each one forces you to read, and how long | `lab.ipynb` |
| B | The same two questions in PostgreSQL, without and with an index | `lab.ipynb` |
| C | Two people write to one row and €40 disappears | [`PART_C.md`](PART_C.md) |

Part C needs two terminals side by side. There is an optional Redis stretch at
the end of the notebook.

## Roughly what to expect

Bytes each file must read, with 1,000,000 rows. These are properties of the
files, so they should match yours almost exactly; the times will not.

| Format | Size | Q1 whole table | Q2 avg fare by hour | Q3 one trip |
|---------|--------|--------|--------|--------|
| CSV | 112 MB | 112 MB | 112 MB | 112 MB |
| JSON | 445 MB | 445 MB | 445 MB | 445 MB |
| Parquet | 27 MB | 27 MB | 6.6 MB | 2.7 MB |
| SQLite | 122 MB | 122 MB | 122 MB | 122 MB |

In part B the single-trip lookup goes from ~12 ms to ~0.01 ms once the index
exists. The aggregate does not move.

## Troubleshooting

**<http://localhost:8888> does not open** — something else on your machine is
already using that port (another Jupyter, most likely). Publish this one
elsewhere, from the repository root:

```bash
echo "JUPYTER_PORT=8889" > .env
docker compose up -d
```

Then use <http://localhost:8889>.

**`Cannot connect to the Docker daemon`** — Docker Desktop is not running.

**The download stopped halfway** — re-run it. A partial download is left as a
`.part` file and never mistaken for a finished one. To start over completely,
delete `data/nyc-taxi/` and run it again.

**`No data found. Run scripts/download_nyc_taxi.py first`** — check that
`data/nyc-taxi/trips.parquet` exists. The notebook reads it through the
`./data` folder mounted into the container.

**Part C: my second terminal did not wait** — both terminals must be in the same
database, and terminal A must still be inside its transaction. Reset the balance
to 120 and start round 2 again.
