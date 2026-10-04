"""Anurag Kesarwani – 30s vertical Reel (1080x1920) incl. outro."""
import sys
from engine import Canvas, run
from cards import outro, RAW as R, IMG
from teaser import *
AN = ('ANURAG KESARWANI', 'Co-Founder, Wealth Tank  •  Financial Consultant  •  Sales Training')
cv = Canvas(1080, 1920)
P = lambda n: R + "20261002_%s.jpg" % n
HOUSE = [P("121510"), P("100948"), P("115122"), P("102045"), P("144711")]
SEG = [
    (0, 3.5, cold_open(cv, 0, 3.5, [(0.3, "BARABANKI", 170, WHITE), (1.4, "EK DIN", 220, WHITE), (2.4, "HAR GHAR", 190, GOLD)])),
    (3.5, 6, burst(cv, 3.5, 2.5, HOUSE, big=("HOUSE FULL!", 170, WHITE))),
    (6, 10, cine_clip(cv, 6, 4, "srcV/v4.mp4", 33.0, z=(1.0, 1.06), hits=[0.0],
                      captions=[(0.2, 3.95, "CO-FOUNDER, WEALTH TANK", "ANURAG KESARWANI", "Financial Consultant • Sales Training")])),
    (10, 12, slide_slam(cv, 10, 2, 9, "INCOME IS IN MEETINGS")),
    (12, 15.5, cine_clip(cv, 12, 3.5, "srcV/v3.mp4", 7.0, z=(1.0, 1.06), hits=[0.0],
                         captions=[(0.2, 3.45, "100% PARTICIPATION", "ADVISORS KI AAWAZ", "Har sawaal, live jawab")])),
    (15.5, 17.5, slide_slam(cv, 15.5, 2, 35, "SKILL = 3X POWER")),
    (17.5, 21, cine_clip(cv, 17.5, 3.5, "srcV/v5.mp4", 2.0, who=AN, z=(1.0, 1.06), hits=[0.0],
                         captions=[(0.2, 3.45, "LIVE ROLE-PLAY", "REAL CLOSING", "Practice karo, MDRT tak pahuncho")])),
    (21, 24, countdown(cv, 21, 3, P("121510"), [("AGLA SESSION", 120, WHITE), ("AAPKE SHEHAR", 120, GOLD), ("MEIN?", 120, GOLD)], step=0.5, num_size=380)),
    (24, 30, outro(cv, 24, 6, "Anurag Kesarwani", "Co-Founder • Financial Consultant • Sales Training", "+91 95807 85406")),
]
TR = {3.5: ("flash", 0.3), 6: ("whip", 0.4), 10: ("flash", 0.3), 12: ("glitch", 0.4), 15.5: ("flash", 0.3), 17.5: ("spin", 0.4),
      21: ("zoom", 0.4), 24: ("flash", 0.4)}
MUSIC_DUR = 30.0
MUSIC_PLAN = [(0, 3.5, "cold"), (3.5, 21, "full"), (21, 24, "countdown"), (24, 30, "outro")]
SFX_EXTRA = [(0.3, "braam", 0.9), (1.4, "impact", 0.8), (2.4, "braam", 1.0), (3.5, "impact", 1.0), (10, "impact", 0.6), (15.5, "impact", 0.6),
             (21.0, "braam", 0.8), (21.5, "braam", 0.8), (22.0, "braam", 0.8), (22.5, "impact", 1.0), (24.0, "impact", 0.85), (25.2, "ding", 0.6)]
if __name__ == "__main__":
    if sys.argv[1] == "preview":
        import engine; engine.PREVDIR = sys.argv[3]
        run(cv, SEG, TR, 30, None, preview=[float(x) for x in sys.argv[2].split(",")])
    else:
        run(cv, SEG, TR, 30, sys.argv[1])
