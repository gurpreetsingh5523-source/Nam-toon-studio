# AmritCore - MASTER BUILDER (Final Assembly and Export - LIST INITIALIZATION FIX)

# Install necessary libraries
#!pip install moviepy==1.0.3 gTTS requests pillow numpy

from moviepy.editor import *  # Using the simpler import style
from moviepy.audio.fx.volumex import volumex
from moviepy.audio.fx.audio_loop import audio_loop
from moviepy.audio.fx.audio_normalize import audio_normalize
from moviepy.audio.AudioClip import AudioArrayClip
from moviepy.video.fx.fadeout import fadeout
from moviepy.video.fx.fadein import fadein
from gtts import gTTS
import argparse
import logging
from pathlib import Path
from PIL import Image
import wave
import numpy as np
import os

# --- Step 1: Setup and Data ---
final_video_filename = "AmritCore_FINAL_STUDIO_LAUNCH.mp4"

# --- CLI / logging ---
parser = argparse.ArgumentParser(description="AmritCore master builder (assemble scenes, TTS and export)")
parser.add_argument("--dry-run", action="store_true", help="Run checks and print diagnostics but don't write final large files")
parser.add_argument("--verbose", "-v", action="store_true", help="Verbose logging")
parser.add_argument("--duck", action="store_true", help="Enable simple background ducking during speech")
parser.add_argument("--bg-gain", type=float, default=0.15, help="Global background gain multiplier (default 0.15)")
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
parser.add_argument("--sfx-preset", type=str, default="birds", choices=["birds", "peacock", "tinds", "flute"], help="Procedural background SFX preset")
args = parser.parse_args()

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
SFX_PRESET = getattr(args, 'sfx_preset', 'birds')

# Create necessary folders (ensures stability)
if not os.path.exists("audio"): os.makedirs("audio")
if not os.path.exists("images"): os.makedirs("images")
if not os.path.exists("assets/animation"): os.makedirs("assets/animation")

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
# If user provided a background image, prefer it
if BACKGROUND_PATH and os.path.exists(BACKGROUND_PATH):
    AI_IMAGE_PATH = BACKGROUND_PATH
    log.info(f"Using user background: {AI_IMAGE_PATH}")
else:
    Image.new('RGB', (1920, 1080), color=SCENE_COLOR).save(AI_IMAGE_PATH)


# --- Step 2: Audio Generation and Combining (with offline/sample mode, panning and dream effects)
# Create empty list to store audio clips
audio_clips = []

voice_cloning = True
subtitles = True
color_grading = "Standard"
keyframes = {}

# If scenes JSON provided, load and convert to dialogues_scene1 format
if SCENES_PATH:
    try:
        import json
        sp = Path(SCENES_PATH)
        if sp.exists():
            data = json.loads(sp.read_text())
            voice_cloning = data.get('voice_cloning', True)
            subtitles = data.get('subtitles', True)
            color_grading = data.get('color_grading', 'Standard')
            keyframes = data.get('keyframes', {})
            first = data.get('scenes', [])[0]
            if first:
                dialogues_scene1 = first.get('dialogues', dialogues_scene1)
                log.info(f"Loaded scenes from {SCENES_PATH}, using scene {first.get('scene_id','0')}")
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

# Load character portraits if provided
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

