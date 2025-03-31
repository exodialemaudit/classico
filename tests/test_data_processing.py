import unittest
import pandas as pd
from src.data_processing.data_cleaning import clean_data
from src.data_processing.data_loader import load_om_stats, load_psg_stats

class TestDataProcessing(unittest.TestCase):
    def test_load_om_stats(self):
        df = load_om_stats()
        self.assertIsInstance(df, pd.DataFrame, "Les statistiques OM doivent être un DataFrame.")
        self.assertTrue(not df.empty, "Le DataFrame OM ne doit pas être vide.")

    def test_load_psg_stats(self):
        df = load_psg_stats()
        self.assertIsInstance(df, pd.DataFrame, "Les statistiques PSG doivent être un DataFrame.")
        self.assertTrue(not df.empty, "Le DataFrame PSG ne doit pas être vide.")

    def test_clean_data(self):
        df = pd.DataFrame({" Column1 ": [1, 2, 3], " Column2 ": ["a", "b", "c"]})
        df_clean = clean_data(df)
        for col in df_clean.columns:
            self.assertEqual(col, col.strip().lower(), "Les colonnes doivent être normalisées.")

if __name__ == "__main__":
    unittest.main()