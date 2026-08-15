"""Normalize the NYC taxi trips into the six-table schema used in session 3.

    uv run python scripts/prepare_nyc_taxi_normalized.py

The TLC files hold trips and nothing else: no trip id, no drivers, no riders, no
payments. Those are generated here, consistently enough that every foreign key in
sql/schema.sql holds on the first load. Zones come from the TLC lookup table.

Writes CSV files to data/nyc-taxi-normalized/, and skips whatever is already
there. Delete
the folder to start again. Set ROW_CAP for fewer trips.
"""

import os
import urllib.request
from pathlib import Path

import numpy as np
import pandas as pd

MONTH = "2024-01"
ZONES_URL = "https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv"
TRIPS_URL = (
    f"https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{MONTH}.parquet"
)

DATA = Path(__file__).resolve().parents[1] / "data"
RAW = DATA / "nyc-taxi" / f"yellow_tripdata_{MONTH}.parquet"
OUT = DATA / "nyc-taxi-normalized"

ROWS = int(os.environ.get("ROW_CAP", 1_000_000))
DRIVERS = 600
RIDERS = 20_000
TIP_MISSING = 0.05  # share of trips whose tip was never recorded — see README

# The TLC payment_type codes, spelled out.
METHODS = {
    1: "credit card",
    2: "cash",
    3: "no charge",
    4: "dispute",
    5: "unknown",
    6: "voided trip",
}

FIRST_NAMES = (
    "Ana Luis Marta Pau Nadia Tomas Irene Diego Sofia Marc "
    "Elena Hugo Clara Ivan Rosa Omar Lucia Pere Nuria Adam"
).split()
LAST_NAMES = (
    "Garcia Rossi Novak Haddad Okonjo Silva Muller Dubois Nowak Ferrari "
    "Costa Weber Moreau Kovac Santos Popescu Ahmed Ivanov Lopez Brandt"
).split()


def download(url: str, path: Path) -> None:
    if path.exists():
        return
    print(f"downloading {url}")
    partial = path.with_suffix(".part")
    urllib.request.urlretrieve(url, partial)
    partial.rename(path)


def build_zones() -> pd.DataFrame:
    """The 265 TLC taxi zones. Every trip's pickup and dropoff points at one."""
    lookup = DATA / "nyc-taxi" / "taxi_zone_lookup.csv"
    download(ZONES_URL, lookup)
    zones = pd.read_csv(lookup)
    zones = zones.rename(
        columns={
            "LocationID": "zone_id",
            "Borough": "borough",
            "Zone": "name",
            "service_zone": "service_zone",
        }
    )
    # A few lookup rows have blanks; the schema forbids nulls in these columns.
    for column in ("borough", "name", "service_zone"):
        zones[column] = zones[column].fillna("Unknown")
    return pd.DataFrame(zones[["zone_id", "borough", "name", "service_zone"]])


def build_people(
    rng: np.random.Generator, zone_ids: np.ndarray
) -> tuple[pd.DataFrame, ...]:
    """Drivers, their balances, and riders. None of this is in the TLC data."""
    names = [
        f"{first} {last}"
        for first, last in zip(
            rng.choice(FIRST_NAMES, DRIVERS + RIDERS),
            rng.choice(LAST_NAMES, DRIVERS + RIDERS),
            strict=True,
        )
    ]

    drivers = pd.DataFrame(
        {
            "driver_id": np.arange(1, DRIVERS + 1),
            "full_name": names[:DRIVERS],
            # Unique by construction: the schema also insists on it.
            "licence_no": [f"NYC-{100000 + i}" for i in range(DRIVERS)],
            "hired_on": pd.to_datetime("2019-01-01")
            + pd.to_timedelta(rng.integers(0, 1800, DRIVERS), unit="D"),
            "home_zone_id": rng.choice(zone_ids, DRIVERS),
        }
    )
    drivers["hired_on"] = drivers["hired_on"].dt.date

    balances = pd.DataFrame(
        {
            "driver_id": drivers["driver_id"],
            "balance": np.round(rng.uniform(0, 900, DRIVERS), 2),
            "updated_at": pd.Timestamp(f"{MONTH}-31 23:59:00-05:00"),
        }
    )

    riders = pd.DataFrame(
        {
            "rider_id": np.arange(1, RIDERS + 1),
            "full_name": names[DRIVERS:],
            "signed_up_on": pd.to_datetime("2020-01-01")
            + pd.to_timedelta(rng.integers(0, 1400, RIDERS), unit="D"),
        }
    )
    riders["signed_up_on"] = riders["signed_up_on"].dt.date
    return drivers, balances, riders


