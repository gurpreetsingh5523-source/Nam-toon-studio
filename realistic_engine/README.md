# THE FORTY-FOURTH

A 4m26s narrated hard-sci-fi short, built end to end from the Breath Empire script.
**Everything runs locally on the M5 — no cloud, no paid API, no stock footage.**

    ./make.sh          # full build, resumable (skips any stage whose output exists)

Output: `out/THE_FORTY_FOURTH.mp4` — 1920×1080, 24fps, 2.4:1 anamorphic letterbox,
h264 CRF 16, AAC 256k, −14.7 LUFS integrated (streaming standard).

## Pipeline

| Stage | File | Model / method | Cost |
|---|---|---|---|
| Narration | `tts.py` | Piper — `ryan-high` (host 1) / `lessac-high` (host 2) | ~1 min |
| Imagery | `gen_shots.py` | FLUX.1-schnell 4-bit via mflux (MLX/Metal) | ~2.5 min per shot |
| Depth | `depth.py` | Apple DepthPro (bundled with mflux) | ~6s per shot |
| Camera | `camera_mlx.py` | 2.5D depth parallax + anamorphic bloom, grain, gate weave | 35 ms/frame |
| Score | `score.py` | procedural synthesis — drones, sub pulses, braams, risers | 3s |
| Type | `titles.py` | PIL (Avenir Next), letterbox-bar captions | — |
| Render | `render.py` | one continuous frame stream → ffmpeg, real dissolves | ~9 min |
| Mix | `assemble.py` | narration + sidechain-ducked score, loudnorm | ~1 min |

Total cold build ≈ 1h (dominated by the 17 FLUX shots).

## Why it's built this way

**No stills-slideshow.** Each shot is a FLUX still driven by a virtual camera: DepthPro
gives a depth map, and `camera_mlx.py` inverse-warps every frame with depth-scaled
parallax, so foreground and background separate as the camera moves. On top of that
sit anamorphic bloom, chromatic aberration, vignette, a filmic curve and animated
grain — the grade is what makes a still read as photography.

**MLX, not numpy.** The identical numpy implementation in `camera.py` runs at 657
ms/frame; the MLX port is 35 ms — 19× — which turns a 95-minute render into 9. Both
produce the same image (verified: 0.007 mean abs diff, i.e. grain only). `camera.py`
is kept as the readable reference and CPU fallback.

**Timing is derived, not guessed.** `tts.py` synthesises each sentence separately and
records its exact duration, so `timings.json` drives shot lengths, caption timings and
the score's act boundaries. Nothing is hand-tuned to fit.

## Environment gotchas (all worked around in the code)

- **This ffmpeg has no libass and no drawtext.** All type is rendered in PIL and
  composited into the frame before encode. Don't reach for `subtitles=` / `drawtext=`.
- **`black-forest-labs/FLUX.1-schnell` is gated** and this HF account isn't authorised.
  We pull `dhairyashil/FLUX.1-schnell-mflux-4bit` — same Apache-2.0 weights, already in
  mflux's 4-bit format, ungated.
- **Coqui TTS is installed under Python 3.9 and is broken there** (a dependency uses
  3.10+ syntax). Hence the Python 3.12 venv and Piper.
- `sidechaincompress` ends with its key input — the sidechain branch needs `apad` or
  the mix gets truncated to the narration.
- numpy 2.x removed `ndarray.ptp()`; use `np.ptp(x)`.

## Known limitation

FLUX renders lettering as gibberish, so hull markings in a couple of wide shots are
nonsense glyphs. They're small and in soft focus. Prompting them away isn't reliable;
the fix if it ever matters is inpainting those regions.

## Editing

- Change the words → `script.py`, then delete `timings.json` and rerun `./make.sh`.
- Change a shot → edit its prompt/seed in `prompts.py`, `rm shots/<name>.png depth/<name>.png`, rerun.
- Change the camera move on a shot → `MOVE` dict in `render.py`.
- Change the music → `score.py` (`acts` list sets the harmonic centre and mood per act).
