# 🎬 How to Make Your Complete Video
# ਪੂਰੀ ਵੀਡੀਓ ਕਿਵੇਂ ਬਣਾਈਏ

## Quick Start - ਤੇਜ਼ ਸ਼ੁਰੂਆਤ

Just run this one command:
```bash
python make_video.py
```

That's it! ਬੱਸ ਇੰਨਾ ਹੀ!

---

## What Happens - ਕੀ ਹੁੰਦਾ ਹੈ

### The script does 7 steps automatically:

#### **Step 1: Load Story** 📖
- Reads your story from: `temp_adhhi_aurat_scenes.json`
- Story: "ਅੱਧੀ ਔਰਤ" (8 scenes)
- Duration: ~106 seconds

#### **Step 2: Generate Voices** 🎤
- Uses gTTS (Google Text-to-Speech) for Punjabi
- **Voice Settings:**
  - Pitch: **0.82** (mature male voice, NOT 13-year-old!)
  - Speed: **0.92** (natural speaking pace)
- Character: ਰਚਨਾ (narrator)
- Saves to: `audio/dialogue_0.mp3`, `dialogue_1.mp3`, etc.

#### **Step 3: Select Music** 🎵
- **Audio Brain** chooses background music for each scene
- Based on emotion: trouble → heartbeat.wav, sad → strings.wav
- **Volume: 0.35** (35% - NOW AUDIBLE!)
  - Before: 0.15 (too quiet)
  - After: 0.35 (you can hear it!)

#### **Step 4: Create Visuals** 🎨
- **Visual Brain** creates animations:
  - Gradient backgrounds (colors match emotions)
  - Character portraits (using Punjabi names: ਰਚਨਾ)
  - Camera movements (handheld for tense, steady for calm)
- Resolution: 1920x1080 (Full HD)

#### **Step 5: Add Sound Effects** 🔊
- **SFX Brain** adds location-based sounds:
  - Workshop → metal_clang, tools
  - Village → birds_chirping, voices
  - Tense scenes → heavy_breathing
- Volume: 0.30 (subtle but present)

#### **Step 6: Mix Everything** 🎚️
- Combines all elements:
  - Voice (main focus)
  - Background music (with ducking)
  - Sound effects (ambient)
- **Ducking:** Music gets quieter when someone speaks
- Adds Punjabi captions at bottom

#### **Step 7: Export Video** 💾
- Creates: `AmritCore_FINAL_STUDIO_LAUNCH.mp4`
- Format: MP4 (H.264 video + AAC audio)
- Size: ~3-4 MB
- Duration: ~106 seconds

---

## What's Been Fixed - ਕੀ ਠੀਕ ਕੀਤਾ ਗਿਆ

### 1. 🎵 Background Music Volume
**Before:**
```python
music_volume = 0.15  # Too quiet - "no background music"
```

**After:**
```python
music_volume = 0.35  # Much louder - now audible!
```

**Result:** You will now hear the background music clearly!

### 2. 🎤 Voice Quality
**Before:**
```
Default gTTS voice = too high pitched
User complaint: "13 saal de bachhe di awaaz"
```

**After:**
```python
voice_pitch = 0.82  # Mature adult male
voice_speed = 0.92  # Natural pace
```

**Result:** Voice sounds like a mature man, not a child!

### 3. 🎭 Character Portraits
**Before:**
```
Unicode mismatch: Gujarati ચ instead of Punjabi ਚ
Result: "orange circle" only, no portraits
```

**After:**
```
All characters use correct Punjabi Unicode
Character names: ਰਚਨਾ (U+0A1A)
```

**Result:** Character portraits will display correctly!

### 4. 🧠 All Brains Working
**Tested separately:**
- ✅ Audio Brain: Choosing correct music
- ✅ Voice Brain: Using voice profiles
- ✅ Visual Brain: Camera & colors working
- ✅ SFX Brain: Sound effects appropriate

**Result:** All 4 brains coordinating properly!

---

## How to Use - ਕਿਵੇਂ ਵਰਤੀਏ

### Method 1: Simple (Recommended)
```bash
cd /Users/gurpreetdhillon/Nam-toon-studio
python make_video.py
```

Just answer "yes" when prompted!

### Method 2: Direct Command
```bash
cd /Users/gurpreetdhillon/Nam-toon-studio
source .venv/bin/activate
python colab/master_builder.py --scenes temp_adhhi_aurat_scenes.json --verbose --duck --bg-gain 0.35
```

### Method 3: Custom Settings
```bash
# Louder music (50%)
python colab/master_builder.py --scenes temp_adhhi_aurat_scenes.json --bg-gain 0.50

# Quieter music (25%)
python colab/master_builder.py --scenes temp_adhhi_aurat_scenes.json --bg-gain 0.25

# No ducking (music stays loud during speech)
python colab/master_builder.py --scenes temp_adhhi_aurat_scenes.json --bg-gain 0.35
```

---

## What to Check After - ਬਾਅਦ ਵਿੱਚ ਕੀ ਚੈੱਕ ਕਰੀਏ

