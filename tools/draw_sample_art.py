"""Draw the original, MIT-licensed release sample art."""
from pathlib import Path
from PIL import Image, ImageDraw

assets = Path(__file__).resolve().parents[1] / "assets"
for i, name in enumerate(("field", "khu", "talab")):
    image = Image.new("RGB", (960, 540), ["#edbd86", "#a1bbc8", "#b5cad6"][i])
    draw = ImageDraw.Draw(image)
    draw.ellipse((686, 77, 798, 189), fill="#fff0cd")
    draw.polygon([(0, 319), (195, 180), (378, 292), (567, 193), (960, 312), (960, 540), (0, 540)], fill="#526b75")
    draw.polygon([(0, 399), (252, 306), (507, 365), (720, 286), (960, 350), (960, 540), (0, 540)], fill="#829472")
    draw.polygon([(0, 425), (460, 352), (960, 401), (960, 540), (0, 540)], fill="#ad935a")
    if i == 0:
        for x in range(0, 960, 57):
            draw.line((478, 369, x, 540), fill="#d8b777", width=5)
    if i == 1:
        draw.rounded_rectangle((404, 329, 547, 423), 22, fill="#654f4d", outline="#ecd2a9", width=6)
        draw.line((420, 339, 420, 249, 530, 249, 530, 339), fill="#492f31", width=9)
    if i == 2:
        draw.ellipse((224, 363, 737, 525), fill="#557c87")
        for y in range(409, 499, 18):
            draw.line((345, y, 598, y), fill="#9ab9b6", width=2)
    image.save(assets / f"{name}.webp", quality=86)

for name, wrap, clothing in (("sant_kaur", "#843c54", "#d5986c"),
                             ("sultan", "#425869", "#687c88"),
                             ("krishna", "#d4a355", "#827866")):
    image = Image.new("RGB", (320, 320), "#e6c6a4")
    draw = ImageDraw.Draw(image)
    draw.ellipse((67, 35, 253, 225), fill=wrap)
    draw.ellipse((34, 202, 286, 417), fill=clothing)
    draw.rounded_rectangle((133, 166, 187, 232), radius=14, fill="#ad6d50")
    draw.ellipse((104, 91, 216, 212), fill="#c98663")
    draw.arc((128, 136, 150, 155), 190, 350, fill="#38292c", width=3)
    draw.arc((173, 136, 195, 155), 190, 350, fill="#38292c", width=3)
    draw.arc((145, 169, 176, 185), 15, 165, fill="#623f3c", width=3)
    draw.arc((86, 51, 230, 177), 202, 342, fill=wrap, width=23)
    image.save(assets / f"{name}.webp", quality=87)
