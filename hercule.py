import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Hercule Tracker Pro", page_icon="🪙", layout="wide")

st.title("🪙 Hercule Silver : Suivi & Stratégie")

# --- 1. RÉCUPÉRATION DU COURS EN DIRECT ---
@st.cache_data(ttl=600)
def get_live_price():
    try:
        # Argent (Silver) et Taux de change EUR/USD
        silver = yf.Ticker("SI=F").fast_info['last_price']
        forex = yf.Ticker("EURUSD=X").fast_info['last_price']
        # Calcul : (Prix USD / once) / 31.1035 / taux_change
        return round((silver / 31.1035) / forex, 3)
    except:
        return 2.46  # Valeur par défaut si l'API échoue

current_gram_price = get_live_price()

st.metric(label="Cours actuel de l'Argent Pur", value=f"{current_gram_price} €/g")

# --- 2. NOUVEAU : TABLEAU DE COMPARAISON (CIBLES D'ACHAT) ---
st.divider()
st.subheader("🎯 Cibles d'Achat (Radar Pépites)")
st.write("Utilisez ce tableau pour juger les annonces Leboncoin en temps réel :")

# Calculs des seuils
val_50f = current_gram_price * 27.0
val_10f = current_gram_price * 22.5

strategie_data = {
    "Pièce": ["50F Hercule", "10F Hercule"],
    "VALEUR MÉTAL (100%)": [f"{round(val_50f, 2)} €", f"{round(val_10f, 2)} €"],
    "-10% (Affaire ⚠️)": [f"{round(val_50f * 0.9, 2)} €", f"{round(val_10f * 0.9, 2)} €"],
    "-20% (🚨 ACHAT !)": [f"{round(val_50f * 0.8, 2)} €", f"{round(val_10f * 0.8, 2)} €"]
}

st.table(pd.DataFrame(strategie_data))

# --- 3. BILAN DE VOS ACHATS PERSONNELS ---
st.divider()
st.subheader("💰 Mon Portefeuille (Vos achats)")

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
    st.write(f"**{a['Nom']}** : Acheté {a['Prix']}€ | Métal : {round(val_m, 2)}€ (:{color}[{round(diff, 2)}€])")

st.divider()
st.metric("Plus-value totale (Métal vs Achat)", f"{round(total_metal, 2)} €", 
          delta=f"{round(total_metal - total_paye, 2)} €")

st.info("Astuce : Si une annonce Leboncoin est proche de la colonne -20%, n'attendez pas, c'est une anomalie de marché !")
