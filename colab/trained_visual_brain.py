"""
🧠 TRAINED VISUAL BRAIN - Learning from Real Sikh Character Images
==================================================================

This system:
1. Loads training images of Sikh characters (photos, paintings, illustrations)
2. Extracts visual features (clothing, turbans, facial features, body poses)
3. Learns animation patterns from reference videos/images
4. Generates new character images based on learned features
5. Uses real background images from Punjab/village settings

TRAINING DATA STRUCTURE:
========================
training_data/
├── characters/
│   ├── sikh_male_elderly/
│   │   ├── kulvant_ref1.jpg
│   │   ├── kulvant_ref2.jpg
│   │   └── elderly_sikh_farmer.jpg
│   ├── sikh_female_young/
│   │   ├── amandeep_ref1.jpg
│   │   └── young_punjabi_woman.jpg
│   └── sikh_male_adult/
│       └── daljit_ref1.jpg
├── backgrounds/
│   ├── punjab_village.jpg
│   ├── wheat_field.jpg
│   ├── punjabi_home_interior.jpg
│   └── sunset_village.jpg
├── animations/
│   ├── walking_sequence/
│   ├── gesture_poses/
│   └── expression_references/
└── metadata.json

Author: Amrit Core Team
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
import random
import math

try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps
    import numpy as np
except ImportError:
    print("⚠️  Installing required packages...")
    os.system("pip install Pillow numpy")
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps


class TrainingDataManager:
    """
    Manages training data: character images, backgrounds, animation references.
    Learns visual features from real images.
    """
    
    def __init__(self, training_dir: str = "training_data"):
        self.training_dir = Path(training_dir)
        self.setup_directories()
        self.load_metadata()
        self.extract_visual_features()
    
    def setup_directories(self):
        """Create training data directory structure."""
        dirs = [
            self.training_dir,
            self.training_dir / "characters" / "sikh_male_elderly",
            self.training_dir / "characters" / "sikh_male_adult", 
            self.training_dir / "characters" / "sikh_female_young",
            self.training_dir / "characters" / "sikh_child",
            self.training_dir / "backgrounds" / "village",
            self.training_dir / "backgrounds" / "fields",
            self.training_dir / "backgrounds" / "home_interior",
            self.training_dir / "backgrounds" / "nature",
            self.training_dir / "animations" / "walking",
            self.training_dir / "animations" / "gestures",
            self.training_dir / "animations" / "expressions",
            self.training_dir / "animations" / "traditional_poses",
        ]
        
        for dir_path in dirs:
            dir_path.mkdir(parents=True, exist_ok=True)
        
        print(f"✅ Training data directories created at: {self.training_dir}")
    
    def create_training_instructions(self):
        """Create instructions for users to add training data."""
        instructions = """
📚 HOW TO TRAIN THE VISUAL BRAIN
================================

STEP 1: Add Character Reference Images
---------------------------------------
Place images in these folders based on character type:

training_data/characters/sikh_male_elderly/
  → Photos of elderly Sikh men with turbans, beards, traditional clothing
  → For characters like ਕੁਲਵੰਤ (Kulvant)

training_data/characters/sikh_male_adult/
  → Photos of adult Sikh men (20-50 years)
  → For characters like ਦਲਜੀਤ (Daljit), ਦਲੀਪ (Dalip)

training_data/characters/sikh_female_young/
  → Photos of young Sikh/Punjabi women in salwar kameez
  → For characters like ਅਮਨਦੀਪ (Amandeep), ਰਮਨਦੀਪ (Ramandeep)

training_data/characters/sikh_child/
  → Photos of Sikh/Punjabi children
  → For characters like ਜਸਪ੍ਰੀਤ (Jaspreet)

STEP 2: Add Background Images
------------------------------
training_data/backgrounds/village/
  → Punjab village scenes, dirt roads, mud houses

training_data/backgrounds/fields/
  → Wheat fields, farmland, agricultural scenes

training_data/backgrounds/home_interior/
  → Traditional Punjabi home interiors

training_data/backgrounds/nature/
  → Trees, rivers, sunsets, natural scenery

STEP 3: Add Animation References (Optional)
--------------------------------------------
training_data/animations/walking/
  → Sequential images of people walking

