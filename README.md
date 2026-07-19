# 🎬 Nam Toon Studio — Advanced AI Storyboard & Video NLE Suite

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100.0%2B-009688.svg)](https://fastapi.tiangolo.com/)

**Nam Toon Studio** is a premium, open-source AI-assisted storyboarding and non-linear video editing (NLE) suite. It transforms script writing and story production into a streamlined, one-click automated process. Featuring a sleek CapCut-inspired glassmorphic interface, multi-track audio mixing, fader keyframing, and automated Python video compilation.

---

## ✨ Features

### 1. 📺 AI Preview Monitor & Premium UI
- **Auto-Scrolling Chat Roll**: Central AI brainstorming room where you can discuss script details with the AI model. Chats automatically slide upwards as new plot lines are added.
- **Modern NLE Theme**: Styled in high-contrast dark space colors (`#07080b`), with glassy frosted borders, and vibrant electric blue buttons.
- **Polished Typography**: Rendered in clean Google Fonts Inter typeface.

### 2. 💎 Advanced Multi-Track Timeline
- **8-Track Professional Layout**:
  - `Scene Background` (set custom backgrounds or presetted vector scenes)
  - `Krishna` (character lane)
  - `Sultan` (character lane)
  - `Dialogues` (mapped script speaking text blocks)
  - `Text Overlay` (for captions and text graphics)
  - `Transitions` (scene transitions)
  - `SFX` (sound effect overlays)
  - `BGM` (background music loops)
- **Fader Keyframing (💎)**: Add keyframe fader nodes directly on track headers to create custom volume fade-ins and fade-outs.
- **Voiceover Recorder**: Select a track, record via microphone, type a script, and it splits/inserts the dialogue block precisely at the active playhead time.

### 3. 🤖 AI Assets Studio
- **🤖 AI Character Creator**: Type prompts (e.g. *"Young girl in a farm"*) to instantly generate new character profiles and spin up timeline lanes.
- **🏞️ AI Background Generator**: Generate custom preset background settings on-the-fly.

### 4. ⚡ One-Click AI Post-Production Compiler
Powered by a backend FastAPI server and the **MoviePy** editing framework:
- **Auto-Generated Subtitles**: Overlays speaker badges and Gurmukhi captions dynamically on render.
- **Volume Interpolation**: Dynamically computes linear curves based on keyframes.
- **AI Color Grading (LUTs)**: Select standard feed, cinematic contrast, sepia sunset glow, or vintage B&W filters to instantly transform video rendering.

---

## 🚀 Quick Start Guide

### Prerequisites
Make sure you have Python 3.8+ installed on your system.

### 1. Install Dependencies
```bash
# Clone the repository
git clone https://github.com/gurpreetsingh5523-source/Nam-toon-studio.git
cd Nam-toon-studio

# Create virtual environment and install packages
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Launch local server
```bash
python3 -m uvicorn server:app --host 127.0.0.1 --port 8000
```
Open **`http://127.0.0.1:8000`** in your web browser.

---

## 🛠️ Tech Stack
- **Frontend**: Vanilla Javascript (ES6), HTML5, Canvas API, CSS Variables, PWA Offline Service Workers.
- **Backend**: FastAPI (Python), Uvicorn.
- **Video Engine**: MoviePy, PIL (Pillow), NumPy, Wave.

---

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
