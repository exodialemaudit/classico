#!/usr/bin/env python3
"""
Module: conversation_manager.py
Description: Orchestre le débat entre une IA supportant l'OM et une IA supportant le PSG.
Cette version accepte des paramètres personnalisés pour définir la personnalité de chaque IA
(p.ex. "Ultra", "Commentateur", "Ancien joueur", "Footix (Troll)") ainsi que le mode général (standard, comique, clash, agressif).
Elle intègre également une instruction pour fournir uniquement des informations factuelles et vérifiables
pour toutes les personnalités, sauf pour "Footix (Troll)".
"""

import os
import sys
import time
import logging

# Ajout du dossier parent 'src' au PYTHONPATH pour que les imports internes fonctionnent correctement
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(current_dir, "..")
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from src.llm_interface.ollama_interface import generate_response
from src.debate_engine.persona_manager import get_persona_prompt

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

async def generate_response_stream(prompt, personality, style):
    """Génère la réponse caractère par caractère."""
    response = ""
    async for token in llm.generate_stream(prompt):
        response += token
        yield response

def simulate_typing():
    """Simule l'effet de frappe."""
    return st.markdown("""
        <div class="typing-indicator">
            <span>●</span><span>●</span><span>●</span>
        </div>
    """, unsafe_allow_html=True)

async def generate_debate_response(speaker: str, topic: str, personality: str, style: str) -> str:
    """
    Génère une réponse pour un intervenant du débat.
    
    Args:
        speaker: Nom de l'équipe qui parle
        topic: Sujet du débat
        personality: Type de personnalité ("Standard", "Ultra", etc.)
        style: Style de débat ("Factuel", "Passionné", etc.)
    
    Returns:
        str: La réponse générée
    """
    # Construit le prompt
    persona_prompt = get_persona_prompt(speaker, personality, style)
    debate_prompt = f"{persona_prompt}\nSujet: {topic}\nRéponse:"
    
    try:
        response = await generate_response(debate_prompt)
        return response
    except Exception as e:
        logging.error(f"Erreur lors de la génération de la réponse: {e}")
        return f"Désolé, je ne peux pas répondre pour le moment. ({str(e)})"

def start_debate(initial_question, mode="standard", max_turns=4, om_personality="Standard", psg_personality="Standard"):
    """
    Lance un débat entre deux IA (supporter OM et supporter PSG) avec personnalités personnalisées.
    
    Args:
        initial_question (str): La question initiale posée aux IA.
        mode (str): Le mode général du débat ("standard", "comique", "clash", "agressif").
        max_turns (int): Nombre total de tours de parole.
        om_personality (str): Personnalité de l'IA supportant l'OM (ex: "Standard", "Ultra", "Commentateur", "Ancien joueur", "Footix (Troll)").
        psg_personality (str): Personnalité de l'IA supportant le PSG.
        
    Returns:
        list of dict: Le transcript du débat, sous forme de liste de dictionnaires avec les clés "speaker" et "message".
    """
    conversation = []
    
    # Récupérer les prompts de base des personas
    base_om = get_om_persona(mode)
    base_psg = get_psg_persona(mode)
    
    # Ajout de l'instruction factuelle pour les personnalités autres que Footix (Troll)
    if om_personality.lower() != "footix (troll)":
        om_extra = " Veuillez fournir uniquement des informations factuelles, vérifiées et à jour."
    else:
        om_extra = ""
    if psg_personality.lower() != "footix (troll)":
        psg_extra = " Veuillez fournir uniquement des informations factuelles, vérifiées et à jour."
    else:
        psg_extra = ""
    
    # Construire la base de prompt pour chaque IA
    om_prompt_base = (
        f"Personnalité OM: {om_personality} | Mode: {mode}. "
        f"{base_om}{om_extra} Réponds en tant que fervent supporter de l'Olympique de Marseille avec tes arguments uniques."
    )
    psg_prompt_base = (
        f"Personnalité PSG: {psg_personality} | Mode: {mode}. "
        f"{base_psg}{psg_extra} Réponds en tant que fervent supporter du Paris Saint-Germain avec tes arguments uniques."
    )
    
    # Premier tour : OM répond à la question initiale
    om_prompt = f"{om_prompt_base}\nQuestion: {initial_question}"
    logging.info("Envoi du prompt OM: %s", om_prompt)
    om_response = generate_response(om_prompt, model="llama3.2")
    conversation.append({"speaker": "OM", "message": om_response})
    time.sleep(1)
    
    # Premier tour : PSG réagit à la réponse de l'OM
    psg_prompt = f"{psg_prompt_base}\nRéaction à la réponse de l'OM: {om_response}\nQuestion: {initial_question}"
    logging.info("Envoi du prompt PSG: %s", psg_prompt)
    psg_response = generate_response(psg_prompt, model="llama3.2")
    conversation.append({"speaker": "PSG", "message": psg_response})
    time.sleep(1)
    
    current_turn = 2
    while current_turn < max_turns:
        # Tour suivant pour OM
        om_followup_prompt = f"{om_prompt_base}\nRéaction à la réponse du PSG: {psg_response}\nQuestion: {initial_question}"
        logging.info("Envoi du prompt OM (tour %d): %s", current_turn+1, om_followup_prompt)
        om_response = generate_response(om_followup_prompt, model="llama3.2")
        conversation.append({"speaker": "OM", "message": om_response})
        current_turn += 1
        if current_turn >= max_turns:
            break
        # Tour suivant pour PSG
        psg_followup_prompt = f"{psg_prompt_base}\nRéaction à la réponse de l'OM: {om_response}\nQuestion: {initial_question}"
        logging.info("Envoi du prompt PSG (tour %d): %s", current_turn+1, psg_followup_prompt)
        psg_response = generate_response(psg_followup_prompt, model="llama3.2")
        conversation.append({"speaker": "PSG", "message": psg_response})
        current_turn += 1
        time.sleep(1)
        
    return conversation

if __name__ == "__main__":
    transcript = start_debate(
        "Quel club est le plus grand en Europe ?",
        mode="standard",
        max_turns=4,
        om_personality="Standard",
        psg_personality="Ultra"
    )
    for entry in transcript:
        print(f"{entry['speaker']} dit :\n{entry['message']}\n{'-'*40}")