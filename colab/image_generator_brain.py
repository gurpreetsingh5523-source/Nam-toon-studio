#!/usr/bin/env python3
"""
🎨 IMAGE GENERATOR BRAIN
========================
Uses Stable Diffusion to create character images and scenes.
Works WITH Visual Brain (Visual Brain decides WHAT, this brain creates HOW)

Author: Nam-toon Studio
Date: November 2, 2025
"""

import os
import sys
from pathlib import Path
from typing import Dict, Optional
import torch
from PIL import Image

class ImageGeneratorBrain:
    """
    Uses Stable Diffusion to generate images based on Visual Brain's decisions
    """
    
    def __init__(self, assets_dir: str = "assets"):
        """Initialize the image generator"""
        self.assets_dir = Path(assets_dir)
        self.assets_dir.mkdir(exist_ok=True)
        
        # Create subdirectories
        (self.assets_dir / "characters").mkdir(exist_ok=True)
        (self.assets_dir / "backgrounds").mkdir(exist_ok=True)
        
        self.pipeline = None
        self.device = "mps" if torch.backends.mps.is_available() else "cpu"
        
        print(f"\n🎨 Image Generator Brain initialized")
        print(f"   Device: {self.device}")
        print(f"   Assets: {self.assets_dir}")
        
    def _load_model(self):
        """Lazy load Stable Diffusion model (only when needed)"""
        if self.pipeline is not None:
            return
            
        print("\n📥 Loading Stable Diffusion model (first time only)...")
        print("   This will download ~4GB model...")
        
        try:
            from diffusers import StableDiffusionPipeline
            
            self.pipeline = StableDiffusionPipeline.from_pretrained(
                "runwayml/stable-diffusion-v1-5",
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
            )
            
            if self.device == "mps":
                self.pipeline = self.pipeline.to("mps")
                # MPS optimization
                self.pipeline.enable_attention_slicing()
            elif self.device == "cuda":
                self.pipeline = self.pipeline.to("cuda")
            
            print("✅ Model loaded successfully!")
            
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            print("⚠️  Will use placeholder images instead")
            self.pipeline = None
    
    def generate_character(
        self,
        character_name: str,
        emotion: str,
        description: str = ""
    ) -> Path:
        """
        Generate a character image
        
        Args:
            character_name: Name of character (e.g., "Amandip", "Dalip")
            emotion: Emotion (happy, sad, worried, etc.)
            description: Additional description
            
        Returns:
            Path to generated/cached image
        """
        # Check if already exists
        asset_path = self.assets_dir / "characters" / f"{character_name.lower()}_{emotion}.png"
        
        if asset_path.exists():
            print(f"✅ Using existing: {asset_path.name}")
            return asset_path
        
        print(f"\n🎨 Generating new character: {character_name} ({emotion})")
        
        # Build prompt based on character and emotion
        prompt = self._build_character_prompt(character_name, emotion, description)
        
        # Generate image
        image = self._generate_image(prompt)
        
        # Save
        image.save(asset_path)
        print(f"💾 Saved: {asset_path.name}")
        
        return asset_path
    
    def generate_background(
        self,
        location: str,
        mood: str = "neutral"
    ) -> Path:
        """
        Generate a background image
        
        Args:
            location: Location description (e.g., "wheat field", "village")
            mood: Mood/lighting (golden, dark, peaceful, etc.)
            
        Returns:
            Path to generated/cached image
        """
        # Check if already exists
        safe_name = location.lower().replace(" ", "_")
        asset_path = self.assets_dir / "backgrounds" / f"{safe_name}_{mood}.png"
        
        if asset_path.exists():
            print(f"✅ Using existing: {asset_path.name}")
            return asset_path
        
        print(f"\n🎨 Generating new background: {location} ({mood})")
        
        # Build prompt
        prompt = self._build_background_prompt(location, mood)
        
        # Generate
        image = self._generate_image(prompt)
        
        # Save
        image.save(asset_path)
        print(f"💾 Saved: {asset_path.name}")
        
        return asset_path
    
    def _build_character_prompt(
        self,
        character_name: str,
        emotion: str,
        description: str
    ) -> str:
        """Build Stable Diffusion prompt for character"""
        
        # Character-specific descriptions
        character_details = {
            "amandip": "young Punjabi man, wearing blue turban and traditional kurta pajama",
            "dalip": "middle-aged Punjabi man, white beard, traditional white kurta",
            "kulwant": "Punjabi woman, wearing colorful salwar kameez, dupatta",
        }
        
        base = character_details.get(character_name.lower(), "Punjabi person")
        
        # Emotion expressions
        emotion_faces = {
            "happy": "bright smile, joyful expression, sparkling eyes",
            "sad": "sad expression, tears, downcast eyes",
            "worried": "concerned face, furrowed brows, anxious",
            "angry": "angry face, fierce expression, intense eyes",
            "peaceful": "calm serene face, gentle smile, relaxed",
            "excited": "excited expression, wide eyes, big smile",
            "nostalgic": "thoughtful expression, distant gaze, slight smile"
        }
        
        emotion_desc = emotion_faces.get(emotion, "neutral expression")
        
        prompt = f"""
{base}, {emotion_desc}, {description},
portrait style, detailed face, realistic,
Punjab India style, professional photography,
clear facial features, high quality, 4k
        """.strip()
        
        return prompt
    
    def _build_background_prompt(self, location: str, mood: str) -> str:
        """Build Stable Diffusion prompt for background"""
        
        # Location descriptions
        locations = {
            "wheat field": "golden wheat field in Punjab India, vast landscape",
            "village": "traditional Punjab village, clay houses, dirt roads",
            "house interior": "traditional Punjabi house interior, simple furniture",
            "gurudwara": "Sikh Gurudwara temple, golden dome, peaceful",
            "protest": "crowd of people, protest scene, urban setting",
            "farm": "Punjab farm, agricultural land, rural setting"
        }
        
        location_desc = locations.get(location.lower(), location)
        
        # Mood/lighting
        moods = {
            "golden": "golden hour lighting, warm sunset glow",
            "bright": "bright daylight, clear blue sky",
            "dark": "dark moody atmosphere, dramatic lighting",
            "peaceful": "peaceful serene atmosphere, soft natural light",
            "dramatic": "dramatic lighting, cinematic atmosphere"
        }
        
        mood_desc = moods.get(mood, "natural lighting")
        
        prompt = f"""
{location_desc}, {mood_desc},
wide angle landscape, detailed environment,
Punjab India, realistic, professional photography,
no people, clean composition, high quality, 4k
        """.strip()
        
        return prompt
    
    def _generate_image(self, prompt: str) -> Image.Image:
        """Actually generate the image using Stable Diffusion"""
        
        # Load model if not loaded
        self._load_model()
        
        if self.pipeline is None:
            # Fallback: create placeholder
            print("⚠️  Using placeholder image")
            return self._create_placeholder()
        
        try:
            # Generate with Stable Diffusion
            print(f"   Prompt: {prompt[:80]}...")
            print(f"   Generating (this may take 10-30 seconds)...")
            
            with torch.no_grad():
                result = self.pipeline(
                    prompt,
                    num_inference_steps=30,  # Lower = faster, higher = better quality
                    guidance_scale=7.5,
                    height=720,
                    width=1280
                )
            
            image = result.images[0]
            print("   ✅ Generated!")
            return image
            
        except Exception as e:
            print(f"   ❌ Generation failed: {e}")
            print("   ⚠️  Using placeholder instead")
            return self._create_placeholder()
    
    def _create_placeholder(self) -> Image.Image:
        """Create a simple placeholder image"""
        from PIL import ImageDraw, ImageFont
        
        img = Image.new('RGB', (1280, 720), color=(200, 200, 200))
        draw = ImageDraw.Draw(img)
        
        # Add text
        text = "Placeholder\n(Stable Diffusion not available)"
        
        # Try to use a font
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 40)
        except:
            font = ImageFont.load_default()
        
        # Center text
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        position = ((1280 - text_width) / 2, (720 - text_height) / 2)
        draw.text(position, text, fill=(100, 100, 100), font=font)
        
        return img
    
    def get_asset(self, asset_type: str, name: str, emotion: str = "") -> Optional[Path]:
        """
        Get existing asset path (doesn't generate)
        
        Args:
            asset_type: "character" or "background"
            name: Asset name
            emotion: For characters only
            
        Returns:
            Path if exists, None otherwise
        """
        if asset_type == "character":
            path = self.assets_dir / "characters" / f"{name.lower()}_{emotion}.png"
        else:
            path = self.assets_dir / "backgrounds" / f"{name.lower()}.png"
        
        return path if path.exists() else None


