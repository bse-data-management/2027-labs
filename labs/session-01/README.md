# Session 1 lab — Tools of the trade

Two commands, from the repository root:

```bash
docker build -t labs .
docker run labs uv run python labs/session-01/trips.py
```

You should see the two monthly means printed:

```
Mean fare per month (missing fares dropped)
-------------------------------------------
  January    25.00
  February   30.00
```

If you see those two numbers, your toolchain works.

## The code

`trips.py` is the end state of the refactor from the slides. Some fares in
`data/test/trips_*.csv` are missing: `dropna()` gives January 25.00, where
`fillna(0)` would give 20.00 by counting missing fares as free rides. Nothing in
the code tells you which is right — that is a question about the data.

Without the container:

```bash
uv run python labs/session-01/trips.py
uv run pytest labs/session-01
```