# Helper: record audio from mic into wav (best-effort)
def _record_clip(path, record_seconds=4, sr=44100):
    try:
        import sounddevice as sd
        log.info(f"Recording {record_seconds}s to {path} (press Ctrl-C to abort)")
        rec = sd.rec(int(record_seconds * sr), samplerate=sr, channels=1, dtype='int16')
        sd.wait()
        # write with wave
        with wave.open(path, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sr)
            wf.writeframes(rec.tobytes())
        return True
    except Exception as e:
        log.warning(f"Recording failed (sounddevice may be missing): {e}")
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
for i, dialogue in enumerate(dialogues_scene1):
    out_path = f"audio/dialogue_{i}.mp3"
    sample_path_wav = f"audio/sample_dialogue_{i}.wav"

    # Check for custom recorded audio override file
    override_path = None
    if dialogue.get("audio_file") and os.path.exists(dialogue["audio_file"]):
        override_path = dialogue["audio_file"]
        log.info(f"Using custom audio override for {dialogue.get('character')}[{i}]: {override_path}")

    if not override_path and AUDIO_DIR and os.path.exists(AUDIO_DIR):
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
            log.info(f"--no-tts: creating sample dialogue asset: {sample_path_wav}")
            _make_sample_wav(sample_path_wav, freq=300 + i * 60, dur=2.0)
        load_path = sample_path_wav
        log.info(f"Using sample dialogue asset for {i}: {load_path}")
    else:
        try:
            tts = gTTS(dialogue["text"], lang='pa')
            tts.save(out_path)
            log.info(f"TTS saved: {out_path}")
            load_path = out_path
        except Exception as e:
            log.warning(f"gTTS failed: {e}. Falling back to sample asset.")
            if not os.path.exists(sample_path_wav):
                _make_sample_wav(sample_path_wav, freq=300 + i * 60, dur=2.0)
            load_path = sample_path_wav

    # Load the clip and add volume
    clip = AudioFileClip(load_path)
    
    track_name = dialogue.get('character')
    default_vol = dialogue.get('volume', 1.0)
    
    def get_interpolated_volume(track, absolute_time, base_vol):
        if 'keyframes' not in globals() or not keyframes or track not in keyframes:
            return base_vol
        kfs = keyframes[track]
        if not kfs:
            return base_vol
        sorted_kfs = sorted(kfs, key=lambda x: x['time'])
        if absolute_time <= sorted_kfs[0]['time']:
            return sorted_kfs[0]['volume']
        if absolute_time >= sorted_kfs[-1]['time']:
            return sorted_kfs[-1]['volume']
        for idx in range(len(sorted_kfs) - 1):
            k1 = sorted_kfs[idx]
            k2 = sorted_kfs[idx+1]
            if k1['time'] <= absolute_time <= k2['time']:
                ratio = (absolute_time - k1['time']) / (k2['time'] - k1['time'])
                return k1['volume'] + ratio * (k2['volume'] - k1['volume'])
        return base_vol

    def vol_filter(gf, t):
        absolute_time = dialogue.get('computed_start', 0.0) + t
        vol = get_interpolated_volume(track_name, absolute_time, default_vol)
        return vol * gf(t)

    clip = clip.fl(vol_filter)

    # Optional per-character panning (best-effort; falls back on failure)
    custom_pan = dialogue.get('pan', None)
    if custom_pan is not None or PAN_WIDTH > 0.0:
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
            # resolve pan value
            if custom_pan is not None:
                pan = float(custom_pan)
            else:
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

# Determine if we mix as a timeline composite or standard sequential concatenation
has_timeline = any(dialogue.get('start_time') is not None for dialogue in dialogues_scene1)

if has_timeline:
    composite_clips = []
    current_time = 0.0
    for idx, dialogue in enumerate(dialogues_scene1):
        c_clip = audio_clips[idx]
        start_time = dialogue.get('start_time')
        if start_time is not None:
            start_time = float(start_time)
            c_clip = c_clip.set_start(start_time)
            current_time = max(current_time, start_time + c_clip.duration)
        else:
            c_clip = c_clip.set_start(current_time)
            current_time += c_clip.duration
        composite_clips.append(c_clip)
    final_dialogue_audio = CompositeAudioClip(composite_clips)
    total_duration = current_time
    log.info(f"Timeline mode active: mixed {len(composite_clips)} clips dynamically")
else:
    final_dialogue_audio = concatenate_audioclips(audio_clips)
    total_duration = final_dialogue_audio.duration
    log.info("Sequential concatenation mode active")

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

# Create SFX (for background) — write a WAV
background_fx_path = f"audio/{SFX_PRESET}.wav"
sample_rate = 44100
duration = 8.0  # 8 seconds loop
t = np.linspace(0, duration, int(duration * sample_rate), False)
samples = np.zeros_like(t)

