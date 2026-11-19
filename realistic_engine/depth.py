"""Depth maps for every shot, via Apple DepthPro (bundled with mflux)."""
import os, sys, time
from mflux.models.depth_pro.model.depth_pro import DepthPro
from prompts import SHOTS

os.makedirs("depth", exist_ok=True)
todo = [n for n in (sys.argv[1:] or SHOTS) if not os.path.exists(f"depth/{n}.png")]
if not todo:
    print("all depth maps present"); raise SystemExit

print("loading DepthPro…", flush=True)
dp = DepthPro(quantize=8)
for n in todo:
    t = time.time()
    dp.create_depth_map(image_path=f"shots/{n}.png").depth_image.save(f"depth/{n}.png")
    print(f"{n:14s} {time.time()-t:5.1f}s", flush=True)
print("done")
