# ============================================================
# queries.py — SQL Queries for MySQL Database
# ============================================================

# ── Database & Table Creation Queries ──
CREATE_DB_QUERY = "CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
USE_DB_QUERY = "USE `{db_name}`"

DROP_TABLES_QUERY = """
DROP TABLE IF EXISTS quotations;
DROP TABLE IF EXISTS users;
"""

CREATE_USERS_TABLE = """
CREATE TABLE IF NOT EXISTS users (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    username      VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name     VARCHAR(200) DEFAULT '',
    phone         VARCHAR(20)  DEFAULT '',
    address       TEXT,
    created_at    TIMESTAMP    DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
"""

CREATE_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS quotations (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    user_id       INT,
    customer      VARCHAR(200)  NOT NULL,
    phone         VARCHAR(20),
    item_name     VARCHAR(200)  NOT NULL,
    category      VARCHAR(100),
    length        FLOAT,
    width         FLOAT,
    height        FLOAT,
    material      VARCHAR(100),
    finish        VARCHAR(100),
    board_area    FLOAT,
    material_cost INT,
    labor_cost    INT,
    finish_cost   INT,
    hardware_cost INT,
    subtotal      INT,
    gst           INT,
    total_price   INT,
    status        VARCHAR(20)  DEFAULT 'confirmed',
    created_at    TIMESTAMP    DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
"""

# ── Users CRUD ──
CREATE_USER = "INSERT INTO users (username, password_hash) VALUES (%s, %s)"
GET_USER_BY_USERNAME = "SELECT * FROM users WHERE username = %s"
GET_USER_BY_ID = "SELECT * FROM users WHERE id = %s"
UPDATE_USER_PROFILE = "UPDATE users SET full_name = %s, phone = %s, address = %s WHERE id = %s"

# ── Quotations CRUD ──
INSERT_QUOTATION_QUERY = """
INSERT INTO quotations
    (user_id, customer, phone, item_name, category,
     length, width, height, material, finish,
     board_area, material_cost, labor_cost, finish_cost,
     hardware_cost, subtotal, gst, total_price, status)
VALUES
    (%s, %s, %s, %s, %s,
     %s, %s, %s, %s, %s,
     %s, %s, %s, %s,
     %s, %s, %s, %s, %s)
"""

GET_ALL_QUOTATIONS_QUERY = """
SELECT * FROM quotations
WHERE user_id = %s
ORDER BY created_at DESC
LIMIT 100
"""

GET_QUOTATION_BY_ID_QUERY = "SELECT * FROM quotations WHERE id = %s"
