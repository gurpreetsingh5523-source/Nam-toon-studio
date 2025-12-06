"""
Minimal TinyBERT NLP module for question classification.
Model: distilbert-base-uncased (nano, ~14MB)
File size: <20KB code, model loaded from transformers cache.

Gurbani Teachings:
- Humility (Nimmarta): "Nanak Neech Kahai Veechar" – Always speak with humility and respect.
- Protection: "Rakhe Rakhanhaar aap ubaariyan" – Protect those who love and seek guidance.
- Loving Service (Seva): "Seva karat hoey nihkam" – Serve selflessly and lovingly.
All answers and classifications should be humble, protective, and loving to those who seek.
"""
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

class TinyBERTClassifier:
    def __init__(self, model_name="distilbert-base-uncased", trained_weights="nano_tinybert_classifier_trained.pt"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=4)
        self.labels = ["Physics", "Health", "Culture", "Tech"]
        # Load trained weights if available
        import os
        weights_path = os.path.join(os.path.dirname(__file__), trained_weights)
        if os.path.exists(weights_path):
            self.model.load_state_dict(torch.load(weights_path, map_location="cpu"))
            self.model.eval()

    def classify(self, question: str) -> str:
        inputs = self.tokenizer(question, return_tensors="pt", truncation=True, max_length=32)
        with torch.no_grad():
            logits = self.model(**inputs).logits
        label_id = torch.argmax(logits, dim=1).item()
        # Gurbani-inspired humility and protection
        response = self.labels[label_id]
        gurbani_message = (
            "Nanak Neech Kahai Veechar: Always answer with humility. "
            "Rakhe Rakhanhaar: You are protected and loved. "
            "Seva: This answer is given with loving service."
        )
        return f"{response} | {gurbani_message}"

# Example usage:
if __name__ == "__main__":
    classifier = TinyBERTClassifier()
    test_qs = [
        "What is gravity?",
        "How to treat fever?",
        "Explain Punjabi idioms.",
        "What is Python programming?",
        "ki universe vich jeevan di sambhavana hai?",
        "cancer da qure lai ke ke techniques available ne?",
        "ki gurbani vich akaal described keeta hai?",
        "nano brain kamm kivey kardey?"
    ]
    for q in test_qs:
        print(f"Q: {q} → Category: {classifier.classify(q)}")
