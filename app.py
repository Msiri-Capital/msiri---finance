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
    st.error("❌ Fichier utils.py manquant !")
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
# FONCTIONS DE PRONOSTIC (SIMPLIFIÉES POUR LE TEST)
# ===================================================================

def calcul_poisson_simple(domicile, exterieur):
    """Version simplifiée pour le test"""
    forces = {
        "Real Madrid": {"off": 2.1, "def": 0.8},
        "Real Sociedad": {"off": 1.6, "def": 1.0},
        "TP Mazembe": {"off": 1.8, "def": 0.7},
        "Saint Éloi Lupopo": {"off": 1.2, "def": 1.1},
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

st.title("🏛️ M'SIRI CAPITAL")
st.caption("Le terminal d'élite pour le Trading et les Statistiques Sportives.")

# --- CITATION ---
st.info(f"📜 {obtenir_citation_du_jour()}")

# --- SECTION PRINCIPALE ---
st.subheader("⚽ ANALYSE FOOT")
col1, col2 = st.columns(2)

with col1:
    domicile = st.text_input("🏠 Domicile", value="Real Madrid")
with col2:
    exterieur = st.text_input("✈️ Extérieur", value="Real Sociedad")

if st.button("🚀 ANALYSER", type="primary"):
    with st.spinner("🔬 Calcul en cours..."):
        res = calcul_poisson_simple(domicile, exterieur)
        
        col_p1, col_p2, col_p3 = st.columns(3)
        col_p1.metric(f"Victoire {domicile}", f"{res['win_a']:.1f}%")
        col_p2.metric("Match Nul", f"{res['nul']:.1f}%")
        col_p3.metric(f"Victoire {exterieur}", f"{res['defaite']:.1f}%")
        
        st.divider()
        st.write("🎯 Scores les plus probables:")
        for score, prob in res['top']:
            st.write(f"• **{score}** → {prob:.1f}%")

# --- FOOTER ---
st.divider()
st.caption("© 2026 M'SIRI CAPITAL - Technologie de Lubumbashi.")