if SFX_PRESET == 'birds':
    # High frequency chirps + noise
    noise = 0.005 * np.random.normal(size=t.shape)
    chirps = np.zeros_like(t)
    for start_t in [0.5, 1.2, 2.0, 3.5, 4.2, 5.0, 6.5, 7.2]:
        idx_start = int(start_t * sample_rate)
        idx_end = idx_start + int(0.2 * sample_rate)
        if idx_end < len(t):
            t_chirp = t[idx_start:idx_end] - start_t
            sweep = np.sin(2 * np.pi * (2500 + 7500 * t_chirp) * t_chirp)
            env = np.sin(np.pi * (t_chirp / 0.2))
            chirps[idx_start:idx_end] += 0.05 * sweep * env
    samples = chirps + noise

elif SFX_PRESET == 'peacock':
    peacock = np.zeros_like(t)
    for start_t in [1.0, 3.5, 6.0]:
        idx_start = int(start_t * sample_rate)
        idx_end = idx_start + int(0.8 * sample_rate)
        if idx_end < len(t):
            t_call = t[idx_start:idx_end] - start_t
            sweep = np.sin(2 * np.pi * (800 + 400 * np.sin(np.pi * t_call / 0.8)) * t_call)
            env = np.exp(-4 * t_call) * (1 - np.exp(-40 * t_call))
            peacock[idx_start:idx_end] += 0.1 * sweep * env
    samples = peacock + 0.003 * np.random.normal(size=t.shape)

elif SFX_PRESET == 'tinds':
    creak = np.sin(2 * np.pi * 50 * t) * (0.04 * (1.0 + np.sin(2 * np.pi * 1.5 * t))) * np.random.normal(size=t.shape)
    splash = np.zeros_like(t)
    for start_t in [0.0, 2.0, 4.0, 6.0]:
        idx_start = int(start_t * sample_rate)
        idx_end = idx_start + int(0.6 * sample_rate)
        if idx_end < len(t):
            t_splash = t[idx_start:idx_end] - start_t
            splash_noise = 0.015 * np.random.normal(size=t_splash.shape)
            env = np.exp(-3 * t_splash)
            splash[idx_start:idx_end] += splash_noise * env
    samples = creak + splash

elif SFX_PRESET == 'flute':
    flute = np.zeros_like(t)
    notes = [432.0, 486.0, 576.0, 486.0, 648.0, 576.0, 729.0, 648.0]
    note_duration = 1.0
    for idx, freq in enumerate(notes):
        start_t = idx * note_duration
        idx_start = int(start_t * sample_rate)
        idx_end = idx_start + int(note_duration * sample_rate)
        if idx_end < len(t):
            t_note = t[idx_start:idx_end] - start_t
            sine = np.sin(2 * np.pi * freq * t_note)
            breath = 0.02 * np.random.normal(size=t_note.shape) * np.sin(2 * np.pi * 5 * t_note)
            env = np.sin(np.pi * t_note / note_duration) ** 2
            flute[idx_start:idx_end] += 0.08 * (sine + breath) * env
    samples = flute

# If user asked for dream effects we build a simple ambient texture (sine pad + noise)
if DREAM:
    pad = 0.08 * np.sin(2 * np.pi * 220.0 * t) * (1.0 - 0.5 * np.sin(2 * np.pi * 0.1 * t))
    samples = samples + pad

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
# Pre-calculate computed start and end times for each dialogue item based on loaded clips
current_time_acc = 0.0
for idx, dialogue in enumerate(dialogues_scene1):
    start = dialogue.get('start_time')
    if start is not None:
        start = float(start)
    else:
        start = current_time_acc
    
    try:
        dur = audio_clips[idx].duration
        if dur is None or dur <= 0:
            dur = 3.0
    except Exception:
        dur = 3.0
        
    dialogue['computed_start'] = start
    dialogue['computed_end'] = start + dur
    current_time_acc = max(current_time_acc, start + dur)

total_duration = current_time_acc
log.info(f"Assembling video storyboard: total duration computed as {total_duration:.2f}s")

# Load Gurmukhi font for subtitles
from PIL import ImageDraw, ImageFont
font_path = "/System/Library/Fonts/Supplemental/Gurmukhi.ttf"
try:
    font = ImageFont.truetype(font_path, 40)
    sfx_font = ImageFont.truetype(font_path, 26)
