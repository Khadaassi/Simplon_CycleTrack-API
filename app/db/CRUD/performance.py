import sqlite3
from app.db.database import get_db_connection

def add_performance(user_id, power_max, vo2_max, hr_max, rf_max, cadence_max, feeling=None):
    """Ajoute une performance pour un utilisateur donné."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO performance (user_id, power_max, vo2_max, hr_max, rf_max, cadence_max, feeling)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (user_id, power_max, vo2_max, hr_max, rf_max, cadence_max, feeling))

    conn.commit()
    conn.close()

def get_performance_by_id(performance_id):
    """Récupère une performance par son ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    print(f"perfomance_id : {performance_id}")
    cursor.execute("SELECT * FROM performance WHERE id = ?", (performance_id,))
    performance = cursor.fetchone()
    print(f"perfomance : {performance}")
    conn.close()
    return performance

def get_all_performances():
    """Récupère toutes les performances."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM performance")
    performances = cursor.fetchall()

    conn.close()
    return performances

def update_performance(performance_id, power_max=None, vo2_max=None, hr_max=None, rf_max=None, cadence_max=None, feeling=None):
    """Met à jour une performance existante."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    update_fields = []
    params = []

    if power_max is not None:
        update_fields.append("power_max = ?")
        params.append(power_max)
    if vo2_max is not None:
        update_fields.append("vo2_max = ?")
        params.append(vo2_max)
    if hr_max is not None:
        update_fields.append("hr_max = ?")
        params.append(hr_max)
    if rf_max is not None:
        update_fields.append("rf_max = ?")
        params.append(rf_max)
    if cadence_max is not None:
        update_fields.append("cadence_max = ?")
        params.append(cadence_max)
    if feeling is not None:
        update_fields.append("feeling = ?")
        params.append(feeling)

    params.append(performance_id)
    
    cursor.execute(f"""
        UPDATE performance
        SET {', '.join(update_fields)}
        WHERE id = ?
    """, params)

    conn.commit()
    conn.close()

def delete_performance(performance_id):
    """Supprime une performance par son ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM performance WHERE id = ?", (performance_id,))
    
    conn.commit()
    conn.close()
