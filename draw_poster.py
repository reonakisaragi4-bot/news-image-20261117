#!/usr/bin/env python3
"""Draw the news poster for Tuesday 17 November 2026.

One 1024x1024 PNG: masthead + six panels, one per verified story of the day.
Flat colours only, so the PNG stays well under 1 MiB. Run from the repo dir:
    python3 draw_poster.py
"""
import textwrap

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FONT_DIR = "/usr/share/fonts/truetype/dejavu/"

F_TITLE = ImageFont.truetype(FONT_DIR + "DejaVuSans-Bold.ttf", 58)
F_DATE = ImageFont.truetype(FONT_DIR + "DejaVuSans-Bold.ttf", 40)
F_SUB = ImageFont.truetype(FONT_DIR + "DejaVuSans.ttf", 21)
F_KICK = ImageFont.truetype(FONT_DIR + "DejaVuSans-Bold.ttf", 19)
F_HEAD = ImageFont.truetype(FONT_DIR + "DejaVuSans-Bold.ttf", 29)
F_CAP = ImageFont.truetype(FONT_DIR + "DejaVuSans.ttf", 21)
F_FOOT = ImageFont.truetype(FONT_DIR + "DejaVuSans.ttf", 17)

NAVY = (11, 31, 58)
GOLD = (212, 175, 55)
RED = (178, 34, 34)
PAPER = (247, 243, 234)
INK = (18, 18, 18)
GREY = (90, 90, 90)
WHITE = (255, 255, 255)

# (kicker, headline, caption, accent colour)
STORIES = [
    ("UKRAINE  •  WAR",
     "UKRAINE STRIKES CRIMEA BRIDGE AGAIN",
     "Kyiv hits the Kerch bridge a second day running. Russia strikes Kyiv's "
     "bridges over the Dnipro, disrupting heating, water and power.",
     (178, 34, 34)),
    ("GULF  •  ENERGY",
     "TANKERS HIT NEAR HORMUZ",
     "Mines strike tankers near the Strait of Hormuz. Iran fires drones at a "
     "US radar base in Bahrain \u2014 intercepted, no casualties.",
     (0, 102, 102)),
    ("DIPLOMACY  •  CHINA",
     "XI\u2013TRUMP\u2013PUTIN SUMMIT SET",
     "China confirms the first three-way meeting of Xi, Trump and Putin: "
     "Thursday 19 Nov in Shenzhen, on APEC sidelines.",
     (146, 90, 0)),
    ("USA  •  MILITARY",
     "THIRD US CARRIER IN MIDDLE EAST",
     "USS Theodore Roosevelt joins two other US carriers already in the region.",
     (11, 31, 58)),
    ("USA  •  DEFENCE",
     "PENTAGON FAILS AUDIT AGAIN",
     "Ninth year running: auditors cannot verify accounts covering "
     "$4.8 trillion in assets.",
     (90, 30, 120)),
    ("FRANCE  •  COURTS",
     "DEPARDIEU PLEADS GUILTY",
     "French actor G\u00e9rard Depardieu drops his appeal and admits a "
     "sexual-assault charge in Paris.",
     (0, 90, 60)),
]


