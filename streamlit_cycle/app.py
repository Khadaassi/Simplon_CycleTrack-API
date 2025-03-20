import streamlit as st
import requests

API_URL = "http://0.0.0.0:8000"

st.markdown(
    """
    <style>
        .main-header {
            text-align: center;
            font-size: 2.5em;
            color: #556B2F;
            font-weight: bold;
            margin-bottom: 30px;
            font-family: Arial, sans-serif;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<div class='main-header'>CycleTrack</div>", unsafe_allow_html=True)

# Page de connexion
def login():
    st.title("Connexion 🔐")
    
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password", key="password_input")
    
    if st.button("Se connecter"):
        if username and password:
            response = requests.post(f"{API_URL}/login", json={"username": username, "password": password})
            
            if response.status_code == 200:
                token = response.json()["access_token"]
                st.session_state["token"] = token
                
                # Récupérer les informations de l'utilisateur
                headers = {"Authorization": f"Bearer {token}"}
                user_response = requests.get(f"{API_URL}/users/self", headers=headers)

                if user_response.status_code == 200:
                    user = user_response.json()
                    st.session_state["user"] = user  # Stocker l'utilisateur en session

                    st.success(f"Connexion réussie ! Bienvenue {user['first_name']} {user['last_name']}")
                    st.rerun()  # Redémarrer l'interface
                else:
                    st.error("Erreur lors de la récupération des informations utilisateur.")
            else:
                st.error("Échec de la connexion, vérifiez vos identifiants")

# Redirige l'utilisateur vers la bonne page en fonction de son rôle
def redirect_user():
    user = st.session_state.get("user")

    if not user:
        st.error("Impossible de récupérer les informations utilisateur.")
        return

    if user["role"].lower() == "coach":
        st.switch_page("pages/Coach.py")
    else:
        st.switch_page("pages/Member.py")

# Page d'accueil après connexion
def home():
    st.title("Bienvenue sur CycleTrack 🚴‍♂️")
    
    if "user" not in st.session_state:
        st.error("Utilisateur non authentifié")
        return

    user = st.session_state["user"]
    st.write(f"👋 Bonjour, {user['first_name']} {user['last_name']} !")
    st.write(f"**Rôle :** {user['role']}")

    # Redirection automatique
    redirect_user()

    if st.button("Se déconnecter"):
        st.session_state.clear()
        st.rerun()

# Gestion des pages
if "token" not in st.session_state:
    login()
else:
    home()


# st.markdown(
#     """
#     <style>
#     .custom-button {
#         display: block;
#         margin: auto;
#         padding: 15px 20px;
#         font-size: 18px;
#         color: black;
#         text-decoration: none;
#         border: 1px solid;
#         border-radius: 5px;
#         cursor: pointer;
#         text-align: center;
#         background-color: transparent;
#     }

#     .custom-button:hover {
#         color: black;
#     }

#     /* Dark mode detection */
#     @media (prefers-color-scheme: dark) {
#         .custom-button {
#             color: white; /* White text by default in dark mode */
#             border-color: white; /* White border in dark mode */
#         }
#         .custom-button:hover {
#             color: white; /* Keep white text on hover in dark mode */
#         }
#     }
#     </style>
#     <a href="http://localhost:8501/Member" class="custom-button">Member</a>
#     """,
#     unsafe_allow_html=True
# )

# # Button to redirect to the quiz page
# st.markdown(
#     """
#     <style>
#     .custom-button {
#         display: block;
#         margin: auto;
#         padding: 15px 20px;
#         font-size: 18px;
#         color: black;
#         text-decoration: none;
#         border: 1px solid;
#         border-radius: 5px;
#         cursor: pointer;
#         text-align: center;
#         background-color: transparent;
#     }

#     .custom-button:hover {
#         color: black;
#     }

#     /* Dark mode detection */
#     @media (prefers-color-scheme: dark) {
#         .custom-button {
#             color: white; /* White text by default in dark mode */
#             border-color: white; /* White border in dark mode */
#         }
#         .custom-button:hover {
#             color: white; /* Keep white text on hover in dark mode */
#         }
#     }
#     </style>
#     <a href="http://localhost:8501/Admin" class="custom-button">Admin</a>
#     """,
#     unsafe_allow_html=True
# )