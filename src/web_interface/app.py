#!/usr/bin/env python3
"""
Interface web pour Classico Foot LLM avec Streamlit.
Permet à l'utilisateur de saisir un prompt, d'appeler generate_response(),
et d'afficher la réponse générée par le modèle Llama 3.2 via Ollama.
"""

import sys
import os

# Ajoute le dossier 'src' au PYTHONPATH pour que les imports fonctionnent
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(current_dir, "..")
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from llm_interface.ollama_interface import generate_response
import streamlit as st

# Titre et description de l'application
st.title("Classico Foot LLM")
st.write("Interface interactive pour interagir avec Llama 3.2 via Ollama.")

# Zone de saisie du prompt
prompt = st.text_area("Entrez votre prompt :", "Décris un fait drôle sur l'Olympique de Marseille.")

# Option de sélection du modèle (pour l'instant, un seul choix)
model = st.selectbox("Sélectionnez le modèle :", options=["llama3.2"], index=0)

# Bouton d'envoi
if st.button("Envoyer"):
    st.write("Envoi du prompt :", prompt)
    response = generate_response(prompt, model=model)
    if response:
        st.write("Réponse du modèle :")
        st.text_area("Sortie", value=response, height=300)
    else:
        st.error("Erreur lors de l'appel au modèle. Vérifiez votre configuration d'Ollama et le nom du modèle.")