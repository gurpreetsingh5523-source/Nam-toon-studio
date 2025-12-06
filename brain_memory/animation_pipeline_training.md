# Animation Pipeline Training Guide
## How Nam-toon Studio Creates Animated Videos

### 🎯 Root Cause Analysis: "Pink Circle Only" Issue

**Problem**: Video showed only background gradient (pink circle) with NO voice, NO music, NO actors, NO SFX

**Root Causes Identified**:
1. ✅ **Audio IS working** - All MP3/WAV files generated correctly
2. ✅ **Video codec IS working** - MP4 has proper H264 video + AAC audio streams
3. ❌ **Character encoding mismatch** - JSON had mixed "ਰચਨਾ" (Gujarati ચ) vs "ਰਚਨਾ" (Punjabi ਚ)
   - Avatar generated for "ਰਚਨਾ" but overlay looked for "ਰચਨਾ" → mismatch → no portrait shown
4. ❌ **Portrait overlay logic** - Portraits dict populated but `make_frame()` character lookup failed

### 🎬 Complete Animation Pipeline Flow

```
INPUT: scenes.json with dialogues[]
    ↓
STEP 1: Character Avatar Generation
    - Collect unique characters from all dialogues
    - Generate colored circle avatars with initials
    - Store in `portraits` dict: {character_name: PIL.Image}
    ↓
STEP 2: Audio Generation (Parallel TTS)
    - For each dialogue: gTTS(text, lang='pa') → MP3
    - Apply voice modulation (pitch/speed) via ffmpeg if character_profiles exist
    - Concatenate all clips → final_dialogue_audio
    - Apply normalization
    ↓
STEP 3: Background Audio
    - Brain selects emotion-appropriate sound (ambient.wav, birds.wav, heartbeat.wav, etc.)
    - Loop background to match dialogue duration
    - Apply ducking: reduce BG volume during speech (envelope with attack/release)
    ↓
STEP 4: Mix Audio
    - CompositeAudioClip([dialogue, background_ducked])
    - Optional mastering: compressor + limiter
    ↓
STEP 5: Video Frame Generation (`make_frame(t)` function)
    A. Background:
       - Create gradient based on scene emotion (HSV colors)
       - Vectorized numpy gradient (1000x faster than putpixel)
    B. Find Current Speaker:
       - Lookup t in DIALOGUE_TIMELINE [{start, end, character, text}]
    C. Overlay Speaking Character Portrait:
       - Resize to 400x400
       - Position center-top with bounce animation
       - ⚠️ KEY: `if portraits and current_char and current_char in portraits:`
    D. Overlay Other Characters (smaller, bottom, semi-transparent)
    E. Add Captions (if CAPTIONS=True):
       - Wrap text, draw rounded rectangle background
       - Center-bottom position
    F. Add Timecode (if TIMECODE=True):
       - Top-left corner with semi-transparent background
    ↓
STEP 6: Assemble Video
    - VideoClip(make_frame, duration=total_duration).set_fps(24)
    - Apply fadein(0.5s)
    - Attach mixed audio: .set_audio(final_audio_mix)
    ↓
STEP 7: Write Output
    - write_videofile(codec='libx264', audio_codec='aac')
    - ffmpeg_params: +faststart, yuv420p for compatibility
```

### 🧠 Critical Lessons for the Brain

#### Lesson 1: Character Name Consistency is CRITICAL
```python
# ❌ WRONG - Mixed Unicode characters
dialogues = [
    {"character": "ਰਚਨਾ", ...},  # Punjabi ਚ (U+0A1A)
    {"character": "ਰચਨਾ", ...},  # Gujarati ચ (U+0A9A) - MISMATCH!
]

# ✅ CORRECT - Consistent character names
dialogues = [
    {"character": "ਰਚਨਾ", ...},  # All using Punjabi ਚ
    {"character": "ਰਚਨਾ", ...},
]
```

**Brain Rule**: Always normalize character names:
- Use Unicode NFD normalization
- Strip whitespace
- Case-sensitive matching for non-Latin scripts

