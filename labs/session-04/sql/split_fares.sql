-- Since January, a rider can split a fare across several cards. Each part is a
-- payment of its own, so one trip may now have several rows in payments.
--
-- Session 3's schema said a trip may not be paid twice. That rule no longer
-- describes the business, so the constraint that enforced it goes. The foreign
-- key stays: every payment must still belong to a real trip.

ALTER TABLE payments DROP CONSTRAINT payments_trip_id_key;
