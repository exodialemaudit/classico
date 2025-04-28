import os
import pandas as pd

def load_om_stats():
    """
    Charge les statistiques de l'OM à partir du fichier CSV situé dans data/om/stats_om.csv.
    Si le fichier n'existe pas, il est créé avec des données d'exemple.
    
    Returns:
        DataFrame: Un DataFrame contenant les statistiques de l'OM.
    """
    # Construire le chemin vers le fichier CSV
    data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../data/om/stats_om.csv")
    
    # Si le fichier n'existe pas, on crée un fichier d'exemple
    if not os.path.exists(data_path):
        sample_data = {
            "fact": ["L'OM a remporté la Ligue des Champions en 1993."],
            "wins": [10],
            "draws": [5],
            "losses": [3]
        }
        df_sample = pd.DataFrame(sample_data)
        # Crée le dossier s'il n'existe pas
        os.makedirs(os.path.dirname(data_path), exist_ok=True)
        df_sample.to_csv(data_path, index=False)
        return df_sample
    
    return pd.read_csv(data_path)

def load_psg_stats():
    """
    Charge les statistiques du PSG à partir du fichier CSV situé dans data/psg/stats_psg.csv.
    Si le fichier n'existe pas, il est créé avec des données d'exemple.
    
    Returns:
        DataFrame: Un DataFrame contenant les statistiques du PSG.
    """
    # Construire le chemin vers le fichier CSV
    data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../data/psg/stats_psg.csv")
    
    # Si le fichier n'existe pas, on crée un fichier d'exemple
    if not os.path.exists(data_path):
        sample_data = {
            "fact": ["Le PSG a remporté plusieurs titres de champion de France."],
            "wins": [15],
            "draws": [4],
            "losses": [2]
        }
        df_sample = pd.DataFrame(sample_data)
        # Crée le dossier s'il n'existe pas
        os.makedirs(os.path.dirname(data_path), exist_ok=True)
        df_sample.to_csv(data_path, index=False)
        return df_sample
    
    return pd.read_csv(data_path)

if __name__ == "__main__":
    print("OM Stats:")
    print(load_om_stats().head())
    print("PSG Stats:")
    print(load_psg_stats().head())