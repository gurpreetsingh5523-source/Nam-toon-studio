# Motion / character-action — status & roadmap

## Kਮਮ ki hੋਇਆ (2026-07)
Motion engine **poora ban ke wired hੈ** — sਿਰਫ਼ is 16GB M5 te AI-video model chੱਲ
nahੀਂ sਕਿਆ. Do vੱਖਰੀਆਂ gੱਲਾਂ ne, rਲਾਓ nਾ:

| Chੀਜ਼ | Haਲਤ |
|---|---|
| Pipeline / wiring (`i2v.py`, `clip_shot.py`, `render.py`, `make.sh`) | ✅ taਿਆਰ, sਹੀ code |
| Is machine te AI-video model chੱਲਣਾ | ❌ 16GB M5 + Metal/torch 2.13 te fail |

`clips/<shot>.mp4` mੌਜੂਦ hੋਵੇ → oh shot **AI motion** vਰਤਦਾ hੈ; nਾ hੋਵੇ → 2.5D camera.
So jਿੱਦਣ clips bਣ gਏ (kਿਸੇ vੀ machine te), movie apਣੇ-aap upgrade hੋ jਾਵੇਗੀ — hੋਰ
kੁਝ nahੀਂ bਦਲਣਾ.

## Kੀ test kੀਤਾ te kੀ nਿਕਲਿਆ (imਾਨਦਾਰ record)

**Stable Video Diffusion (SVD-XT)** — 16GB layi best choice (koi 19GB T5 nahੀਂ,
image-conditioned). Download OK (~4.5GB fp16). Par chalaਉਣ te:
- `fp16` on MPS → frames **corrupt** (chਿੱਟੇ + peele blocks; NaN overflow).
- `fp16 UNet + fp32 VAE` → MPS matmul **assert** (mixed dtype allowed nahੀਂ).
- `fp32` poori pipeline → code clean chੱਲਿਆ par frames **fਿਰ vੀ corrupt**, te
  **~43 min per 8-frame clip**, swap 22GB. Yਾਨੀ dtype di nahੀਂ — **is torch/Metal
  build te SVD de temporal-attention/VAE kernels hੀ galat** ne.

**LTX-Video (2B)** — text-to/i2v, changੀ motion, par T5-XXL text-encoder **19GB** —
oh ikੱਲਾ 16GB RAM tੋਂ vੱਧ. Har shot da vੱਖ prompt = T5 vਾਰ-vਾਰ swap. Practical nahੀਂ.

**Nਤੀਜਾ:** is 16GB M5 te **local photoreal AI-video aਜੇ viable nahੀਂ** — na sਿਰਫ਼
hੌਲੀ, sਗੋਂ output vੀ kharab. 2.5D camera (jੋ film vich pਹਿਲਾਂ tੋਂ hੈ) hੀ asli local
motion hੈ.

## Aglੇ raah (jੋ sਚਮੁੱਚ kੰਮ karਨਗੇ)

1. **Cloud GPU burst (sਸਤਾ, hੁਣੇ chੱਲੇਗਾ).** ਕੋਈ NVIDIA GPU (RunPod/Vast/Lambda,
   ~$0.4–1/hr). `i2v.py` jਿਵੇਂ da tਿਵੇਂ CUDA te chੱਲਦਾ hੈ — 17 clips ~1 ghੰਟੇ vich.
   Clips vਾਪਸ `clips/` vich pਾਓ, `./make.sh` — motion movie taਿਆਰ. **Sਿਫ਼ਾਰਸ਼.**
2. **Naveen Mac / ≥24GB.** Ohੀ `i2v.py`, MPS theek hੋਵੇ tਾਂ local.
3. **AnimateDiff (SD1.5)** — MPS te bharੋਸੇਯੋਗ chੱਲਦਾ, par SD1.5 quality (sਾਡੇ FLUX
   stills naal mel nahੀਂ khਾਂਦਾ). Backup vਿਕਲਪ.
4. **Paid i2v API** (Runway / Kling / Luma) — vਧੀਆ character motion, par cloud +
   paisੇ; sਾਡਾ local rੁਖ਼ tੋੜਦਾ. Nano-banana = image edit, video nahੀਂ.

## Character action (turਨਾ-larਨਾ, lip-sync) — sੱਚ
Koi vੀ **local** model 16GB te vਧੀਆ character-fighting motion bharੋਸੇ naal nahੀਂ
dੇਂਦਾ. Oਹ level cloud i2v (Runway/Kling) ja vੱਡੀ GPU mੰਗਦਾ hੈ. Sਾਡਾ pipeline oਸ layi
vੀ taਿਆਰ hੈ — bੱਸ `clips/` bhਰਨੇ ne.
