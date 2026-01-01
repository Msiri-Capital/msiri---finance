import streamlit as st
import pandas as pd
import numpy as np
import datetime

# Configuration de la page
st.set_page_config(page_title="M'SIRI COMMAND CENTER 2026", layout="wide")

# --- STYLE PERSONNALISÉ ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #e0e0e0; }
    .stButton>button { width: 100%; background-color: #ff4b4b; color: white; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- VÉRIFICATION VIP ---
if "auth" not in st.session_state:
    st.session_state["auth"] = False

if not st.session_state["auth"]:
    st.title("🛡️ M'SIRI CAPITAL - ACCÈS SÉCURISÉ")
    code = st.text_input("CLÉ DE CHIFFREMENT VIP :", type="password")
    if st.button("DÉVERROUILLER LE TERMINAL"):
        if code == "MSIRI2026": # Ton nouveau code pour 2026
            st.session_state["auth"] = True
            st.rerun()
        else:
            st.error("ACCÈS REFUSÉ. CONTACTEZ LE MAIRE GÉNÉRAL.")
            st.write("🍊 Orange Money : **Ton Numéro Ici**")

# --- TERMINAL ACTIF ---
else:
    st.title("📈 TERMINAL DE COMMANDEMENT M'SIRI v2.0")
    st.write(f"Date : {datetime.datetime.now().strftime('%d/%m/%Y')} | État : **Opérationnel**")

    # --- COLONNES PRINCIPALES ---
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("💰 Gestion de Capital")
        capital_initial = st.number_input("Capital Actuel ($)", value=355.0)
        objectif_journalier = st.slider("Objectif de Profit (%)", 1, 15, 5)
        
        profit_cible = capital_initial * (objectif_journalier / 100)
        st.metric("Objectif du Jour", f"+{profit_cible:.2f} $", f"{objectif_journalier}%")
        
        st.divider()
        st.subheader("🤖 Indicateur M'SIRI IA")
        tendance = np.random.choice(["🔥 FORTE ACHAT", "📉 VENTE", "⏳ ATTENTE"])
        st.info(f"Analyse du Signal : **{tendance}**")

    with col2:
        st.subheader("📊 Projection vers le Million")
        # Simulation de croissance composée
        jours = np.arange(1, 31)
        croissance = capital_initial * (1 + objectif_journalier/100)**jours
        df_proj = pd.DataFrame({'Jour': jours, 'Capital Projeté ($)': croissance})
        st.line_chart(df_proj.set_index('Jour'))
        
        st.success(f"À ce rythme, dans 30 jours ton capital sera de : **{croissance[-1]:.2f} $**")

    # --- FOOTER ---
    st.divider()
    if st.button("🔴 Fermer le Terminal"):
        st.session_state["auth"] = False
        st.rerun()
