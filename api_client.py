# app.py - Code complet avec intégration API-Sports.io

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats, optimize
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import json
import os
from typing import Dict, List, Optional, Tuple, Any
import warnings
warnings.filterwarnings('ignore')

# ===================================================================
# IMPORTS POUR L'API-SPORTS.IO
# ===================================================================

from api_client import APISportsClient
import os

# Récupération de la clé API
try:
    API_SPORTS_KEY = st.secrets["API_SPORTS_KEY"]
except:
    # Fallback pour dev local
    API_SPORTS_KEY = os.getenv("API_SPORTS_KEY", "votre_cle_api_ici")
    if API_SPORTS_KEY == "votre_cle_api_ici":
        st.warning("⚠️ API-Sports Key non configurée. Utilisation des données simulées.")
        API_SPORTS_KEY = None

# Initialisation du client
api_client = APISportsClient(API_SPORTS_KEY) if API_SPORTS_KEY else None

# ===================================================================
# FONCTIONS DE BASE POUR LES PRONOSTICS
# ===================================================================

# --- Import des fonctions de base (simulées) ---
def get_simulated_data(nom_equipe: str) -> Dict:
    """Données simulées pour le mode hors-ligne"""
    # ... (votre code existant)
    pass

def generer_conseils(perf_dom: Dict, perf_ext: Dict, win_dom: float, win_ext: float, over25: float) -> List[str]:
    """Génère des conseils basés sur les statistiques"""
    # ... (votre code existant)
    pass

def pronostic_final(win_dom: float, win_ext: float, over25: float, top_scores: List) -> str:
    """Génère le pronostic final"""
    # ... (votre code existant)
    pass

# ===================================================================
# NOUVELLES FONCTIONS DE RECHERCHE AVEC API-SPORTS
# ===================================================================

def rechercher_equipe(api_client: APISportsClient, nom_equipe: str, league_id: int = None) -> Dict:
    """
    Recherche une équipe et récupère ses statistiques complètes
    via API-Sports.io
    """
    if not api_client:
        return get_simulated_data(nom_equipe)
    
    # 1. Récupérer l'ID de l'équipe
    team_id = api_client.get_team_id(nom_equipe, league_id)
    if not team_id:
        st.warning(f"⚠️ Équipe '{nom_equipe}' non trouvée. Utilisation des données simulées.")
        return get_simulated_data(nom_equipe)
    
    # 2. Récupérer les 3 derniers matchs
    fixtures = api_client.get_fixtures_by_team(team_id, last_n=3)
    
    # 3. Récupérer les statistiques de saison
    stats = api_client.get_team_stats(team_id, season=2024)
    
    # 4. Construire les performances
    performances = {
        'nom': nom_equipe,
        'id': team_id,
        'nb_matchs': stats['played'],
        'victoires': stats['wins'],
        'nuls': stats['draws'],
        'defaites': stats['losses'],
        'buts_marques': stats['goals_for'],
        'buts_concedes': stats['goals_against'],
        'force_off': round(stats['avg_goals_for'], 2),
        'force_def': round(stats['avg_goals_against'], 2),
        'forme': round(stats['win_rate'], 1),
        'tendance': stats['form'],
        'matchs': fixtures,
        'moyenne_buts_marques': round(stats['avg_goals_for'], 2),
        'moyenne_buts_concedes': round(stats['avg_goals_against'], 2),
        'clean_sheets': stats['clean_sheets'],
        'source': 'API-Sports.io'
    }
    
    return performances

