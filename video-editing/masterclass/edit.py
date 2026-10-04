"""Wealth Tank masterclass highlight reel: timeline of clips/photos, transitions, kinetic captions, logo intro/outro."""
import subprocess, math, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
from logo import build as build_logo

W, H, FPS = 1920, 1080, 30
DUR = 54.0
IMG = "../../images/"
OUT = sys.argv[1] if len(sys.argv) > 1 else "video_only.mp4"
ONLY = [float(x) for x in sys.argv[2].split(",")] if len(sys.argv) > 2 else None   # preview times

NAVY = (6, 30, 98); NAVY_D = (3, 14, 44); GOLD = (240, 186, 40); GOLD_L = (255, 215, 110); WHITE = (255, 255, 255)
def M(w, s): return ImageFont.truetype(f"fonts/Montserrat-{w}.ttf", s)
def B(s): return ImageFont.truetype("fonts/BebasNeue.ttf", s)

def MX(w, s): return ImageFont.truetype(f"fonts/MontserratExt-{w}.ttf", s)

def rtext(d, xy, txt, w, size, fill):
    """Draw centred (anchor mm) Montserrat text where '₹' comes from the latin-ext subset."""
    parts = []
    for ch in txt:
        f = MX(w, size) if ch == "₹" else M(w, size)
        if parts and parts[-1][1] is f.path and False: pass
        parts.append((ch, f))
    total = sum(d.textlength(ch, font=f) for ch, f in parts)
    x = xy[0] - total / 2
    for ch, f in parts:
        d.text((x, xy[1]), ch, font=f, fill=fill, anchor="lm"); x += d.textlength(ch, font=f)

def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def prog(t, a, b): return clamp((t - a) / (b - a))
def eo(x): return 1 - (1 - x) ** 3
def ei(x): return x ** 3
def eio(x): return 3 * x * x - 2 * x * x * x
def back(x, s=1.7): x -= 1; return x * x * ((s + 1) * x + s) + 1
def lerp(a, b, x): return a + (b - a) * x

# ---------------------------------------------------------------- sources
class Clip:
    def __init__(self, path, src_start):
        self.path, self.s0 = path, src_start
        self.p = None; self.idx = -1; self.last = None
    def frame(self, tl):                       # tl = seconds since segment start (may be negative in transition)
        want = max(0, int(round((self.s0 + tl) * FPS)))
        if self.p is None:
            self.p = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", f"{self.s0 - 0.5:.3f}", "-i", self.path,
                                       "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
            self.idx = int(round((self.s0 - 0.5) * FPS)) - 1
        while self.idx < want:
            buf = self.p.stdout.read(W * H * 3)
            if len(buf) < W * H * 3: break
            self.last = buf; self.idx += 1
        return Image.frombuffer("RGB", (W, H), self.last)

class Photo:
    def __init__(self, path, z0, z1, c0, c1):
        im = Image.open(path).convert("RGB")
        from PIL import ImageEnhance
        im = ImageEnhance.Contrast(im).enhance(1.06); im = ImageEnhance.Color(im).enhance(1.12)
        self.im = im; self.z = (z0, z1); self.c = (c0, c1)
    def frame(self, tl, dur):
        x = clamp(tl / dur, -0.2, 1.2)
        z = max(1.0, lerp(*self.z, x)); cx = lerp(self.c[0][0], self.c[1][0], x); cy = lerp(self.c[0][1], self.c[1][1], x)
        iw, ih = self.im.size
        cw = iw / z; ch = cw * 9 / 16
        if ch > ih / z * 1.0: ch = ih / z; cw = ch * 16 / 9
        cw, ch = min(cw, iw), min(ch, ih)
        x0 = clamp(cx * iw - cw / 2, 0, iw - cw); y0 = clamp(cy * ih - ch / 2, 0, ih - ch)
        return self.im.resize((W, H), Image.BILINEAR, box=(x0, y0, x0 + cw, y0 + ch))

