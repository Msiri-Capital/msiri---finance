import streamlit as st
import pandas as pd
import numpy as np
import datetime
import random

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(page_title="M'SIRI CAPITAL 2.0", layout="wide")

# --- INITIALISATION DU SESSION STATE ---
if "auth" not in st.session_state:
    st.session_state["auth"] = False
if "accueil_vu" not in st.session_state:
    st.session_state["accueil_vu"] = False
if "essais_foot_gratuits" not in st.session_state:
    st.session_state["essais_foot_gratuits"] = 0
if "nb_visites" not in st.session_state:
    st.session_state["nb_visites"] = 0

st.session_state["nb_visites"] += 1

# --- VARIABLES ---
NUMERO_ORANGE_MONEY = "+243 898 213 650" 
CODE_VIP_MOIS = "SLVC2026"        
CODE_ADMIN = "MAIRE243"              

# --- SIDEBAR (ESPACE COMMANDANT) ---
with st.sidebar.expander("🔐 ESPACE COMMANDANT"):
    pass_admin = st.text_input("Code Secret Admin :", type="password")
    if pass_admin == CODE_ADMIN:
        st.write("### 📊 STATS LIVE")
        st.metric("Vues de la session", st.session_state["nb_visites"])
        st.write(f"Clé active : `{CODE_VIP_MOIS}`")

# --- FENÊTRE 1 : MOT D'ACCUEIL CAPTIVANT ---
if not st.session_state["accueil_vu"]:
    st.title("🌟 M'SIRI CAPITAL : LE COMMANDEMENT")
    st.subheader("L'IA au service de votre indépendance financière.")
    st.divider()
    
    st.markdown("""
    ### 🤝 Bonjour Maire Général !
    Bienvenue dans le terminal le plus puissant de Lubumbashi. 
    Ici, nous ne laissons rien au hasard. Que vous soyez ici pour dominer les marchés du **Trading** ou pour valider vos **Pronostics Sportifs**, vous êtes au bon endroit.

    * * pourquoi Nous choisir
    * **Précision IA :** Analyses basées sur des algorithmes avancés.
    * **Gestion de Risque :** Apprenez à protéger votre capital.
    * **Succès Communautaire :** Rejoignez les 100 premiers conquérants.
    """)
    
    if st.button("ACCÉDER AU TERMINAL DE DÉCISION"):
        st.session_state["accueil_vu"] = True
        st.balloons() # Célébration dès l'entrée !
        st.rerun()

# --- FENÊTRE 2 : MODE PUBLIC (DÉCOUVERTE) ---
elif not st.session_state["auth"]:
    st.title("🚀 TERMINAL DE DÉCOUVERTE")
    
    # Graphique TradingView Public
    st.components.v1.html("""
        <div style="height:300px;">
          <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
          <script type="text/javascript">
          new TradingView.widget({"autosize": true, "symbol": "BINANCE:BTCUSDT", "interval": "5", "theme": "dark", "container_id": "tv_chart_pub"});
          </script><div id="tv_chart_pub"></div>
        </div>
    """, height=300)

    st.divider()

    st.subheader("⚽ ANALYSEUR DE MATCHS (Mode Essai)")
    if st.session_state["essais_foot_gratuits"] < 2:
        reste = 2 - st.session_state["essais_foot_gratuits"]
        st.info(f"🎁 Cadeau : Il vous reste **{reste} analyses gratuites**.")
        
        c1, c2 = st.columns(2)
        with c1:
            eq1 = st.text_input("Équipe Domicile :", key="pub_eq1")
        with c2:
            eq2 = st.text_input("Équipe Extérieure :", key="pub_eq2")
        
        if st.button("LANCER L'ANALYSE GRATUITE"):
            if eq1 and eq2:
                st.session_state["essais_foot_gratuits"] += 1
                res = random.choice([
                    f"Victoire de **{eq1}**. Forme imprenable à domicile.",
                    f"Match nul probable. Défenses très compactes.",
                    f"Avantage **{eq2}**. Attention à leur contre-attaque."
                ])
                st.success(f"**PRONOSTIC IA :** {res}")
                st.balloons() # Succès visuel
            else:
                st.warning("Veuillez remplir les deux noms.")
    else:
        st.error("🚫 LIMITE D'ESSAI ATTEINTE !")
        st.warning("Passez en mode VIP pour continuer l'aventure.")

    st.divider()

    # Section Paiement
    st.header("👑 PASSER EN MODE VIP")
    col_pay1, col_pay2 = st.columns(2)
    with col_pay1:
        st.info("Abonnement : **10$ / Mois**")
        st.write(f"Envoyez par Orange Money au : **{NUMERO_ORANGE_MONEY}**")
        st.markdown(f"[🆘 CONTACT WHATSAPP POUR LA CLÉ](https://wa.me/{+243973964067})")
    
    with col_pay2:
        code_input = st.text_input("Entrez votre code d'activation :", type="password")
        if st.button("ACTIVER MON ACCÈS VIP"):
            if code_input == CODE_VIP_MOIS:
                st.session_state["auth"] = True
                st.balloons() # Grande célébration pour le nouveau VIP !
                st.rerun()
            else:
                st.error("Code invalide ou expiré.")

# --- FENÊTRE 3 : MODE VIP (ILLIMITÉ) ---
else:
    st.title("🏆 ESPACE VIP M'SIRI")
    st.success(f"Bienvenue au Commandement Des Vainqueur, session du {datetime.datetime.now().strftime('%d/%m/%Y')}")

    # Graphique TradingView VIP (Aussi présent ici)
    st.subheader("📈 Surveillance des Marchés Live")
    st.components.v1.html("""
        <div style="height:400px;">
          <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
          <script type="text/javascript">
          new TradingView.widget({"autosize": true, "symbol": "BINANCE:BTCUSDT", "interval": "1", "theme": "dark", "container_id": "tv_chart_vip"});
          </script><div id="tv_chart_vip"></div>
        </div>
    """, height=400)

    st.divider()

    tab1, tab2 = st.tabs(["📊 Stratégie de Trading", "⚽ Pronostics Foot Illimités"])

    with tab1:
        st.subheader("Calculateur de Gestion des Risques")
        cap = st.number_input("Votre Capital actuel ($) :", value=100.0)
        st.write(f"Conseil : Ne risquez pas plus de **{cap*0.03:.2f}$** sur ce trade (3%).")
        
        st.divider()
        st.subheader("🤖 Signal IA M'SIRI")
        signal = random.choice(['🟢 ACHAT FORT (BUY)', '🟡 ATTENTE (WAIT)', '🔴 VENTE (SELL)'])
        st.info(f"Tendance actuelle : **{signal}**")

    with tab2:
        st.subheader("Analyses Illimitées")
        v_eq1 = st.text_input("Match Domicile :", key="v_eq1")
        v_eq2 = st.text_input("Match Extérieur :", key="v_eq2")
        if st.button("ANALYSE STRATÉGIQUE VIP"):
            if v_eq1 and v_eq2:
                st.success(f"Analyse pour {v_eq1} vs {v_eq2} : Avantage tactique détecté. Confiance 94%.")
                st.balloons()
            else:
                st.warning("Veuillez entrer les équipes.")

    if st.sidebar.button("🔴 DÉCONNEXION"):
        st.session_state["auth"] = False
        st.session_state["accueil_vu"] = False
        st.rerun()

st.divider()
st.caption("© 2026 M'SIRI CAPITAL - Lubumbashi. L'excellence financièrPrécisionision.")
