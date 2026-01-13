import streamlit as st
import pandas as pd

# 1. CONFIGURATION
st.set_page_config(page_title="Hercule App - Cotations", layout="centered")

# 2. DONNÉES DE BASE (Modifiez ces valeurs ici)
prix_actuel_g = 2.46  # Le prix en €/g
prix_veille_g = 2.40  # Pour le calcul de la tendance
argent_pur_50fr = 27.0   # 50 Francs Hercule = 27g d'argent pur
argent_pur_10fr = 22.5   # 10 Francs Hercule = 22.5g d'argent pur

# 3. FONCTION STICKER (Prix en blanc + Badge couleur)
def afficher_header_prix(actuel, veille):
    variation = ((actuel - veille) / veille) * 100
    couleur_badge = "#28a745" if variation >= 0 else "#dc3545"
    signe = "+" if variation > 0 else ""
    
    html = f"""
    <div style="display: flex; align-items: center; justify-content: center; background-color: #1e1e1e; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
        <span style="font-size: 30px; font-weight: bold; color: white; margin-right: 15px;">
            {actuel:.2f}€/g
        </span>
        <span style="background-color: {couleur_badge}; color: white; padding: 5px 12px; border-radius: 15px; font-size: 18px; font-weight: bold;">
            {signe}{variation:.2f}%
        </span>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

# --- AFFICHAGE ---

st.title("💰 Cotations Pièces Hercule")

# Affichage du bandeau de prix
afficher_header_prix(prix_actuel_g, prix_veille_g)

st.write("### Calcul des rachats (Décotes)")

# 4. PRÉPARATION DU TABLEAU DE COMPARAISON
# Calculs pour 50 Francs
valeur_50fr = argent_pur_50fr * prix_actuel_g
moins_10_50fr = valeur_50fr * 0.90
moins_20_50fr = valeur_50fr * 0.80

# Calculs pour 10 Francs
valeur_10fr = argent_pur_10fr * prix_actuel_g
moins_10_10fr = valeur_10fr * 0.90
moins_20_10fr = valeur_10fr * 0.80

data = {
    "Pièce Hercule": ["50 Francs (27g pur)", "10 Francs (22.5g pur)"],
    "Valeur Spot (€)": [f"{valeur_50fr:.2f} €", f"{valeur_10fr:.2f} €"],
    "-10% (Rachat standard)": [f"{moins_10_50fr:.2f} €", f"{moins_10_10fr:.2f} €"],
    "-20% (Marge haute)": [f"{moins_20_50fr:.2f} €", f"{moins_20_10fr:.2f} €"]
}

df = pd.DataFrame(data)

# Affichage du tableau stylisé
st.table(df)

# Petit rappel du cours de la veille
st.caption(f"Cours de référence de la veille : {prix_veille_g:.2f} €/g")

# 5. ZONE DE CALCUL PERSONNALISÉ
st.divider()
st.write("### Calculateur rapide")
nb_pieces = st.number_input("Nombre de pièces (50 Frs)", min_value=0, value=1)
total = nb_pieces * moins_10_50fr
st.success(f"Prix de rachat total (-10%) : **{total:.2f} €**")
