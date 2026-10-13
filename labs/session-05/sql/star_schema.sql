-- The star: one fact table, two dimensions, each one join away.
--
-- fact_trips
-- Grain:
--
-- State the grain on the line above before writing anything else in this file.
-- The notebook will not build the schema until it is there.

DROP TABLE IF EXISTS fact_trips;
DROP TABLE IF EXISTS dim_zone;
DROP TABLE IF EXISTS dim_date;


-- The calendar. No source system holds it: it is generated, one row per day of
-- 2024, whether or not anyone took a taxi that day. A fixed year rather than the
-- span of the trips, so that a day with no trips still has a row to report zero on.
CREATE TABLE dim_date (
    date_key    integer PRIMARY KEY,           -- 20240115: readable, sorts like the date
    date        date    NOT NULL UNIQUE,
    day_of_week text    NOT NULL,
    is_weekend  boolean NOT NULL,
    month       integer NOT NULL,
    month_name  text    NOT NULL,
    quarter     integer NOT NULL,
    year        integer NOT NULL
);

INSERT INTO dim_date
SELECT to_char(d, 'YYYYMMDD')::integer,
       d,
       to_char(d, 'FMDay'),
       extract(isodow FROM d) IN (6, 7),
       extract(month FROM d),
       to_char(d, 'FMMonth'),
       extract(quarter FROM d),
       extract(year FROM d)
FROM generate_series(date '2024-01-01', date '2024-12-31', interval '1 day') AS d;


-- The zones, with the borough repeated on every zone in it. Deliberate: session 3's
-- rules would move borough into a table of its own, but this table has one writer,
-- the load, so there is no second copy to fall out of step, and grouping by borough
-- costs no extra join.
CREATE TABLE dim_zone (
    zone_key     integer PRIMARY KEY,
    zone_name    text NOT NULL,
    borough      text NOT NULL,
    service_zone text NOT NULL
);


-- Your table. sql/load_fact.sql fills these columns, so they must exist with these
-- names: trip_key, date_key, zone_key (the pickup zone), payment_method, fare, tip,
-- distance_km. Choose the types, the primary key, and what each key refers to.
CREATE TABLE fact_trips (

);
