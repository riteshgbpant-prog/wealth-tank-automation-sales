"""Original Bollywood sports-anthem style score (dhol + brass + strings + choir) – copyright-safe."""
import numpy as np
from instruments import *

def dhol_low(d=0.45):
    n = int(d * SR); t = np.arange(n) / SR
    f = 62 + 70 * np.exp(-t * 22)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 6.5)
    s += lp(rng.standard_normal(n), 900) * np.exp(-t * 60) * 0.5
    return np.tanh(s * 1.8) * 0.95

def dhol_high(d=0.18):
    n = int(d * SR); t = np.arange(n) / SR
    s = np.sin(2 * np.pi * 380 * t) * np.exp(-t * 28) * 0.6 + bp(rng.standard_normal(n), 1500, 6000) * np.exp(-t * 45) * 0.7
    return s * 0.8

def taiko(d=0.9):
    n = int(d * SR); t = np.arange(n) / SR
    f = 45 + 60 * np.exp(-t * 12)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 3.5) + lp(rng.standard_normal(n), 400) * np.exp(-t * 20) * 0.6
    return np.tanh(s * 1.6)

def brass(notes, d):
    n = int(d * SR); t = np.arange(n) / SR
    s = np.zeros(n)
    for m in notes:
        for dt in (-0.08, 0, 0.09):
            s += saw(hz(m + dt), n, rng.random())
    env = np.minimum(1, t / 0.025) * np.exp(-t * 2.2) * 0.8 + 0.2 * np.minimum(1, t / 0.05) * np.maximum(0, 1 - t / d)
    # bright filter that closes (brassy "blat")
    out = np.zeros(n); seg = 12
    for k in range(seg):
        a, b = k * n // seg, (k + 1) * n // seg
        out[a:b] = lp(s[max(0, a - 2000):b], 900 + 4500 * np.exp(-k / 3))[-(b - a):]
    return out / (len(notes) * 3) * env * 1.6

def strings_ostinato(root, d, step=BEAT / 4):
    n = int(d * SR); out = np.zeros(n); seq = [0, 12, 7, 12, 0, 12, 7, 15]
    k = 0; t0 = 0
    while t0 < d:
        m = root + seq[k % len(seq)]; ln = int(step * SR * 0.95); i = int(t0 * SR)
        tt = np.arange(ln) / SR
        note = (saw(hz(m), ln) + saw(hz(m + 0.07), ln)) * np.exp(-tt * 9) * 0.5
        out[i:i + ln] += note[: max(0, min(ln, n - i))]
        t0 += step; k += 1
    return lp(out, 3200) * 0.5

def choir(notes, d):
    n = int(d * SR); t = np.arange(n) / SR
    vib = 1 + 0.004 * np.sin(2 * np.pi * 5.2 * t)
    s = np.zeros(n)
    for m in notes:
        for dt in (-0.06, 0.05):
            s += saw(1, n) * 0 + np.sign(np.sin(2 * np.pi * np.cumsum(hz(m + dt) * vib) / SR)) * 0.5
    s = bp(s, 500, 1400) * 0.6 + bp(s, 2200, 3200) * 0.2       # "aah" formants
    env = np.minimum(1, t / 0.5) * np.minimum(1, (d - t) / 0.6)
    return s / len(notes) * env

PROG = [(45, [57, 60, 64]), (41, [53, 57, 60]), (43, [55, 59, 62]), (40, [52, 56, 59])]   # Am F G E – heroic minor

def braam(d=2.2):
    n = int(d * SR); t = np.arange(n) / SR
    s = sum(saw(hz(m), n, rng.random()) for m in (33, 33.08, 40, 45))
    s = lp(s, 700) * np.minimum(1, t / 0.04) * np.exp(-t * 1.3)
    sub = np.sin(2 * np.pi * 55 * t) * np.exp(-t * 2.0)
    return np.tanh((s * 0.5 + sub) * 1.6) * 0.9

def heartbeat():
    n = int(0.6 * SR); t = np.arange(n) / SR; s = np.zeros(n)
    for o, g in ((0, 1.0), (0.18, 0.7)):
        k = int(o * SR); tt = t[: n - k]
        s[k:] += np.sin(2 * np.pi * (45 + 40 * np.exp(-tt * 30)) * tt) * np.exp(-tt * 14) * g
    return s * 0.9

