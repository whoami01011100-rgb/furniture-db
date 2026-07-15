# database.py — SQLite setup (no MySQL, built-in Python)
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'furniture.db')


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quotations (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            customer    TEXT    NOT NULL,
            phone       TEXT,
            item_name   TEXT    NOT NULL,
            category    TEXT,
            length      REAL,
            width       REAL,
            height      REAL,
            material    TEXT,
            finish      TEXT,
            total_price REAL,
            created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()


def save_quotation(customer, phone, item_name, category, L, W, H, material, finish, total_price):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO quotations
            (customer, phone, item_name, category, length, width, height, material, finish, total_price)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (customer, phone, item_name, category, L, W, H, material, finish, total_price))
    conn.commit()
    qid = cursor.lastrowid
    conn.close()
    return qid


def get_all_quotations():
    conn = get_connection()
    rows = conn.execute(
        'SELECT * FROM quotations ORDER BY created_at DESC LIMIT 50'
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]
