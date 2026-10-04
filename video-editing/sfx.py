"""Synthesize sound effects + a soft music bed (no external assets needed)."""
import numpy as np, wave, sys

SR = 48000
DUR = float(sys.argv[1]) if len(sys.argv) > 1 else 13.4
rng = np.random.default_rng(7)


def write(path, x):
    x = np.clip(x, -1, 1)
    st = np.stack([x, x], 1) if x.ndim == 1 else x
    with wave.open(path, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((st * 32767).astype("<i2").tobytes())


def onepole_lp(x, fc):
    # time-varying one-pole low-pass, fc may be array
    fc = np.broadcast_to(fc, x.shape)
    a = np.exp(-2 * np.pi * fc / SR)
    y = np.zeros_like(x); s = 0.0
    for i in range(len(x)):
        s = (1 - a[i]) * x[i] + a[i] * s
        y[i] = s
    return y


def whoosh(d=0.55, up=True):
    n = int(d * SR); t = np.linspace(0, 1, n)
    noise = rng.standard_normal(n)
    sweep = (300 + 5500 * t ** 1.5) if up else (5800 - 5500 * t ** 0.7)
    lp = onepole_lp(noise, sweep)
    hp = lp - onepole_lp(lp, 250)
    env = np.sin(np.pi * t) ** 2
    return hp * env * 0.9


def pop(f0=900, f1=250, d=0.09):
    n = int(d * SR); t = np.arange(n) / SR
    f = f0 * (f1 / f0) ** (t / d)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-t * 45) * 0.8


def thump(d=0.35):
    n = int(d * SR); t = np.arange(n) / SR
    f = 120 * np.exp(-t * 18) + 45
    ph = 2 * np.pi * np.cumsum(f) / SR
    click = rng.standard_normal(n) * np.exp(-t * 400) * 0.3
    return (np.sin(ph) * np.exp(-t * 9) + click) * 0.95


def ding(d=1.4):
    n = int(d * SR); t = np.arange(n) / SR
    s = (np.sin(2 * np.pi * 1318.5 * t) + 0.6 * np.sin(2 * np.pi * 1975.5 * t)
         + 0.25 * np.sin(2 * np.pi * 2637 * t) * np.exp(-t * 6))
    return s * np.exp(-t * 3.2) * 0.38


def riser(d=0.9):
    n = int(d * SR); t = np.linspace(0, 1, n)
    noise = onepole_lp(rng.standard_normal(n), 400 + 7000 * t ** 2)
    tone = np.sin(2 * np.pi * np.cumsum(220 + 660 * t ** 2) / SR) * 0.25
    return (noise * 0.6 + tone) * t ** 2.2 * 0.6


def music(dur):
    """Soft corporate pad: Cmaj7 - Am7 - Fmaj7 - G6, ~2.2 s per chord, plus gentle plucks."""
    n = int(dur * SR); t = np.arange(n) / SR
    out = np.zeros((n, 2))
    chords = [[48, 55, 59, 64], [45, 52, 55, 60], [41, 48, 52, 57], [43, 50, 55, 59]]
    seg = 2.2
    hz = lambda m: 440 * 2 ** ((m - 69) / 12)
    for ci in range(int(dur / seg) + 1):
        notes = chords[ci % 4]
        s0 = int(ci * seg * SR); s1 = min(n, int((ci + 1) * seg * SR) + int(0.4 * SR))
        if s0 >= n: break
        tt = np.arange(s1 - s0) / SR
        env = np.minimum(1, tt / 0.35) * np.minimum(1, np.maximum(0, (seg + 0.4 - tt) / 0.4))
        for k, m in enumerate(notes):
            f = hz(m + 12)
            v = (np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(2 * np.pi * 2 * f * tt + 0.3)) * env * 0.06
            pan = 0.35 + 0.1 * k
            out[s0:s1, 0] += v * (1 - pan); out[s0:s1, 1] += v * pan
        # pluck arpeggio, 8th notes at 109 bpm
        step = 60 / 109 / 2
        for j in range(int(seg / step)):
            p0 = s0 + int(j * step * SR); pn = int(0.4 * SR)
            if p0 + pn > n: break
            pt = np.arange(pn) / SR
            f = hz(notes[[0, 2, 3, 1][j % 4]] + 24)
            v = np.sin(2 * np.pi * f * pt) * np.exp(-pt * 11) * 0.05
            pan = 0.3 if j % 2 else 0.7
            out[p0:p0 + pn, 0] += v * (1 - pan); out[p0:p0 + pn, 1] += v * pan
    # soft kick on beats
    beat = 60 / 109
    for b in range(int(dur / beat)):
        p0 = int(b * beat * SR); pn = int(0.25 * SR)
        if p0 + pn > n: break
        pt = np.arange(pn) / SR
        k = np.sin(2 * np.pi * np.cumsum(55 + 90 * np.exp(-pt * 30)) / SR) * np.exp(-pt * 14) * 0.12
        out[p0:p0 + pn] += k[:, None]
    fade = np.minimum(1, t / 0.6) * np.minimum(1, (dur - t) / 1.2)
    return out * fade[:, None]


# (time, sound, gain)
EVENTS = [
    (0.00, thump(), 0.9), (0.02, whoosh(0.6), 0.8), (0.45, pop(), 0.7),
    (1.65, whoosh(0.45, up=False), 0.6),
    (2.15, whoosh(0.5), 0.7), (2.45, pop(1200, 400, 0.07), 0.5),
    (4.00, thump(0.3), 0.75),
    (6.30, pop(), 0.75), (6.80, pop(1000, 300), 0.75), (7.30, pop(1100, 330), 0.75),
    (9.90, whoosh(0.4, up=False), 0.55),
    (9.65, riser(0.85), 0.7), (10.50, ding(), 0.9), (10.50, thump(0.3), 0.6),
    (11.40, pop(1300, 500, 0.06), 0.5),
]

n = int(DUR * SR)
fx = np.zeros(n)
for t0, s, g in EVENTS:
    i = int(t0 * SR); e = min(n, i + len(s))
    fx[i:e] += s[: e - i] * g
write("sfx.wav", fx * 0.8)
write("music.wav", music(DUR))
print("ok", DUR)
