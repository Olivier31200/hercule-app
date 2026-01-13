import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# 1. CONFIGURATION
st.set_page_config(page_title="Hercule App - Cotations", layout="centered")

# 2. DONNÉES DE BASE
prix_actuel_g = 2.46
prix_veille_g = 2.40
argent_pur_50fr = 27.0   # 50 Francs = 27g d'argent pur
argent_pur_10fr = 22.5   # 10 Francs = 22.5g d'argent pur

# 3. FONCTION STICKER (Prix en blanc + Badge tendance)
def afficher_header_prix(actuel, veille):
    variation = ((actuel - veille) / veille) * 100
    couleur_badge = "#28a745" if variation >= 0 else "#dc3545"
    signe = "+" if variation > 0 else ""
    
    html = f"""
    <div style="display: flex; align-items: center; justify-content: center; background-color: #1e1e1e; padding: 20px; border-radius: 10px; margin-bottom: 25px; border: 1px solid #333;">
        <span style="font-size: 32px; font-weight: bold; color: white; margin-right: 15px;">
            {actuel:.2f}€/g
        </span>
        <span style="background-color: {couleur_badge}; color: white; padding: 4px 12px; border-radius: 20px; font-size: 18px; font-weight: bold;">
            {signe}{variation:.2f}%
        </span>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

# --- INTERFACE ---

st.title("💰 Cotations & Calculateur Hercule")

# Affichage du bandeau de prix
afficher_header_prix(prix_actuel_g, prix_veille_g)

# 4. GRAPHIQUE DU COURS DE L'ARGENT
st.write("### 📈 Évolution du cours (7 derniers jours)")
# Simulation de données pour le graphique
dates = [(datetime.now() - timedelta(days=i)).strftime("%d/%m") for i in range(7)][::-1]
cours_simules = [2.35, 2.38, 2.37, 2.41, 2.39, 2.40, 2.46]
df_graph = pd.DataFrame({"Prix €/g": cours_simules}, index=dates)

st.line_chart(df_graph)

# 5. TABLEAU RÉCAPITULATIF (SANS INDEX)
st.write("### 📋 Grille de rachat")
valeur_50fr = argent_pur_50fr * prix_actuel_g
valeur_10fr = argent_pur_10fr * prix_actuel_g

data = {
    "Pièce Hercule": ["50 Francs (27g pur)", "10 Francs (22.5g pur)"],
    "Valeur Spot": [f"{valeur_50fr:.2f} €", f"{valeur_10fr:.2f} €"],
    "-10% (Normal)": [f"{valeur_50fr*0.9:.2f} €", f"{valeur_10fr*0.9:.2f} €"],
    "🚨 -20% (Urgence)": [f"{valeur_50fr*0.8:.2f} €", f"{valeur_10fr*0.8:.2f} €"]
}

df = pd.DataFrame(data)
st.dataframe(df, hide_index=True, use_container_width=True)

st.divider()

# 6. LES CALCULATEURS
st.write("### 🧮 Calculateurs de rachat (-10%)")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Pièces de 50 Frs**")
    nb_50fr = st.number_input("Quantité 50 Frs :", min_value=0, step=1, value=1, key="calc_50")
    total_50 = nb_50fr * (valeur_50fr * 0.9)
    st.info(f"Total : **{total_50:.2f} €**")

with col2:
    st.markdown("**Pièces de 10 Frs**")
    nb_10fr = st.number_input("Quantité 10 Frs :", min_value=0, step=1, value=1, key="calc_10")
    total_10 = nb_10fr * (valeur_10fr * 0.9)
    st.info(f"Total : **{total_10:.2f} €**")

# Total général
st.warning(f"**Montant total estimé : {(total_50 + total_10):.2f} €**")

st.caption(f"Dernière mise à jour basée sur : {prix_actuel_g} €/g")
