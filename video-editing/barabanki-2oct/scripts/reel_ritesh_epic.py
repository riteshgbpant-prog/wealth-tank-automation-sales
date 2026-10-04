"""Ritesh Tripathi – 30s vertical 'epic' Reel: warm cinematic grade, swirl/zoom-blur transitions,
word-by-word Hindi captions (own lines), embers, timed to the reference song's phrases."""
import sys, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
from engine import Canvas, run, Clip, photo_frame, zoom, clamp, prog, lerp, eo, ei, eio, back, GOLD, GOLD_L, WHITE, NAVY, M, B
import engine
from cards import RAW as R

W, H = 1080, 1920
cv = Canvas(W, H)
P = lambda n: R + "20261002_%s.jpg" % n
HF = lambda s: ImageFont.truetype("fonts/Mukta-800.ttf", int(s), layout_engine=ImageFont.Layout.RAQM)

# ---- warm epic grade ----
x = np.arange(256) / 255.0
s = np.clip(0.5 + (x - 0.5) * 1.18, 0, 1)
LR = (np.clip(s * 1.08 + 0.03, 0, 1) * 255).astype(np.uint8)
LG = (np.clip(s * 0.97, 0, 1) * 255).astype(np.uint8)
LB = (np.clip(s * 0.80, 0, 1) * 255).astype(np.uint8)
def warm(img):
    a = np.asarray(img.convert("RGB"))
    return Image.fromarray(np.stack([LR[a[..., 0]], LG[a[..., 1]], LB[a[..., 2]]], -1)).convert("RGBA")

yy, xx = np.ogrid[:H, :W]
d = np.sqrt(((xx - W / 2) / (W * 0.7)) ** 2 + ((yy - H * 0.45) / (H * 0.62)) ** 2)
VIG = np.zeros((H, W, 4), np.uint8); VIG[..., 3] = (np.clip(d - 0.45, 0, 1) * 235).astype(np.uint8)
VIG = Image.fromarray(VIG, "RGBA")
LOWER = np.zeros((H, W, 4), np.uint8); LOWER[..., 3] = (np.clip((yy / H - 0.45) / 0.4, 0, 1) * 170 + 0 * xx).astype(np.uint8)
LOWER = Image.fromarray(LOWER, "RGBA")

rng = np.random.default_rng(5)
EMB = [(rng.uniform(0, W), rng.uniform(0, H), rng.uniform(1.5, 4.5), rng.uniform(60, 180), rng.uniform(0, 6.28)) for _ in range(70)]
def embers(t):
    L = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dd = ImageDraw.Draw(L)
    for x0, y0, r, sp, ph in EMB:
        y = (y0 - sp * t) % H; x = x0 + 30 * math.sin(t * 1.3 + ph)
        a = int(180 * (0.5 + 0.5 * math.sin(t * 4 + ph)))
        dd.ellipse([x - r, y - r, x + r, y + r], fill=(255, 170, 60, a))
    return L.filter(ImageFilter.GaussianBlur(1.6))

