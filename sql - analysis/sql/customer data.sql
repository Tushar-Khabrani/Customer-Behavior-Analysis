DROP DATABASE IF EXISTS customer_behavior;
CREATE DATABASE customer_behavior;
USE customer_behavior;

CREATE TABLE customers (
    customer_id  INT PRIMARY KEY,
    name         VARCHAR(50),
    city         VARCHAR(50),
    signup_date  DATE
);

CREATE TABLE products (
    product_id   INT PRIMARY KEY,
    product_name VARCHAR(100),
    category     VARCHAR(50),
    price        DECIMAL(10,2)
);

CREATE TABLE orders (
    order_id    INT PRIMARY KEY,
    customer_id INT,
    order_date  DATETIME,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE order_items (
    order_item_id INT PRIMARY KEY,
    order_id      INT,
    product_id    INT,
    quantity      INT,
    FOREIGN KEY (order_id)   REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

INSERT INTO customers VALUES
(1,  'Rahul',   'Ahmedabad', '2023-01-10'),
(2,  'Priya',   'Mumbai',    '2023-02-05'),
(3,  'Amit',    'Delhi',     '2023-03-12'),
(4,  'Neha',    'Pune',      '2023-04-08'),
(5,  'Karan',   'Bangalore', '2023-05-01'),
(6,  'Sneha',   'Hyderabad', '2023-06-11'),
(7,  'Arjun',   'Jaipur',    '2023-07-02'),
(8,  'Ritika',  'Ahmedabad', '2023-07-20'),
(9,  'Vikram',  'Delhi',     '2023-08-15'),
(10, 'Anjali',  'Mumbai',    '2023-09-10'),
(11, 'Rohit',   'Ahmedabad', '2023-09-25'),
(12, 'Deepika', 'Chennai',   '2023-10-05'),
(13, 'Saurabh', 'Pune',      '2023-10-18'),
(14, 'Meera',   'Bangalore', '2023-11-01'),
(15, 'Nikhil',  'Mumbai',    '2023-11-20');

INSERT INTO products VALUES
(101, 'iPhone 14',        'Electronics', 80000),
(102, 'Laptop HP',        'Electronics', 60000),
(103, 'Samsung Galaxy',   'Electronics', 70000),
(104, 'Headphones',       'Electronics',  4000),
(105, 'Gaming Mouse',     'Electronics',  1500),
(106, 'Nike Shoes',       'Fashion',       5000),
(107, 'Adidas T-Shirt',   'Fashion',       2000),
(108, 'Levi Jeans',       'Fashion',       3500),
(109, 'Smart Watch',      'Accessories',   3000),
(110, 'Backpack',         'Accessories',   2500),
(111, 'Sunglasses',       'Accessories',   1800),
(112, 'Office Chair',     'Furniture',     7000),
(113, 'Study Table',      'Furniture',     5500);

INSERT INTO orders VALUES
(1001, 1,  '2024-01-10 10:30:00'),
(1002, 2,  '2024-01-15 11:00:00'),
(1003, 3,  '2024-02-01 09:15:00'),
(1004, 4,  '2024-02-05 14:45:00'),
(1005, 5,  '2024-02-20 16:10:00'),
(1006, 6,  '2024-03-10 13:00:00'),
(1007, 7,  '2024-03-22 18:30:00'),
(1008, 8,  '2024-04-01 09:00:00'),
(1009, 9,  '2024-04-15 12:40:00'),
(1010, 10, '2024-04-28 10:10:00'),
(1011, 1,  '2024-05-05 11:20:00'),   
(1012, 2,  '2024-05-18 15:25:00'),   
(1013, 5,  '2024-06-01 12:50:00'),   
(1014, 11, '2024-06-15 17:00:00'),
(1015, 12, '2024-07-02 10:30:00'),
(1016, 13, '2024-07-18 14:20:00'),
(1017, 14, '2024-08-05 09:45:00'),
(1018, 15, '2024-08-20 16:00:00'),
(1019, 3,  '2024-09-01 11:10:00'),  
(1020, 6,  '2024-09-15 13:30:00');   

INSERT INTO order_items VALUES
(1,  1001, 101, 1),
(2,  1001, 109, 1),
(3,  1002, 106, 2),
(4,  1003, 102, 1),
(5,  1004, 109, 1),
(6,  1005, 107, 3),
(7,  1006, 104, 2),
(8,  1007, 110, 1),
(9,  1008, 101, 1),
(10, 1009, 106, 2),
(11, 1010, 107, 1),
(12, 1011, 105, 2),
(13, 1011, 111, 1),
(14, 1012, 103, 1),
(15, 1013, 101, 1),
(16, 1014, 112, 1),
(17, 1015, 104, 1),
(18, 1016, 108, 2),
(19, 1017, 102, 1),
(20, 1018, 113, 1),
(21, 1019, 110, 2),
(22, 1020, 109, 1);

SELECT * FROM customers;
SELECT * FROM products;
SELECT * FROM orders;
SELECT * FROM order_items;

SELECT
    c.customer_id,
    c.name,
    c.city,
    DATE(o.order_date)  AS order_date,
    p.product_name,
    p.category,
    p.price,
    oi.quantity,
    (p.price * oi.quantity) AS revenue
FROM orders o
JOIN customers   c  ON o.customer_id  = c.customer_id
JOIN order_items oi ON o.order_id     = oi.order_id
JOIN products    p  ON oi.product_id  = p.product_id
ORDER BY o.order_date;

SELECT SUM(p.price * oi.quantity) AS total_revenue
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id;

SELECT
    DATE_FORMAT(o.order_date, '%Y-%m') AS month,
    SUM(p.price * oi.quantity)         AS monthly_revenue
FROM orders o
JOIN order_items oi ON o.order_id    = oi.order_id
JOIN products    p  ON oi.product_id = p.product_id
GROUP BY month
ORDER BY month;

SELECT
    c.city,
    SUM(p.price * oi.quantity) AS city_revenue
FROM orders o
JOIN customers   c  ON o.customer_id  = c.customer_id
JOIN order_items oi ON o.order_id     = oi.order_id
JOIN products    p  ON oi.product_id  = p.product_id
GROUP BY c.city
ORDER BY city_revenue DESC;

SELECT
    p.category,
    SUM(p.price * oi.quantity) AS category_revenue
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
GROUP BY p.category
ORDER BY category_revenue DESC;

SELECT
    c.customer_id,
    c.name,
    SUM(p.price * oi.quantity) AS total_spent
FROM orders o
JOIN customers   c  ON o.customer_id  = c.customer_id
JOIN order_items oi ON o.order_id     = oi.order_id
JOIN products    p  ON oi.product_id  = p.product_id
GROUP BY c.customer_id, c.name
ORDER BY total_spent DESC
LIMIT 5;

SELECT
    p.product_name,
    SUM(oi.quantity) AS units_sold
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
GROUP BY p.product_name
ORDER BY units_sold DESC;

SELECT
    c.name,
    COUNT(o.order_id) AS total_orders
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.name
HAVING COUNT(o.order_id) > 1
ORDER BY total_orders DESC;

SELECT
    ROUND(AVG(order_total), 2) AS avg_order_value
FROM (
    SELECT o.order_id, SUM(p.price * oi.quantity) AS order_total
    FROM orders o
    JOIN order_items oi ON o.order_id    = oi.order_id
    JOIN products    p  ON oi.product_id = p.product_id
    GROUP BY o.order_id
) t;

SELECT
    c.name,
    SUM(p.price * oi.quantity)                                             AS total_spent,
    RANK() OVER (ORDER BY SUM(p.price * oi.quantity) DESC)                 AS spending_rank
FROM orders o
JOIN customers   c  ON o.customer_id  = c.customer_id
JOIN order_items oi ON o.order_id     = oi.order_id
JOIN products    p  ON oi.product_id  = p.product_id
GROUP BY c.customer_id, c.name;

SELECT
    DATE(o.order_date)                                                         AS order_date,
    SUM(p.price * oi.quantity)                                                 AS daily_revenue,
    SUM(SUM(p.price * oi.quantity)) OVER (ORDER BY DATE(o.order_date))         AS running_total
FROM orders o
JOIN order_items oi ON o.order_id    = oi.order_id
JOIN products    p  ON oi.product_id = p.product_id
GROUP BY DATE(o.order_date)
ORDER BY order_date;

SELECT
    month,
    monthly_revenue,
    LAG(monthly_revenue) OVER (ORDER BY month)                                      AS prev_month_revenue,
    ROUND(
        (monthly_revenue - LAG(monthly_revenue) OVER (ORDER BY month))
        / LAG(monthly_revenue) OVER (ORDER BY month) * 100
    , 2)                                                                             AS growth_percent
FROM (
    SELECT
        DATE_FORMAT(o.order_date, '%Y-%m') AS month,
        SUM(p.price * oi.quantity)         AS monthly_revenue
    FROM orders o
    JOIN order_items oi ON o.order_id    = oi.order_id
    JOIN products    p  ON oi.product_id = p.product_id
    GROUP BY month
) t
ORDER BY month;

SELECT
    c.customer_id,
    c.name,
    COUNT(DISTINCT o.order_id)         AS total_orders,
    SUM(p.price * oi.quantity)         AS lifetime_value,
    RANK() OVER (ORDER BY SUM(p.price * oi.quantity) DESC) AS clv_rank
FROM orders o
JOIN customers   c  ON o.customer_id  = c.customer_id
JOIN order_items oi ON o.order_id     = oi.order_id
JOIN products    p  ON oi.product_id  = p.product_id
GROUP BY c.customer_id, c.name;

CREATE VIEW monthly_revenue_view AS
SELECT
    DATE_FORMAT(o.order_date, '%Y-%m') AS month,
    SUM(p.price * oi.quantity)         AS monthly_revenue
FROM orders o
JOIN order_items oi ON o.order_id    = oi.order_id
JOIN products    p  ON oi.product_id = p.product_id
GROUP BY month;

SELECT * FROM monthly_revenue_view;

DELIMITER //

CREATE PROCEDURE GetRevenueByCity(IN city_name VARCHAR(50))
BEGIN
    SELECT
        c.city,
        SUM(p.price * oi.quantity) AS total_revenue
    FROM orders o
    JOIN customers   c  ON o.customer_id  = c.customer_id
    JOIN order_items oi ON o.order_id     = oi.order_id
    JOIN products    p  ON oi.product_id  = p.product_id
    WHERE c.city = city_name
    GROUP BY c.city;
END //

DELIMITER ;

CALL GetRevenueByCity('Ahmedabad');
CALL GetRevenueByCity('Mumbai');

CREATE TABLE order_log (
    log_id      INT AUTO_INCREMENT PRIMARY KEY,
    order_id    INT,
    logged_at   DATETIME DEFAULT NOW()
);

DELIMITER //

CREATE TRIGGER log_new_order
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    INSERT INTO order_log (order_id, logged_at)
    VALUES (NEW.order_id, NOW());
END //

DELIMITER ;
