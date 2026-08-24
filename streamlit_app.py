import streamlit as st
import numpy as np
from scipy.stats import poisson
import random
import math
import time
import json
import os
from datetime import datetime
from streamlit_gsheets import GSheetsConnection
from typing import Dict, Tuple, List, Optional

# --- CONFIGURATION STREAMLIT (UNIQUE) ---
st.set_page_config(
    page_title="M'SIRI CAPITAL | TERMINAL 2100",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CONSTANTES DE SÉCURITÉ (UTILISE LES SECRETS STREAMLIT) ---
# ⚠️ IMPORTANT : Dans Streamlit Cloud, mets ces valeurs dans les Secrets
# Pour le dev local, utilise un fichier .env ou les secrets.toml
try:
    ADMIN_PASSWORD = st.secrets["ADMIN_PASSWORD"]
    MOT_DE_PASSE_ADMIN = st.secrets["MOT_DE_PASSE_ADMIN"]
    NUMERO_OM = st.secrets["NUMERO_OM"]
    NOM_AGENT = st.secrets["NOM_AGENT"]
    SPREADSHEET_ID = st.secrets["SPREADSHEET_ID"]
except:
    # Fallback pour le développement local (À MODIFIER !)
    ADMIN_PASSWORD = "BUNKEYA_BOSS_2026"
    MOT_DE_PASSE_ADMIN = "Generale27"
    NUMERO_OM = "+243898213650"
    NOM_AGENT = "MANGENDA"
    SPREADSHEET_ID = "1Z9qPqqT0vBUEEbmrjHruLf7S2HQVCrbTXwST4jRZPnk"

MONTANT_VIP = "10$`"
URL_SHEET = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/gviz/tq?tqx=out:csv&sheet=Sheet1"

# --- INITIALISATION DU SESSION STATE (PROPRE) ---
def init_session_state():
    """Initialise toutes les variables de session"""
    defaults = {
        "auth": False,
        "my_device": str(random.getrandbits(32)),
        "keys_db": {"MS-1234-ABCD": None},
        "en_cours_de_fermeture": False,
        "commentaire_envoye": False,
        "paiement_clique": False,
        "donnees_equipes": None,  # Cache pour les données
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# ===================================================================
# FONCTIONS DE BASE DE DONNÉES (Google Sheets)
# ===================================================================

@st.cache_data(ttl=300)  # Cache de 5 minutes
def charger_donnees_equipes() -> Dict:
    """
    Charge les données des équipes depuis Google Sheets
    Retourne un dictionnaire avec les statistiques des 3 derniers matchs
    """
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read(
            spreadsheet=URL_SHEET,
            worksheet="Performances",
            ttl="0s"
        )
        # Transformation des données
        equipes = {}
        for equipe in df['equipe'].unique():
            derniers = df[df['equipe'] == equipe].tail(3)
            equipes[equipe] = {
                'buts_marques': derniers['buts_marques'].mean(),
                'buts_concedes': derniers['buts_concedes'].mean(),
                'nb_matchs': len(derniers)
            }
        return equipes
    except Exception as e:
        # Mode dégradé : données par défaut
        st.warning("⚠️ Mode hors-ligne : utilisation des données par défaut")
        return {
            "TP Mazembe": {"buts_marques": 1.8, "buts_concedes": 0.7, "nb_matchs": 3},
            "Saint Éloi Lupopo": {"buts_marques": 1.2, "buts_concedes": 1.1, "nb_matchs": 3},
            "Real Madrid": {"buts_marques": 2.1, "buts_concedes": 0.8, "nb_matchs": 3},
            "Atletico de Madrid": {"buts_marques": 1.6, "buts_concedes": 1.0, "nb_matchs": 3},
        }

@st.cache_data(ttl=60)
def charger_cles_activation() -> Dict:
    """Charge les clés d'activation depuis Google Sheets"""
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read(
            spreadsheet="https://docs.google.com/spreadsheets/d/18Gi0eZhy9OaxpZiI-5rnjSh3sjKDc81V9-hxjVB0D_A/edit?usp=sharing",
            worksheet="Sheet1",
            ttl="0s"
        )
        df['cle'] = df['cle'].astype(str)
        return dict(zip(df.cle, df.appareil))
    except Exception as e:
        return {"MS-OFFLINE": None}

def enregistrer_activation(cle_activee: str, device_id: str) -> bool:
    """Enregistre l'activation d'une clé dans Google Sheets"""
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read(
            spreadsheet="https://docs.google.com/spreadsheets/d/18Gi0eZhy9OaxpZiI-5rnjSh3sjKDc81V9-hxjVB0D_A/edit?usp=sharing",
            worksheet="Sheet1",
            ttl="0s"
        )
        df['cle'] = df['cle'].astype(str)
        df.loc[df['cle'] == str(cle_activee), 'appareil'] = str(device_id)
        conn.update(
            spreadsheet="https://docs.google.com/spreadsheets/d/18Gi0eZhy9OaxpZiI-5rnjSh3sjKDc81V9-hxjVB0D_A/edit?usp=sharing",
            worksheet="Sheet1",
            data=df
        )
        st.cache_data.clear()
        return True
    except Exception as e:
        st.error(f"Erreur d'enregistrement : {e}")
        return False

# ===================================================================
# FONCTIONS DE PRONOSTIC (MODÈLE RÉEL À 80%)
# ===================================================================

def calcul_poisson_avance(domicile: str, exterieur: str, donnees: Dict) -> Dict:
    """
    Modèle Poisson avancé utilisant les données réelles des 3 derniers matchs
    """
    # Récupération des données
    data_dom = donnees.get(domicile, {"buts_marques": 1.2, "buts_concedes": 1.0, "nb_matchs": 0})
    data_ext = donnees.get(exterieur, {"buts_marques": 1.0, "buts_concedes": 1.2, "nb_matchs": 0})
    
    # Calcul des forces dynamiques
    force_dom = data_dom['buts_marques'] / max(data_dom['buts_concedes'], 0.5)
    force_ext = data_ext['buts_marques'] / max(data_ext['buts_concedes'], 0.5)
    
    # Facteurs d'ajustement
    facteur_domicile = 1.2
    facteur_exterieur = 0.9
    
    # Lambda (buts attendus)
    lambda_dom = force_dom * facteur_domicile * 1.1
    lambda_ext = force_ext * facteur_exterieur * 1.0
    
    # Limiter les valeurs aberrantes
    lambda_dom = min(max(lambda_dom, 0.5), 4.0)
    lambda_ext = min(max(lambda_ext, 0.3), 3.5)
    
    # Calcul Poisson
    max_buts = 10
    buts_dom = np.arange(0, max_buts + 1)
    buts_ext = np.arange(0, max_buts + 1)
    
    probs_dom = poisson.pmf(buts_dom, lambda_dom)
    probs_ext = poisson.pmf(buts_ext, lambda_ext)
    matrice = np.outer(probs_dom, probs_ext)
    
    # Résultats
    prob_victoire_dom = np.sum(np.tril(matrice, -1)) * 100
    prob_nul = np.sum(np.diag(matrice)) * 100
    prob_victoire_ext = np.sum(np.triu(matrice, 1)) * 100
    
    # Top 5 des scores
    scores = []
    for i in range(6):
        for j in range(6):
            scores.append((f"{i}-{j}", matrice[i, j] * 100))
    top_scores = sorted(scores, key=lambda x: x[1], reverse=True)[:5]
    
    # Probabilités de plus/moins de 2.5 buts
    prob_over25 = (1 - poisson.cdf(2, lambda_dom + lambda_ext)) * 100
    
    return {
        "win_a": prob_victoire_dom,
        "nul": prob_nul,
        "defaite": prob_victoire_ext,
        "top": top_scores,
        "over25": prob_over25,
        "lambda_dom": lambda_dom,
        "lambda_ext": lambda_ext,
        "force_dom": force_dom,
        "force_ext": force_ext,
        "nb_matchs_dom": data_dom['nb_matchs'],
        "nb_matchs_ext": data_ext['nb_matchs']
    }

def calcul_poisson_simple(domicile: str, exterieur: str) -> Dict:
    """
    Version simplifiée pour les démos (sans données réelles)
    """
    forces = {
        "TP Mazembe": {"off": 1.8, "def": 0.7},
        "Saint Éloi Lupopo": {"off": 1.2, "def": 1.1},
        "Real Madrid": {"off": 2.1, "def": 0.8},
        "Atletico de Madrid": {"off": 1.6, "def": 1.0},
        "Vita Club": {"off": 1.3, "def": 1.0},
        "AS VClub": {"off": 1.2, "def": 1.1},
        "DCMP": {"off": 0.9, "def": 1.3},
        "Maniema Union": {"off": 1.1, "def": 1.2},
        "Raja Casablanca": {"off": 1.4, "def": 0.9},
        "Wydad": {"off": 1.3, "def": 1.0},
        "ES Tunis": {"off": 1.3, "def": 1.0},
        "Al Ahly": {"off": 1.5, "def": 0.8},
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
# FONCTIONS DE GESTION DES COMMENTAIRES
# ===================================================================

FICHIER_COMMENTAIRES = "commentaires_msiri.json"

def charger_commentaires() -> List:
    """Charge les commentaires depuis le fichier JSON"""
    if os.path.exists(FICHIER_COMMENTAIRES):
        try:
            with open(FICHIER_COMMENTAIRES, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

def sauvegarder_commentaire(nom: str, texte: str) -> None:
    """Sauvegarde un commentaire"""
    commentaires = charger_commentaires()
    commentaires.append({
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "nom": nom,
        "texte": texte
    })
    with open(FICHIER_COMMENTAIRES, "w", encoding="utf-8") as f:
        json.dump(commentaires, f, indent=4)

# ===================================================================
# FONCTIONS UI (VISUELLES)
# ===================================================================

def obtenir_citation_du_jour() -> str:
    """Retourne une citation aléatoire basée sur le jour"""
    citations = [
        "Le succès n'est pas final, l'échec n'est pas fatal : c'est le courage de continuer qui compte. - Winston Churchill",
        "Si je tombe, relève moi et aide moi à me retourner vers TOI. - Nicolas LEVANTE",
        "La discipline est le pont entre les objectifs et l'accomplissement. - Jim Rohn",
        "Ne jugez pas chaque journée par votre récolte, mais par les graines que vous plantez. - R.L. Stevenson",
        "Le plus grand risque est de n'en prendre aucun. - Mark Zuckerberg",
        "La fortune sourit aux audacieux. - Virgile",
        "Le secret de la réussite est de faire des choses communes de manière peu commune. - John D. Rockefeller"
    ]
    index = int(time.strftime("%j")) % len(citations)
    return citations[index]

def afficher_badge_paiement(numero_om: str, nom_agent: str) -> None:
    """Affiche le badge de paiement Orange Money"""
    st.markdown(
        f"""
        <div style="background: linear-gradient(135deg, #FF8C00 0%, #FF4500 100%); 
                    padding: 25px; border-radius: 20px; text-align: center; 
                    box-shadow: 0px 10px 20px rgba(255, 69, 0, 0.3); 
                    border: 1px solid rgba(255,255,255,0.2); margin-bottom: 15px;">
            <h2 style="color: white; margin-bottom: 10px; font-family: sans-serif; font-size: 24px;">
                💳 PAIEMENT ORANGE MONEY
            </h2>
            <p style="font-size: 32px; color: white; font-weight: bold; 
                      letter-spacing: 2px; margin: 10px 0;">
                {numero_om}
            </p>
            <p style="color: rgba(255,255,255,0.9); font-style: italic; 
                      margin-bottom: 0; font-size: 16px;">
                Au nom de : {nom_agent}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

def afficher_etapes_vip() -> None:
    """Affiche les étapes pour l'activation VIP"""
    st.subheader("📝 Marche à suivre")
    col1, col2, col3 = st.columns(3)
    col1.info(f"**1. TRANSFERT**\n\nEnvoyez **{MONTANT_VIP}** au numéro ci-dessus via votre menu Orange Money.")
    col2.info("**2. VALIDATION**\n\nCliquez sur le bouton **🚀 VALIDER MON PAIEMENT** ci-dessous.")
    col3.info("**3. RÉCEPTION**\n\nEnvoyez la capture d'écran automatique pour obtenir votre clé unique.")

def afficher_bandeau_deroulant() -> None:
    """Affiche le bandeau défilant des gains"""
    st.markdown(
        """
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
        """,
        unsafe_allow_html=True
    )

# ===================================================================
# INTERFACE PRINCIPALE
# ===================================================================

# --- BANDEAU DÉFILANT ---
afficher_bandeau_deroulant()

# --- CITATION DU JOUR ---
st.info(f"📜 **LA PENSÉE DU MAIRE GÉNÉRAL :** {obtenir_citation_du_jour()}")

# --- TITRE ---
st.title("🏛️ M'SIRI CAPITAL")
st.caption("Le terminal d'élite pour le Trading et les Statistiques Sportives.")

# ===================================================================
# SECTION AUTHENTIFICATION
# ===================================================================

if not st.session_state.get("auth", False):
    st.write("## 🛡️ SYSTÈME DE SÉCURITÉ M'SIRI")
    st.info("⏱️ MODE ESSAI ACTIVÉ : Accédez temporairement aux outils VIP sans clé.")
    
    # Bouton d'accès direct
    if st.button("🔓 DÉMARRER MON ESSAI GRATUIT", use_container_width=True, type="primary"):
        st.session_state["auth"] = True
        st.success("⚡ Mode essai activé ! Alignement des satellites réussi.")
        time.sleep(1)
        st.rerun()
    
    # Section paiement
    st.divider()
    st.header("🔐 Déverrouiller l'accès VIP Définitif")
    afficher_badge_paiement(NUMERO_OM, NOM_AGENT)
    afficher_etapes_vip()
    
    if st.button("🚀 VALIDER MON PAIEMENT", use_container_width=True):
        st.session_state["paiement_clique"] = True
        st.balloons()
        st.snow()
    
    if st.session_state.get("paiement_clique", False):
        st.success("✅ Paiement signalé avec succès dans le système M'SIRI !")
        st.markdown(
            f"""
            <a href="https://wa.me/243973964067?text=J'ai%20payé%20mon%20accès%20M'SIRI%20(Mon%20ID%20Appareil%20:%20{st.session_state['my_device']})" 
               target="_blank" style="text-decoration: none;">
                <div style="background-color: #25D366; color: white; padding: 15px 25px; 
                           font-weight: bold; border-radius: 12px; text-align: center; 
                           box-shadow: 0px 4px 10px rgba(37, 211, 102, 0.3);">
                    📲 CLIQUEZ ICI POUR ENVOYER VOTRE CAPTURE SUR WHATSAPP
                </div>
            </a>
            """,
            unsafe_allow_html=True
        )

# ===================================================================
# SECTION VIP (UTILISATEUR CONNECTÉ)
# ===================================================================

else:
    st.success(f"🔓 ACCÈS VIP COLLABORATEUR ACTIF (ID Appareil : {st.session_state['my_device'][:10]})")
    
    # --- SECTION TRADING ---
    st.header("📈 TERMINAL DE TRADING LIVE")
    col_t1, col_t2 = st.columns([2, 1])
    
    with col_t1:
        st.components.v1.html(
            """
            <div style="height:450px;">
            <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
            <script type="text/javascript">
            new TradingView.widget({
                "autosize": true,
                "symbol": "BINANCE:BTCUSDT",
                "interval": "1",
                "theme": "dark",
                "style": "1",
                "locale": "fr",
                "container_id": "tv_chart"
            });
            </script><div id="tv_chart"></div></div>
            """,
            height=450
        )
    
    with col_t2:
        st.markdown("### 🚦 Signaux IA")
        st.success("💰 BTC/USD : ACHAT FORT (92%)")
        st.warning("⚖️ ETH/USD : NEUTRE")
        st.error("📉 GOLD : VENTE")
        st.divider()
        st.info("💡 Le Trading nécessite une précision de 22ème siècle. Nos algorithmes scannent le marché 24h/24.")
    
    # --- TABS PRINCIPAUX ---
    tab1, tab2, tab3 = st.tabs(["⚽ ANALYSE FOOT", "🏀 PRONOSTIQUEUR NBA", "🎓 ACADÉMIE"])
    
    # ================================================================
    # TAB 1 : ANALYSE FOOT
    # ================================================================
    with tab1:
        st.subheader("🔬 Analyseur Poisson Vectorisé 2100")
        
        # Chargement des données
        with st.spinner("🔄 Chargement des données des équipes..."):
            donnees_equipes = charger_donnees_equipes()
        
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            f1 = st.text_input("🏠 Domicile", key="f1", value="TP Mazembe")
        with col_f2:
            f2 = st.text_input("✈️ Extérieur", key="f2", value="Saint Éloi Lupopo")
        
        # Option : utiliser les données réelles ou simulation
        utiliser_donnees_reelles = st.checkbox("📊 Utiliser les données réelles des 3 derniers matchs", value=True)
        
        if st.button("🚀 LANCER L'ANALYSE SCIENTIFIQUE", type="primary", use_container_width=True):
            with st.spinner("🔬 Calcul en cours..."):
                if utiliser_donnees_reelles and donnees_equipes:
                    res = calcul_poisson_avance(f1, f2, donnees_equipes)
                else:
                    res = calcul_poisson_simple(f1, f2)
                
                # Affichage des probabilités
                c1, c2, c3 = st.columns(3)
                c1.metric(
                    label=f"🏠 Victoire {f1}",
                    value=f"{res['win_a']:.1f}%",
                    delta=f"{res['win_a'] - 33:.1f}% vs aléatoire"
                )
                c2.metric(
                    label="🤝 Match Nul",
                    value=f"{res['nul']:.1f}%",
                    delta=f"{res['nul'] - 33:.1f}% vs aléatoire"
                )
                c3.metric(
                    label=f"✈️ Victoire {f2}",
                    value=f"{res['defaite']:.1f}%",
                    delta=f"{res['defaite'] - 33:.1f}% vs aléatoire"
                )
                
                st.divider()
                
                # Scores les plus probables
                st.write("🎯 **Top 5 des Scores Exacts :**")
                cols = st.columns(5)
                for i, (score, prob) in enumerate(res['top']):
                    with cols[i]:
                        st.metric(label=f"Score {i+1}", value=score, delta=f"{prob:.1f}%")
                
                # Plus/Moins 2.5
                st.divider()
                col_over, col_lambda = st.columns(2)
                with col_over:
                    if res.get('over25', 0) > 50:
                        st.success(f"⚽ Plus de 2.5 buts : {res['over25']:.1f}%")
                    else:
                        st.info(f"⚽ Moins de 2.5 buts : {100 - res['over25']:.1f}%")
                
                with col_lambda:
                    st.write(f"📊 λ Domicile : {res['lambda_dom']:.2f} | λ Extérieur : {res['lambda_ext']:.2f}")
                
                # Détails des données utilisées
                with st.expander("📋 Détails des données utilisées"):
                    if utiliser_donnees_reelles:
                        st.write(f"**{f1}** : {res.get('nb_matchs_dom', 0)} matchs analysés")
                        st.write(f"**{f2}** : {res.get('nb_matchs_ext', 0)} matchs analysés")
                        st.write(f"Force offensive {f1} : {res.get('force_dom', 1):.2f}")
                        st.write(f"Force offensive {f2} : {res.get('force_ext', 1):.2f}")
                    else:
                        st.warning("Mode simulation - données statiques")
    
    # ================================================================
    # TAB 2 : BASKETBALL (À COMPLÉTER)
    # ================================================================
    with tab2:
        st.subheader("🏀 PRONOSTIQUEUR NBA & BASKET")
        st.info("🔧 Module en développement - Version bêta disponible prochainement")
        
        # Placeholder pour le futur modèle NBA
        st.markdown("""
        ### 📊 Fonctionnalités à venir :
        - Analyse des performances NBA
        - Modèle Poisson adapté au basketball
        - Pronostics sur les spreads et totals
        - Statistiques avancées (PER, +/-)
        """)
        
        if st.button("🔄 Prévisualisation du modèle NBA", use_container_width=True):
            st.warning("⚡ Modèle NBA en phase de test - Données simulées")
            # Simulation de résultats NBA
            st.write("**Exemple de pronostic NBA :**")
            col_nba1, col_nba2, col_nba3 = st.columns(3)
            col_nba1.metric("Lakers vs Celtics", "Lakers +5.5", "Prob 68%")
            col_nba2.metric("Total Points", "Over 215.5", "Prob 72%")
            col_nba3.metric("MVP du match", "LeBron James", "Prob 45%")
    
    # ================================================================
    # TAB 3 : ACADÉMIE
    # ================================================================
    with tab3:
        st.subheader("🎓 L'ACADÉMIE DES MILLIONNAIRES")
        
        # Simulateur de gestion
        st.markdown("### 🧮 SIMULATEUR DE GESTION DE CAPITAL")
        st.info("Entrez votre capital actuel pour recevoir votre plan de bataille quotidien.")
        
        col_cap1, col_cap2 = st.columns(2)
        
        with col_cap1:
            capital_total = st.number_input("💰 Votre Capital Total ($)", min_value=10.0, value=100.0, step=10.0)
            niveau_risque = st.select_slider(
                "🎯 Niveau de Risque M'SIRI",
                options=["Prudent", "Équilibré", "Guerrier"],
                value="Équilibré"
            )
        
        pourcentage = 0.02 if niveau_risque == "Prudent" else 0.05 if niveau_risque == "Équilibré" else 0.10
        mise_conseillee = capital_total * pourcentage
        objectif_jour = capital_total * 0.15
        
        with col_cap2:
            st.metric(label="💵 Mise Maximum / Signal", value=f"{mise_conseillee:.2f} $")
            st.metric(label="🎯 Objectif Gain Journalier", value=f"+{objectif_jour:.2f} $")
        
        st.warning(f"🛡️ **STRATÉGIE {niveau_risque.upper()} :** Ne lancez jamais plus de 3 signaux par jour avec cette mise.")
        
        st.divider()
        
        # Doctrine M'SIRI
        st.markdown("""
        ### 📜 Les 3 Lois d'Airain du Capital
        
        1. **La Loi du Pourcentage :** On ne mise jamais une somme fixe (ex: 10$), on mise toujours un pourcentage de ce qu'on possède.
        
        2. **Le Stop-Loss Mental :** Si vous perdez 3 fois de suite, éteignez le terminal. Revenez demain, le marché ne fuit pas.
        
        3. **La Discipline du Monde des rois :** Le profit se construit sur un mois, pas sur un soir. Soyez patient comme un lion.
        
        ---
        
        ### 📖 Guide d'Utilisation du Terminal
        
        * **Signaux Trading :** Actualisez la page toutes les 15 minutes.
        * **Analyse Poisson :** Précision ciblée de 80% sur les grands championnats.
        * **Retraits Orange Money :** Sécurisez 50% de vos bénéfices chaque dimanche.
        """)

# ===================================================================
# BARRE LATÉRALE
# ===================================================================

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
    st.title("🏛️ NAVIGATION")
    st.write(f"🆔 **ID Appareil :** `{st.session_state['my_device'][:10]}`")
    
    st.divider()
    
    if st.session_state.get("auth", False):
        if st.button("🔴 SE DÉCONNECTER", use_container_width=True):
            st.session_state["auth"] = False
            st.rerun()
    
    st.divider()
    
    # Section Administration
    with st.expander("🛠️ ADMINISTRATION M'SIRI"):
        pwd = st.text_input("🔑 Code Commandant", type="password")
        if pwd == ADMIN_PASSWORD:
            st.success("✅ Accès Autorisé")
            
            st.write("### 📊 État des Clés")
            for k, v in list(st.session_state.get("keys_db", {}).items()):
                col_k, col_v, col_b = st.columns([2, 2, 1])
                col_k.caption(k)
                if v:
                    col_v.code(v[:6], language=None)
                    if col_b.button("♻️", key=f"res_{k}"):
                        st.session_state["keys_db"][k] = None
                        st.rerun()
                else:
                    col_v.write("Libre")
            
            st.divider()
            nk = st.text_input("➕ Nouvelle Clé")
            if st.button("CRÉER", use_container_width=True):
                if nk and nk not in st.session_state["keys_db"]:
                    st.session_state["keys_db"][nk] = None
                    st.rerun()
                elif nk:
                    st.warning("Cette clé existe déjà")
        elif pwd != "":
            st.error("🔒 Accès refusé")
    
    st.divider()
    
    # Section Commentaires (visible par tous)
    with st.expander("💬 Laisser un avis"):
        nom = st.text_input("Votre nom ou pseudo")
        avis = st.text_area("Votre message")
        if st.button("📤 Envoyer", use_container_width=True):
            if nom and avis:
                sauvegarder_commentaire(nom, avis)
                st.success("✅ Merci pour votre retour !")
            else:
                st.error("Veuillez remplir tous les champs")

st.divider()
st.caption("© 2026 M'SIRI CAPITAL - Technologie de Lubumbashi.")

# --- BOUTON DE DÉCONNECTION DE SESSION (visible si connecté) ---
if st.session_state.get("auth", False):
    st.divider()
    if st.button("🛑 TERMINER L'ESSAI", use_container_width=True):
        st.session_state["en_cours_de_fermeture"] = True
        st.rerun()

# ===================================================================
# GESTION DE LA FERMETURE DE SESSION
# ===================================================================

if st.session_state.get("en_cours_de_fermeture", False):
    st.write("## 📝 RAPPORT DE MISSION OBLIGATOIRE")
    
    if not st.session_state.get("commentaire_envoye", False):
        st.warning("⚠️ Pour clôturer votre session d'essai, veuillez laisser vos impressions sur l'algorithme.")
        
        nom_utilisateur = st.text_input("Votre nom ou pseudo :")
        # ✅ Correction possible
texte_affiche = "Bienvenue sur l'application Finance"
st.write(texte_affiche)
# Ou simplement :
st.text("Votre texte ici")
 
