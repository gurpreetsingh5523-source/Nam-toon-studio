Setup & run — Nam-toon-studio (macOS / zsh)

This file explains how to set up a reproducible Python environment and run the studio builder `colab/master_builder.py`.

Prerequisites
- Python 3.10+ (system Python or pyenv). A virtual env was used for development.
- ffmpeg installed and on PATH (moviepy requires ffmpeg).
  - Install via Homebrew: `brew install ffmpeg`

Quick setup (copy & paste into your zsh terminal from repo root)

1) Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2) Upgrade pip and install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

3) Run the master builder script

```bash
# from repo root
python colab/master_builder.py
```

Notes and troubleshooting
- ffmpeg: If moviepy raises an ffmpeg error, ensure `ffmpeg` is installed and in your PATH. Test with `ffmpeg -version`.
- Virtual environment path: We use `.venv` in this project (recommended). Use the absolute venv python if needed:
  - `.venv/bin/python colab/master_builder.py`
- Pillow + MoviePy: Older code used `Image.ANTIALIAS` which is removed in recent Pillow; the builder has a compatible implementation, so you shouldn't hit that error.
- pydub: If you get errors importing pydub related to `audioop` / `pyaudioop` on newer Python versions, it can be worked around (we avoided pydub for critical paths). If you need pydub features, use Python 3.11 or install a compatible helper.

Outputs
- `audio/` — generated TTS files and temporary audio assets
- `images/` — scene base image(s)
- `assets/animation/` — temporary animation clips
- `AmritCore_FINAL_STUDIO_LAUNCH.mp4` — final assembled demo (video + audio)

Next recommended steps
- Add a `--dry-run` / `--verbose` flag to `colab/master_builder.py` for easy CI smoke tests (I can add this).
- Add a small GitHub Actions workflow (CI) to run a fast smoke test on PRs.

If you'd like, I can now:
- implement `--dry-run` / `--verbose` in `colab/master_builder.py`, or
- scaffold a minimal GitHub Actions workflow that runs a smoke test.
