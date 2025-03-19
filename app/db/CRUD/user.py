from db.database import get_db_connection

def add_user(username, password, first_name, last_name, role, age=None, weight=None, size=None, vo2max=None, power_max=None, hr_max=None, rf_max=None, cadence_max=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO user (username, password, first_name, last_name, role, age, weight, size, vo2max, power_max, hr_max, rf_max, cadence_max)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (username, password, first_name, last_name, role, age, weight, size, vo2max, power_max, hr_max, rf_max, cadence_max))

    conn.commit()
    conn.close()