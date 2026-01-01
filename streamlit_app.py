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

    # 4. SYSTÈME DE SÉCURITÉ (LA PORTE VIP - Après le graphique public)
    if "auth" not in st.session_state:
        st.session_state["auth"] = False

    if not st.session_state["auth"]:
        st.divider()
        st.title("🛡️ ZONE COMMANDEMENT - ACCÈS VIP")
        st.write("### Débloquez votre plein potentiel avec nos outils exclusifs.")
        
        code_entre = st.text_input("CLÉ DE CHIFFREMENT VIP :", type="password")
        
        if st.button("DÉVERROUILLER L'ACCÈS VIP"):
            if code_entre == "MSIRI2026": # TON CODE SECRET
                st.session_state["auth"] = True
                st.rerun()
            else:
                st.error("ACCÈS REFUSÉ. Contactez le Maire Général.")
                st.write("💳 Paiement Orange Money : ** +243 898 213 650 **")

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
            
        st.divider        st.subheader("📝 Journal de Guerre (Profits)")
        gain_reel = st.number_input("Gain réalisé aujourd'hui ($)", value=0.0)
        
        if st.button("ENREGISTRER LA SESSION"):
            st.toast("Session enregistrée !")

        if st.button("🔴 Fermer le Terminal (Se déconnecter)"):
            st.session_state["auth"] = False
            st.rerun()

    st.divider()
    st.caption("© 2026 M'SIRI COMMANDEMENT - Lubumbashi, RDC. Tous droits réservésTon
