#!/usr/bin/env python3
"""
🎨 AI IMAGE GENERATOR
Uses Stable Diffusion to create diverse characters and scenes
"""

import torch
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
from PIL import Image
import os

class AIImageGenerator:
    """Generate diverse AI images for videos"""
    
    def __init__(self, model_id="stabilityai/stable-diffusion-2-1"):
        """Initialize with lightweight model"""
        print("🎨 Loading AI Image Generator...")
        
        try:
            self.pipe = StableDiffusionPipeline.from_pretrained(
                model_id,
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                safety_checker=None  # Disable for speed
            )
            
            # Use faster scheduler
            self.pipe.scheduler = DPMSolverMultistepScheduler.from_config(
                self.pipe.scheduler.config
            )
            
            # Move to GPU if available
            if torch.cuda.is_available():
                self.pipe = self.pipe.to("cuda")
                print("   ✅ Using GPU acceleration")
            elif torch.backends.mps.is_available():
                self.pipe = self.pipe.to("mps")
                print("   ✅ Using Apple Silicon acceleration")
            else:
                print("   ⚠️  Using CPU (slower)")
            
            # Enable memory optimizations
            self.pipe.enable_attention_slicing()
            
            print("✅ AI Generator ready!")
            self.enabled = True
            
        except Exception as e:
            print(f"⚠️  AI Generator failed: {e}")
            print("   Falling back to simple renderer")
            self.enabled = False
    
    def generate_character(self, description: str, style="realistic") -> Image.Image:
        """Generate character image"""
        if not self.enabled:
            return None
        
        prompt = f"{style} portrait, {description}, high quality, detailed, 8k"
        negative_prompt = "blurry, low quality, distorted, ugly, deformed"
        
        try:
            image = self.pipe(
                prompt=prompt,
                negative_prompt=negative_prompt,
                num_inference_steps=20,  # Fast
                height=512,
                width=512
            ).images[0]
            
            return image
            
        except Exception as e:
            print(f"   ⚠️  Character generation failed: {e}")
            return None
    
    def generate_scene(self, description: str, style="cinematic") -> Image.Image:
        """Generate scene/background"""
        if not self.enabled:
            return None
        
        prompt = f"{style} scene, {description}, beautiful, detailed, high quality"
        negative_prompt = "people, faces, text, blurry, low quality"
        
        try:
            image = self.pipe(
                prompt=prompt,
                negative_prompt=negative_prompt,
                num_inference_steps=15,  # Very fast
                height=512,
                width=768
            ).images[0]
            
            return image
            
        except Exception as e:
            print(f"   ⚠️  Scene generation failed: {e}")
            return None
    
    def generate_punjabi_character(self, gender="male", age="young", action="walking"):
        """Generate Punjabi character"""
        if gender == "male":
            desc = f"{age} Punjabi man wearing kurta pajama, {action}, traditional, smiling"
        else:
            desc = f"{age} Punjabi woman wearing salwar kameez, dupatta, {action}, traditional, smiling"
        
        return self.generate_character(desc, style="realistic")
    
    def generate_punjabi_scene(self, location="village"):
        """Generate Punjabi scene"""
        scenes = {
            "village": "Punjab village, wheat fields, mud houses, blue sky, peaceful",
            "gurdwara": "Golden Temple Gurdwara, holy place, beautiful architecture, serene",
            "fields": "Green Punjab fields, mustard flowers, tractors, farmer working",
            "home": "Traditional Punjabi home interior, colorful, warm, family atmosphere",
            "langar": "Gurdwara langar hall, people serving food, community, devotion",
            "market": "Punjabi market, colorful shops, fruits, vegetables, busy street"
        }
        
        description = scenes.get(location, scenes["village"])
        return self.generate_scene(description, style="cinematic")


# Test function
if __name__ == "__main__":
    print("\n🧪 Testing AI Image Generator...")
    
    generator = AIImageGenerator()
    
    if generator.enabled:
        print("\n1️⃣ Generating Punjabi man...")
        img = generator.generate_punjabi_character(gender="male", age="young", action="walking")
        if img:
            img.save("test_character.png")
            print("   ✅ Saved: test_character.png")
        
        print("\n2️⃣ Generating village scene...")
        img = generator.generate_punjabi_scene("village")
        if img:
            img.save("test_scene.png")
            print("   ✅ Saved: test_scene.png")
        
        print("\n✅ Test complete!")
    else:
        print("❌ AI Generator not available")
