"""Generate all shots with FLUX.1-schnell on MLX. Loads the model once."""
import os, sys, time
from mflux.models.flux.variants.txt2img.flux import Flux1
from mflux.models.common.config import ModelConfig
from prompts import SHOTS, STYLE, NEG

W, H, STEPS = 1920, 800, 4          # 2.4:1 anamorphic; schnell is a 4-step model
OUT = "shots"
os.makedirs(OUT, exist_ok=True)

only = sys.argv[1:] or list(SHOTS)

from huggingface_hub import snapshot_download

# BFL's own repo is gated; this is the same weights, pre-quantised for mflux and ungated.
MODEL = snapshot_download("dhairyashil/FLUX.1-schnell-mflux-4bit",
                          allow_patterns=["*.json", "*.safetensors", "*.txt", "*.model"])

print("loading FLUX.1-schnell (4-bit)…", flush=True)
t0 = time.time()
flux = Flux1(model_config=ModelConfig.from_name(model_name="schnell"), model_path=MODEL)
print(f"model ready in {time.time()-t0:.0f}s", flush=True)

for name in only:
    path = f"{OUT}/{name}.png"
    if os.path.exists(path):
        print(f"skip {name}", flush=True)
        continue
    prompt, seed = SHOTS[name]
    t = time.time()
    img = flux.generate_image(
        seed=seed,
        prompt=f"{prompt}. {STYLE}",
        negative_prompt=NEG,
        width=W, height=H,
        num_inference_steps=STEPS,
        guidance=0.0,
    )
    img.save(path=path)
    print(f"{name:14s} {time.time()-t:6.1f}s -> {path}", flush=True)

print("done", flush=True)
