# AmritCore - 14_prompt_generator_node.py (Translates Brain Data to GPU Command)

import os

# --- 1. CONTEXTUAL BRAIN DATA (Simulated Input from Node 11) ---
def get_current_scene_context():
    """Returns the current emotional and setting data from the Brain."""
    return {
        "emotion": "Hope",
        "time_of_day": "Golden Hour Afternoon",
        "setting_type": "Village Well",
        "character_focus": "Krishna",
        "style": "Photorealistic, Cinematic"
    }

# --- 2. DEFINE THE PROMPT GENERATOR LOGIC ---
def build_master_prompt(context):
    """
    Builds the final, complex prompt string required by the Diffusion Model (GPU).
    This logic contains the core stylistic rules.
    """
    
    # Map emotion to color/lighting details
    lighting_detail = ""
    if context["emotion"] == "Hope":
        lighting_detail = "Sun-drenched, warm golden hour lighting, cinematic focus."
    elif context["emotion"] == "Doubt":
        lighting_detail = "Overcast lighting, muted blue tones, strong side shadows."
    else:
        lighting_detail = "Clear day lighting."
    
    # Build the structural core of the prompt
    master_prompt = (
        f"{context['style']}, {lighting_detail}. "
        f"A wide-shot scene of a traditional Punjabi village well. The well is old brick, surrounded by very dense, gnarled mulberry trees. "
        f"In the foreground, {context['character_focus']} is standing with a {context['emotion']} posture. "
        f"Subtle ambient details. High resolution."
    )
    
    return master_prompt

# --- 3. TEST THE NODE ---
scene_context = get_current_scene_context()

if scene_context:
    final_prompt = build_master_prompt(scene_context)
    
    print("\n--- PROMPT GENERATOR NODE STATUS: SUCCESS ---")
    print("1. Brain Input (Emotion):", scene_context["emotion"])
    print("2. Final Command (GPU Prompt):")
    print("------------------------------------------")
    print(final_prompt)
    print("------------------------------------------")
    print("\nThis module is ready to execute on your new laptop!")

