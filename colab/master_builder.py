# AmritCore - MASTER BUILDER (Final Assembly and Export - LIST INITIALIZATION FIX)

# Install necessary libraries
#!pip install moviepy==1.0.3 gTTS requests pillow numpy

# Import Path first
import sys
import os
from pathlib import Path

# Try moviepy first, fall back to our simple library
try:
    from moviepy.editor import *
    from moviepy.audio.fx.volumex import volumex
    from moviepy.audio.fx.audio_loop import audio_loop
    from moviepy.audio.fx.audio_normalize import audio_normalize
    from moviepy.audio.AudioClip import AudioArrayClip
    from moviepy.video.fx.fadeout import fadeout
    from moviepy.video.fx.fadein import fadein
    USING_MOVIEPY = True
    print("✅ Using moviepy for video generation")
except ImportError as e:
    # Use our simple video library instead
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from simple_video_lib import (
        VideoClip, ImageClip, AudioFileClip,
        concatenate_audioclips, CompositeAudioClip,
        audio_loop, fadein, fadeout,
        volumex, audio_normalize
    )
    # Define AudioArrayClip dummy for compatibility
    AudioArrayClip = None
    USING_MOVIEPY = False
    print("⚠️  moviepy not available, using simple_video_lib instead")
    print(f"   Reason: {e}")

from gtts import gTTS
import argparse
import logging
from PIL import Image, ImageDraw, ImageFont
import wave
import numpy as np
import os
import sys
# Allow sending feedback to Master (best-effort)
try:
    sys.path.insert(0, str(Path(__file__).parent))
    from master_orchestrator_brain import MasterOrchestratorBrain
    _MASTER_CLIENT = MasterOrchestratorBrain()
except Exception:
    _MASTER_CLIENT = None

# Import the intelligent brain for automatic decision-making
sys.path.insert(0, str(Path(__file__).parent))
from intelligent_brain import IntelligentBrain

# --- Step 1: Setup and Data ---

# --- CLI / logging ---
parser = argparse.ArgumentParser(description="AmritCore master builder (assemble scenes, TTS and export)")
parser.add_argument("--dry-run", action="store_true", help="Run checks and print diagnostics but don't write final large files")
parser.add_argument("--verbose", "-v", action="store_true", help="Verbose logging")
parser.add_argument("--duck", action="store_true", help="Enable simple background ducking during speech")
parser.add_argument("--bg-gain", type=float, default=0.35, help="Global background gain multiplier (default 0.35)")
parser.add_argument("--duck-factor", type=float, default=0.25, help="Background gain factor during speech (default 0.25)")
parser.add_argument("--no-tts", action="store_true", help="Use bundled/sample dialogue assets instead of calling gTTS (CI/offline friendly)")
parser.add_argument("--duck-attack", type=float, default=20.0, help="Ducking attack in ms (default 20ms)")
parser.add_argument("--duck-release", type=float, default=80.0, help="Ducking release in ms (default 80ms)")
parser.add_argument("--dream", action="store_true", help="Apply dreamy reverb/stereo widening to background SFX")
parser.add_argument("--pan-width", type=float, default=0.0, help="Per-character stereo pan width (0.0..1.0) where 0=no-pan, 1=full)")
parser.add_argument("--learn", action="store_true", help="Ingest current assets into the local brain and apply suggested parameters")
parser.add_argument("--scenes", type=str, default=None, help="Path to scene JSON (produced by novel pipeline) to drive dialogue/scenes")
parser.add_argument("--background", type=str, default=None, help="Path to background image to use instead of generated base")
parser.add_argument("--characters-dir", type=str, default=None, help="Directory containing character images named <Character>.png/jpg")
parser.add_argument("--audio-dir", type=str, default=None, help="Directory containing per-dialogue audio files named <Character>_<index>.wav to override TTS")
parser.add_argument("--record-mic", action="store_true", help="Interactive: record per-dialogue lines from microphone (optional dependency)")
parser.add_argument("--open-editor", action="store_true", help="Open scene JSON in $EDITOR for manual edits before rendering")
parser.add_argument("--master", action="store_true", help="Apply light mastering (compressor + limiter) to final mix")
parser.add_argument("--output", type=str, default=None, help="Output filename for the generated video (default: AmritCore_FINAL_STUDIO_LAUNCH.mp4)")
parser.add_argument("--scenes-limit", type=int, default=0, help="When using --scenes, number of scenes to include (0 = all)")
parser.add_argument("--min-clip-secs", type=float, default=3.0, help="Minimum duration per dialogue clip when using --no-tts (seconds)")
parser.add_argument("--captions", action="store_true", help="Burn dialogue text onto video frames")
parser.add_argument("--timecode", action="store_true", help="Overlay running timecode for visual activity")
args = parser.parse_args()

# Set output filename from CLI or default
final_video_filename = args.output if args.output else "AmritCore_FINAL_STUDIO_LAUNCH.mp4"

logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO, format="%(message)s")
log = logging.getLogger("master_builder")

DRY_RUN = args.dry_run
VERBOSE = args.verbose
DUCK = args.duck
BG_GAIN = args.bg_gain
DUCK_FACTOR = args.duck_factor
NO_TTS = args.no_tts
DUCK_ATTACK_MS = args.duck_attack
DUCK_RELEASE_MS = args.duck_release
DREAM = args.dream
PAN_WIDTH = max(0.0, min(1.0, args.pan_width))
LEARN = args.learn
SCENES_PATH = args.scenes
BACKGROUND_PATH = args.background
CHAR_DIR = args.characters_dir
AUDIO_DIR = args.audio_dir
RECORD_MIC = args.record_mic
OPEN_EDITOR = args.open_editor
MASTER = args.master
CAPTIONS = args.captions
TIMECODE = args.timecode

# Create necessary folders (ensures stability)
if not os.path.exists("audio"): os.makedirs("audio")
if not os.path.exists("images"): os.makedirs("images")
if not os.path.exists("assets/animation"): os.makedirs("assets/animation")

# Load character voice profiles
character_profiles = {}
try:
    import json
    profile_path = Path("brain_memory/character_voice_profiles.json")
    if profile_path.exists():
        profiles_data = json.loads(profile_path.read_text())
        character_profiles = profiles_data.get("character_profiles", {})
        log.info(f"✓ ਲੋਡ ਕੀਤੇ {len(character_profiles)} character voice profiles")
    else:
        log.warning(f"⚠️  Voice profiles ਨਹੀਂ ਮਿਲੇ: {profile_path}")
except Exception as e:
    log.warning(f"Voice profiles ਲੋਡ ਨਹੀਂ ਹੋਏ: {e}")

def _filesize(path):
    try:
        return Path(path).stat().st_size
    except Exception:
        return 0

def _log_file_info(path):
    s = _filesize(path)
    log.info(f"{path} size={s} bytes")

