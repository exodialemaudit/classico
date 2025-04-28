#!/usr/bin/env python3
"""
Module: api_football_client.py
Description: Ce module interroge l'API-Football pour récupérer des informations et des statistiques sur les équipes.
Il propose également des fonctions dédiées pour obtenir les données de l'OM et du PSG.
"""

import os
import requests

# Définissez directement votre clé API ici (à remplacer par votre clé réelle)
API_KEY = "c4557313eeefad9e3d8cf744eff754bd"  
# Vous pouvez aussi utiliser : os.getenv("API_FOOTBALL_KEY") si vous préférez récupérer la clé depuis une variable d'environnement

# URL de base de l'API-Football (v3)
BASE_URL = "https://v3.football.api-sports.io"

# Headers pour authentifier les requêtes
HEADERS = {
    "x-apisports-key": API_KEY
}

def get_team_info(team_id: int):
    """
    Récupère les informations générales d'une équipe à partir de son team_id.

    Args:
        team_id (int): L'identifiant de l'équipe dans API-Football.
    
    Returns:
        dict: Les informations de l'équipe.
    """
    url = f"{BASE_URL}/teams?id={team_id}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def get_team_stats(team_id: int, season: int):
    """
    Récupère les statistiques d'une équipe pour une saison donnée.

    Args:
        team_id (int): L'identifiant de l'équipe.
        season (int): L'année de la saison (exemple: 2023).
    
    Returns:
        dict: Les statistiques de l'équipe.
    """
    url = f"{BASE_URL}/teams/statistics?team={team_id}&season={season}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def get_om_data(season: int = 2023):
    """
    Récupère les données complètes de l'Olympique de Marseille (OM).

    Args:
        season (int): Saison de référence.
    
    Returns:
        dict: Dictionnaire contenant les informations et statistiques de l'OM.
    """
    # Remplacez cet ID par l'ID réel de l'OM tel que défini par API-Football
    team_id_om = 33  
    info = get_team_info(team_id_om)
    stats = get_team_stats(team_id_om, season)
    return {"info": info, "stats": stats}

def get_psg_data(season: int = 2023):
    """
    Récupère les données complètes du Paris Saint-Germain (PSG).

    Args:
        season (int): Saison de référence.
    
    Returns:
        dict: Dictionnaire contenant les informations et statistiques du PSG.
    """
    # Remplacez cet ID par l'ID réel du PSG tel que défini par API-Football
    team_id_psg = 2  
    info = get_team_info(team_id_psg)
    stats = get_team_stats(team_id_psg, season)
    return {"info": info, "stats": stats}

if __name__ == "__main__":
    season_example = 2023
    try:
        om_data = get_om_data(season_example)
        psg_data = get_psg_data(season_example)
        print("Données OM:")
        print(om_data)
        print("\nDonnées PSG:")
        print(psg_data)
    except Exception as e:
        print("Erreur lors de l'appel à l'API-Football :", e)