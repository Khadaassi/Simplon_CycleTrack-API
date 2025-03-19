import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import pytest
import sqlite3
from app.db.database import get_db_connection
from app.db.CRUD.performance import add_performance, get_performance_by_id, get_all_performances, update_performance, delete_performance

@pytest.fixture
def setup_database():
    """Crée une base de test et nettoie après chaque test."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.executescript("""
    DROP TABLE IF EXISTS user;
    DROP TABLE IF EXISTS performance;

    CREATE TABLE user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        role TEXT CHECK (role IN ('athlete', 'coach')) NOT NULL,
        age INTEGER CHECK (age > 0),
        weight REAL CHECK (weight > 0),
        size REAL CHECK (size > 0),
        power_max REAL CHECK (power_max > 0),
        vo2max REAL CHECK (vo2max > 0),
        hr_max REAL CHECK (hr_max > 0),
        rf_max REAL CHECK (rf_max > 0),
        cadence_max REAL CHECK (cadence_max > 0)
    );

    CREATE TABLE performance (
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

@pytest.fixture
def add_test_user():
    """Ajoute un utilisateur fictif pour les tests."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO user (username, password, first_name, last_name, role, age, weight, size, power_max, vo2max, hr_max, rf_max, cadence_max)
        VALUES ('test_user', 'password', 'Test', 'User', 'athlete', 25, 70.0, 1.75, 300, 60, 180, 50, 90)
    """)

    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    return user_id

def test_add_performance(setup_database, add_test_user):
    """Teste l'ajout d'une performance."""
    user_id = add_test_user
    add_performance(user_id, 320, 58, 190, 55, 95, 8)

    performance = get_performance_by_id(1)
    
    assert performance is not None
    assert performance[1] == user_id
    assert performance[2] is not None  # Vérifier la date
    assert performance[3] == 320
    assert performance[4] == 58
    assert performance[5] == 190
    assert performance[6] == 55
    assert performance[7] == 95
    assert performance[8] == 8

def test_get_all_performances(setup_database, add_test_user):
    """Teste la récupération de toutes les performances."""
    user_id = add_test_user
    add_performance(user_id, 300, 55, 180, 50, 90, 7)
    add_performance(user_id, 310, 56, 185, 52, 92, 6)

    performances = get_all_performances()
    assert len(performances) == 2

def test_update_performance(setup_database, add_test_user):
    """Teste la mise à jour d'une performance."""
    user_id = add_test_user
    add_performance(user_id, 300, 55, 180, 50, 90, 7)
    
    update_performance(1, power_max=350, feeling=9)
    performance = get_performance_by_id(1)

    assert performance[3] == 350  # power_max mis à jour
    assert performance[8] == 9  # feeling mis à jour

def test_delete_performance(setup_database, add_test_user):
    """Teste la suppression d'une performance."""
    user_id = add_test_user
    add_performance(user_id, 300, 55, 180, 50, 90, 7)

    delete_performance(1)
    performance = get_performance_by_id(1)
    
    assert performance is None
