#!/usr/bin/env python3
"""
Module: data_cleaning.py
Description: Fournit une fonction pour nettoyer et normaliser les données, par exemple, en nettoyant les noms de colonnes.
"""

def clean_data(df):
    """
    Nettoie un DataFrame en supprimant les espaces autour des noms de colonnes et en les convertissant en minuscules.

    Args:
        df (DataFrame): Le DataFrame à nettoyer.

    Returns:
        DataFrame: Le DataFrame avec des noms de colonnes nettoyés.
    """
    df.columns = [col.strip().lower() for col in df.columns]
    return df

if __name__ == "__main__":
    import pandas as pd
    # Exemple de DataFrame pour tester la fonction
    df = pd.DataFrame({
        " Column1 ": [1, 2, 3],
        " Column2 ": ["a", "b", "c"]
    })
    print("Avant nettoyage :", df.columns)
    df_clean = clean_data(df)
    print("Après nettoyage :", df_clean.columns)