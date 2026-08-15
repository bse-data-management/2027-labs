-- The company's database: six tables, one fact in one place.
-- Runs from empty, in this order, because a table cannot point at one that does
-- not exist yet.

DROP TABLE IF EXISTS payments;
DROP TABLE IF EXISTS trips;
DROP TABLE IF EXISTS driver_balances;
DROP TABLE IF EXISTS drivers;
DROP TABLE IF EXISTS riders;
DROP TABLE IF EXISTS zones;

-- Timestamps are stored with their offset, and read back as New York time.
ALTER DATABASE labs SET timezone = 'America/New_York';


-- Zones come from the city. The id is theirs, so it is a natural key.
CREATE TABLE zones (
    zone_id      integer PRIMARY KEY,
    borough      text NOT NULL,
    name         text NOT NULL,
    service_zone text NOT NULL
);


CREATE TABLE drivers (
    driver_id    integer PRIMARY KEY,          -- surrogate key: ours, not the city's
    full_name    text NOT NULL,
    -- The licence number is unique in the world, so it must be unique here.
    licence_no   text NOT NULL UNIQUE,
    hired_on     date NOT NULL,
    home_zone_id integer NOT NULL REFERENCES zones (zone_id)
);


CREATE TABLE riders (
    rider_id     integer PRIMARY KEY,
    full_name    text NOT NULL,
    signed_up_on date NOT NULL
);


-- One row per driver, and no driver may have two. The primary key says both.
CREATE TABLE driver_balances (
    driver_id  integer PRIMARY KEY REFERENCES drivers (driver_id),
    balance    numeric(10, 2) NOT NULL,
    updated_at timestamptz NOT NULL
);


CREATE TABLE trips (
    trip_id         bigint PRIMARY KEY,        -- assigned on load; the city has no trip id
    driver_id       integer NOT NULL REFERENCES drivers (driver_id),
    rider_id        integer NOT NULL REFERENCES riders (rider_id),
    pickup_zone_id  integer NOT NULL REFERENCES zones (zone_id),
    dropoff_zone_id integer NOT NULL REFERENCES zones (zone_id),
    pickup_at       timestamptz NOT NULL,
    dropoff_at      timestamptz NOT NULL,
    distance_km     numeric(8, 2) NOT NULL,
    -- Money is numeric, never a floating point type.
    fare            numeric(10, 2) NOT NULL,
    -- Nullable on purpose: a missing tip is unknown, which is not the same as 0.
    tip             numeric(10, 2),

    -- A trip cannot end before it starts.
    CONSTRAINT trips_end_after_start CHECK (dropoff_at >= pickup_at),
    CONSTRAINT trips_fare_not_negative CHECK (fare >= 0),
    CONSTRAINT trips_distance_not_negative CHECK (distance_km >= 0)
);


CREATE TABLE payments (
    payment_id integer PRIMARY KEY,
    -- One payment per trip: the trip must exist, and may not be paid twice.
    trip_id    bigint NOT NULL UNIQUE REFERENCES trips (trip_id),
    method     text NOT NULL,
    amount     numeric(10, 2) NOT NULL,
    paid_at    timestamptz NOT NULL,

    CONSTRAINT payments_method_known CHECK (
        method IN ('credit card', 'cash', 'no charge', 'dispute', 'unknown', 'voided trip')
    )
);
