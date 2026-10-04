"""Ritesh Tripathi – 120s cinematic teaser (16:9). Body 0-114s, outro 114-120 rendered separately."""
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
PLATE = ("FOUNDER, WEALTH TANK", "Ritesh Tripathi", "Master Facilitator & Financial Planner", "12+ saal  •  Insurance industry ka tajurba")
GO = GOLD
RI = ('RITESH TRIPATHI', 'Founder, Wealth Tank  •  Master Facilitator & Financial Planner')

VENUE = [P("083554"), P("085648"), P("085755"), P("085729"), P("090240"), P("090334"), P("085732"), IMG + "11.jpg"]
ENERGY2 = [P("100953"), P("121510"), P("101921"), P("144711"), P("115122"), P("100948"), P("102045"), P("122441")]
HOUSE = [P("100948"), P("121510"), P("102045"), P("115122"), P("100939"), P("144007"), P("101921"), P("100953")]
ENERGY = [P("121510"), P("144711"), P("115122"), P("122441"), P("102045"), P("100949"), P("123331"), P("111009")]
ROLE = [P("152938"), P("153001"), P("155312"), P("152938")]
DAY = [IMG + "10.jpg", P("110847"), P("113601"), P("100823"), P("101026"), P("144007"), P("115353"), P("121510")]

SEG = [
    (0, 8, cold_open(cv, 0, 8, [(0.5, "2 OCTOBER 2026", 150, WHITE), (2.0, "BARABANKI", 230, WHITE), (3.5, "EK DIN", 260, WHITE),
                                 (4.5, "EK MISSION", 230, WHITE), (5.5, "HAR GHAR SURAKSHA", 190, GO)])),
    (8, 12, burst(cv, 8, 4, VENUE, caption=("THE REGAL HERITAGE", "BARABANKI", "Wealth Tank x LIC Champions"))),
    (12, 16, cine_photo(cv, 12, 4, [(P("090720"), 1, dict(z0=1.3, z1=1.55, c0=(0.47, 0.55), c1=(0.47, 0.5)))], plate=(0.2, 3.95) + PLATE)),
    (16, 20, modules_card(cv, 16, 4)),
    (20, 24, burst(cv, 20, 4, HOUSE, big=("HOUSE FULL!", 200, WHITE))),
    (24, 30, cine_photo(cv, 24, 6, [(P("122407"), 1, dict(z0=1.45, z1=1.9, c0=(0.78, 0.45), c1=(0.84, 0.42)))],
                        caption=("MASTER FACILITATOR", "ADVISORS KE BEECH", "Har sawaal ka seedha jawab"), who=RI)),
    (30, 33, slide_slam(cv, 30, 3, 36, "NEED BASED SELLING KE 6 FAAYDE")),
    (33, 36, slide_slam(cv, 33, 3, 65, "TOP AGENTS KI DAILY HABITS")),
    (36, 42, cine_clip(cv, 36, 6, "src/v3.mp4", 9.0, z=(1.0, 1.1), centre=(0.35, 0.5), hits=[0.0],
                       captions=[(0.3, 5.9, "100% PARTICIPATION", "ADVISORS KI AAWAZ", "Har sawaal, live jawab")])),
    (42, 47, stat_punch(cv, 42, 5, "penetration")),
    (47, 51, burst(cv, 47, 4, ENERGY, big=("JOSH HIGH!", 220, GO))),
    (51, 55, cine_photo(cv, 51, 4, [(P("105021"), 1, dict(z0=1.0, z1=1.08, fill="blur"))],
                        caption=("FOUNDER, WEALTH TANK", "ENERGY IN THE HALL", "Facilitator ki energy = hall ki energy"), who=RI)),
    (55, 58, slide_slam(cv, 55, 3, 104, "GOAL FINDER — 8 STEPS")),
    (58, 61, slide_slam(cv, 58, 3, 125, "TIME VALUE OF MONEY")),
    (61, 67, cine_clip(cv, 61, 6, "src/v4.mp4", 9.0, z=(1.1, 1.2), centre=(0.4, 0.6), hits=[0.0],
                       captions=[(0.3, 5.9, "EVERY MIND ENGAGED", "NOTES, SAWAAL AUR JOSH", "Seekhne ki bhookh, har chehre par")])),
    (67, 71, burst(cv, 67, 4, DAY, caption=("EK DIN", "SEEKHO • SAMJHO • JEETO", None))),
    (71, 76, stat_punch(cv, 71, 5, "gap")),
    (76, 79, slide_slam(cv, 76, 3, 131, "FUTURE VALUE — LIVE CALCULATION")),
    (79, 82, slide_slam(cv, 79, 3, 144, "DER KI KEEMAT")),
    (82, 86, cine_photo(cv, 82, 4, [(P("083554"), 1, dict(z0=1.15, z1=1.0, c0=(0.55, 0.4), c1=(0.55, 0.45))),
                                    (P("083520"), 1, dict(z0=1.0, z1=1.12))],
                        caption=("SAFAR", "FOUNDER & CO-FOUNDER, EK MISSION", "Har ghar tak suraksha"))),
    (86, 90, burst(cv, 86, 4, ENERGY2, big=("LIC CHAMPIONS", 200, WHITE))),
    (90, 93, cine_photo(cv, 90, 3, [(P("085648"), 1, dict(z0=1.0, z1=1.08, fill="blur"))],
                        caption=("NEXT STOP?", "AAPKA SHEHAR!", None), who=RI)),
    (93, 98, stat_punch(cv, 93, 5, "zaroorat")),
    (98, 102, thank_you(cv, 98, 4, P("121510"))),
    (102, 109, countdown(cv, 102, 7, P("121510"), [("AGLA SESSION", 150, WHITE), ("AAPKE SHEHAR MEIN?", 150, GO)])),
    (109, 114, cine_photo(cv, 109, 5, [(P("100948"), 1, dict(z0=1.2, z1=1.0))],
                          caption=("AAPKI TEAM KE LIYE", "ABHI BOOK KAREIN!", "Har Ghar Suraksha • Wealth Tank"))),
]
TR = {8: ("flash", 0.4), 12: ("leak", 0.6), 16: ("iris", 0.6), 20: ("glitch", 0.4), 24: ("spin", 0.5), 30: ("flash", 0.3),
      33: ("flash", 0.3), 36: ("whip", 0.5), 42: ("panels", 0.6), 47: ("glitch", 0.4), 51: ("leak", 0.6), 55: ("flash", 0.3),
      58: ("flash", 0.3), 61: ("spin", 0.5), 67: ("glitch", 0.4), 71: ("iris", 0.6), 76: ("flash", 0.3), 79: ("flash", 0.3),
      82: ("whip", 0.5), 86: ("glitch", 0.4), 90: ("spin", 0.5), 93: ("panels", 0.6), 98: ("leak", 0.6), 102: ("zoom", 0.5), 109: ("flash", 0.4)}

