import streamlit as st
import requests
import pandas as pd

API_URL = "http://0.0.0.0:8000"

# Vérification de l'authentification
if "token" not in st.session_state:
    st.error("Vous devez être connecté pour accéder à cette page.")
    st.stop()

# Récupération des informations de l'utilisateur
headers = {"Authorization": f"Bearer {st.session_state['token']}"}
user_response = requests.get(f"{API_URL}/users/self", headers=headers)

if user_response.status_code != 200:
    st.error("Impossible de récupérer les informations utilisateur.")
    st.stop()

user = user_response.json()

st.title(f"👤 Profil de {user['first_name']} {user['last_name']}")

# Affichage des informations du membre
st.subheader("📋 Informations personnelles")
st.write(f"**Nom d'utilisateur :** {user['username']}")
st.write(f"**Rôle :** {user['role']}")
st.write(f"**Âge :** {user['age'] if user['age'] else 'Non renseigné'}")
st.write(f"**Poids :** {user['weight']} kg" if user['weight'] else "**Poids :** Non renseigné")
st.write(f"**Taille :** {user['size']} cm" if user['size'] else "**Taille :** Non renseigné")
st.write(f"**Puissance max :** {user['power_max']} " if user['power_max'] else "**Puissance max :** Non renseigné")
st.write(f"**hr max :** {user['hr_max']} " if user['hr_max'] else "**hr max :** Non renseigné")
st.write(f"**rf max :** {user['rf_max']} " if user['rf_max'] else "**rf max :** Non renseigné")
st.write(f"**VO2 max :** {user['vo2max']} " if user['vo2max'] else "**VO2 max :** Non renseigné")
st.write(f"**cadence max :** {user['cadence_max']} " if user['cadence_max'] else "**cadence max :** Non renseigné")

# Récupération des performances du membre
performance_response = requests.get(f"{API_URL}/perfs/user/{user['id']}", headers=headers)

if performance_response.status_code == 200:
    performances = performance_response.json()
    if performances:
        st.subheader("📊 Performances")
        
        # Transformation des données en DataFrame
        df = pd.DataFrame.from_dict(performances, orient="index")
        print(df.dtypes)
        df = df.rename(columns={"id": "ID", "power_max": "Puissance Max", "vo2_max": "VO2 Max",
                                "hr_max": "Fréquence Cardiaque Max", "rf_max": "RF Max",
                                "cadence_max": "Cadence Max", "feeling": "Feeling", "date": "Date"})
        
        # Sélection de la colonne pour le tri
        col_sort = st.selectbox("Trier par :", df.columns)

        # Affichage du tableau avec tri dynamique
        st.dataframe(df.sort_values(by=col_sort, ascending=True), use_container_width=True)

    else:
        st.info("Aucune performance enregistrée pour l'instant.")
else:
    st.error("Erreur lors de la récupération des performances.")

# Formulaire pour ajouter une nouvelle performance
st.subheader("➕ Ajouter une nouvelle performance")

with st.form(key="new_performance_form"):
    power_max = st.number_input("Puissance Max (W)", min_value=1.0, step=1.0)
    vo2_max = st.number_input("VO2 Max", min_value=1.0, step=1.0)
    hr_max = st.number_input("Fréquence Cardiaque Max", min_value=1.0, step=1.0)
    rf_max = st.number_input("RF Max", min_value=1.0, step=1.0)
    cadence_max = st.number_input("Cadence Max", min_value=1.0, step=1.0)
    feeling = st.slider("Feeling (0-10)", min_value=0, max_value=10, step=1)
    
    submit_button = st.form_submit_button(label="Ajouter")

if submit_button:
    new_performance = {
        "user_id": user["id"],
        "power_max": power_max,
        "vo2_max": vo2_max,
        "hr_max": hr_max,
        "rf_max": rf_max,
        "cadence_max": cadence_max,
        "feeling": feeling
    }
    
    response = requests.post(f"{API_URL}/perfs/create", json=new_performance, headers=headers)
    
    if response.status_code == 201:
        st.success("Performance ajoutée avec succès !")
        st.rerun()  # Recharge la page pour afficher la nouvelle performance
    else:
        st.error(f"Erreur : {response.json()['detail']}")

# Bouton de déconnexion
if st.button("Se déconnecter"):
    st.session_state.clear()
    st.rerun()
