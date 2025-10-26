# AmritCore - 07_Bariki_Brain_Setup.py (Defining all Subtle Details)

import os

# --- 1. THE BARIKI BRAIN: STORING ALL SUBTLETY ---
# This dictionary stores all the fine-grained instructions for the Synthesis Node.
def get_scene_bariki():
    """
    Returns the complete, detailed data structure for Scene 1 (The Thinking Node's Output).
    """
    return {
        "scene_id": "SCENE_1_THE_WELL",
        "visuals": {
            "image_description": "A close-up of two young Punjabi men standing near an old brick well, surrounded by tall, sun-drenched mulberry trees. Golden hour lighting.",
            "character_pose": "Krishna standing, Sultan sitting on the well's edge."
        },
        "audio_layers": {
            "music_mood": "Affectionate and melancholic flute melody (Low Volume)",
            "sfx_1_primary": "Peacock crying in the distance (High frequency SFX)",
            "sfx_2_secondary": "Rustling of dry leaves and gentle wind (Ambient noise)",
            "sfx_3_tertiary": "Sound of the well bucket dropping and rope creaking (Contextual SFX)"
        },
        "dialogue_flow": [
            {"character": "Krishna", "emotion": "Calmness", "volume": 1.0, "text": "ਸੁਲਤਾਨਾ, ਕਦੇ ਸੋਚਿਆ ਈ, ਆਪਾਂ ਵੀ ਕਦੀ ਸ਼ਹਿਰ ਜਾਈਏ?"},
            {"character": "Sultan", "emotion": "Doubt", "volume": 0.8, "text": "ਕ੍ਰਿਸ਼ਨਾ, ਮੈਂ ਤਾਂ ਏਸੇ ਪਿੰਡ ਵਿੱਚ ਖੁਸ਼ ਆਂ। ਬਸ ਰੱਬ ਸੁੱਖ ਰੱਖੇ, ਆਪਣੀ ਦੋਸਤੀ ਕਾਇਮ ਰਹੇ।"},
            {"character": "Krishna", "emotion": "Hope", "volume": 1.0, "text": "ਰੱਬ ਜ਼ਰੂਰ ਸੁੱਖ ਰੱਖੇਗਾ। ਆਹ ਤੂਤਾਂ ਵਾਲਾ ਖੂਹ ਹਮੇਸ਼ਾ ਆਪਣੀ ਦੋਸਤੀ ਦਾ ਗਵਾਹ ਰਹੇਗਾ।"}
        ]
    }

# --- 2. Test the Brain ---
scene_data = get_scene_bariki()

if scene_data:
    print("--- Bariki Brain Status: SUCCESS ---")
    print(f"Loaded Scene: {scene_data['scene_id']}")
    print(f"Required Visuals: {scene_data['visuals']['image_description'][:50]}...")
    print(f"Required SFX: {scene_data['audio_layers']['sfx_1_primary']}")
    print("The Studio Brain is now highly intelligent and structured.")
    print("\nReady for the Synthesis Node (creating these detailed assets)!")

