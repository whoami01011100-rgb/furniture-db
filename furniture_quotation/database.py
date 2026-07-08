# ============================================================
# database.py — MySQL Database Connection & Operations
# ============================================================
# Ye file MySQL se connect karti hai aur quotations save/fetch karti hai.
#
# SQLite se MySQL kyun switch kiya?
#   - MySQL ek real production database hai
#   - Multiple users ek saath use kar sakte hain
#   - MySQL Workbench se data visually dekh sakte hain
#
# Is file mein teen kaam hain:
#   1. get_connection()     → MySQL se ek connection banana
#   2. init_db()            → Database + Table auto-create karna
#   3. save_quotation()     → Ek quotation MySQL mein save karna
#   4. get_all_quotations() → Saari quotations fetch karna
#   5. get_quotation_by_id()→ Ek specific quotation fetch karna
# ============================================================

import mysql.connector
from mysql.connector import Error
from config import MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE
from queries import (
    CREATE_DB_QUERY, USE_DB_QUERY, CREATE_TABLE_QUERY,
    CREATE_USERS_TABLE, 
    CREATE_USER, GET_USER_BY_USERNAME, GET_USER_BY_ID, UPDATE_USER_PROFILE,
    INSERT_QUOTATION_QUERY, GET_ALL_QUOTATIONS_QUERY, GET_QUOTATION_BY_ID_QUERY
)


# ── Step 1: MySQL se connect karo ────────────────────────────────
def get_connection():
    """
    MySQL database se connection return karta hai.
    Agar connection fail ho, error print karta hai.
    """
    try:
        conn = mysql.connector.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE
        )
        return conn
    except Error as e:
        print(f"[ERROR] MySQL connection failed: {e}")
        print(f"[HINT] config.py mein MYSQL_PASSWORD check karo!")
        raise


# ── Step 2: Database + Table auto-create karo ────────────────────
def init_db():
    """
    1. Pehle 'woodcraft_db' database create karta hai (agar nahi hai)
    2. Phir 'quotations' table create karta hai (agar nahi hai)

    Ye function app.py mein startup pe call hota hai.
    """
    try:
        # Pehle bina database ke connect karo (root level connection)
        conn = mysql.connector.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD
        )
        cursor = conn.cursor()

        # Database create karo agar exist nahi karta
        cursor.execute(CREATE_DB_QUERY.format(db_name=MYSQL_DATABASE))
        cursor.execute(USE_DB_QUERY.format(db_name=MYSQL_DATABASE))

        # Quotations table create karo agar exist nahi karta
        cursor.execute(CREATE_USERS_TABLE)
        cursor.execute(CREATE_TABLE_QUERY)

        conn.commit()
        cursor.close()
        conn.close()
        print("[OK] MySQL database ready — woodcraft_db.quotations table exists")

    except Error as e:
        print(f"[ERROR] Database init failed: {e}")
        raise


# ── User Functions ──
def create_user(username, password_hash):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(CREATE_USER, (username, password_hash))
        conn.commit()
        return True
    except mysql.connector.IntegrityError:
        return False  # Username already exists
    finally:
        cursor.close()
        conn.close()

def get_user(username):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(GET_USER_BY_USERNAME, (username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

def get_user_by_id(user_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(GET_USER_BY_ID, (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

def update_user_profile(user_id, full_name, phone, address):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(UPDATE_USER_PROFILE, (full_name, phone, address, user_id))
    conn.commit()
    cursor.close()
    conn.close()


# ── Step 3: Quotation save karo ──────────────────────────────────
def save_quotation(user_id, customer, phone, item_name, category,
                   L, W, H, material, finish, quote_dict):
    """
    MySQL mein ek naya quotation record insert karta hai.

    Parameters:
        customer   → customer ka naam
        phone      → phone number
        item_name  → furniture naam
        category   → furniture category
        L, W, H    → dimensions (feet)
        material   → selected material
        finish     → selected finish
        quote_dict → calculate_quotation() ka return value (dictionary)

    Returns:
        qid → naye record ka ID (integer)
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(INSERT_QUOTATION_QUERY, (
        user_id, customer, phone, item_name, category,
        L, W, H, material, finish,
        quote_dict.get("board_area", 0),
        quote_dict.get("material_cost", 0),
        quote_dict.get("labor_cost", 0),
        quote_dict.get("finish_cost", 0),
        quote_dict.get("hardware_cost", 0),
        quote_dict.get("subtotal", 0),
        quote_dict.get("gst", 0),
        quote_dict.get("total", 0),
        "confirmed"
    ))

    conn.commit()
    qid = cursor.lastrowid  # Naya record ka ID
    cursor.close()
    conn.close()
    print(f"[OK] Quotation #{qid} saved to MySQL")
    return qid


# ── Step 4: Saari quotations fetch karo ──────────────────────────
def get_all_quotations(user_id):
    """
    History page ke liye logged-in user ki last 100 quotations fetch karta hai.
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)  # dictionary=True → row dict mein milti hai

    cursor.execute(GET_ALL_QUOTATIONS_QUERY, (user_id,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


# ── Step 5: Ek specific quotation fetch karo ─────────────────────
def get_quotation_by_id(qid):
    """
    PDF banane ke liye ek specific quotation fetch karta hai.

    Parameters:
        qid → quotation ID (integer)

    Returns:
        row → dictionary ya None (agar nahi mila)
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(GET_QUOTATION_BY_ID_QUERY, (qid,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row
