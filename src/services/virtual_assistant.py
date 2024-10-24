# services/virtual_assistant.py

from transformers import pipeline

class VirtualHealthAssistant:
    def __init__(self):
        self.qa_model = pipeline("question-answering")
        self.health_tips = {
            "diet": "Eat a balanced diet rich in fruits, vegetables, and whole grains.",
            "exercise": "Aim for at least 30 minutes of moderate exercise most days of the week.",
            "hydration": "Drink plenty of water throughout the day to stay hydrated."
        }

    def answer_question(self, question: str, context: str) -> str:
        """Answer health-related questions based on the provided context."""
        result = self.qa_model(question=question, context=context)
        return result['answer']

    def get_health_tip(self, category: str) -> str:
        """Provide health tips based on the specified category."""
        return self.health_tips.get(category.lower(), "No tips available for this category.")

# Example usage:
if __name__ == "__main__":
    assistant = VirtualHealthAssistant()
    context = "A balanced diet includes a variety of foods from all food groups."
    question = "What is a balanced diet?"
    print("Answer:", assistant.answer_question(question, context))
    print("Health Tip:", assistant.get_health_tip("diet"))