#### Lesson 2: Portrait Overlay Logic Must Be Defensive
```python
# Current logic (fragile):
if portraits and current_char and current_char in portraits:
    speaker_img = portraits[current_char]
    # overlay logic...

# ✅ Better logic (defensive):
if portraits:
    # Normalize character name before lookup
    lookup_char = current_char.strip() if current_char else None
    if lookup_char and lookup_char in portraits:
        speaker_img = portraits[lookup_char]
        try:
            # overlay with error handling
            frame.paste(speaker_resized, (pos_x, pos_y), speaker_resized)
        except Exception as e:
            log.warning(f"Portrait paste failed for {lookup_char}: {e}")
            # Try fallback: paste as RGB without alpha
            try:
                frame.paste(speaker_resized.convert('RGB'), (pos_x, pos_y))
            except Exception:
                pass  # Skip this character overlay
```

#### Lesson 3: Audio Pipeline Verification
```python
# Always verify intermediate audio exists and has content:
def verify_audio_clip(clip, name="audio"):
    try:
        duration = clip.duration
        if duration <= 0:
            raise ValueError(f"{name} has zero duration")
        # Try to sample audio
        arr = clip.to_soundarray(fps=44100, nbytes=2)
        if arr.size == 0:
            raise ValueError(f"{name} has empty audio array")
        return True
    except Exception as e:
        log.error(f"Audio verification failed for {name}: {e}")
        return False

# Use before mixing:
verify_audio_clip(final_dialogue_audio, "dialogue")
verify_audio_clip(background_audio, "background")
```

#### Lesson 4: Debug Visualization for Frames
```python
# Add diagnostic overlay when DEBUG=True
if DEBUG:
    draw = ImageDraw.Draw(frame, 'RGBA')
    font = _get_font(20)
    debug_text = f"t={t:.1f}s char={current_char} portraits={len(portraits)}"
    draw.text((10, height-30), debug_text, font=font, fill=(0, 255, 0, 255))
```

### 🎓 Training Recommendations for Brain

#### Auto-Fix Strategy 1: Character Name Validation
```python
def validate_and_fix_character_names(scenes_json):
    """Scan all dialogues and normalize character names"""
    import unicodedata
    
    # Collect all unique character names
    char_names = set()
    for scene in scenes_json['scenes']:
        for d in scene.get('dialogues', []):
            char = d.get('character')
            if char:
                char_names.add(char)
    
    # Build normalization map (find similar names)
    name_map = {}
    for name1 in char_names:
        normalized1 = unicodedata.normalize('NFD', name1).strip()
        for name2 in char_names:
            if name1 != name2:
                normalized2 = unicodedata.normalize('NFD', name2).strip()
                # If normalized forms are similar, map to canonical form
                if normalized1 == normalized2:
                    # Use the first occurrence as canonical
                    canonical = min(name1, name2)
                    name_map[name1] = canonical
                    name_map[name2] = canonical
    
    # Apply fixes
    fixes_applied = 0
    for scene in scenes_json['scenes']:
        for d in scene.get('dialogues', []):
            char = d.get('character')
            if char and char in name_map:
                d['character'] = name_map[char]
                fixes_applied += 1
    
    return fixes_applied, name_map
```

#### Auto-Fix Strategy 2: Portrait Rendering Validation
```python
def validate_portrait_rendering(portraits, dialogue_timeline):
    """Check that all speaking characters have portraits"""
    missing = []
    for seg in dialogue_timeline:
        char = seg.get('character')
        if char and char not in portraits:
            missing.append(char)
    
    if missing:
        log.warning(f"Missing portraits for: {set(missing)}")
        log.info("Portrait keys available: {list(portraits.keys())}")
        # Suggest: generate fallback avatars or use default
    
    return len(missing) == 0
```

#### Auto-Fix Strategy 3: Frame Content Verification
```python
def verify_frame_has_content(frame_array, threshold_std=5.0):
    """Check if frame has visual content (not just solid color)"""
    import numpy as np
    std = np.std(frame_array)
    if std < threshold_std:
        return False, f"Frame too uniform (std={std:.1f})"
    return True, "OK"

# Use during render:
sample_frame = make_frame(10.0)  # Sample at 10s
ok, msg = verify_frame_has_content(sample_frame)
if not ok:
    log.error(f"Frame validation failed: {msg}")
    # Trigger diagnostic mode or abort
```

### 🔧 Recommended Master Brain Improvements

