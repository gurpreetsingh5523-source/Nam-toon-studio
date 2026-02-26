# Nam-toon Studio 🎬

**Intelligent story-to-video pipeline with Punjabi language support**

Transform your stories (Punjabi/English text) into animated videos with **automatic intelligence** that understands character age, gender, emotion, and scene mood.

---

## 🧠 Intelligent Brain System (7 Creative Systems)

The studio now **thinks like a film director** with advanced creative logic:

### ✅ **Voice Modulation** (Age/Gender/Emotion)
- **Age detection**: Child (high pitch, fast), Adult (normal), Elder (low pitch, slow)
- **Gender detection**: Female (+15% pitch), Male (-10% pitch)
- **Emotion detection**: Happy (uplifting), Sad (slow), Angry (aggressive), Fearful (urgent)

### ✅ **Scene Emotion Analysis**
- Detects scene mood from keywords (Punjabi + English)
- **Happy**: ਖੁਸ਼, ਹੱਸ → birds.wav (bright, 4/4 rhythm)
- **Sad**: ਦੁੱਖ, ਉਦਾਸ → rain.wav (waltz, 3/4 rhythm)
- **Tragic**: ਮੌਤ, ਅੱਗ → strings.wav (dissonant, sustained)
- **Tense**: ਡਰ, ਪੁਲਿਸ → heartbeat.wav (irregular, pulsing)

### ✅ **Behavior Detection** (12 Actions)
- **Emotional**: crying, laughing, shouting, whispering
- **Physical**: walking, running, sitting, standing
- **Cultural**: prayer (ਅਰਦਾਸ), farming (ਖੇਤ), celebration (ਜਸ਼ਨ), mourning (ਸੋਗ)
- **Effect**: Camera adapts to character actions

### ✅ **Rhythm Analysis** (Dialogue Pacing)
- **Pattern**: steady, varied, dynamic
- **Pace**: rapid (<30 chars), normal (30-80), slow (>80)
- **Effect**: Controls scene timing and pause durations

### ✅ **Camera Intelligence** (Auto-Cinematography)
- **7 camera types**: smooth_pan, slow_zoom, static_close, shaky_zoom, handheld, drift, steady
- **FOV adjustment**: 60° (wide) to 35° (tight) based on intensity
- **Behavior override**: Tracking shots for walking, static holds for prayer

### ✅ **Cross-Scene Learning** (Story Arc Awareness)
- **Emotional distance**: Measures transition intensity (0.0-1.0)
- **Transition types**: continuation, shift, dramatic_turn
- **Effect**: Suggests hard cuts vs crossfades

### ✅ **Self-Learning Memory** (Continuous Improvement)
- Tracks character patterns, timing preferences, transition effectiveness
- **12 behaviors** + learns new actions automatically
- **Memory**: Character profiles, rhythm patterns, emotional arcs

📖 **Full documentation**: 
- Basic features: [BRAIN_SYSTEM.md](BRAIN_SYSTEM.md)
- **Creative features**: [CREATIVE_BRAIN.md](CREATIVE_BRAIN.md) ⭐

---

## 🚀 Quick Start

### Install Dependencies
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Generate Video from Story
```bash
# 1. Convert story text to structured scenes
python colab/novel_pipeline.py novel.txt

# 2. Render video with intelligent brain
python colab/master_builder.py \
  --scenes colab/scenes.json \
  --captions \
  --timecode \
  --output MyStory.mp4

# Brain will automatically:
# - Analyze character age/gender/emotion
# - Detect scene moods
# - Apply voice modulation (pitch/speed)
# - Select appropriate background music
# - Choose animation style
```

---

## 📁 Project Structure

```
Nam-toon-studio/
├── colab/
│   ├── intelligent_brain.py   # 🧠 Brain logic (character/emotion analysis)
│   ├── master_builder.py      # Video renderer (integrates brain)
│   ├── novel_pipeline.py      # Text → scenes.json converter
│   ├── scenes.json            # Structured scene data
│   └── fast_tts.py            # Parallel TTS system
├── Core/                      # Legacy brain nodes
│   ├── 19_ultimate_brain_logic.py
│   └── ...
├── novel.txt                  # Your story (Punjabi/English)
├── BRAIN_SYSTEM.md            # Detailed brain documentation
└── README.md                  # This file
```

---

## 🎭 Example: Brain Analysis

### Input Story (novel.txt)
```
ਕੁਲਵੰਤ ਬੋਲਦਾ ਹੈ:
"ਅਮਨਦੀਪ ਇੱਕ ਖੁਸ਼ ਬੱਚਾ ਸੀ। ਉਹ ਹਮੇਸ਼ਾ ਹੱਸਦਾ ਰਹਿੰਦਾ ਸੀ।"

ਪਰ ਫਿਰ ਇੱਕ ਦਿਨ ਅੱਗ ਲੱਗ ਗਈ। ਦਲਜੀਤ ਕੌਰ ਬਹੁਤ ਗੁੱਸੇ ਵਿੱਚ ਸੀ।
```

