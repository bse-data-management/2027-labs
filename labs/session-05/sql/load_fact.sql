-- The load: from the normalised schema of sessions 3 and 4 into the star.
-- In a warehouse this runs on a schedule; here it runs when you call build_star().
-- dim_date is not loaded here, because it has no source to load from.

INSERT INTO dim_zone (zone_key, zone_name, borough, service_zone)
SELECT zone_id, name, borough, service_zone
FROM zones;


-- One row per trip. A fare split across several cards has several payments, so
-- payments are reduced to one row per trip before the join: session 4's fan-out,
-- dealt with once, here, instead of in every query that comes after.
--
-- There is no dim_payment. The method is the only thing known about a payment type,
-- so it stays on the fact row.
INSERT INTO fact_trips (
    trip_key, date_key, zone_key, payment_method, fare, tip, distance_km
)
SELECT t.trip_id,
       to_char(t.pickup_at, 'YYYYMMDD')::integer,  -- the pickup date, in New York
       t.pickup_zone_id,
       p.method,
       t.fare,
       t.tip,
       t.distance_km
FROM trips t
JOIN (
    -- Every part of a split fare is paid the same way, so any one method will do.
    SELECT trip_id, min(method) AS method
    FROM payments
    GROUP BY trip_id
) p ON p.trip_id = t.trip_id;

ANALYZE dim_date;
ANALYZE dim_zone;
ANALYZE fact_trips;
