import streamlit as st
import pandas as pd
import numpy as np
import datetime

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(page_title="M'SIRI CAPITAL - MAÎTRISE TON AVENIR", layout="wide", initial_sidebar_state="collapsed")

# --- STYLE PERSONNALISÉ ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #e0e0e0; }
    .stButton>button { width: 100%; background-color: #ff4b4b; color: white; border-radius: 5px; }
    .stAlert { color: #ffffff; }
    </style>
    """, unsafe_allow_html=True)

# 2. MESSAGE D'ACCUEIL STRATÉGIQUE (Visible par tous)
if "message_initial_vu" not in st.session_state:
    st.session_state["message_initial_vu"] = False

if not st.session_state["message_initial_vu"]:
    st.title("🌟 Bienvenue au Commandement M'SIRI CAPITAL 🌟")
    st.image("https://via.placeholder.com/600x200?text=M'SIRI+CAPITAL+LOGO", caption="Votre QG pour dominer les marchés") # REMPLACE PAR TON LOGO SI TU EN AS UN
    st.write("---")
    st.info("""
    **Cher futur Maire Général,**
    
    Naviguez avec confiance dans l'univers du trading. M'SIRI CAPITAL est votre co-pilote intelligent, conçu pour transformer votre potentiel en profit réel.
    
    **Pourquoi nous choisir ?**
    * **📊 Gestion du Risque :** Finis les comptes brûlés ! Notre algorithme vous guide vers des objectifs réalistes.
    * **📈 Analyse du Marché :** Visualisez les tendances en temps réel, comme un professionnel.
    * **💎 Accès VIP :** Pour 10$ seulement (Orange Money), débloquez nos signaux précis et nos stratégies exclusives.
    
    **Découvrez notre interface ci-dessous et rejoignez l'élite du trading !**
    """)
    if st.button("J'AI COMPRIS, CONTINUER"):
        st.session_state["message_initial_vu"] = True
        st.rerun()
else: # Si le message a été vu, on affiche le reste de l'application
    # 3. GRAPHIQUE TRADINGVIEW PUBLIC (Visible par tous)
    st.subheader("📊 Marché en Temps Réel (Vue Générale)")
    st.components.v1.html("""
        <div class="tradingview-widget-container" style="height:350px;">
          <div id="tradingview_8534a"></div>
          <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
          <script type="text/javascript">
          new TradingView.widget({
            "autosize": true,
            "symbol": "BINANCE:BTCUSDT",
            "interval": "5",
            "timezone": "Etc/UTC",
            "theme": "dark",
            "style": "1",
            "locale": "fr",
            "toolbar_bg": "#f1f3f6",
            "enable_publishing": false,
            "hide_side_toolbar": true, /* Cache la barre latérale pour un affichage plus propre */
            "allow_symbol_change": true,
            "container_id": "tradingview_8534a"
          });
          </script>
        </div>
    """, height=350)
    st.caption("Données fournies par TradingView.com")

    
# --- SYSTÈME DE PAIEMENT AUTOMATISÉ (IMIDATION 1XBET) ---

if not st.session_state["auth"]:
    st.divider()
    st.title("🛡️ ZONE COMMANDEMENT - ACCÈS VIP")
    
    col_pay1, col_pay2 = st.columns(2)
    
    with col_pay1:
        st.write("### 1. Effectuez votre dépôt")
        st.info("Abonnement Mensuel : **10$**")
        
        # Bouton simulant l'ouverture du service Orange
        # Note: En RDC, on utilise souvent l'USSD *144#
        if st.button("💳 PAYER VIA ORANGE MONEY"):
            st.warning("Composez le *144# sur votre téléphone pour envoyer 10$ au numéro ci-dessous.")
            st.code("+243 898 213 650 ") # Ton numéro Orange
            st.write("Une fois le SMS de confirmation reçu, copiez l'ID de transaction.")

    with col_pay2:
        st.write("### 2. Activez votre accès")
        # Ici le client entre l'ID de transaction Orange
        transaction_id = st.text_input("Collez l'ID de transaction Orange Money :")
        
        if st.button("VÉRIFIER LE PAIEMENT"):
            if len(transaction_id) > 5: # Simule une vérification de longueur d'ID
                st.success("✅ TRANSACTION EN COURS DE VÉRIFICATION...")
                st.balloons()
                st.info(f"VOTRE CODE VIP EST : **MSIRI2026**")
                st.write("Notez ce code et entrez-le ci-dessous.")
            else:
                st.error("ID de transaction invalide.")

    # Bouton d'urgence WhatsApp avec Truemessage personnalisé
    st.write("---")
    whatsapp_link = "https://wa.me/243 898 213 650 ?text=Bonjour%20Maire%20Général,%20j'ai%20un%20problème%20avec%20mon%20dépôt."
    st.markdown(f"""
        <a href="{whatsapp_link}" target="_blank">
            <button style="width:100%; background-color:#25D366; color:white; border:none; padding:10px; border-radius:5px;">
                🆘 PROBLÈME ? CONTACTER LE GRAND BLAISE (WHATSAPP)
            </button>
        </a>
    """, unsafe_allow_html=True)
    
    st.write("---")
    # Zone finale pour entrer le code obtenu
    code_entre = st.text_input("ENTREZ LA CLÉ VIP OBTENUE :", type="password")
    if st.button("DÉVERROUILLER LE TERMINAL"):
        if code_entre == "MSIRI2026":
            st.session_state["auth"] = True
            st.rerun()
    # 5. CONTENU VIP (Calculateur + Projection + Journal - Visible après connexion)
    else:
        st.title("📈 TERMINAL DE COMMANDEMENT M'SIRI v2.0")
        st.success(f"Bienvenue Maire Général | Session du {datetime.datetime.now().strftime('%d/%m/%Y')}")

        col1, col2 = st.columns([1, 2])

        with col1:
            st.subheader("💰 Gestion de Capital")
            capital_initial = st.number_input("Capital Actuel ($)", value=355.0)
            objectif_journalier = st.slider("Objectif de Profit (%)", 1, 15, 5)
            
            profit_cible = capital_initial * (objectif_journalier / 100)
            st.metric("Objectif du Jour", f"+{profit_cible:.2f} $")
            
            st.divider()
            st.subheader("🤖 Indicateur M'SIRI IA")
            tendance = np.random.choice(["🔥 FORTE ACHAT", "📉 VENTE", "⏳ ATTENTE"])
            st.info(f"Analyse du Signal : **{tendance}**")

        with col2:
            st.subheader("📊 Projection vers le Million")
            jours = np.arange(1, 31)
            croissance = capital_initial * (1 + objectif_journalier/100)**jours
            df_proj = pd.DataFrame({'Jour': jours, 'Capital Projeté ($)': croissance})
            st.line_chart(df_proj.set_index('Jour'))
            
        st.divider()
        st.subheader("📝 Journal de Guerre (Profits)")
        gain_reel = st.number_input("Gain réalisé aujourd'hui ($)", value=0.0)
        
        if st.button("ENREGISTRER LA SESSION"):
            st.toast("Session enregistrée !")

        if st.button("🔴 Fermer le Terminal (Se déconnecter)"):
            st.session_state["auth"] = False
        messagererun()

    st.divider()
    st.caption("© 2026 M'SIRI COMMANDEMENT - Lubumbashi, RDC. Tous droits réservés.")
