#!/usr/bin/env python3
"""
🎬 ADVANCED VIDEO GENERATOR
With audio, sprite animation, and professional quality
"""

import cv2
import numpy as np
from pathlib import Path
from datetime import datetime
import json

# Import our systems
try:
    from audio_generator import AudioGenerator
    from character_sprite import CharacterSprite
except ImportError:
    print("⚠️  Import modules manually if needed")
    AudioGenerator = None
    CharacterSprite = None

class AdvancedVideoGenerator:
    def __init__(self):
        self.fps = 30
        self.resolution = (1280, 720)
        self.audio_gen = AudioGenerator() if AudioGenerator else None
        
    def create_professional_video(self, story):
        """Create professional video with all features"""
        print("🎬 ADVANCED VIDEO GENERATION")
        print("="*70)
        
        output_file = f"ADVANCED_{story['title'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
        
        # Setup video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video_temp = output_file.replace('.mp4', '_temp.mp4')
        out = cv2.VideoWriter(video_temp, fourcc, self.fps, self.resolution)
        
        # Create characters
        characters = {}
        for char_name in story.get('characters', ['Main']):
            characters[char_name] = CharacterSprite(char_name) if CharacterSprite else None
        
        print(f"✅ Created {len(characters)} characters")
        
        # Generate scenes
        frame_count = 0
        audio_texts = []
        
        for scene in story.get('scenes', []):
            print(f"🎬 Scene: {scene['name']}")
            
            duration_frames = int(scene['duration'] * self.fps)
            
            for i in range(duration_frames):
                # Create frame
                frame = np.ones((*self.resolution[::-1], 3), dtype=np.uint8) * 255
                
                # Add character (animated)
                if characters:
                    char = list(characters.values())[0]
                    if char:
                        pose = scene.get('action', 'idle')
                        if pose == 'walk':
                            sprite_frame = char.get_frame('walk', i)
                        elif pose == 'talk':
                            sprite_frame = char.get_frame('talk', i)
                        else:
                            sprite_frame = char.get_frame('idle')
                        
                        # Place sprite
                        frame = self.place_sprite(frame, sprite_frame, 300, 600)
                
                # Add dialogue
                if 'dialogue' in scene and i > duration_frames // 3:
                    cv2.putText(frame, scene['dialogue'], 
                               (50, 650), cv2.FONT_HERSHEY_SIMPLEX, 
                               1, (0, 0, 0), 2)
                
                out.write(frame)
                frame_count += 1
            
            if 'dialogue' in scene:
                audio_texts.append(scene['dialogue'])
        
        out.release()
        print(f"✅ Video frames generated: {frame_count}")
        
        # Add audio
        if self.audio_gen and audio_texts:
            print("🎵 Generating audio...")
            combined_text = " ... ".join(audio_texts)
            audio_file = self.audio_gen.generate_speech(
                combined_text, 
                output_file=output_file.replace('.mp4', '_audio.mp3')
            )
            
            if audio_file:
                print("🎵 Syncing audio to video...")
                final_video = self.audio_gen.sync_audio_to_video(
                    video_temp, audio_file, output_file
                )
                if final_video:
                    print(f"✅ Final video with audio: {output_file}")
                    Path(video_temp).unlink()  # Delete temp
                    return output_file
        
        # No audio - rename temp to final
        Path(video_temp).rename(output_file)
        print(f"✅ Video created (no audio): {output_file}")
        
        return output_file
    
    def place_sprite(self, frame, sprite, x, y):
        """Place animated sprite on frame"""
        if sprite is None:
            return frame
        
        h, w = sprite.shape[:2]
        y1 = max(0, y - h)
        y2 = min(frame.shape[0], y)
        x1 = max(0, x - w//2)
        x2 = min(frame.shape[1], x + w//2)
        
        if y2 <= y1 or x2 <= x1:
            return frame
        
        # Alpha blend
        sprite_rgb = sprite[:y2-y1, :x2-x1, :3]
        sprite_alpha = sprite[:y2-y1, :x2-x1, 3:4] / 255.0
        
        bg_region = frame[y1:y2, x1:x2]
        blended = sprite_rgb * sprite_alpha + bg_region * (1 - sprite_alpha)
        frame[y1:y2, x1:x2] = blended.astype(np.uint8)
        
        return frame

# Test
if __name__ == "__main__":
    generator = AdvancedVideoGenerator()
    
    test_story = {
        'title': 'Punjabi Greeting',
        'characters': ['Amrit'],
        'scenes': [
            {
                'name': 'Greeting',
                'duration': 3,
                'action': 'walk',
                'dialogue': 'ਸਤਿ ਸ੍ਰੀ ਅਕਾਲ'
            },
            {
                'name': 'Talking',
                'duration': 3,
                'action': 'talk',
                'dialogue': 'ਕਿਵੇਂ ਹੋ ਜੀ?'
            }
        ]
    }
    
    video = generator.create_professional_video(test_story)
    print(f"✅ Test video created: {video}")
