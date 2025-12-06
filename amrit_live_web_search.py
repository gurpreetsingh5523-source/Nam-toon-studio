"""
Amrit Live Web Search & Knowledge Expansion Module

Purpose:
- Integrate real-time web search (Wikipedia, news, spiritual sites)
- Auto-update local knowledge files from trusted sources
- Gurbani-inspired humility, seva, and protection in all logic

Gurbani Teachings:
- Nimmarta (Humility): "Nanak Neech Kahai Veechar" – Har search vich nimmarta.
- Protection: "Rakhe Rakhanhaar aap ubaariyan" – User te system protection.
- Seva: "Seva karat hoey nihkam" – Har update seva de roop vich.
"""

import requests
import os

def search_wikipedia(query):
    print("Nanak Neech Kahai Veechar: Searching Wikipedia with humility.")
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query.replace(' ', '_')}"
    resp = requests.get(url)
    if resp.status_code == 200:
        data = resp.json()
        return data.get('extract', 'No summary found.')
    return "No result found."

def update_knowledge_file(query, answer, knowledge_file="brain_07_gyan_vigyan.txt"):
    print("Seva: Auto-updating knowledge file with new info.")
    entry = f"Q: {query}\nA: {answer}\n"
    with open(knowledge_file, "a") as f:
        f.write(entry)
    print("Knowledge file updated.")

def live_search_and_update(query, knowledge_file="brain_07_gyan_vigyan.txt"):
    print("Rakhe Rakhanhaar: User and system protected during search.")
    answer = search_wikipedia(query)
    update_knowledge_file(query, answer, knowledge_file)
    return answer

# Example usage
if __name__ == "__main__":
    q = "Guru Nanak"
    ans = live_search_and_update(q)
    print(f"Answer: {ans}")