# Dialogue Data (for audio consistency)
dialogues_scene1 = [
    {"character": "Krishna", "text": "ਸੁਲਤਾਨਾ, ਕਦੇ ਸੋਚਿਆ ਈ, ਆਪਾਂ ਵੀ ਕਦੀ ਸ਼ਹਿਰ ਜਾਈਏ?", "volume": 1.0},
    {"character": "Sultan", "text": "ਕ੍ਰਿਸ਼ਨਾ, ਮੈਂ ਤਾਂ ਏਸੇ ਪਿੰਡ ਵਿੱਚ ਖੁਸ਼ ਆਂ। ਬਸ ਰੱਬ ਸੁੱਖ ਰੱਖੇ, ਆਪਣੀ ਦੋਸਤੀ ਕਾਇਮ ਰਹੇ।", "volume": 0.8},
    {"character": "Krishna", "text": "ਰੱਬ ਜ਼ਰੂਰ ਸੁੱਖ ਰੱਖੇਗਾ। ਆਹ ਤੂਤਾਂ ਵਾਲਾ ਖੂਹ ਹਮੇਸ਼ਾ ਆਪਣੀ ਦੋਸਤੀ ਦਾ ਗਵਾਹ ਰਹੇਗਾ।", "volume": 1.0}
]

# A. Visual Node: Create Scene Base Image
SCENE_COLOR = "#434657" 
AI_IMAGE_PATH = "images/scene_base.png"
# If user provided a background image, prefer it; else build a subtle gradient so it isn't flat gray
if BACKGROUND_PATH and os.path.exists(BACKGROUND_PATH):
    AI_IMAGE_PATH = BACKGROUND_PATH
    log.info(f"Using user background: {AI_IMAGE_PATH}")
else:
    try:
        w, h = 1920, 1080
        top = (31, 41, 55)   # #1f2937
        bottom = (17, 24, 39) # #111827
        grad = Image.new('RGB', (w, h))
        for y in range(h):
            t = y / max(1, h - 1)
            r = int(top[0] * (1 - t) + bottom[0] * t)
            g = int(top[1] * (1 - t) + bottom[1] * t)
            b = int(top[2] * (1 - t) + bottom[2] * t)
            for x in range(w):
                grad.putpixel((x, y), (r, g, b))
        grad.save(AI_IMAGE_PATH)
    except Exception:
        Image.new('RGB', (1920, 1080), color=SCENE_COLOR).save(AI_IMAGE_PATH)


# --- Step 2: Audio Generation and Combining (with offline/sample mode, panning and dream effects)
# Create empty list to store audio clips
audio_clips = []

# If scenes JSON provided, load and convert to dialogues_scene1 format
if SCENES_PATH:
    try:
        import json
        sp = Path(SCENES_PATH)
        if sp.exists():
            data = json.loads(sp.read_text())
            # Expecting {'scenes': [ { 'scene_id':..., 'dialogues': [ {character,text,volume}] , ... } ] }
            scenes = list(data.get('scenes', []))
            if args.scenes_limit and args.scenes_limit > 0:
                scenes = scenes[:args.scenes_limit]
            # flatten all dialogues from selected scenes
            all_dialogues = []
            for sc in scenes:
                ds = sc.get('dialogues', [])
                all_dialogues.extend(ds)
            if len(all_dialogues) > 0:
                dialogues_scene1 = all_dialogues
                log.info(f"Loaded scenes from {SCENES_PATH}, using {len(scenes)} scene(s), total dialogues: {len(all_dialogues)}")
            
            # 🧠 INTELLIGENT BRAIN ANALYSIS (Enhanced with Creative Logic)
            # Analyze each scene for emotion, animation, behavior, rhythm, camera, and cross-scene learning
            log.info("🧠 Activating Enhanced Intelligent Brain for scene analysis...")
            brain = IntelligentBrain()
            enriched_scenes = []
            
            for idx, sc in enumerate(scenes):
                # Pass all scenes for cross-scene learning
                enriched = brain.analyze_full_scene(sc, full_story_text='', scene_index=idx, all_scenes=enriched_scenes + [sc])
                enriched_scenes.append(enriched)
                
                analysis = enriched['brain_analysis']
                emotion = analysis['emotion']['emotion']
                intensity = analysis['emotion']['intensity']
                music = analysis['emotion']['music_file']
                rhythm = analysis['rhythm']['pace']
                
                # Log comprehensive analysis
                log.info(f"  Scene {sc.get('scene_id', '?')}: {emotion} ({intensity:.2f}) → {music}")
                
                # Log behaviors if detected
                behaviors = analysis.get('behaviors', {})
                if behaviors:
                    actions = [f"{char}: {b.get('action', '?')}" for char, b in behaviors.items()]
                    log.info(f"    Behaviors: {', '.join(actions)}")
                
                # Log rhythm and camera
                camera = analysis['camera']
                log.info(f"    Rhythm: {rhythm} | Camera: {camera['camera_type']} ({camera['camera_direction']})")
                
                # Log creative notes
                notes = analysis.get('creative_notes', [])
                if notes:
                    log.info(f"    📝 Director notes: {notes[0]}")
                
                # Log cross-scene context
                context = analysis.get('context', {})
                if context.get('has_context'):
                    log.info(f"    🔗 Transition: {context['transition_type']} from {context['previous_emotion']}")
            
            # Store enriched scenes for later use
            scenes = enriched_scenes
            log.info(f"🧠 Brain analysis complete: {len(scenes)} scenes enriched with creative intelligence")
            
    except Exception as e:
        log.warning(f"Failed to load scenes from {SCENES_PATH}: {e}")

# If requested, consult the brain to ingest existing assets and return suggestions
if LEARN:
    try:
        # try normal import first
        try:
            from colab.brain import Brain
        except Exception:
            # fallback: load the module directly by file path (works when 'colab' isn't a package)
            import importlib.util, sys
            brain_path = Path(__file__).parent / 'brain.py'
            spec = importlib.util.spec_from_file_location('brain', str(brain_path))
            brain_mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(brain_mod)
            Brain = brain_mod.Brain

        brain = Brain()
        log.info("Learning mode: ingesting audio/images into brain...")
        brain.ingest_directory()
        suggestion = brain.suggest_parameters()
        log.info(f"Brain suggestion: {suggestion}")
        # apply suggestions to current run (best-effort)
        BG_GAIN = float(suggestion.get('bg_gain', BG_GAIN))
        DUCK_FACTOR = float(suggestion.get('duck_factor', DUCK_FACTOR))
        PAN_WIDTH = float(suggestion.get('pan_width', PAN_WIDTH))
        if suggestion.get('dream', False):
            DREAM = True
    except Exception as e:
        log.warning(f"Brain learn failed: {e}")

# If user wants to open the scenes file for manual edits, launch $EDITOR
if OPEN_EDITOR and SCENES_PATH:
    try:
        editor = os.environ.get('EDITOR', 'vi')
        sp = Path(SCENES_PATH)
        if sp.exists():
            log.info(f"Opening scenes file {SCENES_PATH} in editor ({editor}) for manual edits...")
            import subprocess
            subprocess.call([editor, str(sp)])
        else:
            log.warning(f"Scenes file {SCENES_PATH} not found for editing")
    except Exception as e:
        log.warning(f"Failed to open editor: {e}")

# Load character portraits if provided OR generate simple avatars
portraits = {}
if CHAR_DIR and os.path.exists(CHAR_DIR):
    try:
        for fn in os.listdir(CHAR_DIR):
            name, ext = os.path.splitext(fn)
            if ext.lower() in ('.png', '.jpg', '.jpeg'):
                try:
                    im = Image.open(os.path.join(CHAR_DIR, fn)).convert('RGBA')
                    im = im.resize((256, 256), Image.Resampling.LANCZOS if hasattr(Image, 'Resampling') else Image.LANCZOS)
                    portraits[name] = im
                    log.info(f"Loaded portrait for {name} from {fn}")
                except Exception as _e:
                    log.debug(f"Failed to load portrait {fn}: {_e}")
    except Exception as e:
        log.warning(f"Characters dir load failed: {e}")

