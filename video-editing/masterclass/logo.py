"""Vector recreation of the Wealth Tank badge logo (drawn on a 1600x1600 canvas, then scaled)."""
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

NAVY = (6, 30, 98)
GOLD_D, GOLD_L = np.array([170, 120, 28]), np.array([248, 212, 92])
SS = 1600
FONT = "fonts/Montserrat-900.ttf"


def gold_fill(size=SS):
    x = np.linspace(0, 1, size)[None, :]; y = np.linspace(0, 1, size)[:, None]
    k = 0.5 + 0.5 * np.sin((x * 2.6 + y * 0.9) * np.pi * 1.4)          # metallic banding
    rgb = GOLD_D[None, None] + (GOLD_L - GOLD_D)[None, None] * k[..., None]
    return Image.fromarray(rgb.astype(np.uint8), "RGB")


HEX = [(800, 15), (1440, 318), (1440, 1135), (1380, 1235), (800, 1588), (220, 1235), (160, 1135), (160, 318)]


def inset(poly, d):
    c = np.array([800, 800.0])
    return [tuple(c + (np.array(p) - c) * (1 - d / 800)) for p in poly]


def tank_mask():
    m = Image.new("L", (SS, SS), 0); d = ImageDraw.Draw(m)
    d.rectangle([345, 318, 600, 352], fill=255)                                   # rear barrel
    d.polygon([(985, 300), (1300, 252), (1312, 284), (995, 345)], fill=255)        # main barrel
    d.ellipse([1300, 228, 1380, 308], fill=255)                                   # muzzle ring
    d.polygon([(555, 335), (660, 278), (905, 278), (1000, 318), (1030, 345), (940, 412), (625, 412)], fill=255)
    d.rectangle([705, 238, 850, 282], fill=255)                                   # hatch
    d.polygon([(358, 515), (410, 445), (520, 445), (530, 425), (1080, 425), (1095, 445), (1195, 445), (1240, 515)], fill=255)
    d.polygon([(368, 522), (1232, 522), (1212, 605), (1105, 660), (488, 660), (382, 605)], fill=255)
    return m


def tank_lines():
    m = Image.new("L", (SS, SS), 0); d = ImageDraw.Draw(m)
    W = 255
    d.line([(345, 335), (600, 335)], fill=W, width=7)
    d.ellipse([1322, 250, 1358, 286], fill=W)                                      # ring hole
    d.line([(870, 282), (935, 408)], fill=W, width=8)                             # turret facet
    d.ellipse([940, 312, 966, 338], fill=W)
    d.line([(722, 255), (835, 255)], fill=W, width=0)
    d.line([(360, 518), (1240, 518)], fill=W, width=8)                            # hull/track split
    for cx, r in [(435, 38), (538, 47), (643, 47), (745, 47), (848, 47), (950, 47), (1052, 47), (1160, 36)]:
        d.ellipse([cx - r - 6, 582 - r - 6, cx + r + 6, 582 + r + 6], outline=W, width=8)
    return m


def chevron_mask():
    m = Image.new("L", (SS, SS), 0); d = ImageDraw.Draw(m)
    d.polygon([(697, 1262), (797, 1318), (797, 1362), (697, 1306)], fill=255)
    d.polygon([(897, 1262), (797, 1318), (797, 1362), (897, 1306)], fill=255)
    d.polygon([(775, 1345), (797, 1330), (820, 1345), (820, 1410), (797, 1432), (775, 1410)], fill=255)
    return m


def build(size=800):
    gold = gold_fill()
    img = Image.new("RGBA", (SS, SS), (0, 0, 0, 0))
    outer = Image.new("L", (SS, SS), 0); ImageDraw.Draw(outer).polygon(HEX, fill=255)
    img.paste(gold, (0, 0), outer)                                                   # gold band
    white = Image.new("L", (SS, SS), 0); ImageDraw.Draw(white).polygon(inset(HEX, 28), fill=255)
    img.paste((255, 255, 255), (0, 0), white)
    navy = Image.new("L", (SS, SS), 0); ImageDraw.Draw(navy).polygon(inset(HEX, 48), fill=255)
    img.paste(NAVY, (0, 0), navy)
    inner = Image.new("L", (SS, SS), 0); ImageDraw.Draw(inner).polygon(inset(HEX, 66), fill=255)
    img.paste((255, 255, 255), (0, 0), inner)
    tm = tank_mask()
    outline = tm.filter(ImageFilter.MaxFilter(13))
    img.paste((255, 255, 255), (0, 0), outline)
    img.paste(gold, (0, 0), tm)
    img.paste((255, 255, 255), (0, 0), Image.fromarray(np.minimum(np.array(tank_lines()), np.array(tm))))
    d = ImageDraw.Draw(img)
    for y, x0, x1 in [(735, 295, 1305), (1222, 300, 1295)]:
        lm = Image.new("L", (SS, SS), 0); ImageDraw.Draw(lm).rounded_rectangle([x0, y - 6, x1, y + 6], 6, fill=255)
        img.paste(gold, (0, 0), lm)
    f = ImageFont.truetype(FONT, 235)
    d.text((800, 893), "WEALTH", font=f, fill=NAVY, anchor="mm")
    d.text((806, 1097), "TANK", font=f, fill=NAVY, anchor="mm")
    img.paste(gold, (0, 0), chevron_mask())
    return img.resize((size, size), Image.LANCZOS)


if __name__ == "__main__":
    build(800).save("frames/logo_test.png")
