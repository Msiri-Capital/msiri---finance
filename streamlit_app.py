import streamlit as st
import pandas as pd
import numpy as np
import datetime

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(page_title="M'SIRI COMMAND CENTER 2026", layout="wide")

# 2. SYSTÈME DE SÉCURITÉ (LA PORTE VIP)
if "auth" not in st.session_state:
    st.session_state["auth"] = False

# --- SI L'UTILISATEUR N'EST PAS CONNECTÉ ---
if not st.session_state["auth"]:
    st.title("🛡️ M'SIRI CAPITAL - ACCÈS SÉCURISÉ")
    st.write("### Identifiez-vous pour accéder au Commandement")
    
    # LA ZONE OÙ METTRE LE CODE EST ICI :
    code_entre = st.text_input("CLÉ DE CHIFFREMENT VIP :", type="password")
    
    if st.button("DÉVERROUILLER LE TERMINAL"):
        if code_entre == "MSIRI2026": # TON CODE SECRET
            st.session_state["auth"] = True
            st.rerun() # Relance l'application pour afficher le contenu
        else:
            st.error("ACCÈS REFUSÉ. CONTACTEZ LE MAIRE GÉNÉRAL.")
            st.write("🍊 Orange Money : ** +243 898 213 650 **")

# --- SI L'UTILISATEUR EST CONNECTÉ (LE CONTENU VIP) ---
else:
    st.title("📈 TERMINAL DE COMMANDEMENT M'SIRI v2.0")
    st.success(f"Bienvenue Maire Général | Session du {datetime.datetime.now().strftime('%d/%m/%Y')}")

    # --- COLONNES PRINCIPALES ---
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("💰 Gestion de Capital")
        capital_initial = st.number_input("Capital Actuel ($)", value=355.0)
        objectif_journalier = st.slider("Objectif de Profit (%)", 1, 15, 5)
        
        profit_cible = capital_initial * (objectif_journalier / 100)
        st.metric("Objectif du Jour", f"+{profit_cible:.2f} $")
        
        st.divider()
        st.subheader("🤖 Indicateur M'SIRI IA")
        tendance = np.random.choice(["🔥 FORTE ACHAT", "📉 VENTE", "⏳ ATTENTE"])
        st.info(f"Analyse du Signal : **{tendance}**")

    with col2:
        st.subheader("📊 Projection vers le Million")
        jours = np.arange(1, 31)
        croissance = capital_initial * (1 + objectif_journalier/100)**jours
        df_proj = pd.DataFrame({'Jour': jours, 'Capital Projeté ($)': croissance})
        st.line_chart(df_proj.set_index('Jour'))
  
    # --- SECTION JOURNAL DE BORD ---
    st.divider()
    st.subheader("📝 Journal de Guerre (Profits)")
    gain_reel = st.number_input("Gain réalisé aujourd'hui ($)", value=0.0)
    if st.button("ENREGISTRER LA SESSION"):
        st.toast("Session enregistrée !")

    if st.button("🔴 Fermer le Terminal (Se déconnecter)"):
        st.session_state["auth"] = False
        st.rerun()
