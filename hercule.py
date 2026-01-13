import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime

# 1. CONFIGURATION
st.set_page_config(page_title="Hercule App", layout="centered")

# 2. RÉCUPÉRATION DES DONNÉES (Yahoo Finance)
@st.cache_data(ttl=3600)
def get_market_data():
    # XAGUSD=X : Argent en Dollar/Once
    # XAGEUR=X : Argent en Euro/Once
    ticker_usd = yf.Ticker("XAGUSD=X")
    ticker_eur = yf.Ticker("XAGEUR=X")
    
    hist_usd = ticker_usd.history(period="1mo")
    hist_eur = ticker_eur.history(period="1mo")
    
    # Prix actuels
    usd_oz = hist_usd['Close'].iloc[-1]
    eur_oz = hist_eur['Close'].iloc[-1]
    eur_g = eur_oz / 31.1035
    
    # Pour le calcul de variation (%)
    veille_eur_g = hist_eur['Close'].iloc[-2] / 31.1035
    
    return usd_oz, eur_g, veille_eur_g, hist_usd['Close']

try:
    prix_usd_oz, prix_eur_g, prix_veille_g, graph_data = get_market_data()
except:
    # Valeurs de secours si l'API est indisponible
    prix_usd_oz, prix_eur_g, prix_veille_g = 86.00, 2.46, 2.40
    graph_data = pd.Series([82, 83, 85, 86])

# 3. HEADER AVEC DOUBLE VALEUR + STICKER
def afficher_double_header(eur_g, usd_oz, veille_g):
    variation = ((eur_g - veille_g) / veille_g) * 100
    couleur_badge = "#28a745" if variation >= 0 else "#dc3545"
    signe = "+" if variation > 0 else ""
    
    html = f"""
    <div style="display: flex; flex-direction: column; align-items: center; background-color: #1e1e1e; padding: 20px; border-radius: 15px; margin-bottom: 25px; border: 1px solid #444;">
        <div style="display: flex; align-items: center; gap: 20px;">
            <span style="font-size: 32px; font-weight: bold; color: white;">
                {eur_g:.2f}€/g
            </span>
            <span style="font-size: 24px; color: #aaaaaa; font-weight: 500;">
                ${usd_oz:.2f}/oz
            </span>
            <span style="background-color: {couleur_badge}; color: white; padding: 4px 12px; border-radius: 15px; font-size: 18px; font-weight: bold;">
                {signe}{variation:.2f}%
            </span>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

# --- INTERFACE ---
st.title("🪙 Hercule Silver Tracker")

# 1. Le Header Double
afficher_double_header(prix_eur_g, prix_usd_oz, prix_veille_g)

# 2. Le Graphique Officiel en $/oz
st.write("### 📈 Cours Mondial de l'Argent ($/oz)")
st.line_chart(graph_data)

# 3. Grille de Rachat (Hercule)
st.write("### 📋 Valeur des pièces")
argent_pur_50fr, argent_pur_10fr = 27.0, 22.5
val_50 = argent_pur_50fr * prix_eur_g
val_10 = argent_pur_10fr * prix_eur_g

data_pieces = {
    "Pièce": ["50 Francs Hercule", "10 Francs Hercule"],
    "Spot (€)": [f"{val_50:.2f}", f"{val_10:.2f}"],
    "-10% (Normal)": [f"{val_50*0.9:.2f}", f"{val_10*0.9:.2f}"],
    "🚨 -20% (Urgence)": [f"{val_50*0.8:.2f}", f"{val_10*0.8:.2f}"]
}
st.dataframe(pd.DataFrame(data_pieces), hide_index=True, use_container_width=True)

# 4. Calculateurs
st.divider()
col1, col2 = st.columns(2)
with col1:
    nb_50 = st.number_input("Qté 50 Frs", min_value=0, value=1)
    st.info(f"Rachat : **{nb_50 * val_50 * 0.9:.2f} €**")
with col2:
    nb_10 = st.number_input("Qté 10 Frs", min_value=0, value=1)
    st.info(f"Rachat : **{nb_10 * val_10 * 0.9:.2f} €**")

# 5. Leboncoin
st.write("### 🛒 Leboncoin (Catégorie Collection)")
c1, c2 = st.columns(2)
with c1:
    st.link_button("Chercher 50 Frs", "https://www.leboncoin.fr/recherche?category=53&text=50%20francs%20hercule", use_container_width=True)
with c2:
    st.link_button("Chercher 10 Frs", "https://www.leboncoin.fr/recherche?category=53&text=10%20francs%20hercule", use_container_width=True)
