import streamlit as st

st.title("💰 M'SIRI CAPITAL - TRADING")
st.write("Bienvenue, Maire Général Nicolas.")

# Zone de calcul de profit
capital = st.number_input("Capital sur Pocket Broker ($)", value=355.0)
taux = st.slider("Objectif de profit journalier (%)", 1, 10, 5)
gain = capital * (taux / 100)

st.success(f"Ton objectif aujourd'hui est de gagner : {gain:.2f} $")

# Message pour les futurs clients
st.warning("⚠️ Pour accéder aux signaux VIP, payez via Orange-money.")