### Brain Output
```
🧠 Activating Intelligent Brain for scene analysis...
  Scene 0 (ਸ਼ੁਰੂਆਤ): happy (0.40) → birds.wav
  Scene 1 (ਹਾਦਸਾ): tragic (1.00) → strings.wav

🧠 ਕੁਲਵੰਤ (Narrator):
  age=adult, gender=male, emotion=calm
  voice: pitch=0.97x, speed=1.10x

🧠 ਅਮਨਦੀਪ:
  age=young_adult, gender=female, emotion=calm
  voice: pitch=1.37x, speed=1.16x

🧠 ਦਲਜੀਤ ਕੌਰ:
  age=adult, gender=female, emotion=angry
  voice: pitch=1.21x, speed=1.15x
```

---

## 🛠️ Features

### Video Generation
- ✅ Punjabi TTS (gTTS) with voice modulation (ffmpeg pitch/speed)
- ✅ Parallel TTS rendering (5x faster than serial)
- ✅ Avatar generation (colored circles with initials)
- ✅ Ken Burns animation (zoom/pan)
- ✅ Captions and timecode overlay
- ✅ Scene-based background music
- ✅ Audio normalization and ducking

### Pipeline
- ✅ Text → Scenes converter (novel_pipeline.py)
- ✅ Punjabi character extraction (Gurmukhi script)
- ✅ Smart dialogue assignment (narrator vs character)
- ✅ Scene emotion keywords (happy/sad/tragic/tense/angry/peaceful)

### Brain Intelligence
- ✅ Character age/gender/emotion detection
- ✅ Voice pitch/speed modulation
- ✅ Scene emotion analysis (Punjabi + English keywords)
- ✅ Background music selection (7 emotion types)
- ✅ Animation style decisions

---

## 📊 Supported Languages

- **Primary**: Punjabi (ਪੰਜਾਬੀ) — Gurmukhi script
- **Secondary**: English — For mixed-language stories

---

## 🔧 Advanced Usage

### Render with Custom Limits
```bash
# Render only first 3 scenes (faster testing)
python colab/master_builder.py --scenes colab/scenes.json --scenes-limit 3 --captions --output Test3.mp4
```

### Dry-Run (Check Logic Without Rendering)
```bash
# See brain analysis without video generation
python colab/master_builder.py --scenes colab/scenes.json --dry-run
```

### Test Brain Standalone
```bash
cd colab
python intelligent_brain.py
```

---

## 📝 PWA (Web App)

The studio also includes a PWA for recording and playback:

### Files
- `index.html`, `styles.css`, `app.js`
- `manifest.json`, `sw.js` (service worker)
- `icons/` (192x192, 512x512 SVG)

### Run Locally
```bash
python3 -m http.server 8000
# Open http://localhost:8000
```

### Deploy to GitHub Pages
1. Push to `main` branch
2. Enable Pages in Settings → Pages → Deploy from branch
3. Access at `https://<username>.github.io/<repo>/`

### Install on iPad/iPhone
Open in Safari → Share → Add to Home Screen

---

## 🎓 How the Brain Works

1. **Character Analysis**
   - Reads character names (ਕੌਰ = female, ਸਿੰਘ = male)
   - Detects age from keywords (ਬੱਚਾ = child, ਬੁੱਢਾ = elder)
   - Identifies emotion from dialogue (ਗੁੱਸਾ = angry, ਦੁੱਖ = sad)

2. **Scene Emotion**
   - Scans text for emotion keywords
   - Counts matches and calculates intensity
   - Selects music based on dominant emotion

3. **Voice Modulation**
   - Generates base TTS (gTTS Punjabi)
   - Applies pitch shift via ffmpeg `asetrate`
   - Applies speed change via ffmpeg `atempo`

4. **Animation Style**
   - Maps emotion → movement type (gentle/intense/chaotic)
   - Adjusts zoom speed (0.7x peaceful → 1.5x angry)
   - Chooses pan direction (up=happy, down=sad)

**See full details**: [BRAIN_SYSTEM.md](BRAIN_SYSTEM.md)

---

## 🤝 Contributing

This studio is designed for **logical, responsible AI-driven storytelling**. Contributions welcome:

- Improve character detection (NER for Punjabi names)
- Add more emotion keywords
- Enhance animation variety
- Support more languages

---

## 📄 License

Open source. Use responsibly.

---

## 🙏 Philosophy

> "The studio should **think like a director** — understanding character, emotion, and pacing automatically."

**ਵਾਹਿਗੁਰੂ ਜੀ ਕਾ ਖਾਲਸਾ, ਵਾਹਿਗੁਰੂ ਜੀ ਕੀ ਫਤਹਿ!**
