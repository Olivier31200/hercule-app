import streamlit as st
import pandas as pd
import yfinance as yf
import streamlit.components.v1 as components

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(page_title="Hercule App - Live Silver", layout="centered", page_icon="🪙")

# 2. RÉCUPÉRATION DES PRIX (Version Robuste : cherche la dernière valeur connue)
@st.cache_data(ttl=300)
def get_live_prices():
    try:
        # On télécharge 5 jours de données pour être sûr de traverser les week-ends
        # Intervalle '1h' est plus fiable que '1m' pour les valeurs historiques
        data = yf.download(["XAGUSD=X", "EURUSD=X"], period="5d", interval="1h", progress=False)
        
        # On nettoie les données : on garde uniquement les lignes complètes
        # ffill() remplit les trous, dropna() supprime si vraiment vide
        prices = data['Close'].ffill().dropna()
        
        if prices.empty:
            return 0.945, 30.50, 0.00 # Valeurs de secours si tout échoue

        # On récupère la dernière ligne valide
        last_row = prices.iloc[-1]
        p_usd_oz = float(last_row['XAGUSD=X'])
        eur_usd_rate = float(last_row['EURUSD=X'])
        
        # Calcul du prix en €/g
        p_eur_oz = p_usd_oz / eur_usd_rate
        p_eur_g = p_eur_oz / 31.1034768
        
        # Calcul de la variation (différence avec le premier point des 5 jours ou la veille)
        p_ouverture = float(prices.iloc[0]['XAGUSD=X'])
        variation = ((p_usd_oz - p_ouverture) / p_ouverture) * 100
        
        return p_eur_g, p_usd_oz, variation

    except Exception:
        # En cas de bug réseau total, on renvoie une estimation fixe pour ne pas casser l'affichage
        return 0.94, 30.40, 0.00

# Exécution de la récupération
prix_eur_g, prix_usd_oz, var_percent = get_live_prices()

# 3. AFFICHAGE DU HEADER
def afficher_header_style(eur_g, usd_oz, variation):
    couleur_badge = "#28a745" if variation >= 0 else "#dc3545"
    signe = "+" if variation > 0 else ""
    
    html_header = f"""
    <div style="background-color: #1e1e1e; padding: 25px; border-radius: 15px; border: 1px solid #444; text-align: center; font-family: sans-serif; margin-bottom: 20px;">
        <div style="display: flex; align-items: center; justify-content: center; gap: 15px;">
            <span style="font-size: 40px; font-weight: bold; color: white; white-space: nowrap;">
                {eur_g:.3f}€/g
            </span>
            <span style="background-color: {couleur_badge}; color: white; padding: 5px 15px; border-radius: 20px; font-size: 20px; font-weight: bold;">
                {signe}{variation:.2f}%
            </span>
        </div>
        <div style="font-size: 20px; color: #aaaaaa; margin-top: 10px;">
            Cours Mondial : ${usd_oz:.2f}/oz
        </div>
    </div>
    """
    st.markdown(html_header, unsafe_allow_html=True)

# --- INTERFACE ---

st.title("🪙 Hercule Live Tracker")

afficher_header_style(prix_eur_g, prix_usd_oz, var_percent)

# 4. GRAPHIQUE TRADINGVIEW
with st.expander("📈 Voir le graphique en temps réel", expanded=False):
    tradingview_widget = """
    <div class="tradingview-widget-container" style="height:400px;">
      <div id="tradingview_xag"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
      <script type="text/javascript">
      new TradingView.widget({
        "autosize": true, "symbol": "OANDA:XAGUSD", "interval": "H",
        "timezone": "Europe/Paris", "theme": "dark", "style": "1",
        "locale": "fr", "container_id": "tradingview_xag"
      });
      </script>
    </div>
    """
    components.html(tradingview_widget, height=420)

# 5. TABLEAU DE VALEUR DES PIÈCES
st.write("### 📋 Valeur intrinsèque (Argent Pur)")

poids_50f = 27.0
poids_10f = 22.5

val_spot_50 = poids_50f * prix_eur_g
val_spot_10 = poids_10f * prix_eur_g

data_pieces = {
    "Pièce": ["Hercule 50 Francs", "Hercule 10 Francs"],
    "Argent Pur": ["27.00g", "22.50g"],
    "Valeur Spot (€)": [f"{val_spot_50:.2f}", f"{val_spot_10:.2f}"],
    "Rachat -10%": [f"{val_spot_50*0.9:.2f}", f"{val_spot_10*0.9:.2f}"],
    "Rachat -20%": [f"{val_spot_50*0.8:.2f}", f"{val_spot_10*0.8:.2f}"]
}
st.dataframe(pd.DataFrame(data_pieces), hide_index=True, use_container_width=True)

# 6. CALCULATEURS
st.divider()
st.write("### 🧮 Estimateur de rachat direct (-10%)")
c1, c2 = st.columns(2)
with c1:
    q50 = st.number_input("Nombre de 50 Frs", min_value=0, value=0, step=1)
with c2:
    q10 = st.number_input("Nombre de 10 Frs", min_value=0, value=0, step=1)

total_rachat = (q50 * val_spot_50 * 0.9) + (q10 * val_spot_10 * 0.9)
if total_rachat > 0:
    st.success(f"**Montant total estimé (Net) : {total_rachat:.2f} €**")

# 7. BOUTONS LBC
st.write("### 🛒 Opportunités Leboncoin")
b1, b2 = st.columns(2)
with b1:
    st.link_button("Rechercher 50 Frs", "https://www.leboncoin.fr/recherche?category=40&text=50%20francs%20hercule", use_container_width=True)
with b2:
    st.link_button("Rechercher 10 Frs", "https://www.leboncoin.fr/recherche?category=40&text=10%20francs%20hercule", use_container_width=True)

st.caption(f"Dernière actualisation : {prix_eur_g:.4f} €/g. (Données persistantes en cas de fermeture des marchés)")
