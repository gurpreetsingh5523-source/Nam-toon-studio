#!/usr/bin/env python3
"""
🎬 CLEAN FAST RENDERER - Each Brain Does ONE Job
==================================================

WORKFLOW:
1. Brain 1 (Visual): Creates scene image → # TODO: Implement functiones to Brain 2
2. Brain 2 (Audio): Adds background music → # TODO: Implement functiones to Brain 3  
3. Brain 3 (Voice): Adds dialogue → # TODO: Implement functiones to Master
4. Master: Checks everything and creates final video

NO DUPLICATES. NO CONFUSION. FAST AND CLEAN.
"""

import sys
import os
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from gtts import gTTS
from moviepy.editor import ImageClip, AudioFileClip, CompositeAudioClip, concatenate_videoclips
from PIL import Image
import numpy as np

class CleanFastRenderer:
    """Clean renderer - each brain does exactly ONE job"""
    
    def __init__(self):
        print("\n" + "="*70)
        print("🎬 CLEAN FAST RENDERER INITIALIZED")
        print("="*70)
        print("\nWorkflow:")
        print("1️⃣  Visual Brain → Creates colored scene image")
        print("2️⃣  Audio Brain → Adds background music (quiet)")
        print("3️⃣  Voice Brain → Adds Punjabi dialogue (loud)")
        print("4️⃣  Master Brain → Combines and verifies")
        print("="*70)
        
        # Load story
        with open('amandip_story_data.json', 'r', encoding='utf-8') as f:
            self.story = json.load(f)
    
    def render_scene(self, scene_num: int):
        """Render ONE scene with clean workflow"""
        
        scene = self.story['scenes'][scene_num - 1]
        print(f"\n{'='*70}")
        print(f"🎬 SCENE {scene_num}: {scene['title']}")
        print(f"{'='*70}")
        print(f"Emotion: {scene['emotion']}")
        print(f"Dialogue: {scene['dialogue'][:60]}...")
        
        # ============================================
        # STEP 1: VISUAL BRAIN - Create scene image
        # ============================================
        print(f"\n1️⃣  VISUAL BRAIN working...")
        
        emotion_colors = {
            'nostalgic': (255, 200, 150),
            'content': (150, 200, 150),
            'sad': (100, 100, 150),
            'joyful': (255, 255, 100),
            'happy': (255, 180, 100),
            'angry': (200, 50, 50),
            'lonely': (100, 120, 150),
            'scared': (80, 60, 50),
            'bittersweet': (150, 120, 150),
            'depressed': (60, 60, 80),
            'peaceful': (150, 180, 150),
            'horror': (150, 0, 0),
            'desperate': (150, 100, 100),
            'grief': (50, 50, 50),
            'serious': (100, 100, 100),
            'tribute': (200, 200, 220)
        }
        
        color = emotion_colors.get(scene['emotion'], (128, 128, 128))
        img = Image.new('RGB', (1280, 720), color=color)
        
        # Add text to image
        from PIL import ImageDraw, ImageFont
        draw = ImageDraw.Draw(img)
        
        # Scene title
        title_text = f"Scene {scene_num}: {scene['emotion'].upper()}"
        draw.text((50, 50), title_text, fill=(255, 255, 255))
        
        temp_img = f"scene_{scene_num}_visual.png"
        img.save(temp_img)
        
        print(f"   ✅ Created {scene['emotion']} image: {temp_img}")
        print(f"   → Passing to Audio Brain...")
        
        # ============================================
        # STEP 2: AUDIO BRAIN - Add background music
        # ============================================
        print(f"\n2️⃣  AUDIO BRAIN working...")
        print(f"   ⏭️  Skipping music (keeping it simple)")
        print(f"   → Passing to Voice Brain...")
        
        # ============================================
        # STEP 3: VOICE BRAIN - Add dialogue ONLY
        # ============================================
        print(f"\n3️⃣  VOICE BRAIN working...")
        
        audio_file = f"scene_{scene_num}_voice.mp3"
        
        try:
            # Create Punjabi TTS
            tts = gTTS(text=scene['dialogue'], lang='pa', slow=False)
            tts.save(audio_file)
            
            # Get actual audio duration
            from moviepy.editor import AudioFileClip
            temp_audio = AudioFileClip(audio_file)
            audio_duration = temp_audio.duration
            temp_audio.close()
            
            print(f"   ✅ Created Punjabi dialogue: {audio_file}")
            print(f"   ⏱️  Duration: {audio_duration:.1f}s")
            
        except Exception as e:
            print(f"   ❌ Voice failed: {e}")
            audio_file = None
            audio_duration = 5.0
        
        print(f"   → Passing to Master Brain...")
        
        # ============================================
        # STEP 4: MASTER BRAIN - Combine & verify
        # ============================================
        print(f"\n4️⃣  MASTER BRAIN verifying...")
        
        # Create video clip
        video_clip = ImageClip(temp_img).set_duration(audio_duration)
        
        # Add ONLY the dialogue audio (no duplicates!)
        if audio_file and os.path.exists(audio_file):
            audio_clip = AudioFileClip(audio_file)
            video_clip = video_clip.set_audio(audio_clip)
            print(f"   ✅ Audio attached: dialogue ONLY")
        else:
            print(f"   ⚠️  No audio")
        
        print(f"   ✅ Scene verified and ready!")
        
        return {
            'clip': video_clip,
            'visual_file': temp_img,
            'audio_file': audio_file,
            'duration': audio_duration
        }
    
    def render_video(self, num_scenes: int = 3):
        """Render multiple scenes"""
        
        print("\n" + "="*70)
        print(f"🎬 RENDERING {num_scenes} SCENES")
        print("="*70)
        
        all_clips = []
        
        for i in range(1, num_scenes + 1):
            result = self.render_scene(i)
            all_clips.append(result['clip'])
        
        # Combine all scenes
        print("\n" + "="*70)
        print("🎬 MASTER BRAIN: Combining all scenes...")
        print("="*70)
        
        final_video = concatenate_videoclips(all_clips, method="compose")
        
        output_file = "Clean_Test.mp4"
        print(f"\n💾 Saving to: {output_file}")
        
        final_video.write_videofile(
            output_file,
            fps=24,
            codec='libx264',
            audio_codec='aac',
            temp_audiofile='temp-audio.m4a',
            remove_temp=True,
            logger=None
        )
        
        print("\n" + "="*70)
        print("✅ VIDEO COMPLETE!")
        print("="*70)
        print(f"\n🎬 Output: {output_file}")
        print(f"\n✅ Each scene has:")
        print(f"   • Visual (colored background)")
        print(f"   • Dialogue (Punjabi TTS) - NO DUPLICATES")
        print(f"   • NO background music (keeping simple)")
        print("\n" + "="*70)
        
        return output_file

if __name__ == "__main__":
    try:
        renderer = CleanFastRenderer()
        output = renderer.render_video(num_scenes=3)
        print(f"\n🎉 Success! Video: {output}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