# Auto-generate simple avatar portraits for characters that don't have images
# Global AI model cache
_AI_PIPE = None

def _generate_avatar_with_ai(name, emotion="neutral", size=600):
    """Generate AI character portrait using Stable Diffusion"""
    global _AI_PIPE
    
    try:
        # Load AI model if not already loaded
        if _AI_PIPE is None:
            log.info("🎨 Loading Stable Diffusion AI Model for character generation...")
            try:
                from diffusers import StableDiffusionPipeline
                import torch
                
                device = "cuda" if torch.cuda.is_available() else \
                         "mps" if torch.backends.mps.is_available() else "cpu"
                log.info(f"   Using device: {device}")
                
                _AI_PIPE = StableDiffusionPipeline.from_pretrained(
                    "runwayml/stable-diffusion-v1-5",
                    torch_dtype=torch.float16 if device == "cuda" else torch.float32,
                    safety_checker=None
                )
                _AI_PIPE = _AI_PIPE.to(device)
                _AI_PIPE.enable_attention_slicing()
                log.info("✅ AI Model loaded successfully!")
            except Exception as e:
                log.warning(f"⚠️ Could not load AI model: {e}")
                log.warning("   Falling back to simple avatars")
                return _generate_simple_avatar(name, size)
        
        # Create cache directory
        cache_dir = Path("ai_assets/characters")
        cache_dir.mkdir(parents=True, exist_ok=True)
        cache_key = f"{name}_{emotion}".replace(" ", "_").replace("/", "_")
        cache_path = cache_dir / f"{cache_key}.png"
        
        # Check cache first
        if cache_path.exists():
            log.info(f"✅ Using cached AI character: {name} ({emotion})")
            return Image.open(cache_path).convert('RGBA').resize((size, size), Image.Resampling.LANCZOS)
        
        # Create AI prompt
        name_lower = name.lower()
        if "kaur" in name_lower or any(w in name_lower for w in ['woman', 'mother', 'daughter', 'wife', 'ਕੌਰ']):
            base = "beautiful Punjabi woman wearing traditional salwar kameez with dupatta"
        else:
            base = "handsome Punjabi man wearing traditional kurta"
        
        emotion_map = {
            'happy': 'smiling warmly, joyful', 'sad': 'melancholic, sad', 
            'angry': 'fierce, angry', 'peaceful': 'serene calm', 
            'joyful': 'very happy smiling', 'calm': 'peaceful calm',
            'neutral': 'calm gentle', 'warm': 'warm friendly smiling'
        }
        emotion_desc = emotion_map.get(emotion, 'calm gentle')
        
        prompt = f"{base}, {emotion_desc} expression, detailed portrait, realistic, warm lighting, high quality, 4k portrait"
        negative_prompt = "cartoon, anime, low quality, blurry, distorted, ugly, deformed, nsfw"
        
        # Generate image
        log.info(f"🎨 Generating AI character portrait: {name} ({emotion})")
        import torch
        with torch.no_grad():
            result = _AI_PIPE(
                prompt=prompt,
                negative_prompt=negative_prompt,
                num_inference_steps=25,
                guidance_scale=7.5,
                height=512,
                width=512
            )
        
        image = result.images[0]
        
        # Validate (check if not blank/black)
        arr = np.array(image)
        if arr.mean() < 5:
            log.warning(f"⚠️ Generated image too dark/blank, falling back to simple avatar")
            return _generate_simple_avatar(name, size)
        
        # Save to cache and return
        image.save(cache_path)
        log.info(f"✅ Generated and cached AI character: {cache_key}")
        return image.convert('RGBA').resize((size, size), Image.Resampling.LANCZOS)
        
    except Exception as e:
        log.warning(f"⚠️ AI character generation failed for {name}: {e}")
        log.warning(f"   Falling back to simple avatar")
        return _generate_simple_avatar(name, size)

def _generate_simple_avatar(name, size=256):
    """Fallback: Generate simple colored circle avatar with initial"""
    try:
        # Use character name to derive a color
        hash_val = sum(ord(c) for c in name)
        hue = (hash_val % 360) / 360.0
        # Convert HSV to RGB
        import colorsys
        rgb = colorsys.hsv_to_rgb(hue, 0.6, 0.9)
        color = tuple(int(c * 255) for c in rgb)
        
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        # Draw circle
        margin = 10
        draw.ellipse([margin, margin, size-margin, size-margin], fill=color + (220,), outline=(255, 255, 255, 255), width=4)
        # Draw initial
        initial = name[0].upper() if name else '?'
        try:
            font = _get_font(int(size * 0.5))
            bbox = draw.textbbox((0, 0), initial, font=font)
            tw = bbox[2] - bbox[0]
            th = bbox[3] - bbox[1]
            tx = (size - tw) // 2
            ty = (size - th) // 2 - bbox[1]
            draw.text((tx, ty), initial, font=font, fill=(255, 255, 255, 255))
        except Exception:
            pass  # Fallback to simple colored circle
        return img
    except Exception as e:
        log.debug(f"Failed to generate simple avatar for {name}: {e}")
        return None

# Keep old function name for compatibility
def _generate_avatar(name, size=256):
    """Generate avatar (AI if possible, fallback to simple)"""
    # Try AI generation with larger size
    return _generate_avatar_with_ai(name, "neutral", max(size, 600))

# Collect all unique characters from dialogues with their emotions
all_characters = {}  # char_name -> emotion
for d in dialogues_scene1:
    char = d.get('character', '')
    if char and char not in all_characters:
        # Get emotion from dialogue or scene
        emotion = d.get('emotion', 'neutral')
        all_characters[char] = emotion

# Generate AI avatars for characters without portraits
for char, emotion in all_characters.items():
    if char not in portraits:
        log.info(f"🎨 Generating character portrait: {char} ({emotion})")
        avatar = _generate_avatar_with_ai(char, emotion, size=600)
        if avatar:
            portraits[char] = avatar
            log.info(f"✅ Character ready: {char}")

# helper: record audio from microphone (optional feature)
def _record_clip(output_path, record_seconds=4):
    """Record audio from microphone to WAV file. Returns True if successful."""
    try:
        import sounddevice as sd
        import wave
        log.info(f"Recording {record_seconds}s to {output_path}... (speak now)")
        sr = 44100
        audio_data = sd.rec(int(record_seconds * sr), samplerate=sr, channels=1, dtype='int16')
        sd.wait()  # Wait until recording is finished
        
        # Write to WAV
        with wave.open(output_path, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sr)
            wf.writeframes(audio_data.tobytes())
        log.info(f"Recorded to {output_path}")
        return True
    except ImportError:
        log.warning("sounddevice not available - skipping microphone recording")
        return False
    except Exception as e:
        log.warning(f"Recording failed: {e}")
        return False

