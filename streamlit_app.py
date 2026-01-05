import streamlit as st
import pandas as pd
import numpy as np
import datetime
import random # <--- LE MOTEUR DU HASARD EST ICI
import streamlit as st
import random

# --- INITIALISATION DES COMPTEURS ---
if "nb_visites" not in st.session_state:
    st.session_state["nb_visites"] = 0 # Compteur de visites pour ta session
if "essais_foot_gratuits" not in st.session_state:
    st.session_state["essais_foot_gratuits"] = 0

# Chaque fois que le script tourne, on compte une interaction (vue cachée simplifiée)
st.session_state["nb_visites"] += 1

# --- SECTION FOOT (CORRIGÉE) ---
st.subheader("⚽ Analyseur de Pronostics (Mode Essai)")

if st.session_state["essais_foot_gratuits"] < 2:
    st.write(f"🎁 Il vous reste **{2 - st.session_state['essais_foot_gratuits']} analyses gratuites**.")
    
    col_e1, col_e2 = st.columns(2)
    with col_e1:
        eq_dom = st.text_input("Équipe à Domicile :", placeholder="Ex: TP Mazembe", key="pub_dom")
    with col_e2:
        eq_ext = st.text_input("Équipe Visiteuse :", placeholder="Ex: Lupopo", key="pub_ext")

    if st.button("LANCER L'ANALYSE"):
        if eq_dom and eq_ext:
            # On incrémente AVANT d'afficher
            st.session_state["essais_foot_gratuits"] += 1
            
            # Logique de résultat
            res = random.choice([
                f"Victoire de {eq_dom}. La forme actuelle favorise les locaux.",
                f"Match nul. Les deux équipes se neutralisent au milieu.",
                f"Avantage {eq_ext}. Attention à leur efficacité à l'extérieur."
            ])
            
            # AFFICHAGE DIRECT (Sans st.rerun pour éviter que ça disparaisse)
            st.success(f"**RÉSULTAT M'SIRI :** {res}")
            st.balloons()
        else:
            st.warning("Entrez le nom des deux équipes.")
else:
    st.error("🚫 Limite d'essais atteinte. Passez VIP pour continuer.")

# --- LA VUE CACHÉE DU MAIRE GÉNÉRAL (ADMIN) ---
st.sidebar.markdown("---")
with st.sidebar.expander("🔐 ESPACE COMMANDANT"):
    admin_pass = st.text_input("Code Secret Admin :", type="password")
    if admin_pass == "MAIRE243": # Ton mot de passe secret
        st.write("### 📊 STATISTIQUES LIVE")
        st.metric("Interactions Session", st.session_state["nb_visites"])
        st.write("Ce compteur montre l'activité sur ton site depuis ton ouverture.")
        st.info("Note : Pour un vrai compteur global, il faudrait une base de données, mais ceci te donne déjà une idée de l'engagement actuel.")
# --- CONFIGURATION ET INITIALISATION ---
if "auth" not in st.session_state:
    st.session_state["auth"] = False
# ... (le reste de ton code)
# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="M'SIRI COMMAND CENTER 2026", layout="wide", initial_sidebar_state="collapsed")

# --- INITIALISATION ROBUSTE DU SESSION STATE ---
if "auth" not in st.session_state:
    st.session_state["auth"] = False
if "accueil_vu" not in st.session_state:
    st.session_state["accueil_vu"] = False
if "essais_foot_gratuits" not in st.session_state:
    st.session_state["essais_foot_gratuits"] = 0 # Compteur pour les essais foot

