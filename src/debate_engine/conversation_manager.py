#!/usr/bin/env python3
"""
Module: conversation_manager.py
Description: Orchestre le débat entre une IA supportant l'OM et une IA supportant le PSG.
Utilise les personas définis dans persona_manager.py et la fonction generate_response() pour obtenir les réponses successives.
"""

import os
import sys
import time
import logging

# Ajouter le dossier parent 'src' au PYTHONPATH pour permettre l'import des modules internes.
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(current_dir, "..")
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from llm_interface.ollama_interface import generate_response
from debate_engine.persona_manager import get_om_persona, get_psg_persona

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def start_debate(initial_question="Quel est le plus grand club d'Europe ?", mode="standard", max_turns=4):
    conversation = []
    
    om_persona = get_om_persona(mode)
    psg_persona = get_psg_persona(mode)
    
    # Tour 1 : OM répond à la question initiale
    om_prompt = f"{om_persona}\nQuestion: {initial_question}"
    logging.info("Envoi du prompt OM: %s", om_prompt)
    om_response = generate_response(om_prompt, model="llama3.2")
    conversation.append({"speaker": "OM", "message": om_response})
    time.sleep(1)
    
    # Tour 2 : PSG répond en tenant compte de la réponse de l'OM
    psg_prompt = f"{psg_persona}\nRéaction à la réponse de l'OM: {om_response}\nQuestion: {initial_question}"
    logging.info("Envoi du prompt PSG: %s", psg_prompt)
    psg_response = generate_response(psg_prompt, model="llama3.2")
    conversation.append({"speaker": "PSG", "message": psg_response})
    time.sleep(1)
    
    current_turn = 2
    while current_turn < max_turns:
        # Tour suivant pour OM
        om_followup = f"{om_persona}\nRéaction à la réponse du PSG: {psg_response}\nQuestion: {initial_question}"
        logging.info("Envoi du prompt OM (tour %d): %s", current_turn+1, om_followup)
        om_response = generate_response(om_followup, model="llama3.2")
        conversation.append({"speaker": "OM", "message": om_response})
        current_turn += 1
        if current_turn >= max_turns:
            break
        # Tour suivant pour PSG
        psg_followup = f"{psg_persona}\nRéaction à la réponse de l'OM: {om_response}\nQuestion: {initial_question}"
        logging.info("Envoi du prompt PSG (tour %d): %s", current_turn+1, psg_followup)
        psg_response = generate_response(psg_followup, model="llama3.2")
        conversation.append({"speaker": "PSG", "message": psg_response})
        current_turn += 1
        time.sleep(1)
        
    return conversation

if __name__ == "__main__":
    transcript = start_debate("Quel club domine le football européen ?", mode="standard", max_turns=4)
    for entry in transcript:
        print(f"{entry['speaker']} : {entry['message']}")
        print("-"*40)