def wrap(text, font, max_w):
    """Greedy word wrap by pixel width."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        cur = ""
        for w in words:
            trial = (cur + " " + w).strip()
            if font.getlength(trial) <= max_w:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
    return lines


def draw_bridge(d, x, y, s, c):
    # Simple suspension bridge: deck, two towers, arc cable.
    d.line([(x, y + 26 * s), (x + 72 * s, y + 26 * s)], fill=c, width=max(3, int(3 * s)))
    for tx in (x + 10 * s, x + 56 * s):
        d.line([(tx, y + 4 * s), (tx, y + 26 * s)], fill=c, width=max(3, int(3 * s)))
    d.arc([x, y - 6 * s, x + 72 * s, y + 30 * s], 180, 360, fill=c, width=max(2, int(2 * s)))
    d.line([(x + 6 * s, y + 30 * s), (x + 66 * s, y + 30 * s)], fill=c, width=max(2, int(2 * s)))


def draw_ship(d, x, y, s, c):
    # Tanker: hull + containers + waves.
    d.polygon([(x, y + 14 * s), (x + 70 * s, y + 14 * s), (x + 62 * s, y + 28 * s),
               (x + 8 * s, y + 28 * s)], fill=c)
    d.rectangle([x + 12 * s, y + 2 * s, x + 26 * s, y + 14 * s], fill=c)
    d.rectangle([x + 30 * s, y + 6 * s, x + 44 * s, y + 14 * s], fill=c)
    d.arc([x, y + 30 * s, x + 24 * s, y + 40 * s], 180, 360, fill=c, width=max(2, int(2 * s)))
    d.arc([x + 26 * s, y + 30 * s, x + 50 * s, y + 40 * s], 180, 360, fill=c, width=max(2, int(2 * s)))
    d.arc([x + 52 * s, y + 30 * s, x + 72 * s, y + 40 * s], 180, 360, fill=c, width=max(2, int(2 * s)))


def draw_flags(d, x, y, s, c):
    # Three small flags on poles (three leaders, one table).
    for i, col in enumerate([(178, 34, 34), (11, 31, 58), (0, 102, 102)]):
        px = x + i * 24 * s
        d.line([(px, y), (px, y + 34 * s)], fill=c, width=max(2, int(2 * s)))
        d.polygon([(px, y), (px + 18 * s, y + 5 * s), (px, y + 10 * s)], fill=col)
    d.line([(x - 4 * s, y + 36 * s), (x + 72 * s, y + 36 * s)], fill=c, width=max(3, int(3 * s)))


def draw_carrier(d, x, y, s, c):
    # Aircraft carrier: long flat deck, island, hull.
    d.rectangle([x, y + 10 * s, x + 72 * s, y + 16 * s], fill=c)
    d.rectangle([x + 50 * s, y, x + 60 * s, y + 10 * s], fill=c)
    d.polygon([(x + 6 * s, y + 16 * s), (x + 66 * s, y + 16 * s),
               (x + 56 * s, y + 30 * s), (x + 16 * s, y + 30 * s)], fill=c)
    d.arc([x, y + 32 * s, x + 24 * s, y + 42 * s], 180, 360, fill=c, width=max(2, int(2 * s)))
    d.arc([x + 26 * s, y + 32 * s, x + 50 * s, y + 42 * s], 180, 360, fill=c, width=max(2, int(2 * s)))


def draw_audit(d, x, y, s, c):
    # Ledger page with a big red cross.
    d.rectangle([x + 8 * s, y, x + 46 * s, y + 38 * s], outline=c, width=max(2, int(2 * s)))
    for i in range(3):
        d.line([(x + 14 * s, y + (8 + i * 8) * s), (x + 40 * s, y + (8 + i * 8) * s)],
               fill=c, width=max(2, int(2 * s)))
    d.line([(x + 48 * s, y + 4 * s), (x + 70 * s, y + 26 * s)], fill=(178, 34, 34),
           width=max(4, int(4 * s)))
    d.line([(x + 70 * s, y + 4 * s), (x + 48 * s, y + 26 * s)], fill=(178, 34, 34),
           width=max(4, int(4 * s)))


def draw_gavel(d, x, y, s, c):
    # Gavel: angled head + handle + base.
    d.rectangle([x + 6 * s, y + 2 * s, x + 46 * s, y + 16 * s], fill=c)
    d.line([(x + 26 * s, y + 16 * s), (x + 46 * s, y + 36 * s)], fill=c,
           width=max(4, int(4 * s)))
    d.line([(x + 2 * s, y + 38 * s), (x + 56 * s, y + 38 * s)], fill=c,
           width=max(3, int(3 * s)))


ICONS = [draw_bridge, draw_ship, draw_flags, draw_carrier, draw_audit, draw_gavel]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- Masthead ---
    d.rectangle([0, 0, W, 158], fill=NAVY)
    d.rectangle([0, 158, W, 164], fill=GOLD)
    title = "THE WORLD IN ONE DAY"
    tw = d.textlength(title, font=F_TITLE)
    d.text(((W - tw) / 2, 14), title, font=F_TITLE, fill=WHITE)
    date = "TUESDAY 17 NOVEMBER 2026"
    dw = d.textlength(date, font=F_DATE)
    d.text(((W - dw) / 2, 84), date, font=F_DATE, fill=GOLD)
    sub = "Six stories from around the globe \u2014 one day"
    sw = d.textlength(sub, font=F_SUB)
    d.text(((W - sw) / 2, 128), sub, font=F_SUB, fill=(200, 210, 225))

    # --- Panels: 2 cols x 3 rows ---
    margin, gap = 24, 16
    pw = (W - 2 * margin - gap) // 2
    ph = 258
    top = 182
    for i, (kicker, headline, caption, accent) in enumerate(STORIES):
        col, row = i % 2, i // 2
        x0 = margin + col * (pw + gap)
        y0 = top + row * (ph + gap)
        d.rectangle([x0, y0, x0 + pw, y0 + ph], fill=WHITE, outline=(200, 195, 180), width=2)
        d.rectangle([x0, y0, x0 + pw, y0 + 8], fill=accent)
        # Icon top-right, kicker top-left.
        ICONS[i](d, x0 + pw - 92, y0 + 26, 1.0, accent)
        d.text((x0 + 18, y0 + 24), kicker, font=F_KICK, fill=accent)
        # Headline, wrapped, below kicker.
        hl = wrap(headline, F_HEAD, pw - 36)
        hy = y0 + 56
        for line in hl:
            d.text((x0 + 18, hy), line, font=F_HEAD, fill=INK)
            hy += 36
        # Caption.
        cy = hy + 6
        for line in wrap(caption, F_CAP, pw - 36):
            d.text((x0 + 18, cy), line, font=F_CAP, fill=(40, 40, 40))
            cy += 27

    # --- Footer ---
    foot = "All six stories happened or were first reported on Tuesday 17 November 2026."
    fw = d.textlength(foot, font=F_FOOT)
    d.text(((W - fw) / 2, 996), foot, font=F_FOOT, fill=GREY)

    img.save("entry.png", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()
