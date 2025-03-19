from app.db.database import create_tables
from app.db.CRUD.user import add_user

def init_create_tables():
    try:
        create_tables()
        print("Tables créés avec succés")
    except Exception as e:
        print(f"Pb lors de la création des tables :{e}")

def create_coach():
    try:
        add_user(username = "supercoach", password = "password", first_name="coach", last_name="super", role="coach")
        print("Coach ajouté avec succès")
    except Exception as e:
        print(f"Pb lors de la création du super coach :{e}")

if __name__ == '__main__':
    init_create_tables()
    create_coach()