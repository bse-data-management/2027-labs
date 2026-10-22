"""What each endpoint returns, built from the database. Nothing here knows HTTP."""

from datetime import date

from sqlalchemy.orm import Session

from app.db import Zone
from app.schemas import DriverOut, EarningsOut, ZoneOut


def get_zone(session: Session, zone_id: int) -> ZoneOut | None:
    zone = session.get(Zone, zone_id)
    if zone is None:
        return None
    return ZoneOut.model_validate(zone)


# Part B, 1.
def get_driver(session: Session, driver_id: int) -> DriverOut | None:
    raise NotImplementedError


# Part B, 2. Trips picked up from `start` to `end`, both days included, New York
# time. Careful: a trip may have several payments, so joining trips to payments
# and summing fares counts some fares twice. Session 4, question 4.
def driver_earnings(
    session: Session, driver_id: int, start: date, end: date
) -> EarningsOut | None:
    raise NotImplementedError
