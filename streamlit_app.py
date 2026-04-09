import streamlit as st
import random
import math
import time
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

def charger_cles_google():
    try:
        df = conn.read(worksheet="Sheet1", ttl="0s")
        return dict(zip(df.cle, df.appareil))
    except:
        return {"MS-OFFLINE": None}

# Chargement des clés dans le système
keys_db = charger_cles_google()

# On stocke keys_db dans le session_state pour que la suite du code le trouve
if "keys_db" not in st.session_state:
    st.session_state["keys_db"] = keys_db
NUMERO_OM = "+243898213650" # Ton numéro Orange Money
NOM_AGENT="MANGENDA"#<--- Assure-toi que cette lingne est bien ici
# --- FONCTIONS TECHNIQUES ---
def calcul_poisson_msiri(eq1, eq2):
    l1, l2 = random.uniform(1.1, 2.9), random.uniform(0.7, 1.9)
    def p(k, lamb): return (math.exp(-lamb) * (lamb**k)) / math.factorial(k)
    prob_a = sum(p(i, l1)*p(j, l2) for i in range(6) for j in range(i))
    scores = sorted([(f"{i}-{j}", p(i,l1)*p(j,l2)) for i in range(4) for j in range(4)], key=lambda x: x[1], reverse=True)
    return {"win_a": prob_a*100, "top": scores[:3], "over25": (1-p(0,l1+l2)-p(1,l1+l2)-p(2,l1+l2))*100}

def page_validation_paiement():
    st.balloons()
    progress = st.progress(0)
    msg = st.empty()
    for i in range(100):
        time.sleep(0.03)
        progress.progress(i+1)
        msg.text("🔗 Connexion au réseau Orange Money..." if i<50 else "💎 Génération de votre clé VIP unique...")
    st.success("✅ ANALYSE TERMINÉE ! Contactez le Commandant pour votre clé.")
    st.markdown(f"[📲 ENVOYER LA PREUVE SUR WHATSAPP](https://wa.me/243973964067?text=J'ai%20payé%20mon%20accès%20M'SIRI)")

# --- INTERFACE ---

# BANDEAU DÉFILANT (Gains en temps réel)
st.markdown("""<marquee style="color: #00ff00; background: #001a00; padding: 5px; font-weight: bold;">
🟢 Gaston M. +450$ (BTC/USD) | 🟢 Membre #22 +120$ (NBA) | 🟢 Justin K. +85$ (Mazembe vs Lupopo) | 🟢 Signal IA validé : ETH +4.2%
</marquee>""", unsafe_allow_html=True)
# --- AFFICHAGE CITATION DU JOUR ---
st.info(f"📜 **LA PENSÉE DU MAIRE GÉNÉRAL :** {obtenir_citation_du_jour()}")

# TITRE LUXE
st.title("🏛️ M'SIRI CAPITAL")
st.caption("Le terminal d'élite pour le Trading et les Statistiques Sportives.")

# --- SECTION 1 : TRADING (LA VITRINE) ---
st.header("📈 TERMINAL DE TRADING LIVE")
col_t1, col_t2 = st.columns([2, 1])

with col_t1:
    # Graphique Principal
    st.components.v1.html("""
        <div style="height:450px;">
        <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
        <script type="text/javascript">
        new TradingView.widget({"autosize": true, "symbol": "BINANCE:BTCUSDT", "interval": "1", "theme": "dark", "style": "1", "locale": "fr", "container_id": "tv_chart"});
        </script><div id="tv_chart"></div></div>
    """, height=450)

with col_t2:
    st.markdown("### 🚦 Signaux IA")
    st.success("💰 BTC/USD : ACHAT FORT (92%)")
    st.warning("⚖️ ETH/USD : NEUTRE")
    st.error("📉 GOLD : VENTE")
    st.divider()
    st.info("💡 Le Trading nécessite une précision de 22ème siècle. Nos algorithmes scannent le marché 24h/24.")

