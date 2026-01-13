import streamlit as st

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(page_title="Hercule App", page_icon="📈")

def afficher_prix_avec_sticker(prix_actuel, prix_veille):
    # Calcul de la variation
    if prix_veille == 0:
        variation = 0
    else:
        variation = ((prix_actuel - prix_veille) / prix_veille) * 100

    # Détermination de la couleur et du signe
    couleur = "#28a745" if variation >= 0 else "#dc3545"  # Vert ou Rouge
    signe = "+" if variation > 0 else ""
    
    # Code HTML pour le sticker
    sticker_html = f"""
    <div style="display: flex; align-items: center; font-family: sans-serif;">
        <span style="font-size: 24px; font-weight: bold; color: #31333F;">
            {prix_actuel:.2f}€/g
        </span>
        <span style="
            background-color: {couleur};
            color: white;
            padding: 2px 10px;
            border-radius: 15px;
            margin-left: 12px;
            font-size: 16px;
            font-weight: bold;
        ">
            {signe}{variation:.2f}%
        </span>
    </div>
    """
    st.markdown(sticker_html, unsafe_allow_html=True)

# 2. DONNÉES (À modifier selon vos besoins)
st.title("Tableau de bord Hercule")

# Simulation de données
prix_du_jour = 2.46
prix_hier = 2.40

# 3. AFFICHAGE
st.write("### Cours actuel")
afficher_prix_avec_sticker(prix_du_jour, prix_hier)

# Espace vide
st.divider()

# Optionnel : Affichage standard Streamlit (plus simple)
st.write("### Vue détaillée (Format Metric)")
delta_val = prix_du_jour - prix_hier
st.metric(label="Prix de l'or (exemple)", value="2,46 €/g", delta=f"{delta_val:.2f} €/g")
