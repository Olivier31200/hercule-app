import streamlit as st
import yfinance as yf
import pandas as pd

# Configuration de la page pour un affichage optimal sur iPhone
st.set_page_config(page_title="Hercule Tracker", page_icon="🪙", layout="wide")

st.title("🪙 Hercule Silver : Dashboard Pro")

# --- 1. RÉCUPÉRATION DU COURS EN DIRECT ---
@st.cache_data(ttl=600)  # Mise à jour toutes les 10 minutes
def get_live_price():
    try:
        # Ticker Silver (SI=F) et Taux de change (EURUSD=X)
        silver = yf.Ticker("SI=F").fast_info['last_price']
        forex = yf.Ticker("EURUSD=X").fast_info['last_price']
        # Calcul : (Prix USD / once 31.1035g) / taux_change
        return round((silver / 31.1035) / forex, 3)
    except Exception:
        return 2.46  # Valeur par défaut de sécurité

current_gram_price = get_live_price()

st.metric(label="Cours actuel de l'Argent Pur", value=f"{current_gram_price} €/g")

# --- 2. TABLEAU DE STRATÉGIE (CIBLES D'ACHAT) ---
st.divider()
st.subheader("🎯 Stratégie : Radar de Pépites")
st.write("Seuils de rentabilité pour vos futures recherches :")

val_50f = current_gram_price * 27.0
val_10f = current_gram_price * 22.5

strategie_data = {
    "Pièce": ["50F Hercule (27g)", "10F Hercule (22.5g)"],
    "VALEUR MÉTAL (100%)": [f"{round(val_50f, 2)} €", f"{round(val_10f, 2)} €"],
    "-10% (Affaire ⚠️)": [f"{round(val_50f * 0.9, 2)} €", f"{round(val_10f * 0.9, 2)} €"],
    "-20% (🚨 ACHAT !)": [f"{round(val_50f * 0.8, 2)} €", f"{round(val_10f * 0.8, 2)} €"]
}

st.table(pd.DataFrame(strategie_data))

# --- 3. RECHERCHE LEBONCOIN (FRANCE ENTIÈRE) ---
st.subheader("🕵️‍♂️ Liens de recherche rapide")
col_lbc1, col_lbc2 = st.columns(2)

# On filtre Leboncoin sur le prix "Valeur Métal" pour ne voir que les bonnes affaires
with col_lbc1:
    url_50f = f"https://www.leboncoin.fr/recherche?category=30&text=50%20francs%20hercule&price=min-{int(val_50f)}&sort=time"
    st.link_button("Chercher 50F sur Leboncoin", url_50f, use_container_width=True)

with col_lbc2:
    url_10f = f"https://www.leboncoin.fr/recherche?category=30&text=10%20francs%20hercule&price=min-{int(val_10f)}&sort=time"
    st.link_button("Chercher 10F sur Leboncoin", url_10f, use_container_width=True)

# --- 4. VOTRE PORTEFEUILLE (VOS ACHATS) ---
st.divider()
st.subheader("💰 Mon Portefeuille")

mes_achats = [
    {"Nom": "50F Hercule", "Argent": 27.0, "Prix": 77.0},
    {"Nom": "10F Hercule", "Argent": 22.5, "Prix": 67.0}
]

total_metal = 0
total_paye = 0

for a in mes_achats:
    val_m = a["Argent"] * current_gram_price
    total_metal += val_m
    total_paye += a["Prix"]
    
    diff = val_m - a["Prix"]
    color = "green" if diff > 0 else "red"
    st.write(f"**{a['Nom']}** : Acheté {a['Prix']}€ | Métal : **{round(val_m, 2)}€** (:{color}[{round(diff, 2)}€])")

st.divider()
perf_globale = total_metal - total_paye
st.metric("Bilan Global (Valeur Métal vs Achat)", f"{round(total_metal, 2)} €", 
          delta=f"{round(perf_globale, 2)} €")

st.caption("Note : La valeur métal est le socle de sécurité. La valeur réelle peut inclure une prime de collection.")
