-- A second driver holding a licence number that driver 1 already has.
-- Refused by: drivers_licence_no_key, the unique constraint.

INSERT INTO drivers (driver_id, full_name, licence_no, hired_on, home_zone_id)
VALUES (999999, 'Someone Else', 'NYC-100000', '2024-01-15', 132);
