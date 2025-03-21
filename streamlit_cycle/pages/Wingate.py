import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

st.set_page_config(page_title="Analyse des données Wingate", layout="wide")

st.title("Analyse des performances cyclistes - Test Wingate")

# Fonction pour charger les données
@st.cache_data
def load_data(subject_number):
    try:
        filename = f"app/data_int/sbj_{subject_number}_Wingate.csv"
        data = pd.read_csv(filename)
        return data
    except Exception as e:
        st.error(f"Erreur lors du chargement du fichier {filename}: {e}")
        return None

# Charger les fichiers CSV automatiquement
subjects_data = {}
subject_names = []

for i in range(1, 8):  # Charger les fichiers sbj_1_Wingate.csv à sbj_7_Wingate.csv
    data = load_data(i)
    if data is not None:
        subjects_data[str(i)] = data
        subject_names.append(f"Sujet {i}")

# Vérifier si les données ont été chargées
if not subjects_data:
    st.warning("Aucune donnée disponible. Veuillez vérifier les fichiers CSV.")

colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2']

if subjects_data:
    measures = ["Power", "Oxygen", "Cadence", "HR", "RF"]
    
    st.subheader("Sélectionner les sujets à afficher")
    selected_subjects = st.multiselect("Choisir les joueurs", subject_names, default=subject_names)

    # Option pour filtrer les données
    smoothing = st.slider("Lissage (fenêtre mobile)", 1, 10, 1)
    
    # Afficher les 5 graphiques pour chaque mesure
    for measure in measures:
        st.subheader(f"Mesure: {measure}")
        fig, ax = plt.figure(figsize=(10, 6)), plt.gca()
        
        for i, (subject_number, data) in enumerate(subjects_data.items()):
            if f"Sujet {subject_number}" in selected_subjects:
                if measure in data.columns:
                    y_values = data[measure].rolling(window=smoothing, min_periods=1).mean()
                    ax.plot(data['time'], y_values, label=f"Sujet {subject_number}", color=colors[i % len(colors)], linewidth=2)
        
        ax.set_xlabel('Temps (secondes)')
        ax.set_ylabel(measure)
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.legend()

        units = {
            "Power": "Watts", 
            "Oxygen": "mL/min", 
            "Cadence": "RPM", 
            "HR": "BPM", 
            "RF": "Resp/min"
        }
        
        if measure in units:
            ax.set_ylabel(f"{measure} ({units[measure]})")

        st.pyplot(fig)

        st.subheader(f"Statistiques pour {measure}")
        stats_cols = st.columns(3)
        
        with stats_cols[0]:
            st.write("Valeurs maximales:")
            max_values = {}
            for subject_number, data in subjects_data.items():
                if f"Sujet {subject_number}" in selected_subjects and measure in data.columns:
                    max_values[f"Sujet {subject_number}"] = data[measure].max()
            st.write(pd.Series(max_values))
        
        with stats_cols[1]:
            st.write("Valeurs moyennes:")
            mean_values = {}
            for subject_number, data in subjects_data.items():
                if f"Sujet {subject_number}" in selected_subjects and measure in data.columns:
                    mean_values[f"Sujet {subject_number}"] = data[measure].mean()
            st.write(pd.Series(mean_values))
        
        with stats_cols[2]:
            st.write("Écart-type:")
            std_values = {}
            for subject_number, data in subjects_data.items():
                if f"Sujet {subject_number}" in selected_subjects and measure in data.columns:
                    std_values[f"Sujet {subject_number}"] = data[measure].std()
            st.write(pd.Series(std_values))
        
        st.markdown("---")

    st.subheader("Tableau de données")
    selected_subject = st.selectbox("Choisir un sujet pour voir ses données", list(subjects_data.keys()))
    if selected_subject:
        st.dataframe(subjects_data[selected_subject])
