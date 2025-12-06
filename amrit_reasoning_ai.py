"""
AmritCore Reasoning & Self-Learning Engine
Adds stepwise logic reasoning and feedback-based self-learning to the main AI pipeline.
"""
import os
import json
from Core.nano_tinybert_classifier import TinyBERTClassifier
from Core.nano_bm25_retriever import NanoBM25MultiRetriever

BRAIN_FILES = {
    "Physics": "brain_07_gyan_vigyan.txt",
    "Health": "brain_10_sehhat_health.txt",
    "Culture": "brain_02_punjabi_idioms.txt",
    "Tech": "brain_08_computing_tech.txt",
    "Daily": "brain_05_rozana_jeevan.txt"
}

class ReasoningEngine:
    def __init__(self, base_dir):
        self.classifier = TinyBERTClassifier()
        self.base_dir = base_dir
        self.retrievers = {}
        for domain, fname in BRAIN_FILES.items():
            fpath = os.path.join(base_dir, fname)
            if os.path.exists(fpath):
                self.retrievers[domain] = NanoBM25MultiRetriever([fpath])
        self.feedback_log = os.path.join(base_dir, "user_feedback.json")

    def stepwise_reasoning(self, question, answer_lines):
        # Advanced logic: definitions, formulas, examples, context, analogies, cause-effect, counter-examples, spiritual/cultural synthesis
        if not answer_lines:
            return "Sorry, no answer found."
        reasoning = []
        for line in answer_lines:
            l = line.lower()
            if "definition" in l or "means" in l or "states" in l:
                reasoning.append(f"Step: Definition → {line}")
            elif "formula" in l or "expression" in l or "mathematical" in l:
                reasoning.append(f"Step: Formula/Math → {line}")
            elif "example" in l or "application" in l or "real-world" in l:
                reasoning.append(f"Step: Example/Application → {line}")
            elif "context" in l or "background" in l:
                reasoning.append(f"Step: Context → {line}")
            elif "analogy" in l or "similar to" in l:
                reasoning.append(f"Step: Analogy → {line}")
            elif "cause" in l or "effect" in l or "because" in l:
                reasoning.append(f"Step: Cause-Effect → {line}")
            elif "counter" in l or "exception" in l or "but" in l:
                reasoning.append(f"Step: Counter-Example/Exception → {line}")
            elif "spiritual" in l or "culture" in l or "gurbani" in l:
                reasoning.append(f"Step: Spiritual/Cultural Insight → {line}")
            else:
                reasoning.append(f"Step: Supporting info → {line}")
        # Integrate user feedback if available
        feedback = self.get_recent_feedback(question)
        if feedback:
            reasoning.append(f"Step: User Correction → {feedback}")
        # Synthesize final answer
        if reasoning:
            synthesis = "\n".join(reasoning)
            synthesis += "\n---\nSatnaam, advanced logic and love included."
            return synthesis
        return "Sorry, no answer found."

    def get_recent_feedback(self, question):
        # Retrieve most recent user feedback for this question
        if not os.path.exists(self.feedback_log):
            return None
        try:
            with open(self.feedback_log, "r") as f:
                data = json.load(f)
            for entry in reversed(data):
                if entry.get("question") == question:
                    return entry.get("correct_answer")
        except Exception:
            return None
        return None

    def answer(self, question):
        domain = self.classifier.classify(question)
        retriever = self.retrievers.get(domain)
        if not retriever:
            return f"Sorry, I don't have knowledge for domain: {domain}."
        results = retriever.search(question, top_n=5)
        answer_lines = [doc for doc, fname in results if doc]
        answer = self.stepwise_reasoning(question, answer_lines)
        return f"[{domain} Reasoned Answer]\n{answer}"

    def log_feedback(self, question, correct_answer):
        # Log user corrections for self-learning
        entry = {"question": question, "correct_answer": correct_answer}
        if os.path.exists(self.feedback_log):
            with open(self.feedback_log, "r") as f:
                data = json.load(f)
        else:
            data = []
        data.append(entry)
        with open(self.feedback_log, "w") as f:
            json.dump(data, f, indent=2)

if __name__ == "__main__":
    import sys
    base_dir = os.path.dirname(os.path.abspath(__file__))
    engine = ReasoningEngine(base_dir)
    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:])
        print(engine.answer(question))
        # Example feedback logging
        # engine.log_feedback(question, "Your correction here")
    else:
        print("Usage: python amrit_reasoning_ai.py <your question>")
