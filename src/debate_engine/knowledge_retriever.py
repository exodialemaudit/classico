#!/usr/bin/env python3
"""
Module: knowledge_retriever.py
Description: Extrait et formate des faits clés sur l'OM et le PSG à partir des données récupérées via API-Football.
"""

from src.data_processing.api_data_loader import load_om_data, load_psg_data
from src.data_processing.data_cleaning import clean_team_info, clean_team_stats

def get_om_fact(season: int = 2023) -> str:
    """
    Récupère et formate un fait marquant sur l'OM.
    
    Args:
        season (int): La saison pour laquelle récupérer les statistiques.
    
    Returns:
        str: Un fait formaté sur l'OM.
    """
    data = load_om_data(season)
    info = clean_team_info(data["info"])
    stats = clean_team_stats(data["stats"])
    # Exemple : utiliser le nombre de victoires comme fait marquant
    wins = stats.get("wins", "N/A")
    team_name = info.get("team", "L'OM")
    return f"{team_name} a remporté {wins} matchs cette saison."

def get_psg_fact(season: int = 2023) -> str:
    """
    Récupère et formate un fait marquant sur le PSG.
    
    Args:
        season (int): La saison pour laquelle récupérer les statistiques.
    
    Returns:
        str: Un fait formaté sur le PSG.
    """
    data = load_psg_data(season)
    info = clean_team_info(data["info"])
    stats = clean_team_stats(data["stats"])
    wins = stats.get("wins", "N/A")
    team_name = info.get("team", "Le PSG")
    return f"{team_name} a remporté {wins} matchs cette saison."

if __name__ == "__main__":
    print("Fait OM :", get_om_fact())
    print("Fait PSG :", get_psg_fact())