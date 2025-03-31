#!/usr/bin/env python3
"""
Module: knowledge_retriever.py
Description: Extrait des faits marquants sur l'OM et le PSG à partir de fichiers de données.
Si les fichiers ne sont pas disponibles, renvoie un fait par défaut.
"""

import os
import pandas as pd

def get_om_fact():
    data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../data/om/stats_om.csv")
    try:
        df = pd.read_csv(data_path)
        if 'fact' in df.columns and not df['fact'].empty:
            fact = df['fact'].iloc[0]
            return f"Fait OM: {fact}"
        else:
            return "Fait OM: L'OM a remporté la Ligue des Champions en 1993."
    except Exception as e:
        return "Fait OM: L'OM a remporté la Ligue des Champions en 1993."

def get_psg_fact():
    data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../data/psg/stats_psg.csv")
    try:
        df = pd.read_csv(data_path)
        if 'fact' in df.columns and not df['fact'].empty:
            fact = df['fact'].iloc[0]
            return f"Fait PSG: {fact}"
        else:
            return "Fait PSG: Le PSG est soutenu par d'importants investissements."
    except Exception as e:
        return "Fait PSG: Le PSG est soutenu par d'importants investissements."

if __name__ == "__main__":
    print("Test get_om_fact():")
    print(get_om_fact())
    print("\nTest get_psg_fact():")
    print(get_psg_fact())