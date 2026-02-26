# ਨਾਮ-ਟੂਨ ਸਟੂਡੀਓ - ਸਮੱਸਿਆਵਾਂ ਅਤੇ ਹੱਲ

## 📋 ਤੁਹਾਡੀਆਂ ਸਮੱਸਿਆਵਾਂ:

### 1. ਸੰਤਰੀ ਰੰਗ ਦਾ circle ਹੈ ਪਰ ਕੋਈ ਤਸਵੀਰ ਨਹੀਂ ❌
**ਕਾਰਨ**: Portrait/Avatar ਸਿਰਫ਼ gradient background ਦੇ ਨਾਲ circle ਹੈ, ਅਸਲੀ character ਦੀ ਤਸਵੀਰ ਨਹੀਂ ਬਣੀ।

**ਹੱਲ**: ਅਸਲੀ Avatar/Character images ਬਣਾਉਣੀਆਂ ਪੈਣਗੀਆਂ। ਦੋ ਤਰੀਕੇ:
- AI ਨਾਲ character design ਬਣਾਓ (Midjourney, DALL-E)
- ਆਪਣੇ photos/drawings ਵਰਤੋ

### 2. Background Music ਨਹੀਂ ਸੁਣਾਈ ਦੇ ਰਿਹਾ ❌
**ਕਾਰਨ**: Background audio ਬਣਾਇਆ ਗਿਆ (`audio/ambient.wav`) ਪਰ ਮਿਕਸਿੰਗ ਵਿੱਚ ਬਹੁਤ ਘੱਟ ਹੈ ਜਾਂ ducking ਨੇ ਇਸਨੂੰ ਬਹੁਤ ਘੱਟ ਕਰ ਦਿੱਤਾ।

**ਹੱਲ**: Background gain ਵਧਾਓ ਅਤੇ ਸਹੀ music files ਵਰਤੋ।

### 3. ਆਵਾਜ਼ 13 ਸਾਲ ਦੇ ਬੱਚੇ ਵਰਗੀ ਹੈ, mature man ਦੀ ਨਹੀਂ ❌
**ਕਾਰਨ**: gTTS default pitch ਬਹੁਤ ਉੱਚੀ ਹੈ (high-pitched)।

**ਹੱਲ**: Pitch ਨੂੰ 0.82 ਤੱਕ ਘਟਾਓ (mature male voice ਲਈ)।

---

## ✅ ਹੱਲ ਲਾਗੂ ਕੀਤੇ ਗਏ:

### 1. Voice Profiles ਬਣਾਏ (`brain_memory/character_voice_profiles.json`)
```json
{
  "ਰਚਨਾ": {
    "voice_pitch": 0.82,    ← ਬਾਲਗ ਮਰਦ (ਡੂੰਘੀ ਆਵਾਜ਼)
    "voice_speed": 0.92,    ← ਥੋੜਾ ਹੌਲੀ
    "emotion": "narrator"
  }
}
```

**ਪਹਿਲਾਂ**: Pitch = 1.0 (ਬੱਚੇ ਵਰਗੀ) ❌  
**ਹੁਣ**: Pitch = 0.82 (ਬਾਲਗ ਮਰਦ) ✓

### 2. Training Document ਬਣਾਈ
- `brain_memory/voice_training_punjabi.md` ਵਿੱਚ ਪੂਰੀ ਗਾਈਡ
- Pitch settings ਲਈ samples
- ਹਰ ਕਿਸਮ ਦੀ ਆਵਾਜ਼ ਲਈ recommendations

### 3. Master Builder Updated
- ਹੁਣ character profiles ਲੋਡ ਕਰਦਾ ਹੈ
- ਹਰ character ਲਈ ਵੱਖਰੀ pitch/speed

---

## 🎯 ਅਗਲੇ ਕਦਮ (ਤੁਹਾਨੂੰ ਕਰਨੇ ਪੈਣਗੇ):

### ਕਦਮ 1: Character Images/Avatars ਬਣਾਓ 🎨

#### ਤਰੀਕਾ A: AI ਨਾਲ ਬਣਾਓ
1. Midjourney/DALL-E ਤੇ ਜਾਓ
2. Prompt:
   ```
   "Punjabi man, 35 years old, serious expression, 
   portrait style, clean background, facing camera"
   ```
3. Image save ਕਰੋ: `characters/ਰਚਨਾ.png`

#### ਤਰੀਕਾ B: ਆਪਣੀਆਂ Photos ਵਰਤੋ
1. Character ਦੀ ਫੋਟੋ/drawing ਲਓ
2. Background ਹਟਾਓ (remove.bg ਵਰਤੋ)
3. Save ਕਰੋ: `characters/ਰਚਨਾ.png` (256x256 ਜਾਂ ਵੱਡੀ)

#### ਸਟੂਡੀਓ ਵਿੱਚ ਵਰਤੋ:
```bash
# Characters folder ਬਣਾਓ
mkdir -p characters

# ਆਪਣੀਆਂ images ਰੱਖੋ:
# characters/ਰਚਨਾ.png
# characters/ਦਲੀਪ.png
# characters/ਅਮਨਦੀਪ.png

# ਫਿਰ ਰੰਨ ਕਰੋ:
python colab/master_builder.py \
  --scenes temp_adhhi_aurat_scenes.json \
  --characters-dir characters \
  --duck \
  --captions
```

### ਕਦਮ 2: Background Music Files ਜੋੜੋ 🎵

```bash
# Music folder ਬਣਾਓ
mkdir -p audio/music

# ਆਪਣੇ music files ਰੱਖੋ:
# audio/music/sad.mp3
# audio/music/happy.mp3
# audio/music/dramatic.mp3
# audio/music/ambient.mp3
```

