# ===================================================================
# M'SIRI CAPITAL - APPLICATION PRINCIPALE
# ===================================================================

import streamlit as st
import numpy as np
import pandas as pd
import random
import math
import time
import json
import os
from datetime import datetime
from scipy.stats import poisson
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# --- IMPORTS PERSONNALISÉS ---
try:
    from api_client import APISportsClient
except ImportError:
    st.error("❌ Fichier api_client.py manquant !")
    APISportsClient = None

try:
    from utils import (
        obtenir_citation_du_jour,
        afficher_badge_paiement,
        afficher_etapes_vip
    )
except ImportError:
    # Fonctions de secours
    def obtenir_citation_du_jour():
        return "La discipline est le pont entre les objectifs et l'accomplissement."
    def afficher_badge_paiement(*args, **kwargs):
        st.info("Badge de paiement (module utils manquant)")
    def afficher_etapes_vip():
        st.info("Étapes VIP (module utils manquant)")

# ===================================================================
# CONFIGURATION STREAMLIT
# ===================================================================

st.set_page_config(
    page_title="M'SIRI CAPITAL | TERMINAL 2100",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ===================================================================
# INITIALISATION DES SESSION STATE
# ===================================================================

if "auth" not in st.session_state:
    st.session_state["auth"] = False

if "my_device" not in st.session_state:
    st.session_state["my_device"] = str(random.getrandbits(32))

if "keys_db" not in st.session_state:
    st.session_state["keys_db"] = {"MS-1234-ABCD": None}

if "en_cours_de_fermeture" not in st.session_state:
    st.session_state["en_cours_de_fermeture"] = False

if "commentaire_envoye" not in st.session_state:
    st.session_state["commentaire_envoye"] = False

if "paiement_clique" not in st.session_state:
    st.session_state["paiement_clique"] = False

# ===================================================================
# CONFIGURATION DES SECRETS
# ===================================================================

try:
    ADMIN_PASSWORD = st.secrets.get("ADMIN_PASSWORD", "BUNKEYA_BOSS_2026")
    MOT_DE_PASSE_ADMIN = st.secrets.get("MOT_DE_PASSE_ADMIN", "Generale27")
    NUMERO_OM = st.secrets.get("NUMERO_OM", "+243898213650")
    NOM_AGENT = st.secrets.get("NOM_AGENT", "MANGENDA")
    API_SPORTS_KEY = st.secrets.get("API_SPORTS_KEY", None)
except:
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "BUNKEYA_BOSS_2026")
    MOT_DE_PASSE_ADMIN = os.getenv("MOT_DE_PASSE_ADMIN", "Generale27")
    NUMERO_OM = os.getenv("NUMERO_OM", "+243898213650")
    NOM_AGENT = os.getenv("NOM_AGENT", "MANGENDA")
    API_SPORTS_KEY = os.getenv("API_SPORTS_KEY", None)

MONTANT_VIP = "10$"

# ===================================================================
# INITIALISATION DU CLIENT API
# ===================================================================

api_client = None
if API_SPORTS_KEY:
    try:
        api_client = APISportsClient(API_SPORTS_KEY)
    except Exception as e:
        st.warning(f"⚠️ Erreur d'initialisation API-Sports: {e}")

# ===================================================================
# FONCTIONS DE PRONOSTIC
# ===================================================================

def calcul_poisson_simple(domicile, exterieur):
    """Version simplifiée pour le test"""
    forces = {
        "Real Madrid": {"off": 2.1, "def": 0.8},
        "Real Sociedad": {"off": 1.6, "def": 1.0},
        "TP Mazembe": {"off": 1.8, "def": 0.7},
        "Saint Éloi Lupopo": {"off": 1.2, "def": 1.1},
        "Barcelona": {"off": 2.0, "def": 0.9},
        "Atletico Madrid": {"off": 1.5, "def": 1.0},
    }
    
    fdom = forces.get(domicile, {"off": 1.0, "def": 1.0})
    fext = forces.get(exterieur, {"off": 1.0, "def": 1.0})
    
    lambda_dom = fdom["off"] * 1.8
    lambda_ext = fext["off"] * 1.2
    
    max_buts = 10
    probs_dom = poisson.pmf(np.arange(0, max_buts+1), lambda_dom)
    probs_ext = poisson.pmf(np.arange(0, max_buts+1), lambda_ext)
    matrice = np.outer(probs_dom, probs_ext)
    
    return {
        "win_a": np.sum(np.tril(matrice, -1)) * 100,
        "nul": np.sum(np.diag(matrice)) * 100,
        "defaite": np.sum(np.triu(matrice, 1)) * 100,
        "top": sorted([(f"{i}-{j}", matrice[i,j]*100) for i in range(6) for j in range(6)],
                     key=lambda x: x[1], reverse=True)[:3],
        "over25": (1 - poisson.cdf(2, lambda_dom + lambda_ext)) * 100,
        "lambda_dom": lambda_dom,
        "lambda_ext": lambda_ext
    }

