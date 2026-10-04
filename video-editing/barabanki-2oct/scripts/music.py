"""Timeline-driven soundtrack: sections -> music.wav, transitions/events -> sfx.wav."""
import numpy as np, sys, importlib
from instruments import *
from anthem import build_anthem

CH = [[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]]       # Am F C G
BASS = [33, 29, 36, 31]

def build(dur, plan, trans, extra=(), out_prefix="", style="anthem"):
    N = int(dur * SR)
    music = np.zeros((N, 2)); fx = np.zeros((N, 2))
    K, C, HC, HO = kick(), clap(), hat(), hat(True)
    def section(t0, t1, kick_=True, clap_=True, hats=True, bass=True, chords=True, plucks=False, cutoff=2600):
        b = t0
        while b < t1 - 1e-6:
            bar = int(round(b / (BEAT * 4))); ci = bar % 4
            for q in range(4):
                tb = b + q * BEAT
                if tb >= t1: break
                if kick_: add(music, tb, K, 0.85)
                if clap_ and q in (1, 3): add(music, tb, C, 0.6, 0.55)
                if hats:
                    add(music, tb + BEAT / 2, HO, 0.33, 0.65)
                    add(music, tb + BEAT / 4, HC, 0.22, 0.35); add(music, tb + 3 * BEAT / 4, HC, 0.22, 0.4)
                if bass:
                    add(music, tb + BEAT / 2, bass_note(BASS[ci], int(BEAT / 2 * SR * 0.95)), 0.55)
                    add(music, tb, bass_note(BASS[ci], int(BEAT / 2 * SR * 0.6)), 0.3)
                if plucks:
                    for e, m in enumerate([0, 2, 1, 2]):
                        add(music, tb + e * BEAT / 4, pluck(CH[ci][m] + 12), 0.15, 0.3 + 0.4 * (e % 2))
            if chords:
                n = int(min(BEAT * 4, t1 - b) * SR)
                ss = supersaw([m + 12 for m in CH[ci]], n, cutoff)
                tt = (np.arange(n) / SR) % BEAT
                ss *= 0.35 + 0.65 * np.minimum(1, tt / 0.18)
                add(music, b, np.stack([ss, np.roll(ss, 300)], 1), 0.30)
            b += BEAT * 4
    for a, b, mode in plan:
        if mode == "intro":
            add(music, a, np.stack([pad([57, 64, 69], int((b - a + 0.3) * SR))] * 2, 1), 0.22)
            add(music, a, riser(max(0.5, b - a - 2.5)), 0.5)
        elif mode == "light": section(a, b, clap_=False)
        elif mode == "groove": section(a, b, plucks=True)
        elif mode == "full": section(a, b, plucks=True, cutoff=3400)
        elif mode == "break":
            add(music, a, np.stack([pad([57, 60, 64, 69], int((b - a + 0.3) * SR))] * 2, 1), 0.28)
            for q in range(int((b - a) / BEAT)):
                add(music, a + q * BEAT, pluck(CH[(q // 4 + 1) % 4][q % 3] + 12), 0.17, 0.3 + 0.4 * (q % 2))
        elif mode == "build":
            section(a, b, clap_=False, bass=False, cutoff=1800); add(music, b - 2.0, riser(2.0), 0.5)
        elif mode == "outro":
            add(music, a, np.stack([pad([45, 57, 64, 69], int((b - a) * SR))] * 2, 1), 0.33)
            ss = supersaw([69, 72, 76], int(3.5 * SR), 3000) * np.exp(-np.arange(int(3.5 * SR)) / SR * 1.2)
            add(music, a, np.stack([ss, np.roll(ss, 300)], 1), 0.35); add(music, a, K, 0.9)
            section(a + 2.0, b - 1.0, kick_=True, clap_=False, hats=True, bass=True, chords=False)
    music = np.tanh(music * 1.25) * 0.8
    t = np.arange(N) / SR
    music *= np.minimum(1, (dur - t) / 1.5)[:, None]
    if style == "anthem": music = build_anthem(dur, plan)
    SFX = {"flash": [(-0.25, whoosh(0.5), 0.6), (0, impact(), 0.35)], "whip": [(-0.25, whoosh(0.45), 0.7)],
           "wipe": [(-0.3, whoosh(0.5, False), 0.6)], "zoom": [(-0.25, whoosh(0.45), 0.6), (0, impact(), 0.25)],
           "glitch": [(-0.15, glitch(), 0.5)], "iris": [(-0.35, whoosh(0.6), 0.6), (0, shutter(), 0.4)],
           "panels": [(-0.35, whoosh(0.6, False), 0.55), (0, shutter(), 0.45)], "spin": [(-0.25, whoosh(0.5), 0.75)],
           "leak": [(-0.3, whoosh(0.6), 0.5), (0, impact(), 0.3)], "cut": []}
    for c, (name, d) in trans.items():
        for off, s, g in SFX[name]: add(fx, c + off, np.stack([s, s], 1), g)
    for t0, kind, g in extra:
        s = {"impact": impact(), "ding": ding(), "shutter": shutter(), "whoosh": whoosh(0.5), "riser": riser(1.5), "tick": tick(), "braam": __import__("anthem").braam()}[kind]
        add(fx, t0, np.stack([s, s], 1), g)
    write(out_prefix + "music.wav", music); write(out_prefix + "sfx.wav", fx * 0.85)

if __name__ == "__main__":
    tl = importlib.import_module(sys.argv[1])
    build(tl.MUSIC_DUR, tl.MUSIC_PLAN, tl.TR, tl.SFX_EXTRA, sys.argv[2])
    print("ok")
