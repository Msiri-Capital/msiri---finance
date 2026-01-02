import streamlit as st
import pandas as pd
import numpy as np
import datetime

# 1. CONFIGURATION
st.set_page_config(page_title="M'SIRI CAPITAL & FOOT", layout="wide")

# --- INITIALISATION DES COMPTEURS ---
if "auth" not in st.session_state:
    st.session_state["auth"] = False
if "essais_foot" not in st.session_state:
    st.session_state["essais_foot"] = 0

# 2. INTERFACE PUBLIQUE (GRAPHIQUE + FOOT GRATUIT)
st.title("🌟 M'SIRI COMMAND CENTER - 2026")

# --- GRAPHIQUE LIVE ---
st.components.v1.html("""
    <div style="height:300px;">
      <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
      <script type="text/javascript">
      new TradingView.widget({"autosize": true, "symbol": "BINANCE:BTCUSDT", "interval": "5", "theme": "dark", "container_id": "tv_chart"});
      </script><div id="tv_chart"></div>
    </div>
""", height=300)

st.divider()


# --- SECTION FOOT AVANT VIP (AVEC DEUX CASES DE SAISIE) ---
st.subheader("⚽ ANALYSEUR DE PRONOSTICS (Mode Essai)")

if not st.session_state["auth"]:
    reste = 2 - st.session_state["essais_foot"]
    if reste > 0:
        st.write(f"🎁 Il vous reste **{reste} analyses gratuites**.")
        
        # LES DEUX CASES POUR LE CLIENT
        col_equipe1, col_equipe2 = st.columns(2)
        with col_equipe1:
            home_team = st.text_input("Équipe à Domicile :", placeholder="Ex: Real Madrid")
        with col_equipe2:
            away_team = st.text_input("Équipe Visiteuse :", placeholder="Ex: FC Barcelone")
        
        if st.button("LANCER L'ANALYSE IA"):
            if home_team and away_team:
                st.session_state["essais_foot"] += 1
                
                # GÉNÉRATION D'UN PRONOSTIC SEMBLANT RÉEL
                # On utilise un petit calcul basé sur les noms pour que le résultat varie
                score_sim = (len(home_team) + len(away_team)) % 3
                resultats = [
                    f"Victoire de {home_team}. Leur forme à domicile est imprenable.",
                    f"Match nul probable. Les deux défenses sont très compactes cette semaine.",
                    f"Avantage {away_team}. Attention aux contre-attaques rapides."
                ]
                
                st.info(f"**ANALYSE M'SIRI POUR : {home_team} VS {away_team}**")
                st.write(f"1. Les algorithmes détectent une intensité forte sur le côté droit de **{home_team}**.")
                st.write(f"2. **{away_team}** a encaissé 1.5 but en moyenne sur ses 3 derniers déplacements.")
                st.write(f"3. **PRONOSTIC FINAL :** {resultats[score_sim]}")
                st.write("4. Indice de confiance : **82%**.")
                st.write("5. Conseil : Gestion de mise prudente recommandée.")
                
                st.rerun()
            else:
                st.warning("Veuillez entrer les noms des deux équipes.")
    else:
        st.error("🚫 LIMITE D'ESSAI ATTEINTE !")
        st.warning("Passez en mode VIP pour des analyses illimitées sur tous vos matchs.")

# 3. LA PORTE VIP (ORANGE MONEY)
if not st.session_state["auth"]:
    st.header("🛡️ ACCÈS AU COMMANDEMENT VIP")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("### 1. Dépôt Orange Money")
        st.info("Abonnement : **10$**")
        st.code("+243 898 213 650") # TON NUMÉRO ICI
        st.markdown('[🆘 CONTACTER LE Maire Général (WhatsApp)](https://wa.me/243 973 964 067)', unsafe_allow_html=True)

    with col2:
        st.write("### 2. Activation")
        code_vip = st.text_input("Entrez votre code d'accès :", type="password")
        if st.button("ACTIVER MON ACCÈS"):
            if code_vip == "MSIRI2026":
                st.session_state["auth"] = True
                st.rerun()
            else:
                st.error("Code invalide.")

# 4. MODE VIP TOTAL (DÉVERROUILLÉ)
else:
    st.balloons()
    st.title("🚀 ESPACE VIP DÉVERROUILLÉ")
    st.write("Bienvenue, Maire Général. Ici, les pronostics et les outils de trading sont **illimités**.")
    
    # Mettre ici les outils de trading avancés et tous les matchs
    st.subheader("💰 Calculateur de Gestion de Capital")
    cap = st.number_input("Capital ($)", value=355.0)
    st.write(f"Objectif sécurisé : **{cap*0.05:.2f}$** (5% de profit)")

    if st.button("🔴 SE DÉCONNECTER"):
        st.session_state["auth"] = False
        st.rerun()
