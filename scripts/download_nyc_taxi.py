"""Download one month of NYC yellow taxi trips and convert it to four formats.

    uv run --group session02 python scripts/download_nyc_taxi.py

Writes to data/nyc-taxi/, and skips whatever is already there. To start over,
delete that folder. Set ROW_CAP to use fewer rows on a small laptop.
"""

import os
import sqlite3
import urllib.request
from pathlib import Path

import pandas as pd

MONTH = "2024-01"
URL = f"https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{MONTH}.parquet"
ROWS = int(os.environ.get("ROW_CAP", 1_000_000))

DATA = Path(__file__).resolve().parents[1] / "data" / "nyc-taxi"
RAW = DATA / f"yellow_tripdata_{MONTH}.parquet"


def to_sqlite(trips, path):
    with sqlite3.connect(path) as connection:
        trips.to_sql("trips", connection, index=False, chunksize=100_000)


FORMATS = {
    # Chunked, as Parquet files normally are: one 1M-row chunk would leave the
    # reader nothing to skip.
    "trips.parquet": lambda trips, path: trips.to_parquet(
        path, index=False, row_group_size=100_000
    ),
    "trips.csv": lambda trips, path: trips.to_csv(path, index=False),
    "trips.jsonl": lambda trips, path: trips.to_json(
        path, orient="records", lines=True, date_format="iso"
    ),
    "trips.sqlite": to_sqlite,
}


def main():
    DATA.mkdir(parents=True, exist_ok=True)

    if not RAW.exists():
        print(f"downloading {URL}")
        partial = RAW.with_suffix(".part")
        urllib.request.urlretrieve(URL, partial)
        partial.rename(RAW)  # so an interrupted download never looks finished

    missing = {
        name: write for name, write in FORMATS.items() if not (DATA / name).exists()
    }
    if not missing:
        print(f"already converted, in {DATA}")
        return

    trips = pd.read_parquet(RAW).head(ROWS)
    trips.insert(0, "trip_id", range(1, len(trips) + 1))  # the TLC data has no id

    # Shuffled on purpose: ids assigned in order would sit in order on disk, and a
    # lookup by id would then be answerable from Parquet's chunk statistics alone.
    # Real files are rarely sorted by the thing you happen to search for.
    trips = trips.sample(frac=1, random_state=0)
    print(f"{len(trips):,} rows, {len(trips.columns)} columns, shuffled")

    for name, write in missing.items():
        write(trips, DATA / name)
        print(f"  {name:<14} {(DATA / name).stat().st_size / 1_000_000:6,.0f} MB")


main()
