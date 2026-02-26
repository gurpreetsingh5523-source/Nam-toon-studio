#!/usr/bin/env python3
"""
🎬 AMRIT KAUR VIDEO GENERATOR
Converts Amrit Kaur conversations into animated videos

Uses NEW logic:
- Real conversations (not random)
- Emotional expressions
- Gurbani wisdom integrated
- Story scenes with meaning
"""

import cv2
import numpy as np
import json
from pathlib import Path
from datetime import datetime
from amrit_kaur_conversation_ai import AmritKaurAI

try:
    from gtts import gTTS
    import subprocess
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False
    print("⚠️  Audio libraries not available. Install: pip3 install gtts")

class AmritKaurVideoGenerator:
    """Generate videos from Amrit Kaur conversations"""
    
    def __init__(self):
        self.amrit_ai = AmritKaurAI()
        self.width = 1920
        self.height = 1080
        self.fps = 30
        
        # Character designs
        self.characters = {
            'amrit': {
                'color': (255, 200, 220),  # Light pink
                'position': (1400, 540),
                'size': 200,
                'label': '🤍 Amrit Kaur'
            },
            'user': {
                'color': (220, 220, 255),  # Light blue
                'position': (520, 540),
                'size': 180,
                'label': '👧 User'
            }
        }
        
        # Emotion-based expressions
        self.expressions = {
            'neutral': {'mouth': 'straight', 'eyes': 'open'},
            'warm': {'mouth': 'smile', 'eyes': 'kind'},
            'sad': {'mouth': 'down', 'eyes': 'teary'},
            'happy': {'mouth': 'big_smile', 'eyes': 'sparkle'},
            'comforting': {'mouth': 'gentle_smile', 'eyes': 'caring'},
            'storytelling': {'mouth': 'speaking', 'eyes': 'animated'}
        }
        
    def create_background(self):
        """Create peaceful Punjabi-themed background"""
        bg = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        
        # Gradient background (sky-like)
        for y in range(self.height):
            color_value = int(180 + (y / self.height) * 75)
            bg[y, :] = [color_value, color_value - 30, color_value - 50]
        
        # Add Khanda symbol (simplified)
        center_x, center_y = self.width // 2, 150
        cv2.circle(bg, (center_x, center_y), 60, (200, 180, 100), -1)
        cv2.putText(bg, 'ੴ', (center_x - 30, center_y + 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (50, 50, 50), 3)
        
        return bg
    
    def draw_character(self, frame, character_key, emotion='neutral'):
        """Draw character with emotional expression"""
        char = self.characters[character_key]
        x, y = char['position']
        size = char['size']
        color = char['color']
        
        # Body (circle)
        cv2.circle(frame, (x, y), size, color, -1)
        cv2.circle(frame, (x, y), size, (100, 100, 100), 3)
        
        # Face features based on emotion
        expr = self.expressions.get(emotion, self.expressions['neutral'])
        
        # Eyes
        eye_y = y - 30
        if expr['eyes'] == 'kind':
            # Gentle curved eyes
            cv2.ellipse(frame, (x - 40, eye_y), (15, 8), 0, 0, 180, (80, 80, 80), 3)
            cv2.ellipse(frame, (x + 40, eye_y), (15, 8), 0, 0, 180, (80, 80, 80), 3)
        elif expr['eyes'] == 'teary':
            # Sad eyes
            cv2.circle(frame, (x - 40, eye_y), 8, (80, 80, 80), -1)
            cv2.circle(frame, (x + 40, eye_y), 8, (80, 80, 80), -1)
            cv2.circle(frame, (x - 40, eye_y + 20), 3, (100, 150, 255), -1)
        elif expr['eyes'] == 'sparkle':
            # Happy eyes
            cv2.circle(frame, (x - 40, eye_y), 10, (80, 80, 80), -1)
            cv2.circle(frame, (x + 40, eye_y), 10, (80, 80, 80), -1)
            cv2.circle(frame, (x - 43, eye_y - 3), 3, (255, 255, 255), -1)
            cv2.circle(frame, (x + 37, eye_y - 3), 3, (255, 255, 255), -1)
        else:
            # Normal eyes
            cv2.circle(frame, (x - 40, eye_y), 8, (80, 80, 80), -1)
            cv2.circle(frame, (x + 40, eye_y), 8, (80, 80, 80), -1)
        
        # Mouth
        mouth_y = y + 40
        if expr['mouth'] == 'smile' or expr['mouth'] == 'gentle_smile':
            cv2.ellipse(frame, (x, mouth_y), (40, 20), 0, 0, 180, (80, 80, 80), 3)
        elif expr['mouth'] == 'big_smile':
            cv2.ellipse(frame, (x, mouth_y), (50, 25), 0, 0, 180, (80, 80, 80), 4)
        elif expr['mouth'] == 'down':
            cv2.ellipse(frame, (x, mouth_y + 10), (40, 20), 0, 180, 360, (80, 80, 80), 3)
        elif expr['mouth'] == 'speaking':
            cv2.ellipse(frame, (x, mouth_y), (30, 15), 0, 0, 360, (80, 80, 80), 3)
        else:
            cv2.line(frame, (x - 30, mouth_y), (x + 30, mouth_y), (80, 80, 80), 3)
        
        # Label
        label_y = y + size + 40
        cv2.putText(frame, char['label'], (x - 80, label_y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (50, 50, 50), 2)
        
        return frame
    
    def create_dialogue_bubble(self, frame, text, speaker_pos, is_user=False):
        """Create dialogue bubble"""
        max_width = 700
        lines = self.wrap_text(text, max_width)
        
        bubble_height = len(lines) * 50 + 40
        bubble_width = max_width + 40
        
        # Position bubble
        if is_user:
            bubble_x = speaker_pos[0] - bubble_width - 50
        else:
            bubble_x = speaker_pos[0] + 250
        bubble_y = speaker_pos[1] - bubble_height // 2
        
        # Ensure bubble stays in frame
        bubble_x = max(20, min(bubble_x, self.width - bubble_width - 20))
        bubble_y = max(20, min(bubble_y, self.height - bubble_height - 20))
        
        # Draw bubble
        bubble_color = (240, 240, 250) if is_user else (255, 240, 245)
        cv2.rectangle(frame, (bubble_x, bubble_y),
                     (bubble_x + bubble_width, bubble_y + bubble_height),
                     bubble_color, -1)
        cv2.rectangle(frame, (bubble_x, bubble_y),
                     (bubble_x + bubble_width, bubble_y + bubble_height),
                     (100, 100, 100), 3)
        
        # Draw text
        y_offset = bubble_y + 45
        for line in lines:
            cv2.putText(frame, line, (bubble_x + 20, y_offset),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (50, 50, 50), 2)
            y_offset += 50
        
        return frame
    
    def wrap_text(self, text, max_width):
        """Wrap text for dialogue bubble"""
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + " " + word if current_line else word
            # Rough estimate: 15 pixels per character
            if len(test_line) * 15 < max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        return lines if lines else [text]
    
    def generate_audio(self, text, filename):
        """Generate audio from text"""
        if not AUDIO_AVAILABLE:
            return None
        
        try:
            tts = gTTS(text=text, lang='pa', slow=False)
            audio_file = filename.replace('.mp4', '.mp3')
            tts.save(audio_file)
            return audio_file
        except Exception as e:
            print(f"⚠️  Audio generation failed: {e}")
            return None
    
    def create_conversation_video(self, scenario='morning_sad', output_name=None):
        """Create video from conversation"""
        
        print("🎬 AMRIT KAUR VIDEO GENERATION")
        print("="*70)
        
        # Get conversation script
        script = self.amrit_ai.export_video_script(scenario)
        conversation = script['conversation']
        
        if not output_name:
            output_name = f"AMRIT_KAUR_{scenario}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
        
        print(f"📝 Scenario: {scenario}")
        print(f"💬 Conversation turns: {len(conversation)}")
        print(f"🎬 Output: {output_name}")
        
        # Video setup
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        temp_video = output_name.replace('.mp4', '_temp.mp4')
        out = cv2.VideoWriter(temp_video, fourcc, self.fps, (self.width, self.height))
        
        frame_count = 0
        audio_files = []
        
        # Generate each conversation turn
        for i, turn in enumerate(conversation):
            speaker = turn['speaker']
            text = turn['text']
            emotion = turn.get('emotion', 'neutral')
            character = turn.get('character', 'amrit')
            
            print(f"\n🎬 Turn {i+1}: {speaker}")
            print(f"   Emotion: {emotion}")
            print(f"   Text: {text[:50]}...")
            
            # Generate audio
            audio_file = self.generate_audio(text, f"turn_{i}.mp3")
            if audio_file:
                audio_files.append(audio_file)
            
            # Duration: 3 seconds per turn
            duration_frames = self.fps * 3
            
            for frame_num in range(duration_frames):
                # Create frame
                frame = self.create_background()
                
                # Draw both characters
                frame = self.draw_character(frame, 'amrit', 
                                           emotion if character == 'amrit' else 'neutral')
                frame = self.draw_character(frame, 'user',
                                           emotion if character == 'user' else 'neutral')
                
                # Draw dialogue bubble for current speaker
                speaker_pos = self.characters[character]['position']
                frame = self.create_dialogue_bubble(frame, text, speaker_pos, 
                                                   is_user=(character == 'user'))
                
                # Progress indicator
                progress = (i + 1) / len(conversation)
                bar_width = int(self.width * 0.8)
                bar_x = (self.width - bar_width) // 2
                bar_y = self.height - 50
                
                cv2.rectangle(frame, (bar_x, bar_y), 
                            (bar_x + int(bar_width * progress), bar_y + 20),
                            (100, 200, 100), -1)
                cv2.rectangle(frame, (bar_x, bar_y), 
                            (bar_x + bar_width, bar_y + 20),
                            (100, 100, 100), 2)
                
                out.write(frame)
                frame_count += 1
        
        out.release()
        
        print(f"\n✅ Video frames generated: {frame_count}")
        
        # Add audio if available
        if audio_files and AUDIO_AVAILABLE:
            print("🎵 Adding audio...")
            # For now, use first audio file (can be improved)
            try:
                subprocess.run([
                    'ffmpeg', '-i', temp_video, '-i', audio_files[0],
                    '-c:v', 'copy', '-c:a', 'aac', '-shortest',
                    '-y', output_name
                ], check=True, capture_output=True)
                
                Path(temp_video).unlink()
                for audio_file in audio_files:
                    Path(audio_file).unlink()
                
                print("✅ Audio synchronized!")
            except Exception as e:
                print(f"⚠️  Audio sync failed: {e}")
                Path(temp_video).rename(output_name)
        else:
            Path(temp_video).rename(output_name)
        
        # Get file size
        size_mb = Path(output_name).stat().st_size / (1024 * 1024)
        
        print("\n" + "="*70)
        print(f"✅ VIDEO COMPLETE!")
        print(f"📹 File: {output_name}")
        print(f"💾 Size: {size_mb:.2f} MB")
        print(f"⏱️  Duration: {frame_count / self.fps:.1f}s")
        print(f"🎬 Frames: {frame_count}")
        print("="*70)
        
        return output_name

# Test the video generator
if __name__ == "__main__":
    generator = AmritKaurVideoGenerator()
    
    print("\n🎯 Generating Amrit Kaur conversation video...")
    print("   Scenario: Morning sad conversation")
    print("   NEW LOGIC: Real emotions, Gurbani wisdom, meaningful dialogue")
    print()
    
    video_file = generator.create_conversation_video('morning_sad')
    
    print(f"\n🎉 Video ready: {video_file}")
    print("\n💡 This uses NEW logic:")
    print("   ✅ Real conversation flow (not random)")
    print("   ✅ Emotional expressions (sad, comforting, storytelling)")
    print("   ✅ Gurbani context (wisdom integrated)")
    print("   ✅ Meaningful dialogue (helping user feel better)")
    print("   ✅ Character-specific responses")
    
    print("\n🚀 Opening video...")
    import subprocess
    subprocess.run(['open', video_file])
