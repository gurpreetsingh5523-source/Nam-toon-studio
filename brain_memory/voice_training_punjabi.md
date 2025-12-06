# ਆਵਾਜ਼ ਦੀ ਸਿਖਲਾਈ - Voice Training Guide (ਪੰਜਾਬੀ)

## 🎤 ਸਮੱਸਿਆ: ਆਵਾਜ਼ 13 ਸਾਲ ਦੇ ਬੱਚੇ ਵਰਗੀ ਹੈ

### ਕਾਰਨ (Root Cause)
gTTS (Google Text-to-Speech) ਪੰਜਾਬੀ ਲਈ ਸਿਰਫ਼ ਇੱਕ default voice ਦਿੰਦਾ ਹੈ ਜੋ:
- ਬਹੁਤ ਹਾਈ pitch ਹੈ (ਬੱਚੇ ਵਰਗੀ)
- ਕੋਈ depth/bass ਨਹੀਂ
- Monotone (ਇੱਕੋ ਸੁਰ)

## ✅ ਹੱਲ 1: Pitch ਅਤੇ Speed ਬਦਲੋ (ffmpeg ਨਾਲ)

### Character Profiles ਬਣਾਓ
```python
character_profiles = {
    "ਰਚਨਾ": {
        "age": "adult",           # adult, young, elder
        "gender": "male",         # male, female, neutral
        "voice_pitch": 0.85,      # 0.85 = mature male (lower)
        "voice_speed": 0.95,      # 0.95 = slightly slower
        "emotion": "serious"      # serious, happy, sad, angry
    },
    "ਦਲੀਪ": {
        "age": "middle_aged",
        "gender": "male",
        "voice_pitch": 0.80,      # ਹੋਰ ਵੀ ਨੀਵਾਂ (deeper)
        "voice_speed": 0.90,
        "emotion": "troubled"
    },
    "ਅਮਨਦੀਪ": {
        "age": "young_adult",
        "gender": "male",
        "voice_pitch": 0.90,      # ਜਵਾਨ ਪਰ mature
        "voice_speed": 1.0,
        "emotion": "neutral"
    }
}
```

### Pitch ਬਦਲਣ ਦਾ Formula
```python
# ਹਾਈ pitch (ਬੱਚੇ ਵਰਗੀ) → Low pitch (ਆਦਮੀ ਵਰਗੀ)
pitch_multiplier = {
    "child": 1.2,           # ਬੱਚਾ (higher)
    "young_male": 0.90,     # ਜਵਾਨ ਮੁੰਡਾ
    "adult_male": 0.85,     # ਬਾਲਗ ਆਦਮੀ
    "mature_male": 0.80,    # ਪੱਕੀ ਉਮਰ ਦਾ ਆਦਮੀ
    "elder_male": 0.75,     # ਬਜ਼ੁਰਗ
    
    "young_female": 1.05,   # ਜਵਾਨ ਕੁੜੀ
    "adult_female": 1.0,    # ਬਾਲਗ ਔਰਤ
    "elder_female": 0.95    # ਬਜ਼ੁਰਗ ਔਰਤ
}
```

### ffmpeg Command (ਮੌਜੂਦਾ ਕੋਡ ਵਿੱਚ)
```python
# ਇਹ master_builder.py ਵਿੱਚ ਪਹਿਲਾਂ ਹੀ ਹੈ, ਪਰ pitch ਠੀਕ ਚਾਹੀਦੀ ਹੈ:
pitch = 0.85  # ਬਾਲਗ ਮਰਦ ਲਈ
speed = 0.95

cmd = [
    'ffmpeg', '-y', '-i', temp_path,
    '-filter_complex',
    f'atempo={speed},asetrate=44100*{pitch},aresample=44100',
    '-q:a', '2',
    out_path
]
```

## ✅ ਹੱਲ 2: macOS 'say' Command (ਬਿਹਤਰ Quality)