MUSIC_DUR = 120.0
MUSIC_PLAN = [(0, 8, "cold"), (8, 24, "full"), (24, 30, "groove"), (30, 36, "full"), (36, 47, "groove"), (47, 51, "full"),
              (51, 55, "groove"), (55, 61, "full"), (61, 71, "groove"), (71, 76, "light"), (76, 93, "full"), (93, 98, "break"),
              (98, 102, "build"), (102, 109, "countdown"), (109, 114, "full"), (114, 120, "outro")]
SFX_EXTRA = [(0.5, "braam", 0.9), (2.0, "braam", 0.9), (3.5, "impact", 0.8), (4.5, "impact", 0.8), (5.5, "braam", 1.0), (8.0, "impact", 1.0),
             (30.0, "impact", 0.6), (33.0, "impact", 0.6), (55.0, "impact", 0.6), (58.0, "impact", 0.6), (76.0, "impact", 0.6),
             (79.0, "impact", 0.6), (102.0, "braam", 0.9), (103.0, "braam", 0.9), (104.0, "braam", 0.9), (105.0, "impact", 1.0),
             (114.0, "impact", 0.85), (115.2, "ding", 0.6)]

if __name__ == "__main__":
    if sys.argv[1] == "preview":
        import engine; engine.PREVDIR = sys.argv[3] if len(sys.argv) > 3 else "prev"
        run(cv, SEG, TR, 114, None, preview=[float(x) for x in sys.argv[2].split(",")])
    else:
        run(cv, SEG, TR, 114, sys.argv[1])
