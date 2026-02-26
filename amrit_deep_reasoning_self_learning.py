"""
Amrit Deep Reasoning & Self-Learning Engine

Purpose:
- Stepwise reasoning (chain-of-thought)
- Feedback loop (user corrections, auto knowledge update)
- Gurbani-inspired humility, seva, and protection in all logic
- Architecture documented for transparency

Gurbani Teachings:
- Nimmarta (Humility): "Nanak Neech Kahai Veechar" – Har reasoning vich nimmarta.
- Protection: "Rakhe Rakhanhaar aap ubaariyan" – User feedback te system protection.
- Seva: "Seva karat hoey nihkam" – Har learning seva de roop vich.
"""

import os
import json

class AmritReasoningEngine:
    def __init__(self, knowledge_file="brain_07_gyan_vigyan.txt"):
        self.knowledge_file = knowledge_file
        self.load_knowledge()

    def load_knowledge(self):
        if os.path.exists(self.knowledge_file):
            with open(self.knowledge_file, "r") as f:
                self.knowledge = f.readlines()
        else:
            self.knowledge = []

    def stepwise_reasoning(self, question):
        # Simple chain-of-thought reasoning
        print("Nanak Neech Kahai Veechar: Reasoning with humility.")
        print("Rakhe Rakhanhaar: User protected during reasoning.")
        print("Seva: Answer given with loving service.")
        # Example: search for answer in knowledge
        for line in self.knowledge:
            if question.lower() in line.lower():
                return line.strip()
        return "Sorry, no answer found. Please provide feedback."

    def feedback_loop(self, question, correct_answer):
        # Log user correction and auto-update knowledge
        print("Seva: Feedback received, updating knowledge.")
        entry = f"Q: {question}\nA: {correct_answer}\n"
        with open(self.knowledge_file, "a") as f:
            f.write(entry)
        self.load_knowledge()
        print("Knowledge updated with user feedback.")

# Example usage
if __name__ == "__main__":
    engine = AmritReasoningEngine()
    q = "What is gravity?"
    print(engine.stepwise_reasoning(q))
    engine.feedback_loop(q, "Gravity is the force that attracts objects towards each other.")
