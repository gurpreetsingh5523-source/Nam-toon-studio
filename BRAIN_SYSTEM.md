# 🧠 Nam-toon Studio Intelligent Brain System

## Overview

Your studio now has **automatic intelligence** that analyzes stories and makes smart decisions about:
1. **Voice characteristics** (age/gender/emotion → pitch/speed)
2. **Animation style** (mood → movement type)
3. **Background music** (scene emotion → audio selection)

No manual configuration needed — the brain **thinks and decides** based on story context!

---

## How It Works

### 1. Character Analysis 🎭

The brain reads character names and dialogue to determine:

#### Age Detection
- **Child**: ਬੱਚਾ, ਬੱਚੀ, child, kid → Voice: pitch **1.3x**, speed **1.2x**
- **Young Adult**: ਜਵਾਨ, young, names with "ਦੀਪ"/deep → Voice: pitch **1.1x**, speed **1.05x**
- **Adult**: Default → Voice: pitch **1.0x**, speed **1.0x**
- **Elder**: ਬੁੱਢਾ, ਬੁੱਢੀ, ਬਜ਼ੁਰਗ, old, elder → Voice: pitch **0.85x**, speed **0.85x**

#### Gender Detection
- **Female**: ਕੌਰ, Kaur, preet, jeet, ਪਤਨੀ, wife, mother → Voice: pitch **+15%**
- **Male**: ਸਿੰਘ, Singh, ਪਤੀ, husband, father → Voice: pitch **-10%**

#### Emotion Detection
- **Happy**: ਖੁਸ਼, ਹੱਸ, happy, laugh → Voice: pitch **+8%**, speed **+10%**
- **Sad**: ਦੁੱਖ, ਉਦਾਸ, sad, cry → Voice: pitch **-5%**, speed **-15%**
- **Angry**: ਗੁੱਸਾ, angry, rage → Voice: pitch **+5%**, speed **+15%**
- **Fearful**: ਡਰ, fear, scared → Voice: pitch **+12%**, speed **+20%**

### Example Results
```
ਅਮਨਦੀਪ (young male):
  Age: young_adult → pitch 1.1x, speed 1.05x
  Gender: male → pitch × 0.90
  Final: pitch 0.99x, speed 1.05x

ਦਲਜੀਤ ਕੌਰ (angry female):
  Age: adult → pitch 1.0x, speed 1.0x
  Gender: female → pitch × 1.15
  Emotion: angry → pitch × 1.05, speed × 1.15
  Final: pitch 1.21x, speed 1.15x
```

---

### 2. Scene Emotion Analysis 🎬

The brain reads scene text to detect emotional tone:

#### Emotion Keywords (Punjabi + English)
- **Happy**: ਖੁਸ਼, ਹੱਸ, ਮੁਸਕਾਨ, ਵਿਆਹ, happy, joy, smile, celebration
- **Sad**: ਦੁੱਖ, ਉਦਾਸ, ਰੋ, ਅੱਥਰੂ, sad, cry, tears, grief
- **Tragic**: ਮੌਤ, ਅੱਗ, ਜਲ, ਹਾਦਸਾ, death, fire, tragedy, accident (2x weight!)
- **Angry**: ਗੁੱਸਾ, ਕ੍ਰੋਧ, ਚੀਕ, ਜ਼ੁਲਮ, angry, rage, fight
- **Tense**: ਡਰ, ਘਬਰਾ, ਪੁਲਿਸ, ਧਮਕੀ, fear, police, threat, danger
- **Peaceful**: ਸ਼ਾਂਤ, ਸੁਕੂਨ, ਬਾਗ, peaceful, calm, nature

#### Intensity Calculation
- Counts keyword matches
- Normalizes to 0.0-1.0 scale
- Multiple strong emotions → **tense** (intensity 0.8)

### Example Results
```
ਸ਼ੁਰੂਆਤ (Introduction):
  Keywords: ਖੁਸ਼ (happy), ਬੱਚਾ (child), ਹੱਸ (laugh)
  Emotion: happy (intensity 0.40)
  Music: birds.wav @ 0.06 volume

ਹਾਦਸਾ (Tragedy):
  Keywords: ਅੱਗ (fire), ਜਲ (burn), ਮੌਤ (death), ਦੁੱਖ (sad)
  Emotion: tragic (intensity 1.00)
  Music: strings.wav @ 0.20 volume

ਪੁਲਿਸ (Police):
  Keywords: ਪੁਲਿਸ (police), ਧਮਕੀ (threat), ਡਰ (fear)
  Emotion: tense (intensity 0.60)
  Music: heartbeat.wav @ 0.11 volume
```

---

### 3. Animation Style Selection 🎨

Based on scene emotion, the brain decides movement parameters:

| Emotion | Movement | Zoom Speed | Pan Direction | Color Intensity |
|---------|----------|------------|---------------|-----------------|
| **Peaceful** | gentle | 0.7x | center | 0.2 |
| **Happy** | normal | 1.2x | up | 0.15 |
| **Sad** | gentle | 0.8x | down | 0.4 |
| **Angry** | intense | 1.5x | right | 0.5 |
| **Tragic** | intense | 1.3x | center | 0.6 |
| **Tense** | chaotic | 1.4x | left | 0.45 |

---

### 4. Background Music Selection 🎵

Each emotion has specific audio characteristics:

