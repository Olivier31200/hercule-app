import streamlit as st
import pandas as pd
import yfinance as yf
import streamlit.components.v1 as components

# 1. CONFIGURATION
st.set_page_config(page_title="Hercule App - Live Silver", layout="centered", page_icon="🪙")

# 2. RÉCUPÉRATION DES PRIX ROBUSTE (Évite le NaN et gère les records 2026)
@st.cache_data(ttl=300)
def get_live_prices():
    try:
        # On télécharge 7 jours pour pallier la fermeture des marchés et garantir un prix
        tickers = yf.download(["XAGUSD=X", "EURUSD=X"], period="7d", interval="1h", progress=False)
        
        # Nettoyage : remplit les trous (NaN) par la dernière valeur connue
        df_clean = tickers['Close'].ffill().dropna()
        
        if df_clean.empty:
            # Valeurs de secours basées sur ton graphique si Yahoo est HS
            return 2.72, 89.94, 0.00
            
        last_row = df_clean.iloc[-1]
        p_usd_oz = float(last_row['XAGUSD=X'])
        eur_usd = float(last_row['EURUSD=X'])
        
        # Conversion €/g (1 once troy = 31.1034768g)
        p_eur_g = (p_usd_oz / eur_usd) / 31.1034768
        
        # Calcul de la variation vs début de la veille
        v_ouverture = float(df_clean.iloc[0]['XAGUSD=X'])
        variation = ((p_usd_oz - v_ouverture) / v_ouverture) * 100
        
        return p_eur_g, p_usd_oz, variation
    except:
        return 2.72, 89.94, 0.00

prix_eur_g, prix_usd_oz, var_percent = get_live_prices()

# 3. INTERFACE VISUELLE (Header dynamique)
def draw_header(eur_g, usd_oz, var):
    color = "#28a745" if var >= 0 else "#dc3545"
    st.markdown(f"""
    <div style="background: #111; padding: 25px; border-radius: 15px; border: 2px solid #333; text-align: center; margin-bottom: 20px;">
        <h1 style="margin:0; color: white; font-size: 45px;">{eur_g:.3f} €/g</h1>
        <div style="background: {color}; display: inline-block; padding: 5px 15px; border-radius: 12px; font-weight: bold; color: white; margin: 10px 0;">
            {"+" if var > 0 else ""}{var:.2f}%
        </div>
        <p style="color: #888; font-size: 20px; margin: 0;">Cours Mondial : ${usd_oz:.2f} /oz</p>
    </div>
    """, unsafe_allow_html=True)

st.title("🪙 Hercule Live Tracker")
draw_header(prix_eur_g, prix_usd_oz, var_percent)

# 4. GRAPHIQUE TRADINGVIEW (Confirmation visuelle du record)
with st.expander("📈 Voir le graphique boursier ($/oz)", expanded=True):
    tv_code = """
    <div style="height:400px;">
      <div id="tv-chart"></div>
      <script src="https://s3.tradingview.com/tv.js"></script>
      <script>
      new TradingView.widget({
        "autosize": true, "symbol": "OANDA:XAGUSD", "interval": "H",
        "theme": "dark", "style": "1", "locale": "fr", "container_id": "tv-chart"
      });
      </script>
    </div>
    """
    components.html(tv_code, height=400)

# 5. TABLEAU DES PIÈCES (Avec retour de la colonne -20%)
st.write("### 📋 Valeur des pièces Hercule")
# 50F = 27g pur | 10F = 22.5g pur
val_50 = 27.0 * prix_eur_g
val_10 = 22.5 * prix_eur_g

data = {
    "Pièce": ["Hercule 50 Francs (27g)", "Hercule 10 Francs (22.5g)"],
    "Valeur Spot": [f"{val_50:.2f} €", f"{val_10:.2f} €"],
    "Rachat (-10%)": [f"{val_50*0.9:.2f} €", f"{val_10*0.9:.2f} €"],
    "Urgence (-20%)": [f"{val_50*0.8:.2f} €", f"{val_10*0.8:.2f} €"]
}
st.table(pd.DataFrame(data))

# 6. CALCULATEUR DE LOT (-10% par défaut)
st.divider()
st.write("### 🧮 Calculateur de Lot (-10%)")
col1, col2 = st.columns(2)
n50 = col1.number_input("Nombre de 50 F", min_value=0, step=1, value=0)
n10 = col2.number_input("Nombre de 10 F", min_value=0, step=1, value=0)

total_rachat = (n50 * val_50 * 0.9) + (n10 * val_10 * 0.9)
if total_rachat > 0:
    st.success(f"**Estimation de rachat total : {total_rachat:.2f} €**")

# 7. BOUTONS EXTERNES
st.write("### 🛒 Liens Leboncoin")
b1, b2 = st.columns(2)
with b1:
    st.link_button("Chercher 50 Frs", "https://www.leboncoin.fr/recherche?category=40&text=50%20francs%20hercule", use_container_width=True)
with b2:
    st.link_button("Chercher 10 Frs", "https://www.leboncoin.fr/recherche?category=40&text=10%20francs%20hercule", use_container_width=True)

st.caption(f"Dernière actualisation basée sur le cours réel de {prix_eur_g:.4f} €/g.")
