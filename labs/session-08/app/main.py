"""The routes: HTTP in, HTTP out. The work is in services.py."""

from datetime import date
from typing import Annotated

from fastapi import FastAPI, HTTPException, Query

from app import services
from app.db import SessionDep
from app.schemas import DriverOut, EarningsOut, ZoneOut

app = FastAPI(title="Taxi company API")


@app.get("/zones/{zone_id}")
def read_zone(zone_id: int, session: SessionDep) -> ZoneOut:
    zone = services.get_zone(session, zone_id)
    if zone is None:
        raise HTTPException(status_code=404, detail=f"no zone {zone_id}")
    return zone


@app.get("/drivers/{driver_id}")
def read_driver(driver_id: int, session: SessionDep) -> DriverOut:
    # Part B, 1. 501 Not Implemented until you replace this line.
    raise HTTPException(status_code=501, detail="not written yet")


@app.get("/drivers/{driver_id}/earnings")
def read_earnings(
    driver_id: int,
    session: SessionDep,
    # `from` is a Python keyword, so the parameter is from_ in Python and from in
    # the URL.
    from_: Annotated[date, Query(alias="from")],
    to: date,
) -> EarningsOut:
    # Part B, 2.
    raise HTTPException(status_code=501, detail="not written yet")
