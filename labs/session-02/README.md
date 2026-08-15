# Session 2 lab — Data storage systems

One month of NYC yellow taxi trips (the first million rows), stored four ways,
plus PostgreSQL in Docker.

You will not write any SQL. Every query is already written — you run cells, read
numbers, and fill in the table at the top of the notebook.

## Setup

From the repository root:

```bash
uv sync
uv run python scripts/download_nyc_taxi.py
docker compose up -d
```

Then open **<http://localhost:8888/lab?token=labs>** and click into
`session-02/lab.ipynb`.

The notebook runs inside Docker, next to the databases — there is no kernel to
choose and no connection to configure. What you type is saved to your own
`labs/` folder.

The download is ~50 MB and writes ~750 MB to `data/nyc-taxi/`; nothing after it
needs internet. It is safe to re-run — it skips what it has already produced.
Tight on disk or RAM? Prefix it with `ROW_CAP=250000`.

### Prefer VS Code to the browser?

Open `labs/session-02/lab.ipynb`, then **Select Kernel** (top right) &rarr;
*Existing Jupyter Server…* &rarr; paste `http://localhost:8888/?token=labs`
&rarr; pick *Python 3*. The code still runs in the container; VS Code is only the
editor.

The token matters: paste the URL with `?token=labs` and use `localhost`, not the
`0.0.0.0` address Jupyter prints in the log. Without the token VS Code fails with
`'_xsrf' argument missing from POST`.

For import autocompletion as well, install the **Dev Containers** extension and
run *Dev Containers: Attach to Running Container…* &rarr; `2027-labs-jupyter-1`,
then open `/app/labs/session-02/lab.ipynb` there.

When you are done: `docker compose down`.

## The parts

| Part | What | Where |
|---|---|---|
| A | Four files, three questions: bytes each one forces you to read, and how long | `lab.ipynb` |
| B | The same two questions in PostgreSQL, without and with an index | `lab.ipynb` |
| C | *Optional.* Two people write to one row and €40 disappears | [`PART_C.md`](PART_C.md) |

Part C is extra: two terminals side by side, for anyone who finishes early or is
curious afterwards. Nothing later in the course depends on it.

## Roughly what to expect

Bytes each file must read, with 1,000,000 rows. These are properties of the
files, so they should match yours almost exactly; the times will not.

| Format | Size | Q1 whole table | Q2 avg fare by hour | Q3 one trip |
|---------|--------|--------|--------|--------|
| CSV | 112 MB | 112 MB | 112 MB | 112 MB |
| JSON | 445 MB | 445 MB | 445 MB | 445 MB |
| Parquet | 35 MB | 34.5 MB | 9.8 MB | 9.7 MB |
| SQLite | 122 MB | 122 MB | 122 MB | 122 MB |

In part B the single-trip lookup goes from ~12 ms to ~0.01 ms once the index
exists. The aggregate does not move.