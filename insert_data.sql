-- Do'konlar
INSERT INTO stores (store_name, location) VALUES
('Ishonch Center', 'Toshkent'),
('Ishonch West', 'Samarqand'),
('Ishonch East', 'Buxoro');

-- Mahsulotlar
INSERT INTO products (product_name, category, price) VALUES
('Televizor', 'Electronics', 500.00),
('Muzlatkich', 'Appliance', 300.00),
('Kir yuvish mashinasi', 'Appliance', 400.00),
('Kompyuter', 'Electronics', 800.00);

-- Mijozlar
INSERT INTO customers (name, age, gender, location) VALUES
('Ali', 30, 'Male', 'Toshkent'),
('Vali', 45, 'Male', 'Samarqand'),
('Gulnora', 28, 'Female', 'Buxoro'),
('Olim', 35, 'Male', 'Toshkent');

-- Savdolar (faqat kredit savdolari uchun misollar)
INSERT INTO sales (store_id, product_id, sale_date, sale_type, amount) VALUES
(1, 1, '2025-03-01', 'credit', 500.00),
(1, 2, '2025-03-02', 'cash', 300.00),
(2, 3, '2025-03-03', 'credit', 400.00),
(3, 4, '2025-03-04', 'credit', 800.00);

-- Kredit arizalari
INSERT INTO credit_applications (customer_id, store_id, application_date, status) VALUES
(1, 1, '2025-03-01', 'approved'),
(2, 2, '2025-03-03', 'approved'),
(3, 3, '2025-03-04', 'pending'),
(4, 1, '2025-03-05', 'rejected');

-- To'lovlar
INSERT INTO payments (credit_id, payment_date, amount, payment_status) VALUES
(1, '2025-03-15', 250.00, 'on_time'),
(1, '2025-04-15', 250.00, 'on_time'),
(2, '2025-03-20', 400.00, 'delayed'),
(3, '2025-03-25', 200.00, 'on_time');

-- Inventarizatsiya
INSERT INTO inventory (store_id, product_id, quantity, last_updated) VALUES
(1, 1, 10, '2025-03-01'),
(1, 2, 15, '2025-03-01'),
(2, 3, 8, '2025-03-01'),
(3, 4, 5, '2025-03-01');

-- Moliyaviy ko'rsatkichlar
INSERT INTO financials (store_id, record_date, revenue, expenses) VALUES
(1, '2025-03-31', 10000.00, 7000.00),
(2, '2025-03-31', 8000.00, 5000.00),
(3, '2025-03-31', 6000.00, 4000.00);
