CREATE TABLE cp_datawarehouse.rides (
  ride_id text PRIMARY KEY,
  user_id text,
  from_zipcode text,
  to_zipcode text,
  state text,
  quote_date timestamp,
  completed_date timestamp,
  price_nominal numeric,
  loyalty_points_earned int
);
