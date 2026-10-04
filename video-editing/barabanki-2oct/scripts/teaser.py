"""Cinematic teaser toolkit: grade, letterbox, flares, beat shake, text slams, photo bursts, slide slams, countdown."""
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops
from engine import *
import engine
from cards import load_photo, photo_frame, zoom, SLIDE, RAW, IMG
_cache = engine._photo_cache

# ---------------- look ----------------
_x = np.arange(256) / 255.0
_s = np.clip(0.5 + (_x - 0.5) * 1.12, 0, 1)                         # contrast
LUT_R = (np.clip(_s + 0.06 * _s ** 2 - 0.02 * (1 - _s), 0, 1) * 255).astype(np.uint8)   # warm highlights
LUT_G = (np.clip(_s * 1.0, 0, 1) * 255).astype(np.uint8)
LUT_B = (np.clip(_s + 0.07 * (1 - _s) ** 2 - 0.05 * _s ** 2, 0, 1) * 255).astype(np.uint8)  # teal shadows

def grade(img):
    a = np.asarray(img.convert("RGB"))
    out = np.stack([LUT_R[a[..., 0]], LUT_G[a[..., 1]], LUT_B[a[..., 2]]], -1)
    return Image.fromarray(out).convert("RGBA")

def bars(cv, img, a=1.0):
    if cv.vert: return
    h = int(cv.H * 0.105 * a); d = ImageDraw.Draw(img)
    d.rectangle([0, 0, cv.W, h], fill=(0, 0, 0, 255)); d.rectangle([0, cv.H - h, cv.W, cv.H], fill=(0, 0, 0, 255))

def flare(cv, img, x, y, strength=1.0):
    """Anamorphic horizontal streak + glow, screen-blended."""
    W, H = cv.W, cv.H; key = ("flare", W, H)
    if key not in _cache:
        L = Image.new("RGB", (W * 2, H * 2), (0, 0, 0)); d = ImageDraw.Draw(L)
        cx, cy = W, H
        d.ellipse([cx - 90, cy - 90, cx + 90, cy + 90], fill=(255, 230, 190))
        d.rectangle([0, cy - 5, W * 2, cy + 5], fill=(120, 190, 255))
        d.rectangle([cx - W * 0.6, cy - 2, cx + W * 0.6, cy + 2], fill=(255, 255, 255))
        L = L.filter(ImageFilter.GaussianBlur(10))
        for k, (r, col) in enumerate([(26, (255, 200, 120)), (14, (120, 200, 255)), (40, (255, 140, 60))]):
            px = cx - (k + 1) * 260
            d2 = ImageDraw.Draw(L); d2.ellipse([px - r, cy - r, px + r, cy + r], outline=col, width=4)
        _cache[key] = np.asarray(L.filter(ImageFilter.GaussianBlur(3)), dtype=np.float32) / 255
    F = _cache[key]
    x, y = clamp(x, 0, W), clamp(y, 0, H)
    x0, y0 = int(W - x), int(H - y)
    crop = F[y0:y0 + H, x0:x0 + W] * strength
    base = np.asarray(img.convert("RGB"), dtype=np.float32) / 255
    out = 1 - (1 - base) * (1 - np.clip(crop, 0, 1))
    return Image.fromarray((out * 255).astype(np.uint8)).convert("RGBA")

def chroma(img, amt):
    if amt < 1: return img
    a = np.array(img.convert("RGB")); s = int(amt)
    a[..., 0] = np.roll(a[..., 0], s, 1); a[..., 2] = np.roll(a[..., 2], -s, 1)
    return Image.fromarray(a).convert("RGBA")

def shake(img, t, hits, amp=18):
    """Decaying camera shake after each beat hit time."""
    k = 0.0
    for h in hits:
        if 0 <= t - h < 0.25: k = max(k, (1 - (t - h) / 0.25) * amp)
    if k < 0.5: return img
    r = np.random.default_rng(int(t * 1000))
    return ImageChops.offset(img, int(r.uniform(-k, k)), int(r.uniform(-k, k)))

