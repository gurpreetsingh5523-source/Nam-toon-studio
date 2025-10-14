# AmritCore V5 - 25_Interactive_Control_Node.py (UI Button Mapping Logic)

import json
import os
import random

# --- 1. THE UI CONTROL DATABASE ---
# This maps the user's clicks from the UI buttons to the animation logic.
ANIMATION_MAPPING = {
    "walk":      {"code": "ANIM_WALK_01", "duration": 3.0, "status_msg": "Character is walking (ਸੇਵਾ ਵਿੱਚ ਜੁਟਿਆ)"},
    "sit":       {"code": "ANIM_SIT_02",  "duration": 5.0, "status_msg": "Character sitting (ਸੁਰਤ ਵਿੱਚ ਜੁੜਿਆ)"},
    "jump":      {"code": "ANIM_JUMP_04", "duration": 1.5, "status_msg": "Character jumping (ਉਤਸ਼ਾਹ ਨਾਲ ਭਰਿਆ)"},
    "swim":      {"code": "ANIM_SWIM_01", "duration": 8.0, "status_msg": "Character swimming (ਸੰਸਾਰ ਸਾਗਰ ਤਰ ਰਿਹਾ)"},
    "default":   {"code": "ANIM_IDLE_00", "duration": 2.0, "status_msg": "Character is still (ਧਿਆਨ ਵਿੱਚ)"}
}

# --- 2. THE UI CONTROL FUNCTION (Simulated API Endpoint) ---
def receive_ui_command(action_command):
    """
    Receives a command from the web UI and translates it into an animation code.
    In the final V5 system, this runs on the backend server.
    """
    action_command = action_command.lower()
    
    # Use the mapping logic
    action_data = ANIMATION_MAPPING.get(action_command, ANIMATION_MAPPING["default"])
    
    # The final output to the Animation Node
    final_output = {
        "command": action_data["code"],
        "duration": action_data["duration"],
        "message": action_data["status_msg"]
    }
    
    return final_output

# --- 3. TEST THE LOGIC ---
test_commands = ["walk", "jump", "meditation", "sit"]

print("--- INTERACTIVE CONTROL NODE STATUS ---")

for command in test_commands:
    result = receive_ui_command(command)
    print(f"\nUI Command: '{command}'")
    print(f"  -> Animation Code: {result['command']}")
    print(f"  -> Status Message: {result['message']}")
    
print("\nInteractive Control Node is fully functional. Ready to be integrated into the web UI.")
