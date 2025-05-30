import unittest
from src.llm_interface.ollama_interface import generate_response

class TestOllamaInterface(unittest.TestCase):
    def test_basic_prompt(self):
        """Vérifie qu'un prompt simple renvoie une réponse non vide."""
        prompt = "Bonjour!"
        response = generate_response(prompt, model="llama3.2")
        self.assertTrue(len(response) > 0, "La réponse devrait être non vide.")

if __name__ == '__main__':
    unittest.main()