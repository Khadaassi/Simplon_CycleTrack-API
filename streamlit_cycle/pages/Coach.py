import streamlit as st
import requests
import pandas as pd
import numpy as np

API_URL = "http://0.0.0.0:8000"

# Vérification de l'authentification
if "token" not in st.session_state:
    st.error("Vous devez être connecté pour accéder à cette page.")
    st.stop()

# Récupération des informations de l'utilisateur
headers = {"Authorization": f"Bearer {st.session_state['token']}"}
coach_response = requests.get(f"{API_URL}/users/self", headers=headers)

if coach_response.status_code != 200:
    st.error("Impossible de récupérer les informations utilisateur.")
    st.stop()

st.header("➕ Add a New User")
with st.form("add_user_form"):
    username = st.text_input("Username", placeholder="Enter username")
    password = st.text_input("Password", type="password")
    first_name = st.text_input("First Name", placeholder="Enter first name")
    last_name = st.text_input("Last Name", placeholder="Enter last name")
    role = st.selectbox("Role", ["athlete", "coach"])
    age = st.number_input("Age", min_value=1, step=1)
    weight = st.number_input("Weight (kg)", min_value=1.0, step=0.1)
    size = st.number_input("Size (cm)", min_value=1.0, step=0.1)

    submit_button = st.form_submit_button("Register User")

    if submit_button:
        user_data = {
            "username": username,
            "password": password,
            "first_name": first_name,
            "last_name": last_name,
            "role": role,
            "age": age,
            "weight": weight,
            "size": size,
        }

        response = requests.post(f"{API_URL}/user/register", json=user_data)

        if response.status_code == 201:
            st.success("✅ User registered successfully!")
        else:
            st.error("❌ Error registering user")

# 📌 Affichage de tous les utilisateurs
st.header("📋 All Users")

user_response = requests.get(f"{API_URL}/users/all", headers=headers)

if user_response.status_code == 200:
    users = user_response.json()

    if users:
        print(type(users))
        df = pd.DataFrame.from_dict(users, orient='index')
        print(df)
        df.drop("password", axis=1, inplace=True)

        df = df.rename(columns={
            "id": "ID",
            "username": "Username",
            "first_name": "First Name",
            "last_name": "Last Name",
            "role": "Role",
            "age": "Age",
            "weight": "Weight",
            "size": "Size",
            "vo2max": "VO2 Max",
            "power_max": "Max Power",
            "hr_max": "Max Heart Rate",
            "rf_max": "Max RF",
            "cadence_max": "Max Cadence"
        })

        col_sort = st.selectbox("Sort by:", df.columns)
        st.dataframe(df.sort_values(by=col_sort, ascending=True, na_position="last"), use_container_width=True)
    else:
        st.info("No users found.")

else:
    st.error("Error fetching users.")

# 📌 Sélection d'un utilisateur pour voir ses performances
st.header("📊 User Performances")
user_mapping = dict(zip(df["Username"], df["ID"]))
selected_username = st.selectbox("Select a user:", df["Username"]) if not df.empty else None
selected_user_id = user_mapping[selected_username]
if selected_user_id:
    perf_response = requests.get(f"{API_URL}/perfs/user/{selected_user_id}", headers=headers)

    if perf_response.status_code == 200:
        performances = perf_response.json()

        if performances:
            df_perf = pd.DataFrame.from_dict(performances, orient='index')

            # Sélection de la colonne de tri pour les performances
            col_perf_sort = st.selectbox("Sort performances by:", df_perf.columns)

            # Affichage du tableau trié des performances
            st.dataframe(df_perf.sort_values(by=col_perf_sort, ascending=True), use_container_width=True)


            # Convertir les colonnes en nombres et gérer les erreurs
            df_perf["power_max"] = pd.to_numeric(df_perf["power_max"], errors="coerce")
            df_perf["vo2_max"] = pd.to_numeric(df_perf["vo2_max"], errors="coerce")
            df_perf["hr_max"] = pd.to_numeric(df_perf["hr_max"], errors="coerce")
            df_perf["rf_max"] = pd.to_numeric(df_perf["rf_max"], errors="coerce")
            df_perf["cadence_max"] = pd.to_numeric(df_perf["cadence_max"], errors="coerce")

            # Calcul des statistiques en ignorant les NaN
            avg_power_max = df_perf["power_max"].mean(skipna=True)
            avg_vo2_max = df_perf["vo2_max"].mean(skipna=True)
            avg_hr_max = df_perf["hr_max"].mean(skipna=True)
            avg_rf_max = df_perf["rf_max"].mean(skipna=True)
            avg_cadence_max = df_perf["cadence_max"].mean(skipna=True)
            best_performance = df_perf["power_max"].max(skipna=True)
            last_performance_date = df_perf["date"].max() 
            total_performances = len(df_perf)
            
            # Affichage des statistiques
            st.write("### 📊 User Statistics")
            st.metric("Total Performances", total_performances)
            st.metric("Average Power Max", f"{avg_power_max:.2f} W")
            st.metric("Average VO2 Max", f"{avg_vo2_max:.2f} ml/kg/min")
            st.metric("Average HR Max", f"{avg_hr_max:.0f} bpm")
            st.metric("Average RF Max", f"{avg_rf_max:.0f}")
            st.metric("Average Cadence Max", f"{avg_cadence_max:.0f} rpm")
            st.metric("Best Performance (Power Max)", f"{best_performance:.2f} W")
            st.metric("Last Performance Date", last_performance_date)

        else:
            st.info("No performances recorded for this user.")
    else:
        st.error("Error fetching user performances.")
