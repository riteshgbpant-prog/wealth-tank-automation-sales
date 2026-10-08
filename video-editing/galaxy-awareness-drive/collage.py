"""Galaxy Marvel health awareness drive – 1080x1350 photo collage (Wealth Tank branding)."""
import sys
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageEnhance, ImageFilter

G, BB, OUT = sys.argv[1], sys.argv[2], sys.argv[3]          # photos dir, assets dir (fonts + logo), output
W, H = 1080, 1350
NAVY = (6, 30, 98); NAVY_D = (3, 14, 44); GOLD = (240, 186, 40); GOLD_L = (255, 215, 110); WHITE = (255, 255, 255)
B = lambda s: ImageFont.truetype(f"{BB}/fonts/BebasNeue.ttf", s)
M = lambda w, s: ImageFont.truetype(f"{BB}/fonts/Montserrat-{w}.ttf", s)

def tile(path, w, h, centre=(0.5, 0.5)):
    im = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
    im = ImageOps.fit(im, (w, h), Image.LANCZOS, centering=centre)
    im = ImageEnhance.Contrast(im).enhance(1.06); im = ImageEnhance.Color(im).enhance(1.12)
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], 18, fill=255)
    out = Image.new("RGBA", (w, h)); out.paste(im, (0, 0), m)
    return out

def place(canvas, path, x, y, w, h, centre=(0.5, 0.5)):
    sh = Image.new("RGBA", (w + 40, h + 40), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([20, 26, w + 20, h + 26], 18, fill=(0, 0, 0, 150))
    canvas.alpha_composite(sh.filter(ImageFilter.GaussianBlur(12)), (x - 20, y - 20))
    ImageDraw.Draw(canvas).rounded_rectangle([x - 4, y - 4, x + w + 3, y + h + 3], 21, fill=GOLD + (255,))
    canvas.alpha_composite(tile(path, w, h, centre), (x, y))

# background: deep navy gradient
c = Image.new("RGBA", (W, H), NAVY_D + (255,))
grad = Image.linear_gradient("L").resize((W, H)).point(lambda v: int(v * 0.55))
c.paste(Image.new("RGBA", (W, H), (14, 48, 130, 255)), (0, 0), grad)
d = ImageDraw.Draw(c)

# header
d.text((W / 2, 40), "HEALTH INSURANCE AWARENESS ACTIVITY", font=B(80), fill=WHITE, anchor="mt")
d.rectangle([W / 2 - 170, 140, W / 2 + 170, 145], fill=GOLD)
d.text((W / 2, 158), "Janeshwar Mishra Park, Lucknow", font=M(700, 30), fill=GOLD_L, anchor="mt")

m, gap = 26, 14
place(c, f"{G}/g1.jpg", m, 214, W - 2 * m, 380, (0.55, 0.5))                       # team + Galaxy Marvel standee
y2 = 214 + 380 + gap + 8
bh = 1196 - y2
lw = 300
place(c, f"{G}/g9.jpg", m, y2, lw, bh, (0.5, 0.42))                                  # standee
rx = m + lw + gap + 6; rw = W - m - rx
th = (bh - gap - 6) // 2
place(c, f"{G}/g7.jpg", rx, y2, rw, th, (0.55, 0.45))                                # one-to-one explanation
hw = (rw - gap - 6) // 2
place(c, f"{G}/g4.jpg", rx, y2 + th + gap + 6, hw, bh - th - gap - 6, (0.5, 0.5))     # explaining to walkers
place(c, f"{G}/g3.jpg", rx + hw + gap + 6, y2 + th + gap + 6, rw - hw - gap - 6, bh - th - gap - 6, (0.55, 0.5))  # team at gate

# footer (no company branding / phone)
d.text((W / 2, 1232), "Your health is your real wealth", font=B(64), fill=GOLD_L, anchor="mt")
d.text((W / 2, 1298), "Spreading health insurance awareness, one family at a time", font=M(600, 26), fill=WHITE, anchor="mt")
c.convert("RGB").save(OUT, quality=95)
print("saved", OUT)