# Test function
def test_image_generator():
    """Test the image generator"""
    print("\n" + "="*70)
    print("🧪 TESTING IMAGE GENERATOR BRAIN")
    print("="*70)
    
    brain = ImageGeneratorBrain()
    
    # Test 1: Generate character
    print("\n1️⃣  Test: Generate Amandip (happy)")
    img_path = brain.generate_character(
        character_name="Amandip",
        emotion="happy",
        description="young energetic"
    )
    print(f"   Result: {img_path}")
    
    # Test 2: Generate background
    print("\n2️⃣  Test: Generate wheat field background")
    bg_path = brain.generate_background(
        location="wheat field",
        mood="golden"
    )
    print(f"   Result: {bg_path}")
    
    # Test 3: Check caching
    print("\n3️⃣  Test: Try to generate same character again (should use cache)")
    img_path2 = brain.generate_character(
        character_name="Amandip",
        emotion="happy"
    )
    print(f"   Result: {img_path2}")
    
    print("\n" + "="*70)
    print("✅ IMAGE GENERATOR BRAIN TESTS COMPLETE")
    print("="*70)
    print(f"\n📁 Check assets folder: {brain.assets_dir}")
    print(f"   Characters: {list((brain.assets_dir / 'characters').glob('*.png'))}")
    print(f"   Backgrounds: {list((brain.assets_dir / 'backgrounds').glob('*.png'))}")


if __name__ == "__main__":
    test_image_generator()
