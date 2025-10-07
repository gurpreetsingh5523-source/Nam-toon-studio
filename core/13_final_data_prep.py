# AmritCore - Master Prompt Test (ABSOLUTE FINAL LOCAL FIX)

!pip install requests

import os

# --- Step 1: Define the Brain's Master Task (Data is hardcoded for reliability) ---
MASTER_PROMPT_CONTENT = """
A hyper-detailed, photorealistic, and culturally accurate wide-shot scene of a traditional Punjabi village well. The well is old brick, surrounded by very dense, gnarled mulberry trees (toot). The time is golden hour afternoon. In the foreground, two young men, KRISHNA and SULTAN, are talking. Krishna is standing with a hopeful posture, Sultan is sitting with a worried posture. Add subtle ambient details like a bullock cart trail and a few small birds. The lighting must be cinematic and warm.
"""

def save_master_prompt(content):
    MASTER_PROMPT_PATH = "master_prompt.txt"
    try:
        with open(MASTER_PROMPT_PATH, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"FATAL ERROR: Could not write local file. Error: {e}")
        return False


# --- Step 2: Test and Display ---
if save_master_prompt(MASTER_PROMPT_CONTENT):
    print("--- MASTER PROMPT STATUS: SUCCESS ---")
    print("\nNext Task for AmritCore V2 (Your New Laptop):")
    print("------------------------------------------")
    print(MASTER_PROMPT_CONTENT)
    print("------------------------------------------")
    print("The Studio is READY. We have successfully prepared all data locally!")
else:
    print("FATAL ERROR: Could not save the Master Prompt locally.")