def slam_text(cv, L, t, t0, txt, size, y, col=WHITE, font=None, ring=True):
    """Text slams in from 1.6x with blur, plus a shockwave ring."""
    if t < t0: return
    S = cv.S; p = prog(t, t0, t0 + 0.18)
    sc = lerp(1.7, 1.0, eo(p)); a = int(255 * min(1, p * 2.5))
    f = font or B(size * S)
    tmp = Image.new("RGBA", (cv.W, int(size * S * 1.6)), (0, 0, 0, 0)); d = ImageDraw.Draw(tmp)
    d.text((cv.W / 2, tmp.height / 2), txt, font=f, fill=col + (a,), anchor="mm")
    if sc != 1.0:
        tmp = tmp.resize((int(tmp.width * sc), int(tmp.height * sc)), Image.BILINEAR)
        if p < 0.8: tmp = tmp.filter(ImageFilter.GaussianBlur((1 - p) * 8))
    L.alpha_composite(tmp, (int(cv.W / 2 - tmp.width / 2), int(y - tmp.height / 2)))
    if ring:
        q = prog(t, t0, t0 + 0.5)
        if 0 < q < 1:
            R = lerp(60, cv.W * 0.55, eo(q)) * S; dd = ImageDraw.Draw(L)
            dd.ellipse([cv.W / 2 - R, y - R * 0.35, cv.W / 2 + R, y + R * 0.35], outline=GOLD + (int(220 * (1 - q)),), width=max(2, int(10 * (1 - q) * S)))


def tag(cv, img, t, info):
    """Top-left designation tag (logo + name + designation) shown whenever the speaker is on screen."""
    if not info: return
    name, desig = info; S = cv.S
    p = eo(prog(t, 0.15, 0.55))
    if p <= 0: return
    x = 40 * S; y = (cv.H * 0.105 + 22 * S) if not cv.vert else 150 * S
    L = cv.layer(); d = ImageDraw.Draw(L)
    fn, fd = M(800, 30 * S), M(600, 21 * S)
    w = max(d.textlength(name, font=fn), d.textlength(desig, font=fd)) + 150 * S
    h = 92 * S; ww = w * p
    d.rounded_rectangle([x, y, x + ww, y + h], 12, fill=NAVY + (225,))
    d.rectangle([x, y, x + 8 * S, y + h], fill=GOLD + (255,))
    if p > 0.6:
        lg = cv.logo(76 * S); L.alpha_composite(lg, (int(x + 18 * S), int(y + h / 2 - lg.height / 2)))
        d.text((x + 108 * S, y + 14 * S), name, font=fn, fill=WHITE)
        d.text((x + 108 * S, y + 54 * S), desig, font=fd, fill=GOLD_L)
    img.alpha_composite(L)


