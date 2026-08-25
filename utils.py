# ===================================================================
# utils.py - Fonctions utilitaires M'SIRI CAPITAL
# ===================================================================

import random
import time
import streamlit as st

def obtenir_citation_du_jour():
    """Retourne une citation aléatoire basée sur le jour"""
    citations = [
        "Le succès n'est pas final, l'échec n'est pas fatal : c'est le courage de continuer qui compte. - Winston Churchill",
        "La discipline est le pont entre les objectifs et l'accomplissement. - Jim Rohn",
        "Ne jugez pas chaque journée par votre récolte, mais par les graines que vous plantez. - R.L. Stevenson",
        "Le plus grand risque est de n'en prendre aucun. - Mark Zuckerberg",
        "La fortune sourit aux audacieux. - Virgile",
        "Le secret de la réussite est de faire des choses communes de manière peu commune. - John D. Rockefeller"
    ]
    index = int(time.strftime("%j")) % len(citations)
    return citations[index]

def afficher_badge_paiement(numero_om, nom_agent):
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

def afficher_etapes_vip():
    """Affiche les étapes pour l'activation VIP"""
    st.subheader("📝 Marche à suivre")
    col1, col2, col3 = st.columns(3)
    col1.info("**1. TRANSFERT**\n\nEnvoyez le montant au numéro Orange Money.")
    col2.info("**2. VALIDATION**\n\nCliquez sur le bouton de validation.")
    col3.info("**3. RÉCEPTION**\n\nEnvoyez la capture pour obtenir votre clé.")
