"""Frame-by-frame edit: color grade (ffmpeg) -> punch-in zooms + motion graphics (PIL) -> encode."""
import subprocess, sys, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

SRC = sys.argv[1]; OUT = sys.argv[2]
W, H, FPS = 1920, 1080, 30
DUR = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                     "-of", "csv=p=0", SRC]).decode())
NFR = int(DUR * FPS)
FD = "fonts/"
F = lambda w, s: ImageFont.truetype(f"{FD}Montserrat-{w}.ttf", s)

NAVY = (10, 32, 64); NAVY2 = (18, 52, 98); GOLD = (245, 182, 10); WHITE = (255, 255, 255)

def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def prog(t, t0, t1): return clamp((t - t0) / (t1 - t0))
def ease_out(x): return 1 - (1 - x) ** 3
def ease_in(x): return x ** 3
def back_out(x, s=1.9):
    x -= 1; return x * x * ((s + 1) * x + s) + 1
def lerp(a, b, x): return a + (b - a) * x

# ---------------- zoom plan (scale, applied around the face) ----------------
FACE = (1250, 450)
def zoom_at(t):
    if t < 4.0:  return lerp(1.00, 1.05, t / 4.0)
    if t < 8.0:  return lerp(1.20, 1.24, (t - 4.0) / 4.0)       # punch-in
    if t < 10.5: return lerp(1.06, 1.08, (t - 8.0) / 2.5)
    return lerp(1.12, 1.16, (t - 10.5) / (DUR - 10.5))

def apply_zoom(img, z):
    cw, ch = W / z, H / z
    x0 = clamp(FACE[0] - cw / 2, 0, W - cw); y0 = clamp(FACE[1] - ch / 2.2, 0, H - ch)
    return img.resize((W, H), Image.LANCZOS, box=(x0, y0, x0 + cw, y0 + ch))