# ---------------- segments ----------------
def cold_open(cv, t0, dur, lines):
    """lines: [(time_offset, text, size, colour)] slammed on black with drifting dust; last line stays."""
    W, H, S = cv.W, cv.H, cv.S
    def fn(t):
        tl = t - t0
        img = Image.new("RGBA", (W, H), (4, 6, 14, 255))
        img.alpha_composite(cv.particles(t, 0.35))
        L = cv.layer()
        cur = [ln for ln in lines if tl >= ln[0]]
        last = lines[-1][0]
        if cur:
            off, txt, size, col = cur[-1]
            ty = H / 2 if off < last else lerp(H / 2, H * (0.70 if not cv.vert else 0.64), eio(prog(tl, last + 0.5, last + 1.1)))
            slam_text(cv, L, tl, off, txt, size, ty, col, ring=(off < last))
        pl = eo(prog(tl, last + 0.5, last + 1.3))
        if pl > 0:
            sz = (300 if not cv.vert else 420) * S
            gl = Image.new("RGBA", (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(gl)
            cy = H * (0.40 if not cv.vert else 0.40) + (1 - pl) * 60 * S
            gd.ellipse([W / 2 - sz * 0.75, cy - sz * 0.75, W / 2 + sz * 0.75, cy + sz * 0.75], fill=GOLD + (int(110 * pl),))
            img.alpha_composite(gl.filter(ImageFilter.GaussianBlur(60 * S)))
            lg = cv.logo(sz).copy(); lg.putalpha(lg.split()[3].point(lambda v: int(v * pl)))
            img.alpha_composite(lg, (int(W / 2 - lg.width / 2), int(cy - lg.height / 2)))
            img = flare(cv, img, lerp(-0.2, 1.2, prog(tl, last + 0.6, last + 2.2)) * W, cy, 0.6 * pl)
            if len(cur) >= 2 and tl - off < 0.12:                      # previous word flashes out
                pass
        img.alpha_composite(L)
        hits = [ln[0] for ln in lines]
        img = shake(img, tl, hits, 14 * S)
        if any(0 <= tl - h < 0.06 for h in hits):
            img.alpha_composite(Image.new("RGBA", (W, H), (255, 240, 220, 120)))
        bars(cv, img)
        return img
    return fn


def burst(cv, t0, dur, photos, beat=0.5, caption=None, big=None, flare_on=True):
    """Fast beat-synced photo montage: each photo punches in, flashes, chroma-splits."""
    W, H, S = cv.W, cv.H, cv.S
    n = max(1, int(round(dur / beat)))
    def fn(t):
        tl = t - t0; i = min(n - 1, int(tl / beat)); lt = tl - i * beat
        path = photos[i % len(photos)]
        img = grade(photo_frame(cv, path, lt, beat, 1.18, 1.04, (0.5, 0.48), (0.5, 0.5)))
        if lt < 0.07: img = chroma(img, (0.07 - lt) / 0.07 * 22 * S)
        img.alpha_composite(cv.VIG)
        if flare_on:
            img = flare(cv, img, lerp(-0.2, 1.2, tl / dur) * W, H * 0.32, 0.55)
        if lt < 0.05: img.alpha_composite(Image.new("RGBA", (W, H), (255, 250, 240, 150)))
        L = cv.layer()
        if big: slam_text(cv, L, tl, 0.0, big[0], big[1], H * (0.5 if not cv.vert else 0.42), big[2] if len(big) > 2 else WHITE, ring=False)
        if caption: cv.caption(L, tl, 0.1, dur - 0.05, *caption)
        img.alpha_composite(cv.shadow(L, 14, 160) if big else L)
        img = shake(img, tl, [k * beat for k in range(n)], 8 * S)
        bars(cv, img); cv.bug(img)
        return img
    return fn


def cine_photo(cv, t0, dur, items, caption=None, plate=None, speed=1.0, who=None):
    """Graded Ken Burns photo(s) with flare sweep, optional caption or name plate."""
    W, H = cv.W, cv.H
    tot = sum(s for _, s, _ in items)
    def fn(t):
        tl = t - t0; acc = 0.0
        for path, share, kw in items:
            seg = dur * share / tot
            if tl < acc + seg or path == items[-1][0]:
                img = grade(photo_frame(cv, path, tl - acc, seg, **kw)); break
            acc += seg
        img.alpha_composite(cv.VIG)
        img = flare(cv, img, lerp(1.1, -0.1, tl / dur) * W, H * 0.28, 0.45)
        L = cv.layer()
        if caption: cv.caption(L, tl, 0.2, dur - 0.05, *caption)
        if plate: cv.name_plate(L, tl, *plate)
        img.alpha_composite(L); bars(cv, img); tag(cv, img, tl, who); cv.bug(img)
        return img
    return fn


def cine_clip(cv, t0, dur, path, src_start, z=(1.0, 1.1), centre=(0.5, 0.45), captions=(), speed=1.0, hits=(), who=None):
    C = Clip(path, src_start, speed)
    W, H = cv.W, cv.H
    def fn(t):
        tl = t - t0
        img = grade(zoom(cv, C.frame(tl, W, H), lerp(z[0], z[1], clamp(tl / dur)), *centre))
        img.alpha_composite(cv.VIG)
        L = cv.layer()
        for a, b, *cap in captions: cv.caption(L, tl, a, b, *cap)
        img.alpha_composite(L)
        img = shake(img, tl, hits, 10 * cv.S)
        bars(cv, img); tag(cv, img, tl, who); cv.bug(img)
        return img
    return fn


def slide_slam(cv, t0, dur, slide_no, kicker):
    """Session slide slams in (scale 1.5->1, blur, flash, shake) then slowly pushes in."""
    W, H, S = cv.W, cv.H, cv.S
    sl = load_photo(SLIDE % slide_no, 2048)
    bgp = RAW + "20261002_121510.jpg"
    def fn(t):
        tl = t - t0
        key = ("ssbg", W, H)
        if key not in _cache:
            b = ImageOps.fit(load_photo(bgp), (W // 4, H // 4)).filter(ImageFilter.GaussianBlur(5)).resize((W, H), Image.BILINEAR)
            _cache[key] = ImageEnhance.Brightness(b).enhance(0.35).convert("RGBA")
        img = _cache[key].copy()
        img = img.resize((W, H), Image.BILINEAR, box=(tl * 8, tl * 4, W - tl * 8, H - tl * 4)) if tl > 0 else img
        p = prog(tl, 0, 0.2)
        sc = lerp(1.5, 1.0, eo(p)) * (1 + 0.05 * eio(prog(tl, 0.2, dur)))
        sw = (W * 0.78 if not cv.vert else W * 0.94) * sc; sh = sw * 9 / 16
        card = sl.resize((int(sw), int(sh)), Image.BILINEAR).convert("RGBA")
        if p < 1: card = card.filter(ImageFilter.GaussianBlur((1 - p) * 10))
        cy = H / 2 + (20 * S if not cv.vert else 0)
        x, y = W / 2 - sw / 2, cy - sh / 2
        glow = Image.new("RGBA", (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(glow)
        gd.rectangle([x - 14, y - 14, x + sw + 14, y + sh + 14], fill=GOLD + (200,))
        img.alpha_composite(glow.filter(ImageFilter.GaussianBlur(22)))
        ImageDraw.Draw(img).rectangle([x - 5, y - 5, x + sw + 5, y + sh + 5], fill=GOLD + (255,))
        img.alpha_composite(card, (int(x), int(y)))
        L = cv.layer(); d = ImageDraw.Draw(L)
        pk = eo(prog(tl, 0.15, 0.45))
        if pk > 0:
            fk = M(800, 32 * S); tw = d.textlength(kicker, font=fk); bw = (tw + 48 * S) * pk
            ky = y - 75 * S
            d.rectangle([W / 2 - bw / 2, ky, W / 2 + bw / 2, ky + 54 * S], fill=GOLD + (255,))
            if pk > 0.6: d.text((W / 2, ky + 27 * S), kicker, font=fk, fill=NAVY, anchor="mm")
        img.alpha_composite(L)
        img = flare(cv, img, lerp(-0.1, 1.1, tl / dur) * W, y + 10, 0.5)
        if tl < 0.06: img.alpha_composite(Image.new("RGBA", (W, H), (255, 250, 235, 170)))
        img = chroma(img, max(0, (0.12 - tl) / 0.12) * 18 * S)
        img = shake(img, tl, [0.0], 20 * S)
        bars(cv, img); cv.bug(img)
        return img
    return fn


def countdown(cv, t0, dur, bg, final_lines, step=1.0, num_size=420):
    """3..2..1 slams on a graded, darkened hero photo, then the call-to-action line."""
    W, H, S = cv.W, cv.H, cv.S
    def fn(t):
        tl = t - t0
        img = grade(photo_frame(cv, bg, tl, dur, 1.25, 1.0))
        img.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 150))); img.alpha_composite(cv.VIG)
        L = cv.layer()
        if tl < 3 * step:
            k = int(tl / step); slam_text(cv, L, tl, k * step, str(3 - k), num_size, H / 2, GOLD)
            hits = [0.0, step, 2 * step]
        else:
            hits = [3 * step]
            pl = eo(prog(tl, 3 * step, 3 * step + 0.5)); lg = cv.logo((220 if not cv.vert else 300) * S).copy()
            lg.putalpha(lg.split()[3].point(lambda v: int(v * pl)))
            L.alpha_composite(lg, (int(W / 2 - lg.width / 2), int(H * (0.18 if not cv.vert else 0.2))))
            for i, (txt, size, col) in enumerate(final_lines):
                slam_text(cv, L, tl, 3 * step + i * 0.3, txt, size, H * 0.58 + (i - (len(final_lines) - 1) / 2) * size * S * 1.05, col, ring=(i == 0))
        img.alpha_composite(cv.shadow(L, 16, 170))
        img = shake(img, tl, hits, 22 * S)
        if any(0 <= tl - h < 0.06 for h in hits): img.alpha_composite(Image.new("RGBA", (W, H), (255, 240, 220, 140)))
        bars(cv, img)
        return img
    return fn
