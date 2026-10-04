"""Reusable full-screen graphic segments: logo intro, invitation, fact punches, slide punches, thank-you, outro."""
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from engine import *
import engine
_photo_cache = engine._photo_cache

IMG = "../../images/"
RAW = "raw/"
SLIDE = "ppt/x/ppt/media/image-%d-1.jpeg"


def intro(cv, t0, dur=4.0):
    """Gold streaks -> real logo slams in with flash + shake -> tagline."""
    W, H, S = cv.W, cv.H, cv.S
    def fn(t):
        t -= t0
        img = cv.navy_bg(t)
        img.alpha_composite(cv.rays(t, eo(prog(t, 1.4, 2.1))))
        img.alpha_composite(cv.particles(t, prog(t, 0, 1)))
        if t < 1.5:
            L = cv.layer(); d = ImageDraw.Draw(L); p = eo(prog(t, 0.1, 1.5))
            for k in range(6):
                yy = H * (0.18 + k * 0.13); xx = lerp(-W if k % 2 else 2 * W, W / 2, p)
                d.rounded_rectangle([xx - 300 * S, yy - 3, xx + 300 * S, yy + 3], 3, fill=GOLD_L + (int(200 * (1 - p) + 40),))
            img.alpha_composite(L.filter(ImageFilter.GaussianBlur(1.5)))
        if t >= 1.05:
            p = prog(t, 1.05, 1.5)
            s = lerp(2.6, 1.0, ei(p)) if p < 1 else 1 + 0.06 * back(prog(t, 1.5, 1.9)) - 0.06
            base = (560 if not cv.vert else 620) * S
            lg = cv.logo(base * s)
            lg = lg.copy(); lg.putalpha(lg.split()[3].point(lambda v: int(v * prog(t, 1.05, 1.3))))
            cy = H / 2 - 70 * S - eo(prog(t, 2.1, 2.6)) * 40 * S
            img.alpha_composite(lg, (int(W / 2 - lg.width / 2), int(cy - lg.height / 2)))
            if 1.5 <= t < 1.8:
                k = (1.8 - t) / 0.3 * 14
                img = ImageChops.offset(img, int(np.random.uniform(-k, k)), int(np.random.uniform(-k, k)))
        if 1.5 <= t < 1.75:
            img.alpha_composite(Image.new("RGBA", (W, H), (255, 245, 220, int(255 * (1 - prog(t, 1.5, 1.75))))))
        L = cv.layer()
        cv.reveal(L, (W / 2, H / 2 + 270 * S), "INSURANCE  •  LOANS  •  SALES TRAINING", M(700, 36 * S), GOLD_L, prog(t, 2.2, 2.7), anchor="mt")
        cv.reveal(L, (W / 2, H / 2 + 330 * S), "presents", M(600, 30 * S), WHITE, prog(t, 2.5, 3.0), anchor="mt")
        img.alpha_composite(L)
        return img
    return fn