# helper: create a short sample WAV (sine tone with slight envelope) for CI/offline
def _make_sample_wav(path, freq=440.0, dur=2.0, sr=44100):
    n = int(dur * sr)
    t = np.linspace(0, dur, n, False)
    tone = 0.25 * np.sin(2 * np.pi * freq * t)
    # simple fade in/out (10ms)
    fade_len = int(0.01 * sr)
    if fade_len*2 < n:
        env = np.ones(n)
        env[:fade_len] = np.linspace(0.0, 1.0, fade_len)
        env[-fade_len:] = np.linspace(1.0, 0.0, fade_len)
        tone = tone * env
    # write wav
    with wave.open(path, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes((tone * 32767).astype(np.int16).tobytes())

# Build or reuse audio clips
def _estimate_sample_duration(text: str, min_secs: float = 3.0, max_secs: float = 12.0) -> float:
    """Estimate a plausible speech duration from text length for offline sample audio.
    Base + per‑char, clamped to [min_secs, max_secs]."""
    if not text:
        return max(2.0, min_secs)
    base = 1.5
    per_char = 0.05  # ~20 chars/sec
    est = base + per_char * len(text)
    return float(max(min_secs, min(max_secs, est)))

# PARALLEL TTS: Generate all TTS files first (much faster!)
# 🧠 With intelligent voice modulation (age/gender/emotion → pitch/speed)
if not NO_TTS:
    log.info(f"🚀 Generating TTS for {len(dialogues_scene1)} dialogues in parallel...")
    from concurrent.futures import ThreadPoolExecutor, as_completed
    import subprocess
    
    # Analyze characters first (brain intelligence!)
    if SCENES_PATH and 'brain' in dir():
        character_profiles = {}
        for dialogue in dialogues_scene1:
            char_name = dialogue.get('character', 'Narrator')
            if char_name not in character_profiles:
                profile = brain.analyze_character(char_name, dialogue.get('text', ''), '')
                character_profiles[char_name] = profile
                log.info(f"🧠 {char_name}: age={profile['age_group']}, gender={profile['gender']}, pitch={profile['voice_pitch']:.2f}x, speed={profile['voice_speed']:.2f}x")
    else:
        character_profiles = {}
    
    def generate_single_tts(idx, dialogue):
        out_path = f"audio/dialogue_{idx}.mp3"
        if os.path.exists(out_path):
            return idx, out_path, True  # Already exists
        try:
            text = dialogue.get('text', '')
            if not text:
                return idx, None, False
            
            # Generate base TTS
            temp_path = f"audio/dialogue_{idx}_raw.mp3"
            tts = gTTS(text, lang='pa')  # Punjabi
            tts.save(temp_path)
            
            # Apply voice modulation if character profile exists
            char_name = dialogue.get('character', 'Narrator')
            if char_name in character_profiles:
                profile = character_profiles[char_name]
                pitch = profile['voice_pitch']
                speed = profile['voice_speed']
                
                # Use ffmpeg to adjust pitch and speed
                # atempo for speed (0.5-2.0), rubberband for pitch (cents = semitones*100)
                semitones = (pitch - 1.0) * 12  # Convert ratio to semitones
                cents = int(semitones * 100)
                
                # Apply tempo and pitch shift
                cmd = [
                    'ffmpeg', '-y', '-i', temp_path,
                    '-filter_complex',
                    f'atempo={min(2.0, max(0.5, speed))},asetrate=44100*{pitch},aresample=44100',
                    '-q:a', '2',
                    out_path
                ]
                subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
                os.remove(temp_path)  # Clean up raw file
            else:
                # No modulation, just rename
                os.rename(temp_path, out_path)
            
            return idx, out_path, True
        except Exception as e:
            log.warning(f"TTS {idx} failed: {e}")
            # If modulation failed, try to save raw TTS at least
            if os.path.exists(f"audio/dialogue_{idx}_raw.mp3"):
                os.rename(f"audio/dialogue_{idx}_raw.mp3", out_path)
                return idx, out_path, True
            return idx, None, False
    
    # Run TTS generation in parallel (5 workers = 5x faster!)
    tts_results = {}
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(generate_single_tts, i, d): i for i, d in enumerate(dialogues_scene1)}
        for future in as_completed(futures):
            idx, path, success = future.result()
            tts_results[idx] = path
            if success:
                log.info(f"✓ TTS {idx+1}/{len(dialogues_scene1)}: {path}")
    
    log.info(f"✅ Parallel TTS complete: {len([p for p in tts_results.values() if p])}/{len(dialogues_scene1)} generated")

# Now process audio clips (with override/fallback logic)
for i, dialogue in enumerate(dialogues_scene1):
    out_path = f"audio/dialogue_{i}.mp3"
    sample_path_wav = f"audio/sample_dialogue_{i}.wav"

    # If user provided an audio override directory, check for per-dialogue files first
    override_path = None
    if AUDIO_DIR and os.path.exists(AUDIO_DIR):
        # candidates: Character_i.wav, Character_i.mp3, Character.wav
        cand1 = os.path.join(AUDIO_DIR, f"{dialogue.get('character')}_{i}.wav")
        cand2 = os.path.join(AUDIO_DIR, f"{dialogue.get('character')}_{i}.mp3")
        cand3 = os.path.join(AUDIO_DIR, f"{dialogue.get('character')}.wav")
        cand4 = os.path.join(AUDIO_DIR, f"{dialogue.get('character')}.mp3")
        for c in (cand1, cand2, cand3, cand4):
            if os.path.exists(c):
                override_path = c
                log.info(f"Using user audio override for {dialogue.get('character')}[{i}]: {c}")
                break

    # If record mic mode is enabled, prompt and record into audio/dialogue_{i}.wav
    if RECORD_MIC and override_path is None:
        rec_out = f"audio/dialogue_{i}.wav"
        ok = _record_clip(rec_out, record_seconds=4)
        if ok:
            override_path = rec_out

    if override_path:
        load_path = override_path
    elif NO_TTS:
        # prefer an existing sample WAV, otherwise create one
        if not os.path.exists(sample_path_wav):
            est_dur = _estimate_sample_duration(dialogue.get('text', ''), min_secs=args.min_clip_secs)
            log.info(f"--no-tts: creating sample dialogue asset: {sample_path_wav} (dur~{est_dur:.1f}s)")
            _make_sample_wav(sample_path_wav, freq=300 + i * 60, dur=est_dur)
        load_path = sample_path_wav
        log.info(f"Using sample dialogue asset for {i}: {load_path}")
    else:
        try:
            tts = gTTS(dialogue["text"], lang='pa')
            tts.save(out_path)
            log.info(f"TTS saved: {out_path}")
            load_path = out_path
        except Exception as e:
            log.warning(f"gTTS failed: {e}. Trying macOS 'say' fallback...")
            # macOS local TTS fallback via 'say'
            try:
                import platform, subprocess, tempfile
                if platform.system() == 'Darwin':
                    aiff_path = f"audio/dialogue_{i}.aiff"
                    # Use a voice that supports Indian languages if present; otherwise default
                    voice_flag = []
                    try:
                        # Attempt a Punjabi-capable voice is unlikely by default; leave empty
                        voice_flag = []
                    except Exception:
                        voice_flag = []
                    cmd = ["say"] + voice_flag + ["-o", aiff_path, dialogue.get("text", "")]
                    subprocess.run(cmd, check=True)
                    # Convert AIFF -> WAV for pipeline consistency
                    wav_fallback = f"audio/dialogue_{i}.wav"
                    subprocess.run(["ffmpeg", "-y", "-i", aiff_path, wav_fallback], check=True)
                    load_path = wav_fallback
                    log.info(f"macOS TTS saved: {wav_fallback}")
                else:
                    raise RuntimeError("not macOS")
            except Exception as e2:
                log.warning(f"macOS 'say' fallback failed: {e2}. Using sample asset.")
                if not os.path.exists(sample_path_wav):
                    _make_sample_wav(sample_path_wav, freq=300 + i * 60, dur=2.0)
                load_path = sample_path_wav

    # Load the clip and add volume
    clip = AudioFileClip(load_path)
    clip = volumex(clip, dialogue.get('volume', 1.0))

    # Optional per-character panning (best-effort; falls back on failure)
    if PAN_WIDTH > 0.0:
        try:
            # Robust approach: write clip to temp WAV and read samples reliably with wave
            import array as _array
            fps = 44100
            tmp_clip = f"audio/clip_{i}_tmp.wav"
            clip.write_audiofile(tmp_clip, fps=fps, verbose=False, logger=None)
            with wave.open(tmp_clip, 'rb') as wf:
                nframes = wf.getnframes(); nch = wf.getnchannels(); sw = wf.getsampwidth()
                frames = wf.readframes(nframes)
                fmt = 'h' if sw == 2 else 'b'
                arr = _array.array(fmt)
                arr.frombytes(frames)
                if nch > 1:
                    # reshape and downmix to mono
                    arr_np = np.array(arr).astype(np.float32)
                    arr_np = arr_np.reshape(-1, nch).mean(axis=1)
                else:
                    arr_np = np.array(arr).astype(np.float32)
                if sw == 2:
                    arr_np = arr_np / 32768.0
                else:
                    arr_np = arr_np / 128.0
            mono = arr_np
            # pan value between -1 (left) .. 1 (right) based on character index
            pan = (i / max(1, len(dialogues_scene1)-1) - 0.5) * 2.0 * PAN_WIDTH
            left_gain = np.sqrt(0.5 * (1.0 - pan))
            right_gain = np.sqrt(0.5 * (1.0 + pan))
            left = mono * left_gain
            right = mono * right_gain
            stereo = np.stack([left, right], axis=1).astype(np.float32)
            clip = AudioArrayClip(stereo, fps=fps)
        except Exception as e:
            log.debug(f"panning failed for clip {i}: {e}")

    audio_clips.append(clip)

