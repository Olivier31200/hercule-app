import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# 1. CONFIGURATION
st.set_page_config(page_title="Hercule App", layout="centered")

# 2. DONNÉES (Valeurs à ajuster)
prix_actuel_g = 2.46
prix_veille_g = 2.30
argent_pur_50fr = 27.0
argent_pur_10fr = 22.5

# 3. HEADER AVEC STICKER (Prix en Blanc + Badge Couleur)
def afficher_header(actuel, veille):
    variation = ((actuel - veille) / veille) * 100
    couleur_badge = "#28a745" if variation >= 0 else "#dc3545"
    signe = "+" if variation > 0 else ""
    
    html = f"""
    <div style="display: flex; align-items: center; justify-content: center; background-color: #1e1e1e; padding: 25px; border-radius: 15px; margin-bottom: 20px; border: 1px solid #444;">
        <span style="font-size: 36px; font-weight: bold; color: white; margin-right: 20px;">
            {actuel:.2f}€/g
        </span>
        <span style="background-color: {couleur_badge}; color: white; padding: 6px 15px; border-radius: 20px; font-size: 20px; font-weight: bold;">
            {signe}{variation:.2f}%
        </span>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

# --- INTERFACE ---
st.title("🪙 Hercule Silver Tracker")

# Affichage du prix principal
afficher_header(prix_actuel_g, prix_veille_g)

# 4. GRAPHIQUE OFFICIEL (TRADINGVIEW)
st.write("### 📈 Cours de l'Argent (XAGEUR)")
tradingview_chart = """
<div class="tradingview-widget-container" style="height:400px;">
  <div id="tradingview_chart"></div>
  <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
  <script type="text/javascript">
  new TradingView.widget({
    "autosize": true,
    "symbol": "OANDA:XAGEUR",
    "interval": "D",
    "timezone": "Europe/Paris",
    "theme": "dark",
    "style": "1",
    "locale": "fr",
    "toolbar_bg": "#f1f3f6",
    "enable_publishing": false,
    "allow_symbol_change": true,
    "container_id": "tradingview_chart"
  });
  </script>
</div>
"""
components.html(tradingview_chart, height=400)

# 5. GRILLE DE RACHAT (SANS INDEX)
st.write("### 📋 Valeur des pièces")
val_50 = argent_pur_50fr * prix_actuel_g
val_10 = argent_pur_10fr * prix_actuel_g

data = {
    "Pièce": ["50 Francs Hercule", "10 Francs Hercule"],
    "Spot (€)": [f"{val_50:.2f}", f"{val_10:.2f}"],
    "-10% (Normal)": [f"{val_50*0.9:.2f}", f"{val_10*0.9:.2f}"],
    "🚨 -20% (Urgence)": [f"{val_50*0.8:.2f}", f"{val_10*0.8:.2f}"]
}
st.dataframe(pd.DataFrame(data), hide_index=True, use_container_width=True)

# 6. CALCULATEURS
st.divider()
col1, col2 = st.columns(2)
with col1:
    nb_50 = st.number_input("Quantité 50 Frs", min_value=0, value=1, key="50")
    st.info(f"Rachat (-10%) : **{nb_50 * val_50 * 0.9:.2f} €**")
with col2:
    nb_10 = st.number_input("Quantité 10 Frs", min_value=0, value=1, key="10")
    st.info(f"Rachat (-10%) : **{nb_10 * val_10 * 0.9:.2f} €**")

# 7. BOUTONS LEBONCOIN
st.write("### 🛒 Vérifier les prix sur Leboncoin")
col_lb1, col_lb2 = st.columns(2)

# URL Leboncoin filtrée sur Catégorie Collection (53)
url_50fr = "https://www.leboncoin.fr/recherche?category=53&text=50%20francs%20hercule"
url_10fr = "https://www.leboncoin.fr/recherche?category=53&text=10%20francs%20hercule"

with col_lb1:
    st.link_button("Rechercher 50 Frs", url_50fr, use_container_width=True)
with col_lb2:
    st.link_button("Rechercher 10 Frs", url_10fr, use_container_width=True)

st.caption(f"Calculé sur la base de {prix_actuel_g}€/g (Argent pur)")
