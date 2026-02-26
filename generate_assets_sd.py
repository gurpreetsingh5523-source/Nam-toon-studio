#!/usr/bin/env python3
"""
Generate 3 scene images using Stable Diffusion (diffusers).
Saves images to assets/scenes/scene_1.png ... scene_3.png

If the model isn't available locally it will download (first run may be slow).
"""
import os
from pathlib import Path

try:
    import torch
    from diffusers import StableDiffusionPipeline
except Exception as e:
    print("Missing packages or environment for diffusers:", e)
    print("Please install dependencies: pip install diffusers transformers accelerate torch")
    raise

OUT_DIR = Path('assets/scenes')
OUT_DIR.mkdir(parents=True, exist_ok=True)

prompts = [
    "A young Punjabi farmer named Amandip standing in golden wheat fields at sunset, wearing a blue turban and traditional kurta pajama, smiling broadly, cinematic, photorealistic, high detail",
    "A young Punjabi farmer named Amandip looking worried under dark clouds and light rain in a village wheat field, realistic, moody lighting, emotional expression",
    "A young Punjabi farmer named Amandip looking at a beautiful rainbow over a wet wheat field, hopeful expression, soft golden light, photorealistic"
]

# Try to use GPU if available
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

# Load pipeline
print("Loading Stable Diffusion pipeline (this may download models on first run)...")
pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
if device == "cuda":
    pipe = pipe.to(device)

# Reduce guidance/steps for speed
num_inference_steps = 20

for i, prompt in enumerate(prompts, start=1):
    out_file = OUT_DIR / f"scene_{i}.png"
    if out_file.exists():
        print(f"Skipping existing: {out_file}")
        continue
    print(f"Generating scene {i}: {prompt[:80]}...")
    image = pipe(prompt, num_inference_steps=num_inference_steps).images[0]
    image.save(out_file)
    print(f"Saved: {out_file}")

print("Done. Generated images saved in assets/scenes/")