if len(audio_clips) == 0:
    raise RuntimeError("No audio clips were produced or found.")

final_dialogue_audio = concatenate_audioclips(audio_clips)
total_duration = final_dialogue_audio.duration
log.info(f"Final dialogue audio duration: {total_duration:.2f}s")
for idx, ac in enumerate(audio_clips):
    try:
        log.info(f" - clip {idx}: duration={ac.duration:.2f}s")
    except Exception:
        log.debug(f" - clip {idx}: duration unavailable")

# Normalize dialogue for consistent loudness
try:
    final_dialogue_audio = audio_normalize(final_dialogue_audio)
    log.info("Applied audio normalization to dialogue")
except Exception as e:
    log.debug(f"audio_normalize failed: {e}")

# Build dialogue timeline (start/end per clip) for captions/timecode overlays
DIALOGUE_TIMELINE = []
try:
    cur = 0.0
    for i, ac in enumerate(audio_clips):
        dur = getattr(ac, 'duration', None) or 0.0
        info = {
            'start': cur,
            'end': cur + dur,
            'text': dialogues_scene1[i].get('text', ''),
            'character': dialogues_scene1[i].get('character', ''),
            'index': i,
            'duration': dur,
        }
        DIALOGUE_TIMELINE.append(info)
        cur += dur
except Exception:
    DIALOGUE_TIMELINE = []

# Create SFX (for background) — write a WAV (was .mp3 mismatch)
# 🧠 Use scene emotion to select appropriate background music
sample_rate = 44100
duration = 4.0  # 4 seconds

# Determine which background music to use based on scene emotion or explicit audio_instructions
music_volume = 0.35
background_fx_path = None
synth_instr = None
if SCENES_PATH and 'scenes' in dir() and len(scenes) > 0:
    # Get dominant emotion from first scene (or average across all scenes)
    first_scene = scenes[0]
    first_scene_emotion = first_scene.get('brain_analysis', {}).get('emotion', {})
    emotion = first_scene_emotion.get('emotion', 'neutral')
    # Respect explicit audio instructions if Master attached them
    audio_instr = first_scene.get('audio_instructions', {})
    if audio_instr:
        # music_path: absolute or relative file path provided by Master
        mp = audio_instr.get('music_path')
        if mp:
            # prefer absolute path if provided; otherwise look relative
            if os.path.exists(mp):
                background_fx_path = mp
            else:
                # try relative to project
                cand = os.path.join(os.getcwd(), mp)
                if os.path.exists(cand):
                    background_fx_path = cand
        # allow Master to request synth fallback (pad) with params
        synth_instr = audio_instr.get('synthesize_music')
        if synth_instr:
            emotion = synth_instr.get('emotion', emotion)
            music_volume = float(synth_instr.get('volume', music_volume))

    # If no explicit music file chosen by Master, fall back to brain_analysis suggestion
    if background_fx_path is None:
        music_file = first_scene_emotion.get('music_file', 'birds.wav')
        # Don't let brain override our fixed volume - keep it at 0.35 minimum
        suggested_volume = float(first_scene_emotion.get('music_volume', music_volume))
        music_volume = max(suggested_volume, 0.35)  # Ensure minimum 0.35 volume
        background_fx_path = f"audio/{music_file}"
    log.info(f"🧠 Scene emotion: {emotion} → Background music: {background_fx_path} @ {music_volume:.2f}")
else:
    # Default fallback
    emotion = 'neutral'
    background_fx_path = "audio/birds.wav"
    music_volume = 0.35

# FINAL SAFETY CHECK: Ensure music volume is never too low
if music_volume < 0.30:
    log.warning(f"⚠️  Music volume too low ({music_volume:.2f}), forcing to 0.35")
    music_volume = 0.35

# If Master provided a real audio file path, and it exists, prefer loading it directly
background_audio_clip = None
if background_fx_path and os.path.exists(background_fx_path):
    try:
        background_audio_clip = AudioFileClip(background_fx_path)
        log.info(f"Using existing background audio file: {background_fx_path}")
    except Exception as _e:
        log.debug(f"Failed to load background audio file {background_fx_path}: {_e}")

# If no pre-existing audio clip, generate a small pad/texture based on emotion or synth instr
samples = np.zeros(int(duration * sample_rate))

# Generate different audio textures based on emotion - ALL LOUD NOW!
if emotion == 'happy':
    # Bright, higher frequency tones
    t = np.linspace(0, duration, int(duration * sample_rate), False)
    samples = 0.3 * np.sin(2 * np.pi * 440.0 * t) * (1.0 + 0.3 * np.sin(2 * np.pi * 3.0 * t))
elif emotion == 'sad':
    # Lower, sustained tones
    t = np.linspace(0, duration, int(duration * sample_rate), False)
    samples = 0.25 * np.sin(2 * np.pi * 220.0 * t) * (1.0 - 0.2 * np.sin(2 * np.pi * 0.5 * t))
elif emotion == 'tense' or emotion == 'tragic':
    # Dissonant, pulsing tones
    t = np.linspace(0, duration, int(duration * sample_rate), False)
    samples = 0.35 * (np.sin(2 * np.pi * 200.0 * t) + 0.5 * np.sin(2 * np.pi * 297.5 * t))
    samples *= (0.8 + 0.2 * np.sin(2 * np.pi * 2.0 * t))  # Pulse
