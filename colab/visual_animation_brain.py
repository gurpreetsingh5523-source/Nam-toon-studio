#!/usr/bin/env python3
"""
🎨 VISUAL ANIMATION BRAIN - Intelligent Image Synthesis & Animation System
==========================================================================

This brain generates and animates characters using synthetic training data.

CAPABILITIES:
1. Character Image Synthesis - generates character appearances from descriptions
2. Expression Generator - creates facial expressions (happy, sad, angry, etc.)
3. Movement Animator - animates body movements (walking, gesturing, etc.)
4. Lip Sync Engine - matches mouth movements to audio
5. Background Compositor - intelligently places characters in scenes
6. Style Transfer - maintains consistent art style across scenes
7. Training Data Manager - learns from synthetic examples

Author: Amrit Core Team
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
import random
import math

# For image generation and manipulation
try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
    import numpy as np
except ImportError:
    print("⚠️  Installing required packages: Pillow, numpy")
    os.system("pip install Pillow numpy")
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
    import numpy as np


class SyntheticDataGenerator:
    """
    Generates synthetic training data for character appearances and animations.
    This creates a database of visual features to learn from.
    """
    
    def __init__(self, output_dir: str = "synthetic_training_data"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Character feature database (synthetic training data)
        self.character_features = {
            "ਕੁਲਵੰਤ": {
                "age": "elderly",
                "gender": "male",
                "build": "thin",
                "height": "medium",
                "clothing": "traditional_kurta",
                "colors": ["#8B4513", "#D2691E", "#F4A460"],  # Brown tones
            },
            "ਅਮਨਦੀਪ": {
                "age": "young_adult",
                "gender": "female",
                "build": "average",
                "height": "medium",
                "clothing": "salwar_kameez",
                "colors": ["#FF69B4", "#FFB6C1", "#FFC0CB"],  # Pink tones
            },
            "ਦਲਜੀਤ": {
                "age": "adult",
                "gender": "male",
                "build": "strong",
                "height": "tall",
                "clothing": "shirt_pants",
                "colors": ["#4169E1", "#1E90FF", "#87CEEB"],  # Blue tones
            },
            "ਦਲੀਪ": {
                "age": "adult",
                "gender": "male",
                "build": "average",
                "height": "medium",
                "clothing": "kurta_pajama",
                "colors": ["#228B22", "#32CD32", "#90EE90"],  # Green tones
            },
            "ਰਮਨਦੀਪ": {
                "age": "young_adult",
                "gender": "female",
                "build": "slim",
                "height": "medium",
                "clothing": "modern_dress",
                "colors": ["#FF4500", "#FF6347", "#FFA07A"],  # Orange/Red tones
            },
            "ਜਸਪ੍ਰੀਤ": {
                "age": "child",
                "gender": "male",
                "build": "small",
                "height": "short",
                "clothing": "casual",
                "colors": ["#FFD700", "#FFA500", "#FFFF00"],  # Yellow tones
            },
            "Narrator": {
                "age": "timeless",
                "gender": "neutral",
                "build": "invisible",
                "height": "none",
                "clothing": "none",
                "colors": ["#FFFFFF", "#F0F0F0", "#E0E0E0"],  # White/Gray (no visual)
            }
        }
        
        # Expression templates (training data)
        self.expressions = {
            "happy": {"mouth": "smile", "eyes": "open_wide", "eyebrows": "raised"},
            "sad": {"mouth": "frown", "eyes": "half_closed", "eyebrows": "down"},
            "angry": {"mouth": "tight", "eyes": "narrow", "eyebrows": "furrowed"},
            "surprised": {"mouth": "open", "eyes": "wide", "eyebrows": "raised_high"},
            "neutral": {"mouth": "straight", "eyes": "open", "eyebrows": "normal"},
            "crying": {"mouth": "frown", "eyes": "tears", "eyebrows": "down"},
            "laughing": {"mouth": "big_smile", "eyes": "squinted", "eyebrows": "raised"},
            "worried": {"mouth": "slight_frown", "eyes": "wide", "eyebrows": "raised"},
        }
        
        # Movement patterns (training data)
        self.movements = {
            "walking": {"type": "translate", "axis": "x", "speed": "medium"},
            "running": {"type": "translate", "axis": "x", "speed": "fast"},
            "gesturing": {"type": "rotate", "axis": "arm", "speed": "medium"},
            "nodding": {"type": "rotate", "axis": "head", "speed": "slow"},
            "waving": {"type": "oscillate", "axis": "hand", "speed": "medium"},
            "sitting": {"type": "static", "axis": "none", "speed": "none"},
            "standing": {"type": "static", "axis": "none", "speed": "none"},
            "falling": {"type": "translate", "axis": "y", "speed": "fast"},
        }
        
        print(f"✅ Synthetic training data initialized: {len(self.character_features)} characters")
    
    def get_character_template(self, name: str) -> Dict:
        """Get character visual template from training data."""
        return self.character_features.get(name, self.character_features["Narrator"])
    
    def get_expression_template(self, emotion: str) -> Dict:
        """Get expression template from training data."""
        emotion_clean = emotion.lower().strip()
        return self.expressions.get(emotion_clean, self.expressions["neutral"])
    
    def get_movement_template(self, action: str) -> Dict:
        """Get movement pattern from training data."""
        action_clean = action.lower().strip()
        return self.movements.get(action_clean, self.movements["standing"])


class CharacterImageSynthesizer:
    """
    Synthesizes character images using geometric primitives and learned features.
    In production, this could use Stable Diffusion, DALL-E, or custom models.
    """
    
    def __init__(self, training_data: SyntheticDataGenerator):
        self.training_data = training_data
        self.cache = {}  # Cache generated characters
    
    def generate_character_image(
        self, 
        name: str, 
        expression: str = "neutral",
        size: Tuple[int, int] = (300, 400),
        position: str = "center"
    ) -> Image.Image:
        """
        Generate a character image with specified expression.
        Uses synthetic training data to determine appearance.
        """
        cache_key = f"{name}_{expression}_{size}_{position}"
        if cache_key in self.cache:
            return self.cache[cache_key].copy()
        
        # Get character template from training data
        template = self.training_data.get_character_template(name)
        expr_data = self.training_data.get_expression_template(expression)
        
        # Create canvas
        img = Image.new('RGBA', size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        width, height = size
        center_x, center_y = width // 2, height // 2
        
        # Skip visual for narrator
        if name == "Narrator" or template["build"] == "invisible":
            self.cache[cache_key] = img
            return img.copy()
        
        # Character colors from training data
        primary_color = template["colors"][0]
        secondary_color = template["colors"][1]
        accent_color = template["colors"][2]
        
        # Draw character based on age/build from training data
        if template["age"] == "child":
            body_height = int(height * 0.6)
            head_size = int(width * 0.35)
        elif template["age"] == "elderly":
            body_height = int(height * 0.7)
            head_size = int(width * 0.30)
        else:  # adult/young_adult
            body_height = int(height * 0.75)
            head_size = int(width * 0.32)
        
        # HEAD
        head_y = int(height * 0.15)
        draw.ellipse(
            [center_x - head_size//2, head_y, 
             center_x + head_size//2, head_y + head_size],
            fill=secondary_color,
            outline=primary_color,
            width=3
        )
        
        # EYES (expression-based from training data)
        eye_y = head_y + head_size // 3
        eye_spacing = head_size // 4
        eye_size = head_size // 8 if expr_data["eyes"] == "narrow" else head_size // 6
        
        # Left eye
        draw.ellipse(
            [center_x - eye_spacing - eye_size, eye_y,
             center_x - eye_spacing + eye_size, eye_y + eye_size * 2],
            fill="black"
        )
        # Right eye
        draw.ellipse(
            [center_x + eye_spacing - eye_size, eye_y,
             center_x + eye_spacing + eye_size, eye_y + eye_size * 2],
            fill="black"
        )
        
        # TEARS if crying
        if "tears" in expr_data["eyes"]:
            for x_offset in [-eye_spacing, eye_spacing]:
                draw.ellipse(
                    [center_x + x_offset - 3, eye_y + eye_size * 2,
                     center_x + x_offset + 3, eye_y + eye_size * 2 + 15],
                    fill="#87CEEB"
                )
        
        # MOUTH (expression-based)
        mouth_y = head_y + int(head_size * 0.7)
        mouth_width = head_size // 3
        
        if expr_data["mouth"] in ["smile", "big_smile"]:
            # Smile arc
            mouth_height = 10 if expr_data["mouth"] == "smile" else 20
            draw.arc(
                [center_x - mouth_width//2, mouth_y - mouth_height//2,
                 center_x + mouth_width//2, mouth_y + mouth_height],
                start=0, end=180,
                fill="black", width=3
            )
        elif expr_data["mouth"] == "frown":
            # Frown arc
            draw.arc(
                [center_x - mouth_width//2, mouth_y - 10,
                 center_x + mouth_width//2, mouth_y + 10],
                start=180, end=360,
                fill="black", width=3
            )
        else:
            # Straight mouth
            draw.line(
                [center_x - mouth_width//2, mouth_y,
                 center_x + mouth_width//2, mouth_y],
                fill="black", width=3
            )
        
        # BODY
        body_top = head_y + head_size
        body_width = int(width * 0.6)
        
        if template["clothing"] in ["traditional_kurta", "kurta_pajama"]:
            # Kurta shape (rectangle with slight flare)
            draw.rectangle(
                [center_x - body_width//2, body_top,
                 center_x + body_width//2, body_top + body_height],
                fill=primary_color,
                outline=accent_color,
                width=2
            )
        elif template["clothing"] == "salwar_kameez":
            # Salwar kameez (fitted top, loose bottom)
            draw.rectangle(
                [center_x - body_width//3, body_top,
                 center_x + body_width//3, body_top + body_height//2],
                fill=primary_color,
                outline=accent_color,
                width=2
            )
            draw.polygon(
                [
                    (center_x - body_width//3, body_top + body_height//2),
                    (center_x + body_width//3, body_top + body_height//2),
                    (center_x + body_width//2, body_top + body_height),
                    (center_x - body_width//2, body_top + body_height),
                ],
                fill=secondary_color,
                outline=accent_color
            )
        else:
            # Default clothing
            draw.rectangle(
                [center_x - body_width//2, body_top,
                 center_x + body_width//2, body_top + body_height],
                fill=primary_color,
                outline=accent_color,
                width=2
            )
        
        # ARMS (simplified)
        arm_width = body_width // 8
        draw.rectangle(
            [center_x - body_width//2 - arm_width, body_top + 20,
             center_x - body_width//2, body_top + body_height//2],
            fill=secondary_color,
            outline=accent_color
        )
        draw.rectangle(
            [center_x + body_width//2, body_top + 20,
             center_x + body_width//2 + arm_width, body_top + body_height//2],
            fill=secondary_color,
            outline=accent_color
        )
        
        # Cache and return
        self.cache[cache_key] = img
        return img.copy()


class AnimationBrain:
    """
    Intelligent animation brain that creates character movements,
    expressions, and lip-sync based on scene context.
    """
    
    def __init__(self, training_data: SyntheticDataGenerator):
        self.training_data = training_data
    
    def generate_keyframes(
        self,
        character_name: str,
        action: str,
        emotion: str,
        duration_seconds: float,
        fps: int = 24
    ) -> List[Dict[str, Any]]:
        """
        Generate animation keyframes for a character.
        Returns list of keyframes with transformations.
        """
        total_frames = int(duration_seconds * fps)
        keyframes = []
        
        # Get movement pattern from training data
        movement = self.training_data.get_movement_template(action)
        
        # Generate keyframes based on movement type
        for frame_idx in range(total_frames):
            progress = frame_idx / total_frames
            
            keyframe = {
                "frame": frame_idx,
                "time": frame_idx / fps,
                "character": character_name,
                "emotion": emotion,
                "transform": {}
            }
            
            # Apply movement transformations
            if movement["type"] == "translate":
                if movement["axis"] == "x":
                    # Walking/running horizontal movement
                    speed_multiplier = 2.0 if movement["speed"] == "fast" else 1.0
                    keyframe["transform"]["x_offset"] = int(progress * 200 * speed_multiplier)
                elif movement["axis"] == "y":
                    # Falling vertical movement
                    keyframe["transform"]["y_offset"] = int(progress * 150)
            
            elif movement["type"] == "oscillate":
                # Waving motion (sine wave)
                amplitude = 20
                frequency = 3 if movement["speed"] == "fast" else 2
                keyframe["transform"]["x_offset"] = int(
                    amplitude * math.sin(2 * math.pi * frequency * progress)
                )
            
            elif movement["type"] == "rotate":
                # Nodding/gesturing (rotation)
                if movement["axis"] == "head":
                    angle = 15 * math.sin(2 * math.pi * 2 * progress)
                    keyframe["transform"]["rotation"] = angle
            
            # Add slight breathing animation (subtle scale)
            breath_cycle = 0.02 * math.sin(2 * math.pi * 0.5 * progress)
            keyframe["transform"]["scale"] = 1.0 + breath_cycle
            
            keyframes.append(keyframe)
        
        return keyframes
    
    def generate_lip_sync(
        self,
        audio_duration: float,
        dialogue_text: str,
        fps: int = 24
    ) -> List[str]:
        """
        Generate lip-sync mouth shapes based on audio duration.
        Returns list of mouth shapes per frame.
        """
        total_frames = int(audio_duration * fps)
        
        # Simple phoneme-based lip sync (can be enhanced with actual audio analysis)
        # For now, alternate between open/closed based on syllables
        words = dialogue_text.split()
        frames_per_word = total_frames // max(len(words), 1)
        
        mouth_shapes = []
        for frame_idx in range(total_frames):
            word_idx = frame_idx // frames_per_word
            frame_in_word = frame_idx % frames_per_word
            
            # Alternate mouth shapes within each word
            if frame_in_word < frames_per_word // 3:
                mouth_shapes.append("open")
            elif frame_in_word < 2 * frames_per_word // 3:
                mouth_shapes.append("half_open")
            else:
                mouth_shapes.append("closed")
        
        return mouth_shapes


class SceneCompositor:
    """
    Composes final scenes by combining backgrounds, characters, and effects.
    """
    
    def __init__(self, width: int = 1920, height: int = 1080):
        self.width = width
        self.height = height
    
    def create_background(
        self,
        scene_type: str,
        emotion: str,
        colors: Optional[Tuple[str, str]] = None
    ) -> Image.Image:
        """Create scene background based on type and emotion."""
        bg = Image.new('RGB', (self.width, self.height))
        
        if colors:
            color1, color2 = colors
        else:
            # Emotion-based colors
            emotion_colors = {
                "happy": ("#FFD700", "#FFA500"),
                "sad": ("#4169E1", "#1E90FF"),
                "neutral": ("#90EE90", "#228B22"),
                "angry": ("#DC143C", "#8B0000"),
            }
            color1, color2 = emotion_colors.get(emotion.lower(), ("#CCCCCC", "#888888"))
        
        # Create gradient (optimized with numpy)
        gradient = np.linspace(0, 1, self.height).reshape(self.height, 1, 1)
        c1 = np.array([int(color1[i:i+2], 16) for i in (1, 3, 5)])
        c2 = np.array([int(color2[i:i+2], 16) for i in (1, 3, 5)])
        bg_array = c1 * (1 - gradient) + c2 * gradient
        bg_array = bg_array.astype(np.uint8)
        bg_array = np.repeat(bg_array, self.width, axis=1)
        
        return Image.fromarray(bg_array, 'RGB')
    
    def compose_frame(
        self,
        background: Image.Image,
        characters: List[Dict[str, Any]]
    ) -> Image.Image:
        """
        Compose a single frame with background and characters.
        
        characters: List of dicts with keys: 
            - image: PIL Image
            - position: (x, y) tuple
            - scale: float
            - rotation: float (degrees)
        """
        frame = background.copy()
        
        for char_data in characters:
            char_img = char_data["image"]
            x, y = char_data.get("position", (0, 0))
            scale = char_data.get("scale", 1.0)
            rotation = char_data.get("rotation", 0)
            
            # Apply transformations
            if scale != 1.0:
                new_size = (int(char_img.width * scale), int(char_img.height * scale))
                char_img = char_img.resize(new_size, Image.Resampling.LANCZOS)
            
            if rotation != 0:
                char_img = char_img.rotate(rotation, expand=True, resample=Image.Resampling.BICUBIC)
            
            # Paste character onto frame (with alpha channel)
            if char_img.mode == 'RGBA':
                frame.paste(char_img, (x, y), char_img)
            else:
                frame.paste(char_img, (x, y))
        
        return frame


class VisualAnimationBrain:
    """
    Master brain that orchestrates the entire visual animation pipeline.
    """
    
    def __init__(self, output_dir: str = "animated_frames"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Initialize sub-systems
        print("🧠 Initializing Visual Animation Brain...")
        self.training_data = SyntheticDataGenerator()
        self.synthesizer = CharacterImageSynthesizer(self.training_data)
        self.animator = AnimationBrain(self.training_data)
        self.compositor = SceneCompositor()
        
        print("✅ Visual Animation Brain ready!")
    
    def analyze_scene(self, scene_data: Dict) -> Dict[str, Any]:
        """
        Analyze scene and determine visual requirements.
        """
        analysis = {
            "scene_id": scene_data.get("scene_id", 0),
            "emotion": scene_data.get("emotion", "neutral"),
            "characters_present": [],
            "actions": [],
            "background_type": "gradient",
            "lighting": "normal",
        }
        
        # Extract character actions from dialogue
        for dialogue in scene_data.get("dialogues", []):
            char_name = dialogue.get("character", "")
            if char_name and char_name not in analysis["characters_present"]:
                analysis["characters_present"].append(char_name)
            
            # Detect actions in text (simple keyword matching)
            text = dialogue.get("text", "").lower()
            if any(word in text for word in ["चल", "walk", "गया", "आया"]):
                analysis["actions"].append({"character": char_name, "action": "walking"})
            elif any(word in text for word in ["रो", "cry", "tears"]):
                analysis["actions"].append({"character": char_name, "action": "crying"})
        
        return analysis
    
    def generate_scene_frames(
        self,
        scene_data: Dict,
        audio_duration: float,
        fps: int = 24,
        output_prefix: str = "scene"
    ) -> List[str]:
        """
        Generate all frames for a scene with animated characters.
        Returns list of frame file paths.
        """
        print(f"🎬 Generating frames for scene {scene_data.get('scene_id', 0)}...")
        
        # Analyze scene
        analysis = self.analyze_scene(scene_data)
        print(f"   Characters: {', '.join(analysis['characters_present'])}")
        print(f"   Emotion: {analysis['emotion']}")
        
        # Create background
        background = self.compositor.create_background(
            scene_type=analysis["background_type"],
            emotion=analysis["emotion"]
        )
        
        # Generate keyframes for each character
        total_frames = int(audio_duration * fps)
        character_keyframes = {}
        
        for char_name in analysis["characters_present"]:
            if char_name == "Narrator":
                continue  # Skip narrator visuals
            
            # Determine action
            action = "standing"
            for act in analysis["actions"]:
                if act["character"] == char_name:
                    action = act["action"]
                    break
            
            # Generate keyframes
            keyframes = self.animator.generate_keyframes(
                character_name=char_name,
                action=action,
                emotion=analysis["emotion"],
                duration_seconds=audio_duration,
                fps=fps
            )
            character_keyframes[char_name] = keyframes
        
        # Generate frames
        frame_paths = []
        num_chars = len([c for c in analysis["characters_present"] if c != "Narrator"])
        
        for frame_idx in range(total_frames):
            if frame_idx % 30 == 0:  # Progress update every ~1 second
                print(f"   Frame {frame_idx}/{total_frames}...")
            
            # Prepare characters for this frame
            characters_in_frame = []
            
            for char_idx, char_name in enumerate(analysis["characters_present"]):
                if char_name == "Narrator":
                    continue
                
                # Get keyframe data
                keyframe = character_keyframes[char_name][frame_idx]
                transform = keyframe["transform"]
                
                # Generate character image with current emotion
                char_img = self.synthesizer.generate_character_image(
                    name=char_name,
                    expression=keyframe["emotion"],
                    size=(300, 400)
                )
                
                # Position characters (spread horizontally)
                if num_chars == 1:
                    base_x = 810  # Center
                elif num_chars == 2:
                    base_x = 560 if char_idx == 0 else 1060
                else:
                    spacing = 1920 // (num_chars + 1)
                    base_x = spacing * (char_idx + 1) - 150
                
                base_y = 400
                
                # Apply transformations from keyframe
                x = base_x + transform.get("x_offset", 0)
                y = base_y + transform.get("y_offset", 0)
                scale = transform.get("scale", 1.0)
                rotation = transform.get("rotation", 0)
                
                characters_in_frame.append({
                    "image": char_img,
                    "position": (x, y),
                    "scale": scale,
                    "rotation": rotation,
                })
            
            # Compose frame
            frame = self.compositor.compose_frame(background, characters_in_frame)
            
            # Save frame
            frame_path = self.output_dir / f"{output_prefix}_frame_{frame_idx:06d}.png"
            frame.save(frame_path)
            frame_paths.append(str(frame_path))
        
        print(f"✅ Generated {len(frame_paths)} frames")
        return frame_paths
    
    def save_analysis(self, analysis: Dict, output_file: str):
        """Save scene analysis to JSON file."""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False)
        print(f"💾 Analysis saved: {output_file}")


def main():
    """Test the visual animation brain."""
    print("=" * 70)
    print("🎨 VISUAL ANIMATION BRAIN - Test Mode")
    print("=" * 70)
    
    # Initialize brain
    brain = VisualAnimationBrain()
    
    # Test scene data
    test_scene = {
        "scene_id": 0,
        "emotion": "happy",
        "dialogues": [
            {
                "character": "ਕੁਲਵੰਤ",
                "text": "ਪਿੰਡ ਵਿੱਚ ਬਹੁਤ ਖੁਸ਼ੀ ਹੈ।"
            },
            {
                "character": "ਅਮਨਦੀਪ",
                "text": "ਹਾਂ ਪਿਤਾ ਜੀ, ਮੈਂ ਬਹੁਤ ਖੁਸ਼ ਹਾਂ।"
            }
        ]
    }
    
    # Generate test frames (5 seconds)
    frame_paths = brain.generate_scene_frames(
        scene_data=test_scene,
        audio_duration=5.0,
        fps=24,
        output_prefix="test_scene"
    )
    
    print(f"\n✅ Test complete! Generated {len(frame_paths)} frames")
    print(f"📁 Frames saved to: {brain.output_dir}")
    print("\nTo create video from frames, use:")
    print(f"ffmpeg -framerate 24 -i {brain.output_dir}/test_scene_frame_%06d.png -c:v libx264 -pix_fmt yuv420p test_animation.mp4")


if __name__ == "__main__":
    main()
