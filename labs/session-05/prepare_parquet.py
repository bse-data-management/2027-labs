"""Write the trips table out as Parquet, once whole and once partitioned by day.

    uv run python labs/session-05/prepare_parquet.py

Reads the same trips.csv that sessions 3 and 4 load into PostgreSQL, so both
engines in part A answer from the same 1,000,000 rows. Writes to
data/nyc-taxi-parquet/ and skips the work if the files are already there. Delete
the folder to start again.

The data holds one month, so part C partitions by day: a partition per
month would be one partition, and there would be nothing to skip.
"""

from pathlib import Path

import duckdb

DATA = Path(__file__).resolve().parents[2] / "data"
SOURCE = DATA / "nyc-taxi-normalized" / "trips.csv"
OUT = DATA / "nyc-taxi-parquet"
WHOLE = OUT / "trips.parquet"
BY_DAY = OUT / "trips_by_day"

# The types PostgreSQL holds, so that both engines see the same values.
COLUMNS = {
    "trip_id": "BIGINT",
    "driver_id": "INTEGER",
    "rider_id": "INTEGER",
    "pickup_zone_id": "INTEGER",
    "dropoff_zone_id": "INTEGER",
    "pickup_at": "VARCHAR",
    "dropoff_at": "VARCHAR",
    "distance_km": "DECIMAL(8, 2)",
    "fare": "DECIMAL(10, 2)",
    "tip": "DECIMAL(10, 2)",
}

# The CSV states New York time with its offset. Keeping the wall-clock part gives
# the same hours PostgreSQL reports in its America/New_York session, without
# DuckDB needing time zone data.
TRIPS = f"""
    SELECT * REPLACE (
        CAST(left(pickup_at, 19) AS TIMESTAMP)  AS pickup_at,
        CAST(left(dropoff_at, 19) AS TIMESTAMP) AS dropoff_at
    )
    FROM read_csv('{SOURCE}', header = true, columns = {COLUMNS})
"""


def main() -> None:
    if WHOLE.exists() and BY_DAY.exists():
        print(f"already prepared, in {OUT}")
        return
    if not SOURCE.exists():
        raise SystemExit(
            f"not found: {SOURCE}\n"
            "run scripts/prepare_nyc_taxi_normalized.py first (see the README)"
        )

    OUT.mkdir(parents=True, exist_ok=True)
    db = duckdb.connect()
    db.execute(f"COPY ({TRIPS}) TO '{WHOLE}' (FORMAT parquet)")
    db.execute(
        f"""
        COPY (SELECT *, CAST(pickup_at AS DATE) AS pickup_date FROM ({TRIPS}))
        TO '{BY_DAY}' (FORMAT parquet, PARTITION_BY (pickup_date))
        """
    )

    files = list(BY_DAY.rglob("*.parquet"))
    print(f"  {WHOLE.name:<16} {WHOLE.stat().st_size / 1e6:6.1f} MB")
    print(
        f"  {BY_DAY.name:<16} {sum(f.stat().st_size for f in files) / 1e6:6.1f} MB,"
        f" {len(files)} files"
    )


if __name__ == "__main__":
    main()
