import sqlite3
from db.database import get_db_connection
from core.update_stats import update_user_stats_new_perf

def add_performance(user_id, power_max, vo2_max, hr_max, rf_max, cadence_max, feeling=None):
    """
    Adds a new performance entry for a specific user.

    Args:
        user_id (int): The ID of the user.
        power_max (float): Maximum power recorded.
        vo2_max (float): VO2 max value.
        hr_max (float): Maximum heart rate.
        rf_max (float): Maximum respiratory frequency.
        cadence_max (float): Maximum cadence.
        feeling (int, optional): Subjective feeling rating (0-10).

    Returns:
        None
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO performance (user_id, power_max, vo2_max, hr_max, rf_max, cadence_max, feeling)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (user_id, power_max, vo2_max, hr_max, rf_max, cadence_max, feeling))
    perf_id = cursor.lastrowid
    conn.commit()
    conn.close()
    update_user_stats_new_perf(user_id, perf_id)

def get_performance_by_id(performance_id):
    """
    Retrieves a performance entry by its unique ID.

    Args:
        performance_id (int): The ID of the performance.

    Returns:
        sqlite3.Row: The performance record, or None if not found.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    print(f"perfomance_id : {performance_id}")
    cursor.execute("SELECT * FROM performance WHERE id = ?", (performance_id,))
    performance = cursor.fetchone()
    print(f"perfomance : {performance}")
    conn.close()
    return performance

def get_all_performances():
    """
    Retrieves all performance records from the database.

    Returns:
        list: A list of all performance records.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM performance")
    performances = cursor.fetchall()

    conn.close()
    return performances

def update_performance(performance_id, power_max=None, vo2_max=None, hr_max=None, rf_max=None, cadence_max=None, feeling=None):
    """
    Updates an existing performance record with new values.

    Args:
        performance_id (int): The ID of the performance to update.
        power_max (float, optional): Updated maximum power.
        vo2_max (float, optional): Updated VO2 max value.
        hr_max (float, optional): Updated maximum heart rate.
        rf_max (float, optional): Updated maximum respiratory frequency.
        cadence_max (float, optional): Updated maximum cadence.
        feeling (int, optional): Updated subjective feeling rating (0-10).

    Returns:
        None
    """
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
    # Retrieve the user ID from the performance record
    user_id = get_performance_by_id(performance_id)["user_id"]
    # Update user's overall stats based on the new performance data
    update_user_stats_new_perf(user_id, performance_id)

def delete_performance(performance_id):
    """
    Deletes a performance record by its unique ID.

    Args:
        performance_id (int): The ID of the performance to delete.

    Returns:
        None
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM performance WHERE id = ?", (performance_id,))
    
    conn.commit()
    conn.close()

def get_performances_by_user(user_id):
    """
    Retrieves all performances associated with a specific user.

    Args:
        user_id (int): The ID of the user.

    Returns:
        list: A list of performance records linked to the user.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM performance WHERE user_id = ?", (user_id,))
    performances = cursor.fetchall()
    conn.close()
    return performances
