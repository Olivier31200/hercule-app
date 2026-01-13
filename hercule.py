import streamlit as st
import pandas as pd

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(page_title="Hercule - Cours de l'Or", layout="wide")

# Style CSS pour forcer le fond sombre si besoin et améliorer le rendu
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    div.stButton > button { width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# 2. FONCTION POUR LE PRIX ET LE STICKER
def afficher_en_tete(prix_actuel, prix_veille):
    variation = ((prix_actuel - prix_veille) / prix_veille) * 100
    couleur_sticker = "#28a745" if variation >= 0 else "#dc3545"
    signe = "+" if variation > 0 else ""
    
    sticker_html = f"""
    <div style="display: flex; align-items: center; padding: 10px 0;">
        <span style="font-size: 32px; font-weight: bold; color: white; margin-right: 15px;">
            {prix_actuel:.2f}€/g
        </span>
        <span style="
            background-color: {couleur_sticker};
            color: white;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 18px;
            font-weight: bold;
        ">
            {signe}{variation:.2f}%
        </span>
    </div>
    """
    st.markdown(sticker_html, unsafe_allow_html=True)

# --- LOGIQUE DE L'APPLICATION ---

st.title("📈 Application Hercule")

# Simulation des prix (à remplacer par vos calculs/API)
prix_actuel_cours = 2.46
prix_veille_cours = 2.40

# Affichage du prix principal
st.subheader("Cours du jour")
afficher_en_tete(prix_actuel_cours, prix_veille_cours)

st.divider()

# 3. TABLEAU DE COMPARAISON DES PIÈCES (Fonctionnalité restaurée)
st.subheader("🔍 Comparaison des pièces")

# Exemple de données pour votre tableau - Modifiez les chiffres ici
data = {
    "Nom de la pièce": ["Napoléon 20Fr", "Krugerrand", "Souverain", "Vreneli"],
    "Poids d'or pur (g)": [5.81, 31.10, 7.32, 5.81],
    "Prix Estimé (€)": [
        5.81 * prix_actuel_cours, 
        31.10 * prix_actuel_cours, 
        7.32 * prix_actuel_cours, 
        5.81 * prix_actuel_cours
    ],
    "Variation": ["+1.2%", "+0.5%", "+0.8%", "+1.1%"]
}

df = pd.DataFrame(data)

# Affichage du tableau
st.dataframe(df, use_container_width=True)

# 4. AUTRES FONCTIONNALITÉS (Graphiques, etc.)
col1, col2 = st.columns(2)
with col1:
    st.info("💡 **Info :** Le prix est mis à jour toutes les 15 minutes.")
with col2:
    st.metric(label="Spread moyen", value="2.5%", delta="-0.2%")
