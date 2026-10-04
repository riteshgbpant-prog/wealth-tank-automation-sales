"""Wealth Tank event-video engine: timeline of photos / clips / graphic cards, transitions, Hinglish kinetic captions.
Works for 16:9 (1920x1080) and 9:16 (1080x1920). A timeline module defines SEGMENTS and TRANSITIONS."""
import subprocess, math, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops, ImageOps, ImageEnhance

FPS = 30
PREVDIR = "prev"
NAVY = (6, 30, 98); NAVY_D = (3, 14, 44); GOLD = (240, 186, 40); GOLD_L = (255, 215, 110); WHITE = (255, 255, 255)
ORANGE = (226, 132, 32)
_fc = {}
def _font(path, s):
    k = (path, s)
    if k not in _fc: _fc[k] = ImageFont.truetype(path, s)
    return _fc[k]
def M(w, s): return _font(f"fonts/Montserrat-{w}.ttf", int(s))
def MX(w, s): return _font(f"fonts/MontserratExt-{w}.ttf", int(s))
def B(s): return _font("fonts/BebasNeue.ttf", int(s))

def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def prog(t, a, b): return clamp((t - a) / (b - a)) if b > a else float(t >= a)
def eo(x): return 1 - (1 - x) ** 3
def ei(x): return x ** 3
def eio(x): return 3 * x * x - 2 * x * x * x
def back(x, s=1.7): x -= 1; return x * x * ((s + 1) * x + s) + 1
def lerp(a, b, x): return a + (b - a) * x


