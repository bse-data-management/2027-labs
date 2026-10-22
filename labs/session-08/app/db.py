"""The engine, the session each request gets, and the mapped classes."""

import sys
from collections.abc import Iterator
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from typing import Annotated

from fastapi import Depends
from sqlalchemy import ForeignKey, Numeric, create_engine
from sqlalchemy.orm import Mapped, Session, mapped_column

# Session 7's classes, imported from where you completed them.
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "session-07"))
from models import Base, Driver, Trip, Zone  # noqa: E402

if not hasattr(Trip, "fare"):
    raise SystemExit(
        "Trip in labs/session-07/models.py is not finished. See the README."
    )


# The one table session 7 did not map. Since session 4 a trip may have several
# payments.
class Payment(Base):
    __tablename__ = "payments"

    payment_id: Mapped[int] = mapped_column(primary_key=True)
    trip_id: Mapped[int] = mapped_column(ForeignKey("trips.trip_id"))
    method: Mapped[str]
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    paid_at: Mapped[datetime]


engine = create_engine("postgresql+psycopg://labs:labs@postgres:5432/labs")


def get_session() -> Iterator[Session]:
    """One session per request, closed when the response has been sent."""
    with Session(engine) as session:
        yield session


# Declared as a parameter of a route, this gives the route its session.
SessionDep = Annotated[Session, Depends(get_session)]

__all__ = ["Driver", "Payment", "SessionDep", "Trip", "Zone"]
