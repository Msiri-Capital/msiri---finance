import streamlit as st

st.set_page_config(page_title="M'SIRI CAPITAL VIP", page_icon="🔒")

# --- TITRE ET ACCUEIL ---
st.title("🚀 M'SIRI CAPITAL - COMMANDEMENT")
st.write("### Outil de Gestion de Fortune - Maire Général Nicolas")

# --- SYSTÈME DE VÉRIFICATION ---
if "authentifie" not in st.session_state:
    st.session_state["authentifie"] = False

# Zone de saisie du code
if not st.session_state["authentifie"]:
    st.warning("🔒 CET OUTIL EST RÉSERVÉ AUX MEMBRES VIP")
    code_entre = st.text_input("Entrez votre Code d'Accès unique :", type="password")
    
    # Ton code secret (Tu peux le changer ici)
    CODE_SECRET = "MSIRI2025" 
    
    if st.button("Débloquer l'accès"):
        if code_entre == CODE_SECRET:
            st.session_state["authentifie"] = True
            st.rerun()
        else:
            st.error("Code incorrect. Payez votre abonnement au +243 898 213 650")
            st.info("Prix : 10$ / mois via M-Pesa")

# --- CONTENU VERROUILLÉ (S'affiche seulement si le code est bon) ---
if st.session_state["authentifie"]:
    st.balloons()
    st.success("✅ ACCÈS VIP ACTIVÉ")
    
    # Ton outil de trading ici
    capital = st.number_input("Capital Actuel ($)", value=355.0)
    objectif = st.slider("Objectif (%)", 1, 10, 5)
    st.write(f"### Mise conseillée : **{(capital * (objectif/100)):.2f} $**")
    
    if st.button("Se déconnecter"):
        st.session_state["authentifie"] = False
        st.rerun()
