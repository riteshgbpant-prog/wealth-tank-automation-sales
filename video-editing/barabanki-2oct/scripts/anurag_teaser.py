"""Anurag Kesarwani – 120s cinematic teaser (16:9). Body 0-114s, outro 114-120 rendered separately."""
import sys
from engine import Canvas, run
from cards import stat_punch, thank_you, modules_card, RAW as R, IMG
from teaser import *

cv = Canvas(1920, 1080)
def cine(fn):
    def g(t):
        img = fn(t); bars(cv, img); return img
    return g
P = lambda n: R + "20261002_%s.jpg" % n
PLATE = ("CO-FOUNDER, WEALTH TANK", "Anurag Kesarwani", "Financial Consultant  •  Sales Training", None)
GO = GOLD
AN = ('ANURAG KESARWANI', 'Co-Founder, Wealth Tank  •  Financial Consultant  •  Sales Training')

VENUE = [P("083519"), P("085729"), P("085751"), P("090240"), P("090334"), P("085732"), P("090259"), IMG + "11.jpg"]
HOUSE = [P("100948"), P("121510"), P("102045"), P("115122"), P("100939"), P("144007"), P("101921"), P("100953")]
ENERGY = [P("121510"), P("144711"), P("115122"), P("122441"), P("102045"), P("100949"), P("123331"), P("111009")]
ROLE = [P("152938"), P("153001"), P("155312"), P("152938")]
DAY = [IMG + "10.jpg", P("110847"), P("113601"), P("100823"), P("101026"), P("144007"), P("115353"), P("121510")]

