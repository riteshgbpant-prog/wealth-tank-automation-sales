"""Synthesize an energetic 120 BPM corporate/motivational track + transition SFX, synced to the edit."""
import numpy as np, wave
from scipy.signal import butter, lfilter, sosfilt

SR = 48000
BPM = 120; BEAT = 60 / BPM
DUR = 54.0
N = int(DUR * SR)
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


# ---------------- arrangement ----------------
music = np.zeros((N, 2))
CH = [[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]]       # Am F C G
BASS = [33, 29, 36, 31]
K, C, HC, HO = kick(), clap(), hat(), hat(True)

def section(t0, t1, kick_=True, clap_=True, hats=True, bass=True, chords=True, plucks=False, cutoff=2600):
    b = t0
    while b < t1 - 1e-6:
        bar = int(round(b / (BEAT * 4)))
        ci = bar % 4
        for q in range(4):
            tb = b + q * BEAT
            if tb >= t1: break
            if kick_: add(music, tb, K, 0.85)
            if clap_ and q in (1, 3): add(music, tb, C, 0.6, 0.55)
            if hats:
                add(music, tb + BEAT / 2, HO, 0.35, 0.65)
                add(music, tb + BEAT / 4, HC, 0.25, 0.35); add(music, tb + 3 * BEAT / 4, HC, 0.25, 0.4)
            if bass:
                for e in range(2):
                    ts = tb + BEAT / 2 + e * 0  # off-beat pumping bass
                add(music, tb + BEAT / 2, bass_note(BASS[ci], int(BEAT / 2 * SR * 0.95)), 0.55)
                add(music, tb, bass_note(BASS[ci], int(BEAT / 2 * SR * 0.6)), 0.3)
            if plucks:
                for e, m in enumerate([0, 2, 1, 2]):
                    add(music, tb + e * BEAT / 4, pluck(CH[ci][m] + 12), 0.16, 0.3 + 0.4 * (e % 2))
        if chords:
            n = int(BEAT * 4 * SR)
            ss = supersaw([m + 12 for m in CH[ci]], n, cutoff)
            # sidechain pump
            t = (np.arange(n) / SR) % BEAT
            ss *= 0.35 + 0.65 * np.minimum(1, t / 0.18)
            add(music, b, np.stack([ss, np.roll(ss, 300)], 1), 0.32)
        b += BEAT * 4

# intro 0-4: pad + riser into the logo slam
add(music, 0, np.stack([pad([57, 64, 69], int(4.2 * SR))] * 2, 1), 0.22)
add(music, 0.0, riser(1.75), 0.55)
section(4, 16, clap_=False, plucks=False)
add(music, 14.0, riser(2.0), 0.35)
section(16, 24, plucks=True)
section(24, 40, plucks=True, cutoff=3400)
# breakdown 40-44 (emotional), build 44-48
add(music, 40, np.stack([pad([57, 60, 64, 69], int(4.3 * SR))] * 2, 1), 0.28)
for q in range(8): add(music, 40 + q * BEAT, pluck(CH[q // 4 % 4 + 1][q % 3] + 12), 0.18, 0.3 + 0.4 * (q % 2))
section(44, 48, kick_=True, clap_=False, hats=True, bass=False, chords=True, cutoff=1800)
add(music, 46.0, riser(2.0), 0.5)
# outro 48-54: big final chord + pad tail
add(music, 48, np.stack([pad([45, 57, 64, 69], int(6 * SR))] * 2, 1), 0.33)
ss = supersaw([69, 72, 76], int(3.5 * SR), 3000) * np.exp(-np.arange(int(3.5 * SR)) / SR * 1.2)
add(music, 48, np.stack([ss, np.roll(ss, 300)], 1), 0.35)
add(music, 48, K, 0.9)

# master: gentle glue + fade
music = np.tanh(music * 1.25) * 0.8
t = np.arange(N) / SR
music *= np.minimum(1, (DUR - t) / 2.0)[:, None]

# ---------------- SFX synced to the edit ----------------
fx = np.zeros((N, 2))
EV = [
    (2.0, impact(), 0.9), (1.98, whoosh(0.5), 0.5),                        # logo slam
    (3.6, whoosh(0.5), 0.7), (4.0, impact(), 0.45),                        # into title
    (4.55, glitch(), 0.35),
    (7.75, whoosh(0.45), 0.7), (8.0, shutter(), 0.7),                      # photo of the coach
    (11.75, whoosh(0.45, False), 0.6),
    (17.75, glitch(), 0.5), (18.0, impact(), 0.35),                        # data section
    (23.75, whoosh(0.45), 0.6), (24.0, shutter(), 0.6),
    (27.75, whoosh(0.45, False), 0.6), (28.0, impact(), 0.3),
    (33.75, glitch(), 0.45),
    (39.75, whoosh(0.5), 0.6), (40.0, shutter(), 0.6),
    (43.75, whoosh(0.45, False), 0.55), (44.0, shutter(), 0.5),
    (47.7, whoosh(0.6), 0.7), (48.0, impact(), 0.85), (48.6, ding(), 0.6),
]
for t0, s, g in EV:
    add(fx, t0, np.stack([s, s], 1) if s.ndim == 1 else s, g)
for k in range(22):                                                          # counter ticks 18.9-20.9
    add(fx, 18.9 + k * 0.09, tick(), 0.45, 0.5)
add(fx, 21.0, ding(), 0.45)

write("music.wav", music)
write("sfx.wav", fx * 0.85)
print("ok")