# ---------------- reusable drawing helpers ----------------
def shadowed(layer, draw_fn, blur=14, offset=(0, 8), alpha=110):
    sh = Image.new("RGBA", layer.size, (0, 0, 0, 0))
    draw_fn(ImageDraw.Draw(sh), shadow=True)
    a = sh.split()[3].point(lambda v: v * alpha // 255)
    sh = Image.merge("RGBA", (*Image.new("RGB", sh.size, (0, 0, 0)).split(), a)).filter(ImageFilter.GaussianBlur(blur))
    layer.alpha_composite(sh, offset)
    draw_fn(ImageDraw.Draw(layer), shadow=False)

def with_alpha(layer, a):
    if a >= 1: return layer
    r, g, b, al = layer.split()
    return Image.merge("RGBA", (r, g, b, al.point(lambda v: int(v * a))))

def vignette():
    y, x = np.ogrid[:H, :W]
    d = np.sqrt(((x - W * 0.62) / (W * 0.75)) ** 2 + ((y - H / 2) / (H * 0.8)) ** 2)
    a = (np.clip(d - 0.55, 0, 1) * 150).astype(np.uint8)
    v = np.zeros((H, W, 4), np.uint8); v[..., 3] = a
    return Image.fromarray(v, "RGBA")
VIG = vignette()

# ---------------- graphics ----------------
def intro(t):
    if t > 2.05: return None
    L = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    out = ease_in(prog(t, 1.7, 2.0))
    # dark wash over the frame for title legibility
    wash = int(150 * ease_out(prog(t, 0, 0.25)) * (1 - out))
    L.alpha_composite(Image.new("RGBA", (W, H), (6, 18, 38, wash)))
    d = ImageDraw.Draw(L)
    # gold sweep bar
    sx = lerp(-900, 2200, ease_out(prog(t, 0.0, 0.55)))
    d.polygon([(sx, 0), (sx + 140, 0), (sx - 160, H), (sx - 300, H)], fill=GOLD + (230,))
    shift = -out * 1400
    tx = lerp(-700, 150, ease_out(prog(t, 0.12, 0.6))) + shift
    f1 = F(800, 132)
    d.text((tx, 360), "WEALTH", font=f1, fill=WHITE)
    tx2 = lerp(-900, 150, ease_out(prog(t, 0.2, 0.68))) + shift
    d.text((tx2, 500), "TANK", font=f1, fill=GOLD)
    # underline grows
    ul = 620 * ease_out(prog(t, 0.45, 0.9))
    d.rounded_rectangle([150 + shift, 668, 150 + shift + max(ul, 1), 680], 6, fill=GOLD)
    a = ease_out(prog(t, 0.5, 0.9))
    tag = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(tag).text((152 + shift, 708 + 20 * (1 - a)), "INSURANCE  •  LOANS  •  CONSULTING",
                             font=F(600, 40), fill=WHITE)
    L.alpha_composite(with_alpha(tag, a))
    return L

def lower_third(t):
    t0, t1 = 2.15, 6.0
    if not (t0 <= t < t1 + 0.3): return None
    L = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gin = ease_out(prog(t, t0, t0 + 0.45)); gout = ease_in(prog(t, t1, t1 + 0.3))
    x, y, h = 90, 840, 150
    bw = 760 * gin * (1 - gout)
    def draw(d, shadow):
        if bw < 4: return
        d.rounded_rectangle([x, y, x + 16, y + h], 4, fill=(0, 0, 0, 255) if shadow else GOLD + (255,))
        d.rounded_rectangle([x + 24, y, x + 24 + bw, y + h], 10, fill=(0, 0, 0, 255) if shadow else NAVY + (235,))
    shadowed(L, draw)
    if bw > 60:
        txt = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(txt)
        a = prog(t, t0 + 0.25, t0 + 0.6)
        d.text((x + 56, y + 20 + 14 * (1 - a)), "WEALTH TANK", font=F(800, 56), fill=WHITE)
        d.text((x + 58, y + 92 + 14 * (1 - a)), "Insurance & Loan Experts", font=F(600, 34), fill=GOLD)
        mask = Image.new("L", (W, H), 0)
        ImageDraw.Draw(mask).rectangle([x + 24, y, x + 24 + bw, y + h], fill=255)
        txt.putalpha(Image.composite(txt.split()[3], Image.new("L", (W, H), 0), mask))
        L.alpha_composite(with_alpha(txt, a))
    return L

CHIPS = [("Health Insurance", 6.3), ("Life Insurance", 6.8), ("Home Loan & LAP", 7.3)]
def chips(t):
    if not (6.3 <= t < 10.25): return None
    L = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    fade = 1 - ease_in(prog(t, 9.9, 10.25))
    for i, (label, ts) in enumerate(CHIPS):
        if t < ts: continue
        s = back_out(prog(t, ts, ts + 0.35))
        cx, cy = 90, 300 + i * 150
        ch = Image.new("RGBA", (720, 160), (0, 0, 0, 0))
        def draw(d, shadow, label=label):
            k = (0, 0, 0, 255)
            d.rounded_rectangle([10, 10, 690, 130], 60, fill=k if shadow else WHITE + (245,))
            d.ellipse([22, 22, 118, 118], fill=k if shadow else NAVY + (255,))
            if not shadow:
                d.line([(46, 72), (64, 92), (96, 50)], fill=GOLD, width=11, joint="curve")
                d.text((142, 44), label, font=F(700, 44), fill=NAVY)
        shadowed(ch, draw, blur=10, offset=(0, 6), alpha=90)
        sw, sh_ = int(720 * s), int(160 * s)
        if sw < 4 or sh_ < 4: continue
        chs = ch.resize((sw, sh_), Image.LANCZOS)
        L.alpha_composite(with_alpha(chs, fade), (cx, int(cy + (160 - sh_) / 2)))
    return L

def cta(t):
    t0 = 10.5
    if t < t0 - 0.05: return None
    L = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    a = ease_out(prog(t, t0 - 0.05, t0 + 0.3))
    # left gradient panel
    g = np.zeros((H, W, 4), np.uint8)
    ramp = np.clip(1 - np.linspace(0, 1, W) / 0.55, 0, 1) ** 1.3
    g[..., 0], g[..., 1], g[..., 2] = NAVY
    g[..., 3] = (ramp * 225 * a).astype(np.uint8)[None, :]
    L.alpha_composite(Image.fromarray(g, "RGBA"))
    T = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(T)
    off = lambda ts: 40 * (1 - ease_out(prog(t, ts, ts + 0.4)))
    al = lambda ts: int(255 * ease_out(prog(t, ts, ts + 0.4)))
    d.rounded_rectangle([110, 300 + off(10.55), 470, 356 + off(10.55)], 28, fill=GOLD + (al(10.55),))
    d.text((140, 309 + off(10.55)), "FREE CONSULTATION", font=F(800, 28), fill=NAVY + (al(10.55),))
    d.text((106, 390 + off(10.7)), "Call / WhatsApp", font=F(800, 84), fill=WHITE + (al(10.7),))
    d.text((106, 490 + off(10.85)), "Today", font=F(800, 84), fill=GOLD + (al(10.85),))
    d.text((110, 610 + off(11.0)), "Health • Life • Motor Insurance\nHome Loan • Vehicle Loan • LAP",
           font=F(600, 36), fill=WHITE + (al(11.0),), spacing=14)
    # pulsing button
    if t >= 11.4:
        s = back_out(prog(t, 11.4, 11.75)) * (1 + 0.035 * math.sin((t - 11.75) * 2 * math.pi * 1.2) * (t > 11.75))
        bw, bh = int(560 * s), int(96 * s)
        bx, by = 110 + (560 - bw) // 2, 760 + (96 - bh) // 2
        if bw > 10:
            d.rounded_rectangle([bx, by, bx + bw, by + bh], bh // 2, fill=GOLD + (255,))
            fs = max(8, int(38 * s))
            d.text((bx + bw / 2, by + bh / 2), "FOLLOW WEALTH TANK", font=F(800, fs), fill=NAVY, anchor="mm")
    L.alpha_composite(T)
    return L

def chrome(t):
    L = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.rectangle([0, H - 8, int(W * t / DUR), H], fill=GOLD + (255,))           # progress bar
    if 2.1 < t < 10.4:                                                         # corner bug
        a = int(200 * prog(t, 2.1, 2.5) * (1 - prog(t, 10.1, 10.4)))
        d.rounded_rectangle([1640, 40, 1880, 96], 28, fill=NAVY + (int(a * 0.85),))
        d.text((1760, 68), "WEALTH TANK", font=F(800, 26), fill=GOLD + (a,), anchor="mm")
    return L

LAYERS = [intro, lower_third, chips, cta, chrome]

# ---------------- pipeline ----------------
GRADE = "eq=contrast=1.08:saturation=1.12:gamma=0.97,unsharp=5:5:0.4"
dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", SRC, "-vf", f"{GRADE},format=rgb24",
                        "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
                        "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium",
                        "-crf", "18", "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709",
                        "-colorspace", "bt709", OUT], stdin=subprocess.PIPE)
fs = W * H * 3; i = 0
while True:
    buf = dec.stdout.read(fs)
    if len(buf) < fs: break
    t = i / FPS
    fr = Image.frombuffer("RGB", (W, H), buf).convert("RGBA")
    fr = apply_zoom(fr, zoom_at(t))
    fr.alpha_composite(VIG)
    for fn in LAYERS:
        lay = fn(t)
        if lay is not None: fr.alpha_composite(lay)
    enc.stdin.write(fr.convert("RGB").tobytes())
    i += 1
    if i % 60 == 0: print(f"{i} frames", flush=True)
enc.stdin.close(); enc.wait(); dec.wait()
print("done", i, "frames", DUR)