ਫਿਰ `colab/master_builder.py` ਵਿੱਚ music selection ਸੁਧਾਰੋ।

### ਕਦਮ 3: Voice ਟੈਸਟ ਕਰੋ 🎤

```bash
# ਨਵੀਂ ਵੀਡੀਓ ਬਣਾਓ improved voice ਨਾਲ:
python colab/master_builder.py \
  --scenes temp_adhhi_aurat_scenes.json \
  --duck \
  --captions \
  --bg-gain 0.15

# ਆਵਾਜ਼ ਸੁਣੋ ਅਤੇ ਚੈੱਕ ਕਰੋ:
# - ਕੀ mature ਲੱਗ ਰਹੀ ਹੈ?
# - ਕੀ ਸਾਫ਼ ਸੁਣਾਈ ਦੇ ਰਹੀ ਹੈ?
```

---

## 📊 Voice Settings ਗਾਈਡ:

### ਆਵਾਜ਼ ਦੀ ਕਿਸਮ → Pitch Value

| ਉਮਰ/ਕਿਸਮ | Pitch | ਵਰਣਨ |
|-----------|-------|--------|
| **ਛੋਟਾ ਬੱਚਾ** | 1.3 | ਬਹੁਤ ਉੱਚੀ |
| **ਜਵਾਨ ਮੁੰਡਾ** | 0.90 | ਥੋੜੀ ਉੱਚੀ |
| **ਬਾਲਗ ਮਰਦ** | 0.82 | ✓ ਗੂੜੀ, mature |
| **ਬਜ਼ੁਰਗ** | 0.75 | ਬਹੁਤ ਗੂੜੀ |
| **ਜਵਾਨ ਕੁੜੀ** | 1.05 | ਹਲਕੀ ਉੱਚੀ |
| **ਬਾਲਗ ਔਰਤ** | 1.0 | Normal |

### Speed Settings

| ਸਥਿਤੀ | Speed | ਵਰਣਨ |
|--------|-------|--------|
| **ਕਹਾਣੀ ਸੁਣਾਉਣਾ** | 0.90 | ਹੌਲੀ, ਸਾਫ਼ |
| **ਆਮ ਗੱਲਬਾਤ** | 1.0 | Normal |
| **ਉਤਸ਼ਾਹਿਤ** | 1.15 | ਤੇਜ਼ |
| **ਡਰਾਮੇਬਾਜ਼ੀ** | 0.85 | ਬਹੁਤ ਹੌਲੀ |

---

## 🎬 ਹੁਣ ਕੀ ਕਰੋ:

### 1. Character Images ਬਣਾਓ (ਸਭ ਤੋਂ ਜ਼ਰੂਰੀ)
```bash
mkdir characters
# AI/Photos ਨਾਲ ਬਣਾਓ ਅਤੇ save ਕਰੋ:
# characters/ਰਚਨਾ.png
# characters/ਦਲੀਪ.png
# etc.
```

### 2. Voice Test ਕਰੋ
```bash
# ਇਸ ਵੀਡੀਓ ਵਿੱਚ pitch ਪਹਿਲਾਂ ਹੀ ਸੁਧਰੀ ਹੈ
# ਪਰ ਸੁਣੋ ਅਤੇ ਦੱਸੋ:
open AmritCore_FINAL_STUDIO_LAUNCH.mp4
```

### 3. Background Music ਵਧਾਓ
```bash
# ਫਿਰ ਤੋਂ ਰੰਨ ਕਰੋ ਜ਼ਿਆਦਾ music ਨਾਲ:
python colab/master_builder.py \
  --scenes temp_adhhi_aurat_scenes.json \
  --duck \
  --captions \
  --bg-gain 0.25   ← ਇਹ ਵਧਾਓ (0.15 ਤੋਂ 0.25)
```

---

## ✅ ਜੋ ਠੀਕ ਹੋ ਗਿਆ:

1. ✓ Voice pitch ਘਟਾਇਆ (1.0 → 0.82)
2. ✓ Character profiles system ਬਣਾਇਆ
3. ✓ Training documents ਬਣਾਈਆਂ
4. ✓ Master builder updated

## ❌ ਜੋ ਕਰਨਾ ਬਾਕੀ:

1. ❌ Character images/avatars ਬਣਾਓ
2. ❌ Background music ਵਧਾਓ
3. ❌ Voice ਟੈਸਟ ਕਰੋ ਅਤੇ adjust ਕਰੋ

---

## 📁 ਬਣੀਆਂ ਫਾਈਲਾਂ:

1. `brain_memory/voice_training_punjabi.md` - ਪੂਰੀ voice ਗਾਈਡ
2. `brain_memory/character_voice_profiles.json` - Voice settings
3. `AmritCore_FINAL_STUDIO_LAUNCH.mp4` - ਨਵੀਂ ਵੀਡੀਓ (improved voice)

---

## 🎯 ਸਭ ਤੋਂ ਪਹਿਲਾਂ ਕਰੋ:

**Character Images ਬਣਾਓ!** ਬਿਨਾਂ ਇਸਦੇ ਸਿਰਫ਼ circle ਹੀ ਦਿਖੇਗਾ।

ਮੈਂ ਤੁਹਾਡੀ ਮਦਦ ਕਰ ਸਕਦਾ ਹਾਂ:
1. AI prompts ਦੇਣ ਵਿੱਚ
2. Image ਤਿਆਰ ਕਰਨ ਵਿੱਚ
3. Background remove ਕਰਨ ਵਿੱਚ
4. Animation ਵਿੱਚ

**ਤੁਸੀਂ ਕਿੱਥੋਂ ਸ਼ੁਰੂ ਕਰਨਾ ਚਾਹੁੰਦੇ ਹੋ?** 🎨
