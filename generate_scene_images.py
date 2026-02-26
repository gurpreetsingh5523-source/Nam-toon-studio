#!/usr/bin/env python3
"""
Generate FULL SCENE images for Tootan Wala Khoo story
Creates complete backgrounds with environment, not just character portraits
"""

import json
import torch
from pathlib import Path
from PIL import Image
from diffusers import StableDiffusionPipeline

print("🎬 FULL SCENE GENERATOR")
print("="*60)

# Load scenes
with open('tootan_wala_khoo_scenes.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    scenes = data['scenes']

print(f"✅ Loaded {len(scenes)} scenes")
print()

# Setup AI model
device = "cuda" if torch.cuda.is_available() else \
         "mps" if torch.backends.mps.is_available() else "cpu"
print(f"🖥️  Using device: {device}")

# Load Stable Diffusion
print("🎨 Loading Stable Diffusion AI Model...")
pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float16 if device == "cuda" else torch.float32,
    safety_checker=None
)
pipe = pipe.to(device)
pipe.enable_attention_slicing()
print("✅ AI Model loaded!")
print()

# Create output directory
output_dir = Path("ai_assets/scenes")
output_dir.mkdir(parents=True, exist_ok=True)

# Generate each scene
for scene in scenes:
    scene_id = scene['scene_id']
    prompt = scene.get('scene_prompt', '')
    
    if not prompt:
        print(f"⚠️  Scene {scene_id}: No scene_prompt found, skipping")
        continue
    
    # Check cache
    cache_path = output_dir / f"scene_{scene_id}.png"
    if cache_path.exists():
        print(f"✅ Scene {scene_id}: Using cached image")
        continue
    
    # Generate
    print(f"🎨 Scene {scene_id}: Generating...")
    print(f"   Prompt: {prompt[:80]}...")
    
    negative_prompt = "portrait only, headshot, close-up face, no background, modern style, low quality, blurry, distorted, multiple wells, cars, phones"
    
    with torch.no_grad():
        result = pipe(
            prompt=prompt,
            negative_prompt=negative_prompt,
            num_inference_steps=30,
            guidance_scale=7.5,
            height=720,   # Cinematic height
            width=1280,   # Wide screen
        )
    
    image = result.images[0]
    
    # Check quality
    import numpy as np
    arr = np.array(image)
    mean_val = arr.mean()
    
    if mean_val < 5:
        print(f"   ⚠️  Scene {scene_id}: Generated dark image, retrying...")
        continue
    
    # Save
    image.save(cache_path)
    print(f"   ✅ Saved: {cache_path.name}")
    print()

print("="*60)
print("✅ SCENE GENERATION COMPLETE!")
print("="*60)
print(f"\n📁 Scenes saved to: {output_dir}")
print("\nTo view scenes:")
print(f"  open {output_dir}")
print("\nTo generate video:")
print("  python colab/master_builder.py --scenes tootan_wala_khoo_scenes.json --output Tootan_Final.mp4")