def build_trips(
    rng: np.random.Generator, zone_ids: list[int]
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """One month of real trips, with synthetic ids attached, plus their payments."""
    raw = pd.read_parquet(RAW)

    month_start = pd.Timestamp(f"{MONTH}-01")
    month_end = month_start + pd.offsets.MonthBegin(1)
    sane = (
        raw["tpep_pickup_datetime"].between(month_start, month_end, inclusive="left")
        & (raw["tpep_dropoff_datetime"] >= raw["tpep_pickup_datetime"])
        & (raw["fare_amount"] >= 0)
        & (raw["trip_distance"] >= 0)
        & raw["total_amount"].notna()
        & raw["payment_type"].notna()
        & raw["PULocationID"].isin(zone_ids)
        & raw["DOLocationID"].isin(zone_ids)
    )
    raw = raw.loc[sane]
    if len(raw) > ROWS:
        # Sampled, not the first N rows: taking the head would cover the first ten
        # days of the month and leave the rest of it empty.
        raw = raw.sample(n=ROWS, random_state=0)
    raw = raw.sort_values(by=["tpep_pickup_datetime"]).reset_index(drop=True)

    # Wall-clock New York time in the source; stated as such so timestamptz is right.
    pickup = raw["tpep_pickup_datetime"].dt.tz_localize(
        "America/New_York", ambiguous=True, nonexistent="shift_forward"
    )
    dropoff = raw["tpep_dropoff_datetime"].dt.tz_localize(
        "America/New_York", ambiguous=True, nonexistent="shift_forward"
    )

    tip = raw["tip_amount"].round(2)
    # Some tips were never recorded. Not zero — unknown.
    tip = tip.mask(rng.random(len(raw)) < TIP_MISSING)

    trips = pd.DataFrame(
        {
            "trip_id": np.arange(1, len(raw) + 1),
            "driver_id": rng.integers(1, DRIVERS + 1, len(raw)),
            "rider_id": rng.integers(1, RIDERS + 1, len(raw)),
            "pickup_zone_id": raw["PULocationID"],
            "dropoff_zone_id": raw["DOLocationID"],
            "pickup_at": pickup,
            "dropoff_at": dropoff,
            "distance_km": (raw["trip_distance"] * 1.60934).round(2),
            "fare": raw["fare_amount"].round(2),
            "tip": tip,
        }
    )

    payments = pd.DataFrame(
        {
            "payment_id": np.arange(1, len(raw) + 1),
            "trip_id": trips["trip_id"],
            "method": raw["payment_type"].map(
                lambda code: METHODS.get(int(code), "unknown")
            ),
            "amount": raw["total_amount"].round(2),
            "paid_at": dropoff,
        }
    )
    return trips, payments


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    tables = ["zones", "drivers", "driver_balances", "riders", "trips", "payments"]
    if all((OUT / f"{name}.csv").exists() for name in tables):
        print(f"already prepared, in {OUT}")
        return

    download(TRIPS_URL, RAW)
    rng = np.random.default_rng(0)

    zones = build_zones()
    drivers, balances, riders = build_people(rng, zones["zone_id"].to_numpy())
    trips, payments = build_trips(rng, zones["zone_id"].tolist())

    written = {
        "zones": zones,
        "drivers": drivers,
        "driver_balances": balances,
        "riders": riders,
        "trips": trips,
        "payments": payments,
    }
    for name, frame in written.items():
        frame.to_csv(OUT / f"{name}.csv", index=False)
        print(f"  {name:<16} {len(frame):>9,} rows")

    missing = trips["tip"].isna().mean()
    print(f"\ntips missing: {missing:.1%} of trips")


main()
