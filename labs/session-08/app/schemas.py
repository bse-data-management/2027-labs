"""What a caller sends and receives. These, not the tables, are the contract."""

from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class ZoneOut(BaseModel):
    # Read the fields from a mapped object's attributes.
    model_config = ConfigDict(from_attributes=True)

    zone_id: int
    name: str
    borough: str


# Part B, 1. A driver as a caller should see one. Choose the fields: there is no
# rule that every column of `drivers` belongs here.
class DriverOut(BaseModel):
    pass


# Part B, 2. A driver's earnings over a period: the driver, the period, the
# number of trips, the total of their fares, the total of their tips, and the
# total amount collected in payments. Money is Decimal, which JSON carries as a
# string, so that no cent is lost to floating point.
class EarningsOut(BaseModel):
    pass
