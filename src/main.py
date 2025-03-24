#!/usr/bin/env python3
"""
Script de démo pour Classico Foot LLM
Ce script envoie un prompt au modèle Llama 3.2 via Ollama et affiche la réponse générée.
"""

from llm_interface.ollama_interface import generate_response

def main():
    print("=== Démo de l'appel au LLM (Llama 3.2) via Ollama ===\n")
    
    # Définir le prompt à envoyer
    prompt = "Décris un fait drôle sur l'Olympique de Marseille."
    print("Prompt envoyé :", prompt)
    
    # Appeler la fonction generate_response et récupérer la réponse
    response = generate_response(prompt, model="llama3.2")
    
    # Vérifier et afficher la réponse
    if response:
        print("\nRéponse du modèle :")
        print(response)
    else:
        print("\nAucune réponse générée. Vérifiez la configuration d'Ollama et le modèle.")

if __name__ == "__main__":
    main()