# --- STYLES PERSONNALISÉS ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #e0e0e0; }
    .stButton>button { 
        width: 100%; 
        background-color: #ff4b4b; /* Rouge M'SIRI */
        color: white; 
        border-radius: 5px; 
        padding: 10px 0; 
        font-size: 1.1em;
        font-weight: bold;
    }
    .stAlert { color: #ffffff; }
    /* Style pour le bouton WhatsApp */
    .whatsapp-button button {
        background-color: #25D366 !important; /* Vert WhatsApp */
        color: white !important;
        border: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- NUMÉRO ORANGE MONEY ET WHATSAPP (À REMPLACER) ---
TON_NUMERO_OM = "+243898213650" # <<< Mets ton numéro Orange Money ici
TON_CODE_VIP = "SLVC2026" # <<< Ton code VIP final

# --- FENÊTRE 1: ÉCRAN D'ACCUEIL CAPTIVANT ---
if not st.session_state["accueil_vu"]:
    st.image("https://via.placeholder.com/600x250?text=M'SIRI+CAPITAL+LOGO+2026", caption="Votre QG pour dominer les marchés") # Remplace par ton logo
    st.title("🌟 Bienvenue au Commandement M'SIRI CAPITAL 🌟")
    st.subheader("Transformez votre ambition en succès financier.")
    st.write("---")
    st.info("""
    **Cher futur Maire Général,**
    
    Fatigué des pertes et des pronostics incertains ? **M'SIRI CAPITAL 2.0** est votre terminal de décision ultime.
    Nous vous offrons une approche stratégique pour le **Trading** et des analyses poussées pour les **Pronostics Sportifs**.
    
    **Pourquoi M'SIRI ?**
    * **📊 Vision Claire :** Accédez aux marchés en temps réel.
    * **🎯 Stratégie Gagnante :** Des outils pour protéger et faire fructifier votre capital.
    * **⚽ Pronostics Affûtés :** Des analyses IA pour vos paris footballistiques (2 essais gratuits !).
    * **🤝 Support Local :** Le Maire Général est là pour vous accompagner.
    
    Prêt à cesser de deviner et commencer à conquérir ?
    """)
    if st.button("ACCÉDER AU TERMINAL DU COMMANDEMENT"):
        st.session_state["accueil_vu"] = True
        st.rerun()

# --- FENÊTRE 2: DÉCOUVERTE (GRAPHIQUE + 2 ESSAIS FOOT + ACCÈS VIP) ---
elif not st.session_state["auth"]:
    st.title("🚀 Terminal de Découverte M'SIRI")
    st.caption("Découvrez la puissance avant de rejoindre l'élite.")

    # --- GRAPHIQUE LIVE (TOUJOURS VISIBLE) ---
    st.subheader("📈 Marché Mondial en Direct")
    st.components.v1.html("""
        <div style="height:350px;">
          <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
          <script type="text/javascript">
          new TradingView.widget({"autosize": true, "symbol": "BINANCE:BTCUSDT", "interval": "5", "theme": "dark", "container_id": "tv_chart_public"});
          </script><div id="tv_chart_public"></div>
        </div>
    """, height=350)
    st.caption("Données en temps réel fournies par TradingView.com")

    st.divider()

    if st.button("OBTENIR LE PRONOSTIC GRATUIT"):
            if equipe_dom and equipe_ext:
                st.session_state["essais_foot_gratuits"] += 1
                
                # ... ta logique de choix de résultat ...
                pronostic_choisi = random.choice(resultats_possibles)
                
                # ON AFFICHE SANS FAIRE DE RERUN APRÈS
                st.success(f"**ANALYSE M'SIRI :** {pronostic_choisi}")
                st.balloons()
            else:
                st.warning("Veuillez saisir les noms des deux équipes.")
                
                # Génération de pronostic (simulé pour l'exemple)
                import random
                resultats_possibles = [
                    f"Victoire de **{equipe_dom}**. Leur attaque est en feu à domicile.",
                    f"Match nul probable. Les défenses des deux équipes sont très solides.",
                    f"**{equipe_ext}** pourrait créer la surprise. Attention à leur vitesse en contre."
                ]
                pronostic_choisi = random.choice(resultats_possibles)
                
                st.success(f"**ANALYSE M'SIRI :** {pronostic_choisi}")
                st.write("Indice de confiance : **75%**.")
                st.write("Conseil : 'Moins de 3.5 buts' pourrait être une option sécurisée.")
                st.info(f"Il vous reste {2 - st.session_state['essais_foot_gratuits']} essai(s) gratuit(s).")
                st.rerun() # Rafraîchir pour mettre à jour le compteur
            else:
                st.warning("Veuillez saisir les noms des deux équipes.")
    

    st.divider()

    # --- ACCÈS VIP ET PAIEMENT ---
    st.header("👑 Débloquez l'Accès VIP Complet")
    st.write("Le mode VIP vous donne un pouvoir illimité sur les analyses et les outils.")
    
    col_pay_info, col_pay_action = st.columns(2)
    
    with col_pay_info:
        st.subheader("1. Dépôt Orange Money")
        st.info(f"**Abonnement Mensuel : 10$**")
        st.write(f"Envoyez votre paiement à ce numéro : **{+243898213650}**")
        
        whatsapp_link = f"https://wa.me/{+243973964067}?text=Bonjour%20Maire%20Général,%20je%20viens%20de%20faire%20un%20dépôt%20pour%20l'accès%20VIP."
        st.markdown(
            f'<div class="whatsapp-button"><a href="{whatsapp_link}" target="_blank">'
            '<button style="background-color:#25D366; color:white;">🆘 CONTACTER LE Maire Général (WhatsApp)</button>'
            '</a></div>', unsafe_allow_html=True
        )

    with col_pay_action:
        st.subheader("2. Activer votre Accès")
        code_vip_input = st.text_input("CLÉ D'ACTIVATION VIP :", type="password", key="vip_code_public")
        
        if st.button("DÉVERROUILLER L'ESPACE VIP"):
            if code_vip_input == TON_CODE_VIP:
                st.session_state["auth"] = True
                st.rerun()
            else:
                st.error("Clé VIP incorrecte. Veuillez vérifier ou contacter le support.")

# --- FENÊTRE 3: ESPACE VIP (ILLIMITÉ) ---
else:
    st.balloons()
    st.title("🏆 BIENVENUE DANS L'ESPACE VIP M'SIRI !")
    st.success(f"Accès Illimité Actif. Maire Général, session du {datetime.datetime.now().strftime('%d/%m/%Y')}")

    # --- SECTION TRADING AVANCÉE (VIP) ---
    st.header("📈 Terminal de Trading Avancé")
    col_t1, col_t2 = st.columns([1, 2])
    
    with col_t1:
        st.subheader("💰 Gestion de Capital Personnalisée")
        capital_actuel = st.number_input("Mon Capital Actuel ($)", value=355.0, min_value=1.0)
        objectif_perso = st.slider("Objectif de Profit Journalier (%)", 1, 15, 5)
        
        gain_cible = capital_actuel * (objectif_perso / 100)
        st.metric("Gain Cible du Jour", f"+{gain_cible:.2f} $")
        
        st.divider()
        st.subheader("🤖 Signal d'Indicateur IA M'SIRI")
        # Ici tu peux mettre des signaux plus sophistiqués ou des conseils quotidiens
        tendances_vip = ["🟢 ACHAT FORT : Préparer l'entrée", "🟡 ATTENTE : Observation du marché", "🔴 VENTE : Consolider les profits"]
        st.info(f"Signal du jour : **{random.choice(tendances_vip)}**")

    with col_t2:
        st.subheader("📊 Plan de Croissance vers le Million")
        jours_proj = np.arange(1, 31)
        croissance_proj = capital_actuel * (1 + objectif_perso/100)**jours_proj
        df_projection = pd.DataFrame({'Jour': jours_proj, 'Capital Projeté ($)': croissance_proj})
        st.line_chart(df_projection.set_index('Jour'))
        
        st.caption("Cette projection n'est pas une garantie, mais un objectif de croissance basé sur votre discipline.")

    st.divider()

    # --- SECTION FOOT ILLIMITÉE (VIP) ---
    st.header("⚽ Pronostics Football Illimités")
    st.write("Entrez les équipes de votre choix pour obtenir des analyses précises sans limite.")
    
    col_eq_vip1, col_eq_vip2 = st.columns(2)
    with col_eq_vip1:
        equipe_dom_vip = st.text_input("Équipe à Domicile (VIP) :", placeholder="Ex: Bayern Munich", key="eq_dom_vip")
    with col_eq_vip2:
        equipe_ext_vip = st.text_input("Équipe Visiteuse (VIP) :", placeholder="Ex: Borussia Dortmund", key="eq_ext_vip")
    
    if st.button("ANALYSER LE MATCH (VIP)"):
        if equipe_dom_vip and equipe_ext_vip:
            import random
            resultats_vip = [
                f"Victoire nette de **{equipe_dom_vip}**. Leur historique à domicile est dominant.",
                f"Un match nul serré est possible. Les deux équipes sont de force égale.",
                f"**{equipe_ext_vip}** a des atouts pour surprendre. Ne les sous-estimez pas."
            ]
            pronostic_vip = random.choice(resultats_vip)

            st.success(f"**ANALYSE STRATÉGIQUE VIP :** {pronostic_vip}")
            st.write("Conseils supplémentaires : 'Plus de 1.5 buts' ou 'Les deux équipes marquent'.")
            st.write("Indice de confiance du Commandement M'SIRI : **90%**.")
        else:
            st.warning("Veuillez saisir les noms des deux équipes pour l'analyse VIP.")

    st.divider()
    if st.button("🔴 DÉCONNEXION SÉCURISÉE"):
        st.session_state["auth"] = False
        st.session_state["accueil_vu"] = False # Retour à l'accueil pour nouvelle session
        st.session_state["essais_foot_gratuits"] = 0 # Réinitialiser les essais gratuits
        st.rerun()

st.divider()
st.caption("© 2026 M'SIRI COMMANDEMENT - Lubumbashi, RDC. Tous droits réservés.")
