import streamlit as st

st.set_page_config(page_title="M'SIRI CAPITAL", page_icon="💰")

st.title("🚀 M'SIRI CAPITAL - TRADING & STRATÉGIE")
st.write(f"### Bienvenue, Maire Général Nicolas")

# Section Calculateur (Gratuit)
st.subheader("📊 Gestionnaire de Risque")
capital = st.number_input("Capital sur Pocket Broker ($)", value=355.0)
taux = st.slider("Objectif de profit journalier (%)", 1, 10, 5)
gain = capital * (taux / 100)
st.success(f"Ton objectif aujourd'hui : **{gain:.2f} $**")

st.divider()

# SECTION VIP (Payante)
st.subheader("💎 ACCÈS AUX SIGNAUX VIP (SÉCURISÉS)")
st.info("Pour copier mes trades et atteindre le million, rejoins le groupe VIP.")

col1, col2 = st.columns(2)
with col1:
    st.write("**Abonnement Mensuel :** 10$")
    st.write("**Contact Direct :** Maire Général")

with col2:
    # ICI TU METS TON NUMÉRO Orange-money
    st.warning("💳 PAIEMENT VIA Orange-Money / AIRTEL MONEY")
    st.code(" +243 898 213 650 / +243 973 964 067")
    st.write("Envoyez le message 'VIP' après le transfert.")

st.divider()
st.write("🛡️ *Propriété du Commandement M'siri 1 - ISTM Lubumbashi*")