def zoom(img, z, cx=0.5, cy=0.5):
    if z <= 1.001: return img
    cw, ch = W / z, H / z
    x0 = clamp(cx * W - cw / 2, 0, W - cw); y0 = clamp(cy * H - ch / 2, 0, H - ch)
    return img.resize((W, H), Image.BILINEAR, box=(x0, y0, x0 + cw, y0 + ch))

# ---------------------------------------------------------------- shared assets
LOGO = build_logo(900)
def vignette(strength=170):
    y, x = np.ogrid[:H, :W]
    d = np.sqrt(((x - W / 2) / (W * 0.62)) ** 2 + ((y - H / 2) / (H * 0.62)) ** 2)
    v = np.zeros((H, W, 4), np.uint8); v[..., 3] = (np.clip(d - 0.6, 0, 1) * strength).astype(np.uint8)
    return Image.fromarray(v, "RGBA")
VIG = vignette()

def _scrim():
    y, x = np.ogrid[:H, :W]
    a = np.clip((y / H - 0.5) / 0.5, 0, 1) ** 1.2 * np.clip(1.25 - x / W * 1.3, 0, 1) * 215
    s = np.zeros((H, W, 4), np.float32); s[..., 0:3] = NAVY_D; s[..., 3] = a
    return s
SCRIM = _scrim()
SCRIM_IMG = Image.fromarray(SCRIM[..., :3].astype(np.uint8), "RGB").convert("RGBA")
SCRIM_A = Image.fromarray(SCRIM[..., 3].astype(np.uint8), "L")

def navy_bg(t):
    y, x = np.ogrid[:H, :W]
    cx = W / 2 + 120 * math.sin(t * 0.7); cy = H / 2
    d = np.sqrt(((x - cx) / W) ** 2 + ((y - cy) / H) ** 2)
    k = np.clip(1 - d * 1.5, 0, 1)[..., None]
    rgb = np.array(NAVY_D)[None, None] + (np.array((14, 48, 130)) - np.array(NAVY_D))[None, None] * k
    return Image.fromarray(rgb.astype(np.uint8), "RGB").convert("RGBA")

