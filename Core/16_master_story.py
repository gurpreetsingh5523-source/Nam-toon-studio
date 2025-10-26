# AmritCore V2 - FINAL MASTER STORY DATA STRUCTURE (FIXED)

# --- THE FIX: Installing all required dependencies ---
!pip install moviepy gTTS pydub numpy

import json
import os
import numpy as np
from gtts import gTTS # Now correctly imported
# The rest of the imports are implicitly handled or not needed for this script

# --- FINAL MASTER STORY DATA STRUCTURE ---
# Dialogue Data (The complete, structured data for the Brain)
scene1_dialogues = [
    {"character": "Krishna", "emotion": "Calmness", "volume": 1.0, "text": "ਸੁਲਤਾਨਾ, ਕਦੇ ਸੋਚਿਆ ਈ, ਆਪਾਂ ਵੀ ਕਦੀ ਸ਼ਹਿਰ ਜਾਈਏ?"},
    {"character": "Sultan", "emotion": "Doubt", "volume": 0.8, "text": "ਸ਼ਹਿਰ? ਕੀ ਹੋ ਗਿਆ? ਮੈਂ ਤਾਂ ਇੱਥੇ ਖੇਤਾਂ ਵਿੱਚ ਖੁਸ਼ ਆਂ।"},
    {"character": "Krishna", "emotion": "Hope", "volume": 1.0, "text": "ਕੁਝ ਵੱਡਾ ਕਰਨਾ ਚਾਹੁੰਦਾ ਹਾਂ। ਮੇਰੇ ਅੰਦਰ ਬਹੁਤ ਹੌਸਲਾ ਹੈ।"},
    {"character": "Sultan", "emotion": "Affection", "volume": 0.8, "text": "ਠੀਕ ਹੈ, ਕ੍ਰਿਸ਼ਨਾ। ਆਪਣੀ ਹਿੰਮਤ ਨਾ ਹਾਰੀਂ। ਸਾਡੀ ਦੋਸਤੀ ਹਮੇਸ਼ਾ ਤੇਰੇ ਨਾਲ ਰਹੇਗੀ।"}
]

scene3_dialogues = [
    {"character": "Sant Kaur", "emotion": "Worry", "volume": 1.0, "text": "ਕ੍ਰਿਸ਼ਨਾ, ਕੀ ਤੂੰ ਸੱਚਮੁੱਚ ਜਾ ਰਿਹਾ ਹੈਂ? ਮੇਰਾ ਦਿਲ ਡਰਦਾ ਹੈ।"},
    {"character": "Krishna", "emotion": "Determination", "volume": 1.0, "text": "ਮਾਂ, ਮੈਂ ਵਾਅਦਾ ਕਰਦਾ ਹਾਂ। ਮੈਂ ਤੁਹਾਡੇ ਲਈ ਜ਼ਰੂਰ ਕੁਝ ਵਧੀਆ ਬਣਾਵਾਂਗਾ।"},
    {"character": "Sant Kaur", "emotion": "Affection/Grief", "volume": 0.9, "text": "ਰੱਬ ਤੈਨੂੰ ਬਰਕਤ ਬਖ਼ਸ਼ੇ, ਪਰ ਮੈਨੂੰ ਤੇਰੀ ਬਹੁਤ ਯਾਦ ਆਵੇਗੀ, ਪੁੱਤ।"},
    {"character": "Krishna", "emotion": "Sadness/Gratitude", "volume": 1.0, "text": "ਬਾਬੇ ਨਾਨਕ ਦਾ ਹੱਥ ਹੈ ਮਾਂ। ਮੈਂ ਜਲਦੀ ਵਾਪਸ ਆਵਾਂਗਾ।"}
]


MASTER_STORY_DATA = {
    "title": "Tootan Wala Khooh - The Journey Begins",
    "total_scenes": 2,
    "scenes": [
        {"scene_id": "SCENE_1_MEETING", "setting": "Village_Well_Day", "dialogues": scene1_dialogues},
        {"scene_id": "SCENE_3_FAREWELL", "setting": "Krishna's_Home_Morning", "dialogues": scene3_dialogues}
    ]
}

# --- SAVE THE MASTER DATA ---
MASTER_FILE_PATH = "master_story_data.json"
with open(MASTER_FILE_PATH, 'w', encoding='utf-8') as f:
    # Save the data in a beautiful, structured JSON format
    json.dump(MASTER_STORY_DATA, f, ensure_ascii=False, indent=4)
    
print("--- AMRIT CORE V2: STORY CONSOLIDATED ---")
print(f"Master Story Data created successfully. Total Scenes: {MASTER_STORY_DATA['total_scenes']}")
print(f"Find the Master Story File: {MASTER_FILE_PATH}")
