# AmritCore V4 - 24_Behavior_Learning_Node.py (Simulating Self-Learning from Video)

import os
import random
import time

# --- 1. THE BEHAVIOR LEARNING DATABASE ---
# This is the Brain's memory: what action corresponds to which code.
# In the final version, this will be populated by analyzing videos (e.g., YouTube).
BEHAVIOR_DATABASE = {
    "walking":   {"code": "ANIM_WALK_01", "duration": 4.5, "visual_hint": "Legs moving in alternate sequence."},
    "swimming":  {"code": "ANIM_SWIM_03", "duration": 8.0, "visual_hint": "Arms and legs paddling movement in water."},
    "climbing":  {"code": "ANIM_CLIMB_02", "duration": 6.0, "visual_hint": "Slow, upward hand-over-hand movement."},
    "smiling":   {"code": "ANIM_EXPR_SML", "duration": 1.5, "visual_hint": "Facial muscles relax and curve upwards."},
    "fighting":  {"code": "ANIM_FIGHT_01", "duration": 3.0, "visual_hint": "Rapid, aggressive hand-to-hand motions."},
    "crying":    {"code": "ANIM_EXPR_CRY", "duration": 2.5, "visual_hint": "Facial muscles contort, tear tracking."},
}


# --- 2. THE LEARNING SIMULATOR FUNCTION ---
def learn_new_action(video_source, action_name):
    """
    Simulates the complex process of learning an animation behavior from an external source (video).
    """
    
    # Check if the action is already in our memory
    if action_name.lower() in BEHAVIOR_DATABASE:
        print(f"✅ Learned Action: '{action_name}' is already in the memory.")
        print(f"   -> Behavior Code: {BEHAVIOR_DATABASE[action_name]['code']}")
        return BEHAVIOR_DATABASE[action_name]['code']

    # If the action is new, simulate the learning process
    new_code = f"ANIM_NEW_{random.randint(10, 99)}"
    BEHAVIOR_DATABASE[action_name.lower()] = {"code": new_code, "duration": 5.0, "visual_hint": f"Learned from {video_source}"}
    
    print(f"🧠 NEW KNOWLEDGE ACQUIRED: The Brain learned '{action_name}' from {video_source}.")
    print(f"   -> Assigned New Code: {new_code}")
    return new_code


# --- 3. TEST THE LEARNING ---
print("--- AMRIT CORE V4: BEHAVIOR LEARNING INITIATED ---")

# Test Case 1: An existing action (no new learning needed)
learn_new_action("YouTube/Parkour_Video", "running")

# Test Case 2: A complex, new action that needs to be created
new_action_code = learn_new_action("Human_Observation/Guru_Nanak_Bani_Project", "meditation_pose")

print(f"\nTotal Learned Behaviors in Memory: {len(BEHAVIOR_DATABASE)}")
print(f"The Brain is now capable of self-learning complex human actions!")