RNG = np.random.default_rng(3)
PARTS = [(RNG.uniform(0, W), RNG.uniform(0, H), RNG.uniform(2, 7), RNG.uniform(10, 60), RNG.uniform(0, 6.28)) for _ in range(90)]
def particles(t, alpha=1.0):
    L = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    for x, y, r, sp, ph in PARTS:
        yy = (y - sp * t * 3) % H; xx = x + 25 * math.sin(t * 0.8 + ph)
        a = int(255 * alpha * (0.35 + 0.65 * (0.5 + 0.5 * math.sin(t * 2 + ph))))
        d.ellipse([xx - r, yy - r, xx + r, yy + r], fill=GOLD_L + (a // 2,))
    return L.filter(ImageFilter.GaussianBlur(2))

def light_rays(t, a):
    L = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    cx, cy = W / 2, H / 2
    for k in range(14):
        ang = k * 2 * math.pi / 14 + t * 0.25
        p1 = (cx + 1600 * math.cos(ang - 0.05), cy + 1600 * math.sin(ang - 0.05))
        p2 = (cx + 1600 * math.cos(ang + 0.05), cy + 1600 * math.sin(ang + 0.05))
        d.polygon([(cx, cy), p1, p2], fill=GOLD + (int(40 * a),))
    return L.filter(ImageFilter.GaussianBlur(18))

def shine(img, p, width=160):
    """Diagonal light sweep across an RGBA image (respecting its alpha)."""
    w, h = img.size
    m = Image.new("L", (w, h), 0); d = ImageDraw.Draw(m)
    x = lerp(-w * 0.6, w * 1.4, p)
    d.polygon([(x, 0), (x + width, 0), (x + width - h * 0.5, h), (x - h * 0.5, h)], fill=150)
    m = ImageChops.multiply(m.filter(ImageFilter.GaussianBlur(20)), img.split()[3])
    out = img.copy(); out.paste((255, 255, 240), (0, 0), m); return out

def text_layer(): return Image.new("RGBA", (W, H), (0, 0, 0, 0))

def reveal_text(L, xy, txt, font, fill, p, anchor="la", direction="up", dist=60):
    """Text slides in from behind an invisible mask line (pro 'mask reveal')."""
    if p <= 0: return
    tmp = text_layer(); d = ImageDraw.Draw(tmp)
    off = (1 - eo(p)) * dist
    x, y = xy
    if direction == "up": y += off
    else: x -= off
    d.text((x, y), txt, font=font, fill=fill, anchor=anchor)
    bb = ImageDraw.Draw(text_layer()).textbbox(xy, txt, font=font, anchor=anchor)
    m = Image.new("L", (W, H), 0)
    ImageDraw.Draw(m).rectangle([bb[0] - 40, bb[1] - 30, bb[2] + 40, bb[3] + 20], fill=255)
    tmp.putalpha(ImageChops.multiply(tmp.split()[3], m))
    L.alpha_composite(tmp)

def shadow_of(L, blur=16, alpha=150, off=(0, 6)):
    a = L.split()[3].point(lambda v: v * alpha // 255).filter(ImageFilter.GaussianBlur(blur))
    s = Image.new("RGBA", (W, H), (0, 0, 0, 0)); s.putalpha(a)
    out = text_layer(); out.alpha_composite(s, off); out.alpha_composite(L); return out

def letterbox(img, a):
    if a <= 0: return
    h = int(70 * a); d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, h], fill=(0, 0, 0, 255)); d.rectangle([0, H - h, W, H], fill=(0, 0, 0, 255))

def bug(img, a=1.0):
    """Corner logo watermark."""
    sm = LOGO.resize((110, 110), Image.LANCZOS)
    if a < 1: sm.putalpha(sm.split()[3].point(lambda v: int(v * a)))
    img.alpha_composite(sm, (W - 150, 40 + 30))

def caption(L, t, t0, t1, kicker, line, sub=None, pos="bl"):
    """Kinetic caption block: gold kicker tag, big Bebas headline, sub line; bottom-left."""
    if not (t0 - 0.01 <= t <= t1): return
    out = eo(prog(t, t1 - 0.3, t1))
    x = 110 - out * 80; y = 700
    C = text_layer(); d = ImageDraw.Draw(C)
    pk = prog(t, t0, t0 + 0.35)
    if pk > 0:
        fk = M(800, 30); tw = d.textlength(kicker, font=fk)
        bw = (tw + 44) * eo(pk)
        d.rectangle([x, y, x + bw, y + 50], fill=GOLD + (255,))
        if pk > 0.5: d.text((x + 22, y + 9), kicker, font=fk, fill=NAVY)
    reveal_text(C, (x - 4, y + 64), line, B(128), WHITE, prog(t, t0 + 0.15, t0 + 0.6))
    if sub:
        reveal_text(C, (x, y + 200), sub, M(600, 38), GOLD_L, prog(t, t0 + 0.35, t0 + 0.8))
    C = shadow_of(C, 18, 170)
    a_in = eo(prog(t, t0, t0 + 0.4)) * (1 - out)
    sc = SCRIM_IMG.copy(); sc.putalpha(SCRIM_A.point(lambda v: int(v * a_in)))
    L.alpha_composite(sc)
    if out > 0: C.putalpha(C.split()[3].point(lambda v: int(v * (1 - out))))
    L.alpha_composite(C)

# ---------------------------------------------------------------- segments
SEG = []   # (start, end, render_fn)
def seg(a, b):
    def deco(fn): SEG.append((a, b, fn)); return fn
    return deco

# 0-4 LOGO INTRO
@seg(0, 4)
def s_intro(t):
    img = navy_bg(t)
    img.alpha_composite(light_rays(t, eo(prog(t, 1.9, 2.6))))
    img.alpha_composite(particles(t, prog(t, 0, 1)))
    # logo slams in at 2.0 (scale from 2.4 -> 1 with slight overshoot), then breathes
    if t >= 1.55:
        p = prog(t, 1.55, 2.0)
        s = lerp(2.6, 1.0, ei(p)) if p < 1 else 1 + 0.06 * back(prog(t, 2.0, 2.4)) - 0.06 + 0.02 * (t - 2.4) * (t > 2.4)
        size = int(560 * s)
        lg = LOGO.resize((size, size), Image.LANCZOS)
        if t > 2.15: lg = shine(lg, prog(t, 2.15, 2.9))
        a = prog(t, 1.55, 1.8)
        lg.putalpha(lg.split()[3].point(lambda v: int(v * a)))
        cy = H / 2 - 70 - eo(prog(t, 2.6, 3.1)) * 40
        img.alpha_composite(lg, (int(W / 2 - size / 2), int(cy - size / 2)))
        # camera shake on impact
        if 2.0 <= t < 2.3:
            k = (2.3 - t) / 0.3 * 14
            img = ImageChops.offset(img, int(RNG.uniform(-k, k)), int(RNG.uniform(-k, k)))
    # pre-impact: gold streaks converge
    if t < 2.0:
        L = text_layer(); d = ImageDraw.Draw(L)
        p = eo(prog(t, 0.2, 2.0))
        for k in range(6):
            yy = 200 + k * 140
            xx = lerp(-900 if k % 2 else W + 900, W / 2, p)
            d.rounded_rectangle([xx - 300, yy - 3, xx + 300, yy + 3], 3, fill=GOLD_L + (int(200 * (1 - p) + 40),))
        img.alpha_composite(L.filter(ImageFilter.GaussianBlur(1.5)))
    # flash on impact
    if 2.0 <= t < 2.25:
        img.alpha_composite(Image.new("RGBA", (W, H), (255, 245, 220, int(255 * (1 - prog(t, 2.0, 2.25))))))
    L = text_layer()
    reveal_text(L, (W / 2, 850), "INSURANCE  •  LOANS  •  CONSULTING", M(700, 40), GOLD_L, prog(t, 2.7, 3.2), anchor="mt")
    img.alpha_composite(L)
    return img

# 4-8 TITLE over wide room shot
C1 = Clip("src1.mp4", 14.0)
@seg(4, 8)
def s_title(t):
    tl = t - 4
    img = zoom(C1.frame(tl), lerp(1.12, 1.0, eo(prog(tl, -0.3, 4.3))), 0.55, 0.45).convert("RGBA")
    img.alpha_composite(Image.new("RGBA", (W, H), NAVY_D + (150,)))
    img.alpha_composite(VIG)
    L = text_layer(); d = ImageDraw.Draw(L)
    # gold rule grows
    gw = 520 * eo(prog(tl, 0.2, 0.8))
    d.rectangle([W / 2 - gw / 2, 300, W / 2 + gw / 2, 306], fill=GOLD + (255,))
    reveal_text(L, (W / 2, 330), "WEALTH TANK PRESENTS", M(800, 36), GOLD_L, prog(tl, 0.3, 0.8), anchor="mt")
    reveal_text(L, (W / 2, 390), "2-DAY SALES", B(190), WHITE, prog(tl, 0.45, 1.0), anchor="mt")
    reveal_text(L, (W / 2, 560), "MASTERCLASS", B(190), GOLD, prog(tl, 0.6, 1.15), anchor="mt")
    reveal_text(L, (W / 2, 770), "for LIC Development Officers", M(600, 46), WHITE, prog(tl, 0.9, 1.4), anchor="mt")
    L = shadow_of(L, 20, 180)
    if tl > 3.7: L.putalpha(L.split()[3].point(lambda v: int(v * (1 - prog(tl, 3.7, 4.0)))))
    img.alpha_composite(L)
    letterbox(img, 1)
    return img

# 8-12 THE COACH (portrait photo)
P1 = Photo(IMG + "1.jpg", 1.25, 1.42, (0.47, 0.42), (0.43, 0.38))
@seg(8, 12)
def s_coach(t):
    tl = t - 8
    img = P1.frame(tl, 4).convert("RGBA"); img.alpha_composite(VIG)
    L = text_layer(); d = ImageDraw.Draw(L)
    # right-side name plate
    x0 = 1080; p = eo(prog(tl, 0.25, 0.7))
    d.rectangle([x0 + 580 * (1 - p), 560, x0 + 660 + 140, 830], fill=NAVY + (225,))
    d.rectangle([x0 - 4 + 580 * (1 - p), 560, x0 + 8 + 580 * (1 - p), 830], fill=GOLD + (255,))
    L2 = text_layer()
    reveal_text(L2, (x0 + 40, 582), "THE MASTER SALES COACH", M(800, 26), GOLD_L, prog(tl, 0.55, 0.9))
    reveal_text(L2, (x0 + 36, 620), "Mr. Anurag Kesarwani", M(800, 54), WHITE, prog(tl, 0.65, 1.05))
    reveal_text(L2, (x0 + 40, 700), "Co-Founder, Wealth Tank", M(600, 34), WHITE, prog(tl, 0.8, 1.2))
    reveal_text(L2, (x0 + 40, 752), "MDRT Achiever  •  Sales Trainer", M(600, 30), GOLD_L, prog(tl, 0.95, 1.35))
    L.alpha_composite(L2)
    L = shadow_of(L, 18, 140)
    if tl > 3.7: L.putalpha(L.split()[3].point(lambda v: int(v * (1 - prog(tl, 3.7, 4.0)))))
    img.alpha_composite(L); bug(img)
    return img

# 12-18 SPEAKING at the board
C1b = Clip("src1.mp4", 4.2)
@seg(12, 18)
def s_speak(t):
    tl = t - 12
    z = 1.08 if tl < 3 else 1.28                     # punch-in on the beat at 15s
    cx = 0.36 if tl < 3 else 0.33
    img = zoom(C1b.frame(tl), z + 0.02 * (tl % 3), cx, 0.42).convert("RGBA"); img.alpha_composite(VIG)
    L = text_layer()
    caption(L, tl, 0.3, 2.95, "LIVE COACHING", "RECRUIT. TRAIN. GROW.", "Building a winning agency team")
    caption(L, tl, 3.1, 5.95, "THE TARGET", "RECRUITMENT DRIVE", "From today till 31 March 2027")
    img.alpha_composite(L); bug(img)
    return img

# 18-24 DATA: same hours, ten times the return
P3 = Photo(IMG + "3.jpg", 1.0, 1.12, (0.5, 0.45), (0.45, 0.42))
@seg(18, 24)
def s_data(t):
    tl = t - 18
    base = P3.frame(tl, 6)
    img = base.filter(ImageFilter.GaussianBlur(lerp(0, 14, eo(prog(tl, 0.3, 0.9))))).convert("RGBA")
    img.alpha_composite(Image.new("RGBA", (W, H), NAVY_D + (int(200 * eo(prog(tl, 0.3, 0.9))),)))
    L = text_layer(); d = ImageDraw.Draw(L)
    reveal_text(L, (W / 2, 120), "SAME HOURS.  TEN TIMES THE RETURN.", B(110), WHITE, prog(tl, 0.6, 1.1), anchor="mt")
    # two cards
    for i, (lab, val, sub, col, tstart) in enumerate([
            ("SALARIED JOB", 156, "160 hrs/month  •  ₹25,000 earned", (150, 190, 230), 0.9),
            ("FULL-TIME AGENT", 1575, "160 hrs/month  •  ₹2,52,000 first-year commission", GOLD, 1.4)]):
        p = back(prog(tl, tstart, tstart + 0.45))
        if p <= 0: continue
        cx = 520 if i == 0 else 1400
        w_, h_ = 760 * p, 470 * p
        d.rounded_rectangle([cx - w_ / 2, 560 - h_ / 2, cx + w_ / 2, 560 + h_ / 2], 26,
                            fill=(255, 255, 255, 24), outline=col + (255,), width=4)
        if p > 0.8:
            d.text((cx, 380), lab, font=M(800, 34), fill=col, anchor="mm")
            n = int(val * eo(prog(tl, tstart + 0.2, tstart + 1.9)))
            rtext(d, (cx, 520), f"₹{n:,}", 900, 150, WHITE if i == 0 else GOLD)
            d.text((cx, 625), "per hour", font=M(600, 34), fill=(220, 225, 240), anchor="mm")
            bw = (60 if i == 0 else 600) * eo(prog(tl, tstart + 0.2, tstart + 1.9))
            d.rounded_rectangle([cx - 300, 670, cx - 300 + max(bw, 2), 692], 11, fill=col + (255,))
            rtext(d, (cx, 745), sub, 600, 25, (220, 225, 240))
    pv = back(prog(tl, 1.2, 1.5))
    if pv > 0:
        r = 52 * pv; d.ellipse([W / 2 - 40 - r, 560 - r, W / 2 - 40 + r, 560 + r], fill=GOLD + (255,))
        d.text((W / 2 - 40, 560), "VS", font=B(56), fill=NAVY, anchor="mm")
    # 10x stamp
    ps = prog(tl, 3.4, 3.7)
    if ps > 0:
        s = lerp(2.2, 1.0, eo(ps))
        st = Image.new("RGBA", (520, 200), (0, 0, 0, 0)); sd = ImageDraw.Draw(st)
        sd.rounded_rectangle([30, 25, 490, 175], 20, fill=GOLD + (255,))
        sd.text((260, 100), "10X RETURN", font=B(110), fill=NAVY, anchor="mm")
        st = st.rotate(-4, resample=Image.BICUBIC, expand=False)
        sw, sh = int(520 * s), int(200 * s)
        st = st.resize((sw, sh), Image.BILINEAR)
        st.putalpha(st.split()[3].point(lambda v: int(v * min(1, ps * 2))))
        L.alpha_composite(st, (int(W / 2 - sw / 2), int(915 - sh / 2)))
    L = shadow_of(L, 16, 160)
    if tl > 5.7: L.putalpha(L.split()[3].point(lambda v: int(v * (1 - prog(tl, 5.7, 6.0)))))
    img.alpha_composite(L); bug(img)
    d2 = ImageDraw.Draw(img)
    d2.text((W - 40, H - 30), "Figures from the session presentation", font=M(600, 20), fill=(200, 205, 220, 200), anchor="rb")
    return img

# 24-28 FULL HOUSE
P2 = Photo(IMG + "2.jpg", 1.32, 1.0, (0.5, 0.42), (0.5, 0.5))
@seg(24, 28)
def s_house(t):
    tl = t - 24
    img = P2.frame(tl, 4).convert("RGBA"); img.alpha_composite(VIG)
    L = text_layer(); caption(L, tl, 0.3, 3.95, "DAY 1  •  DAY 2", "FULL HOUSE. FULL FOCUS.", "LIC Development Officers learning to win")
    img.alpha_composite(L); bug(img); return img

# 28-34 ACTIVITY (clip 3), slight speed ramp
C3 = Clip("src3.mp4", 0.3)
@seg(28, 34)
def s_act(t):
    tl = t - 28
    img = zoom(C3.frame(tl * 1.05), 1.05 + 0.03 * tl / 6, 0.55, 0.45).convert("RGBA"); img.alpha_composite(VIG)
    L = text_layer()
    caption(L, tl, 0.3, 2.95, "HANDS-ON", "LEARNING BY DOING", "Live team activities")
    caption(L, tl, 3.1, 5.95, "TEAMWORK", "EVERY OFFICER ENGAGED", "Practical skills you can use tomorrow")
    img.alpha_composite(L); bug(img); return img

# 34-40 ACTIVITY (clip 2 rotated)
C2 = Clip("src2.mp4", 2.55)
@seg(34, 40)
def s_act2(t):
    tl = t - 34
    img = zoom(C2.frame(tl), 1.12 + 0.03 * tl / 6, 0.47, 0.45).convert("RGBA"); img.alpha_composite(VIG)
    L = text_layer()
    caption(L, tl, 0.3, 2.95, "MASTER SALES COACH", "COACHING UP CLOSE", "Personal guidance for every participant")
    caption(L, tl, 3.1, 5.95, "MINDSET", "SELL THE CAREER", "Turning officers into recruiters and leaders")
    img.alpha_composite(L); bug(img); return img

# 40-44 LEADERS (photo 5)
P5 = Photo(IMG + "5.jpg", 1.08, 1.25, (0.5, 0.45), (0.62, 0.4))
@seg(40, 44)
def s_lead(t):
    tl = t - 40
    img = P5.frame(tl, 4).convert("RGBA"); img.alpha_composite(VIG)
    L = text_layer(); caption(L, tl, 0.3, 3.95, "THE NEXT GENERATION", "BUILDING LEADERS", "Recognising and inspiring talent")
    img.alpha_composite(L); bug(img); return img

# 44-48 QUOTE over presenting photo (photo 4), cinematic
P4 = Photo(IMG + "4.jpg", 1.0, 1.15, (0.55, 0.45), (0.62, 0.4))
@seg(44, 48)
def s_quote(t):
    tl = t - 44
    img = P4.frame(tl, 4).convert("RGBA")
    img.alpha_composite(Image.new("RGBA", (W, H), NAVY_D + (120,))); img.alpha_composite(VIG)
    L = text_layer(); d = ImageDraw.Draw(L)
    d.text((140, 250), "“", font=M(900, 260), fill=GOLD + (int(255 * prog(tl, 0.2, 0.5)),))
    reveal_text(L, (150, 430), "A LIFE-CHANGING", B(150), WHITE, prog(tl, 0.35, 0.8))
    reveal_text(L, (150, 570), "TWO DAYS", B(150), GOLD, prog(tl, 0.55, 1.0))
    reveal_text(L, (155, 740), "for every LIC Development Officer in the room", M(600, 38), WHITE, prog(tl, 0.8, 1.25))
    L = shadow_of(L, 18, 170)
    if tl > 3.7: L.putalpha(L.split()[3].point(lambda v: int(v * (1 - prog(tl, 3.7, 4.0)))))
    img.alpha_composite(L); letterbox(img, 1); return img

# 48-54 OUTRO
@seg(48, 54)
def s_outro(t):
    tl = t - 48
    img = navy_bg(t); img.alpha_composite(light_rays(t, 0.8)); img.alpha_composite(particles(t))
    p = back(prog(tl, 0.0, 0.5))
    size = max(4, int(420 * p))
    lg = LOGO.resize((size, size), Image.LANCZOS)
    if tl > 0.5: lg = shine(lg, prog(tl, 0.5, 1.3))
    img.alpha_composite(lg, (int(W / 2 - size / 2), int(330 - size / 2)))
    L = text_layer(); d = ImageDraw.Draw(L)
    reveal_text(L, (W / 2, 580), "TRAIN  •  RECRUIT  •  GROW", B(96), WHITE, prog(tl, 0.6, 1.1), anchor="mt")
    reveal_text(L, (W / 2, 700), "Insurance  •  Loans  •  Consulting  •  Sales Training", M(600, 38), GOLD_L, prog(tl, 0.8, 1.3), anchor="mt")
    pb = back(prog(tl, 1.3, 1.7))
    if pb > 0:
        bw, bh = 640 * pb, 92 * pb
        d.rounded_rectangle([W / 2 - bw / 2, 820 - bh / 2, W / 2 + bw / 2, 820 + bh / 2], int(bh / 2), fill=GOLD + (255,))
        if pb > 0.7: d.text((W / 2, 820), "SUBSCRIBE  •  SHARE  •  FOLLOW", font=M(800, 32), fill=NAVY, anchor="mm")
    L = shadow_of(L, 16, 150); img.alpha_composite(L)
    if tl > 5.0: img.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, int(255 * prog(tl, 5.0, 6.0)))))
    return img

