-- A trip that ends half an hour before it starts.
-- Refused by: trips_end_after_start, the check constraint.

INSERT INTO trips (
    trip_id, driver_id, rider_id, pickup_zone_id, dropoff_zone_id,
    pickup_at, dropoff_at, distance_km, fare, tip
) VALUES (
    999000002, 1, 1, 132, 138,
    '2024-01-15 08:00:00-05', '2024-01-15 07:30:00-05', 12.5, 40.00, 5.00
);
