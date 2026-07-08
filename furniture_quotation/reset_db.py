import mysql.connector
from config import MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE
from queries import CREATE_DB_QUERY, USE_DB_QUERY, DROP_TABLES_QUERY, CREATE_USERS_TABLE, CREATE_TABLE_QUERY, CREATE_USER
from werkzeug.security import generate_password_hash

def reset():
    print("Connecting to MySQL...")
    conn = mysql.connector.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD
    )
    cursor = conn.cursor()
    cursor.execute(CREATE_DB_QUERY.format(db_name=MYSQL_DATABASE))
    cursor.execute(USE_DB_QUERY.format(db_name=MYSQL_DATABASE))
    
    print("Dropping old tables...")
    for query in DROP_TABLES_QUERY.split(';'):
        if query.strip():
            cursor.execute(query.strip())
            
    print("Recreating tables...")
    cursor.execute(CREATE_USERS_TABLE)
    cursor.execute(CREATE_TABLE_QUERY)
    
    print("Creating test admin user...")
    cursor.execute(CREATE_USER, ("admin", generate_password_hash("admin123")))
    
    conn.commit()
    cursor.close()
    conn.close()
    print("Database reset complete! The old broken tables are gone, and new ones are ready.")

if __name__ == "__main__":
    reset()
