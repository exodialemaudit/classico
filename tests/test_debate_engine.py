import unittest
from src.debate_engine.conversation_manager import start_debate
from src.debate_engine.persona_manager import get_om_persona, get_psg_persona

class TestDebateEngine(unittest.TestCase):
    def test_persona_manager(self):
        om_standard = get_om_persona("standard")
        psg_standard = get_psg_persona("standard")
        self.assertTrue(len(om_standard) > 0, "Le prompt OM en mode standard doit être non vide.")
        self.assertTrue(len(psg_standard) > 0, "Le prompt PSG en mode standard doit être non vide.")
        
        om_comique = get_om_persona("comique")
        psg_clash = get_psg_persona("clash")
        self.assertTrue(len(om_comique) > 0, "Le prompt OM en mode comique doit être non vide.")
        self.assertTrue(len(psg_clash) > 0, "Le prompt PSG en mode clash doit être non vide.")
    
    def test_start_debate_transcript(self):
        initial_question = "Quel club est le plus grand en Europe ?"
        transcript = start_debate(initial_question, mode="standard", max_turns=4)
        self.assertIsInstance(transcript, list, "Le transcript doit être une liste.")
        self.assertTrue(len(transcript) > 0, "Le transcript ne doit pas être vide.")
        for entry in transcript:
            self.assertIsInstance(entry, dict, "Chaque entrée du transcript doit être un dictionnaire.")
            self.assertIn("speaker", entry, "Chaque entrée doit contenir la clé 'speaker'.")
            self.assertIn("message", entry, "Chaque entrée doit contenir la clé 'message'.")
            self.assertTrue(len(entry["message"]) > 0, "Les messages doivent être non vides.")
        speakers = [entry["speaker"] for entry in transcript]
        self.assertIn("OM", speakers, "Le transcript doit contenir un message d'OM.")
        self.assertIn("PSG", speakers, "Le transcript doit contenir un message de PSG.")

if __name__ == "__main__":
    unittest.main()