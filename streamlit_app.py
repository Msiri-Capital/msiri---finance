import streamlit as st
import random
import math
import time
import numpy as np
from streamlit_gsheets import GSheetsConnection
# --- 1. CONFIGURATION (DOIT ÊTRE EN PREMIER) ---
st.set_page_config(page_title="M'SIRI CAPITAL | TERMINAL 2100", layout="wide", initial_sidebar_state="collapsed")
# --- SÉCURITÉ ADMIN ---
ADMIN_PASSWORD = "BUNKEYA_BOSS_2026" # Change ce mot de passe !
# --- 2. INITIALISATION DU SYSTÈME (LA CORRECTION ICI) ---
if "auth" not in st.session_state:
    st.session_state["auth"] = False

if "my_device" not in st.session_state:
    # Génère un identifiant unique pour le téléphone/tablette
    st.session_state["my_device"] = str(random.getrandbits(32))
def obtenir_citation_du_jour():
    citations = [
        "Le succès n'est pas final, l'échec n'est pas fatal : c'est le courage de continuer qui compte. - Winston Churchill",
        "si je tombe, relève moi et aide moi à me retourner vers TOI. - Nicolas LEVANTE",
        "La discipline est le pont entre les objectifs et l'accomplissement. - Jim Rohn",
        "Ne jugez pas chaque journée par votre récolte, mais par les graines que vous plantez. - R.L. Stevenson",
        "Le plus grand risque est de n'en prendre aucun. - Mark Zuckerberg",
        "La fortune sourit aux audacieux. - Virgile",
        "Le secret de la réussite est de faire des choses communes de manière peu commune. - John D. Rockefeller"
    ]
    # Utilise le jour de l'année pour changer la citation
    index = int(time.strftime("%j")) % len(citations)
    return citations[index]
# APRES LA FONCTION, REVIENS BIEN AU BORD POUR LA SUITE DU CODE
# --- 3. CONNEXION À LA BASE DE DONNÉES GOOGLE ---
conn = st.connection("gsheets", type=GSheetsConnection)
def enregistrer_activation(cle_activee, device_id):
    url = "https://docs.google.com/spreadsheets/d/18Gi0eZhy9OaxpZiI-5rnjSh3sjKDc81V9-hxjVB0D_A/edit?usp=sharing"
    
    try:
        # 1. On lit tout le tableau
        df = conn.read(spreadsheet=url, worksheet="Sheet1", ttl="0s")
        
        # 2. On s'assure que tout est traité comme du texte pour éviter les bugs de format
        df['cle'] = df['cle'].astype(str)
        
        # 3. On fait la modification
        df.loc[df['cle'] == str(cle_activee), 'appareil'] = str(device_id)
        
        # 4. On renvoie UNIQUEMENT les données propres
        conn.update(spreadsheet=url, worksheet="Sheet1", data=df)
        
        st.cache_data.clear()
        return True
    except Exception as e:
        st.error(f"Erreur 400 ou technique : {e}")
        return False
        
def charger_cles_google():
    url = "https://docs.google.com/spreadsheets/d/18Gi0eZhy9OaxpZiI-5rnjSh3sjKDc81V9-hxjVB0D_A/edit?usp=sharing"

    try:
        df = conn.read(spreadsheet=url, worksheet="Sheet1", ttl="0s")
        return dict(zip(df.cle, df.appareil))
    except Exception as e:
        return {"MS-OFFLINE": None}
    
