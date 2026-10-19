"""The company's tables, as Python classes.

Every class here describes a table that already exists: session 3's schema.sql
created them. Nothing in this lab creates a table from these classes, so each one
must agree with the database exactly: the same table name, the same column names,
the same types.
"""

from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import BigInteger, DateTime, ForeignKey, Numeric, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    # The schema uses text and timestamptz throughout. With these two lines a
    # plain Mapped[str] or Mapped[datetime] means the same, so no column has to
    # say so.
    type_annotation_map = {
        str: Text,
        datetime: DateTime(timezone=True),
    }


# Zones and riders are mapped only so that the foreign keys below have a table to
# point at. The lab does not query them.


class Zone(Base):
    __tablename__ = "zones"

    zone_id: Mapped[int] = mapped_column(primary_key=True)
    borough: Mapped[str]
    name: Mapped[str]
    service_zone: Mapped[str]


class Rider(Base):
    __tablename__ = "riders"

    rider_id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str]
    signed_up_on: Mapped[date]


# The worked example. Compare it line by line with CREATE TABLE drivers in
# labs/session-03/sql/schema.sql.


class Driver(Base):
    __tablename__ = "drivers"

    driver_id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str]
    licence_no: Mapped[str] = mapped_column(unique=True)
    hired_on: Mapped[date]
    home_zone_id: Mapped[int] = mapped_column(ForeignKey("zones.zone_id"))

    # Part A: a driver's trips, the other side of Trip.driver, goes here.


# Part A: complete this class. The columns are in CREATE TABLE trips in
# labs/session-03/sql/schema.sql; copy their names exactly.
#
# - trip_id is a bigint, not an integer.
# - Money is numeric(10, 2) and distance numeric(8, 2): give each Numeric its
#   precision and scale, and annotate it as Mapped[Decimal].
# - tip may be NULL. Say so in the annotation.
# - Four columns point at other tables, and each needs its ForeignKey.
# - Add a `driver` relationship here, and `trips` on Driver, each naming the
#   other in back_populates.


class Trip(Base):
    __tablename__ = "trips"

    trip_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
