# tests/test_virtual_assistant.py

import unittest
from services.virtual_assistant import VirtualHealthAssistant

class TestVirtualHealthAssistant(unittest.TestCase):
    def setUp(self):
        self.assistant = VirtualHealthAssistant()

    def test_answer_question(self):
        context = "A balanced diet includes a variety of foods from all food groups."
        question = "What is a balanced diet?"
        answer = self.assistant.answer_question(question, context)
        self.assertIn("balanced diet", answer.lower())

    def test_get_health_tip(self):
        tip = self.assistant.get_health_tip("diet")
        self.assertEqual(tip, "Eat a balanced diet rich in fruits, vegetables, and whole grains.")

    def test_get_health_tip_invalid_category(self):
        tip = self.assistant.get_health_tip("invalid")
        self.assertEqual(tip, "No tips available for this category.")

if __name__ == '__main__':
    unittest.main()