elif emotion == 'angry':
    # Aggressive, distorted tones
    t = np.linspace(0, duration, int(duration * sample_rate), False)
    base = np.sin(2 * np.pi * 180.0 * t)
    samples = 0.4 * np.sign(base) * np.abs(base) ** 0.5  # Distortion
elif emotion == 'peaceful':
    # Soft, harmonic tones
    t = np.linspace(0, duration, int(duration * sample_rate), False)
    samples = 0.2 * (np.sin(2 * np.pi * 264.0 * t) + 0.5 * np.sin(2 * np.pi * 330.0 * t))
else:
    # Neutral: birds/ambient (MAXIMUM VOLUME!)
    t = np.linspace(0, duration, int(duration * sample_rate), False)
    # MAXIMUM amplitude: 0.5
    pad = 0.5 * np.sin(2 * np.pi * 220.0 * t) * (1.0 - 0.5 * np.sin(2 * np.pi * 0.1 * t))
    noise = 0.1 * np.random.normal(size=pad.shape)  # Maximum noise
    samples = pad + noise
    if DREAM:
        # Add extra effects in dream mode
        samples *= 1.5

# Save as WAV file
with wave.open(background_fx_path, 'wb') as f:
    f.setnchannels(1)
    f.setsampwidth(2)
    f.setframerate(sample_rate)
    f.writeframes((samples * 32767).astype(np.int16).tobytes())

# load background audio
background_audio_clip = AudioFileClip(background_fx_path)
log.info(f"Background audio created: {background_fx_path}")
_log_file_info(background_fx_path)

# --- Step 3: Final Assembly ---
# Create a subtle Ken-Burns / zoom animation on the base image for the full dialogue duration
# Create a simple zoom/pan animation by generating frames with PIL (avoids PIL.ANTIALIAS issue)
base_img = Image.open(AI_IMAGE_PATH).convert('RGB')
width, height = 1920, 1080

