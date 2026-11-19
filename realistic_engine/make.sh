#!/bin/bash
# THE FORTY-FOURTH — full build. Everything runs locally; no cloud, no paid APIs.
set -e
cd "$(dirname "$0")"
PY=./venv/bin/python

echo "▸ 1/5  narration  (Piper TTS, 2 voices)"
[ -f timings.json ] || $PY tts.py

echo "▸ 2/5  shots      (FLUX.1-schnell 4-bit on MLX)"
$PY gen_shots.py

echo "▸ 3/6  depth      (Apple DepthPro)"
$PY depth.py

echo "▸ 4/6  score      (procedural synthesis)"
[ -f audio/score.wav ] || $PY score.py

# OPTIONAL motion upgrade: any clips/<name>.mp4 is used instead of the 2.5D camera for
# that shot. Create them with:  ./venv/bin/python i2v.py <shot names>   (Stable Video Diffusion)
echo "▸ 5/6  motion     ($(ls clips/*.mp4 2>/dev/null | wc -l | tr -d ' ') shot(s) upgraded to SVD video; rest use 2.5D camera)"

echo "▸ 6/6  render     (motion clips where present, else 2.5D camera + titles, then mix)"
$PY render.py
$PY assemble.py

echo
echo "✓ out/THE_FORTY_FOURTH.mp4"
