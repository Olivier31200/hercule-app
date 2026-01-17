import streamlit as st
import pandas as pd
import yfinance as yf
import streamlit.components.v1 as components

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(page_title="Hercule App - Live Silver", layout="centered", page_icon="🪙")

# 2. RÉCUPÉRATION DES PRIX RÉELS (Mise à jour au lancement)
@st.cache_data(ttl=300)  # Actualise les données toutes les 5 minutes maximum
def get_live_prices():
    try:
        # Téléchargement des tickers Argent ($) et Taux de change (€/$)
        # On prend l'intervalle 1m pour avoir le dernier prix exact du marché
        data = yf.download(["XAGUSD=X", "EURUSD=X"], period="2d", interval="1m", progress=False)
        
        # Prix de l'once en Dollar
        p_usd_oz = data['Close']['XAGUSD=X'].iloc[-1]
        # Taux de change (combien de $ pour 1€)
        eur_usd_rate = data['Close']['EURUSD=X'].iloc[-1]
        
        # Conversion en Euro par gramme
        # 1 once troy = 31.1034768 grammes
        p_eur_oz = p_usd_oz / eur_usd_rate
        p_eur_g = p_eur_oz / 31.1034768
        
        # Calcul de la variation sur 24h
        veille_usd_oz = data['Close']['XAGUSD=X'].iloc[0]
        variation = ((p_usd_oz - veille_usd_oz) / veille_usd_oz) * 100
        
        return p_eur_g, p_usd_oz, variation
    except Exception as e:
        # Valeurs de secours réalistes si l'API Yahoo ne répond pas
        return 0.94, 30.50, 0.00

# APPEL DES DONNÉES (Se rafraîchit à chaque exécution du script)
prix_eur_g, prix_usd_oz, var_percent = get_live_prices()

# 3. FONCTION D'AFFICHAGE DU HEADER
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

# --- INTERFACE UTILISATEUR ---

st.title("🪙 Hercule Live Tracker")

# Affichage du bandeau de prix dynamique
afficher_header_style(prix_eur_g, prix_usd_oz, var_percent)

# 4. GRAPHIQUE TRADINGVIEW (Optionnel, dans un expander pour gagner de la place)
with st.expander("📈 Voir le graphique en temps réel", expanded=False):
    tradingview_widget = """
    <div class="tradingview-widget-container" style="height:400px;">
      <div id="tradingview_xag"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
      <script type="text/javascript">
      new TradingView.widget({
        "autosize": true,
        "symbol": "OANDA:XAGUSD",
        "interval": "H",
        "timezone": "Europe/Paris",
        "theme": "dark",
        "style": "1",
        "locale": "fr",
        "container_id": "tradingview_xag"
      });
      </script>
    </div>
    """
    components.html(tradingview_widget, height=420)

# 5. TABLEAU DES VALEURS PAR PIÈCE (MIS À JOUR EN TEMPS RÉEL)
st.write("### 📋 Valeur intrinsèque (Argent Pur)")

# Calculs basés sur le titre à 900/1000e
# 50 Francs Hercule = 30g brut (27g fin) | 10 Francs Hercule = 25g brut (22.5g fin)
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

# 6. CALCULATEURS DE LOTS
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

# 7. BOUTONS VERS LEBONCOIN
st.write("### 🛒 Opportunités Leboncoin")
b1, b2 = st.columns(2)
with b1:
    st.link_button("Rechercher 50 Frs", "https://www.leboncoin.fr/recherche?category=40&text=50%20francs%20hercule", use_container_width=True)
with b2:
    st.link_button("Rechercher 10 Frs", "https://www.leboncoin.fr/recherche?category=40&text=10%20francs%20hercule", use_container_width=True)

# Footer de mise à jour
st.caption(f"Les prix sont actualisés automatiquement. Cours actuel : {prix_eur_g:.4f} €/g.")
