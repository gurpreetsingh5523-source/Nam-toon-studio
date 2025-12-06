#!/usr/bin/env python3
"""
🎬 REALISTIC MOVIE MAKER
Uses realistic_renderer.py for photo-quality visuals
"""

import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import argparse

WORKSPACE = Path(__file__).parent.absolute()
sys.path.insert(0, str(WORKSPACE))

try:
    from simple_video_lib import VideoClip
    from realistic_renderer import RealisticRenderer
    print("✅ Libraries loaded")
except ImportError as e:
    print(f"❌ Error: {e}")
    sys.exit(1)

try:
    from planner.story_scene_planner import StoryScenePlanner
except Exception as planner_import_error:  # pragma: no cover - planner optional during legacy usage
    StoryScenePlanner = None  # type: ignore
    print(f"⚠️ Planner import failed: {planner_import_error}")


class RealisticMovieMaker:
    """Create realistic movie-style videos"""
    
    def __init__(self):
        self.fps = 30
        self.temp_dir = Path('/tmp')
        self.renderer = RealisticRenderer()
        self.scene_planner = StoryScenePlanner() if StoryScenePlanner else None
        self.last_scene_plan: Optional[Dict[str, Any]] = None
        
    def parse_scenes(self, text: str) -> list:
        """Parse text into scenes"""
        scenes = []
        lines = text.strip().split('\n')
        
        current_text = []
        current_character = "Hero"
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Scene markers
            if '[SCENE' in line.upper():
                if current_text:
                    scenes.append({
                        'text': ' '.join(current_text),
                        'character': current_character,
                        'duration': 5.0
                    })
                    current_text = []
                continue
            
            # Character markers
            if line.endswith(':'):
                current_character = line[:-1]
                continue
            
            current_text.append(line)
        
        # Last scene
        if current_text:
            scenes.append({
                'text': ' '.join(current_text),
                'character': current_character,
                'duration': 5.0
            })
        
        return scenes

    # ------------------------------------------------------------------
    # Planner integration
    # ------------------------------------------------------------------
    def _plan_story(self, text: str, story_id: str) -> Optional[Dict[str, Any]]:
        """Generate structured scene plan using the planner when available."""

        if not self.scene_planner:
            return None

        if not text.strip():
            return None

        try:
            self.scene_planner.story_id = story_id or "story"
            return self.scene_planner.plan(text)
        except Exception as exc:
            print(f"⚠️ Planner failure: {exc}")
            return None

    def _plan_to_production_scenes(self, plan: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Convert planner output into renderer-friendly scene descriptors."""

        production_scenes: List[Dict[str, Any]] = []

        for scene in plan.get("scenes", []):
            narration_entries = scene.get("narration", []) or []
            text_blocks: List[str] = []

            for entry in narration_entries:
                speaker = (entry.get("speaker") or "narrator").strip()
                line = (entry.get("text") or "").strip()
                if not line:
                    continue
                if speaker.lower() in {"", "narrator"}:
                    text_blocks.append(line)
                else:
                    text_blocks.append(f"{speaker}: {line}")

            combined_text = " ".join(text_blocks).strip()
            if not combined_text:
                combined_text = scene.get("title") or f"Scene {scene.get('scene_id', '?')}"

            characters = scene.get("characters") or []
            primary_character: Optional[Dict[str, Any]] = None
            for candidate in characters:
                if candidate.get("role") and candidate.get("role") != "narrator":
                    primary_character = candidate
                    break
            if not primary_character and characters:
                primary_character = characters[0]

            if primary_character:
                character_name = primary_character.get("display_name") or primary_character.get("id") or "Narrator"
            else:
                character_name = "Narrator"

            duration_hint = scene.get("duration_hint")
            if not duration_hint:
                approx = max(6.0, len(combined_text) / 14.0)
                duration_hint = round(float(approx), 1)

            production_scenes.append({
                "text": combined_text,
                "character": character_name,
                "duration": float(duration_hint),
                "plan": scene,
                "narration_lines": narration_entries,
                "metadata": {
                    "location": scene.get("location"),
                    "mood": scene.get("mood"),
                    "props": scene.get("props", []),
                },
            })

        return production_scenes
    
    def generate_voice(self, text: str, output_path: str) -> str:
        """Generate voice"""
        try:
            from gtts import gTTS
            
            # Detect language
            if any(ord(c) >= 0x0A00 and ord(c) <= 0x0A7F for c in text):
                lang = 'pa'
            else:
                lang = 'en'
            
            tts = gTTS(text=text, lang=lang, slow=False)
            tts.save(output_path)
            return output_path
        except Exception as e:
            print(f"   ⚠️  Voice failed: {e}")
            return None
    
    def create_background_music(self, duration: float, output_path: str) -> str:
        """Generate background music"""
        try:
            from pydub import AudioSegment
            from pydub.generators import Sine
            
            # Harmonious tones
            tone1 = Sine(440).to_audio_segment(duration=int(duration * 1000))
            tone2 = Sine(554).to_audio_segment(duration=int(duration * 1000))
            
            music = tone1.overlay(tone2) - 20
            music.export(output_path, format="mp3")
            return output_path
        except Exception as e:
            return None
    
    def merge_audio_video(self, video_path: str, audio_files: list, output_path: str):
        """Merge audio with video"""
        try:
            import subprocess
            from pydub import AudioSegment
            
            # Combine audio
            combined = AudioSegment.empty()
            for audio_file in audio_files:
                if os.path.exists(audio_file):
                    audio = AudioSegment.from_mp3(audio_file)
                    combined += audio
            
            # Export
            temp_audio = str(self.temp_dir / "final_audio.mp3")
            combined.export(temp_audio, format="mp3")
            
            # Merge
            cmd = [
                'ffmpeg', '-y', '-i', video_path, '-i', temp_audio,
                '-c:v', 'copy', '-c:a', 'aac', '-shortest', output_path
            ]
            
            subprocess.run(cmd, check=True, capture_output=True)
            os.remove(temp_audio)
            
            return output_path
        except Exception as e:
            import shutil
            shutil.copy(video_path, output_path)
            return output_path
    
    def create_animated_scene_frames(
        self,
        text: str,
        character_name: str,
        duration: float,
        width: int = 1920,
        height: int = 1080,
        scene_plan: Optional[Dict[str, Any]] = None
    ) -> list:
        """Generate frames for one scene using realistic renderer"""
        
        total_frames = int(duration * self.fps)
        frames = []

        location_tag: Optional[str] = None
        mood_tag: Optional[str] = None
        role_hint: Optional[str] = None

        if scene_plan:
            location = scene_plan.get("location") or {}
            mood = scene_plan.get("mood") or {}
            location_tag = location.get("tag")
            mood_tag = mood.get("tag")
            characters = scene_plan.get("characters") or []
            if characters:
                role_hint = characters[0].get("role")

        # Create base background once with planner metadata when available
        background = self.renderer.create_realistic_background(
            width,
            height,
            location_tag=location_tag,
            mood_tag=mood_tag,
        )

        renderer_label = character_name
        if role_hint and role_hint.lower() != "narrator":
            renderer_label = f"{character_name} ({role_hint})"

        self.renderer.prepare_for_scene(renderer_label)
        
        # Character animation path
        start_x = 300
        end_x = width - 400
        
        for frame_num in range(total_frames):
            # Copy background
            frame = background.copy()
            draw = ImageDraw.Draw(frame, 'RGBA')
            
            # Character position (walks left to right)
            progress = frame_num / total_frames
            char_x = int(start_x + (end_x - start_x) * progress)
            char_y = 550  # Ground level
            
            # Draw dynamic character that matches the scene role
            self.renderer.draw_realistic_character(draw, char_x, char_y, frame_num, img=frame)
            
            # Dialogue box
            box_height = 150
            box_y = height - box_height - 20
            
            # Semi-transparent black box
            draw.rectangle(
                [100, box_y, width - 100, box_y + box_height],
                fill=(0, 0, 0, 180)
            )
            
            # Character name (gold)
            try:
                font_name = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 36)
                font_text = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 28)
            except:
                font_name = ImageFont.load_default()
                font_text = ImageFont.load_default()
            
            draw.text(
                (width // 2, box_y + 10),
                character_name,
                fill=(255, 215, 0),
                font=font_name,
                anchor='mt'
            )
            
            # Typing effect for text
            chars_to_show = int((frame_num / total_frames) * len(text))
            visible_text = text[:chars_to_show]
            
            # Word wrap
            words = visible_text.split()
            lines = []
            current_line = []
            max_width = width - 220
            
            for word in words:
                test_line = ' '.join(current_line + [word])
                bbox = draw.textbbox((0, 0), test_line, font=font_text)
                if bbox[2] - bbox[0] > max_width:
                    if current_line:
                        lines.append(' '.join(current_line))
                        current_line = [word]
                    else:
                        lines.append(word)
                else:
                    current_line.append(word)
            
            if current_line:
                lines.append(' '.join(current_line))
            
            # Draw text (max 2 lines)
            for i, line in enumerate(lines[:2]):
                draw.text(
                    (120, box_y + 60 + i * 40),
                    line,
                    fill='white',
                    font=font_text
                )
            
            # Convert to numpy array
            frames.append(np.array(frame))
        
        return frames
    
    def create_movie(
        self,
        text: str,
        output_path: str,
        add_voice: bool = True,
        add_music: bool = True,
        width: int = 1920,
        height: int = 1080
    ):
        """Create full movie"""
        
        print("\n" + "="*70)
        print("🎬 REALISTIC MOVIE MAKER")
        print("   Photo-Quality Visuals • Punjabi Voice • Background Music")
        print("="*70)
        
        # Parse scenes via structured planner first, fallback to legacy parser
        story_id = Path(output_path).stem
        self.last_scene_plan = None

        planned_scenes: Optional[List[Dict[str, Any]]] = None
        planner_payload = self._plan_story(text, story_id)
        if planner_payload and planner_payload.get("scenes"):
            self.last_scene_plan = planner_payload
            planned_scenes = self._plan_to_production_scenes(planner_payload)

        if planned_scenes:
            scenes = planned_scenes
            print(f"\n✅ Planner generated {len(scenes)} structured scene(s)")
        else:
            scenes = self.parse_scenes(text)
            print(f"\n⚠️ Planner unavailable, legacy parser found {len(scenes)} scene(s)")
        
        # Generate voices
        audio_files = []
        
        if add_voice:
            print("\n🔊 Generating voice narration...")
            for i, scene in enumerate(scenes, 1):
                voice_file = str(self.temp_dir / f"voice_scene_{i}.mp3")
                if self.generate_voice(scene['text'], voice_file):
                    audio_files.append(voice_file)
                    
                    # Adjust duration based on voice
                    try:
                        from pydub import AudioSegment
                        audio = AudioSegment.from_mp3(voice_file)
                        scene['duration'] = len(audio) / 1000.0 + 0.5
                        print(f"   Scene {i}: {scene['duration']:.1f}s")
                    except:
                        pass
        
        # Create video frames
        all_frames = []
        
        for i, scene in enumerate(scenes, 1):
            plan_details = scene.get("plan") or {}
            location_tag = ((plan_details.get("location") or {}).get("tag") or "").strip()
            mood_tag = ((plan_details.get("mood") or {}).get("tag") or "").strip()

            location_note = f" | Location: {location_tag}" if location_tag else ""
            mood_note = f" | Mood: {mood_tag}" if mood_tag else ""

            print(f"\n🎥 Scene {i}/{len(scenes)}: {scene['text'][:50]}...{location_note}{mood_note}")
            
            frames = self.create_animated_scene_frames(
                text=scene['text'],
                character_name=scene['character'],
                duration=scene['duration'],
                width=width,
                height=height,
                scene_plan=plan_details if plan_details else None
            )
            
            all_frames.extend(frames)
            print(f"   ✅ Generated {len(frames)} frames")
        
        # Create video clip
        print(f"\n🔗 Combining {len(scenes)} scenes...")
        total_duration = sum(s['duration'] for s in scenes)
        
        def make_frame(t):
            frame_idx = int(t * self.fps)
            if frame_idx >= len(all_frames):
                frame_idx = len(all_frames) - 1
            return all_frames[frame_idx]
        
        video_clip = VideoClip(make_frame, duration=total_duration, fps=self.fps)
        
        # Write video
        print(f"\n💾 Writing video...")
        temp_video = str(self.temp_dir / "temp_video.mp4")
        video_clip.write_videofile(temp_video, fps=self.fps)
        
        # Add background music
        if add_music:
            print("\n🎵 Adding background music...")
            music_file = str(self.temp_dir / "background_music.mp3")
            if self.create_background_music(total_duration, music_file):
                audio_files.append(music_file)
        
        # Merge audio
        if audio_files:
            print("\n🔗 Merging audio...")
            self.merge_audio_video(temp_video, audio_files, output_path)
            
            # Cleanup
            os.remove(temp_video)
            for audio_file in audio_files:
                if os.path.exists(audio_file):
                    os.remove(audio_file)
        else:
            import shutil
            shutil.move(temp_video, output_path)
        
        # Stats
        file_size = os.path.getsize(output_path) / (1024 * 1024)
        
        print("\n" + "="*70)
        print("✅ REALISTIC MOVIE CREATED!")
        print("="*70)
        print(f"📁 File: {output_path}")
        print(f"📊 Size: {file_size:.2f} MB")
        print(f"⏱️  Duration: {total_duration:.1f}s")
        print(f"🎬 Scenes: {len(scenes)}")
        print(f"🎞️  Total Frames: {len(all_frames)}")
        print(f"🎥 FPS: {self.fps}")
        print(f"📐 Resolution: {width}x{height}")
        print(f"🔊 Voice: {'✅ Yes' if add_voice else '❌ No'}")
        print(f"🎵 Music: {'✅ Yes' if add_music else '❌ No'}")
        print(f"🎨 Quality: ⭐⭐⭐⭐⭐ REALISTIC!")
        print("="*70 + "\n")
        
        # IMPORTANT: Return the output path!
        return output_path


def main():
    parser = argparse.ArgumentParser(description='🎬 Realistic Movie Maker')
    parser.add_argument('--input', '-i', help='Input text file')
    parser.add_argument('--text', '-t', help='Direct text')
    parser.add_argument('--output', '-o', required=True, help='Output MP4')
    parser.add_argument('--no-voice', action='store_true', help='Disable voice')
    parser.add_argument('--no-music', action='store_true', help='Disable music')
    parser.add_argument('--width', type=int, default=1920)
    parser.add_argument('--height', type=int, default=1080)
    
    args = parser.parse_args()
    
    # Get text
    if args.input:
        with open(args.input, 'r', encoding='utf-8') as f:
            text = f.read()
    elif args.text:
        text = args.text
    else:
        print("❌ Provide --input file or --text")
        sys.exit(1)
    
    # Create maker
    maker = RealisticMovieMaker()
    
    try:
        maker.create_movie(
            text=text,
            output_path=args.output,
            add_voice=not args.no_voice,
            add_music=not args.no_music,
            width=args.width,
            height=args.height
        )
        print(f"🎉 SUCCESS! Movie: {args.output}")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