def invitation(cv, t0, dur):
    """Invitation poster as a tilted card that settles, with event facts beside it."""
    W, H, S = cv.W, cv.H, cv.S
    poster = load_photo(IMG + "8.jpg")
    def fn(t):
        t -= t0
        img = cv.navy_bg(t + 3); img.alpha_composite(cv.particles(t, 0.6))
        p = back(prog(t, 0.0, 0.6), 1.2)
        ph = (H * 0.86 if not cv.vert else H * 0.5) * (0.9 + 0.1 * p) * (1 + 0.03 * t / dur)
        pw = ph * poster.width / poster.height
        card = poster.resize((int(pw), int(ph)), Image.BILINEAR).convert("RGBA")
        card = card.rotate(lerp(-12, -3, eo(prog(t, 0, 0.7))), resample=Image.BICUBIC, expand=True)
        cx = W * 0.70 if not cv.vert else W / 2
        cy = H / 2 if not cv.vert else H * 0.34
        sh = Image.new("RGBA", card.size, (0, 0, 0, 0)); sh.putalpha(card.split()[3].point(lambda v: v // 2))
        sh = sh.filter(ImageFilter.GaussianBlur(20))
        x = int(cx - card.width / 2 + (1 - eo(prog(t, 0, 0.6))) * W * 0.5)
        img.alpha_composite(sh, (x + 16, int(cy - card.height / 2) + 24)); img.alpha_composite(card, (x, int(cy - card.height / 2)))
        L = cv.layer(); d = ImageDraw.Draw(L)
        tx = 110 * S if not cv.vert else W / 2
        ty = H * 0.26 if not cv.vert else H * 0.66
        an = "la" if not cv.vert else "mt"
        pk = eo(prog(t, 0.4, 0.8))
        if pk > 0:
            fk = M(800, 30 * S); txt = "AAPKA KHAAS INVITATION"; tw = d.textlength(txt, font=fk)
            bx = tx if not cv.vert else tx - (tw + 44 * S) / 2
            d.rectangle([bx, ty, bx + (tw + 44 * S) * pk, ty + 50 * S], fill=ORANGE + (255,))
            if pk > 0.6: d.text((bx + 22 * S, ty + 9 * S), txt, font=fk, fill=WHITE)
        cv.reveal(L, (tx, ty + 80 * S), "HAR GHAR", B(150 * S), WHITE, prog(t, 0.5, 0.95), anchor=an)
        cv.reveal(L, (tx, ty + 220 * S), "SURAKSHA", B(150 * S), ORANGE, prog(t, 0.65, 1.1), anchor=an)
        cv.reveal(L, (tx, ty + 390 * S), "2 October 2026", M(800, 44 * S), WHITE, prog(t, 0.9, 1.3), anchor=an)
        cv.reveal(L, (tx, ty + 450 * S), "The Regal Heritage, Barabanki", M(600, 36 * S), GOLD_L, prog(t, 1.05, 1.45), anchor=an)
        L = cv.shadow(L, 14, 150)
        img.alpha_composite(L)
        return img
    return fn


def photo_seg(cv, t0, dur, items, caption=None, bug=True, letterbox=False):
    """items: list of (path, share, kb-kwargs). Optional caption=(kicker, line, sub)."""
    tot = sum(s for _, s, _ in items)
    def fn(t):
        tl = t - t0; acc = 0.0
        for path, share, kw in items:
            seg = dur * share / tot
            if tl < acc + seg or path == items[-1][0]:
                img = photo_frame(cv, path, tl - acc, seg, **kw).convert("RGBA"); break
            acc += seg
        img.alpha_composite(cv.VIG)
        L = cv.layer()
        if caption: cv.caption(L, tl, 0.3, dur - 0.05, *caption)
        img.alpha_composite(L)
        if bug: cv.bug(img)
        if letterbox: cv.letterbox(img)
        return img
    return fn


def clip_seg(cv, t0, dur, path, src_start, z=(1.0, 1.06), centre=(0.5, 0.45), captions=(), plate=None, punch_at=None):
    """Video segment with slow push-in; captions=[(a, b, kicker, line, sub)], plate=(a, b, role, name, l2, l3)."""
    C = Clip(path, src_start)
    def fn(t):
        tl = t - t0
        zz = lerp(z[0], z[1], clamp(tl / dur))
        if punch_at is not None and tl >= punch_at: zz += 0.18
        img = zoom(cv, C.frame(tl, cv.W, cv.H), zz, *centre).convert("RGBA"); img.alpha_composite(cv.VIG)
        L = cv.layer()
        for a, b, *cap in captions: cv.caption(L, tl, a, b, *cap)
        if plate: cv.name_plate(L, tl, *plate)
        img.alpha_composite(L); cv.bug(img)
        return img
    return fn


def slide_punch(cv, t0, dur, slide_no, kicker="SESSION HIGHLIGHT", focus=(0.5, 0.5), zoom_to=1.25):
    """Actual session slide: drops in as a floating screen over blurred venue, then pushes into its key number."""
    W, H, S = cv.W, cv.H, cv.S
    sl = load_photo(SLIDE % slide_no, 2048)
    bgp = RAW + "20261002_100948.jpg"
    def fn(t):
        tl = t - t0
        key = ("slbg", W, H)
        if key not in _photo_cache:
            b = ImageOps.fit(load_photo(bgp), (W // 4, H // 4)).filter(ImageFilter.GaussianBlur(6)).resize((W, H), Image.BILINEAR)
            _photo_cache[key] = ImageEnhance.Brightness(b).enhance(0.45).convert("RGBA")
        img = _photo_cache[key].copy()
        p = back(prog(tl, 0, 0.55), 1.3)
        zf = 1.0
        sw = (W * 0.80 if not cv.vert else W * 0.92) * (0.85 + 0.15 * p) * (1 + 0.06 * eio(prog(tl, 0.6, dur)))
        sh = sw * 9 / 16
        # crop slide towards focus as it zooms
        iw, ih = sl.size; cw, ch = iw / zf, ih / zf
        x0 = clamp(focus[0] * iw - cw / 2, 0, iw - cw); y0 = clamp(focus[1] * ih - ch / 2, 0, ih - ch)
        card = sl.resize((int(sw), int(sh)), Image.BILINEAR, box=(x0, y0, x0 + cw, y0 + ch)).convert("RGBA")
        cy = H / 2 + 30 * S if not cv.vert else H * 0.45
        y = cy - sh / 2 + (1 - eo(prog(tl, 0, 0.5))) * H * 0.6
        shd = Image.new("RGBA", (int(sw) + 80, int(sh) + 80), (0, 0, 0, 0))
        ImageDraw.Draw(shd).rectangle([40, 40, 40 + sw, 40 + sh], fill=(0, 0, 0, 170))
        img.alpha_composite(shd.filter(ImageFilter.GaussianBlur(24)), (int(W / 2 - sw / 2 - 40), int(y - 20)))
        d = ImageDraw.Draw(img)
        d.rectangle([W / 2 - sw / 2 - 6, y - 6, W / 2 + sw / 2 + 6, y + sh + 6], fill=GOLD + (255,))
        img.alpha_composite(card, (int(W / 2 - sw / 2), int(y)))
        L = cv.layer(); dl = ImageDraw.Draw(L)
        pk = eo(prog(tl, 0.4, 0.8))
        if pk > 0:
            fk = M(800, 30 * S); tw = dl.textlength(kicker, font=fk); bw = (tw + 44 * S) * pk
            ky = y - 70 * S if not cv.vert else y - 80 * S
            dl.rectangle([W / 2 - bw / 2, ky, W / 2 + bw / 2, ky + 50 * S], fill=GOLD + (255,))
            if pk > 0.6: dl.text((W / 2, ky + 25 * S), kicker, font=fk, fill=NAVY, anchor="mm")
        img.alpha_composite(L); cv.bug(img)
        return img
    return fn


def stat_punch(cv, t0, dur, kind):
    """Researched fact punches drawn as animated infographics."""
    W, H, S = cv.W, cv.H, cv.S
    def fn(t):
        tl = t - t0
        img = cv.navy_bg(t); img.alpha_composite(cv.particles(t, 0.5))
        L = cv.layer(); d = ImageDraw.Draw(L)
        if kind == "penetration":
            cv.reveal(L, (W / 2, H * 0.12), "INDIA KA BADA MAUKA", B(110 * S), WHITE, prog(tl, 0.1, 0.5), anchor="mt")
            cv.reveal(L, (W / 2, H * 0.12 + 120 * S), "Insurance penetration (premium as % of GDP)", M(600, 34 * S), GOLD_L, prog(tl, 0.3, 0.7), anchor="mt")
            bars = [("INDIA", 3.7, ORANGE, 0.6), ("WORLD AVERAGE", 7.3, (120, 160, 220), 0.9)]
            maxh = H * (0.42 if not cv.vert else 0.32)
            for i, (lab, v, col, ts) in enumerate(bars):
                p = eo(prog(tl, ts, ts + 1.2))
                bw = (220 if not cv.vert else 260) * S
                cx = W / 2 + (-1 if i == 0 else 1) * (200 if not cv.vert else 230) * S
                base = H * (0.82 if not cv.vert else 0.72)
                h = maxh * v / 7.3 * p
                d.rounded_rectangle([cx - bw / 2, base - h, cx + bw / 2, base], 12, fill=col + (255,))
                d.text((cx, base - h - 20 * S), f"{v * p:.1f}%", font=M(900, 70 * S), fill=WHITE, anchor="mb")
                d.text((cx, base + 20 * S), lab, font=M(800, 30 * S), fill=WHITE, anchor="mt")
            pt = back(prog(tl, 2.6, 3.0))
            if pt > 0:
                st = Image.new("RGBA", (int(620 * S), int(120 * S)), (0, 0, 0, 0)); sd = ImageDraw.Draw(st)
                sd.rounded_rectangle([0, 0, st.width - 1, st.height - 1], 20, fill=GOLD + (255,))
                sd.text((st.width / 2, st.height / 2), "AADHA BHI NAHI = BADA MAUKA!", font=B(64 * S), fill=NAVY, anchor="mm")
                st = st.rotate(-3, resample=Image.BICUBIC, expand=True)
                st = st.resize((max(2, int(st.width * pt)), max(2, int(st.height * pt))), Image.BILINEAR)
                pos = (int(W / 2 - st.width / 2), int(H * 0.86 - st.height / 2)) if cv.vert else (int(W * 0.80 - st.width / 2), int(H * 0.52 - st.height / 2))
                L.alpha_composite(st, pos)
            src = "Source: IRDAI Annual Report 2024-25"
        elif kind == "gap":
            cv.reveal(L, (W / 2, H * 0.12), "HAR GHAR KO SURAKSHA CHAHIYE", B(100 * S), WHITE, prog(tl, 0.1, 0.5), anchor="mt")
            cv.reveal(L, (W / 2, H * 0.12 + 115 * S), "Ek family ko jitni protection chahiye...", M(600, 34 * S), GOLD_L, prog(tl, 0.3, 0.7), anchor="mt")
            gw = (W * 0.7 if not cv.vert else W * 0.84); gx = W / 2 - gw / 2
            gy = H * (0.42 if not cv.vert else 0.40); gh = 110 * S
            p1 = eo(prog(tl, 0.6, 1.4)); p2 = eo(prog(tl, 1.6, 2.4))
            d.rounded_rectangle([gx, gy, gx + gw * p1, gy + gh], 16, fill=(120, 160, 220, 255))
            if p1 > 0.3: cv.rtext(d, (gx + 30 * S, gy + gh / 2), "Zaroorat: ₹100", 800, 44 * S, NAVY, anchor="lm")
            d.rounded_rectangle([gx, gy + gh + 40 * S, gx + max(gw * 0.078 * p2, 6), gy + 2 * gh + 40 * S], 16, fill=ORANGE + (255,))
            if p2 > 0.3: cv.rtext(d, (gx + gw * 0.078 + 30 * S, gy + gh * 1.5 + 40 * S), "Cover hai: sirf ₹7.8", 800, 44 * S, WHITE, anchor="lm")
            pg = eo(prog(tl, 2.7, 3.2))
            if pg > 0:
                cv.reveal(L, (W / 2, gy + 2 * gh + 120 * S), "92% GAP = AAPKA MAUKA", B(120 * S), GOLD, pg, anchor="mt")
            src = "Source: Swiss Re mortality protection gap study (2015)"
        elif kind == "zaroorat":
            cv.reveal(L, (W / 2, H * 0.20), "PRODUCT MAT BECHO,", B(150 * S), WHITE, prog(tl, 0.1, 0.5), anchor="mt")
            cv.reveal(L, (W / 2, H * 0.20 + 150 * S), "ZAROORAT SAMJHAO", B(150 * S), ORANGE, prog(tl, 0.3, 0.7), anchor="mt")
            cv.reveal(L, (W / 2, H * 0.20 + 320 * S), "— income triple karo!", M(700, 46 * S), GOLD_L, prog(tl, 0.6, 1.0), anchor="mt")
            pc = back(prog(tl, 1.5, 1.9))
            if pc > 0:
                bw, bh = (900 if not cv.vert else 940) * S * pc, 150 * S * pc
                by = H * (0.66 if not cv.vert else 0.62)
                d.rounded_rectangle([W / 2 - bw / 2, by, W / 2 + bw / 2, by + bh], 20, fill=(255, 255, 255, 30), outline=GOLD + (255,), width=3)
                if pc > 0.8:
                    d.text((W / 2, by + 48 * S), "~98% LIC policies", font=M(900, 54 * S), fill=GOLD, anchor="mm")
                    d.text((W / 2, by + 108 * S), "aap jaise advisors ke through bikti hain (FY25)", font=M(600, 30 * S), fill=WHITE, anchor="mm")
            src = "Source: LIC analyst & investor meet, June 2025"
        L = cv.shadow(L, 14, 140); img.alpha_composite(L)
        ImageDraw.Draw(img).text((W - 30 * S, H - 26 * S), src, font=M(600, 20 * S), fill=(200, 205, 220, 220), anchor="rb")
        cv.bug(img)
        return img
    return fn


def thank_you(cv, t0, dur, bg_path):
    W, H, S = cv.W, cv.H, cv.S
    def fn(t):
        tl = t - t0
        img = photo_frame(cv, bg_path, tl, dur, 1.15, 1.0).convert("RGBA")
        img = img.filter(ImageFilter.GaussianBlur(lerp(0, 10, eo(prog(tl, 0, 0.6)))))
        img.alpha_composite(Image.new("RGBA", (W, H), NAVY_D + (int(190 * eo(prog(tl, 0, 0.6))),)))
        img.alpha_composite(cv.particles(t, 0.6))
        L = cv.layer(); d = ImageDraw.Draw(L)
        pl = eo(prog(tl, 0.1, 0.6)); lg = cv.logo((200 if not cv.vert else 260) * S).copy()
        lg.putalpha(lg.split()[3].point(lambda v: int(v * pl)))
        img.alpha_composite(lg, (int(W / 2 - lg.width / 2), int(H * 0.30 - lg.height - 30 * S)))
        gw = 420 * S * eo(prog(tl, 0.2, 0.7))
        d.rectangle([W / 2 - gw / 2, H * 0.30, W / 2 + gw / 2, H * 0.30 + 6], fill=GOLD + (255,))
        cv.reveal(L, (W / 2, H * 0.30 + 40 * S), "DIL SE DHANYAVAAD", B(150 * S), WHITE, prog(tl, 0.3, 0.8), anchor="mt")
        cv.reveal(L, (W / 2, H * 0.30 + 200 * S), "LIC TEAM BARABANKI", B(120 * S), GOLD, prog(tl, 0.5, 1.0), anchor="mt")
        cv.reveal(L, (W / 2, H * 0.30 + 340 * S), "aur sabhi LIC Champions ko — aapke josh ke liye!", M(600, 38 * S), WHITE, prog(tl, 0.8, 1.3), anchor="mt")
        L = cv.shadow(L, 16, 160); img.alpha_composite(L)
        return img
    return fn


def outro(cv, t0, dur, name, role, phone):
    W, H, S = cv.W, cv.H, cv.S
    def fn(t):
        tl = t - t0
        img = cv.navy_bg(t); img.alpha_composite(cv.rays(t, 0.8)); img.alpha_composite(cv.particles(t))
        p = back(prog(tl, 0, 0.5))
        size = (330 if not cv.vert else 420) * S * p
        lg = cv.logo(size)
        ly = H * (0.24 if not cv.vert else 0.22)
        img.alpha_composite(lg, (int(W / 2 - lg.width / 2), int(ly - lg.height / 2)))
        L = cv.layer(); d = ImageDraw.Draw(L)
        y = ly + (200 if not cv.vert else 260) * S
        cv.reveal(L, (W / 2, y), "AAPKI TEAM KE LIYE BHI? ABHI CALL KAREIN!", B(88 * S if not cv.vert else 70 * S), WHITE, prog(tl, 0.5, 1.0), anchor="mt")
        cv.reveal(L, (W / 2, y + 110 * S), name, M(800, 52 * S), GOLD, prog(tl, 0.7, 1.2), anchor="mt")
        cv.reveal(L, (W / 2, y + 180 * S), role, M(600, 30 * S), WHITE, prog(tl, 0.85, 1.3), anchor="mt")
        pb = back(prog(tl, 1.2, 1.6))
        if pb > 0:
            bw, bh = min(W - 80, 900 * S) * pb, 110 * S * pb; by = y + 255 * S
            pulse = 1 + 0.03 * math.sin((tl - 1.6) * 2 * math.pi * 1.2) * (tl > 1.6)
            bw *= pulse; bh *= pulse
            d.rounded_rectangle([W / 2 - bw / 2, by, W / 2 + bw / 2, by + bh], int(bh / 2), fill=GOLD + (255,))
            if pb > 0.7:
                txt = "Call / WhatsApp:  " + phone
                d.text((W / 2, by + bh / 2), txt, font=cv.fit_text(d, txt, lambda s: M(800, s), 46 * S * pb, bw - 80 * S), fill=NAVY, anchor="mm")
        cv.reveal(L, (W / 2, y + 410 * S), "Wealth Tank  •  Har Ghar Suraksha", M(600, 30 * S), GOLD_L, prog(tl, 1.4, 1.9), anchor="mt")
        L = cv.shadow(L, 14, 150); img.alpha_composite(L)
        if tl > dur - 0.8: img.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, int(255 * prog(tl, dur - 0.8, dur)))))
        return img
    return fn


def modules_card(cv, t0, dur, title="EK DIN  •  4 POWER MODULES"):
    """What the training covered (modules 01-04 of the deck) – sells the depth of the programme."""
    W, H, S = cv.W, cv.H, cv.S
    MODS = [("01", "Why Need Based Selling"), ("02", "Success Habits & Income Plan"),
            ("03", "Reaching Maximum Customers"), ("04", "Finding Needs with HLV & TVM")]
    def fn(t):
        tl = t - t0
        img = cv.navy_bg(t + 7); img.alpha_composite(cv.particles(t, 0.5))
        L = cv.layer(); d = ImageDraw.Draw(L)
        cv.reveal(L, (W / 2, H * 0.10), "HAR GHAR SURAKSHA", B(70 * S), ORANGE, prog(tl, 0.0, 0.4), anchor="mt")
        cv.reveal(L, (W / 2, H * 0.10 + 80 * S), title, B(110 * S), WHITE, prog(tl, 0.15, 0.55), anchor="mt")
        cols = 1 if cv.vert else 2
        cw = (W * 0.38 if not cv.vert else W * 0.84); ch = 150 * S
        for i, (n, txt) in enumerate(MODS):
            p = back(prog(tl, 0.6 + i * 0.35, 1.0 + i * 0.35))
            if p <= 0: continue
            r, c = (i // cols, i % cols)
            x = (W / 2 - cw - 20 * S + c * (cw + 40 * S)) if cols == 2 else W / 2 - cw / 2
            y = H * (0.40 if not cv.vert else 0.32) + r * (ch + 30 * S)
            card = Image.new("RGBA", (int(cw), int(ch)), (0, 0, 0, 0)); cd = ImageDraw.Draw(card)
            cd.rounded_rectangle([0, 0, cw - 1, ch - 1], 18, fill=(255, 255, 255, 235))
            cd.rectangle([0, 0, 12 * S, ch], fill=ORANGE + (255,))
            cd.text((40 * S, ch / 2), n, font=M(900, 64 * S), fill=ORANGE, anchor="lm")
            cd.text((140 * S, ch / 2), txt, font=cv.fit_text(cd, txt, lambda s: M(800, s), 34 * S, cw - 260 * S), fill=NAVY, anchor="lm")
            ck = prog(tl, 0.9 + i * 0.35, 1.2 + i * 0.35)
            if ck > 0:
                cx, cy = cw - 60 * S, ch / 2
                cd.ellipse([cx - 32 * S, cy - 32 * S, cx + 32 * S, cy + 32 * S], fill=(30, 160, 90, 255))
                cd.line([(cx - 14 * S, cy), (cx - 3 * S, cy + 12 * S), (cx + 16 * S, cy - 12 * S)], fill=WHITE, width=int(7 * S))
            card = card.resize((max(2, int(cw * p)), max(2, int(ch * p))), Image.BILINEAR)
            L.alpha_composite(card, (int(x + cw / 2 - card.width / 2), int(y + ch / 2 - card.height / 2)))
        L = cv.shadow(L, 14, 140); img.alpha_composite(L); cv.bug(img)
        return img
    return fn
