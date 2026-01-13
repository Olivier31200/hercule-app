import streamlit as st
import pandas as pd
import yfinance as yf
import streamlit.components.v1 as components

# 1. CONFIGURATION
st.set_page_config(page_title="Hercule App - Live Silver", layout="centered")

# 2. RÉCUPÉRATION DES PRIX RÉELS
@st.cache_data(ttl=600)
def get_live_prices():
    try:
        usd_data = yf.Ticker("XAGUSD=X").history(period="2d")
        eur_data = yf.Ticker("XAGEUR=X").history(period="2d")
        
        prix_usd_oz = usd_data['Close'].iloc[-1]
        prix_eur_g = eur_data['Close'].iloc[-1] / 31.1035
        
        # Calcul de la variation sur le prix en Euro
        veille_eur_g = eur_data['Close'].iloc[-2] / 31.1035
        variation = ((prix_eur_g - veille_eur_g) / veille_eur_g) * 100
        
        return prix_eur_g, prix_usd_oz, variation
    except:
        return 2.46, 86.00, 1.20

p_eur_g, p_usd_oz, p_var = get_live_prices()

# 3. HEADER CORRIGÉ (Prix + Sticker en haut, USD en bas)
def afficher_double_header(eur_g, usd_oz, variation):
    couleur_badge = "#28a745" if variation >= 0 else "#dc3545"
    signe = "+" if variation > 0 else ""
    
    html = f"""
    <div style="
        background-color: #1e1e1e; 
        padding: 20px; 
        border-radius: 15px; 
        margin-bottom: 25px; 
        border: 1px solid #444;
        text-align: center;
    ">
        <div style="display: flex; align-items: center; justify-content: center; gap: 15px; margin-bottom: 5px;">
            <span style="
                font-size: 36px; 
                font-weight: bold; 
                color: white; 
                white-space: nowrap;
            ">
                {eur_g:.2f}€/g
            </span>
            <span style="
                background-color: {couleur_badge}; 
                color: white; 
                padding: 4px 12px; 
                border-radius: 15px; 
                font-size: 18px; 
                font-weight: bold;
                white-space: nowrap;
            ">
                {signe}{variation:.2f}%
            </span>
        </div>
        
        <div style="font-size: 24px; color: #aaaaaa; font-weight: 500;">
            ${usd_oz:.2f}/oz
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

# --- INTERFACE ---
st.title("🪙 Hercule Live Tracker")

# Affichage du bandeau de prix réorganisé
afficher_double_header(p_eur_g, p_usd_oz, p_var)

# 4. GRAPHIQUE OFFICIEL TRADINGVIEW ($/oz)
st.write("### 📈 Cours de l'Argent (TradingView)")
tradingview_widget = """
<div class="tradingview-widget-container" style="height:450px; width:100%;">
  <div id="tradingview_xag"></div>
  <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
  <script type="text/javascript">
  new TradingView.widget({
    "autosize": true,
    "symbol": "OANDA:XAGUSD",
    "interval": "D",
    "timezone": "Europe/Paris",
    "theme": "dark",
    "style": "1",
    "locale": "fr",
    "toolbar_bg": "#f1f3f6",
    "enable_publishing": false,
    "hide_top_toolbar": false,
    "save_image": false,
    "container_id": "tradingview_xag"
  });
  </script>
</div>
"""
components.html(tradingview_widget, height=450)

# 5. GRILLE DE RACHAT
st.write("### 📋 Valeur des pièces Hercule")
argent_pur_50fr, argent_pur_10fr = 27.0, 22.5
val_50 = argent_pur_50fr * p_eur_g
val_10 = argent_pur_10fr * p_eur_g

df_pieces = pd.DataFrame({
    "Pièce": ["50 Francs Hercule (27g)", "10 Francs Hercule (22.5g)"],
    "Spot (€)": [f"{val_50:.2f}", f"{val_10:.2f}"],
    "-10% (Normal)": [f"{val_50*0.9:.2f}", f"{val_10*0.9:.2f}"],
    "🚨 -20% (Urgence)": [f"{val_50*0.8:.2f}", f"{val_10*0.8:.2f}"]
})
st.dataframe(df_pieces, hide_index=True, use_container_width=True)

# 6. CALCULATEURS
st.divider()
st.write("### 🧮 Calculateurs")
c1, c2 = st.columns(2)
with c1:
    q50 = st.number_input("Nombre de 50 Frs", min_value=0, value=1)
    st.info(f"Total (-10%) : **{q50 * val_50 * 0.9:.2f} €**")
with c2:
    q10 = st.number_input("Nombre de 10 Frs", min_value=0, value=1)
    st.info(f"Total (-10%) : **{q10 * val_10 * 0.9:.2f} €**")

# 7. BOUTONS LEBONCOIN
st.write("### 🛒 Leboncoin (Collection)")
lb1, lb2 = st.columns(2)
with lb1:
    st.link_button("Chercher 50 Frs", "https://www.leboncoin.fr/recherche?category=53&text=50%20francs%20hercule", use_container_width=True)
with lb2:
    st.link_button("Chercher 10 Frs", "https://www.leboncoin.fr/recherche?category=53&text=10%20francs%20hercule", use_container_width=True)