def analyser_match_api(equipe_dom: str, equipe_ext: str, league_id: int = None) -> Dict:
    """
    Analyse complète d'un match avec données API-Sports.io
    """
    if not api_client:
        st.warning("⚠️ Mode hors-ligne - Utilisation des données simulées")
        return analyser_match(equipe_dom, equipe_ext)
    
    # Récupérer les performances
    perf_dom = rechercher_equipe(api_client, equipe_dom, league_id)
    perf_ext = rechercher_equipe(api_client, equipe_ext, league_id)
    
    # Vérifier que les données sont réelles
    if 'source' not in perf_dom or 'source' not in perf_ext:
        return analyser_match(equipe_dom, equipe_ext)
    
    # Facteur domicile
    facteur_dom = 1.25
    
    # Calcul des lambdas
    lambda_dom = perf_dom['force_off'] * facteur_dom
    lambda_ext = perf_ext['force_off'] * 0.9
    
    lambda_dom = max(0.3, min(5.0, lambda_dom))
    lambda_ext = max(0.3, min(4.5, lambda_ext))
    
    # Calcul Poisson
    max_buts = 10
    probs_dom = poisson.pmf(np.arange(0, max_buts+1), lambda_dom)
    probs_ext = poisson.pmf(np.arange(0, max_buts+1), lambda_ext)
    matrice = np.outer(probs_dom, probs_ext)
    
    win_dom = np.sum(np.tril(matrice, -1)) * 100
    nul = np.sum(np.diag(matrice)) * 100
    win_ext = np.sum(np.triu(matrice, 1)) * 100
    
    # Scores les plus probables
    scores = []
    for i in range(6):
        for j in range(6):
            scores.append((f"{i}-{j}", matrice[i, j] * 100))
    top_scores = sorted(scores, key=lambda x: x[1], reverse=True)[:5]
    
    # Plus/Moins 2.5
    over25 = (1 - poisson.cdf(2, lambda_dom + lambda_ext)) * 100
    
    # Générer les conseils enrichis
    conseils = generer_conseils(perf_dom, perf_ext, win_dom, win_ext, over25)
    conseils.append(f"📊 Source des données : API-Sports.io (saison 2024)")
    conseils.append(f"🏟️ {perf_dom['nom']} - Clean sheets: {perf_dom['clean_sheets']}")
    
    return {
        'domicile': {
            'nom': equipe_dom,
            'perf': perf_dom,
            'lambda': lambda_dom
        },
        'exterieur': {
            'nom': equipe_ext,
            'perf': perf_ext,
            'lambda': lambda_ext
        },
        'probabilites': {
            'victoire_dom': win_dom,
            'nul': nul,
            'victoire_ext': win_ext
        },
        'scores': top_scores,
        'over25': over25,
        'conseils': conseils,
        'pronostic_final': pronostic_final(win_dom, win_ext, over25, top_scores),
        'source': 'API-Sports.io'
    }

# ===================================================================
# INTERFACE STREAMLIT
# ===================================================================

st.set_page_config(
    page_title="Prédictions Matchs de Foot",
    page_icon="⚽",
    layout="wide"
)

# --- CSS personnalisé ---
# ... (votre CSS existant)

# --- HEADER ---
# ... (votre header existant)

# --- SIDEBAR ---
# ... (votre sidebar existant)

# ===================================================================
# ZONE PRINCIPALE - AVANT LES PRONOSTICS
# ===================================================================

st.markdown("""
    <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #1a1a2e, #16213e); border-radius: 15px; margin-bottom: 30px;'>
        <h1 style='color: #FFD700;'>⚽ Système de Prédiction Football</h1>
        <p style='color: #E0E0E0;'>Analyse avancée basée sur le modèle de Poisson et données API-Sports.io</p>
    </div>
""", unsafe_allow_html=True)

# Colonnes de sélection
col1, col2, col3 = st.columns([2, 2, 1])

with col1:
    equipe_dom = st.text_input("🏠 Équipe Domicile", value="Paris Saint-Germain", placeholder="Entrez le nom de l'équipe")

with col2:
    equipe_ext = st.text_input("✈️ Équipe Extérieure", value="Olympique Lyonnais", placeholder="Entrez le nom de l'équipe")

with col3:
    st.write("")
    st.write("")
    analyser_btn = st.button("🔮 Analyser", type="primary", use_container_width=True)

# Indicateur de l'état de l'API
if api_client:
    st.sidebar.success("✅ API-Sports.io connectée")
else:
    st.sidebar.warning("⚠️ API-Sports.io non configurée - Mode hors-ligne")

# --- SI ANALYSE DEMANDÉE ---
if analyser_btn and equipe_dom and equipe_ext:
    with st.spinner("🔄 Analyse en cours..."):
        # Utiliser l'API si disponible
        if api_client:
            resultats = analyser_match_api(equipe_dom, equipe_ext)
        else:
            # Fallback vers l'analyse simulée
            resultats = analyser_match(equipe_dom, equipe_ext)
        
        # ===================================================================
        # PRONOSTICS - AFFICHAGE DES RÉSULTATS
        # ===================================================================
        
        # --- MÉTRIQUES PRINCIPALES ---
        # ... (votre code d'affichage existant)
        
        # --- PROBABILITÉS ET SCORES ---
        # ... (votre code d'affichage existant)
        
        # --- CONSEILS ---
        # ... (votre code d'affichage existant)

    # --- FOOTER ---
    # ... (votre footer existant)

# ===================================================================
# LANCEMENT DE L'APPLICATION
# ===================================================================

if __name__ == "__main__":
    # La fonction main est déjà gérée par Streamlit
    pass