def build_anthem(dur, plan):
    N = int(dur * SR); mus = np.zeros((N, 2))
    L, Hh, T = dhol_low(), dhol_high(), taiko()
    PAT = [1, 0, 2, 1, 2, 0, 1, 2]   # 8ths: 1=low 2=high (kaharwa feel)
    def bars(a, b, dhol=True, taiko_=False, strings=True, brass_=False, choir_=False, bass_=True, cut=1.0):
        t = a
        while t < b - 1e-6:
            bi = int(round(t / (BEAT * 4))); root, ch = PROG[bi % 4]
            dur_bar = min(BEAT * 4, b - t)
            if dhol:
                for k in range(8):
                    tk = t + k * BEAT / 2
                    if tk >= b: break
                    if PAT[k] == 1: add(mus, tk, L, 0.75, 0.45)
                    elif PAT[k] == 2: add(mus, tk, Hh, 0.5, 0.6)
            if taiko_:
                add(mus, t, T, 0.8); add(mus, t + BEAT * 2, T, 0.6)
            if strings:
                s = strings_ostinato(root + 12, dur_bar) * cut
                add(mus, t, np.stack([s, np.roll(s, 240)], 1), 0.55)
            if bass_:
                bn = bass_note(root - 12 + 12, int(dur_bar * SR * 0.98))
                add(mus, t, bn, 0.35)
            if brass_:
                add(mus, t, brass([m + 12 for m in ch], BEAT * 1.5), 0.55, 0.5)
                add(mus, t + BEAT * 2.5, brass([m + 12 for m in ch], BEAT * 1.4), 0.45, 0.5)
            if choir_:
                c = choir([m + 12 for m in ch], dur_bar + 0.2)
                add(mus, t, np.stack([c, np.roll(c, 500)], 1), 0.45)
            t += BEAT * 4
    for a, b, mode in plan:
        if mode == "intro":
            c = choir([57, 64, 69], b - a + 0.3); add(mus, a, np.stack([c, c], 1), 0.35)
            add(mus, a, riser(max(0.5, b - a - 2.5)), 0.5)
            add(mus, max(a, b - 2.6), T, 0.9); add(mus, max(a, b - 2.0), T, 0.9)
        elif mode == "light": bars(a, b, dhol=True, strings=True, bass_=True, cut=0.7)
        elif mode == "groove": bars(a, b, dhol=True, strings=True, brass_=False, choir_=True)
        elif mode == "full": bars(a, b, dhol=True, taiko_=True, strings=True, brass_=True, choir_=True)
        elif mode == "break":
            c = choir([57, 60, 64, 69], b - a + 0.3); add(mus, a, np.stack([c, np.roll(c, 400)], 1), 0.5)
            bars(a, b, dhol=False, strings=True, bass_=False, cut=0.5)
        elif mode == "build":
            bars(a, b, dhol=True, taiko_=True, strings=True, bass_=False)
            add(mus, b - 2.0, riser(2.0), 0.55)
            for k in range(8): add(mus, b - 1.0 + k * 0.125, Hh, 0.5)
        elif mode == "cold":
            c = choir([45, 52, 57], b - a + 0.3); add(mus, a, np.stack([c, c], 1), 0.22)
            hb = heartbeat(); tt = a
            while tt < b - 0.4: add(mus, tt, hb, 0.8); tt += 1.0
            add(mus, b - 1.5, riser(1.5), 0.7)
        elif mode == "countdown":
            for k in range(3): add(mus, a + k, T, 1.0); add(mus, a + k, L, 0.9)
            c = choir([57, 64, 69], b - a); add(mus, a, np.stack([c, c], 1), 0.35)
            bars(a + 3.0, b, dhol=True, taiko_=True, strings=True, brass_=True, choir_=True)
        elif mode == "outro":
            add(mus, a, T, 1.0); add(mus, a, brass([57, 64, 69, 72], 2.5), 0.8)
            c = choir([57, 64, 69, 76], b - a); add(mus, a, np.stack([c, np.roll(c, 400)], 1), 0.55)
            bars(a + 2.0, b - 1.0, dhol=True, strings=True, brass_=False, choir_=False, cut=0.6)
    mus = np.tanh(mus * 1.45) * 0.85
    t = np.arange(N) / SR
    return mus * np.minimum(1, (dur - t) / 1.5)[:, None]
