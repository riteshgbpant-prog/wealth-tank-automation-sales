"""Static top/bottom branding frame for the 9:16 (Reels / Status / Shorts) version."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from logo import build
W, H = 1080, 1920
NAVY = (6, 30, 98); GOLD = (240, 186, 40); GOLD_L = (255, 215, 110)
M = lambda w, s: ImageFont.truetype(f"fonts/Montserrat-{w}.ttf", s)
B = lambda s: ImageFont.truetype("fonts/BebasNeue.ttf", s)
L = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
# dark fades so text pops over the blurred background
for y in range(0, 560):
    d.line([(0, y), (W, y)], fill=(3, 14, 44, int(235 * (1 - y / 560) ** 0.7)))
for y in range(1360, H):
    d.line([(0, y), (W, y)], fill=(3, 14, 44, int(235 * ((y - 1360) / 560) ** 0.7)))
lg = build(230); L.alpha_composite(lg, (W // 2 - 115, 60))
d.text((W / 2, 320), "2-DAY SALES MASTERCLASS", font=B(96), fill=(255, 255, 255), anchor="mt")
d.text((W / 2, 425), "for LIC Development Officers", font=M(600, 40), fill=GOLD_L, anchor="mt")
d.rectangle([W / 2 - 160, 1430, W / 2 + 160, 1436], fill=GOLD)
d.text((W / 2, 1460), "Mr. Anurag Kesarwani", font=M(800, 56), fill=(255, 255, 255), anchor="mt")
d.text((W / 2, 1535), "Co-Founder, Wealth Tank  •  Master Sales Coach", font=M(600, 32), fill=GOLD_L, anchor="mt")
d.rounded_rectangle([W / 2 - 290, 1640, W / 2 + 290, 1730], 45, fill=GOLD)
d.text((W / 2, 1685), "FOLLOW WEALTH TANK", font=M(800, 36), fill=NAVY, anchor="mm")
L.save("vertical_overlay.png")