| Emotion | Audio Type | Frequency | Character |
|---------|-----------|-----------|-----------|
| **Happy** | Bright tones | 440 Hz (A4) | Uplifting, modulated |
| **Sad** | Low sustain | 220 Hz (A3) | Slow, descending |
| **Tragic** | Dissonant | 200 + 297.5 Hz | Pulsing, unstable |
| **Angry** | Distorted | 180 Hz | Aggressive, clipped |
| **Peaceful** | Harmonic | 264 + 330 Hz | Soft, consonant |
| **Tense** | Complex | 200 + 297.5 Hz | Pulsing, urgent |
| **Neutral** | Ambient | 220 Hz + noise | Birds/nature |

---

## Technical Implementation

### Files

1. **`colab/intelligent_brain.py`** — Core brain logic
   - `IntelligentBrain` class
   - Character analysis methods
   - Scene emotion detection
   - Animation style decisions

2. **`colab/master_builder.py`** — Integration
   - Imports brain at line 22-24
   - Scene analysis at line 149-165
   - Voice modulation at line 340-388
   - Background music at line 621-677

### Usage

The brain activates **automatically** when using `--scenes`:

```bash
# Automatic brain analysis
python colab/master_builder.py --scenes colab/scenes.json --captions --timecode

# Brain will:
# 1. Analyze each character's age/gender/emotion
# 2. Detect scene emotion from keywords
# 3. Select appropriate background music
# 4. Apply voice modulation (pitch/speed via ffmpeg)
# 5. Choose animation style
```

### Voice Modulation Pipeline

1. **Generate base TTS** (gTTS Punjabi voice)
2. **Analyze character** (brain determines pitch/speed)
3. **Apply ffmpeg filters**:
   - `atempo={speed}` — Speed adjustment (0.5-2.0x)
   - `asetrate=44100*{pitch}` — Pitch shift
   - `aresample=44100` — Resample to standard rate

Example command:
```bash
ffmpeg -i dialogue_0_raw.mp3 \
  -filter_complex 'atempo=1.15,asetrate=44100*1.21,aresample=44100' \
  -q:a 2 dialogue_0.mp3
```

---

## Console Output Examples

### Brain Activation
```
🧠 Activating Intelligent Brain for scene analysis...
  Scene 0: happy (0.40) → birds.wav
  Scene 1: tense (0.80) → heartbeat.wav
```

### Character Analysis
```
🧠 ਕੁਲਵੰਤ (Narrator): age=adult, gender=male, pitch=0.97x, speed=1.10x
🧠 ਅਮਨਦੀਪ: age=young_adult, gender=female, pitch=1.37x, speed=1.16x
🧠 ਦਲਜੀਤ ਕੌਰ: age=adult, gender=female, pitch=1.21x, speed=1.15x
```

### Scene Emotion
```
🧠 Scene emotion: happy → Background music: birds.wav @ 0.06
```

---

## Future Enhancements

### Planned Additions
1. **Dynamic animation** — Different movement patterns per emotion (bounce, drift, shake)
2. **Multi-track music** — Layer multiple instruments based on intensity
3. **Facial expressions** — Avatar mood changes based on dialogue emotion
4. **Learning system** — Brain remembers character traits across sessions
5. **Voice variety** — Multiple TTS engines for more natural variation

### Configuration (Future)
```python
brain_config = {
    'voice_modulation': {
        'enabled': True,
        'pitch_range': (0.7, 1.5),  # Min/max pitch multiplier
        'speed_range': (0.7, 1.3),  # Min/max speed multiplier
    },
    'music_selection': {
        'enabled': True,
        'volume_range': (0.05, 0.25),
    },
    'animation_style': {
        'enabled': True,
        'movement_intensity': 1.0,  # Global multiplier
    }
}
```

---

## Testing the Brain

### Standalone Test
```bash
cd /Users/gurpreetdhillon/Nam-toon-studio/colab
python intelligent_brain.py
```

Output:
```
=== CHARACTER ANALYSIS ===
ਅਮਨਦੀਪ:
  Age: young_adult, Gender: male, Emotion: calm
  Voice: Pitch=0.99, Speed=1.05

=== SCENE EMOTION ANALYSIS ===
ਹਾਦਸਾ:
  Emotion: tragic (intensity: 1.00)
  Music: strings.wav @ 0.20
  Animation: intense, zoom=1.56, pan=center

✅ Brain test complete!
```

### Integrated Test
```bash
# Dry-run with 2 scenes
python colab/master_builder.py --scenes colab/scenes.json --scenes-limit 2 --dry-run --captions

# Full render with brain intelligence
python colab/master_builder.py --scenes colab/scenes.json --captions --timecode --output Intelligent_Test.mp4
```

---

## Brain Philosophy

The studio brain follows these principles:

1. **Context-Aware**: Analyzes full story context, not just individual lines
2. **Culturally Sensitive**: Understands Punjabi names, emotions, cultural markers
3. **Logically Consistent**: Character traits remain stable within a scene
4. **Emotionally Intelligent**: Detects subtle mood changes from keywords
5. **Artistically Balanced**: Modulations are subtle, not extreme

**The goal**: Make the studio **think like a director** — understanding character, emotion, and pacing automatically.

---

## Credits

Created by: Nam-toon Studio
Brain Version: 1.0
Integration Date: 2025-11-01
Language Support: Punjabi (ਪੰਜਾਬੀ) + English

**ਵਾਹਿਗੁਰੂ ਜੀ ਕਾ ਖਾਲਸਾ, ਵਾਹਿਗੁਰੂ ਜੀ ਕੀ ਫਤਹਿ!** 🙏
