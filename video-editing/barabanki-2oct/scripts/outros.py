"""Render the 6s end screens (114-120s) with phone numbers, opening on a gold flash."""
import sys
from engine import Canvas, run, Image
from cards import outro

who = sys.argv[1]; W, H = (1920, 1080) if len(sys.argv) < 4 else (1080, 1920)
t0 = float(sys.argv[3]) if len(sys.argv) > 3 else 114.0
cv = Canvas(W, H)
INFO = {"anurag": ("Anurag Kesarwani", "Co-Founder • Financial Consultant • Sales Training", "+91 95807 85406"),
        "ritesh": ("Ritesh Tripathi", "Founder • Master Facilitator & Financial Planner", "+91 93051 60843")}
base = outro(cv, t0, 6.0, *INFO[who])
def fn(t):
    img = base(t)
    if t - t0 < 0.3:
        img.alpha_composite(Image.new("RGBA", (W, H), (255, 245, 220, int(255 * (1 - (t - t0) / 0.3)))))
    return img
run(cv, [(t0, t0 + 6, fn)], {}, t0 + 6, sys.argv[2], t_from=t0)
