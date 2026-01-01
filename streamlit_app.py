import streamlit as st
import pandas as pd
import numpy as np
import datetime

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(page_title="M'SIRI CAPITAL - 2026", layout="wide")

# --- INITIALISATION DE LA MÉMOIRE (INDISPENSABLE) ---
if "auth" not in st.session_state:
    st.session_state["auth"] = False
if "message_initial_vu" not in st.session_state:
    st.session_state["message_initial_vu"] = False

# --- STYLE ---
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; font-weight: bold; }
    .main { background-color: #0e1117; }
    </style>
    """, unsafe_allow_html=True)

# 2. MESSAGE D'ACCUEIL (L'ENCOURAGEMENT)
if not st.session_state["message_initial_vu"]:
    st.title("🌟 BIENVENUE CHEZ M'SIRI CAPITAL")
    st.success("### Votre succès commence ici, avec la rigueur du Commandement.")
    st.write("""
    **Cher futur investisseur,**
    
    Le trading n'est pas un jeu de hasard, c'est une science de précision. **M'SIRI CAPITAL** est conçu pour vous donner 
    une vision claire du marché et une gestion de risque de fer. 
    
    En utilisant cet outil, vous rejoignez une élite qui ne trade plus à l'aveugle. 
    L'avantage ? Une discipline mathématique qui protège votre capital et vise la croissance constante.
    
    *Prêt à dominer 2026 ?*
    """)
    if st.button("ACCÉDER AU TERMINAL DE MARCHÉ"):
        st.session_state["message_initial_vu"] = True
        st.rerun()

else:
    # 3. GRAPHIQUE PUBLIC (POUR LA CONFIANCE)
    st.subheader("📊 Marché Mondial en Direct")
    st.components.v1.html("""
        <div style="height:400px;">
          <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
          <script type="text/javascript">
          new TradingView.widget({
            "autosize": true, "symbol": "BINANCE:BTCUSDT", "interval": "5",
            "timezone": "Etc/UTC", "theme": "dark", "style": "1",
            "locale": "fr", "enable_publishing": false, "container_id": "tv_chart"
          });
          </script>
          <div id="tv_chart"></div>
        </div>
    """, height=400)

    # 4. LA BARRIÈRE VIP (SYSTÈME IMITATION 1XBET)
    if not st.session_state["auth"]:
        st.divider()
        st.header("🛡️ ACCÈS AU COMMANDEMENT VIP")
        
        col_pay1, col_pay2 = st.columns(2)
        
        with col_pay1:
            st.write("### 1. Effectuez votre dépôt")
            st.warning("💰 Abonnement : 10$ / mois")
            st.write("Dépôt via **Orange Money** au :")
            st.code("+243 898 213 650") # METS TON NUMÉRO ICI
            
            whatsapp_url = "https://wa.me/243 898 213 650 ?text=Salut%20Maire%20Général,%20je%20viens%20de%20faire%20mon%20dépôt."
            st.markdown(f'<a href="{whatsapp_url}" target="_blank"><button style="width:100%; background-color:#25D366; color:white; border:none; padding:10px; border-radius:5px; cursor:pointer;">🆘 CONTACTER LE GRAND BLAISE (WhatsApp)</button></a>', unsafe_allow_html=True)

        with col_pay2:
            st.write("### 2. Activation")
            trans_id = st.text_input("ID de transaction (Reçu Orange) :")
            code_vip = st.text_input("Code d'accès reçu :", type="password")
            
            if st.button("DÉVERROUILLER LE TERMINAL VIP"):
                if code_vip == "MSIRI2026":
                    st.session_state["auth"] = True
                    st.rerun()
                else:
                    st.error("Code incorrect ou paiement non vérifié.")

    # 5. CONTENU VIP (RÉSERVÉ)
    else:
        st.title("📈 TERMINAL VIP M'SIRI")
        st.success("Accès autorisé - Maire Général")
        
        cap = st.number_input("Ton Capital ($)", value=355.0)
        obj = st.slider("Objectif (%)", 1, 10, 5)
        st.metric("Gain à atteindre", f"{cap*(obj/100):.2f} $")
        
        if st.button("🔴 DÉCONNEXION"):
            st.session_state["auth"] = False
            st.rerun()

st.divider()
st.caption("© 2026 M'SIRI CAPITAL | ISTM Lubumbashi")