class Canvas:
    """Holds output size + cached overlays."""
    def __init__(self, W, H):
        self.W, self.H = W, H
        self.S = min(W, H) / 1080.0           # text scale unit
        self.vert = H > W
        y, x = np.ogrid[:H, :W]
        d = np.sqrt(((x - W / 2) / (W * 0.62)) ** 2 + ((y - H / 2) / (H * 0.62)) ** 2)
        v = np.zeros((H, W, 4), np.uint8); v[..., 3] = (np.clip(d - 0.6, 0, 1) * 170).astype(np.uint8)
        self.VIG = Image.fromarray(v, "RGBA")
        # caption scrim (bottom-left for 16:9, bottom for 9:16)
        if self.vert:
            a = np.clip((y / H - 0.55) / 0.45, 0, 1) ** 1.1 * 225 + 0 * x
        else:
            a = np.clip((y / H - 0.5) / 0.5, 0, 1) ** 1.2 * np.clip(1.25 - x / W * 1.3, 0, 1) * 215
        self.SCRIM_A = Image.fromarray(a.astype(np.uint8), "L")
        self.SCRIM_RGB = Image.new("RGBA", (W, H), NAVY_D + (255,))
        self.LOGO = Image.open("logo_real.png").convert("RGBA")
        self._logo_cache = {}
        r = np.random.default_rng(3)
        self.PARTS = [(r.uniform(0, W), r.uniform(0, H), r.uniform(2, 7) * self.S, r.uniform(10, 60), r.uniform(0, 6.28)) for _ in range(90)]

    def logo(self, size):
        size = max(4, int(size))
        if size not in self._logo_cache:
            if len(self._logo_cache) > 40: self._logo_cache.clear()
            self._logo_cache[size] = self.LOGO.resize((size, size), Image.LANCZOS)
        return self._logo_cache[size]

    def layer(self): return Image.new("RGBA", (self.W, self.H), (0, 0, 0, 0))

    # ---------- backgrounds ----------
    def navy_bg(self, t):
        W, H = self.W, self.H
        y, x = np.ogrid[:H, :W]
        cx = W / 2 + 0.06 * W * math.sin(t * 0.7)
        d = np.sqrt(((x - cx) / W) ** 2 + ((y - H / 2) / H) ** 2)
        k = np.clip(1 - d * 1.5, 0, 1)[..., None]
        rgb = np.array(NAVY_D)[None, None] + (np.array((14, 48, 130)) - np.array(NAVY_D))[None, None] * k
        return Image.fromarray(rgb.astype(np.uint8), "RGB").convert("RGBA")

    def particles(self, t, alpha=1.0):
        L = self.layer(); d = ImageDraw.Draw(L)
        for x, y, r, sp, ph in self.PARTS:
            yy = (y - sp * t * 3) % self.H; xx = x + 25 * math.sin(t * 0.8 + ph)
            a = int(255 * alpha * (0.35 + 0.65 * (0.5 + 0.5 * math.sin(t * 2 + ph))))
            d.ellipse([xx - r, yy - r, xx + r, yy + r], fill=GOLD_L + (a // 2,))
        return L.filter(ImageFilter.GaussianBlur(2))

    def rays(self, t, a):
        L = self.layer(); d = ImageDraw.Draw(L); cx, cy = self.W / 2, self.H / 2; R = max(self.W, self.H)
        for k in range(14):
            ang = k * 2 * math.pi / 14 + t * 0.25
            d.polygon([(cx, cy), (cx + R * math.cos(ang - .05), cy + R * math.sin(ang - .05)),
                       (cx + R * math.cos(ang + .05), cy + R * math.sin(ang + .05))], fill=GOLD + (int(40 * a),))
        return L.filter(ImageFilter.GaussianBlur(18))

    # ---------- text helpers ----------
    def reveal(self, L, xy, txt, font, fill, p, anchor="la", dist=60):
        if p <= 0: return
        tmp = self.layer(); d = ImageDraw.Draw(tmp)
        x, y = xy; d.text((x, y + (1 - eo(p)) * dist * self.S), txt, font=font, fill=fill, anchor=anchor)
        bb = d.textbbox(xy, txt, font=font, anchor=anchor)
        m = Image.new("L", (self.W, self.H), 0)
        ImageDraw.Draw(m).rectangle([bb[0] - 40, bb[1] - 30, bb[2] + 40, bb[3] + 20], fill=255)
        tmp.putalpha(ImageChops.multiply(tmp.split()[3], m)); L.alpha_composite(tmp)

    def rtext(self, d, xy, txt, w, size, fill, anchor="mm"):
        """Montserrat text with ₹ taken from latin-ext; anchor mm or lm."""
        parts = [(ch, MX(w, size) if ch == "₹" else M(w, size)) for ch in txt]
        total = sum(d.textlength(ch, font=f) for ch, f in parts)
        x = xy[0] - (total / 2 if anchor == "mm" else 0)
        for ch, f in parts:
            d.text((x, xy[1]), ch, font=f, fill=fill, anchor="lm"); x += d.textlength(ch, font=f)

    def shadow(self, L, blur=16, alpha=150, off=(0, 6)):
        a = L.split()[3].point(lambda v: v * alpha // 255).filter(ImageFilter.GaussianBlur(blur))
        s = self.layer(); s.putalpha(a); out = self.layer(); out.alpha_composite(s, off); out.alpha_composite(L); return out

    def fade(self, L, a):
        if a >= 1: return L
        L.putalpha(L.split()[3].point(lambda v: int(v * max(0, a)))); return L

    def fit_text(self, d, txt, font_fn, size, maxw):
        while size > 20 and d.textlength(txt, font=font_fn(size)) > maxw: size -= 4
        return font_fn(size)

    def caption(self, L, t, t0, t1, kicker, line, sub=None):
        """Gold kicker tag + big Bebas headline + sub line, with scrim; bottom-left (16:9) / lower-centre (9:16)."""
        if not (t0 - 0.01 <= t <= t1): return
        S = self.S; W, H = self.W, self.H
        out = eo(prog(t, t1 - 0.3, t1))
        a_in = eo(prog(t, t0, t0 + 0.4)) * (1 - out)
        sc = self.SCRIM_RGB.copy(); sc.putalpha(self.SCRIM_A.point(lambda v: int(v * a_in))); L.alpha_composite(sc)
        C = self.layer(); d = ImageDraw.Draw(C)
        if self.vert:
            x = 70 - out * 60; y = H - 640; maxw = W - 140; big = 150
        else:
            x = 110 - out * 80; y = 700; maxw = W * 0.62; big = 128
        pk = prog(t, t0, t0 + 0.35)
        if pk > 0 and kicker:
            fk = M(800, 30 * S); tw = d.textlength(kicker, font=fk); bw = (tw + 44 * S) * eo(pk)
            d.rectangle([x, y, x + bw, y + 50 * S], fill=GOLD + (255,))
            if pk > 0.5: d.text((x + 22 * S, y + 9 * S), kicker, font=fk, fill=NAVY)
        fb = self.fit_text(d, line, B, big * S, maxw)
        self.reveal(C, (x - 4, y + 64 * S), line, fb, WHITE, prog(t, t0 + 0.15, t0 + 0.6))
        if sub:
            fs = self.fit_text(d, sub, lambda s: M(600, s), 38 * S, maxw)
            self.reveal(C, (x, y + 64 * S + fb.size * 1.05), sub, fs, GOLD_L, prog(t, t0 + 0.35, t0 + 0.8))
        C = self.shadow(C, 18, 170)
        if out > 0: C = self.fade(C, 1 - out)
        L.alpha_composite(C)

    def bug(self, img, a=1.0):
        sm = self.logo(140 * self.S).copy()
        if a < 1: sm.putalpha(sm.split()[3].point(lambda v: int(v * a)))
        img.alpha_composite(sm, (int(self.W - 175 * self.S), int(self.H * 0.105 + 12 * self.S) if self.W > self.H else int(60 * self.S)))

    def letterbox(self, img, a=1):
        h = int(70 * a * self.S); d = ImageDraw.Draw(img)
        d.rectangle([0, 0, self.W, h], fill=(0, 0, 0, 255)); d.rectangle([0, self.H - h, self.W, self.H], fill=(0, 0, 0, 255))

    def name_plate(self, L, t, t0, t1, role, name, line2, line3=None, side="right"):
        """Big lower-third name card for a co-founder."""
        if not (t0 <= t <= t1): return
        S = self.S; W, H = self.W, self.H
        p = eo(prog(t, t0, t0 + 0.45)); out = ei(prog(t, t1 - 0.35, t1))
        if self.vert:
            w, h = W - 120, 330 * S; x0, y0 = 60, H - 560
        else:
            w, h = 780, 290; x0 = W - w - 70 if side == "right" else 70; y0 = H - h - 160
        off = (1 - p) * w * 0.6 + out * w * 0.6
        P = self.layer(); d = ImageDraw.Draw(P)
        d.rectangle([x0 + off, y0, x0 + off + w, y0 + h], fill=NAVY + (232,))
        d.rectangle([x0 + off - 6, y0, x0 + off + 10, y0 + h], fill=GOLD + (255,))
        T = self.layer()
        tx = x0 + 44 * S
        self.reveal(T, (tx, y0 + 26 * S), role, M(800, 26 * S), GOLD_L, prog(t, t0 + 0.3, t0 + 0.7))
        self.reveal(T, (tx - 2, y0 + 64 * S), name, M(800, 62 * S), WHITE, prog(t, t0 + 0.4, t0 + 0.85))
        self.reveal(T, (tx, y0 + 150 * S), line2, M(600, 30 * S), WHITE, prog(t, t0 + 0.55, t0 + 1.0))
        if line3: self.reveal(T, (tx, y0 + 198 * S), line3, M(700, 30 * S), GOLD_L, prog(t, t0 + 0.7, t0 + 1.15))
        P.alpha_composite(T); P = self.shadow(P, 18, 140)
        if out > 0: P = self.fade(P, 1 - out)
        L.alpha_composite(P)

    def frame_out(self, img):
        return np.asarray(img.convert("RGB"))


# ---------------------------------------------------------------- media sources
class Clip:
    """Sequential frame reader for a pre-scaled intermediate (must match canvas size)."""
    def __init__(self, path, src_start, speed=1.0):
        self.path, self.s0, self.speed = path, src_start, speed
        self.p = None; self.idx = -1; self.last = None; self.size = None
    def frame(self, tl, W, H):
        want = max(0, int(round((self.s0 + tl * self.speed) * FPS)))
        if self.p is None:
            st = max(0.0, self.s0 - 0.6)
            self.p = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", f"{st:.3f}", "-i", self.path,
                                       "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
            self.idx = int(round(st * FPS)) - 1
        while self.idx < want:
            buf = self.p.stdout.read(W * H * 3)
            if len(buf) < W * H * 3: break
            self.last = buf; self.idx += 1
        return Image.frombuffer("RGB", (W, H), self.last)


_photo_cache = {}
def load_photo(path, maxside=2600):
    if path not in _photo_cache:
        im = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
        im.thumbnail((maxside, maxside), Image.LANCZOS)
        im = ImageEnhance.Contrast(im).enhance(1.06); im = ImageEnhance.Color(im).enhance(1.12)
        _photo_cache[path] = im
    return _photo_cache[path]


def photo_frame(cv, path, tl, dur, z0=1.0, z1=1.12, c0=(0.5, 0.5), c1=(0.5, 0.5), fill="crop"):
    """Ken Burns. fill='crop' covers the frame; fill='blur' shows the whole photo over a blurred copy."""
    im = load_photo(path); W, H = cv.W, cv.H
    x = clamp(tl / dur, -0.2, 1.2)
    z = max(1.0, lerp(z0, z1, x)); cx = lerp(c0[0], c1[0], x); cy = lerp(c0[1], c1[1], x)
    iw, ih = im.size
    if fill == "blur":
        key = ("bg", path, W, H)
        if key not in _photo_cache:
            bg = ImageOps.fit(im, (W // 4, H // 4)).filter(ImageFilter.GaussianBlur(10)).resize((W, H), Image.BILINEAR)
            _photo_cache[key] = ImageEnhance.Brightness(bg).enhance(0.6)
        out = _photo_cache[key].copy()
        s = min(W / iw, H / ih) * 0.92 * z
        fw, fh = int(iw * s), int(ih * s)
        fg = im.resize((fw, fh), Image.BILINEAR)
        out.paste(fg, (int(W / 2 - fw / 2 + (cx - 0.5) * 0), int(H / 2 - fh / 2)))
        return out
    ar = W / H
    cw = iw / z; ch = cw / ar
    if ch > ih / z: ch = ih / z; cw = ch * ar
    cw, ch = min(cw, iw), min(ch, ih)
    x0 = clamp(cx * iw - cw / 2, 0, iw - cw); y0 = clamp(cy * ih - ch / 2, 0, ih - ch)
    return im.resize((W, H), Image.BILINEAR, box=(x0, y0, x0 + cw, y0 + ch))


def zoom(cv, img, z, cx=0.5, cy=0.5):
    if z <= 1.001: return img
    W, H = cv.W, cv.H; cw, ch = W / z, H / z
    x0 = clamp(cx * W - cw / 2, 0, W - cw); y0 = clamp(cy * H - ch / 2, 0, H - ch)
    return img.resize((W, H), Image.BILINEAR, box=(x0, y0, x0 + cw, y0 + ch))


# ---------------------------------------------------------------- transitions
def t_flash(cv, a, b, p):
    out = (a if p < 0.5 else b).copy()
    out.alpha_composite(Image.new("RGBA", (cv.W, cv.H), (255, 250, 235, int(255 * (1 - abs(p - 0.5) * 2) ** 1.5)))); return out

def _smear(cv, img, amount, vertical=False):
    if amount < 0.02: return img
    k = int(1 + 60 * amount)
    if vertical: return img.resize((cv.W, max(8, cv.H // k)), Image.BILINEAR).resize((cv.W, cv.H), Image.BILINEAR)
    return img.resize((max(8, cv.W // k), cv.H), Image.BILINEAR).resize((cv.W, cv.H), Image.BILINEAR)

def t_whip(cv, a, b, p):
    e = eio(p); blur = 1 - abs(p - 0.5) * 2
    if cv.vert:
        off = int(e * cv.H); out = Image.new("RGBA", (cv.W, cv.H))
        out.paste(_smear(cv, a, blur, True), (0, -off)); out.paste(_smear(cv, b, blur, True), (0, cv.H - off)); return out
    off = int(e * cv.W); out = Image.new("RGBA", (cv.W, cv.H))
    out.paste(_smear(cv, a, blur), (-off, 0)); out.paste(_smear(cv, b, blur), (cv.W - off, 0)); return out

def t_zoom(cv, a, b, p):
    src = a if p < 0.5 else b; q = p * 2 if p < 0.5 else (1 - p) * 2
    img = zoom(cv, src, 1 + 0.6 * q ** 2)
    if q > 0.1:
        small = img.resize((cv.W // 6, cv.H // 6), Image.BILINEAR).filter(ImageFilter.GaussianBlur(q * 4))
        img = Image.blend(img, small.resize((cv.W, cv.H), Image.BILINEAR), min(0.85, q))
    return img

def t_glitch(cv, a, b, p):
    src = (a if p < 0.5 else b).convert("RGB"); q = 1 - abs(p - 0.5) * 2
    arr = np.array(src); sh = int(40 * q)
    arr[..., 0] = np.roll(arr[..., 0], sh, 1); arr[..., 2] = np.roll(arr[..., 2], -sh, 1)
    r = np.random.default_rng(int(p * 1000))
    for _ in range(int(14 * q)):
        y = r.integers(0, cv.H - 60); h = r.integers(8, 60)
        arr[y:y + h] = np.roll(arr[y:y + h], r.integers(-200, 200), 1)
    return Image.fromarray(arr).convert("RGBA")

def t_wipe(cv, a, b, p):
    out = a.copy(); e = eio(p); W, H = cv.W, cv.H; sl = H * 0.46
    m = Image.new("L", (W, H), 0); d = ImageDraw.Draw(m); x = lerp(-sl - 200, W + sl + 200, e)
    d.polygon([(x, 0), (x - W - 2000, 0), (x - W - 2000 - sl, H), (x - sl, H)], fill=255)
    out.paste(b, (0, 0), m); d2 = ImageDraw.Draw(out)
    for k, (wd, col) in enumerate([(70, GOLD), (26, NAVY), (14, GOLD_L)]):
        xo = x + 20 + k * 80
        d2.polygon([(xo, 0), (xo + wd, 0), (xo + wd - sl, H), (xo - sl, H)], fill=col + (255,))
    return out

def t_cut(cv, a, b, p): return a if p < 0.5 else b

def t_iris(cv, a, b, p):
    """Circle reveal of B from centre with a glowing gold ring."""
    W, H = cv.W, cv.H; e = eio(p); R = math.hypot(W, H) / 2 * 1.05; r = max(1, R * e)
    out = a.copy(); m = Image.new("L", (W, H), 0)
    ImageDraw.Draw(m).ellipse([W / 2 - r, H / 2 - r, W / 2 + r, H / 2 + r], fill=255)
    out.paste(zoom(cv, b, 1 + 0.15 * (1 - e)), (0, 0), m)
    ring = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ring); w = int(18 * cv.S)
    d.ellipse([W / 2 - r, H / 2 - r, W / 2 + r, H / 2 + r], outline=GOLD + (255,), width=w)
    out.alpha_composite(ring.filter(ImageFilter.GaussianBlur(6))); out.alpha_composite(ring)
    return out

def t_panels(cv, a, b, p):
    """B slides in as staggered vertical (or horizontal) strips with gold edges."""
    W, H = cv.W, cv.H; n = 6; out = a.copy(); d = ImageDraw.Draw(out)
    for i in range(n):
        q = eio(clamp((p - i * 0.07) / (1 - (n - 1) * 0.07)))
        if q <= 0: continue
        if cv.vert:
            y0, y1 = int(i * H / n), int((i + 1) * H / n); off = int((1 - q) * W) * (1 if i % 2 else -1)
            out.paste(b.crop((0, y0, W, y1)), (off, y0))
            if 0 < q < 1: d.rectangle([off - 6 if off > 0 else off + W, y0, (off if off > 0 else off + W) + 6, y1], fill=GOLD + (255,))
        else:
            x0, x1 = int(i * W / n), int((i + 1) * W / n); off = int((1 - q) * H) * (1 if i % 2 else -1)
            out.paste(b.crop((x0, 0, x1, H)), (x0, off))
            if 0 < q < 1:
                ey = off if off > 0 else off + H
                d.rectangle([x0, ey - 5, x1, ey + 5], fill=GOLD + (255,))
    return out

def t_spin(cv, a, b, p):
    """Rotational zoom-blur whip."""
    src = a if p < 0.5 else b; q = p * 2 if p < 0.5 else (1 - p) * 2
    ang = (1 if p < 0.5 else -1) * 25 * q ** 2
    img = zoom(cv, src, 1 + 0.5 * q ** 2).rotate(ang, resample=Image.BILINEAR)
    acc = np.asarray(img, dtype=np.float32)
    for k in (1, 2, 3):
        acc = acc + np.asarray(zoom(cv, src, 1 + 0.5 * q ** 2 + 0.04 * k * q).rotate(ang * (1 + 0.15 * k), resample=Image.BILINEAR), dtype=np.float32)
    return Image.fromarray((acc / 4).astype(np.uint8), "RGBA")

def t_leak(cv, a, b, p):
    """Warm film light-leak burn between shots."""
    W, H = cv.W, cv.H; src = (a if p < 0.5 else b).copy(); q = 1 - abs(p - 0.5) * 2
    key = ("leak", W, H)
    if key not in _photo_cache:
        y, x = np.ogrid[:H, :W]; L = np.zeros((H, W, 3), np.float32)
        for cx, cy, r, col in [(0.15, 0.3, 0.55, (255, 140, 40)), (0.85, 0.7, 0.6, (255, 60, 90)), (0.5, 0.5, 0.45, (255, 220, 150))]:
            g = np.exp(-(((x / W - cx) ** 2 + (y / H - cy) ** 2) / (r * r * 0.25)))[..., None]
            L += g * np.array(col, np.float32)
        _photo_cache[key] = np.clip(L, 0, 255)
    leak = _photo_cache[key]; shift = int((p - 0.5) * W * 0.4)
    leak = np.roll(leak, shift, axis=1)
    base = np.asarray(src.convert("RGB"), dtype=np.float32) / 255
    scr = 1 - (1 - base) * (1 - leak / 255 * min(1, q * 1.4))
    return Image.fromarray((np.clip(scr, 0, 1) * 255).astype(np.uint8)).convert("RGBA")

TRANS_FN = {"flash": t_flash, "whip": t_whip, "zoom": t_zoom, "glitch": t_glitch, "wipe": t_wipe, "cut": t_cut,
            "iris": t_iris, "panels": t_panels, "spin": t_spin, "leak": t_leak}


# ---------------------------------------------------------------- render loop
def grain(cv, img, t):
    n = (np.random.default_rng(int(t * 30)).standard_normal((cv.H // 2, cv.W // 2)) * 5).astype(np.int16)
    n = np.repeat(np.repeat(n, 2, 0), 2, 1)
    return np.clip(np.asarray(img.convert("RGB"), dtype=np.int16) + n[..., None], 0, 255).astype(np.uint8)

def run(cv, segments, transitions, dur, out_path, preview=None, t_from=0.0, t_to=None):
    """segments: list of (start, end, fn(t)->RGBA). transitions: {cut_time: (name, duration)}."""
    def seg_at(t):
        for a, b, fn in segments:
            if a <= t < b: return fn
        return segments[-1][2]
    def render(t):
        for c, (name, d) in transitions.items():
            if c - d / 2 <= t < c + d / 2:
                p = (t - (c - d / 2)) / d
                return TRANS_FN[name](cv, seg_at(c - 1e-3)(t), seg_at(c)(t), p)
        return seg_at(t)(t)
    if preview:
        for tt in preview:
            Image.fromarray(grain(cv, render(tt), tt)).resize((cv.W // 2, cv.H // 2)).save(f"{PREVDIR}/p_{tt:06.2f}.jpg", quality=86)
        return
    t_to = dur if t_to is None else t_to
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{cv.W}x{cv.H}",
                            "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "17",
                            "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", out_path],
                           stdin=subprocess.PIPE)
    n0, n1 = int(round(t_from * FPS)), int(round(t_to * FPS))
    for i in range(n0, n1):
        t = i / FPS
        enc.stdin.write(grain(cv, render(t), t).tobytes())
        if i % 300 == 0: print(f"{t:.1f}s", flush=True)
    enc.stdin.close(); enc.wait(); print("done", out_path)
