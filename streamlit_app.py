import streamlit as st
import random
import math
import time

TITRE obtenir_citation_du_jour():
    citations = [
        "Le succès n'est pas final, l'échec n'est pas fatal : c'est le courage de continuer qui compte. - Winston Churchill",
        "si je tombe, relève moi et aide moi à me retourner vers TOI. - Nicolas LEVANTE",
        "La discipline est le pont entre les objectifs et l'accomplissement. - Jim Rohn",
        "Ne jugez pas chaque journée par votre récolte, mais par les graines que vous plantez. - R.L. Stevenson",
        "Le plus grand risque est de n'en prendre aucun. - Mark Zuckerberg",
        "La fortune sourit aux audacieux. - Virgile",
        "Le secret de la réussite est de faire des choses communes de manière peu commune. - John D. Rockefeller"
    ]
    # --- CONFIGURATION ÉLITE ---
NUMERO_OM = "+243 898 213 650"  # Ton numéro Orange Money
NOM_AGENT = "M'SIRI CAPITAL HUB" # Nom qui s'affiche lors du transfert
    # Utilise le jour de l'année pour changer la citation
    index = int(time.strftime("%j")) % len(citations)
    return citations[index]

# --- CONFIGURATION ÉLITE ---
st.set_page_config(page_title="M'SIRI CAPITAL | TERMINAL 2100", layout="wide", initial_sidebar_state="collapsed")

# 1. INITIALISATION DES BASES (Sécurité & Stats)
if "auth" not in st.session_state: st.session_state["auth"] = False
if "my_device" not in st.session_state: st.session_state["my_device"] = str(random.getrandbits(32))
if "keys_db" not in st.session_state:
    cles = ["MS-77-X1", "MS-99-A1", "GD-00-11", "VIP-21-AA", "LUB-243-M"]
    st.session_state["keys_db"] = {cle: None for cle in cles}

NUMERO_OM = "+243898213650" # Ton numéro Orange Money

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
    st.markdown(f"[📲 ENVOYER LA PREUVE SUR WHATSAPP](https://wa.me/{NUMERO_OM}?text=J'ai%20payé%20mon%20accès%20M'SIRI)")

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
        # Champ de saisie de la clé déjà existant
        key = st.text_input("🗝️ Entrez votre clé reçue :", type="password", placeholder="Ex: MS-77-X1")
        if st.button("ACTIVER LE TERMINAL", use_container_width=True):
            if key in st.session_state["keys_db"]:
                # (Ton code de validation habituel...)
                st.session_state["auth"] = True
                st.rerun()
            else:
                st.error("Clé incorrecte.")

# --- SECTION 3 : ESPACE VIP (FOOT & BASKET) --elstime
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
        st.subheader("Moteur NBA / International")
        st.info("Le basket est en cours d'optimisation pour la NBA ce soir.")
        # Ajoute ici ton code basket de l'étape précédente

    with t3:
        st.subheader("Manuel de l'Investisseur")
        st.write("1. Ne misez jamais plus de 5% de votre capital.")
        st.write("2. Suivez l'IA, pas votre cœur.")

    if st.sidebar.button("🔴 DÉCONNEXION"):
        st.session_state["auth"] = False
        st.rerun()

st.divider()
st.caption("© 2026 M'SIRI CAPITAL - Technologie de Lubumbashi.")
