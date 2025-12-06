#!/usr/bin/env python3
"""
Diagnostic script to debug why portraits aren't showing in video
"""
import sys
sys.path.insert(0, '/Users/gurpreetdhillon/Nam-toon-studio')

import json
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

# Load the scenes file
with open('temp_adhhi_aurat_scenes.json', 'r') as f:
    data = json.load(f)

print("=== SCENE ANALYSIS ===")
print(f"Total scenes: {data.get('total_scenes')}")
print()

# Collect all unique characters
all_characters = set()
for scene in data['scenes']:
    for d in scene.get('dialogues', []):
        char = d.get('character', '')
        if char:
            all_characters.add(char)
            print(f"Scene {scene['scene_id']}: character='{char}' (unicode: {[hex(ord(c)) for c in char]})")

print()
print(f"✓ Unique characters found: {all_characters}")
print()

# Simulate avatar generation logic from master_builder.py
print("=== SIMULATING AVATAR GENERATION ===")
def _generate_avatar(name, size=256):
    """Generate a simple colored circle avatar with initial"""
    try:
        import colorsys
        # Use character name to derive a color
        hash_val = sum(ord(c) for c in name)
        hue = (hash_val % 360) / 360.0
        rgb = colorsys.hsv_to_rgb(hue, 0.6, 0.9)
        color = tuple(int(c * 255) for c in rgb)
        
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        # Draw circle
        margin = 10
        draw.ellipse([margin, margin, size-margin, size-margin], fill=color + (220,), outline=(255, 255, 255, 255), width=4)
        
        # Draw initial
        initial = name[0].upper() if name else '?'
        font = ImageFont.load_default()
        bbox = draw.textbbox((0, 0), initial, font=font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        tx = (size - tw) // 2
        ty = (size - th) // 2 - bbox[1]
        draw.text((tx, ty), initial, font=font, fill=(255, 255, 255, 255))
        
        return img
    except Exception as e:
        print(f"Failed to generate avatar for {name}: {e}")
        return None

portraits = {}
for char in all_characters:
    avatar = _generate_avatar(char)
    if avatar:
        portraits[char] = avatar
        print(f"✓ Generated avatar for '{char}'")
        # Save for inspection
        avatar.save(f'debug_avatar_{char.replace("/", "_")}.png')
        print(f"  Saved to: debug_avatar_{char.replace('/', '_')}.png")

print()
print(f"✓ Total portraits generated: {len(portraits)}")
print(f"✓ Portrait keys: {list(portraits.keys())}")
print()

# Simulate dialogue timeline
print("=== SIMULATING DIALOGUE TIMELINE ===")
timeline = []
cur_time = 0.0
for scene in data['scenes']:
    for idx, d in enumerate(scene.get('dialogues', [])):
        char = d.get('character', '')
        text = d.get('text', '')
        # Estimate duration (rough: 0.5s per word)
        est_duration = max(2.0, len(text.split()) * 0.5)
        
        timeline.append({
            'start': cur_time,
            'end': cur_time + est_duration,
            'character': char,
            'text': text[:50] + '...' if len(text) > 50 else text,
            'duration': est_duration
        })
        cur_time += est_duration

for i, seg in enumerate(timeline):
    print(f"Segment {i}: t={seg['start']:.1f}-{seg['end']:.1f}s, char='{seg['character']}', text='{seg['text'][:30]}...'")

print()
print("=== CHARACTER LOOKUP TEST ===")
# Test if character lookups would work
test_times = [5.0, 20.0, 40.0, 80.0]
for t in test_times:
    current_char = None
    for seg in timeline:
        if seg['start'] <= t < seg['end']:
            current_char = seg['character']
            break
    
    print(f"t={t}s: current_char='{current_char}'")
    if current_char:
        if current_char in portraits:
            print(f"  ✓ Portrait found for '{current_char}'")
        else:
            print(f"  ✗ NO PORTRAIT for '{current_char}'")
            print(f"  Available portraits: {list(portraits.keys())}")
            # Check for similar names
            for p_name in portraits.keys():
                if p_name.strip() == current_char.strip():
                    print(f"  ! Found after strip(): '{p_name}'")

print()
print("=== DIAGNOSIS COMPLETE ===")
print("Check debug_avatar_*.png files to verify avatars were created correctly")
