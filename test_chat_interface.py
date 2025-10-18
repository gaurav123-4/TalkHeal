import unittest
from components import chat_interface

class TestChatInterface(unittest.TestCase):
    def test_get_personality_list(self):
        personalities = chat_interface.get_personality_list()
        self.assertIsInstance(personalities, list)
        self.assertGreater(len(personalities), 0)

    def test_generate_response(self):
        # This is a basic test; in real cases, mock AI responses
        user_input = "I feel stressed."
        personality = "Compassionate Listener"
        response = chat_interface.generate_response(user_input, personality)
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 0)

if __name__ == "__main__":
    unittest.main()
