"""Session 1: the mean fare per month."""

from pathlib import Path

import pandas as pd

DATA = Path(__file__).resolve().parents[2] / "data" / "test"

MONTHS = [
    ("January", "trips_jan.csv"),
    ("February", "trips_feb.csv"),
]


def load_trips(path):
    return pd.read_csv(path)


def mean_fare(trips):
    return trips["fare"].dropna().mean()


def main():
    print("Mean fare per month (missing fares dropped)")
    print("-------------------------------------------")
    for label, filename in MONTHS:
        trips = load_trips(DATA / filename)
        print(f"  {label:<9} {mean_fare(trips):>6.2f}")


if __name__ == "__main__":
    main()
