#!/usr/bin/env python3
"""
Application Streamlit pour Classico Foot LLM - Débat OM vs PSG
Cette application intègre le traitement du débat (backend) et l'affichage (frontend) dans Streamlit.
L'utilisateur peut saisir une question initiale, choisir un mode (standard, comique, clash, agressif)
et définir le nombre de tours. L'application appelle ensuite la logique de débat et affiche le transcript.
"""

import os
import sys
import streamlit as st
import time
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# --- Ajout du dossier 'src' au PYTHONPATH pour permettre l'import des modules internes ---
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, "..", "src")
if src_path not in sys.path:
    sys.path.append(src_path)

# Importer la logique de débat depuis les modules développés
from debate_engine.conversation_manager import start_debate

# Titre et description de l'application Streamlit
st.title("Classico Foot LLM - Débat OM vs PSG")
st.write("Lancez un débat interactif entre une IA pro OM et une IA pro PSG directement via Streamlit.")

# Formulaire pour saisir les paramètres du débat
with st.form(key="debate_form"):
    initial_question = st.text_input("Entrez la question initiale pour le débat :", 
                                     "Quel club domine le football européen ?")
    mode = st.selectbox("Choisissez le mode de débat :", 
                        options=["standard", "comique", "clash", "agressif"], index=0)
    max_turns = st.number_input("Nombre de tours de parole :", min_value=2, max_value=10, value=4, step=1)
    submit_button = st.form_submit_button(label="Lancer le débat")

if submit_button:
    st.info("Génération du débat en cours... Cela peut prendre quelques instants.")
    try:
        # Appel de la logique de débat (backend) : la fonction start_debate retourne un transcript.
        transcript = start_debate(initial_question, mode=mode, max_turns=int(max_turns))
    except Exception as e:
        st.error(f"Erreur lors du traitement du débat : {e}")
        transcript = []
    
    # Affichage du transcript
    if transcript:
        st.success("Débat généré avec succès !")
        st.markdown("### Transcript du débat")
        for entry in transcript:
            if entry["speaker"] == "OM":
                st.markdown(f"**OM** : {entry['message']}")
            elif entry["speaker"] == "PSG":
                st.markdown(f"**PSG** : {entry['message']}")
            else:
                st.markdown(f"**{entry['speaker']}** : {entry['message']}")
            st.markdown("---")
    else:
        st.error("Aucun transcript généré. Vérifiez la configuration et réessayez.")

# Optionnel : Footer ou informations supplémentaires
st.markdown("**Classico Foot LLM** - Backend et Frontend intégrés avec Streamlit")