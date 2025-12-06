#!/usr/bin/env python3
"""
🎬 ANIMATED MASTER BUILDER - Full Pipeline with Visual Animation
================================================================

Combines:
1. Audio brain (voice modulation, TTS)
2. Creative brain (behaviors, camera, timing)
3. Visual animation brain (character synthesis, animation)

Creates fully animated videos with moving, expressive characters!

Author: Amrit Core Team
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional
import argparse

# Import existing brains
sys.path.insert(0, str(Path(__file__).parent))
from visual_animation_brain import VisualAnimationBrain

# For video creation
try:
    from moviepy.editor import (
        VideoFileClip, AudioFileClip, ImageClip, 
        CompositeVideoClip, concatenate_videoclips,
        ImageSequenceClip
    )
    from gtts import gTTS
    import tempfile
except ImportError:
    print("⚠️  Installing required packages...")
    os.system("pip install moviepy gTTS")
    from moviepy.editor import *
    from gtts import gTTS
    import tempfile


class AnimatedMasterBuilder:
    """
    Master builder that creates fully animated videos with:
    - Synthesized character images
    - Animated movements and expressions
    - Voice-modulated audio
    - Scene composition and transitions
    """
    
    def __init__(self, scenes_file: str, output_dir: str = "animated_output"):
        self.scenes_file = scenes_file
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Load scenes
        with open(scenes_file, 'r', encoding='utf-8') as f:
            self.scenes = json.load(f)
        
        # Initialize visual animation brain
        print("🧠 Initializing Visual Animation Brain...")
        self.visual_brain = VisualAnimationBrain(
            output_dir=str(self.output_dir / "frames")
        )
        
        # Audio cache
        self.audio_cache = {}
        
        print("✅ Animated Master Builder ready!")
    
    def generate_audio_with_modulation(
        self,
        text: str,
        character: str,
        output_path: str
    ) -> str:
        """
        Generate TTS audio with voice modulation based on character.
        """
        # Character voice profiles (age/gender based modulation)
        voice_profiles = {
            "ਕੁਲਵੰਤ": {"pitch": 0.97, "speed": 1.10},  # Elderly male (lower, slower)
            "ਅਮਨਦੀਪ": {"pitch": 1.37, "speed": 1.16},  # Young female (higher, faster)
            "ਦਲਜੀਤ": {"pitch": 0.95, "speed": 1.05},  # Adult male
            "ਦਲੀਪ": {"pitch": 0.98, "speed": 1.08},  # Adult male
            "ਰਮਨਦੀਪ": {"pitch": 1.35, "speed": 1.14},  # Young female
            "ਜਸਪ੍ਰੀਤ": {"pitch": 1.50, "speed": 1.20},  # Child (higher, faster)
            "Narrator": {"pitch": 1.00, "speed": 1.00},  # Neutral
        }
        
        profile = voice_profiles.get(character, {"pitch": 1.0, "speed": 1.0})
        
        # Generate base TTS
        temp_base = output_path.replace('.mp3', '_base.mp3')
        tts = gTTS(text=text, lang='pa', slow=False)
        tts.save(temp_base)
        
        # Apply voice modulation with ffmpeg
        pitch_factor = profile["pitch"]
        speed_factor = profile["speed"]
        
        # Calculate ffmpeg parameters
        # atempo: 0.5 to 2.0 (speed)
        # asetrate: adjust pitch by changing sample rate
        asetrate_value = int(44100 / pitch_factor)
        
        cmd = f'ffmpeg -i "{temp_base}" -filter:a "atempo={speed_factor},asetrate={asetrate_value},aresample=44100" -y "{output_path}" -loglevel error'
        os.system(cmd)
        
        # Clean up temp file
        if os.path.exists(temp_base):
            os.remove(temp_base)
        
        print(f"🧠 {character}: pitch={pitch_factor:.2f}x, speed={speed_factor:.2f}x")
        return output_path
    
    def generate_scene_audio(self, scene_data: Dict, scene_idx: int) -> str:
        """Generate combined audio for a scene."""
        scene_audio_clips = []
        temp_files = []
        
        for dialogue_idx, dialogue in enumerate(scene_data.get("dialogues", [])):
            text = dialogue.get("text", "")
            character = dialogue.get("character", "Narrator")
            
            if not text.strip():
                continue
            
            # Generate audio with modulation
            audio_path = self.output_dir / f"scene_{scene_idx}_dialogue_{dialogue_idx}.mp3"
            self.generate_audio_with_modulation(text, character, str(audio_path))
            
            temp_files.append(str(audio_path))
            scene_audio_clips.append(AudioFileClip(str(audio_path)))
        
        # Combine all dialogue audio
        if scene_audio_clips:
            from moviepy.editor import concatenate_audioclips
            combined_audio = concatenate_audioclips(scene_audio_clips)
            combined_path = self.output_dir / f"scene_{scene_idx}_audio.mp3"
            combined_audio.write_audiofile(str(combined_path), logger=None)
            
            # Close clips
            for clip in scene_audio_clips:
                clip.close()
            
            # Clean up temp files
            for temp_file in temp_files:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            
            return str(combined_path)
        
        return None
    
    def render_scene(
        self,
        scene_data: Dict,
        scene_idx: int,
        fps: int = 24
    ) -> VideoFileClip:
        """
        Render a complete scene with animated characters and audio.
        """
        print(f"\n{'='*70}")
        print(f"🎬 Rendering Scene {scene_idx}")
        print(f"{'='*70}")
        
        # Generate audio first to get duration
        audio_path = self.generate_scene_audio(scene_data, scene_idx)
        
        if not audio_path:
            print("⚠️  No audio generated for scene, skipping...")
            return None
        
        audio_clip = AudioFileClip(audio_path)
        scene_duration = audio_clip.duration
        
        print(f"🎵 Audio duration: {scene_duration:.2f}s")
        
        # Generate animated frames
        frame_paths = self.visual_brain.generate_scene_frames(
            scene_data=scene_data,
            audio_duration=scene_duration,
            fps=fps,
            output_prefix=f"scene_{scene_idx}"
        )
        
        # Create video from frames
        print(f"🎞️  Creating video from {len(frame_paths)} frames...")
        video_clip = ImageSequenceClip(frame_paths, fps=fps)
        video_clip = video_clip.set_audio(audio_clip)
        
        print(f"✅ Scene {scene_idx} rendered: {scene_duration:.2f}s")
        
        # Clean up audio file
        audio_clip.close()
        
        return video_clip
    
    def render_full_video(
        self,
        output_file: str,
        scenes_limit: Optional[int] = None,
        fps: int = 24
    ):
        """
        Render complete video with all scenes.
        """
        print("\n" + "="*70)
        print("🚀 ANIMATED MASTER BUILDER - STARTING RENDER")
        print("="*70)
        
        # Limit scenes if requested
        scenes_to_render = self.scenes[:scenes_limit] if scenes_limit else self.scenes
        print(f"📊 Rendering {len(scenes_to_render)} scenes")
        
        # Render each scene
        scene_clips = []
        for scene_idx, scene_data in enumerate(scenes_to_render):
            scene_clip = self.render_scene(scene_data, scene_idx, fps=fps)
            if scene_clip:
                scene_clips.append(scene_clip)
        
        if not scene_clips:
            print("❌ No scenes rendered!")
            return
        
        # Concatenate all scenes
        print(f"\n🔗 Combining {len(scene_clips)} scenes...")
        final_video = concatenate_videoclips(scene_clips, method="compose")
        
        # Write final video
        print(f"💾 Writing final video: {output_file}")
        final_video.write_videofile(
            output_file,
            fps=fps,
            codec='libx264',
            audio_codec='aac',
            temp_audiofile=str(self.output_dir / 'temp_audio.m4a'),
            remove_temp=True,
            logger=None
        )
        
        # Cleanup
        for clip in scene_clips:
            clip.close()
        final_video.close()
        
        print("\n" + "="*70)
        print("✅ ANIMATED VIDEO COMPLETE!")
        print("="*70)
        print(f"📁 Output: {output_file}")
        print(f"⏱️  Duration: {sum(c.duration for c in scene_clips):.2f}s")
        print(f"🎬 Scenes: {len(scene_clips)}")


def main():
    parser = argparse.ArgumentParser(
        description='🎬 Animated Master Builder - Create animated videos with moving characters'
    )
    parser.add_argument(
        '--scenes',
        type=str,
        required=True,
        help='Path to scenes JSON file'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='animated_video.mp4',
        help='Output video file path'
    )
    parser.add_argument(
        '--scenes-limit',
        type=int,
        help='Limit number of scenes to render (for testing)'
    )
    parser.add_argument(
        '--fps',
        type=int,
        default=24,
        help='Frames per second'
    )
    
    args = parser.parse_args()
    
    # Create builder
    builder = AnimatedMasterBuilder(args.scenes)
    
    # Render video
    builder.render_full_video(
        output_file=args.output,
        scenes_limit=args.scenes_limit,
        fps=args.fps
    )


if __name__ == "__main__":
    main()
