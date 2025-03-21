from db.database import get_db_connection
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
    """
    Adds a new user to the database.

    Args:
        username (str): Unique username of the user.
        password (str): Plaintext password (will be hashed before storing).
        first_name (str): User's first name.
        last_name (str): User's last name.
        role (str): User's role ('athlete' or 'coach').
        age (int, optional): User's age.
        weight (float, optional): User's weight in kg.
        size (float, optional): User's height in cm.
        vo2max (float, optional): User's maximum oxygen uptake.
        power_max (float, optional): User's maximum power output.
        hr_max (float, optional): User's maximum heart rate.
        rf_max (float, optional): User's respiratory frequency max.
        cadence_max (float, optional): User's maximum cadence.

    Returns:
        None
    """    
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
    """
    Retrieves a user from the database by their unique ID.

    Args:
        user_id (int): The ID of the user.

    Returns:
        sqlite3.Row: A row containing the user's data or None if not found.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM user WHERE id = ?", (user_id,))
    user = cursor.fetchone()

    conn.close()
    return user

def get_user_by_username(user_username):
    """
    Retrieves a user from the database by their unique username.

    Args:
        user_username (str): The username of the user.

    Returns:
        sqlite3.Row: A row containing the user's data or None if not found.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM user WHERE username = ?", (user_username,))
    user = cursor.fetchone()

    conn.close()
    return user

def get_all_users():
    """
    Retrieves all users from the database.

    Returns:
        list: A list of all users in the database.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM user")
    users = cursor.fetchall()

    conn.close()
    print(users)
    return users

def update_user(user_id, username=None, password=None, first_name=None, last_name=None, role=None, age=None, weight=None, size=None, vo2max=None, power_max=None, hr_max=None, rf_max=None, cadence_max=None):
    """
    Updates user information dynamically in the database.

    Args:
        user_id (int): The ID of the user to update.
        username (str, optional): Updated username.
        password (str, optional): Updated password (will be hashed before storing).
        first_name (str, optional): Updated first name.
        last_name (str, optional): Updated last name.
        role (str, optional): Updated role ('athlete' or 'coach').
        age (int, optional): Updated age.
        weight (float, optional): Updated weight.
        size (float, optional): Updated height.
        vo2max (float, optional): Updated VO2 max.
        power_max (float, optional): Updated power max.
        hr_max (float, optional): Updated heart rate max.
        rf_max (float, optional): Updated respiratory frequency max.
        cadence_max (float, optional): Updated cadence max.

    Returns:
        None
    """    
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
        hashed_password = hash_password(password)
        values.append(hashed_password)
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
    """
    Deletes a user from the database by their unique ID.

    Args:
        user_id (int): The ID of the user to delete.

    Returns:
        None
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM user WHERE id = ?", (user_id,))
    conn.commit()

    conn.close()


