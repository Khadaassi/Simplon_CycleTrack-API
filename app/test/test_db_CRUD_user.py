import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

import pytest
import sqlite3
from db.database import get_db_connection
from db.CRUD.user import add_user, get_user_by_id, get_all_users, update_user, delete_user

### 🔹 Configuration de la base de test (exécutée avant chaque test)
@pytest.fixture
def setup_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Réinitialisation des tables (pour ne pas interférer avec d'autres tests)
    cursor.executescript("""
    DROP TABLE IF EXISTS user;

    CREATE TABLE user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        role TEXT CHECK (role IN ('athlete', 'coach')) NOT NULL,
        age INTEGER,
        weight REAL,
        size REAL,
        vo2max REAL,
        power_max REAL,
        hr_max REAL,
        rf_max REAL,
        cadence_max REAL
    );
    """)

    conn.commit()
    conn.close()

### 🔹 Test de l'ajout d'un utilisateur
def test_add_user(setup_db):
    add_user(username="testuser", password="testpass", first_name="John", last_name="Doe", role="athlete")
    user = get_user_by_id(1)

    assert user is not None
    assert user[1] == "testuser"  # Vérifie le username
    assert user[5] == "athlete"   # Vérifie le rôle

### 🔹 Test de la récupération d'un utilisateur
def test_get_user_by_id(setup_db):
    add_user(username="testuser2", password="pass123", first_name="Alice", last_name="Smith", role="coach")
    user = get_user_by_id(1)

    assert user is not None
    assert user[1] == "testuser2"
    assert user[5] == "coach"

### 🔹 Test de la récupération de tous les utilisateurs
def test_get_all_users(setup_db):
    add_user(username="user1", password="pass1", first_name="A", last_name="B", role="athlete")
    add_user(username="user2", password="pass2", first_name="C", last_name="D", role="coach")

    users = get_all_users()
    assert len(users) == 2  # Vérifie qu'on a bien 2 utilisateurs

### 🔹 Test de la mise à jour d'un utilisateur
def test_update_user(setup_db):
    add_user(username="updateuser", password="pass", first_name="Mike", last_name="Tyson", role="athlete")

    update_user(1, weight=80.5, vo2max=55.2)
    user = get_user_by_id(1)

    assert user[7] == 80.5  # Vérifie le poids
    assert user[9] == 55.2  # Vérifie le VO2max

### 🔹 Test de la suppression d'un utilisateur
def test_delete_user(setup_db):
    add_user(username="deleteuser", password="pass", first_name="Bob", last_name="Marley", role="coach")

    delete_user(1)
    user = get_user_by_id(1)

    assert user is None  # L'utilisateur doit être supprimé
