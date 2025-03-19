from app.db.database import get_db_connection
import bcrypt


def hash_password(password: str) -> str:
    """
    Hashes a given password using bcrypt to securely store it.

    Args:
        password (str): The plaintext password to hash.

    Returns:
        str: The hashed password as a string.
    """
    salt = bcrypt.gensalt()  # Generate a salt for hashing
    hashed = bcrypt.hashpw(password.encode(), salt)  # Hash the password with the salt
    return hashed.decode()  # Return the hashed password as a string

def add_user(username, password, first_name, last_name, role, age=None, weight=None, size=None, vo2max=None, power_max=None, hr_max=None, rf_max=None, cadence_max=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    hashed_password = hash_password(password)
    
    cursor.execute("""
        INSERT INTO user (username, password, first_name, last_name, role, age, weight, size, vo2max, power_max, hr_max, rf_max, cadence_max)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (username, hashed_password, first_name, last_name, role, age, weight, size, vo2max, power_max, hr_max, rf_max, cadence_max))

    conn.commit()
    conn.close()

def get_user_by_id(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM user WHERE id = ?", (user_id,))
    user = cursor.fetchone()

    conn.close()
    return user

def get_user_by_username(user_username):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM user WHERE username = ?", (user_username,))
    user = cursor.fetchone()

    conn.close()
    return user

def get_all_users():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM user")
    users = cursor.fetchall()

    conn.close()
    return users

def update_user(user_id, username=None, password=None, first_name=None, last_name=None, role=None, age=None, weight=None, size=None, vo2max=None, power_max=None, hr_max=None, rf_max=None, cadence_max=None):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Construire dynamiquement la requête de mise à jour
    fields = []
    values = []

    if username:
        fields.append("username = ?")
        values.append(username)
    if password:
        fields.append("password = ?")
        values.append(password)
    if first_name:
        fields.append("first_name = ?")
        values.append(first_name)
    if last_name:
        fields.append("last_name = ?")
        values.append(last_name)
    if role:
        fields.append("role = ?")
        values.append(role)
    if age:
        fields.append("age = ?")
        values.append(age)
    if weight:
        fields.append("weight = ?")
        values.append(weight)
    if size:
        fields.append("size = ?")
        values.append(size)
    if vo2max:
        fields.append("vo2max = ?")
        values.append(vo2max)
    if power_max:
        fields.append("power_max = ?")
        values.append(power_max)
    if hr_max:
        fields.append("hr_max = ?")
        values.append(hr_max)
    if rf_max:
        fields.append("rf_max = ?")
        values.append(rf_max)
    if cadence_max:
        fields.append("cadence_max = ?")
        values.append(cadence_max)

    if fields:
        query = f"UPDATE user SET {', '.join(fields)} WHERE id = ?"
        values.append(user_id)

        cursor.execute(query, values)
        conn.commit()

    conn.close()

def delete_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM user WHERE id = ?", (user_id,))
    conn.commit()

    conn.close()