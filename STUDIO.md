# Nam-toon Studio

Do engine, ikko studio. Sਾਰਾ kuchh **local** chalda hai — koi cloud nahi, koi paid API nahi.

```
Nam-toon-studio/
├── Core/                 ENGINE 1 — cartoon / Punjabi dialogue films (moviepy + gTTS)
├── realistic_engine/     ENGINE 2 — photoreal cinematic films (FLUX + DepthPro + MLX + Piper)   ← NEW
├── movies/               finished films + saved stills
│   └── the_forty_fourth/ pehli realistic movie (4m26s) — video + 17 photos + recipe
└── STUDIO.md             eh file
```

## Engine 1 — `Core/`  (cartoon / dialogue)
Purana pipeline: moviepy + gTTS Punjabi TTS + colour/ImageMagick slides. Krishna/Sultan
warge character dialogue cartoons layi. Isnu badlia nahi gaya — jinven si onven kaayam.

## Engine 2 — `realistic_engine/`  (photoreal — NEW upgrade)
Jehੜਾ system "THE FORTY-FOURTH" banaਨ layi vartia, oh poora ethe hai. Fully local:

| Kamm | Model | Open source |
|---|---|---|
| Awaaz (narration) | Piper TTS | ✓ |
| Tasveeran (17 shots) | FLUX.1-schnell 4-bit (mflux / MLX-Metal) | ✓ Apache-2.0 |
| Depth | Apple DepthPro | ✓ |
| Camera motion | depth-parallax 2.5D (MLX) | ✓ apna code |
| Sੰਗੀਤ (score) | procedural synthesis | ✓ apna code |
| Titles/captions | PIL | ✓ |
| Assembly | ffmpeg | ✓ |

Apna `venv` naal aaunda hai — hor kuchh install karn di lorh nahi.

### Ikk movie banao
```bash
cd realistic_engine
./make.sh          # resumable: jehੜਾ step ho chukka, chad denda hai
# → out/THE_FORTY_FOURTH.mp4
```

### Nਵੀਂ movie banao (naveen code di lorh NAHI)
Sਿਰਫ਼ do file badlo, phir `./make.sh`:
1. `realistic_engine/script.py`  — narration (kinne beat, kehੜਾ host bolda)
2. `realistic_engine/prompts.py` — har shot di photoreal description + seed
3. `rm -f timings.json` (taan ki naveen awaaz banae) te `./make.sh` chalao.

Pੁਰਾਣੀ movie save karn layi: `script.py prompts.py timings.json shots/ out/`
nu `movies/<naam>/` vich copy kar lao (jinven the_forty_fourth vich keeta).

## Abhi ki possible hai, ki nahi
- ✅ **Cinematic narrated films** (jinven the_forty_fourth) — poora local, share-ready mp4.
- ✅ Camera movement, parallax, atmosphere, grade, score, captions.
- ⚠️ **AI motion / character action** — pipeline **ban ke wired hੈ** (`i2v.py` +
  `clip_shot.py`, render.py apਣੇ-aap `clips/<shot>.mp4` vਰਤਦਾ hੈ), par **is 16GB M5 te
  AI-video model chੱਲ nahੀਂ sਕਿਆ**: SVD de temporal kernels is Metal/torch stack te
  corrupt output dੇਂਦੇ ne, te LTX da T5 (19GB) RAM tੋਂ vੱਧ. Jਿੱਦਣ clips kਿਸੇ GPU te
  bਣ gਏ, movie apਣੇ-aap upgrade. Poora tested record + raah: `MOTION_ROADMAP.md`.

## Motion engine — status
Pipeline taਿਆਰ; sਿਰਫ਼ clips chਾਹੀਦੇ ne. Sਭ tੋਂ sਸਤਾ raah = ਕੋਈ **cloud NVIDIA GPU**
te `i2v.py` chਲਾਓ (~1 ghੰਟਾ, 17 clips), clips `clips/` vich pਾਓ, `./make.sh`.
Vੇਰਵਾ: `realistic_engine/MOTION_ROADMAP.md`.
