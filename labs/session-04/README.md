# Session 4 lab — Relational data management and SQL II

## Setup

From the repository root:

```bash
uv sync
uv run python scripts/prepare_nyc_taxi_normalized.py
docker compose up -d
```

Run the preparation step even if you ran it for session 3: this session needs one
more file. It downloads nothing and takes about a minute.

Then open **<http://localhost:8888/lab?token=labs>** and click into
`session-04/lab.ipynb`.

## If you break the database

Run the `reset_database()` cell again. It rebuilds and reloads everything in
about 20 seconds, including dropping any index you created.
