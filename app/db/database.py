import sqlite3

DB_NAME = "cycletrack.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # Permet d'accéder aux colonnes par leur nom
    return conn

def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        role   TEXT CHECK (role IN ('athlete', 'coach')) NOT NULL,
        age INTEGER CHECK (age > 0) DEFAULT NULL,
        weight REAL CHECK (weight > 0) DEFAULT NULL,
        size REAL CHECK (size > 0) DEFAULT NULL,
        power_max REAL CHECK (power_max > 0) DEFAULT NULL,
        vo2max REAL CHECK (vo2max > 0) DEFAULT NULL,
        hr_max REAL CHECK (hr_max > 0) DEFAULT NULL,
        rf_max REAL CHECK (rf_max > 0) DEFAULT NULL,
        cadence_max REAL CHECK (cadence_max > 0) DEFAULT NULL
    );

    CREATE TABLE IF NOT EXISTS performance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        date TEXT DEFAULT CURRENT_TIMESTAMP,
        power_max REAL CHECK (power_max > 0),
        vo2_max REAL CHECK (vo2_max > 0),
        hr_max REAL CHECK (hr_max > 0),
        rf_max REAL CHECK (rf_max > 0),
        cadence_max REAL CHECK (cadence_max > 0),
        feeling INT CHECK (feeling >= 0 AND feeling <= 10),
        FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
    );
    """)

    conn.commit()
    conn.close()