macOS ਦੀ built-in TTS ਵਧੀਆ ਹੈ:
```python
import subprocess

# ਉਪਲਬਧ voices ਵੇਖੋ:
subprocess.run(['say', '-v', '?'])

# ਪੰਜਾਬੀ ਲਈ ਵਧੀਆ voices:
voices = {
    "male_deep": "Alex",      # ਡੂੰਘੀ ਆਵਾਜ਼
    "male_clear": "Daniel",   # ਸਾਫ਼ ਆਵਾਜ਼
    "female": "Samantha",     # ਔਰਤ
    "elder": "Fred"           # ਬਜ਼ੁਰਗ
}

# ਵਰਤੋਂ:
text = "ਇਹ ਕਹਾਣੀ ਮੇਰੇ ਦੋਸਤ ਦੀ ਮਾਸੀ ਜੀ ਦੇ ਪਰਿਵਾਰ ਦੀ ਹੈ"
subprocess.run([
    'say', '-v', 'Alex',
    '-o', 'output.aiff',
    '--data-format=LEI16@22050',  # ਕੁਆਲਿਟੀ
    text
])
```

## ✅ ਹੱਲ 3: Custom Voice Model (ਸਭ ਤੋਂ ਵਧੀਆ)

### Coqui TTS (Open Source)
```python
from TTS.api import TTS

# Model load ਕਰੋ
tts = TTS("tts_models/multilingual/multi-dataset/your_tts")

# ਆਪਣੀ ਆਵਾਜ਼ clone ਕਰੋ
tts.tts_to_file(
    text="ਤੁਹਾਡਾ ਪੰਜਾਬੀ ਟੈਕਸਟ",
    speaker_wav="reference_voice.wav",  # ਤੁਹਾਡੀ sample ਆਵਾਜ਼
    language="pa",
    file_path="output.wav"
)
```

## 📊 Voice Parameters ਦੀ ਸੂਚੀ

### 1. Pitch (ਸੁਰ)
```python
# 1.0 = original
# 0.5 = ਬਹੁਤ ਨੀਵਾਂ (very deep)
# 2.0 = ਬਹੁਤ ਉੱਚਾ (very high)

recommended = {
    "ਬਾਲਗ_ਮਰਦ": 0.85,      # ✓ Mature male
    "ਜਵਾਨ_ਮੁੰਡਾ": 0.95,     # Young adult male
    "ਬਜ਼ੁਰਗ": 0.75,         # Elder (deeper)
    "ਔਰਤ": 1.05,           # Female
    "ਬੱਚਾ": 1.3            # Child
}
```

### 2. Speed (ਰਫ਼ਤਾਰ)
```python
# 1.0 = normal
# 0.5 = ਅੱਧੀ ਰਫ਼ਤਾਰ (slow)
# 2.0 = ਦੁੱਗਣੀ ਰਫ਼ਤਾਰ (fast)

recommended = {
    "ਕਹਾਣੀ_ਸੁਣਾਉਣਾ": 0.90,   # ਹੌਲੀ, clear
    "ਗੱਲਬਾਤ": 1.0,           # Normal
    "ਜਲਦੀ_ਵਿੱਚ": 1.15,       # ਤੇਜ਼
    "ਡਰਾਮਾ": 0.85            # ਬਹੁਤ ਹੌਲੀ
}
```

### 3. Emphasis (ਜ਼ੋਰ)
```python
# ਖਾਸ ਸ਼ਬਦਾਂ ਤੇ ਜ਼ੋਰ
text_with_emphasis = {
    "normal": "ਇਹ ਕਹਾਣੀ ਹੈ",
    "emphasis": "ਇਹ **ਕਹਾਣੀ** ਹੈ"  # ਕਹਾਣੀ ਤੇ ਜ਼ੋਰ
}

# SSML ਨਾਲ (ਜੇ ਸਹਾਇਤਾ ਹੈ):
ssml = '''
<speak>
  ਇਹ <emphasis level="strong">ਕਹਾਣੀ</emphasis> ਹੈ
</speak>
'''
```

