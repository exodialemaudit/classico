import unittest
import pandas as pd
from src.data_processing.data_loader import load_om_stats, load_psg_stats
from src.data_processing.data_cleaning import clean_data

class TestDataProcessing(unittest.TestCase):
    def test_load_om_stats(self):
        df = load_om_stats()
        self.assertIsInstance(df, pd.DataFrame, "Les stats OM doivent être retournées sous forme de DataFrame.")
        self.assertFalse(df.empty, "Le DataFrame OM ne doit pas être vide.")

    def test_load_psg_stats(self):
        df = load_psg_stats()
        self.assertIsInstance(df, pd.DataFrame, "Les stats PSG doivent être retournées sous forme de DataFrame.")
        self.assertFalse(df.empty, "Le DataFrame PSG ne doit pas être vide.")

    def test_clean_data(self):
        # Créer un DataFrame d'exemple
        df = pd.DataFrame({" Column1 ": [1, 2, 3], " Column2 ": ["a", "b", "c"]})
        df_clean = clean_data(df)
        for col in df_clean.columns:
            self.assertEqual(col, col.strip().lower(), "Les noms de colonnes doivent être nettoyés.")

if __name__ == "__main__":
    unittest.main()