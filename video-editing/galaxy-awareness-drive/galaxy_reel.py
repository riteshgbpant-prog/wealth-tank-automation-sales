"""Galaxy Marvel health awareness drive – 30s vertical reel (1080x1920), English captions, Wealth Tank logo start/end."""
import sys, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from engine import Canvas, run, photo_frame, zoom, clamp, prog, lerp, back, GOLD, WHITE, NAVY, M
import engine

W, H = 1080, 1920
cv = Canvas(W, H)
G = sys.argv[3] if len(sys.argv) > 3 else "../galaxy/in"
P = lambda n: f"{G}/g{n}.jpg"
HF = lambda s: ImageFont.truetype("fonts/Mukta-800.ttf", int(s), layout_engine=ImageFont.Layout.RAQM)
TEAL = (0, 170, 190)

# fresh, bright grade
x = np.arange(256) / 255.0
s = np.clip(0.5 + (x - 0.5) * 1.12, 0, 1)
LR = (np.clip(s * 1.02, 0, 1) * 255).astype(np.uint8); LG = (np.clip(s * 1.02 + 0.01, 0, 1) * 255).astype(np.uint8)
LB = (np.clip(s * 1.04 + 0.02, 0, 1) * 255).astype(np.uint8)
def grade(img):
    a = np.asarray(img.convert("RGB"))
    return Image.fromarray(np.stack([LR[a[..., 0]], LG[a[..., 1]], LB[a[..., 2]]], -1)).convert("RGBA")

yy, xx = np.ogrid[:H, :W]
VIG = np.zeros((H, W, 4), np.uint8)
VIG[..., 3] = (np.clip(np.sqrt(((xx - W / 2) / (W * .7)) ** 2 + ((yy - H * .45) / (H * .62)) ** 2) - .5, 0, 1) * 200).astype(np.uint8)
VIG = Image.fromarray(VIG, "RGBA")
LOWER = np.zeros((H, W, 4), np.uint8); LOWER[..., 3] = (np.clip((yy / H - 0.5) / 0.4, 0, 1) * 175 + 0 * xx).astype(np.uint8)
LOWER = Image.fromarray(LOWER, "RGBA")

def caption(img, t, t0, t1, text, per_word=0.18, y=H * 0.72, size=96):
    if not (t0 <= t < t1): return
    words = text.split(" "); shown = " ".join(words[:min(len(words), int((t - t0) / per_word) + 1)])
    f = HF(size); L = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    lines, cur = [], ""
    for w_ in shown.split(" "):
        trial = (cur + " " + w_).strip()
        if d.textlength(trial, font=f) > W - 120 and cur: lines.append(cur); cur = w_
        else: cur = trial
    lines.append(cur); lh = size * 1.2; y0 = y - lh * (len(lines) - 1) / 2
    for i, ln in enumerate(lines):
        d.text((W / 2, y0 + i * lh), ln, font=f, fill=WHITE, anchor="mm", stroke_width=3, stroke_fill=(0, 0, 0))
    a = 1 - prog(t, t1 - 0.15, t1)
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); sh.putalpha(L.split()[3].point(lambda v: int(v * 0.8 * a)).filter(ImageFilter.GaussianBlur(10)))
    if a < 1: L.putalpha(L.split()[3].point(lambda v: int(v * a)))
    img.alpha_composite(sh, (0, 6)); img.alpha_composite(L)

def shot(t0, dur, path, z=(1.02, 1.15), c=(0.5, 0.5), fill="crop", rot=1.0):
    def fn(t):
        tl = t - t0
        img = photo_frame(cv, path, tl, dur, z[0], z[1], c, c, fill=fill)
        if fill == "crop":
            img = zoom(cv, img.rotate(lerp(-rot, rot, clamp(tl / dur)), resample=Image.BILINEAR), 1.04)
        return grade(img)
    return fn

def logo_card(img, t, t0, t1, big=False):
    if not (t0 <= t < t1): return
    tl = t - t0
    img.alpha_composite(Image.new("RGBA", (W, H), (2, 10, 30, 200)))
    d = ImageDraw.Draw(img)
    for i, (txt, size, col, ts) in enumerate([("HEALTH INSURANCE", 100, (255, 215, 120), 0.1), ("AWARENESS ACTIVITY", 100, (255, 255, 255), 0.35)]):
        a = int(255 * prog(tl, ts, ts + 0.4))
        d.text((W / 2, 720 + i * 135), txt, font=HF(size), fill=col + (a,), anchor="mm", stroke_width=3, stroke_fill=(0, 0, 0, a))
    a = int(255 * prog(tl, 0.7, 1.1))
    d.rectangle([W / 2 - 200, 935, W / 2 + 200, 941], fill=GOLD + (a,))
    d.text((W / 2, 1000), "Janeshwar Mishra Park, Lucknow", font=M(700, 42), fill=(255, 255, 255, a), anchor="mm")
    a2 = int(255 * prog(tl, 1.1, 1.5))
    d.text((W / 2, 1140), "Your health is your real wealth", font=HF(70), fill=(255, 255, 255, a2), anchor="mm", stroke_width=2, stroke_fill=(0, 0, 0, a2))
    d.text((W / 2, 1230), "Get your family covered today!", font=M(700, 40), fill=(200, 235, 255, a2), anchor="mm")

