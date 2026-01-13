import streamlit as st
import pandas as pd
import yfinance as yf
import streamlit.components.v1 as components

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(page_title="Hercule App - Live Silver", layout="centered")

# 2. RÉCUPÉRATION DES PRIX RÉELS (Yahoo Finance)
@st.cache_data(ttl=600)
def get_live_prices():
    try:
        # XAGUSD=X (Argent $) et XAGEUR=X (Argent €)
        usd_data = yf.Ticker("XAGUSD=X").history(period="2d")
        eur_data = yf.Ticker("XAGEUR=X").history(period="2d")
        
        p_usd_oz = usd_data['Close'].iloc[-1]
        p_eur_g = eur_data['Close'].iloc[-1] / 31.1035
        
        # Calcul de la variation sur le prix en Euro (Sticker)
        veille_eur_g = eur_data['Close'].iloc[-2] / 31.1035
        variation = ((p_eur_g - veille_eur_g) / veille_eur_g) * 100
        
        return p_eur_g, p_usd_oz, variation
    except:
        # Valeurs de secours en cas de bug API
        return 2.46, 86.00, 0.00

prix_eur_g, prix_usd_oz, var_percent = get_live_prices()

# 3. FONCTION DU HEADER (Correction du bug d'affichage)
def afficher_header_style(eur_g, usd_oz, variation):
    couleur_badge = "#28a745" if variation >= 0 else "#dc3545"
    signe = "+" if variation > 0 else ""
    
    # HTML avec protection contre le saut de ligne (white-space: nowrap)
    html_header = f"""
    <div style="background-color: #1e1e1e; padding: 25px; border-radius: 15px; border: 1px solid #444; text-align: center; font-family: sans-serif;">
        <div style="display: flex; align-items: center; justify-content: center; gap: 15px; margin-bottom: 5px;">
            <span style="font-size: 36px; font-weight: bold; color: white; white-space: nowrap;">
                {eur_g:.2f}€/g
            </span>
            <span style="background-color: {couleur_badge}; color: white; padding: 4px 12px; border-radius: 15px; font-size: 18px; font-weight: bold; white-space: nowrap;">
                {signe}{variation:.2f}%
            </span>
        </div>
        <div style="font-size: 22px; color: #aaaaaa; font-weight: 500;">
            ${usd_oz:.2f}/oz
        </div>
    </div>
    """
    st.markdown(html_header, unsafe_allow_html=True)

# --- STRUCTURE DE L'INTERFACE ---

st.title("🪙 Hercule Live Tracker")

# Affichage du bandeau prix (Ligne 1: €/g + % | Ligne 2: $/oz)
afficher_header_style(prix_eur_g, prix_usd_oz, var_percent)

# 4. GRAPHIQUE OFFICIEL TRADINGVIEW
st.write("### 📈 Graphique Mondial ($/oz)")
tradingview_widget = """
<div class="tradingview-widget-container" style="height:400px;">
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
    "enable_publishing": false,
    "hide_top_toolbar": false,
    "container_id": "tradingview_xag"
  });
  </script>
</div>
"""
components.html(tradingview_widget, height=400)

# 5. TABLEAU DE RACHAT DES PIÈCES
st.write("### 📋 Valeur des pièces Hercule")
argent_pur_50f = 27.0
argent_pur_10f = 22.5

val_spot_50 = argent_pur_50f * prix_eur_g
val_spot_10 = argent_pur_10f * prix_eur_g

data_pieces = {
    "Pièce": ["50F (27g)", "10F (22.5g)"],
    "Spot (€)": [f"{val_spot_50:.2f}", f"{val_spot_10:.2f}"],
    "-10% (Normal)": [f"{val_spot_50*0.9:.2f}", f"{val_spot_10*0.9:.2f}"],
    "🚨 -20% (Urgence)": [f"{val_spot_50*0.8:.2f}", f"{val_spot_10*0.8:.2f}"]
}
st.dataframe(pd.DataFrame(data_pieces), hide_index=True, use_container_width=True)

# 6. CALCULATEURS DOUBLES
st.divider()
st.write("### 🧮 Calculateurs de rachat (-10%)")
c1, c2 = st.columns(2)
with c1:
    q50 = st.number_input("Qté 50 Frs", min_value=0, value=1, step=1)
    st.info(f"Total : **{q50 * val_spot_50 * 0.9:.2f} €**")
with c2:
    q10 = st.number_input("Qté 10 Frs", min_value=0, value=1, step=1)
    st.info(f"Total : **{q10 * val_spot_10 * 0.9:.2f} €**")

# 7. BOUTONS LEBONCOIN
st.write("### 🛒 Leboncoin (Catégorie Collection)")
b1, b2 = st.columns(2)
with b1:
    st.link_button("Chercher 50 Frs", "https://www.leboncoin.fr/recherche?category=30&text=50%20francs%20hercule", use_container_width=True)
with b2:
    st.link_button("Chercher 10 Frs", "https://www.leboncoin.fr/recherche?category=30&text=10%20francs%20hercule", use_container_width=True)

st.caption(f"Données temps réel. Cours utilisé : {prix_eur_g:.4f} €/g")