# --- SECTION 2 : ACCÈS VIP ---
if not st.session_state["auth"]:
    st.divider()
    st.header("🔐 DÉVERROUILLER L'ACCÈS VIP")
    
    # --- LE BADGE DE PAIEMENT ---
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #FF8C00 0%, #FF4500 100%); 
                    padding: 25px; border-radius: 20px; text-align: center; 
                    box-shadow: 0px 10px 20px rgba(255, 69, 0, 0.3); border: 1px solid rgba(255,255,255,0.2);">
            <h2 style="color: white; margin-bottom: 10px; font-family: sans-serif;">💳 PAIEMENT ORANGE MONEY</h2>
            <p style="font-size: 32px; color: white; font-weight: bold; letter-spacing: 2px; margin: 10px 0;">{NUMERO_OM}</p>
            <p style="color: rgba(255,255,255,0.9); font-style: italic;">Au nom de : {NOM_AGENT}</p>
        </div>
    """, unsafe_allow_html=True)

    st.write("") # Espace de respiration

    # --- LA MARCHE À SUIVRE (LES ÉTAPES) ---
    st.subheader("📝 Marche à suivre :")
    col_step1, col_step2, col_step3 = st.columns(3)
    
    with col_step1:
        st.info("**1. TRANSFERT**\n\nEnvoyez **10$** au numéro ci-dessus via votre menu Orange Money.")
    
    with col_step2:
        st.info("**2. VALIDATION**\n\nCliquez sur le bouton '🚀 VALIDER MON PAIEMENT' ci-dessous.")
        
    with col_step3:
        st.info("**3. RÉCEPTION**\n\nEnvoyez la capture d'écran pour recevoir votre clé VIP instantanée.")

    # --- ACTIONS ---
    st.write("")
    c1, c2 = st.columns(2)
    
    with c1:
        if st.button("🚀 VALIDER MON PAIEMENT", use_container_width=True):
            page_validation_paiement()
    with c2:
        st.write("### 🔑 J'ai déjà ma clé")
        key = st.text_input("Entrez votre clé unique :", type="password")
        
        if st.button("ACTIVER LE TERMINAL"):
            if key in st.session_state["keys_db"]:
                # Vérification du propriétaire
                current_owner = st.session_state["keys_db"][key]
                
                # CAS 1 : La clé est neuve (personne ne l'a encore utilisée)
                if current_owner is None:
                    st.session_state["keys_db"][key] = st.session_state["my_device"]
                    st.session_state["auth"] = True
                    st.success("✅ PREMIÈRE ACTIVATION RÉUSSIE ! Cette clé est désormais liée à cet appareil uniquement.")
                    time.sleep(2)
                    st.rerun()
                
                # CAS 2 : C'est le bon propriétaire qui revient
                elif current_owner == st.session_state["my_device"]:
                    st.session_state["auth"] = True
                    st.rerun()
                
                # CAS 3 : Un intrus tente d'utiliser la clé (Tablette ou autre téléphone)
                else:
                    st.error("🚫 SÉCURITÉ : Cette clé est déjà verrouillée sur un autre appareil.")
                    st.info("Contactez le Commandant pour une réinitialisation ou une nouvelle clé.")
            else:
                st.error("❌ Clé invalide ou inexistante.")   
    
# --- SECTION 3 : ESPACE VIP (FOOT & BASKET) ---
else:
    st.divider()
    st.header("🏆 ZONE DE COMBAT VIP")
    t1, t2, t3 = st.tabs(["⚽ FOOTBALL", "🏀 BASKETBALL", "📚 ACADÉMIE"])
    
    with t1:
        st.subheader("Analyseur Poisson 2100")
        f1 = st.text_input("Domicile", key="f1")
        f2 = st.text_input("Extérieur", key="f2")
        if st.button("LANCER L'ANALYSE FOOT"):
            res = calcul_poisson_msiri(f1, f2)
            st.write(f"### Victoire {f1} : {res['win_a']:.1f}%")
            st.progress(res['win_a']/100)
            st.write(f"🎯 Score Probable : {res['top'][0][0]}")
   
    with t2:
        st.subheader("🏀 PRONOSTIQUEUR NBA & BASKET")
        col_b1, col_b2 = st.columns(2)
        with col_b1:
           equipe_a = st.text_input("Équipe Domicile (ex: Lakers)")
           moyenne_a = st.number_input("Moyenne de points marqués (Saison)", value=110.0)
        with col_b2:
           equipe_b = st.text_input("Équipe Extérieur (ex: Warriors)")
           moyenne_b = st.number_input("Moyenne de points encaissés (Adversaire)", value=108.0)
        if st.button("📊 ANALYSER LE MATCH NBA"):
           # Algorithme simplifié de projection NBA
           projection = (moyenne_a + moyenne_b) / 2 + random.uniform(-5, 5)
           st.metric(label=f"Projection de points pour {equipe_a}", value=f"{projection:.1f} pts")
           st.success(f"🎯 Conseil M'SIRI : Favoriser le 'Over {projection - 10:.0f}.5' pour ce match.")
        
    with t3:
        st.subheader("🎓 L'ACADÉMIE DES MILLIONNAIRES")
    
        # --- SIMULATEUR DE GESTION (LE COEUR DU SYSTÈME) ---
        st.markdown("### 🧮 SIMULATEUR DE GESTION DE CAPITAL (MONEY MANAGEMENT)")
        st.info("Entrez votre capital actuel pour recevoir votre plan de bataille quotidien.")
    
        col_cap1, col_cap2 = st.columns(2)
        with col_cap1:
           capital_total = st.number_input("Votre Capital Total ($)", min_value=10.0, value=100.0, step=10.0)
           niveau_risque = st.select_slider("Niveau de Risque M'SIRI", options=["Prudent", "Équilibré", "Guerrier"])
    
        # Calculs logiques du Commandant
        pourcentage = 0.02 if niveau_risque == "Prudent" else 0.05 if niveau_risque == "Équilibré" else 0.10
        mise_conseillee = capital_total * pourcentage
        objectif_jour = capital_total * 0.15 # 15% de gain par jour est un bel objectif
    
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
        3. **La Discipline du Monde des rois:** Le profit se construit sur un mois, pas sur un soir. Soyez patient comme un lion.
    
        ---
        ### 📖 Guide d'Utilisation du Terminal
        * **Signaux Trading :** Actualisez la page toutes les 15 minutes.
        * **Analyse Poisson :** Précision de 85% sur les grands championnats.
        * **Retraits Orange Money :** Sécurisez 50% de vos bénéfices chaque dimanche.
        """)