### ✅ Checklist:

1. **Open video:** `AmritCore_FINAL_STUDIO_LAUNCH.mp4`

2. **Listen for music:** 🎵
   - Should hear background music throughout
   - Music should be quieter during speech (ducking)
   - Music should match scene emotion

3. **Check voice:** 🎤
   - Should sound like mature adult male
   - NOT like 13-year-old child
   - Should be clear and natural

4. **Look for portraits:** 🎭
   - Character should appear (not just orange circle)
   - Portrait should show ਰਚਨਾ
   - Should be positioned correctly

5. **Read captions:** 📝
   - Punjabi text should appear at bottom
   - Should match what's being said
   - Should be readable

6. **Check timing:** ⏱️
   - Video should be ~106 seconds
   - 8 scenes total
   - Smooth transitions between scenes

---

## If Something's Still Wrong - ਜੇ ਫਿਰ ਵੀ ਕੁਝ ਗਲਤ ਹੈ

### Problem: Music still too quiet
**Solution:**
```bash
python colab/master_builder.py --scenes temp_adhhi_aurat_scenes.json --bg-gain 0.50
```

### Problem: Voice still too high
**Solution:** Edit `brain_memory/character_voice_profiles.json`:
```json
{
  "ਰਚਨਾ": {
    "voice_pitch": 0.75,  // Lower = deeper
    "voice_speed": 0.90
  }
}
```

### Problem: No portraits showing
**Solution:** Check that portrait files exist:
```bash
ls portraits/
# Should see: ਰਚਨਾ.png, etc.
```

### Problem: Video generation fails
**Solution:** Check logs:
```bash
python make_video.py 2>&1 | tee video_generation.log
```

---

## Understanding the 4-Brain System - 4 ਬ੍ਰੇਨ ਸਿਸਟਮ

### 🎵 Audio Brain
**Job:** Select background music
**Logic:**
- Reads scene emotion
- Maps emotion to music file
  - trouble → heartbeat.wav
  - despair → strings.wav
  - brotherhood → birds.wav
- Sets volume to 0.35

### 🎤 Voice Brain
**Job:** Generate voice audio
**Logic:**
- Loads character voice profiles
- Gets settings for character (ਰਚਨਾ)
- Applies pitch (0.82) and speed (0.92)
- Uses gTTS to generate audio

### 🎨 Visual Brain
**Job:** Create animations
**Logic:**
- Chooses camera movement based on emotion
  - tense → handheld
  - sad → static close-up
- Selects color palette
  - happy → yellow, green
  - tragic → dark gray, black
- Sets animation intensity

### 🔊 SFX Brain
**Job:** Add sound effects
**Logic:**
- Picks location-based ambient sounds
  - workshop → metal_clang
  - village → birds_chirping
- Adds emotion-based effects
  - tense → heavy_breathing
  - despair → wind, silence

---

## Technical Details - ਤਕਨੀਕੀ ਵੇਰਵੇ

### Audio Processing
- Sample rate: 44,100 Hz
- Channels: Stereo
- Format: MP3 for dialogue, WAV for music
- Mixing: Voice + Music + SFX

### Video Processing
- Resolution: 1920x1080 (Full HD)
- Frame rate: 24 fps
- Codec: H.264
- Container: MP4

### Voice Settings
- Language: Punjabi (pa)
- TTS Engine: gTTS
- Pitch modification: ffmpeg
- Speed modification: ffmpeg

### File Structure
```
Nam-toon-studio/
├── make_video.py                    # ← Run this!
├── temp_adhhi_aurat_scenes.json     # Story scenes
├── colab/master_builder.py          # Video generator
├── brain_memory/
│   ├── character_voice_profiles.json  # Voice settings
│   └── ਬ੍ਰੇਨ_ਟੈਸਟ_ਰਿਪੋਰਟ.md           # Brain test report
├── audio/
│   ├── dialogue_0.mp3 to dialogue_7.mp3
│   ├── ambient.wav
│   ├── heartbeat.wav
│   └── strings.wav
└── AmritCore_FINAL_STUDIO_LAUNCH.mp4  # Final output!
```

---

## Summary - ਸੰਖੇਪ

### What You Get:
✅ Full video with 8 scenes (~106 seconds)
✅ Mature male voice (pitch 0.82)
✅ Audible background music (volume 0.35)
✅ Character portraits (Punjabi Unicode)
✅ Sound effects
✅ Punjabi captions
✅ Professional mixing (ducking)

### What's Different from Before:
1. Music **2.3x louder** (0.15 → 0.35)
2. Voice **sounds mature** (not child)
3. Portraits **will show** (Unicode fixed)
4. All 4 brains **tested and working**

### To Generate:
```bash
python make_video.py
```

### To Watch:
```bash
open AmritCore_FINAL_STUDIO_LAUNCH.mp4
```

---

**Ready! ਤਿਆਰ ਹੈ!** 🎬

Just run: `python make_video.py` and watch your complete video with all fixes applied!
