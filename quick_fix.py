#!/usr/bin/env python3
"""
Quick Fix Script - Regenerate with maximum settings
ਤੇਜ਼ ਫਿਕਸ ਸਕ੍ਰਿਪਟ
"""

import subprocess
import sys

print("\n" + "="*60)
print("🔧 QUICK FIX - Regenerating with Maximum Settings")
print("="*60 + "\n")

print("🎯 Applying fixes:")
print("  1. Background music volume: 0.50 (50% - VERY AUDIBLE)")
print("  2. Dialogue volume: Maximum")
print("  3. NO ducking (keep music loud always)")
print("  4. Force portrait rendering")
print("\n")

cmd = [
    ".venv/bin/python",
    "colab/master_builder.py",
    "--scenes", "temp_adhhi_aurat_scenes.json",
    "--bg-gain", "0.50",  # 50% volume!
    "--duck-factor", "0.50",  # Keep music at 50% even during speech
    "--verbose"
]

print(f"Running: {' '.join(cmd)}\n")
print("="*60 + "\n")

result = subprocess.run(cmd, cwd=".")

if result.returncode == 0:
    print("\n" + "="*60)
    print("✅ VIDEO REGENERATED!")
    print("="*60)
    print("\nNow try playing: AmritCore_FINAL_STUDIO_LAUNCH.mp4")
    print("You should hear LOUD music and voice!")
else:
    print("\n❌ Generation failed!")
    sys.exit(1)
