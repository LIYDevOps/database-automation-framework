-- Drop table if exists (idempotent)
DROP TABLE IF EXISTS orders;

-- Create table
CREATE TABLE orders (
  order_id SERIAL PRIMARY KEY,
  customer_id INT,
  order_date DATE,
  amount NUMERIC
);

-- Insert sample data
INSERT INTO orders (customer_id, order_date, amount)
SELECT
  (random() * 1000)::INT,
  CURRENT_DATE - (random() * 365)::INT,
  (random() * 5000)::INT
FROM generate_series(1, 100000);