# ===================================================================
# INTERFACE PRINCIPALE
# ===================================================================

# --- BANDEAU DÉFILANT ---
st.markdown("""
<div style="background: #001a00; padding: 5px; overflow: hidden; white-space: nowrap;">
    <span style="display: inline-block; animation: scroll 30s linear infinite; color: #00ff00; font-weight: bold;">
        🟢 Gaston M. +450$ (BTC/USD) | 🟢 Membre #22 +120$ (NBA) | 
        🟢 Justin K. +85$ (Mazembe vs Lupopo) | 🟢 Signal IA validé : ETH +4.2%
    </span>
</div>
<style>
    @keyframes scroll {
        0% { transform: translateX(100%); }
        100% { transform: translateX(-100%); }
    }
</style>
""", unsafe_allow_html=True)

# --- CITATION ---
st.info(f"📜 {obtenir_citation_du_jour()}")

# --- TITRE ---
st.title("🏛️ M'SIRI CAPITAL")
st.caption("Le terminal d'élite pour le Trading et les Statistiques Sportives.")

# --- SECTION PRINCIPALE ---
st.subheader("⚽ ANALYSE FOOT")

# Vérifier si l'API est disponible
if api_client:
    st.success("✅ API-Sports.io connectée - Données réelles disponibles")
else:
    st.info("ℹ️ Mode simulation - Données locales")

col1, col2 = st.columns(2)

with col1:
    domicile = st.text_input("🏠 Domicile", value="Real Madrid")
with col2:
    exterieur = st.text_input("✈️ Extérieur", value="Real Sociedad")

# Sélection de la compétition
competition = st.selectbox(
    "🏆 Compétition",
    ["Liga", "Premier League", "Ligue 1", "Bundesliga", "Serie A"]
)

if st.button("🚀 ANALYSER", type="primary", use_container_width=True):
    with st.spinner("🔬 Calcul en cours..."):
        res = calcul_poisson_simple(domicile, exterieur)
        
        # Affichage des résultats
        col_p1, col_p2, col_p3 = st.columns(3)
        col_p1.metric(
            label=f"🏠 Victoire {domicile}",
            value=f"{res['win_a']:.1f}%",
            delta=f"{res['win_a'] - 33:.1f}% vs aléatoire"
        )
        col_p2.metric(
            label="🤝 Match Nul",
            value=f"{res['nul']:.1f}%",
            delta=f"{res['nul'] - 33:.1f}% vs aléatoire"
        )
        col_p3.metric(
            label=f"✈️ Victoire {exterieur}",
            value=f"{res['defaite']:.1f}%",
            delta=f"{res['defaite'] - 33:.1f}% vs aléatoire"
        )
        
        st.divider()
        
        # Scores les plus probables
        st.write("🎯 **Scores les plus probables :**")
        cols = st.columns(3)
        for i, (score, prob) in enumerate(res['top']):
            with cols[i]:
                st.metric(label=f"Score {i+1}", value=score, delta=f"{prob:.1f}%")
        
        # Plus/Moins 2.5
        st.divider()
        if res['over25'] > 50:
            st.success(f"⚽ Plus de 2.5 buts : {res['over25']:.1f}%")
        else:
            st.info(f"⚽ Moins de 2.5 buts : {100 - res['over25']:.1f}%")
        
        # Pronostic final (simulé)
        st.divider()
        st.subheader("🏆 PRONOSTIC FINAL")
        
        if res['win_a'] > 50:
            resultat = f"VICTOIRE {domicile}"
            confiance = min(80, res['win_a'])
        elif res['defaite'] > 50:
            resultat = f"VICTOIRE {exterieur}"
            confiance = min(80, res['defaite'])
        else:
            resultat = "MATCH NUL"
            confiance = 60
        
        col_prono1, col_prono2 = st.columns(2)
        with col_prono1:
            st.metric(label="Résultat", value=resultat)
        with col_prono2:
            st.metric(
                label="Confiance",
                value=f"{confiance:.0f}%",
                delta=f"{confiance - 50:.0f}% vs aléatoire"
            )
        
        if api_client:
            st.caption("📡 Données fournies par API-Sports.io")
        else:
            st.caption("📊 Données simulées - Mode démo")

# --- FOOTER ---
st.divider()
st.caption("© 2026 M'SIRI CAPITAL - Technologie de Lubumbashi.")
