import sqlite3
import bcrypt

# --- Database setup with hashed password ---
def init_db():
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            analyst_id TEXT UNIQUE,
            name TEXT,
            password TEXT
        )
    """)

    # Insert a test user with a hashed password
    username = "admin"
    password = "1234"
    
    # object list 
    data = [
        {"analyst_id": "A1","name":"Name 1", "password": "passA1"},
        {"analyst_id": "A2","name":"Name 2", "password": "passA2"},
        {"analyst_id": "A3","name":"Name 3", "password": "passA3"},
    ]


    for item in data:
        analyst_id = item["analyst_id"]
        password = item["password"]
        name = item["name"]
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        cur.execute("INSERT OR IGNORE INTO users (analyst_id, name, password) VALUES (?,?,?)", (analyst_id, name, hashed))
    
    conn.commit()
    conn.close()


init_db()