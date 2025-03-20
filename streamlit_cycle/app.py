import streamlit as st
import requests

API_URL = "http://0.0.0.0:8000"

# Page de connexion
def login():
    st.title("Connexion 🔐")
    
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")
    
    if st.button("Se connecter"):
        if username and password:
            response = requests.post(f"{API_URL}/login", json={"username": username, "password": password})
            print(f"{API_URL}/login")
            print({"username": username, "password": password})
            if response.status_code == 200:
                token = response.json()["access_token"]
                st.session_state["token"] = token
                st.success("Connexion réussie !")
                st.experimental_rerun() 
            else:
                st.error("Échec de la connexion, vérifiez vos identifiants")

# Page d'accueil après connexion
def home():
    st.title("Bienvenue sur CycleTrack 🚴‍♂️")
    
    headers = {"Authorization": f"Bearer {st.session_state['token']}"}
    response = requests.get(f"{API_URL}/users/self", headers=headers)
    
    if response.status_code == 200:
        user = response.json()
        st.write(f"👋 Bonjour, {user['first_name']} {user['last_name']} !")
        st.write(f"**Rôle :** {user['role']}")
    else:
        st.error("Erreur lors de la récupération des informations utilisateur.")
    
    if st.button("Se déconnecter"):
        st.session_state.clear()
        st.experimental_rerun()

# Gestion des pages
if "token" not in st.session_state:
    login()
else:
    home()