## 🎯 ਸਟੂਡੀਓ ਬ੍ਰੇਨ ਲਈ ਅਭਿਆਸ

### Sample 1: ਬਾਲਗ ਮਰਦ (Adult Male)
```json
{
  "character": "ਰਚਨਾ",
  "text": "ਏਹ ਕਹਾਣੀ ਮੇਰੇ ਦੋਸਤ ਦੀ ਮਾਸੀ ਜੀ ਦੇ ਪਰਿਵਾਰ ਦੀ ਹੈ",
  "voice_settings": {
    "pitch": 0.85,
    "speed": 0.95,
    "volume": 1.0
  }
}
```

### Sample 2: ਬਜ਼ੁਰਗ ਆਦਮੀ (Elder Male)
```json
{
  "character": "ਬਜ਼ੁਰਗ",
  "text": "ਮੈਂ ਤੁਹਾਨੂੰ ਇੱਕ ਪੁਰਾਣੀ ਕਹਾਣੀ ਸੁਣਾਉਂਦਾ ਹਾਂ",
  "voice_settings": {
    "pitch": 0.75,
    "speed": 0.85,
    "volume": 0.9
  }
}
```

### Sample 3: ਜਵਾਨ ਮੁੰਡਾ (Young Adult)
```json
{
  "character": "ਅਮਨਦੀਪ",
  "text": "ਮੈਂ ਖੇਤੀ ਬਾੜੀ ਕਰਦਾ ਹਾਂ",
  "voice_settings": {
    "pitch": 0.90,
    "speed": 1.0,
    "volume": 1.0
  }
}
```

## 🔧 ਕੋਡ ਵਿੱਚ ਲਾਗੂ ਕਰੋ

### master_builder.py ਵਿੱਚ ਬਦਲਾਅ:

```python
# Character profiles ਸ਼ੁਰੂ ਵਿੱਚ ਜੋੜੋ:
character_profiles = {
    "ਰਚਨਾ": {
        "age": "adult",
        "gender": "male",
        "voice_pitch": 0.85,  # ✓ Mature male voice
        "voice_speed": 0.95,
        "emotion": "narrator"
    }
}

# TTS generation ਵਿੱਚ ਵਰਤੋ:
def generate_single_tts(idx, dialogue):
    char_name = dialogue.get('character', 'Narrator')
    
    # ✓ Profile ਲੋਡ ਕਰੋ
    if char_name in character_profiles:
        profile = character_profiles[char_name]
        pitch = profile['voice_pitch']  # 0.85
        speed = profile['voice_speed']  # 0.95
        
        log.info(f"🧠 {char_name}: age={profile['age']}, "
                 f"pitch={pitch:.2f}x, speed={speed:.2f}x")
```

## 📝 ਨੋਟ ਸਟੂਡੀਓ ਬ੍ਰੇਨ ਲਈ

### ਸਿੱਖੀਆਂ ਗੱਲਾਂ:
1. **gTTS default = ਬੱਚੇ ਵਰਗੀ ਆਵਾਜ਼** ❌
2. **Pitch 0.85 = ਬਾਲਗ ਮਰਦ** ✓
3. **Pitch 0.75 = ਬਜ਼ੁਰਗ** ✓
4. **Speed 0.90-0.95 = ਸਾਫ਼ ਕਹਾਣੀ** ✓

### ਅਗਲੇ ਕਦਮ:
1. Character profiles JSON file ਬਣਾਓ
2. Master builder ਨੂੰ profiles ਲੋਡ ਕਰਨ ਦਿਓ
3. ਹਰ character ਲਈ ਵੱਖਰੀ voice
4. Age/emotion ਮੁਤਾਬਕ pitch ਬਦਲੋ

---

**ਯਾਦ ਰੱਖੋ**: ਜਿੰਨਾ ਘੱਟ pitch (0.75-0.85), ਓਨੀ ਗੂੜੀ/mature ਆਵਾਜ਼!