# ---------------------------------------------------------------- transitions at cut points
def t_flash(a, b, p):
    out = (a if p < 0.5 else b).copy()
    out.alpha_composite(Image.new("RGBA", (W, H), (255, 250, 235, int(255 * (1 - abs(p - 0.5) * 2) ** 1.5))))
    return out

def smear(img, amount):
    if amount < 0.02: return img
    k = int(1 + 60 * amount)
    return img.resize((max(8, W // k), H), Image.BILINEAR).resize((W, H), Image.BILINEAR)

def t_whip(a, b, p, direction=1):
    e = eio(p); off = int(e * W) * direction
    blur = 1 - abs(p - 0.5) * 2
    A = smear(a, blur); Bm = smear(b, blur)
    out = Image.new("RGBA", (W, H))
    out.paste(A, (-off, 0))
    out.paste(Bm, (W * direction - off, 0))
    return out

def t_zoom(a, b, p):
    src = a if p < 0.5 else b
    q = p * 2 if p < 0.5 else (1 - p) * 2
    z = 1 + 0.6 * q ** 2
    img = zoom(src, z)
    if q > 0.1:
        small = img.resize((W // 6, H // 6), Image.BILINEAR).filter(ImageFilter.GaussianBlur(q * 4))
        img = Image.blend(img, small.resize((W, H), Image.BILINEAR), min(0.85, q))
    return img

def t_glitch(a, b, p):
    src = (a if p < 0.5 else b).convert("RGB")
    q = 1 - abs(p - 0.5) * 2
    arr = np.array(src)
    sh = int(40 * q)
    arr[..., 0] = np.roll(arr[..., 0], sh, 1); arr[..., 2] = np.roll(arr[..., 2], -sh, 1)
    r = np.random.default_rng(int(p * 1000))
    for _ in range(int(14 * q)):
        y = r.integers(0, H - 60); h = r.integers(8, 60)
        arr[y:y + h] = np.roll(arr[y:y + h], r.integers(-200, 200), 1)
    return Image.fromarray(arr).convert("RGBA")

def t_wipe(a, b, p):
    """Gold diagonal bars sweep across, revealing B (brand wipe)."""
    out = a.copy()
    e = eio(p)
    m = Image.new("L", (W, H), 0); d = ImageDraw.Draw(m)
    x = lerp(-700, W + 700, e)
    d.polygon([(x, 0), (x - 2000, 0), (x - 2000 - 500, H), (x - 500, H)], fill=255)
    out.paste(b, (0, 0), m)
    d2 = ImageDraw.Draw(out)
    for k, (wdt, col) in enumerate([(70, GOLD), (26, NAVY), (14, GOLD_L)]):
        xo = x + 20 + k * 80
        d2.polygon([(xo, 0), (xo + wdt, 0), (xo + wdt - 500, H), (xo - 500, H)], fill=col + (255,))
    return out

TRANS = {4.0: (t_flash, 0.5), 8.0: (t_whip, 0.5), 12.0: (t_whip, 0.5), 18.0: (t_glitch, 0.5),
         24.0: (t_wipe, 0.6), 28.0: (t_zoom, 0.5), 34.0: (t_glitch, 0.5), 40.0: (t_wipe, 0.6),
         44.0: (t_zoom, 0.5), 48.0: (t_flash, 0.6)}

def seg_at(t):
    for a, b, fn in SEG:
        if a <= t < b: return a, b, fn
    return SEG[-1]

def render(t):
    for c, (fn, d) in TRANS.items():
        if c - d / 2 <= t < c + d / 2:
            p = (t - (c - d / 2)) / d
            A = seg_at(c - 1e-3)[2](t); Bf = seg_at(c)[2](t)
            return fn(A, Bf, p)
    return seg_at(t)[2](t)

def grain(img, t):
    n = (np.random.default_rng(int(t * 30)).standard_normal((H // 2, W // 2)) * 6).astype(np.int16)
    n = np.repeat(np.repeat(n, 2, 0), 2, 1)
    arr = np.array(img.convert("RGB"), dtype=np.int16) + n[..., None]
    return np.clip(arr, 0, 255).astype(np.uint8)

if ONLY:
    for tt in ONLY:
        Image.fromarray(grain(render(tt), tt)).resize((960, 540)).save(f"frames/prev_{tt:05.2f}.jpg", quality=88)
    sys.exit()

enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                        "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "17",
                        "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", OUT],
                       stdin=subprocess.PIPE)
NF = int(DUR * FPS)
for i in range(NF):
    t = i / FPS
    enc.stdin.write(grain(render(t), t).tobytes())
    if i % 150 == 0: print(f"{t:.1f}s", flush=True)
enc.stdin.close(); enc.wait()
print("done")
