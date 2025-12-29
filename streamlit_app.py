import streamlit as st
import pandas as pd
import numpy as np
import time

st.set_page_config(page_title="M'SIRI CAPITAL VIP", page_icon="📈")

# --- STYLE ET TITRE ---
st.title("💎 M'SIRI CAPITAL - TRADING TERMINAL")
st.write("### Station de Commandement - Maire Général Nicolas")

# --- SYSTÈME DE VÉRIFICATION ---
if "authentifie" not in st.session_state:
    st.session_state["authentifie"] = False

if not st.session_state["authentifie"]:
    st.info("🔒 ZONE SÉCURISÉE : IDENTIFICATION REQUISE")
    code_entre = st.text_input("Code d'Accès VIP :", type="password")
    
    # TON CODE SECRET ICI
    if st.button("DÉBLOQUER L'ACCÈS"):
        if code_entre == "MSIRI2025": # Change-le si tu veux
            st.session_state["authentifie"] = True
            st.rerun()
        else:
            st.error("ACCÈS REFUSÉ. Contactez le Maire Général pour obtenir votre clé.")
            st.write("💳 Paiement Orange-money : ** +243 898 213 650 **")

# --- CONTENU VIP (Graphique + Calculateur) ---
if st.session_state["authentifie"]:
    st.success("✅ CONNEXION ÉTABLIE AVEC LES MARCHÉS")
    
    # 1. GRAPHIQUE EN DIRECT (Simulation temps réel)
    st.subheader("📈 Évolution du Marché (Live)")
    
    # Création de données dynamiques pour le graphique
    chart_data = pd.DataFrame(
        np.random.randn(20, 2) / 10 + [0.5, 0.5],
        columns=['Bitcoin (BTC)', 'Gold (XAU)']
    )
    st.line_chart(chart_data)
    
    # 2. CALCULATEUR DE PROFIT
    st.divider()
    st.subheader("🧮 Calculateur de Stratégie")
    col1, col2 = st.columns(2)
    
    with col1:
        cap = st.number_input("Capital ($)", value=355.0)
    with col2:
        obj = st.slider("Objectif journalier (%)", 1, 10, 5)
    
    profit = cap * (obj / 100)
    st.metric(label="Gain Cible", value=f"{profit:.2f} $", delta=f"{obj}%")
    
    if st.button("🔴 Fermer la Session"):
        st.session_state["authentifie"] = False
        st.rerun()

st.divider()
st.caption("© 2025 M'SIRI COMMANDEMENT - Lubumbashi, RDC")