1. **Add Pre-Render Validation Phase**:
   ```python
   def pre_render_validation(scenes, portraits, audio_clips):
       errors = []
       warnings = []
       
       # Check 1: Character name consistency
       char_names = [d['character'] for s in scenes for d in s.get('dialogues', [])]
       unique_chars = set(char_names)
       if len(unique_chars) != len(set(portraits.keys())):
           warnings.append(f"Character mismatch: {unique_chars} vs {set(portraits.keys())}")
       
       # Check 2: Audio clips exist and have duration
       for i, clip in enumerate(audio_clips):
           if not hasattr(clip, 'duration') or clip.duration <= 0:
               errors.append(f"Audio clip {i} has no duration")
       
       # Check 3: Portrait images are valid
       for name, img in portraits.items():
           if img.size[0] == 0 or img.size[1] == 0:
               errors.append(f"Portrait for {name} has zero size")
       
       return errors, warnings
   ```

2. **Add Post-Render Smoke Test**:
   ```python
   def post_render_smoke_test(video_path):
       """Quick validation that output video has expected properties"""
       try:
           from moviepy.editor import VideoFileClip
           import numpy as np
           
           v = VideoFileClip(video_path)
           
           # Test 1: Has audio
           if v.audio is None:
               return False, "No audio track"
           
           # Test 2: Audio duration matches video
           if abs(v.audio.duration - v.duration) > 1.0:
               return False, f"Audio/video duration mismatch"
           
           # Test 3: Sample frames have content
           for t in [v.duration * 0.25, v.duration * 0.5, v.duration * 0.75]:
               frame = v.get_frame(t)
               std = np.std(frame)
               if std < 10.0:
                   return False, f"Frame at t={t:.1f}s too uniform (std={std:.1f})"
           
           v.close()
           return True, "OK"
       except Exception as e:
           return False, str(e)
   ```

3. **Add Character Encoding Sanitizer**:
   ```python
   def sanitize_punjabi_text(text):
       """Fix common Unicode issues in Punjabi text"""
       import unicodedata
       
       # NFD normalization
       text = unicodedata.normalize('NFD', text)
       
       # Replace common mis-typed characters
       replacements = {
           '\u0A9A': '\u0A1A',  # Gujarati ચ → Punjabi ਚ
           '\u0A97': '\u0A17',  # Gujarati ગ → Punjabi ਗ
           # Add more as discovered
       }
       
       for wrong, correct in replacements.items():
           text = text.replace(wrong, correct)
       
       # NFC normalization (canonical composition)
       text = unicodedata.normalize('NFC', text)
       
       return text
   ```

### 📊 Success Metrics to Track

The Brain should log these metrics after each render:

```json
{
  "render_id": "adhhi_aurat_v1",
  "timestamp": "2025-11-03T20:56:00Z",
  "validation": {
    "character_name_consistency": true,
    "all_portraits_rendered": true,
    "audio_duration_match": true,
    "frame_content_variance": 27.1,
    "smoke_test_passed": true
  },
  "stats": {
    "total_scenes": 8,
    "total_dialogues": 8,
    "unique_characters": 1,
    "total_duration_sec": 106.42,
    "dialogue_loudness_db": -3.05,
    "background_loudness_db": -15.49
  },
  "fixes_applied": [
    {"type": "character_encoding", "count": 1, "characters": ["ਰચਨਾ→ਰਚਨਾ"]}
  ]
}
```

### 🎯 Next Steps for Brain Learning

1. **Implement validation hooks** in `colab/master_builder.py`:
   - Pre-render validation
   - Post-render smoke test
   - Character name sanitization

2. **Add diagnostic mode** (`--diagnose` flag):
   - Sample frames at multiple timestamps
   - Print portrait overlay attempts
   - Log character name lookups

3. **Create test suite** with known-good scenes:
   - Single character, multiple dialogues
   - Multiple characters with interactions
   - Edge cases: empty dialogues, missing characters

4. **Build auto-recovery system**:
   - If portrait lookup fails → generate fallback avatar on-the-fly
   - If audio missing → use sample WAV
   - If frame too uniform → add diagnostic overlay

---

**Last Updated**: 2025-11-03  
**Issue**: Character encoding mismatch in JSON  
**Fix**: Normalized "ਰચਨਾ" → "ਰਚਨਾ" (Gujarati → Punjabi)  
**Impact**: Portraits now render correctly in video