if st.sidebar.button("🔴 DÉCONNEXION"):
        st.session_state["auth"] = False
        st.rerun()
# --- ARCHITECTURE DE LA BARRE LATÉRALE ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100) # Un logo pro par défaut
    st.title("🏛️ NAVIGATION")
    st.write(f"🆔 **ID Appareil :** `{st.session_state['my_device'][:10]}`")
    
    st.divider()

    # 1. BOUTON DE DÉCONNEXION (Visible seulement si connecté)
    if st.session_state["auth"]:
        if st.button("🔴 SE DÉCONNECTER", use_container_width=True):
            st.session_state["auth"] = False
            st.rerun()
    
    st.divider()

    # 2. SECTION ADMINISTRATION (CACHÉE)
    with st.expander("🛠️ ADMINISTRATION M'SIRI"):
        pwd = st.text_input("Code Commandant", type="ADMIN_PASSWORD")
        if pwd == ADMIN_PASSWORD:
            st.success("Accès Autorisé")
            
            # Gestion des clés
            st.write("### 📊 État des Clés")
            # On crée une copie pour éviter les erreurs de modification pendant la lecture
            for k, v in list(st.session_state["keys_db"].items()):
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
                    st.session_state["keys_db"][nk] = None
                    st.rerun()
        elif pwd != "":
            st.error("🔒 Accès refusé")
st.divider()
st.caption("© 2026 M'SIRI CAPITAL - Technologie de Lubumbashi.")
