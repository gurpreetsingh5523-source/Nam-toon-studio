#!/usr/bin/env python3
"""
🎬 REALISTIC PUNJABI VIDEO GENERATOR
Uses ALL available power - no more cartoons!

Integrates:
- Stable Diffusion for realistic faces
- Training data (media_training_data.json)
- Torch for AI processing
- Proper Punjabi features
"""

import cv2
import numpy as np
import json
from pathlib import Path
from datetime import datetime
from PIL import Image

# Try to import AI libraries (optional)
try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False

try:
    from diffusers import StableDiffusionPipeline
    SD_AVAILABLE = True
except ImportError:
    SD_AVAILABLE = False
    print("⚠️  Stable Diffusion not available - will use training photos")

try:
    from gtts import gTTS
    import subprocess
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False

class RealisticPunjabiVideoGenerator:
    """Generate REALISTIC Punjabi character videos"""
    
    def __init__(self):
        self.width = 1920
        self.height = 1080
        self.fps = 30
        
        # Load training data
        self.training_data = self.load_training_data()
        
        # Initialize Stable Diffusion if available
        self.sd_pipeline = None
        if SD_AVAILABLE and TORCH_AVAILABLE:
            if torch.cuda.is_available() or torch.backends.mps.is_available():
                print("🚀 GPU available - loading Stable Diffusion...")
                try:
                    self.sd_pipeline = StableDiffusionPipeline.from_pretrained(
                        "runwayml/stable-diffusion-v1-5",
                        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
                    )
                    if torch.cuda.is_available():
                        self.sd_pipeline = self.sd_pipeline.to("cuda")
                    elif torch.backends.mps.is_available():
                        self.sd_pipeline = self.sd_pipeline.to("mps")
                    # Enable memory efficient attention
                    self.sd_pipeline.enable_attention_slicing()
                    print("✅ Stable Diffusion loaded!")
                except Exception as e:
                    print(f"⚠️  Stable Diffusion not available: {e}")
            else:
                print("⚠️  No GPU - will use training photos")
        else:
            print("⚠️  SD not available - using training photos (more realistic anyway!)")
            
    def generate_background(self, scene_desc="Punjabi village home interior"):
        """Generate a realistic background"""
        if self.sd_pipeline:
            try:
                print(f"   🎨 Generating background: {scene_desc}...")
                prompt = f"Cinematic shot of {scene_desc}, detailed, photorealistic, 8k, interior design, warm lighting, depth of field"
                image = self.sd_pipeline(
                    prompt,
                    negative_prompt="people, characters, text, watermark, blurry, distorted",
                    num_inference_steps=30,
                    guidance_scale=7.5
                ).images[0]
                
                img_array = np.array(image)
                img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
                # Resize to video dimensions
                img_bgr = cv2.resize(img_bgr, (self.width, self.height))
                return img_bgr
            except Exception as e:
                print(f"   ⚠️  Background generation failed: {e}")
        
        # Fallback background
        bg = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        # Warm gradient
        for y in range(self.height):
            color_value = int(200 + (y / self.height) * 55)
            bg[y, :] = [color_value - 40, color_value - 20, color_value] # Warm beige/brown
        return bg

    def generate_audio(self, text, filename):
        """Generate audio for dialogue using gTTS"""
        if AUDIO_AVAILABLE:
            try:
                # Detect language (simple heuristic)
                lang = 'pa' if any(ord(c) > 127 for c in text) else 'en'
                tts = gTTS(text=text, lang=lang, slow=False)
                tts.save(filename)
                return True
            except Exception as e:
                print(f"   ⚠️  Audio generation failed: {e}")
        return False

    def get_audio_duration(self, filename):
        """Get duration of audio file in seconds"""
        try:
            result = subprocess.run(
                ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', filename],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            return float(result.stdout)
        except:
            return 3.0 # Default 3 seconds
    
    def load_training_data(self):
        """Load analyzed training data"""
        data_file = Path('media_training_data.json')
        
        if data_file.exists():
            with open(data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"✅ Loaded training data: {len(data.get('characters', []))} characters")
            return data
        else:
            print("⚠️  No training data found")
            return {'characters': []}
    
    def generate_realistic_character(self, character_desc, emotion='neutral'):
        """Generate realistic Punjabi character using Stable Diffusion"""
        
        # Prompts for different characters
        prompts = {
            'amrit': f"Portrait of a young Punjabi Sikh woman wearing traditional Punjabi suit, "
                    f"white dupatta, gentle smile, kind eyes, cultural dress, "
                    f"detailed face, photorealistic, professional lighting, {emotion} expression",
            'user': f"Portrait of a person in casual Punjabi clothing, "
                   f"natural expression, photorealistic, {emotion} emotion"
        }
        
        prompt = prompts.get(character_desc, prompts['amrit'])
        
        # If we have Stable Diffusion
        if self.sd_pipeline:
            try:
                print(f"   🎨 Generating {character_desc} with emotion: {emotion}...")
                image = self.sd_pipeline(
                    prompt,
                    negative_prompt="cartoon, anime, low quality, blurry, distorted",
                    num_inference_steps=30,
                    guidance_scale=7.5
                ).images[0]
                
                # Convert to OpenCV format
                img_array = np.array(image)
                img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
                
                return img_bgr
            except Exception as e:
                print(f"   ⚠️  SD generation failed: {e}")
                return self.create_placeholder_character(character_desc, emotion)
        else:
            # Use placeholder or training data
            return self.create_placeholder_character(character_desc, emotion)
    
    def create_placeholder_character(self, character_desc, emotion='neutral'):
        """Create placeholder when SD not available"""
        # Better than circles - use photo-realistic approach
        
        # Check if we have training photos
        photo_folder = Path('training_photos')
        if photo_folder.exists():
            photos = list(photo_folder.glob('*.jpg')) + list(photo_folder.glob('*.png'))
            if photos:
                # Use a real photo
                import random
                photo = random.choice(photos)
                img = cv2.imread(str(photo))
                if img is not None:
                    # Resize to standard size
                    img = cv2.resize(img, (512, 512))
                    return img
        
        # Fallback: Create simple but better placeholder
        img = np.ones((512, 512, 3), dtype=np.uint8) * 230
        
        # Add text
        text = "Amrit Kaur" if character_desc == 'amrit' else "User"
        cv2.putText(img, text, (150, 250), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1.5, (50, 50, 50), 3)
        cv2.putText(img, f"({emotion})", (180, 300),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (100, 100, 100), 2)
        
        return img
    
    def create_scene_with_characters(self, characters_data, background_img, speaker, frame_index=0):
        """Create a scene with realistic characters and background"""
        
        # Start with background
        frame = background_img.copy()
        
        # Place characters
        for i, char_data in enumerate(characters_data):
            char_img = char_data['image']
            base_position = char_data['position']
            name = char_data['name']
            is_speaking = name == speaker
            
            # Resize character
            char_height = 800 # Taller for "scene" look
            char_width = int(char_img.shape[1] * (char_height / char_img.shape[0]))
            char_resized = cv2.resize(char_img, (char_width, char_height))
            
            # Animation: Breathing effect
            # Calculate vertical offset based on frame_index
            import math
            breath_offset = int(5 * math.sin(frame_index * 0.1))
            
            # Animation: Speaking effect (bounce/scale)
            if is_speaking:
                speak_offset = int(3 * math.sin(frame_index * 0.5)) # Faster bounce
                # Slight scale up for speaker
                scale = 1.02 + (0.01 * math.sin(frame_index * 0.2))
                h = int(char_height * scale)
                w = int(char_width * scale)
                char_resized = cv2.resize(char_img, (w, h))
                char_width, char_height = w, h
            else:
                speak_offset = 0
            
            # Position on frame
            x, y = base_position
            
            # Adjust x for new width
            if name == 'amrit':
                x = self.width - char_width - 100 # Right side
            else:
                x = 100 # Left side
                
            y = self.height - char_height + breath_offset + speak_offset
            
            # Ensure within bounds
            x = max(0, min(x, self.width - char_width))
            y = max(0, min(y, self.height))
            
            # Alpha blending (if image has alpha, but SD images are usually RGB)
            # Simple overlay for now
            # Create mask for simple cutout if needed, but for now just rectangular overlay
            # To make it look better, we could use a feather mask, but let's stick to simple overlay first
            
            # Check bounds for slicing
            y_start = max(0, y)
            y_end = min(self.height, y + char_height)
            x_start = max(0, x)
            x_end = min(self.width, x + char_width)
            
            char_y_start = 0 if y >= 0 else -y
            char_y_end = char_height if y + char_height <= self.height else self.height - y
            char_x_start = 0 if x >= 0 else -x
            char_x_end = char_width if x + char_width <= self.width else self.width - x
            
            if y_end > y_start and x_end > x_start:
                frame[y_start:y_end, x_start:x_end] = char_resized[char_y_start:char_y_end, char_x_start:char_x_end]
            
            # Highlight if speaking (Subtle glow or just the movement is enough)
            # User said "lipsing hundi" - since we can't do real lipsync easily, 
            # the "bounce" and "scale" will indicate speaking.
        
        # NO TEXT OVERLAY as requested ("ik screen te txt a ria hai ohdi lorh ni hundi")
        
        return frame
    
    def create_video_from_script(self, script, output_name=None):
        """Create realistic video from script with AUDIO and SCENE"""
        
        print("🎬 REALISTIC PUNJABI VIDEO GENERATION (WITH AUDIO)")
        print("="*70)
        
        if not output_name:
            output_name = f"REALISTIC_{script['title'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
        
        conversation = script.get('conversation', [])
        
        print(f"📝 Generating {len(conversation)} scenes...")
        
        # 1. Generate Background
        print("\n🎨 Generating Scene Background...")
        background_img = self.generate_background("Punjabi village home courtyard with flowers")
        
        # 2. Generate Characters
        print("\n🎨 Generating Characters...")
        character_images = {}
        emotions = ['neutral', 'warm', 'sad', 'happy', 'comforting']
        
        for char in ['amrit', 'user']:
            character_images[char] = {}
            for emotion in emotions:
                # Update prompt for full body/scene context if possible, but portrait is safer for consistency
                # We will rely on compositing for the "scene" feel
                print(f"   Generating {char} - {emotion}...")
                img = self.generate_realistic_character(char, emotion)
                character_images[char][emotion] = img
        
        print("✅ Assets generated!")
        
        # 3. Create Video & Audio
        print("\n🎬 Creating video sequences...")
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        temp_video = output_name.replace('.mp4', '_temp.mp4')
        out = cv2.VideoWriter(temp_video, fourcc, self.fps, (self.width, self.height))
        
        audio_files = []
        frame_count = 0
        
        import os
        # Create temp audio dir
        os.makedirs("temp_audio", exist_ok=True)
        
        for i, turn in enumerate(conversation):
            speaker = turn['speaker']
            text = turn['text']
            emotion = turn.get('emotion', 'neutral')
            character = turn.get('character', 'amrit')
            
            print(f"\n   Scene {i+1}: {speaker} ({emotion})")
            
            # Generate Audio
            audio_filename = f"temp_audio/line_{i}.mp3"
            if self.generate_audio(text, audio_filename):
                duration = self.get_audio_duration(audio_filename)
                audio_files.append(audio_filename)
            else:
                duration = 3.0 # Fallback
                # Create silent audio file if needed, or just skip audio for this line
            
            # Calculate frames needed
            num_frames = int(duration * self.fps)
            print(f"      Audio duration: {duration:.1f}s ({num_frames} frames)")
            
            # Get character images
            amrit_emotion = emotion if character == 'amrit' else 'neutral'
            user_emotion = emotion if character == 'user' else 'neutral'
            
            characters_data = [
                {
                    'name': 'amrit',
                    'image': character_images['amrit'].get(amrit_emotion, character_images['amrit']['neutral']),
                    'position': (0, 0) # Position handled in create_scene
                },
                {
                    'name': 'user',
                    'image': character_images['user'].get(user_emotion, character_images['user']['neutral']),
                    'position': (0, 0)
                }
            ]
            
            # Generate frames for this line
            for f in range(num_frames):
                frame = self.create_scene_with_characters(characters_data, background_img, speaker, frame_index=frame_count+f)
                out.write(frame)
            
            frame_count += num_frames
        
        out.release()
        print(f"\n✅ Video frames generated: {frame_count}")
        
        # 4. Merge Audio and Video
        print("\n🔊 Merging Audio...")
        
        # Concatenate audio files
        list_file = "temp_audio/list.txt"
        with open(list_file, 'w') as f:
            for audio in audio_files:
                f.write(f"file '{os.path.abspath(audio)}'\n")
        
        combined_audio = "temp_audio/combined.mp3"
        subprocess.run(['ffmpeg', '-f', 'concat', '-safe', '0', '-i', list_file, '-c', 'copy', combined_audio, '-y'], 
                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Merge with video
        print("   Combining video and audio...")
        final_cmd = [
            'ffmpeg', '-i', temp_video, '-i', combined_audio,
            '-c:v', 'copy', '-c:a', 'aac', '-strict', 'experimental',
            '-map', '0:v:0', '-map', '1:a:0', '-shortest',
            output_name, '-y'
        ]
        subprocess.run(final_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Cleanup
        try:
            os.remove(temp_video)
            # Keep audio for debug if needed, or remove
            # import shutil
            # shutil.rmtree("temp_audio") 
        except:
            pass
        
        # Get file size
        if Path(output_name).exists():
            size_mb = Path(output_name).stat().st_size / (1024 * 1024)
            print("\n" + "="*70)
            print(f"✅ REALISTIC VIDEO COMPLETE!")
            print(f"📹 File: {output_name}")
            print(f"💾 Size: {size_mb:.2f} MB")
            print(f"⏱️  Duration: {frame_count / self.fps:.1f}s")
            print("="*70)
            return output_name
        else:
            print("❌ Error creating final video")
            return temp_video

# Test
if __name__ == "__main__":
    print("🎬 Initializing Realistic Video Generator...")
    if TORCH_AVAILABLE:
        print("   Checking for GPU...")
        print(f"   CUDA available: {torch.cuda.is_available()}")
        print(f"   MPS available: {torch.backends.mps.is_available()}")
    else:
        print("   Using training photos for realistic characters")
    print()
    
    generator = RealisticPunjabiVideoGenerator()
    
    # Load Amrit Kaur script
    script_files = list(Path('.').glob('amrit_kaur_script_*.json'))
    if script_files:
        script_file = sorted(script_files)[-1]
        print(f"📝 Using script: {script_file}")
        
        with open(script_file, 'r', encoding='utf-8') as f:
            script = json.load(f)
        
        print("\n🚀 Generating REALISTIC video (this may take a few minutes)...")
        video_file = generator.create_video_from_script(script)
        
        print(f"\n✅ Done! Opening video...")
        import subprocess
        subprocess.run(['open', video_file])
    else:
        print("❌ No script found. Run amrit_kaur_conversation_ai.py first.")
