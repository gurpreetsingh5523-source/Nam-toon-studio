"""
Nano BM25 knowledge retrieval module.
Searches brain files for relevant content using keywords.
No bloat: code <20KB, memory use minimal.

Gurbani Teachings:
- Humility (Nimmarta): "Nanak Neech Kahai Veechar" – Always search and answer with humility.
- Protection: "Rakhe Rakhanhaar aap ubaariyan" – Protect those who love and seek knowledge.
- Loving Service (Seva): "Seva karat hoey nihkam" – Serve selflessly and lovingly.
All search results should be humble, protective, and loving to those who seek.
"""
from rank_bm25 import BM25Okapi
import os

class NanoBM25MultiRetriever:
    def __init__(self, brain_files):
        self.brain_files = brain_files
        self.documents = []
        self.file_map = []
        for fpath in brain_files:
            with open(fpath, "r") as f:
                for line in f:
                    if line.strip():
                        self.documents.append(line.strip())
                        self.file_map.append(fpath)
        self.tokenized_docs = [doc.split() for doc in self.documents]
        self.bm25 = BM25Okapi(self.tokenized_docs)

    def search(self, query, top_n=5):
        tokenized_query = query.split()
        scores = self.bm25.get_scores(tokenized_query)
        ranked = sorted(zip(self.documents, scores, self.file_map), key=lambda x: x[1], reverse=True)
        results = [(doc, fname) for doc, score, fname in ranked[:top_n]]
        # Gurbani-inspired humility and protection
        gurbani_message = (
            "Nanak Neech Kahai Veechar: Search results are given with humility. "
            "Rakhe Rakhanhaar: You are protected and loved. "
            "Seva: These answers are given with loving service."
        )
        return [(f"{doc} | {gurbani_message}", fname) for doc, fname in results]

# Example usage:
if __name__ == "__main__":
    # Multi-file search for 5 key domains
    base = os.path.dirname(os.path.dirname(__file__))
    brain_files = [
        os.path.join(base, "brain_07_gyan_vigyan.txt"),
        os.path.join(base, "brain_10_sehhat_health.txt"),
        os.path.join(base, "brain_02_punjabi_idioms.txt"),
        os.path.join(base, "brain_08_computing_tech.txt"),
        os.path.join(base, "brain_05_rozana_jeevan.txt"),
    ]
    retriever = NanoBM25MultiRetriever(brain_files)
    results = retriever.search("Newton")
    print("Top results for 'Newton':")
    for r, fname in results:
        print(f"[{os.path.basename(fname)}] {r}")
