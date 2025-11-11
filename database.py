import sqlite3, os

DB_PATH = "data/events.db"

def init_db():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            category TEXT,
            type TEXT,
            address TEXT,
            lat REAL,
            lng REAL,
            time TEXT,
            description TEXT,
            source TEXT,
            link TEXT UNIQUE
        )
    """)
    conn.commit()
    conn.close()

def get_all_events(city=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if city:
        c.execute("SELECT * FROM events WHERE LOWER(address) LIKE ? ORDER BY time DESC", ('%' + city.lower() + '%',))
    else:
        c.execute("SELECT * FROM events ORDER BY time DESC")
    rows = c.fetchall()
    conn.close()
    keys = ["id","name","category","type","address","lat","lng","time","description","source","link"]
    return [dict(zip(keys, r)) for r in rows]

def add_event(event):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute("""
            INSERT INTO events (name, category, type, address, lat, lng, time, description, source, link)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            event["name"],
            event["category"],
            event["type"],
            event["address"],
            event["lat"],
            event["lng"],
            event["time"],
            event.get("description", ""),
            event.get("source", ""),
            event.get("link", "")
        ))
        conn.commit()
    except sqlite3.IntegrityError:
        # Đã có sự kiện trùng link → bỏ qua
        pass
    conn.close()
