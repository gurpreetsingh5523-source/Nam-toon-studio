#!/usr/bin/env python3
"""
🕵️‍♂️ LOGIC TRUTH CHECKER
Sachayi Janan Layi (To know the truth)

User asked: "Ki eh AI Text-to-Video hai?"
Answer: Let's check the code logic line-by-line.
"""

import ast
import os
from pathlib import Path

class LogicTruthChecker:
    def __init__(self):
        self.generators = [
            'realistic_punjabi_video_generator.py',
            'amrit_kaur_video_generator.py',
            'advanced_video_generator.py'
        ]
        
    def analyze_generator(self, filename):
        print(f"\n🔍 ANALYZING: {filename}")
        print("-" * 50)
        
        if not Path(filename).exists():
            print("❌ File not found")
            return

        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Check for "Fake" AI (Drawing shapes)
        drawing_shapes = content.count('cv2.circle') + content.count('cv2.rectangle') + content.count('cv2.line')
        
        # Check for "Real" AI (Generation models)
        has_stable_diffusion = 'StableDiffusionPipeline' in content
        has_torch = 'torch' in content
        has_gan = 'GAN' in content
        
        # Check for Audio
        has_audio = 'gTTS' in content or 'pyttsx3' in content
        
        print(f"📊 LOGIC BREAKDOWN:")
        
        if drawing_shapes > 10 and not has_stable_diffusion:
            print("   ⚠️  METHOD: Manual Drawing (Drawing circles/rectangles)")
            print(f"      Evidence: Found {drawing_shapes} drawing commands")
            print("      Verdict: NOT Generative AI. It is 'Programmatic Animation'.")
            
        elif has_stable_diffusion:
            print("   ✅ METHOD: Generative AI (Stable Diffusion)")
            print("      Evidence: Uses Diffusion Models")
            print("      Verdict: YES, this is AI Video Generation.")
            
            # But check if it's actually enabled
            if 'SD_AVAILABLE = False' in content or 'TORCH_AVAILABLE = False' in content:
                 print("      ⚠️  BUT: AI is DISABLED in code! (Falling back to placeholders)")
        
        if has_audio:
            print("   ✅ AUDIO: Logic exists (gTTS/pyttsx3)")
        else:
            print("   ❌ AUDIO: No audio logic found")
            
    def run_audit(self):
        print("🕵️‍♂️ SACHAYI CHECK (TRUTH CHECK)")
        print("==============================")
        
        for gen in self.generators:
            self.analyze_generator(gen)
            
        print("\n⚖️  FINAL CONCLUSION:")
        print("1. 'realistic_punjabi_video_generator.py' has AI code, BUT it crashed, so it turned off AI.")
        print("2. 'amrit_kaur_video_generator.py' is drawing circles (Programmatic Animation), NOT AI Video.")
        print("3. The system is TRYING to be AI, but failing due to library errors.")

if __name__ == "__main__":
    checker = LogicTruthChecker()
    checker.run_audit()