SEG = [
    (0, 8, cold_open(cv, 0, 8, [(0.5, "2 OCTOBER 2026", 150, WHITE), (2.0, "BARABANKI", 230, WHITE), (3.5, "EK DIN", 260, WHITE),
                                 (4.5, "EK MISSION", 230, WHITE), (5.5, "HAR GHAR SURAKSHA", 190, GO)])),
    (8, 12, burst(cv, 8, 4, VENUE, caption=("THE REGAL HERITAGE", "BARABANKI", "Wealth Tank x LIC Champions"))),
    (12, 16, cine_photo(cv, 12, 4, [(P("090912"), 1, dict(z0=1.05, z1=1.22, c0=(0.42, 0.4), c1=(0.42, 0.35)))], plate=(0.2, 3.95) + PLATE)),
    (16, 20, modules_card(cv, 16, 4)),
    (20, 24, burst(cv, 20, 4, HOUSE, big=("HOUSE FULL!", 200, WHITE))),
    (24, 30, cine_clip(cv, 24, 6, "src/v4.mp4", 33.0, who=AN, z=(1.15, 1.3), centre=(0.45, 0.45), hits=[0.0],
                       captions=[(0.3, 5.9, "SALES TRAINING", "TRAINING JO DIL SE JUDE", "Har advisor tak pahunch")])),
    (30, 33, slide_slam(cv, 30, 3, 9, "INCOME IS IN MEETINGS")),
    (33, 36, slide_slam(cv, 33, 3, 35, "SKILL = 3X POWER")),
    (36, 42, cine_clip(cv, 36, 6, "src/v3.mp4", 7.0, z=(1.0, 1.1), centre=(0.35, 0.5), hits=[0.0],
                       captions=[(0.3, 5.9, "100% PARTICIPATION", "ADVISORS KI AAWAZ", "Har sawaal, live jawab")])),
    (42, 47, stat_punch(cv, 42, 5, "penetration")),
    (47, 51, burst(cv, 47, 4, ENERGY, big=("JOSH HIGH!", 220, GO))),
    (51, 57, cine_clip(cv, 51, 6, "src/v2.mp4", 0.5, who=AN, z=(1.4, 1.55), centre=(0.53, 0.42), hits=[0.0],
                       captions=[(0.3, 5.9, "FINANCIAL CONSULTANT", "SEEDHI BAAT, SACCHI SELLING", "Need samjho, solution do")])),
    (57, 60, slide_slam(cv, 57, 3, 29, "THE DOCTOR APPROACH")),
    (60, 63, slide_slam(cv, 60, 3, 72, "DO MEETING ROZ = TARGET PAKKA")),
    (63, 69, cine_clip(cv, 63, 6, "src/v5.mp4", 2.0, who=AN, z=(1.05, 1.18), centre=(0.5, 0.5), hits=[0.0],
                       captions=[(0.3, 5.9, "LIVE ROLE-PLAY", "REAL OBJECTIONS, REAL CLOSING", "Practice karo, MDRT tak pahuncho")])),
    (69, 72, burst(cv, 69, 3, ROLE, beat=0.75)),
    (72, 77, stat_punch(cv, 72, 5, "gap")),
    (77, 80, slide_slam(cv, 77, 3, 144, "DER KI KEEMAT")),
    (80, 83, slide_slam(cv, 80, 3, 123, "RISK COVER GAP")),
    (83, 89, cine_clip(cv, 83, 6, "src/v4.mp4", 3.0, who=AN, z=(1.1, 1.25), centre=(0.5, 0.45), hits=[0.0],
                       captions=[(0.3, 5.9, "ENERGY 100%", "COACH IN THE CROWD", "Ek din, poora badlaav")])),
    (89, 93, burst(cv, 89, 4, DAY, caption=("EK DIN", "SEEKHO • SAMJHO • JEETO", None))),
    (93, 98, stat_punch(cv, 93, 5, "zaroorat")),
    (98, 102, thank_you(cv, 98, 4, P("121510"))),
    (102, 109, countdown(cv, 102, 7, P("121510"), [("AGLA SESSION", 150, WHITE), ("AAPKE SHEHAR MEIN?", 150, GO)])),
    (109, 114, cine_photo(cv, 109, 5, [(P("100948"), 1, dict(z0=1.2, z1=1.0))],
                          caption=("AAPKI TEAM KE LIYE", "ABHI BOOK KAREIN!", "Har Ghar Suraksha • Wealth Tank"))),
]
TR = {8: ("flash", 0.4), 12: ("leak", 0.6), 16: ("iris", 0.6), 20: ("glitch", 0.4), 24: ("spin", 0.5), 30: ("flash", 0.3),
      33: ("flash", 0.3), 36: ("whip", 0.5), 42: ("panels", 0.6), 47: ("glitch", 0.4), 51: ("leak", 0.6), 57: ("flash", 0.3),
      60: ("flash", 0.3), 63: ("spin", 0.5), 69: ("glitch", 0.4), 72: ("iris", 0.6), 77: ("flash", 0.3), 80: ("flash", 0.3),
      83: ("whip", 0.5), 89: ("glitch", 0.4), 93: ("panels", 0.6), 98: ("leak", 0.6), 102: ("zoom", 0.5), 109: ("flash", 0.4)}

MUSIC_DUR = 120.0
MUSIC_PLAN = [(0, 8, "cold"), (8, 24, "full"), (24, 30, "groove"), (30, 36, "full"), (36, 47, "groove"), (47, 51, "full"),
              (51, 57, "groove"), (57, 63, "full"), (63, 72, "groove"), (72, 77, "light"), (77, 93, "full"), (93, 98, "break"),
              (98, 102, "build"), (102, 109, "countdown"), (109, 114, "full"), (114, 120, "outro")]
SFX_EXTRA = [(0.5, "braam", 0.9), (2.0, "braam", 0.9), (3.5, "impact", 0.8), (4.5, "impact", 0.8), (5.5, "braam", 1.0), (8.0, "impact", 1.0),
             (30.0, "impact", 0.6), (33.0, "impact", 0.6), (57.0, "impact", 0.6), (60.0, "impact", 0.6), (77.0, "impact", 0.6),
             (80.0, "impact", 0.6), (102.0, "braam", 0.9), (103.0, "braam", 0.9), (104.0, "braam", 0.9), (105.0, "impact", 1.0),
             (114.0, "impact", 0.85), (115.2, "ding", 0.6)]

if __name__ == "__main__":
    if sys.argv[1] == "preview":
        import engine; engine.PREVDIR = sys.argv[3] if len(sys.argv) > 3 else "prev"
        run(cv, SEG, TR, 114, None, preview=[float(x) for x in sys.argv[2].split(",")])
    else:
        run(cv, SEG, TR, 114, sys.argv[1])