SHOTS = [
    (0.0, 2.0, shot(0.0, 2.0, P(9), fill="blur", z=(1.0, 1.06))),
    (2.0, 4.0, shot(2.0, 2.0, P(2), c=(0.3, 0.5), z=(1.05, 1.2))),
    (4.0, 6.5, shot(4.0, 2.5, P(1), c=(0.32, 0.5))),
    (6.5, 8.5, shot(6.5, 2.0, P(1), c=(0.66, 0.5), z=(1.1, 1.25))),
    (8.5, 11.0, shot(8.5, 2.5, P(3), c=(0.5, 0.5))),
    (11.0, 13.5, shot(11.0, 2.5, P(7), c=(0.5, 0.5))),
    (13.5, 16.0, shot(13.5, 2.5, P(4), c=(0.5, 0.5))),
    (16.0, 18.0, shot(16.0, 2.0, P(5), c=(0.45, 0.5))),
    (18.0, 20.0, shot(18.0, 2.0, P(6), c=(0.5, 0.5))),
    (20.0, 22.0, shot(20.0, 2.0, P(8), c=(0.55, 0.5))),
    (22.0, 24.5, shot(22.0, 2.5, P(9), z=(1.05, 1.25), c=(0.5, 0.45))),
    (24.5, 30.0, shot(24.5, 5.5, P(1), z=(1.2, 1.3), c=(0.5, 0.5))),
]
CAPS = [
    (2.2, 3.95, "A morning in Lucknow"),
    (4.2, 6.45, "Health insurance awareness activity"),
    (6.7, 8.45, "with Galaxy Health Insurance"),
    (8.7, 10.95, "At Janeshwar Mishra Park"),
    (11.2, 13.45, "One family at a time"),
    (13.7, 15.95, "Answering every question"),
    (16.2, 19.95, "Your health is your real wealth"),
    (20.2, 21.95, "Know your policy, protect your family"),
    (22.2, 24.4, "Protect your family today"),
]
CUTS = [s_[0] for s_ in SHOTS[1:]]

def zoomblur(img, amt):
    acc = np.asarray(img, dtype=np.float32)
    for k in range(1, 6): acc = acc + np.asarray(zoom(cv, img, 1 + amt * 0.35 * k / 6), dtype=np.float32)
    return Image.fromarray((acc / 6).astype(np.uint8), "RGBA")

def frame(t):
    i = max(k for k, s_ in enumerate(SHOTS) if s_[0] <= t or k == 0)
    img = SHOTS[i][2](t)
    for c in CUTS:
        dt = t - c
        if -0.2 <= dt < 0.2:
            img = zoomblur(img, 1 - abs(dt) / 0.2)
            if abs(dt) < 0.04: img.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, 110)))
    img.alpha_composite(VIG)
    if t < 24.5:
        img.alpha_composite(LOWER)
        for a, b, txt in CAPS: caption(img, t, a, b, txt)
    else:
        img = img.filter(ImageFilter.GaussianBlur(min(10, (t - 24.5) * 20)))
        logo_card(img, t, 24.5, 30.0, big=True)
    if t < 0.25: img.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, int(255 * (1 - t / 0.25)))))
    if t > 29.3: img.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, int(255 * prog(t, 29.3, 30)))))
    return img

TR = {c: ("cut", 0.01) for c in CUTS}
MUSIC_DUR = 30.0
MUSIC_PLAN = [(0, 2, "intro"), (2, 8.5, "light"), (8.5, 24.5, "groove"), (24.5, 30, "outro")]
SFX_EXTRA = [(0.1, "whoosh", 0.6), (2.0, "impact", 0.5), (24.5, "impact", 0.7), (25.6, "ding", 0.6)]

if __name__ == "__main__":
    segs = [(0, 30, frame)]
    if sys.argv[1] == "preview":
        engine.PREVDIR = sys.argv[2].split("|")[1]
        run(cv, segs, {}, 30, None, preview=[float(v) for v in sys.argv[2].split("|")[0].split(",")])
    else:
        run(cv, segs, {}, 30, sys.argv[1])
