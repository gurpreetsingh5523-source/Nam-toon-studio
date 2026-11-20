"""Make the original storyboard icon in each platform's required format."""
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw

folder = Path(sys.argv[1])
folder.mkdir(parents=True, exist_ok=True)
image = Image.new("RGBA", (1024, 1024))
draw = ImageDraw.Draw(image)
draw.rounded_rectangle((72, 72, 952, 952), radius=198, fill="#162d42")
draw.rounded_rectangle((222, 266, 802, 758), radius=72, fill="#79dec3")
draw.rounded_rectangle((247, 369, 777, 733), radius=45, fill="#102335")
for x in (280, 414, 548, 682):
    draw.polygon([(x, 281), (x + 67, 281), (x + 31, 354), (x - 36, 354)], fill="#28656a")
draw.polygon([(444, 437), (444, 665), (648, 551)], fill="#ffc678")
image.save(folder / "studio-icon.png")
if sys.platform == "win32":
    image.save(folder / "studio.ico", sizes=[(size, size) for size in (16, 32, 48, 64, 128, 256)])
elif sys.platform == "darwin":
    iconset = folder / "studio.iconset"
    iconset.mkdir(exist_ok=True)
    for size in (16, 32, 128, 256, 512):
        for scale, suffix in ((1, ""), (2, "@2x")):
            actual = size * scale
            image.resize((actual, actual), Image.Resampling.LANCZOS).save(iconset / f"icon_{size}x{size}{suffix}.png")
    subprocess.run(["iconutil", "-c", "icns", str(iconset)], check=True)
