"""
AmritCore Main AI Pipeline (Smartest Local AI)
Integrates TinyBERT NLP, BM25 search, smart routing, and real answer extraction.
"""
import os
from Core.nano_tinybert_classifier import TinyBERTClassifier
from Core.nano_bm25_retriever import NanoBM25MultiRetriever

# Map domain to brain file
BRAIN_FILES = {
    "Physics": "brain_07_gyan_vigyan.txt",
    "Health": "brain_10_sehhat_health.txt",
    "Culture": "brain_02_punjabi_idioms.txt",
    "Tech": "brain_08_computing_tech.txt",
    "Daily": "brain_05_rozana_jeevan.txt"
}

class AmritCoreAI:
    def __init__(self, base_dir):
        self.classifier = TinyBERTClassifier()
        self.base_dir = base_dir
        self.retrievers = {}
        for domain, fname in BRAIN_FILES.items():
            fpath = os.path.join(base_dir, fname)
            if os.path.exists(fpath):
                self.retrievers[domain] = NanoBM25MultiRetriever([fpath])

    def answer(self, question):
        domain = self.classifier.classify(question)
        retriever = self.retrievers.get(domain)
        if not retriever:
            return f"Sorry, I don't have knowledge for domain: {domain}."
        results = retriever.search(question, top_n=3)
        if results:
            answer_lines = [doc for doc, fname in results if doc]
            answer = "\n".join(answer_lines)
            return f"[{domain} Answer]\n{answer}"
        else:
            return f"[{domain}] Sorry, no answer found."

if __name__ == "__main__":
    import sys
    base_dir = os.path.dirname(os.path.abspath(__file__))
    ai = AmritCoreAI(base_dir)
    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:])
        print(ai.answer(question))
    else:
        print("Usage: python amrit_main_ai.py <your question>")