# --- 1. CONFIGURATION ET CONSTANTES (TOUT EN HAUT) ---
st.set_page_config(
    page_title="M'SIRI CAPITAL | TERMINAL 2100", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

MONTANT_VIP = "10$`"
NUMERO_OM = "+243898213650"  # Ton numéro Orange Money
NOM_AGENT = "MANGENDA"       # Le nom de l'agent de validation
SPREADSHEET_ID = "1Z9qPqqT0vBUEEbmrjHruLf7S2HQVCrbTXwST4jRZPnk"
URL_SHEET = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/gviz/tq?tqx=out:csv&sheet=Sheet1"

# --- 2. INITIALISATION DU SESSION STATE ---
if "auth" not in st.session_state:
    st.session_state["auth"] = False

if "my_device" not in st.session_state:
    st.session_state["my_device"] = str(random.getrandbits(32))

if "keys_db" not in st.session_state:
    st.session_state["keys_db"] = {"MS-1234-ABCD": None}  # Simulation locale

# --- 3. FONCTIONS TECHNIQUES ET LOGIQUES ---
def obtenir_citation_du_jour():
    return "La discipline est le pont entre les objectifs et l'accomplissement. - Jim Rohn"

def calcul_poisson_msiri(eq1, eq2):
    l1, l2 = random.uniform(1.1, 2.9), random.uniform(0.7, 1.9)
    def p(k, lamb): return (math.exp(-lamb) * (lamb**k)) / math.factorial(k)
    prob_a = sum(p(i, l1)*p(j, l2) for i in range(6) for j in range(i))
    scores = sorted([(f"{i}-{j}", p(i,l1)*p(j,l2)) for i in range(4) for j in range(4)], key=lambda x: x[1], reverse=True)
    return {"win_a": prob_a*100, "top": scores[:3], "over25": (1-p(0,l1+l2)-p(1,l1+l2)-p(2,l1+l2))*100}

def enregistrer_activation(cle, device):
    if "keys_db" in st.session_state:
        st.session_state["keys_db"][cle] = device
    return True

# --- 4. FONCTIONS VISUELLES VIP ---
def afficher_badge_paiement(numero_om, nom_agent):
    st.markdown(
        f"""
        <div style="background: linear-gradient(135deg, #FF8C00 0%, #FF4500 100%); padding: 25px; border-radius: 20px; text-align: center; box-shadow: 0px 10px 20px rgba(255, 69, 0, 0.3); border: 1px solid rgba(255,255,255,0.2); margin-bottom: 15px;">
            <h2 style="color: white; margin-bottom: 10px; font-family: sans-serif; font-size: 24px;">💳 PAIEMENT ORANGE MONEY</h2>
            <p style="font-size: 32px; color: white; font-weight: bold; letter-spacing: 2px; margin: 10px 0;">{numero_om}</p>
            <p style="color: rgba(255,255,255,0.9); font-style: italic; margin-bottom: 0; font-size: 16px;">Au nom de : {nom_agent}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

def afficher_etapes_vip():
    st.subheader("📝 Marche à suivre")
    col1, col2, col3 = st.columns(3)
    col1.info(f"**1. TRANSFERT**\n\nEnvoyez **{MONTANT_VIP}** au numéro ci-dessus via votre menu Orange Money.")
    col2.info("**2. VALIDATION**\n\nCliquez sur le bouton **🚀 VALIDER MON PAIEMENT** ci-dessous.")
    col3.info("**3. RÉCEPTION**\n\nEnvoyez la capture d’écran automatique pour obtenir votre clé unique.")

def afficher_section_vip(numero_om, nom_agent):
    st.divider()
    st.header("🔐 Déverrouiller l'accès VIP")
    afficher_badge_paiement(numero_om, nom_agent)
    afficher_etapes_vip()

    st.write("")
    if "paiement_clique" not in st.session_state:
        st.session_state["paiement_clique"] = False

    if st.button("🚀 VALIDER MON PAIEMENT", use_container_width=True):
        st.session_state["paiement_clique"] = True

    if st.session_state["paiement_clique"]:
        st.success("✅ Paiement signalé avec succès dans le système M'SIRI !")
        st.markdown(
            f"""<a href="https://wa.me/243973964067?text=J'ai%20payé%20mon%20accès%20M'SIRI%20(Mon%20ID%20Appareil%20:%20{st.session_state['my_device']})" target="_blank">
                <button style="background-color: #25D366; color: white; border: none; padding: 15px 25px; font-weight: bold; border-radius: 12px; cursor: pointer; width: 100%; font-size: 16px; box-shadow: 0px 4px 10px rgba(37, 211, 102, 0.3);">
                    📲 CLIQUEZ ICI POUR ENVOYER VOTRE CAPTURE SUR WHATSAPP
                </button>
            </a>""", 
            unsafe_allow_html=True
        )

# ====================================================================================
# --- 5. INTERFACE GRAPHIQUE VISUELLE ---
# ====================================================================================

# BANDEAU DÉFILANT (Gains en temps réel)
st.markdown("""<marquee style="color: #00ff00; background: #001a00; padding: 5px; font-weight: bold;">
🟢 Gaston M. +450`$ (BTC/USD) | 🟢 Membre #22 +120$` (NBA) | 🟢 Justin K. +85`$ (Mazembe vs Lupopo) | 🟢 Signal IA validé : ETH +4.2%
</marquee>""", unsafe_allow_html=True)

# --- AFFICHAGE CITATION DU JOUR ---
st.info(f"📜 **LA PENSÉE DU MAIRE GÉNÉRAL :** {obtenir_citation_du_jour()}")

# --- TITRE LUXE ---
st.title("🏛️ M'SIRI CAPITAL")
st.caption("Le terminal d'élite pour le Trading et les Statistiques Sportives.")

# --- SECTION 1 : TRADING (LA VITRINE RESTAURÉE) ---
st.header("📈 TERMINAL DE TRADING LIVE")

# Correction de la coupure : Création propre des deux colonnes
col_t1, col_t2 = st.columns([2, 1])

with col_t1:
    # Réinjection sécurisée du widget TradingView
    st.components.v1.html("""
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
    """, height=450)

with col_t2:
    st.markdown("### 🚦 Signaux IA")
    st.success("💰 BTC/USD : ACHAT FORT (92%)")
    st.warning("⚖️ ETH/USD : NEUTRE")
    st.error("📉 GOLD : VENTE")
    st.divider()
    st.info("💡 Le Trading nécessite une précision de 22ème siècle. Nos algorithmes scannent le marché 24h/24.")

# ====================================================================================
# --- 6. LOGIQUE DE SÉCURITÉ & EFFETS SPÉCIAUX M'SIRI ---
# ====================================================================================

# CAS A : L'UTILISATEUR N'EST PAS ENCORE CONNECTÉ
if not st.session_state.get("auth", False):
    st.write("## 🛡️ SYSTÈME DE SÉCURITÉ M'SIRI")
    
    # 1. EN PREMIER : Instructions et Badge de Paiement Orange Money
    st.header("🔐 Déverrouiller l'accès VIP")
    afficher_badge_paiement(NUMERO_OM, NOM_AGENT)
    afficher_etapes_vip()
    st.write("")

    # Gestion de la mémoire du clic de paiement
    if "paiement_clique" not in st.session_state:
        st.session_state["paiement_clique"] = False

    # BOUTON VALIDER LE PAIEMENT AVEC EFFETS SPÉCIAUX !
    if st.button("🚀 VALIDER MON PAIEMENT", use_container_width=True):
        st.session_state["paiement_clique"] = True
        st.balloons()
        st.snow() 

    # APPARITION DU BOUTON WHATSAPP APPRÈS LE CLIC
    if st.session_state["paiement_clique"]:
        st.success("✅ Paiement signalé avec succès dans le système M'SIRI !")
        st.markdown(
            f"""<a href="https://wa.me/243973964067?text=J'ai%20payé%20mon%20accès%20M'SIRI%20(Mon%20ID%20Appareil%20:%20{st.session_state['my_device']})" target="_blank">
                <button style="background-color: #25D366; color: white; border: none; padding: 15px 25px; font-weight: bold; border-radius: 12px; cursor: pointer; width: 100%; font-size: 16px; box-shadow: 0px 4px 10px rgba(37, 211, 102, 0.3); width: 100%;">
                    📲 CLIQUEZ ICI POUR ENVOYER VOTRE CAPTURE SUR WHATSAPP
                </button>
            </a>""", 
            unsafe_allow_html=True
        )
    
    st.divider()
    
    # 2. EN DERNIER POSITION : La case de clé d'activation pour basculer VIP
    st.warning("🔑 Une fois votre clé reçue par le Commandant, insérez-la ici pour activer le Terminal :")
    col_input, col_btn = st.columns([3, 1])
    with col_input:
        cle_saisie = st.text_input(
            "Clé d'activation",
            placeholder="Insérez votre clé VIP M'SIRI ici (MS-XXXX-XXXX)...",
            label_visibility="collapsed",
            key="champ_activation_vip"
        )
    with col_btn:
        if st.button("🔓 ACTIVER L'ACCÈS", use_container_width=True, type="primary"):
            if cle_saisie:
                cle_saisie_clean = cle_saisie.strip()
                keys_db = st.session_state.get("keys_db", {})
                
                if cle_saisie_clean in keys_db:
                    appareil_lie = keys_db[cle_saisie_clean]
                    current_device = st.session_state.get("my_device")
                    
                    if appareil_lie is None or appareil_lie == "None" or appareil_lie == current_device:
                        if enregistrer_activation(cle_saisie_clean, current_device):
                            st.session_state["auth"] = True
                            st.success("⚡ Clé validée ! Alignement des satellites réussi.")
                            time.sleep(1)
                            st.rerun()
                    else:
                        st.error("❌ Cette clé est déjà verrouillée sur un autre appareil mobile.")
                else:
                    st.error("❌ Clé invalide ou inexistante. Vérifiez l'orthographe.")
            else:
                st.warning("⚠️ Veuillez saisir une clé avant de cliquer.")


# CAS B : L'UTILISATEUR EST CONNECTÉ (Zone VIP Sécurisée)
def calcul_poisson_msiri(domicile, exterieur):
    """
    Modèle de Poisson prédictif pour le football (version NumPy vectorisée)
    
    Args:
        domicile (str): Nom de l'équipe à domicile
        exterieur (str): Nom de l'équipe à l'extérieur
    
    Returns:
        dict: win_a, nul, defaite, top (scores probables)
    """
    # Base de données des forces d'équipes (à enrichir)
    forces = {
        "TP Mazembe": 1.4,
        "Saint Éloi Lupopo": 1.1,
        "Vita Club": 1.2,
        "AS VClub": 1.15,
        "DCMP": 0.9,
        "Maniema Union": 1.05,
        "Raja Casablanca": 1.3,
        "Wydad": 1.28,
        "ES Tunis": 1.25,
        "Al Ahly": 1.35,
    }
    
    # Force par défaut si équipe non répertoriée
    force_dom = forces.get(domicile, 1.0)
    force_ext = forces.get(exterieur, 1.0)
    
    # Buts attendus (lambda)
    lambda_dom = force_dom * 1.8  # Moyenne générale domicile
    lambda_ext = force_ext * 1.2  # Moyenne générale extérieur
    
    max_buts = 10
    
    # Création des matrices de buts (vectorisation)
    buts_dom = np.arange(0, max_buts + 1)
    buts_ext = np.arange(0, max_buts + 1)
    
    # Calcul vectorisé des probabilités Poisson
    probs_dom = poisson.pmf(buts_dom[:1.0, None], lambda_dom)
    probs_ext = poisson.pmf(buts_ext[None, 1.0:], lambda_ext)
    probs_total = probs_dom * probs_ext
    
    # Classification des résultats
    prob_victoire = np.sum(probs_total[np.triu_indices_from(probs_total, 1)])
    prob_nul = np.sum(np.diag(probs_total))
    prob_defaite = np.sum(probs_total[np.tril_indices_from(probs_total, -1)])
    
    # Top 5 des scores les plus probables
    indices_tri = np.argsort(probs_total.flatten())[-5:][::-1]
    top_scores = []
    for idx in indices_tri:
        i = idx // (max_buts + 1)
        j = idx % (max_buts + 1)
        top_scores.append((int(i), int(j)))
    
    return {
        'win_a': round(float(prob_victoire * 100), 1),
        'nul': round(float(prob_nul * 100), 1),
        'defaite': round(float(prob_defaite * 100), 1),
        'top': top_scores,
        'lambda_dom': round(lambda_dom, 2),
        'lambda_ext': round(lambda_ext, 2)
    }# Test de la fonction
resultat = calcul_poisson_msiri("TP Mazembe", "Saint Éloi Lupopo")
print(f"Victoire: {resultat['win_a']}%")
print(f"Nul: {resultat['nul']}%")
print(f"Défaite: {resultat['defaite']}%")
print(f"Score probable: {resultat['top'][0][0]} - {resultat['top'][0][1]}")
print(f"Top 5: {resultat['top']}")# Version avec cache pour accélérer les calculs répétés
from functools import lru_cache

@lru_cache(maxsize=128)
def calcul_poisson_msiri_cached(domicile, exterieur):
    """Version avec cache pour les mêmes paires d'équipes"""
    return calcul_poisson_msiri(domicile, exterieur)

# Dans Streamlit, utiliser st.cache_data
@st.cache_data(ttl=3600)  # Cache d'une heure
def calcul_poisson_msiri_streamlit(domicile, exterieur):
    return calcul_poisson_msiri(domicile, exterieur)
def visualiser_matrice_poisson(domicile, exterieur):
    """Affiche la matrice des probabilités de scores"""
    res = calcul_poisson_msiri(domicile, exterieur)
    
    st.subheader(f"📊 Matrice des probabilités : {domicile} vs {exterieur}")
    
    # Création de la matrice pour l'affichage
    max_buts = 6  # Afficher jusqu'à 6 buts pour lisibilité
    lambda_dom = res['lambda_dom']
    lambda_ext = res['lambda_ext']
    
    buts_dom = np.arange(0, max_buts + 1)
    buts_ext = np.arange(0, max_buts + 1)
    probs_dom = poisson.pmf(buts_dom[:, None], lambda_dom)
    probs_ext = poisson.pmf(buts_ext[None, :], lambda_ext)
    matrice = (probs_dom * probs_ext) * 100
    
    # Affichage avec Streamlit
    st.dataframe(
        matrice,
        column_config={
            "index": "Domicile →",
            **{str(j): f"{j} buts" for j in range(max_buts + 1)}
        },
        use_container_width=True
    )

    # L'onglet Académie accueille désormais le Simulateur de Gestion de manière étanche
    with tab3:
        st.subheader("🎓 L'ACADÉMIE DES MILLIONNAIRES")
        
        # --- SIMULATEUR DE GESTION (EMBARQUÉ CHEZ LES VIP) ---
        st.markdown("### 🧮 SIMULATEUR DE GESTION DE CAPITAL (MONEY MANAGEMENT)")
        st.info("Entrez votre capital actuel pour recevoir votre plan de bataille quotidien.")

        col_cap1, col_cap2 = st.columns(2)

        with col_cap1:
            capital_total = st.number_input("Votre Capital Total ($)", min_value=10.0, value=100.0, step=10.0)
            niveau_risque = st.select_slider("Niveau de Risque M'SIRI", options=["Prudent", "Équilibré", "Guerrier"], value="Équilibré")

        # Calculs logiques du Commandant
        pourcentage = 0.02 if niveau_risque == "Prudent" else 0.05 if niveau_risque == "Équilibré" else 0.10
        mise_conseillee = capital_total * pourcentage
        objectif_jour = capital_total * 0.15 

        with col_cap2:
            st.metric(label="Mise Maximum / Signal", value=f"{mise_conseillee:.2f} $")
            st.metric(label="Objectif Gain Journalier", value=f"+{objectif_jour:.2f} $")

        st.warning(f"🛡️ **STRATÉGIE {niveau_risque.upper()} :** Ne lancez jamais plus de 3 signaux par jour avec cette mise.")
        st.divider()

        # --- LA DOCTRINE M'SIRI ---
        st.markdown("""
        ### 📜 Les 3 Lois d'Airain du Capital
        1. **La Loi du Pourcentage :** On ne mise jamais une somme fixe (ex: 10$), on mise toujours un pourcentage de ce qu'on possède.
        2. **Le Stop-Loss Mental :** Si vous perdez 3 fois de suite, éteignez le terminal. Revenez demain, le marché ne fuit pas.
        3. **La Discipline du Monde des rois :** Le profit se construit sur un mois, pas sur un soir. Soyez patient comme un lion.    
---
### 📖 Guide d'Utilisation du Terminal
* **Signaux Trading :** Actualisez la page toutes les 15 minutes.
* **Analyse Poisson :** Précision de 85% sur les grands championnats.
* **Retraits Orange Money :** Sécurisez 50% de vos bénéfices chaque dimanche.
""")

# ====================================================================================
# --- ARCHITECTURE DE LA BARRE LATÉRALE (Sidebar unique et ordonnée) ---
# ====================================================================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100) # Logo Pro
    st.title("🏛️ NAVIGATION")
    st.write(f"🆔 **ID Appareil :** `{st.session_state['my_device'][:10]}`")
    
    st.divider()

    # 1. BOUTON DE DÉCONNEXION UNIQUE (Visible seulement si connecté)
    if st.session_state.get("auth", False):
        if st.button("🔴 SE DÉCONNECTER", use_container_width=True):
            st.session_state["auth"] = False
            st.rerun()
    
    st.divider()

    # 2. SECTION ADMINISTRATION SECRÈTE
    with st.expander("🛠️ ADMINISTRATION M'SIRI"):
        pwd = st.text_input("Code Commandant", type="password")
        if pwd == ADMIN_PASSWORD:
            st.success("Accès Autorisé")
            
            # Gestion des clés
            st.write("### 📊 État des Clés")
            # On crée une copie pour éviter les erreurs de modification pendant la lecture
            for k, v in list(st.session_state.get("keys_db", {}).items()):
                c_k, c_v, c_b = st.columns([2, 2, 1])
                c_k.caption(k)
                if v:
                    c_v.code(v[:6], language=None)
                    if c_b.button("♻️", key=f"res_{k}"):
                        st.session_state["keys_db"][k] = None
                        st.rerun()
                else:
                    c_v.write("Libre")
            
            # Ajout de clé
            st.divider()
            nk = st.text_input("Nouvelle Clé")
            if st.button("➕ CRÉER"):
                if nk:
                    if "keys_db" not in st.session_state:
                        st.session_state["keys_db"] = {}
                    st.session_state["keys_db"][nk] = None
                    st.rerun()
        elif pwd != "":
            st.error("🔒 Accès refusé")

st.divider()
st.caption("© 2026 M'SIRI CAPITAL - Technologie de Lubumbashi.")
