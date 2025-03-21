from db.database import create_tables
from db.CRUD.user import add_user, get_user_by_username
from db.CRUD.performance import add_performance
import os
import json
import pandas as pd

def init_create_tables():
    """
    Initialize and create database tables.
    
    This function calls the create_tables() method to set up the database schema.
    It prints a success message if tables are created successfully,
    or an error message if an exception occurs.
    """
    try:
        create_tables()
        print("Tables créés avec succés")
    except Exception as e:
        print(f"Pb lors de la création des tables :{e}")

def create_coach():
    """
    Create a default coach user in the database.
    
    This function adds a coach user with predefined credentials:
    - Username: supercoach
    - Password: password
    - Name: coach super
    - Role: coach
    
    It prints a success message if the coach is added successfully,
    or an error message if an exception occurs.
    """
    try:
        add_user(username = "supercoach", password = "password", first_name="coach", last_name="super", role="coach")
        print("Coach ajouté avec succès")
    except Exception as e:
        print(f"Pb lors de la création du super coach :{e}")

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
DATA_FOLDER = os.path.join(BASE_DIR, "data_int")

json_files = [f for f in os.listdir(DATA_FOLDER) if f.endswith(".json")]

def create_from_csv():
    """
    Import user data and performance metrics from JSON and CSV files.
    
    This function:
    1. Processes all JSON files in the data_int directory
    2. Creates user accounts based on JSON data
    3. Reads associated CSV files to extract performance metrics
    4. Creates performance records for each user based on CSV data
    
    The function expects JSON files to contain user metadata and references to CSV files
    that contain performance time series data. It extracts maximum values for various 
    performance metrics (power, oxygen, heart rate, respiratory frequency, cadence)
    and stores them in the database.
    
    CSV files must contain columns: Power, Oxygen, Cadence, HR, RF
    """
    for json_file in json_files:
        json_path = os.path.join(DATA_FOLDER, json_file)
        with open(json_path, "r", encoding="utf-8") as file:
            user_data = json.load(file)
        username = user_data["name"]  # Ex: "sbj_6"
        password = "default_password"  # Un mot de passe temporaire
        first_name = f"User {username}"  # Exemple : "User sbj_6"
        last_name = "Csv"
        role = "athlete"
        power_max = user_data.get("power.max")
        hr_max = user_data.get("hr.max")
        vo2max = user_data.get("vo2.max")
        rf_max = user_data.get("rf.max")
        cadence_max = user_data.get("cadence.max")
        add_user(username, password, first_name, last_name, role, vo2max=vo2max, power_max=power_max, hr_max=hr_max, rf_max=rf_max, cadence_max=cadence_max)
        print(f"Utilisateur {username} ajouté avec succès.")
        csv_files = user_data.get("csv_trial_1", []) + user_data.get("csv_trial_2", [])
        csv_files = list(set(csv_files))  # Suppression des doublons
        for csv_file in csv_files:
            csv_path = os.path.join(DATA_FOLDER, csv_file)

            # Vérification si le fichier CSV existe
            if not os.path.exists(csv_path):
                print(f"⚠️ Fichier {csv_file} introuvable, ignoré.")
                continue

            # Lecture du fichier CSV
            df = pd.read_csv(csv_path)

            # Vérification des colonnes nécessaires
            if not {"Power", "Oxygen", "Cadence", "HR", "RF"}.issubset(df.columns):
                print(f"⚠️ Fichier {csv_file} a un format incorrect, ignoré.")
                continue

            # Extraction des valeurs maximales
            v_max = []
            v_max.append(df["Power"].max())
            v_max.append(df["Oxygen"].max())
            v_max.append(df["Cadence"].max())
            v_max.append(df["HR"].max())
            v_max.append(df["RF"].max())
            for item in v_max:
                if isinstance(item, bytes):
                    item = 0
            print(f"Valeurs maximales pour {username} depuis {csv_file}: {v_max} (Types: {[type(v) for v in v_max]})")
            user_id = get_user_by_username(username)["id"]
            # Ajout de la performance dans la base de données
            add_performance(user_id=user_id, power_max=v_max[0], vo2_max=v_max[1], hr_max=v_max[3], rf_max=v_max[4], cadence_max=v_max[2])

            print(f"✅ Performance ajoutée pour {username} depuis {csv_file}.")


if __name__ == '__main__':
    init_create_tables()
    create_coach()
    create_from_csv()