#!/usr/bin/env python3
"""
Module: ollama_interface.py
Description: Ce module fournit une interface pour appeler le modèle LLM via Ollama en utilisant subprocess.
La fonction principale, generate_response, envoie un prompt au modèle spécifié et retourne la réponse générée.
"""

import subprocess
import logging

# Configuration du logging (vous pouvez adapter le niveau et le format selon vos besoins)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def generate_response(prompt, model="llama3.2"):
    """
    Envoie une requête au modèle Llama via Ollama en utilisant subprocess.

    Args:
        prompt (str): Le texte à envoyer au modèle.
        model (str): Le nom du modèle à utiliser (par défaut "llama3.2").

    Returns:
        str: La réponse générée par le modèle, ou une chaîne vide en cas d'erreur.
    
    Exemple:
        response = generate_response("Bonjour, qui es-tu ?", model="llama3.2")
    """
    # Préparer la commande à exécuter.
    # La syntaxe utilisée ici est : ollama run <model> <prompt>
    command = ["ollama", "run", model, prompt]
    
    logging.info("Exécution de la commande : %s", " ".join(command))
    
    try:
        # Exécute la commande et capture la sortie.
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        logging.info("Commande exécutée avec succès.")
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        logging.error("Erreur lors de l'exécution de la commande ollama : %s", e)
        logging.error("Sortie : %s", e.output)
        return ""
    except Exception as ex:
        logging.error("Une erreur inattendue est survenue : %s", ex)
        return ""

# Bloc de test optionnel pour exécuter le module directement
if __name__ == "__main__":
    test_prompt = "Bonjour, peux-tu te présenter ?"
    print("Test prompt :", test_prompt)
    response = generate_response(test_prompt)
    print("Réponse du modèle :", response)