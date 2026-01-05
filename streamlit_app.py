import streamlit as st
import pandas as pd
import numpy as np
import datetime
import random

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(page_title="M'SIRI CAPITAL 2026", layout="wide")

# --- INITIALISATION DU CERVEAU (SESSION STATE) ---
if "auth" not in st.session_state:
    st.session_state["auth"] = False
if "accueil_vu" not in st.session_state:
    st.session_state["accueil_vu"] = False
if "essais_foot_gratuits" not in st.session_state:
    st.session_state["essais_foot_gratuits"] = 0
if "nb_visites" not in st.session_state:
    st.session_state["nb_visites"] = 0

# Compteur de visite (Vue cachée)
st.session_state["nb_visites"] += 1

# --- VARIABLES DE CONTRÔLE ---
NUMERO_ORANGE_MONEY = "+243 898 213 650" # Remplace par ton numéro
CODE_VIP_MOIS = "SLVC2026"        # Ton code VIP actuel
CODE_ADMIN = "MAIRE243"              # Ton code secret pour voir les stats

# --- STYLE CSS ---
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; font-weight: bold; }
    .stMetric { background-color: #1e2129; padding: 10px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR (ESPACE COMMANDANT CACHÉ) ---
with st.sidebar.expander("🔐 ESPACE COMMANDANT"):
    pass_admin = st.text_input("Code Secret Admin :", type="password")
    if pass_admin == CODE_ADMIN:
        st.write("### 📊 STATS LIVE")
        st.metric("Interactions Session", st.session_state["nb_visites"])
        st.write(f"Clé VIP active : `{CODE_VIP_MOIS}`")

# --- FENÊTRE 1 : ACCUEIL ---
if not st.session_state["accueil_vu"]:
    st.title("🌟 M'SIRI CAPITAL - LUBUMBASHI")
    st.subheader("Prenez le contrôle de votre destin financier.")
    st.divider()
    st.info("""
    **Bienvenue Maire Général !**
    Découvrez la puissance de l'IA appliquée au Trading et aux Pronostics Sportifs.
    Plus de 85% de précision constatée.
    """)
    if st.button("ENTRER DANS LE TERMINAL"):
        st.session_state["accueil_vu"] = True
        st.rerun()

# --- FENÊTRE 2 : MODE PUBLIC (DÉCOUVERTE) ---
elif not st.session_state["auth"]:
    st.title("🚀 TERMINAL DE DÉCOUVERTE")
    
    # Graphique TradingView
    st.components.v1.html("""
        <div style="height:300px;">
          <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
          <script type="text/javascript">
          new TradingView.widget({"autosize": true, "symbol": "BINANCE:BTCUSDT", "interval": "5", "theme": "dark", "container_id": "tv_chart"});
          </script><div id="tv_chart"></div>
        </div>
    """, height=300)

    st.divider()

    # Section Foot
    st.subheader("⚽ ANALYSEUR DE MATCHS (Mode Essai)")
    if st.session_state["essais_foot_gratuits"] < 2:
        reste = 2 - st.session_state["essais_foot_gratuits"]
        st.write(f"🎁 Il vous reste **{reste} essais gratuits**.")
        
        c1, c2 = st.columns(2)
        with c1:
            eq1 = st.text_input("Équipe Domicile :", key="pub_eq1")
        with c2:
            eq2 = st.text_input("Équipe Extérieure :", key="pub_eq2")
        
        if st.button("LANCER L'ANALYSE IA"):
            if eq1 and eq2:
                st.session_state["essais_foot_gratuits"] += 1
                res = random.choice([
                    f"Victoire de **{eq1}**. Forme imprenable à domicile.",
                    f"Match nul probable. Défenses très compactes.",
                    f"Avantage **{eq2}**. Attention à leur contre-attaque."
                ])
                st.success(f"**PRONOSTIC :** {res}")
                st.balloons()
            else:
                st.warning("Veuillez remplir les deux noms.")
    else:
        st.error("🚫 LIMITE D'ESSAI ATTEINTE !")
        st.warning("Passez en mode VIP pour continuer.")

    st.divider()

    # Paiement
    st.header("👑 DEVENIR MEMBRE VIP")
    col_pay1, col_pay2 = st.columns(2)
    with col_pay1:
        st.write("### 1. Dépôt Orange Money")
        st.info("Abonnement : **10$ / Mois**")
        st.code(NUMERO_ORANGE_MONEY)
        st.markdown(f"[🆘 CONTACT WHATSAPP](https://wa.me/{0973964067})")
    
    with col_pay2:
        st.write("### 2. Activation")
        code_input = st.text_input("Entrez votre code VIP :", type="password")
        if st.button("DÉBLOQUER TOUT"):
            if code_input == CODE_VIP_MOIS:
                st.session_state["auth"] = True
                st.rerun()
            else:
                st.error("Code invalide.")

# --- FENÊTRE 3 : MODE VIP (ILLIMITÉ) ---
else:
    st.title("🏆 ESPACE VIP - ILLIMITÉ")
    st.write(f"Bienvenue Commandant. Session active : {datetime.datetime.now().strftime('%d/%m/%Y')}")

    tab1, tab2 = st.tabs(["📊 Trading Pro", "⚽ Foot Illimité"])

    with tab1:
        st.subheader("Calculateur de Gestion de Risque")
        cap = st.number_input("Votre Capital ($) :", value=100.0)
        st.write(f"Pour un risque de 3%, misez maximum : **{cap*0.03:.2f}$** par trade.")
        st.divider()
        st.info(f"Signal IA Trading : **{random.choice(['🟢 ACHAT FORT', '🟡 ATTENTE', '🔴 VENTE CONSEILLÉE'])}**")

    with tab2:
        st.subheader("Analyses Foot Sans Limite")
        v_eq1 = st.text_input("Équipe Domicile (VIP) :")
        v_eq2 = st.text_input("Équipe Extérieure (VIP) :")
        if st.button("ANALYSE VIP"):
            st.success(f"Analyse terminée pour {v_eq1} vs {v_eq2}. Confiance : 92%.")

    if st.sidebar.button("🔴 SE DÉCONNECTER"):
        st.session_state["auth"] = False
        st.session_state["accueil_vu"] = False
        st.rerun()
