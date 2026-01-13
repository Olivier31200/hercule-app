import streamlit as st
import pandas as pd

# 1. CONFIGURATION
st.set_page_config(page_title="Hercule App - Cotations", layout="centered")

# 2. DONNÉES DE BASE (Modifiez ces valeurs ici)
prix_actuel_g = 2.46  # Le prix actuel en €/g
prix_veille_g = 2.40  # Prix de la veille pour calcul de tendance
argent_pur_50fr = 27.0   # 50 Francs Hercule = 27g d'argent pur
argent_pur_10fr = 22.5   # 10 Francs Hercule = 22.5g d'argent pur

# 3. FONCTION STICKER (Prix en blanc + Badge couleur)
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

st.title("💰 Cotations Pièces Hercule")

# Affichage du bandeau de prix (Prix en blanc)
afficher_header_prix(prix_actuel_g, prix_veille_g)

st.write("### Grille de rachat")

# 4. CALCULS ET TABLEAU
valeur_50fr = argent_pur_50fr * prix_actuel_g
valeur_10fr = argent_pur_10fr * prix_actuel_g

data = {
    "Pièce Hercule": ["50 Francs (27g pur)", "10 Francs (22.5g pur)"],
    "Valeur Spot": [f"{valeur_50fr:.2f} €", f"{valeur_10fr:.2f} €"],
    "-10% (Normal)": [f"{valeur_50fr*0.9:.2f} €", f"{valeur_10fr*0.9:.2f} €"],
    "🚨 -20% (Urgence)": [f"{valeur_50fr*0.8:.2f} €", f"{valeur_10fr*0.8:.2f} €"]
}

df = pd.DataFrame(data)

# Affichage du tableau sans les index (0, 1)
st.dataframe(df, hide_index=True, use_container_width=True)

# 5. CALCULATEUR RAPIDE
st.divider()
st.write("### Calculateur 50 Frs")
nb_50fr = st.number_input("Nombre de pièces de 50 Francs :", min_value=0, step=1, value=1)
total_rachat = nb_50fr * (valeur_50fr * 0.9)
st.success(f"Estimation rachat (-10%) pour {nb_50fr} pièce(s) : **{total_rachat:.2f} €**")

st.caption(f"Comparatif basé sur le cours de la veille : {prix_veille_g:.2f} €/g")