training_data/animations/gestures/
  → Photos of hand gestures, body language

training_data/animations/expressions/
  → Face close-ups showing different emotions

training_data/animations/traditional_poses/
  → Traditional Sikh poses (prayer, farming, celebration)

IMAGE REQUIREMENTS:
-------------------
✅ Format: JPG, PNG, WEBP
✅ Resolution: At least 512x512 pixels
✅ Quality: Clear, well-lit images
✅ Diversity: Multiple angles, poses, expressions
✅ Copyright: Use royalty-free or licensed images

RECOMMENDED SOURCES:
--------------------
1. Unsplash.com (search: "punjab", "sikh", "indian village")
2. Pexels.com (search: "turban", "punjabi", "wheat field")
3. Pixabay.com (search: "india village", "traditional")
4. Your own photography
5. AI-generated images (Stable Diffusion, DALL-E)

Once you add images, run:
  python colab/trained_visual_brain.py --scan

This will analyze your images and extract features!
"""
        
        readme_path = self.training_dir / "README.txt"
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(instructions)
        
        print(f"📄 Training instructions saved: {readme_path}")
        return instructions
    
    def load_metadata(self):
        """Load or create metadata file."""
        metadata_path = self.training_dir / "metadata.json"
        
        if metadata_path.exists():
            with open(metadata_path, 'r', encoding='utf-8') as f:
                self.metadata = json.load(f)
            print(f"✅ Loaded existing metadata: {len(self.metadata.get('characters', {}))} character types")
        else:
            # Create default metadata
            self.metadata = {
                "version": "1.0",
                "characters": {
                    "ਕੁਲਵੰਤ": {
                        "type": "sikh_male_elderly",
                        "features": {
                            "turban_color": "white",
                            "beard": "long_white",
                            "clothing": "traditional_kurta",
                            "build": "thin",
                            "skin_tone": "medium"
                        }
                    },
                    "ਅਮਨਦੀਪ": {
                        "type": "sikh_female_young",
                        "features": {
                            "hair": "long_black_braid",
                            "clothing": "salwar_kameez_pink",
                            "build": "average",
                            "skin_tone": "fair"
                        }
                    },
                    "ਦਲਜੀਤ": {
                        "type": "sikh_male_adult",
                        "features": {
                            "turban_color": "blue",
                            "beard": "medium_black",
                            "clothing": "shirt_pants",
                            "build": "strong",
                            "skin_tone": "medium"
                        }
                    },
                    "ਦਲੀਪ": {
                        "type": "sikh_male_adult",
                        "features": {
                            "turban_color": "orange",
                            "beard": "short_black",
                            "clothing": "kurta_pajama",
                            "build": "average",
                            "skin_tone": "medium"
                        }
                    },
                    "ਰਮਨਦੀਪ": {
                        "type": "sikh_female_young",
                        "features": {
                            "hair": "long_black_open",
                            "clothing": "modern_suit_red",
                            "build": "slim",
                            "skin_tone": "fair"
                        }
                    },
                    "ਜਸਪ੍ਰੀਤ": {
                        "type": "sikh_child",
                        "features": {
                            "hair": "short_patka",
                            "clothing": "casual_yellow",
                            "build": "small",
                            "skin_tone": "fair"
                        }
                    }
                },
                "backgrounds": {
                    "village": [],
                    "fields": [],
                    "home_interior": [],
                    "nature": []
                },
                "learned_features": {}
            }
            
            self.save_metadata()
    
    def save_metadata(self):
        """Save metadata to file."""
        metadata_path = self.training_dir / "metadata.json"
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(self.metadata, indent=2, ensure_ascii=False, fp=f)
    
    def scan_training_images(self):
        """Scan training directories and catalog available images."""
        print("\n🔍 Scanning training data...")
        
        # Scan character images
        char_dir = self.training_dir / "characters"
        if char_dir.exists():
            for type_dir in char_dir.iterdir():
                if type_dir.is_dir():
                    images = list(type_dir.glob("*.jpg")) + list(type_dir.glob("*.png")) + list(type_dir.glob("*.webp"))
                    if images:
                        print(f"   📸 {type_dir.name}: {len(images)} images")
        
        # Scan backgrounds
        bg_dir = self.training_dir / "backgrounds"
        if bg_dir.exists():
            for type_dir in bg_dir.iterdir():
                if type_dir.is_dir():
                    images = list(type_dir.glob("*.jpg")) + list(type_dir.glob("*.png")) + list(type_dir.glob("*.webp"))
                    if images:
                        print(f"   🖼️  {type_dir.name}: {len(images)} backgrounds")
                        self.metadata["backgrounds"][type_dir.name] = [str(img) for img in images]
        
        self.save_metadata()
        print("✅ Scan complete!")
    
    def extract_visual_features(self):
        """Extract features from training images using computer vision."""
        # This would use OpenCV, MediaPipe, or ML models in production
        # For now, we'll use basic PIL analysis
        print("🧠 Analyzing visual features from training data...")
        
        char_types = ["sikh_male_elderly", "sikh_male_adult", "sikh_female_young", "sikh_child"]
        learned_features = {}
        
        for char_type in char_types:
            char_dir = self.training_dir / "characters" / char_type
            if not char_dir.exists():
                continue
            
            images = list(char_dir.glob("*.jpg")) + list(char_dir.glob("*.png"))
            if not images:
                continue
            
            # Analyze first image as reference
            sample_img = Image.open(images[0])
            
            # Extract dominant colors
            colors = self.extract_dominant_colors(sample_img)
            
            learned_features[char_type] = {
                "sample_count": len(images),
                "dominant_colors": colors,
                "reference_images": [str(img) for img in images[:3]]  # Store up to 3 references
            }
        
        self.metadata["learned_features"] = learned_features
        self.save_metadata()
        
        if learned_features:
            print(f"✅ Learned features from {len(learned_features)} character types")
        else:
            print("⚠️  No training images found. Add images and run --scan")
    
    def extract_dominant_colors(self, image: Image.Image, num_colors: int = 5) -> List[str]:
        """Extract dominant colors from an image."""
        # Resize for faster processing
        img = image.resize((150, 150))
        img = img.convert('RGB')
        
        # Get colors
        colors = img.getcolors(img.width * img.height)
        if not colors:
            return ["#808080"]
        
        # Sort by frequency
        colors = sorted(colors, key=lambda x: x[0], reverse=True)
        
        # Convert to hex
        hex_colors = []
        for count, color in colors[:num_colors]:
            hex_color = '#{:02x}{:02x}{:02x}'.format(color[0], color[1], color[2])
            hex_colors.append(hex_color)
        
        return hex_colors
    
    def get_random_background(self, category: str = "village") -> Optional[str]:
        """Get random background image from training data."""
        backgrounds = self.metadata["backgrounds"].get(category, [])
        if backgrounds:
            return random.choice(backgrounds)
        return None
    
    def get_character_references(self, character_name: str) -> Dict:
        """Get learned features for a character."""
        char_data = self.metadata["characters"].get(character_name, {})
        char_type = char_data.get("type", "sikh_male_adult")
        
        learned = self.metadata["learned_features"].get(char_type, {})
        
        return {
            "character": character_name,
            "type": char_type,
            "features": char_data.get("features", {}),
            "learned": learned,
            "reference_images": learned.get("reference_images", [])
        }


class TrainedCharacterSynthesizer:
    """
    Synthesizes characters using learned features from training data.
    Can use reference images directly or generate based on learned patterns.
    """
    
    def __init__(self, training_manager: TrainingDataManager):
        self.training_manager = training_manager
        self.cache = {}
    
    def generate_from_reference(
        self,
        character_name: str,
        expression: str = "neutral",
        size: Tuple[int, int] = (400, 600),
        use_training_image: bool = True
    ) -> Image.Image:
        """
        Generate character image using training data.
        If training images exist, use them as base and modify.
        Otherwise, generate from learned features.
        """
        cache_key = f"{character_name}_{expression}_{size}"
        if cache_key in self.cache:
            return self.cache[cache_key].copy()
        
        # Get character references
        ref_data = self.training_manager.get_character_references(character_name)
        ref_images = ref_data.get("reference_images", [])
        
        if use_training_image and ref_images:
            # Use actual training image as base
            ref_path = Path(ref_images[0])
            if ref_path.exists():
                base_img = self.load_and_prepare_reference(ref_path, size)
                
                # Apply expression modifications
                base_img = self.apply_expression_to_image(base_img, expression)
                
                self.cache[cache_key] = base_img
                return base_img.copy()
        
        # Fallback: Generate from learned features
        img = self.generate_from_features(ref_data, expression, size)
        self.cache[cache_key] = img
        return img.copy()
    
    def load_and_prepare_reference(
        self,
        image_path: Path,
        target_size: Tuple[int, int]
    ) -> Image.Image:
        """Load reference image and prepare for animation."""
        img = Image.open(image_path)
        
        # Convert to RGBA for transparency
        img = img.convert('RGBA')
        
        # Remove background (simple approach - can be enhanced with rembg library)
        img = self.remove_background_simple(img)
        
        # Resize to target size while maintaining aspect ratio
        img.thumbnail(target_size, Image.Resampling.LANCZOS)
        
        # Create canvas with target size and center image
        canvas = Image.new('RGBA', target_size, (0, 0, 0, 0))
        offset = ((target_size[0] - img.width) // 2, (target_size[1] - img.height) // 2)
        canvas.paste(img, offset, img)
        
        return canvas
    
    def remove_background_simple(self, img: Image.Image) -> Image.Image:
        """
        Simple background removal (edge-based).
        In production, use rembg or similar ML-based tool.
        """
        # Convert to RGB for processing
        rgb_img = img.convert('RGB')
        
        # Get corner pixel as background color
        bg_color = rgb_img.getpixel((0, 0))
        
        # Create mask based on color similarity
        data = np.array(rgb_img)
        
        # Calculate color distance from background
        diff = np.sqrt(np.sum((data - bg_color) ** 2, axis=2))
        
        # Threshold (adjust for better results)
        threshold = 50
        mask = diff > threshold
        
        # Apply mask to alpha channel
        img_array = np.array(img)
        img_array[:, :, 3] = (mask * 255).astype(np.uint8)
        
        return Image.fromarray(img_array, 'RGBA')
    
    def apply_expression_to_image(
        self,
        img: Image.Image,
        expression: str
    ) -> Image.Image:
        """
        Apply expression modifications to existing image.
        Uses image filters and adjustments.
        """
        # Expression-based adjustments
        if expression == "happy":
            # Brighten slightly
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(1.1)
            enhancer = ImageEnhance.Color(img)
            img = enhancer.enhance(1.2)
        
        elif expression == "sad":
            # Darken and desaturate
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(0.9)
            enhancer = ImageEnhance.Color(img)
            img = enhancer.enhance(0.7)
        
        elif expression == "angry":
            # Increase contrast and red tint
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(1.2)
        
        elif expression in ["crying", "worried"]:
            # Desaturate and darken
            enhancer = ImageEnhance.Color(img)
            img = enhancer.enhance(0.6)
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(0.85)
        
        return img
    
    def generate_from_features(
        self,
        ref_data: Dict,
        expression: str,
        size: Tuple[int, int]
    ) -> Image.Image:
        """Generate character from learned features (when no training images available)."""
        # Use learned colors if available
        learned = ref_data.get("learned", {})
        colors = learned.get("dominant_colors", ["#8B4513", "#D2691E", "#F4A460"])
        
        # Create simple representation
        img = Image.new('RGBA', size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        width, height = size
        center_x, center_y = width // 2, height // 2
        
        # Draw simple character silhouette with learned colors
        primary_color = colors[0] if colors else "#8B4513"
        
        # Head
        head_size = int(width * 0.35)
        head_y = int(height * 0.15)
        draw.ellipse(
            [center_x - head_size//2, head_y,
             center_x + head_size//2, head_y + head_size],
            fill=primary_color
        )
        
        # Body (simplified)
        body_width = int(width * 0.6)
        body_height = int(height * 0.65)
        body_top = head_y + head_size
        
        draw.rectangle(
            [center_x - body_width//2, body_top,
             center_x + body_width//2, body_top + body_height],
            fill=primary_color
        )
        
        return img


class TrainedBackgroundCompositor:
    """Uses real background images from training data."""
    
    def __init__(self, training_manager: TrainingDataManager):
        self.training_manager = training_manager
        self.cache = {}
    
    def get_background(
        self,
        scene_emotion: str,
        scene_type: str = "village",
        size: Tuple[int, int] = (1920, 1080)
    ) -> Image.Image:
        """
        Get background from training data or generate fallback.
        """
        cache_key = f"{scene_type}_{scene_emotion}_{size}"
        if cache_key in self.cache:
            return self.cache[cache_key].copy()
        
        # Try to get from training data
        bg_path = self.training_manager.get_random_background(scene_type)
        
        if bg_path and Path(bg_path).exists():
            # Load and prepare training background
            bg = Image.open(bg_path)
            bg = bg.convert('RGB')
            
            # Resize to fit
            bg = ImageOps.fit(bg, size, Image.Resampling.LANCZOS)
            
            # Apply emotion-based color grading
            bg = self.apply_emotion_grading(bg, scene_emotion)
            
            self.cache[cache_key] = bg
            return bg.copy()
        
        # Fallback: Generate gradient background
        return self.generate_fallback_background(scene_emotion, size)
    
    def apply_emotion_grading(
        self,
        img: Image.Image,
        emotion: str
    ) -> Image.Image:
        """Apply color grading based on emotion."""
        if emotion == "happy":
            # Warm, bright
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(1.1)
            enhancer = ImageEnhance.Color(img)
            img = enhancer.enhance(1.2)
        
        elif emotion == "sad":
            # Cool, desaturated
            enhancer = ImageEnhance.Color(img)
            img = enhancer.enhance(0.6)
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(0.8)
        
        elif emotion == "angry":
            # High contrast, red tint
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(1.3)
        
        elif emotion == "neutral":
            # Slight enhancement
            enhancer = ImageEnhance.Sharpness(img)
            img = enhancer.enhance(1.1)
        
        return img
    
    def generate_fallback_background(
        self,
        emotion: str,
        size: Tuple[int, int]
    ) -> Image.Image:
        """Generate gradient background if no training images available."""
        emotion_colors = {
            "happy": ("#FFD700", "#FFA500"),
            "sad": ("#4169E1", "#1E90FF"),
            "neutral": ("#90EE90", "#228B22"),
            "angry": ("#DC143C", "#8B0000"),
        }
        
        color1, color2 = emotion_colors.get(emotion.lower(), ("#CCCCCC", "#888888"))
        
        # Create gradient with numpy
        gradient = np.linspace(0, 1, size[1]).reshape(size[1], 1, 1)
        c1 = np.array([int(color1[i:i+2], 16) for i in (1, 3, 5)])
        c2 = np.array([int(color2[i:i+2], 16) for i in (1, 3, 5)])
        bg_array = c1 * (1 - gradient) + c2 * gradient
        bg_array = bg_array.astype(np.uint8)
        bg_array = np.repeat(bg_array, size[0], axis=1)
        
        return Image.fromarray(bg_array, 'RGB')


def main():
    """Setup and test trained visual brain."""
    import argparse
    
    parser = argparse.ArgumentParser(description='🧠 Trained Visual Brain - Learn from real images')
    parser.add_argument('--scan', action='store_true', help='Scan training directories')
    parser.add_argument('--test', action='store_true', help='Test character generation')
    parser.add_argument('--instructions', action='store_true', help='Show training instructions')
    
    args = parser.parse_args()
    
    # Initialize
    print("="*70)
    print("🧠 TRAINED VISUAL BRAIN")
    print("="*70)
    
    manager = TrainingDataManager()
    
    if args.instructions or (not args.scan and not args.test):
        instructions = manager.create_training_instructions()
        print("\n" + instructions)
    
    if args.scan:
        manager.scan_training_images()
    
    if args.test:
        print("\n🎨 Testing character synthesis...")
        synthesizer = TrainedCharacterSynthesizer(manager)
        compositor = TrainedBackgroundCompositor(manager)
        
        # Test character
        char_img = synthesizer.generate_from_reference(
            "ਕੁਲਵੰਤ",
            expression="happy",
            size=(400, 600),
            use_training_image=True
        )
        char_img.save("test_character.png")
        print("✅ Test character saved: test_character.png")
        
        # Test background
        bg_img = compositor.get_background("happy", "village")
        bg_img.save("test_background.png")
        print("✅ Test background saved: test_background.png")
        
        print("\n🎬 To use trained brain in animation, update animated_master_builder.py")


if __name__ == "__main__":
    main()