except Exception:
    font = ImageFont.load_default()
    sfx_font = ImageFont.load_default()

# Find all unique characters in dialogues to load avatars dynamically
unique_chars = sorted(list(set(
    d.get('character') for d in dialogues_scene1 
    if d.get('character') and d.get('character') not in ('SFX', 'BGM')
)))

avatars = {}
for char_name in unique_chars:
    loaded = False
    for ext in (".jpg", ".png", ".jpeg"):
        img_path = f"images/{char_name.lower()}{ext}"
        if os.path.exists(img_path):
            try:
                im = Image.open(img_path).convert('RGBA')
                im = im.resize((180, 180), Image.Resampling.LANCZOS if hasattr(Image, 'Resampling') else Image.LANCZOS)
                avatars[char_name] = im
                loaded = True
                log.info(f"Loaded custom avatar for '{char_name}' from {img_path}")
                break
            except Exception as e:
                log.warning(f"Failed to load avatar for {char_name}: {e}")
                
    # If no custom image exists, generate a dynamic letter avatar!
    if not loaded:
        try:
            avatar_im = Image.new('RGBA', (180, 180), (0, 0, 0, 0))
            adraw = ImageDraw.Draw(avatar_im)
            
            import hashlib
            h = hashlib.md5(char_name.encode('utf-8')).hexdigest()
            r = int(h[0:2], 16) % 180 + 40
            g = int(h[2:4], 16) % 180 + 40
            b = int(h[4:6], 16) % 180 + 40
            
            adraw.ellipse([5, 5, 175, 175], fill=(r, g, b, 255), outline=(255, 255, 255, 255), width=3)
            
            letter = char_name[0].upper()
            try:
                lfont = ImageFont.truetype(font_path, 80)
            except Exception:
                lfont = ImageFont.load_default()
                
            try:
                lbox = adraw.textbbox((0, 0), letter, font=lfont)
                lw = lbox[2] - lbox[0]
                lh = lbox[3] - lbox[1]
            except Exception:
                lw = 40
                lh = 60
                
            adraw.text((90 - lw // 2, 90 - lh // 2 - 5), letter, font=lfont, fill=(255, 255, 255, 255))
            avatars[char_name] = avatar_im
            log.info(f"Generated default avatar for '{char_name}'")
        except Exception as ex:
            log.warning(f"Failed to generate default avatar for {char_name}: {ex}")

# Calculate distributed horizontal positions for each unique character
num_chars = len(unique_chars)
avatar_positions = {}
width, height = 1920, 1080
for idx, name in enumerate(unique_chars):
    margin = 250
    if num_chars > 1:
        pos_x = margin + idx * (width - margin * 2) // (num_chars - 1)
    else:
        pos_x = width // 2
    avatar_positions[name] = pos_x - 90  # center-align offset

base_img = Image.open(AI_IMAGE_PATH).convert('RGB')

def make_frame(t, base=None, duration=total_duration):
    # Identify active dialogue and SFX
    active_dialogue = None
    for d in dialogues_scene1:
        if d.get('character') in ('SFX', 'BGM'):
            continue
        if d.get('computed_start', 0.0) <= t <= d.get('computed_end', 0.0):
            active_dialogue = d
            break

    # Determine which base image to use (check if active block has custom image_file)
    current_base = base_img
    if active_dialogue and active_dialogue.get("image_file"):
        img_path = active_dialogue.get("image_file").split("?")[0]
        if img_path.startswith("/"):
            img_path = img_path[1:]
        local_path = os.path.join(img_path)
        if os.path.exists(local_path):
            try:
                current_base = Image.open(local_path).convert('RGB')
            except Exception as e:
                print(f"Error loading custom block image {local_path}: {e}")

    # scale from 1.00 -> 1.08 across the duration
    scale = 1.0 + 0.08 * (t / max(duration, 1.0))
    new_w = int(current_base.width * scale)
    new_h = int(current_base.height * scale)
    
    resample = getattr(Image, 'Resampling', None)
    resample = Image.Resampling.LANCZOS if resample else Image.LANCZOS
    resized = current_base.resize((new_w, new_h), resample)
    
    left = max(0, (new_w - width) // 2)
    top = max(0, (new_h - height) // 2)
    box = (left, top, left + width, top + height)
    frame = resized.crop(box)

    # Apply Color Grading Filter
    cg = color_grading.lower() if 'color_grading' in globals() else "standard"
    if cg == "cinematic":
        from PIL import ImageEnhance
        enhancer = ImageEnhance.Contrast(frame)
        frame = enhancer.enhance(1.3)
        enhancer_brightness = ImageEnhance.Brightness(frame)
        frame = enhancer_brightness.enhance(0.95)
    elif cg == "sunset":
        r, g, b_ch = frame.split()
        r = r.point(lambda i: min(255, int(i * 1.18)))
        g = g.point(lambda i: min(255, int(i * 1.03)))
        b_ch = b_ch.point(lambda i: int(i * 0.82))
        frame = Image.merge('RGB', (r, g, b_ch))
    elif cg == "vintage":
        frame = frame.convert('L').convert('RGB')
            
    active_sfx = None
    for d in dialogues_scene1:
        if d.get('character') == 'SFX':
            if d.get('computed_start', 0.0) <= t <= d.get('computed_end', 0.0):
                active_sfx = d
                break

    # Render dynamic UI/subtitles
    draw = ImageDraw.Draw(frame, 'RGBA')
    
    # 1. Draw character avatars dynamically
    for char_name in unique_chars:
        if char_name in avatars and char_name in avatar_positions:
            pos_x = avatar_positions[char_name]
            wrapper = Image.new('RGBA', (180, 180), (0,0,0,0))
            wrapper.paste(avatars[char_name], (0,0))
            
            if active_dialogue and active_dialogue.get('character') == char_name:
                glow_layer = Image.new('RGBA', (190, 190), (0,0,0,0))
                gd = ImageDraw.Draw(glow_layer)
                gd.ellipse([0, 0, 190, 190], fill=(251, 191, 36, 180))
                frame.paste(glow_layer, (pos_x - 5, 695), glow_layer)
                frame.paste(wrapper, (pos_x, 700), wrapper)
            else:
                dimmed = wrapper.copy()
                alpha = dimmed.split()[3]
                alpha = alpha.point(lambda p: int(p * 0.4))
                dimmed.putalpha(alpha)
                frame.paste(dimmed, (pos_x, 700), dimmed)

    # 2. Render Subtitle speech bubbles
    if active_dialogue and subtitles:
        text_val = f"{active_dialogue.get('character')}: {active_dialogue.get('text')}"
        draw.rounded_rectangle([200, 920, 1720, 1020], radius=15, fill=(0, 0, 0, 190), outline=(251, 191, 36, 150), width=2)
        try:
            bbox = draw.textbbox((0, 0), text_val, font=font)
            text_w = bbox[2] - bbox[0]
            text_h = bbox[3] - bbox[1]
        except Exception:
            text_w = len(text_val) * 18
            text_h = 40
        tx = 960 - text_w // 2
        ty = 970 - text_h // 2
        
        # outline shadow
        for ox, oy in [(-2,-2), (2,-2), (-2,2), (2,2)]:
            draw.text((tx+ox, ty+oy), text_val, font=font, fill=(0,0,0,255))
        draw.text((tx, ty), text_val, font=font, fill=(251, 191, 36, 255))

    # 3. Render SFX notification
    if active_sfx:
        sfx_name = active_sfx.get('text', 'sound')
        draw.rounded_rectangle([1580, 40, 1880, 95], radius=10, fill=(16, 185, 129, 230))
        draw.text((1600, 50), f"🔊 SFX: {sfx_name.upper()}", font=sfx_font, fill=(255, 255, 255, 255))
        
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
    pass

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
    final_video_clip.write_videofile(final_video_filename, fps=24, audio_codec='aac', verbose=False, logger=None)

print("\n\n--- AMRIT CORE MASTER BUILDER STATUS: LAUNCH SUCCESS ---")
print("The final, fully assembled demonstration video has been created!")
print(f"Find the file: {final_video_filename}")
