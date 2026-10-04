"""Synthesize an energetic 120 BPM corporate/motivational track + transition SFX, synced to the edit."""
import numpy as np, wave
from scipy.signal import butter, lfilter, sosfilt

SR = 48000
BPM = 120; BEAT = 60 / BPM
rng = np.random.default_rng(11)
hz = lambda m: 440 * 2 ** ((m - 69) / 12)


def write(path, st):
    st = np.clip(st, -1, 1)
    with wave.open(path, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((st * 32767).astype("<i2").tobytes())


def lp(x, fc, order=2):
    return sosfilt(butter(order, fc / (SR / 2), "low", output="sos"), x)


def hp(x, fc, order=2):
    return sosfilt(butter(order, fc / (SR / 2), "high", output="sos"), x)


def bp(x, f1, f2):
    return sosfilt(butter(2, [f1 / (SR / 2), f2 / (SR / 2)], "band", output="sos"), x)


def saw(f, n, phase=0.0):
    t = np.arange(n) / SR
    return 2 * ((f * t + phase) % 1.0) - 1


def add(buf, start_s, sig, gain=1.0, pan=0.5):
    i = int(start_s * SR)
    if i >= len(buf): return
    sig = sig[: len(buf) - i]
    if sig.ndim == 1:
        buf[i:i + len(sig), 0] += sig * gain * (1 - pan) * 2 * 0.5
        buf[i:i + len(sig), 1] += sig * gain * pan * 2 * 0.5
    else:
        buf[i:i + len(sig)] += sig * gain


# ---------------- instruments ----------------
def kick():
    n = int(0.42 * SR); t = np.arange(n) / SR
    f = 48 + 140 * np.exp(-t * 35)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7.5)
    s += rng.standard_normal(n) * np.exp(-t * 300) * 0.25
    return np.tanh(s * 1.6) * 0.9


def clap():
    n = int(0.3 * SR); t = np.arange(n) / SR
    env = np.zeros(n)
    for o in (0, 0.011, 0.022):
        k = int(o * SR); env[k:] += np.exp(-(t[: n - k]) * (60 if o < 0.02 else 18))
    return bp(rng.standard_normal(n), 900, 5000) * env * 0.55


def hat(open_=False):
    n = int((0.22 if open_ else 0.06) * SR); t = np.arange(n) / SR
    return hp(rng.standard_normal(n), 7000) * np.exp(-t * (14 if open_ else 70)) * 0.28


def supersaw(notes, n, cutoff=2600):
    out = np.zeros(n)
    for m in notes:
        for d in (-0.12, -0.05, 0, 0.06, 0.13):
            out += saw(hz(m + d), n, rng.random())
    out = lp(out / (len(notes) * 5), cutoff, 4)
    t = np.arange(n) / SR
    return out * np.minimum(1, t / 0.03)


def bass_note(m, n):
    t = np.arange(n) / SR
    s = lp(saw(hz(m), n) * 0.7 + np.sin(2 * np.pi * hz(m) * t) * 0.8, 420, 2)
    return s * np.minimum(1, t / 0.005) * np.minimum(1, (n / SR - t) / 0.02)


def pluck(m, n=int(0.35 * SR)):
    t = np.arange(n) / SR
    s = saw(hz(m), n) * 0.5 + np.sin(2 * np.pi * hz(m) * t)
    return lp(s, 3500) * np.exp(-t * 9)


def pad(notes, n):
    t = np.arange(n) / SR
    s = sum(np.sin(2 * np.pi * hz(m) * t + rng.random()) + 0.4 * np.sin(2 * np.pi * hz(m + 12) * t) for m in notes)
    env = np.minimum(1, t / 0.6) * np.minimum(1, (n / SR - t) / 0.6)
    return s / len(notes) * env


def riser(d):
    n = int(d * SR); x = np.linspace(0, 1, n)
    noise = rng.standard_normal(n)
    out = np.zeros(n)
    chunks = 40
    for c in range(chunks):                                 # stepped sweeping band-pass
        a, b = c * n // chunks, (c + 1) * n // chunks
        fc = 300 + 9000 * (c / chunks) ** 2
        out[a:b] = bp(noise[max(0, a - 2000):b], fc * 0.7, min(fc * 1.4, 23000))[-(b - a):]
    tone = np.sin(2 * np.pi * np.cumsum(200 + 900 * x ** 2) / SR) * 0.3
    return (out * 0.8 + tone) * x ** 2


def impact():
    n = int(2.2 * SR); t = np.arange(n) / SR
    boom = np.sin(2 * np.pi * np.cumsum(30 + 90 * np.exp(-t * 8)) / SR) * np.exp(-t * 2.2)
    crack = lp(rng.standard_normal(n), 3000) * np.exp(-t * 9) * 0.6
    tail = lp(rng.standard_normal(n), 900) * np.exp(-t * 1.6) * 0.25
    return np.tanh((boom + crack + tail) * 1.4) * 0.9


def whoosh(d=0.5, up=True):
    n = int(d * SR); x = np.linspace(0, 1, n)
    noise = rng.standard_normal(n)
    out = np.zeros(n); chunks = 24
    for c in range(chunks):
        a, b = c * n // chunks, (c + 1) * n // chunks
        k = c / chunks if up else 1 - c / chunks
        fc = 400 + 6000 * k ** 1.5
        out[a:b] = bp(noise[max(0, a - 1500):b], fc * 0.6, min(fc * 1.6, 22000))[-(b - a):]
    return out * np.sin(np.pi * x) ** 1.5 * 1.3


def shutter():
    n = int(0.18 * SR); t = np.arange(n) / SR
    s = np.zeros(n)
    for o in (0, 0.07):
        k = int(o * SR); s[k:] += hp(rng.standard_normal(n - k), 2500) * np.exp(-t[: n - k] * 90)
    return s * 0.7


def tick():
    n = int(0.03 * SR); t = np.arange(n) / SR
    return np.sin(2 * np.pi * 2400 * t) * np.exp(-t * 200) * 0.5


def glitch():
    n = int(0.35 * SR); s = np.zeros(n)
    for k in range(7):
        a = rng.integers(0, n - 2000); L = rng.integers(400, 3000)
        s[a:a + L] += np.sign(np.sin(2 * np.pi * rng.uniform(200, 1800) * np.arange(L) / SR)) * 0.35
    return lp(s, 6000)


def ding():
    n = int(1.6 * SR); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * 1568 * t) + 0.5 * np.sin(2 * np.pi * 2349 * t)) * np.exp(-t * 2.8) * 0.35


