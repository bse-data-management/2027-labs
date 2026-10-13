# Session 5 lab — Data warehouses and dimensional modelling

## Setup

From the repository root:

```bash
uv sync
uv run python labs/session-05/prepare_parquet.py
docker compose up -d
```

The second line writes the trips to Parquet, in a few seconds, into
`data/nyc-taxi-parquet/`. It is safe to re-run.

Then open **<http://localhost:8888/lab?token=labs>** and click into
`session-05/lab.ipynb`. If last week's tables are gone, its first cell reloads
PostgreSQL.

You need the data from session 4. If you skipped it, run
`uv run python scripts/prepare_nyc_taxi_normalized.py` first.

## DuckDB

DuckDB is already installed: `uv sync` puts it in the environment, as it is a
dependency of this repository. There is no new container. DuckDB runs inside the
notebook's own Python process and reads the Parquet files directly.

## If you break the star schema

Fix `sql/star_schema.sql` and run the `build_star()` cell again. It drops and
rebuilds the three tables each time.
