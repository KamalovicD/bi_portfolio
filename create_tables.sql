-- Avval mavjud jadvallarni tozalash (agar mavjud bo'lsa)
DROP TABLE IF EXISTS sales, credit_applications, payments, inventory, financials, customers, products, stores CASCADE;

-- Do'konlar
CREATE TABLE IF NOT EXISTS stores (
  store_id SERIAL PRIMARY KEY,
  store_name VARCHAR(100),
  location VARCHAR(100)
);

-- Mahsulotlar
CREATE TABLE IF NOT EXISTS products (
  product_id SERIAL PRIMARY KEY,
  product_name VARCHAR(100),
  category VARCHAR(50),
  price NUMERIC(10,2)
);

-- Mijozlar
CREATE TABLE IF NOT EXISTS customers (
  customer_id SERIAL PRIMARY KEY,
  name VARCHAR(100),
  age INT,
  gender VARCHAR(10),
  location VARCHAR(100)
);

-- Savdolar
CREATE TABLE IF NOT EXISTS sales (
  sale_id SERIAL PRIMARY KEY,
  store_id INT REFERENCES stores(store_id),
  product_id INT REFERENCES products(product_id),
  sale_date DATE,
  sale_type VARCHAR(20),
  amount NUMERIC(10,2)
);

-- Kredit arizalari
CREATE TABLE IF NOT EXISTS credit_applications (
  credit_id SERIAL PRIMARY KEY,
  customer_id INT REFERENCES customers(customer_id),
  store_id INT REFERENCES stores(store_id),
  application_date DATE,
  status VARCHAR(20)
);

-- To'lovlar
CREATE TABLE IF NOT EXISTS payments (
  payment_id SERIAL PRIMARY KEY,
  credit_id INT REFERENCES credit_applications(credit_id),
  payment_date DATE,
  amount NUMERIC(10,2),
  payment_status VARCHAR(20)
);

-- Inventarizatsiya
CREATE TABLE IF NOT EXISTS inventory (
  inventory_id SERIAL PRIMARY KEY,
  store_id INT REFERENCES stores(store_id),
  product_id INT REFERENCES products(product_id),
  quantity INT,
  last_updated DATE
);

-- Moliyaviy ko'rsatkichlar
CREATE TABLE IF NOT EXISTS financials (
  financial_id SERIAL PRIMARY KEY,
  store_id INT REFERENCES stores(store_id),
  record_date DATE,
  revenue NUMERIC(10,2),
  expenses NUMERIC(10,2)
);
