#!/usr/bin/env python3
"""
Module: ollama_interface.py
Description: Interface pour appeler Llama 3.2 via Ollama en utilisant subprocess.
"""

import subprocess
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def generate_response(prompt, model="llama3.2"):
    """
    Envoie un prompt au modèle via Ollama et renvoie la réponse générée.
    
    Args:
        prompt (str): Le texte à envoyer au modèle.
        model (str): Le nom du modèle (par défaut "llama3.2").
        
    Returns:
        str: La réponse générée par le modèle.
    """
    command = ["ollama", "run", model, prompt]
    logging.info("Exécution de la commande : %s", " ".join(command))
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        logging.error("Erreur lors de l'exécution de la commande ollama : %s", e)
        return ""
    except Exception as ex:
        logging.error("Autre erreur : %s", ex)
        return ""

if __name__ == "__main__":
    test_prompt = "Bonjour, peux-tu te présenter ?"
    print("Test prompt :", test_prompt)
    print("Réponse du modèle :", generate_response(test_prompt))