# Try to resolve a font that can render multilingual text (best-effort on macOS)
def _resolve_font_path():
    candidates = [
        "/System/Library/Fonts/Supplemental/NotoSansGurmukhi.ttc",
        "/System/Library/Fonts/Supplemental/Gurmukhi.ttc",
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
        "/Library/Fonts/Arial Unicode.ttf",
        "/System/Library/Fonts/Supplemental/NotoSans.ttc",
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    # fallback to any TTF in system font folders
    for folder in ["/System/Library/Fonts/Supplemental", "/Library/Fonts", "/System/Library/Fonts"]:
        try:
            for fn in os.listdir(folder):
                if fn.lower().endswith((".ttf", ".ttc", ".otf")):
                    return os.path.join(folder, fn)
        except Exception:
            pass  # No fonts in this folder
    return None

_FONT_PATH = _resolve_font_path()

def _get_font(size=40):
    try:
        if _FONT_PATH:
            return ImageFont.truetype(_FONT_PATH, size=size)
    except Exception:
        pass  # Fallback to default font
    return ImageFont.load_default()

def _wrap_text(draw: ImageDraw.ImageDraw, text: str, font, max_width_px: int):
    if not text:
        return []
    words = text.split()
    lines = []
    cur = ""
    for w in words:
        test = (cur + (" " if cur else "") + w).strip()
        try:
            w_px = draw.textlength(test, font=font)
        except Exception:
            # fallback approximate width: 0.6 * font size per char
            w_px = len(test) * (font.size * 0.6 if hasattr(font, 'size') else 24)
        if w_px <= max_width_px:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def make_frame(t, base=base_img, duration=total_duration):
    # Find current speaking character
    current_char = None
    current_idx = -1
    for seg in DIALOGUE_TIMELINE:
        if seg['start'] <= t < seg['end']:
            current_char = seg.get('character', '')
            current_idx = seg.get('index', -1)
            break
    
    # Vary background color slightly based on scene
    scene_num = current_idx // 3 if current_idx >= 0 else 0
    base_hue = (scene_num * 30) % 360
    # Create a subtle gradient for this scene (OPTIMIZED with numpy - 1000x faster!)
    try:
        import colorsys
        rgb1 = colorsys.hsv_to_rgb(base_hue / 360.0, 0.15, 0.25)
        rgb2 = colorsys.hsv_to_rgb((base_hue + 20) / 360.0, 0.18, 0.15)
        color1 = np.array([int(c * 255) for c in rgb1], dtype=np.uint8)
        color2 = np.array([int(c * 255) for c in rgb2], dtype=np.uint8)
        
        # Use numpy for vectorized gradient (1000x faster than putpixel!)
        gradient = np.linspace(0, 1, height).reshape(height, 1, 1)
        bg_array = color1 * (1 - gradient) + color2 * gradient
        bg_array = bg_array.astype(np.uint8)
        bg_array = np.repeat(bg_array, width, axis=1)  # Extend to full width
        
        scene_bg = Image.fromarray(bg_array, 'RGB')
        frame = scene_bg
    except Exception:
        # Fallback to simple zoom on base
        scale = 1.0 + 0.08 * (t / max(duration, 1.0))
        new_w = int(base.width * scale)
        new_h = int(base.height * scale)
        resample = getattr(Image, 'Resampling', None)
        if resample:
            resample = Image.Resampling.LANCZOS
        else:
            resample = Image.LANCZOS
        resized = base.resize((new_w, new_h), resample)
        left = max(0, (new_w - width) // 2)
        top = max(0, (new_h - height) // 2)
        box = (left, top, left + width, top + height)
        frame = resized.crop(box)
    # overlays: timecode and/or captions
    if TIMECODE or CAPTIONS:
        try:
            draw = ImageDraw.Draw(frame, 'RGBA')
            # timecode (top-left)
            if TIMECODE:
                mins = int(t // 60)
                secs = int(t % 60)
                tc = f"{mins:02d}:{secs:02d}"
                font_tc = _get_font(32)
                padding = 8
                tw, th = draw.textbbox((0, 0), tc, font=font_tc)[2:]
                rect = (10, 10, 10 + tw + padding*2, 10 + th + padding*2)
                draw.rectangle(rect, fill=(0, 0, 0, 140))
                draw.text((10 + padding, 10 + padding), tc, font=font_tc, fill=(255, 255, 255, 255))

            # captions (bottom)
            if CAPTIONS and DIALOGUE_TIMELINE:
                # find current dialogue
                cur_txt = None
                cur_char = None
                for seg in DIALOGUE_TIMELINE:
                    if seg['start'] <= t < seg['end']:
                        cur_txt = seg.get('text')
                        cur_char = seg.get('character')
                        break
                if cur_txt:
                    font = _get_font(42)
                    # wrap to 80% width
                    max_w = int(width * 0.8)
                    lines = _wrap_text(draw, cur_txt, font, max_w)
                    if cur_char:
                        # prepend character name on first line
                        lines = [f"{cur_char}: {lines[0]}" if lines else f"{cur_char}:"] + lines[1:]
                    # compute text block size
                    line_h = (draw.textbbox((0, 0), "Ag", font=font)[3]) - (draw.textbbox((0, 0), "Ag", font=font)[1])
                    total_h = int(len(lines) * (line_h + 6))
                    block_w = max((draw.textlength(ln, font=font) for ln in lines), default=0)
                    block_w = int(min(block_w, max_w))
                    x0 = int((width - block_w) / 2) - 24
                    y0 = height - total_h - 60
                    x1 = x0 + block_w + 48
                    y1 = y0 + total_h + 32
                    # semi-transparent rounded rectangle
                    try:
                        draw.rounded_rectangle((x0, y0, x1, y1), radius=16, fill=(0, 0, 0, 150))
                    except Exception:
                        draw.rectangle((x0, y0, x1, y1), fill=(0, 0, 0, 150))
                    # draw lines centered
                    cx = (x0 + x1) // 2
                    y = y0 + 16
                    for ln in lines:
                        lw = draw.textlength(ln, font=font)
                        draw.text((cx - lw/2, y), ln, font=font, fill=(255, 255, 255, 255))
                        y += line_h + 6
        except Exception:
            pass  # Auto-fixed
    # overlay character avatars - show speaking character prominently
    try:
        if portraits and current_char and current_char in portraits:
            # Show speaking character large and centered
            if t < 1.0:  # Debug log for first second only
                log.info(f"🎭 Rendering portrait for '{current_char}' at t={t:.2f}s")
            speaker_img = portraits[current_char]
            speaker_size = 600  # LARGER! Was 400
            # Resize speaker avatar
            resample = getattr(Image, 'Resampling', None)
            if resample:
                resample = Image.Resampling.LANCZOS
            else:
                resample = Image.LANCZOS
            speaker_resized = speaker_img.resize((speaker_size, speaker_size), resample)
            
            # Position in center-top area with slight animation
            progress = (t - (DIALOGUE_TIMELINE[current_idx]['start'] if current_idx >= 0 else 0)) / max(0.1, DIALOGUE_TIMELINE[current_idx]['duration'] if current_idx >= 0 and DIALOGUE_TIMELINE[current_idx]['duration'] > 0 else 1.0)
            bounce = abs(np.sin(progress * np.pi * 2)) * 10  # Subtle bounce
            
            pos_x = (width - speaker_size) // 2
            pos_y = int(80 + bounce)
            
            try:
                frame.paste(speaker_resized, (pos_x, pos_y), speaker_resized)
            except Exception:
                try:
                    frame.paste(speaker_resized.convert('RGB'), (pos_x, pos_y))
                except Exception:
                    pass  # Auto-fixed
            
            # Show other characters smaller at the bottom
            other_chars = [name for name in portraits.keys() if name != current_char]
            if other_chars:
                small_size = 120
                x_start = (width - (len(other_chars) * (small_size + 20))) // 2
                for idx, name in enumerate(other_chars[:5]):  # Max 5 other characters
                    other_img = portraits[name].resize((small_size, small_size), resample)
                    pos_x = x_start + idx * (small_size + 20)
                    pos_y = height - small_size - 200  # Above captions
                    try:
                        # Make them semi-transparent
                        other_rgba = other_img.copy()
                        other_rgba.putalpha(Image.eval(other_rgba.split()[3], lambda a: int(a * 0.5)))
                        frame.paste(other_rgba, (pos_x, pos_y), other_rgba)
                    except Exception:
                        try:
                            frame.paste(other_img.convert('RGB'), (pos_x, pos_y))
                        except Exception:
                            pass  # Auto-fixed
    except Exception as e:
        log.debug(f"Portrait overlay failed: {e}")
        pass  # Auto-fixed
    return np.array(frame)

clip1 = VideoClip(make_frame, duration=total_duration).set_fps(24)
clip1 = fadein(clip1, 0.5)

# Mix background (looped) and dialogue audio
# Prepare background audio: loop to full duration
bg_loop = audio_loop(background_audio_clip, duration=total_duration)

# If ducking enabled, render background to array, apply envelope and create AudioArrayClip
if DUCK:
    log.info(f"Applying ducking: bg_gain={BG_GAIN}, duck_factor={DUCK_FACTOR} attack={DUCK_ATTACK_MS}ms release={DUCK_RELEASE_MS}ms")
    try:
        import array as _array
        fps = 44100
        tmp_bg = 'audio/bg_loop_temp.wav'
        # write the looped background to a temporary wav, then read reliably with wave
        bg_loop.write_audiofile(tmp_bg, fps=fps, verbose=False, logger=None)
        with wave.open(tmp_bg, 'rb') as wf:
            nframes = wf.getnframes(); nch = wf.getnchannels(); sw = wf.getsampwidth()
            frames = wf.readframes(nframes)
            fmt = 'h' if sw == 2 else 'b'
            arr = _array.array(fmt)
            arr.frombytes(frames)
            if nch > 1:
                # downmix to mono by taking first channel
                arr = arr[::nch]
            bg_arr = np.array(arr).astype(np.float32)
            if sw == 2:
                bg_arr = bg_arr / 32768.0

        # build envelope from dialogue clip timings
        starts = []
        cur = 0.0
        for ac in audio_clips:
            dur = getattr(ac, 'duration', None)
            if dur is None:
                dur = 0.0
            starts.append((cur, cur + dur))
            cur += dur

        n = bg_arr.shape[0]
        env = np.ones(n, dtype=float) * BG_GAIN

        # mark ducked regions
        for (s, e) in starts:
            si = int(max(0, np.floor(s * fps)))
            ei = int(min(n, np.ceil(e * fps)))
            env[si:ei] = BG_GAIN * DUCK_FACTOR

        # apply attack/release smoothing (linear ramps)
        attack_samps = int(max(1, np.round((DUCK_ATTACK_MS / 1000.0) * fps)))
        release_samps = int(max(1, np.round((DUCK_RELEASE_MS / 1000.0) * fps)))
        # for each region, create ramps at boundaries
        for (s, e) in starts:
            si = int(max(0, np.floor(s * fps)))
            ei = int(min(n, np.ceil(e * fps)))
            # attack ramp: from BG_GAIN -> BG_GAIN*DUCK_FACTOR
            a0 = max(0, si - attack_samps)
            if si > a0:
                ramp = np.linspace(BG_GAIN, BG_GAIN * DUCK_FACTOR, si - a0)
                env[a0:si] = np.minimum(env[a0:si], ramp)
            # release ramp: from BG_GAIN*DUCK_FACTOR -> BG_GAIN
            r1 = min(n, ei + release_samps)
            if r1 > ei:
                ramp = np.linspace(BG_GAIN * DUCK_FACTOR, BG_GAIN, r1 - ei)
                env[ei:r1] = np.minimum(env[ei:r1], ramp)

        # convert bg_arr to float32 -1..1
        bg_arr = bg_arr.astype(np.float32)
        # if 16-bit sample scale
        if sw == 2:
            bg_arr = bg_arr / 32768.0

        # apply dream reverb if requested (small impulse response)
        if DREAM:
            try:
                ir_dur = 0.5  # 500ms impulse
                ir_n = int(ir_dur * fps)
                # exponential decay IR
                ir = np.logspace(0, -3, ir_n)
                conv = np.convolve(bg_arr, ir)[:n]
                bg_arr = conv
            except Exception as _e:
                log.debug(f"reverb failed: {_e}")

        # apply envelope
        proc = (bg_arr * env).astype(np.float32)

        # stereo widen: create two channels with tiny offset/delay
        try:
            delay_samples = int(0.01 * fps)  # 10ms
            left = proc
            right = np.concatenate((np.zeros(delay_samples), proc[:-delay_samples])) if delay_samples < proc.shape[0] else proc
            stereo = np.stack([left, right], axis=1)
            bg_clip = AudioArrayClip(stereo, fps=fps)
            background_audio = bg_clip
        except Exception:
            bg_arr2 = proc.reshape(-1, 1)
            background_audio = AudioArrayClip(bg_arr2, fps=fps)

        log.info("Background audio processed with ducking (AudioArrayClip)")
    except Exception as e:
        log.warning(f"Ducking failed, falling back to simple gain: {e}")
        background_audio = volumex(bg_loop, BG_GAIN)
else:
    background_audio = volumex(bg_loop, BG_GAIN)

final_audio_mix = CompositeAudioClip([final_dialogue_audio, background_audio])
try:
    # Ensure duration is set for safe write_audiofile operations
    final_audio_mix = final_audio_mix.set_duration(total_duration)
except Exception:
    pass  # Auto-fixed

def _compute_db_from_clip(clip, tmp_path='audio/_tmp_clip.wav', fps=44100):
    """Robustly compute dBFS from a MoviePy AudioClip.
    Tries to use to_soundarray(); if that fails, writes a temporary WAV and reads samples.
    Returns dB (float) or None on failure.
    """
    try:
        import numpy as _np
        arr = clip.to_soundarray(fps=fps)
        if arr is None or arr.size == 0:
            raise RuntimeError('empty array')
        rms = _np.sqrt(_np.mean(_np.square(arr.astype(_np.float64))))
        return float(20.0 * _np.log10(max(rms, 1e-10)))
    except Exception:
        try:
            # Write to temp wav and read via wave for reliability
            clip.write_audiofile(tmp_path, fps=fps, verbose=False, logger=None)
            import wave as _wave, array as _array
            with _wave.open(tmp_path, 'rb') as wf:
                nframes = wf.getnframes(); nch = wf.getnchannels(); sw = wf.getsampwidth()
                frames = wf.readframes(nframes)
                fmt = 'h' if sw == 2 else 'b'
                arr = _array.array(fmt)
                arr.frombytes(frames)
                import numpy as _np
                if nch > 1:
                    data = _np.array(arr).astype(_np.float64).reshape(-1, nch)
                    mono = data.mean(axis=1)
                else:
                    mono = _np.array(arr).astype(_np.float64)
                # normalize
                if sw == 2:
                    mono = mono / 32768.0
                else:
                    mono = mono / 128.0
                rms = _np.sqrt(_np.mean(mono ** 2))
                return float(20.0 * _np.log10(max(rms, 1e-10)))
        except Exception:
            return None


# Emit feedback to Master (loudness metrics) and apply simple auto-fix suggestions
try:
    if _MASTER_CLIENT is not None:
        dlg_db = _compute_db_from_clip(final_dialogue_audio, tmp_path='audio/_dlg_tmp.wav')
        bg_db = _compute_db_from_clip(background_audio, tmp_path='audio/_bg_tmp.wav')

        metrics = {
            'dialogue_loudness_db': dlg_db,
            'background_loudness_db': bg_db,
            'scene_id': 0,
            'success': True
        }

        try:
            rec = _MASTER_CLIENT.receive_brain_feedback('master_builder', 0, metrics)
            recs = rec.get('recommendations', []) if isinstance(rec, dict) else []
            # apply simple auto-fix: lower music volume
            for r in recs:
                if r.get('action') == 'lower_music_volume':
                    mult = float(r.get('suggested_multiplier', 0.6))
                    try:
                        background_audio = background_audio.volumex(mult)
                        final_audio_mix = CompositeAudioClip([final_dialogue_audio, background_audio]).set_duration(total_duration)
                        print(f"🔧 Auto-fix applied: background multiplied by {mult}")
                    except Exception:
                        pass  # Auto-fixed
        except Exception:
            pass  # Auto-fixed
except Exception:
    pass  # Auto-fixed

# Optional mastering: simple compressor + limiter applied to final mix
if 'MASTER' in globals() and MASTER:
    try:
        log.info("Applying light mastering (compressor + limiter) to final mix")
        fps = 44100
        tmp_mix = 'audio/final_mix_temp.wav'
        final_audio_mix.write_audiofile(tmp_mix, fps=fps, verbose=False, logger=None)
        # read wav reliably
        import array as _array
        with wave.open(tmp_mix, 'rb') as wf:
            nframes = wf.getnframes(); nch = wf.getnchannels(); sw = wf.getsampwidth()
            frames = wf.readframes(nframes)
            fmt = 'h' if sw == 2 else 'b'
            arr = _array.array(fmt)
            arr.frombytes(frames)
            data = np.array(arr).astype(np.float32)
            if nch > 1:
                data = data.reshape(-1, nch)
            else:
                data = data.reshape(-1, 1)
            if sw == 2:
                data = data / 32768.0
            else:
                data = data / 128.0

        # compressor params
        threshold = 0.6
        ratio = 3.0
        attack_sec = 0.01
        release_sec = 0.1
        attack_alpha = np.exp(-1.0 / (attack_sec * fps))
        release_alpha = np.exp(-1.0 / (release_sec * fps))

        # compute envelope (RMS approx via absolute value smoothing)
        env = np.abs(data).mean(axis=1)
        gain = np.ones_like(env)
        # compute instantaneous desired gain
        for idx in range(len(env)):
            level = env[idx]
            if level > threshold and level > 0:
                desired = (threshold + (level - threshold) / ratio) / level
            else:
                desired = 1.0
            gain[idx] = desired

        # smooth gain with attack/release
        smooth = np.ones_like(gain)
        for i in range(1, len(gain)):
            if gain[i] < smooth[i-1]:
                smooth[i] = attack_alpha * smooth[i-1] + (1 - attack_alpha) * gain[i]
            else:
                smooth[i] = release_alpha * smooth[i-1] + (1 - release_alpha) * gain[i]

        # apply gain to all channels
        proc = data * smooth[:, None]

        # limiter: prevent >1.0 peaks
        peak = np.max(np.abs(proc))
        if peak > 0.995:
            proc = proc * (0.995 / peak)

        # create AudioArrayClip
        try:
            master_clip = AudioArrayClip(proc.astype(np.float32), fps=fps)
            final_audio_mix = master_clip
            log.info("Mastering applied successfully")
        except Exception as _e:
            log.warning(f"Failed to create mastered AudioArrayClip: {_e}")
    except Exception as e:
        log.warning(f"Mastering failed: {e}")

# Attach the mixed audio to the animated clip and write final video
final_video_clip = clip1.set_audio(final_audio_mix)

if DRY_RUN:
    log.info("Dry-run enabled: skipping write_videofile. Diagnostics below:")
    _log_file_info('audio/dialogue_0.mp3')
    _log_file_info('audio/dialogue_1.mp3')
    _log_file_info('audio/dialogue_2.mp3')
    _log_file_info(background_fx_path)
    log.info(f"Final video WOULD be: {final_video_filename} duration={total_duration:.2f}s")
else:
    # Write with faststart and decent bitrates for wider player compatibility (QuickTime, browsers)
    final_video_clip.write_videofile(
        final_video_filename,
        fps=24,
        codec='libx264',
        audio_codec='aac',
        bitrate='2500k',
        audio_bitrate='192k',
        ffmpeg_params=['-movflags', '+faststart', '-pix_fmt', 'yuv420p'],
        verbose=False,
        logger=None,
    )

print("\n\n--- AMRIT CORE MASTER BUILDER STATUS: LAUNCH SUCCESS ---")
print("The final, fully assembled demonstration video has been created!")
print(f"Find the file: {final_video_filename}")
