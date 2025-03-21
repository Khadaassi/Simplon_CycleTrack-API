import sqlite3

DB_NAME = "cycletrack.db"

def get_db_connection():
    """
    Establishes and returns a connection to the SQLite database.

    Returns:
        sqlite3.Connection: A connection object to the database.
    """
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # Permet d'accéder aux colonnes par leur nom
    return conn

def create_tables():
    """
    Creates the necessary tables for the CycleTrack application if they do not already exist.

    Tables:
        - user: Stores user details (athletes and coaches).
        - performance: Stores user performance data.

    The `user` table:
        - Contains user information such as name, role, and physiological attributes.
        - Enforces constraints to ensure valid data (e.g., positive values for age, weight, and performance metrics).
    
    The `performance` table:
        - Stores recorded performance data linked to a user.
        - Enforces constraints on recorded values (e.g., power_max, vo2_max must be positive).
        - Includes a `feeling` score (0-10) to capture subjective performance perception.

    Relationships:
        - The `performance` table has a foreign key (`user_id`) referencing `user(id)`.
        - If a user is deleted, all their performances are also deleted (`ON DELETE CASCADE`).

    This function ensures data integrity and sets up the necessary schema for the application.

    Returns:
        None
    """
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
        feeling INT CHECK (feeling >= 0 AND feeling <= 10) DEFAULT NULL,
        FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
    );
    """)

    conn.commit()
    conn.close()