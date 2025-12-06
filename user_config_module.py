"""
user_config_module.py
User customization loader for Nam-toon-studio.
"""
import json
import os

def load_user_config(config_path="user_config.json"):
    if not os.path.exists(config_path):
        print(f"No config found at {config_path}. Using defaults.")
        return {}
    with open(config_path, "r") as f:
        return json.load(f)

if __name__ == "__main__":
    config = load_user_config()
    print("Loaded user config:", config)
