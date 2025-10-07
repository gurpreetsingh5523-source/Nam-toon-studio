# AmritCore - Scene 3 Dialogue Node (Adding New Story Logic)

import os
from gtts import gTTS
import numpy as np

# --- 1. THE BRAIN'S OUTPUT STRUCTURE (Scene 3 Data) ---
dialogues_scene3 = [
    {"character": "Sant Kaur", "emotion": "Worry", "volume": 1.0, "text": "ਕ੍ਰਿਸ਼ਨਾ, ਕੀ ਤੂੰ ਸੱਚਮੁੱਚ ਜਾ ਰਿਹਾ ਹੈਂ? ਮੇਰਾ ਦਿਲ ਡਰਦਾ ਹੈ।"},
    {"character": "Krishna", "emotion": "Determination", "volume": 1.0, "text": "ਮਾਂ, ਮੈਂ ਵਾਅਦਾ ਕਰਦਾ ਹਾਂ। ਮੈਂ ਤੁਹਾਡੇ ਲਈ ਜ਼ਰੂਰ ਕੁਝ ਵਧੀਆ ਬਣਾਵਾਂਗਾ।"},
    {"character": "Sant Kaur", "emotion": "Affection/Grief", "volume": 0.9, "text": "ਰੱਬ ਤੈਨੂੰ ਬਰਕਤ ਬਖ਼ਸ਼ੇ, ਪਰ ਮੈਨੂੰ ਤੇਰੀ ਬਹੁਤ ਯਾਦ ਆਵੇਗੀ, ਪੁੱਤ।"},
    {"character": "Krishna", "emotion": "Sadness/Gratitude", "volume": 1.0, "text": "ਬਾਬੇ ਨਾਨਕ ਦਾ ਹੱਥ ਹੈ ਮਾਂ। ਮੈਂ ਜਲਦੀ ਵਾਪਸ ਆਵਾਂਗਾ।"}
]

# --- 2. AUDIO GENERATION TEST ---
if not os.path.exists("audio"): os.makedirs("audio")
print("--- Scene 3 Dialogue Generation Status ---")

for i, dialogue in enumerate(dialogues_scene3):
    tts = gTTS(dialogue["text"], lang='pa')
    
    # We save it as a temporary file to confirm the logic works
    filename = f"audio/scene3_dialogue_{i}_{dialogue['character']}.mp3"
    tts.save(filename)
    
    print(f"Generated: [{dialogue['character']}] ({dialogue['emotion']}) - Volume: {dialogue['volume']}")

print("\nScene 3 Dialogue Node is working perfectly. Ready to save the code.")

