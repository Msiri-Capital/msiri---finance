import streamlit as st
import pandas as pd
import numpy as np
import datetime
import random
import math

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(page_title="M'SIRI CAPITAL 2.0", layout="wide")

# --- CERVEAU MATHÉMATIQUE (VOS FORMULES) ---
def calcul_poisson_msiri(equipe_a, equipe_b):
    # Simulation des lambdas (buts attendus)
    lambda_a = random.uniform(1.2, 2.8) 
    lambda_b = random.uniform(0.8, 2.0)
    
    def poisson_prob(k, lamb):
        return (math.exp(-lamb) * (lamb**k)) / math.factorial(k)

    prob_win_a = 0
    prob_draw = 0
    prob_win_b = 0
    
    for i in range(6):
        for j in range(6):
            p = poisson_prob(i, lambda_a) * poisson_prob(j, lambda_b)
            if i > j: prob_win_a += p
            elif i == j: prob_draw += p
            else: prob_win_b += p

    scores_possibles = []
    for i in range(4):
        for j in range(4):
            prob = poisson_prob(i, lambda_a) * poisson_prob(j, lambda_b)
            scores_possibles.append((f"{i}-{j}", prob))
    
    scores_possibles.sort(key=lambda x: x[1], reverse=True)
    
    return {
        "win_a": prob_win_a * 100,
        "draw": prob_draw * 100,
        "win_b": prob_win_b * 100,
        "top_scores": scores_possibles[:3],
        "btts": (1 - poisson_prob(0, lambda_a)) * (1 - poisson_prob(0, lambda_b)) * 100,
        "over25": (1 - (poisson_prob(0, lambda_a+lambda_b) + poisson_prob(1, lambda_a+lambda_b) + poisson_prob(2, lambda_a+lambda_b))) * 100
    }

# --- INITIALISATION DU SESSION STATE ---
if "auth" not in st.session_state:
    st.session_state["auth"] = False
if "accueil_vu" not in st.session_state:
    st.session_state["accueil_vu"] = False
if "essais_foot_gratuits" not in st.session_state:
    st.session_state["essais_foot_gratuits"] = 0

# --- VARIABLES ---
NUMERO_ORANGE_MONEY = "+243898213650" 
CODE_VIP_MOIS = "SLVC2026"        
CODE_ADMIN = "MAIRE243"

# --- SIDEBAR ADMIN ---
with st.sidebar:
    st.title("🛡️ ADMIN")
    pass_admin = st.text_input("Code Secret :", type="password")
    if pass_admin == CODE_ADMIN:
        st.write("Clé VIP actuelle :", CODE_VIP_MOIS)

# --- FENÊTRE 1 : MOT D'ACCUEIL ---
if not st.session_state["accueil_vu"]:
    st.title("🌟 M'SIRI CAPITAL : LE COMMANDEMENT")
    st.subheader("L'IA au service de votre indépendance financière.")
    st.divider()
    st.write("Bienvenue dans le terminal le plus puissant de Lubumbashi.")
    if st.button("ACCÉDER AU TERMINAL"):
        st.session_state["accueil_vu"] = True
        st.balloons()
        st.rerun()

# --- FENÊTRE 2 : MODE PUBLIC ---
elif not st.session_state["auth"]:
    st.title("🚀 TERMINAL DE DÉCOUVERTE")
    
    # Graphique TradingView
    st.components.v1.html("""<div style="height:300px;"><script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script><script type="text/javascript">new TradingView.widget({"autosize": true, "symbol": "BINANCE:BTCUSDT", "interval": "5", "theme": "dark", "container_id": "tv_chart_pub"});</script><div id="tv_chart_pub"></div></div>""", height=300)

    st.divider()
    st.subheader("⚽ ANALYSEUR IA (Mode Essai)")
    
    if st.session_state["essais_foot_gratuits"] < 2:
        c1, c2 = st.columns(2)
        eq1 = c1.text_input("Domicile :", key="pub_eq1")
        eq2 = c2.text_input("Extérieur :", key="pub_eq2")
        
        if st.button("LANCER L'ANALYSE GRATUITE"):
            if eq1 and eq2:
                st.session_state["essais_foot_gratuits"] += 1
                res = calcul_poisson_msiri(eq1, eq2)
                st.success(f"Probabilité Victoire {eq1} : {res['win_a']:.1f}%")
                st.balloons()
draw']:.1f}%")
                m3.metric(v_eq2, f"{res['win_b']:.1f}%")
                
                st.write("**🎯 Scores Exacts Probables :**")
                for s, p in res['top_scores']:
                    st.write(f"- {s} : ({p*100:.1f}%)")
                st.balloons()

st.divider()
st.caption("© 2026 M'SIRI CAPITAL - Lubumbashi.")