# ---- word-by-word Hindi caption ----
def caption(img, t, t0, t1, text, per_word=0.22, y=H * 0.70, size=92):
    if not (t0 <= t < t1): return
    words = text.split(" "); n = min(len(words), int((t - t0) / per_word) + 1)
    shown = " ".join(words[:n])
    f = HF(size)
    L = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dd = ImageDraw.Draw(L)
    # wrap into lines that fit
    lines, cur = [], ""
    for w_ in shown.split(" "):
        trial = (cur + " " + w_).strip()
        if dd.textlength(trial, font=f) > W - 120 and cur: lines.append(cur); cur = w_
        else: cur = trial
    lines.append(cur)
    lh = size * 1.25; y0 = y - lh * (len(lines) - 1) / 2
    for i, ln in enumerate(lines):
        dd.text((W / 2, y0 + i * lh), ln, font=f, fill=WHITE + (255,), anchor="mm", stroke_width=3, stroke_fill=(0, 0, 0, 255))
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); sh.putalpha(L.split()[3].point(lambda v: v * 200 // 255).filter(ImageFilter.GaussianBlur(10)))
    fade = 1 - prog(t, t1 - 0.15, t1)
    if fade < 1:
        L.putalpha(L.split()[3].point(lambda v: int(v * fade))); sh.putalpha(sh.split()[3].point(lambda v: int(v * fade)))
    img.alpha_composite(sh, (0, 6)); img.alpha_composite(L)

# ---- shots ----
def shot_photo(t0, dur, path, z=(1.02, 1.16), c=(0.5, 0.45), rot=1.2):
    def fn(t):
        tl = t - t0
        img = photo_frame(cv, path, tl, dur, z[0], z[1], c, c)
        img = img.rotate(lerp(-rot, rot, clamp(tl / dur)), resample=Image.BILINEAR, center=(W / 2, H / 2))
        img = zoom(cv, img, 1.04)
        return warm(img)
    return fn

def shot_clip(t0, dur, path, src, z=(1.05, 1.15)):
    C = Clip(path, src)
    def fn(t):
        tl = t - t0
        return warm(zoom(cv, C.frame(tl, W, H), lerp(z[0], z[1], clamp(tl / dur)), 0.5, 0.42))
    return fn

def end_card(t0, dur):
    def fn(t):
        tl = t - t0
        img = photo_frame(cv, P("121510"), tl, dur, 1.25, 1.1).filter(ImageFilter.GaussianBlur(8))
        img = warm(img); img.alpha_composite(Image.new("RGBA", (W, H), (20, 8, 0, 160)))
        p = back(prog(tl, 0, 0.5)); sz = int(520 * max(p, 0.01))
        lg = cv.logo(sz); glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(glow).ellipse([W / 2 - 330, 560 - 330, W / 2 + 330, 560 + 330], fill=(255, 170, 40, int(120 * min(1, p))))
        img.alpha_composite(glow.filter(ImageFilter.GaussianBlur(70)))
        img.alpha_composite(lg, (int(W / 2 - lg.width / 2), int(540 - lg.height / 2)))
        dd = ImageDraw.Draw(img)
        a = int(255 * prog(tl, 0.4, 0.8))
        dd.text((W / 2, 930), "RITESH TRIPATHI", font=HF(100), fill=(255, 215, 120, a), anchor="mm", stroke_width=3, stroke_fill=(0, 0, 0, a))
        dd.text((W / 2, 1040), "Founder, Wealth Tank", font=M(800, 46), fill=(255, 255, 255, a), anchor="mm")
        dd.text((W / 2, 1100), "Master Facilitator & Financial Planner", font=M(600, 34), fill=(255, 230, 190, a), anchor="mm")
        pb = back(prog(tl, 0.8, 1.2))
        if pb > 0:
            bw, bh = 820 * pb, 120 * pb; by = 1230
            dd.rounded_rectangle([W / 2 - bw / 2, by, W / 2 + bw / 2, by + bh], int(bh / 2), fill=GOLD + (255,))
            if pb > 0.7: dd.text((W / 2, by + bh / 2), "📞  +91 93051 60843".replace("📞  ", "Call: "), font=M(800, 50 * pb), fill=NAVY, anchor="mm")
        a2 = int(255 * prog(tl, 1.2, 1.6))
        dd.text((W / 2, 1450), "Next session in your city!", font=HF(70), fill=(255, 255, 255, a2), anchor="mm", stroke_width=2, stroke_fill=(0, 0, 0, a2))
        return img
    return fn

SHOTS = [
    (0.0, 1.63, shot_photo(0.0, 1.63, P("083554"), c=(0.55, 0.45))),
    (1.63, 3.6, shot_photo(1.63, 1.97, P("085648"), c=(0.5, 0.55))),
    (3.6, 5.37, shot_photo(3.6, 1.77, P("085755"), c=(0.55, 0.45))),
    (5.37, 7.4, shot_photo(5.37, 2.03, P("090720"), z=(1.1, 1.3), c=(0.47, 0.55))),
    (7.4, 9.0, shot_photo(7.4, 1.6, P("100948"), c=(0.45, 0.5))),
    (9.0, 10.83, shot_photo(9.0, 1.83, P("121510"), c=(0.4, 0.5))),
    (10.83, 12.5, shot_photo(10.83, 1.67, P("122407"), z=(1.15, 1.35), c=(0.83, 0.45))),
    (12.5, 14.07, shot_clip(12.5, 1.57, "srcV/v3.mp4", 9.0, z=(1.6, 1.75))),
    (14.07, 16.93, shot_photo(14.07, 2.86, P("105021"), c=(0.5, 0.45))),
    (16.93, 19.4, shot_photo(16.93, 2.47, P("115122"), c=(0.55, 0.5))),
    (19.4, 21.0, shot_photo(19.4, 1.6, P("083520"), c=(0.74, 0.45))),
    (21.0, 23.0, shot_photo(21.0, 2.0, P("090720"), z=(1.35, 1.6), c=(0.47, 0.5))),
    (23.0, 25.5, shot_photo(23.0, 2.5, P("122407"), z=(1.3, 1.6), c=(0.84, 0.42))),
    (25.5, 27.5, shot_photo(25.5, 2.0, P("144711"), z=(1.05, 1.2), c=(0.5, 0.4))),
    (27.5, 30.0, end_card(27.5, 2.5)),
]
CAPS = [
    (0.35, 1.6, "Every home is calling"),
    (1.9, 3.6, "Every family needs a shield"),
    (3.9, 7.35, "Protection is the greatest gift"),
    (7.5, 9.0, "A packed hall in Barabanki"),
    (9.3, 10.8, "LIC Champions, all in"),
    (11.3, 14.05, "Those who learn, lead"),
    (15.3, 16.9, "Don't sell products"),
    (17.3, 19.35, "Understand the need"),
    (19.5, 22.95, "Ritesh Tripathi — Founder, Wealth Tank"),
    (23.1, 25.45, "Master Facilitator & Financial Planner"),
    (25.6, 27.45, "Har Ghar Suraksha — the mission continues"),
]
CUTS = [s[0] for s in SHOTS[1:]]

def zoomblur(img, amt):
    """Radial zoom blur (average of progressively zoomed copies)."""
    if amt < 0.02: return img
    acc = np.asarray(img, dtype=np.float32); n = 6
    for k in range(1, n):
        acc = acc + np.asarray(zoom(cv, img, 1 + amt * 0.35 * k / n), dtype=np.float32)
    return Image.fromarray((acc / n).astype(np.uint8), "RGBA")

def swirl(img, amt, direction=1):
    if amt < 0.02: return img
    acc = np.asarray(img, dtype=np.float32); n = 6
    for k in range(1, n):
        acc = acc + np.asarray(zoom(cv, img.rotate(direction * amt * 22 * k / n, resample=Image.BILINEAR), 1 + amt * 0.25), dtype=np.float32)
    return Image.fromarray((acc / n).astype(np.uint8), "RGBA")

def frame(t):
    i = max(k for k, s in enumerate(SHOTS) if s[0] <= t or k == 0)
    img = SHOTS[i][2](t)
    # transition: blur out of previous shot / into next shot around each cut
    for ci, c in enumerate(CUTS):
        dt = t - c
        if -0.22 <= dt < 0.22:
            amt = 1 - abs(dt) / 0.22
            img = swirl(img, amt, 1 if ci % 2 else -1) if ci % 3 == 1 else zoomblur(img, amt)
            if abs(dt) < 0.04: img.alpha_composite(Image.new("RGBA", (W, H), (255, 220, 160, 90)))
    img.alpha_composite(VIG); img.alpha_composite(embers(t))
    if t < 1.63:                                                   # opening logo reveal
        p = back(prog(t, 0.05, 0.45)); fo = 1 - prog(t, 1.35, 1.6)
        img.alpha_composite(Image.new("RGBA", (W, H), (10, 4, 0, int(150 * fo))))
        gl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(gl).ellipse([W / 2 - 360, 700 - 360, W / 2 + 360, 700 + 360], fill=(255, 170, 40, int(130 * fo * min(1, p))))
        img.alpha_composite(gl.filter(ImageFilter.GaussianBlur(80)))
        lg = cv.logo(max(4, int(480 * p))).copy(); lg.putalpha(lg.split()[3].point(lambda v: int(v * fo)))
        img.alpha_composite(lg, (int(W / 2 - lg.width / 2), int(700 - lg.height / 2)))
    if t < 27.5:
        img.alpha_composite(LOWER)
        for a, b, txt in CAPS: caption(img, t, a, b, txt)
        if t >= 1.6:
            lg = cv.logo(120); img.alpha_composite(lg, (W - 150, 70))
    if t < 0.25: img.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, int(255 * (1 - t / 0.25)))))
    return img

if __name__ == "__main__":
    segs = [(0, 30, frame)]
    if sys.argv[1] == "preview":
        engine.PREVDIR = sys.argv[3]
        run(cv, segs, {}, 30, None, preview=[float(v) for v in sys.argv[2].split(",")])
    else:
        run(cv, segs, {}, 30, sys.argv[1])
