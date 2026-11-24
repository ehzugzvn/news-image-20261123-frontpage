#!/usr/bin/env python3
"""FRONTPAGE variant - classic broadsheet, one day: Monday 23 Nov 2026."""
import os
from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
FD = os.path.join(BASE, "fonts")
W, H = 1024, 1024
CREAM = (248, 243, 230)
INK = (20, 20, 20)
RED = (176, 42, 30)
DARK = (20, 20, 20)
GREY = (90, 85, 75)
BLUE = (35, 85, 160)
LIGHT = (232, 222, 198)
WHITE = (255, 255, 255)

def F(name, size):
    return ImageFont.truetype(os.path.join(FD, name), size)

SERIF_B = "LiberationSerif-Bold.ttf"
SERIF = "LiberationSerif-Regular.ttf"
SANS_B = "LiberationSans-Bold.ttf"
SANS = "LiberationSans-Regular.ttf"

def wrap(draw, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def text_block(draw, x, y, text, font, fill, maxw, lh, max_lines=None):
    lines = wrap(draw, text, font, maxw)
    if max_lines and len(lines) > max_lines:
        lines = lines[:max_lines]
        # ellipsize last line
        while lines[-1] and draw.textlength(lines[-1] + "...", font=font) > maxw:
            lines[-1] = lines[-1][:-1]
        lines[-1] = lines[-1].rstrip() + "..."
    for ln in lines:
        draw.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y

def chip(draw, x, y, label, font):
    w = int(draw.textlength(label, font=font)) + 16
    draw.rectangle([x, y, x + w, y + 24], fill=RED)
    draw.text((x + 8, y + 3), label, font=font, fill=WHITE)
    return w

# ---- content (own wording, facts from the day) ----
TIMELINE = [
    ("00:18", "Asian markets tumble"), ("00:39", "WHO Ebola warning"),
    ("01:23", "Democrats hit 258"), ("01:53", "Poland plot claim"),
    ("02:35", "Factory toll 24"), ("02:59", "Corvette sunk"),
    ("03:15", "Belgium airports shut"), ("04:21", "Arena evacuated"),
    ("05:15", "COP31 collapses"), ("05:33", "Boy pulled alive"),
    ("05:38", "Medics figure out"), ("06:08", "Syria-EU talks"),
]
LEADS = [
    ("NO DEAL", "COP31 TALKS COLLAPSE",
     "Longest UN climate summit ends in Turkiye with no deal after overtime; hosts cite hard geopolitical times.",
     "CONFIRMED - BBC, The Guardian", "cop"),
    ("SEA DRONE STRIKE", "RUSSIAN CORVETTE SUNK",
     "Suspected Ukrainian sea drone sinks corvette Merkury at its Benghazi refuelling stop; Kyiv silent.",
     "CONFIRMED - BBC, Al Jazeera", "ship"),
    ("ALIVE AFTER 14 HOURS", "BOY, 7, PULLED FROM RUBBLE",
     "Rescuers free David, 7, after 14 hours in a Dymer block hit by a strike that killed 11.",
     "CONFIRMED - BBC, Al Jazeera", "rubble"),
    ("258 SEATS", "DEMOCRATS TAKE THE HOUSE",
     "North Carolina flip gives Democrats 258 seats to 173 - biggest majority since 1992; 4 races open.",
     "OFFICIAL - BBC, Al Jazeera", "house"),
]
NUMBERS = [
    ("258", "House seats, most since '92"),
    ("14 HRS", "boy trapped in rubble"),
    ("24", "dead in factory fire"),
    ("350%", "medic attacks rise"),
    ("4 TONNES", "US Army blast planned"),
    ("90M+", "Tamagotchi at 30"),
]
TIER_LEFT = [
    ("BELGIUM FLIGHTS OFF", "Controllers strike, flights off.", "REPORTED - Al Jazeera", "plane"),
    ("MEDIC ATTACKS UP 350%", "Rights group: surge in West Bank.", "REPORTED - Al Jazeera, PHRI", "amb"),
    ("EBOLA AT 'GRAVE RISK'", "Fighting threatens Congo response.", "CONFIRMED - BBC, WHO", "virus"),
    ("FACTORY FIRE: 24 DEAD", "Indonesia candy plant; 30 still missing.", "CONFIRMED - BBC Asia", "fire"),
    ("ARMY TO BLOW UP 4T", "Unstable explosive in Iowa; court stay.", "REPORTED - Al Jazeera", "warn"),
]
TIER_RIGHT = [
    ("POLAND: RUSSIA PLOT", "Warsaw: Moscow plotted killing.", "REPORTED - Al Jazeera", "mic"),
    ("ARENA EVACUATED", "Co-op Live emptied mid-show.", "CONFIRMED - BBC", "arena"),
    ("MARKETS TUMBLE ON AI", "Tech sell-off deepens across Asia.", "REPORTED - Al Jazeera, BBC", "chart"),
    ("PARIS MARCHES FILL", "'Destroy capitalism, not France' - BBC.", "REPORTED - BBC", "fist"),
    ("SYRIA-EU TALKS MOVE", "Progress; return fears remain.", "REPORTED - Al Jazeera", "shake"),
]
PINS = [
    (1, 28.9, 41.0), (2, 20.1, 32.1), (3, 30.5, 50.4), (4, -77.0, 38.9),
    (5, 4.35, 50.85), (6, 35.2, 31.9), (7, 23.0, -2.5), (8, 107.0, -6.2),
    (9, -93.5, 42.0), (10, 21.0, 52.2), (11, -2.24, 53.5), (12, 114.2, 22.3),
]
BRIEF_COLS = [
    ("EUROPE", [
        "NHS starts AI cancer trial",
        "Poundland: days to find buyer",
        "Jeweller Bulgari dies, 89",
        "Cost protests sweep cities",
        "Man Utd lose 4-0 to Liverpool",
        "Spain: Feijoo leads polls",
        "NZ-India Test ends in draw",
    ]),
    ("AMERICAS / ASIA", [
        "Bayer $7.25bn deal approved",
        "Trump threatens AI centre ban",
        "Claim: AI Riemann proof",
        "Tamagotchi at 30: 90m shipped",
        "Onosato: back-to-back sumo",
        "Snow isolates 1,000 in Japan",
        "Rikers closure planned 2032",
    ]),
    ("UK / WORLD", [
        "PIP needs overhaul - minister",
        "RAF: next jet may be last crewed",
        "Energy bills to soar - warning",
        "Nigeria: suicide bid reform",
        "Costa Rica reporter murdered",
        "UFO footage: 8th tranche out",
        "Cameroon ex-rebels fear arrest",
    ]),
]

# ---- illustration helpers ----
def art_cop(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(210, 225, 235))
    # table
    d.rectangle([x + 20, y + h - 18, x + w - 20, y + h - 8], fill=(110, 80, 50))
    # cracked globe
    cx, cy, r = x + w // 2, y + h // 2 - 2, 24
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(70, 140, 200), outline=INK, width=2)
    d.line([cx - 10, cy - 20, cx + 2, cy - 4, cx - 6, cy + 8, cx + 8, cy + 22], fill=INK, width=2)
    d.line([cx - 22, cy + 2, cx + 22, cy + 2], fill=INK, width=1)
    d.text((cx + r + 6, cy - 10), "1.5C", font=F(SANS_B, 15), fill=RED)

def art_ship(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(25, 35, 60))
    d.rectangle([x, y + h - 16, x + w, y + h], fill=(15, 60, 90))
    # listing ship
    d.polygon([(x + 70, y + 34), (x + 190, y + 26), (x + 200, y + 44), (x + 80, y + 50)], fill=(150, 150, 155), outline=INK)
    d.rectangle([x + 115, y + 16, x + 150, y + 30], fill=(120, 120, 125), outline=INK)
    # drone boat
    d.polygon([(x + 215, y + 48), (x + 245, y + 48), (x + 238, y + 56), (x + 220, y + 56)], fill=RED, outline=WHITE)
    # crane
    d.line([x + 30, y + 8, x + 30, y + 44], fill=(200, 180, 80), width=3)
    d.line([x + 30, y + 8, x + 75, y + 8], fill=(200, 180, 80), width=3)

def art_rubble(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(225, 210, 180))
    for i in range(7):
        bx = x + 18 + i * 34
        d.polygon([(bx, y + h - 10), (bx + 16, y + h - 34 - (i % 3) * 8), (bx + 32, y + h - 10)], fill=(150, 145, 135), outline=INK)
    # rescuers + child
    d.ellipse([x + 105, y + 18, x + 121, y + 34], fill=(255, 200, 40), outline=INK)
    d.rectangle([x + 108, y + 34, x + 118, y + 50], fill=(255, 120, 20))
    d.ellipse([x + 132, y + 24, x + 144, y + 36], fill=(255, 220, 180), outline=INK)
    d.rectangle([x + 134, y + 36, x + 142, y + 48], fill=BLUE)
    d.ellipse([x + 155, y + 18, x + 171, y + 34], fill=(255, 200, 40), outline=INK)
    d.rectangle([x + 158, y + 34, x + 168, y + 50], fill=(255, 120, 20))

def art_house(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(215, 225, 240))
    cx = x + 62
    d.arc([cx - 28, y + 6, cx + 28, y + 44], 180, 360, fill=INK, width=3)
    d.rectangle([cx - 30, y + 26, cx + 30, y + 32], fill=WHITE, outline=INK)
    for i in range(4):
        d.rectangle([cx - 24 + i * 14, y + 32, cx - 18 + i * 14, y + 48], fill=WHITE, outline=INK)
    # seat bars
    bx = x + 115
    d.rectangle([bx, y + 14, bx + 150, y + 28], fill=BLUE)
    d.text((bx + 4, y + 16), "258", font=F(SANS_B, 13), fill=WHITE)
    d.rectangle([bx, y + 34, bx + 100, y + 48], fill=RED)
    d.text((bx + 4, y + 36), "173", font=F(SANS_B, 13), fill=WHITE)

ART = {"cop": art_cop, "ship": art_ship, "rubble": art_rubble, "house": art_house}

def pictogram(d, x, y, kind):
    # simple bold glyph in a 36px box
    d.rectangle([x, y, x + 36, y + 36], fill=LIGHT, outline=INK, width=1)
    if kind == "plane":
        d.polygon([(x + 6, y + 22), (x + 30, y + 10), (x + 26, y + 24), (x + 18, y + 26)], fill=INK)
        d.line([x + 5, y + 30, x + 31, y + 6], fill=RED, width=3)
    elif kind == "amb":
        d.rectangle([x + 7, y + 10, x + 29, y + 26], fill=WHITE, outline=RED, width=2)
        d.rectangle([x + 15, y + 13, x + 21, y + 23], fill=RED)
        d.rectangle([x + 12, y + 16, x + 24, y + 20], fill=RED)
    elif kind == "virus":
        d.ellipse([x + 11, y + 11, x + 25, y + 25], fill=RED)
        for a in [(18, 6), (18, 30), (6, 18), (30, 18)]:
            d.ellipse([x + a[0] - 3, y + a[1] - 3, x + a[0] + 3, y + a[1] + 3], fill=RED)
    elif kind == "fire":
        d.polygon([(x + 18, y + 4), (x + 28, y + 20), (x + 24, y + 30), (x + 12, y + 30), (x + 8, y + 20)], fill=(255, 120, 20), outline=RED)
    elif kind == "warn":
        d.polygon([(x + 18, y + 5), (x + 32, y + 30), (x + 4, y + 30)], fill=(255, 200, 40), outline=INK)
        d.text((x + 13, y + 16), "4t", font=F(SANS_B, 11), fill=INK)
    elif kind == "mic":
        d.rectangle([x + 14, y + 5, x + 22, y + 22], fill=INK)
        d.ellipse([x + 26, y + 12, x + 34, y + 20], outline=RED, width=2)
        d.ellipse([x + 23, y + 9, x + 37, y + 23], outline=RED, width=1)
    elif kind == "arena":
        d.arc([x + 5, y + 8, x + 31, y + 30], 180, 360, fill=INK, width=3)
        d.line([x + 8, y + 28, x + 28, y + 28], fill=INK, width=3)
        d.polygon([(x + 24, y + 18), (x + 32, y + 22), (x + 24, y + 26)], fill=RED)
    elif kind == "chart":
        d.line([x + 6, y + 8, x + 14, y + 16, x + 20, y + 12, x + 30, y + 26], fill=RED, width=3)
        d.polygon([(x + 30, y + 26), (x + 24, y + 25), (x + 29, y + 20)], fill=RED)
    elif kind == "fist":
        d.rectangle([x + 13, y + 10, x + 23, y + 28], fill=INK)
        d.rectangle([x + 11, y + 5, x + 25, y + 12], fill=INK)
    else:  # shake
        d.ellipse([x + 6, y + 14, x + 18, y + 24], fill=BLUE)
        d.ellipse([x + 18, y + 14, x + 30, y + 24], fill=RED)
        d.rectangle([x + 13, y + 8, x + 23, y + 14], fill=WHITE, outline=INK)

def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(205, 220, 230), outline=INK, width=1)
    land = (175, 195, 160)
    # simplified continents (relative polygons)
    polys = [
        [(0.03, 0.18), (0.22, 0.12), (0.28, 0.28), (0.20, 0.45), (0.10, 0.42), (0.04, 0.30)],  # N America
        [(0.20, 0.48), (0.28, 0.50), (0.30, 0.68), (0.24, 0.82), (0.19, 0.62)],  # S America
        [(0.44, 0.16), (0.56, 0.14), (0.58, 0.28), (0.50, 0.32), (0.44, 0.26)],  # Europe
        [(0.46, 0.34), (0.58, 0.32), (0.62, 0.52), (0.55, 0.72), (0.48, 0.58)],  # Africa
        [(0.58, 0.16), (0.82, 0.14), (0.88, 0.30), (0.78, 0.44), (0.62, 0.36), (0.58, 0.26)],  # Asia
        [(0.76, 0.52), (0.88, 0.50), (0.90, 0.64), (0.78, 0.66)],  # Oceania
    ]
    for poly in polys:
        pts = [(x + px * w, y + py * h) for px, py in poly]
        d.polygon(pts, fill=land, outline=(120, 140, 110))
    for num, lon, lat in PINS:
        px = x + (lon + 180) / 360 * w
        py = y + (90 - lat) / 180 * h
        d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=RED, outline=WHITE, width=1)
        s = str(num)
        tw = d.textlength(s, font=F(SANS_B, 11))
        d.text((px - tw / 2, py - 6), s, font=F(SANS_B, 11), fill=WHITE)

# ---- page assembly ----
def main():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    M = 12
    # Masthead
    d.text((M, 4), "THE WORLD IN ONE IMAGE", font=F(SANS_B, 17), fill=INK)
    r = "ALL TIMES UTC  -  ONE DAY ONLY"
    d.text((W - M - d.textlength(r, font=F(SANS_B, 17)), 4), r, font=F(SANS_B, 17), fill=INK)
    d.line([M, 26, W - M, 26], fill=INK, width=2)
    f_mon = F(SERIF_B, 44)
    d.text((M, 30), "MONDAY", font=f_mon, fill=RED)
    mw = d.textlength("MONDAY", font=f_mon)
    f_date = F(SERIF_B, 62)
    d.text((M + mw + 14, 18), "23 NOVEMBER 2026", font=f_date, fill=INK)
    d.line([M, 92, W - M, 92], fill=INK, width=2)
    # count strip
    d.rectangle([M, 96, W - M, 124], fill=DARK)
    cs = "38 STORIES  -  7 REGIONS  -  EVERY ONE FROM THIS MONDAY"
    cf = F(SANS_B, 19)
    d.text(((W - d.textlength(cs, font=cf)) / 2, 100), cs, font=cf, fill=WHITE)
    # Timeline
    ty = 128
    d.text((M, ty), "THE DAY IN UTC", font=F(SANS_B, 15), fill=RED)
    tf = F(SANS, 13); tfb = F(SANS_B, 13)
    for i, (t, ev) in enumerate(TIMELINE):
        col = i % 6; row = i // 6
        x = M + col * 167; y = ty + 18 + row * 16
        d.text((x, y), t, font=tfb, fill=INK)
        d.text((x + 38, y), ev[:20], font=tf, fill=INK)
    d.line([M, 176, W - M, 176], fill=INK, width=2)
    # Leads 2x2
    ly = 180; cell_w = (W - 2 * M - 8) // 2; cell_h = 135
    for idx, (label, head, summ, tag, kind) in enumerate(LEADS):
        cx = M + (idx % 2) * (cell_w + 8); cy = ly + (idx // 2) * (cell_h + 4)
        ART[kind](d, cx, cy, cell_w, 54)
        chip(d, cx + 6, cy + 6, label, F(SANS_B, 13))
        y2 = text_block(d, cx + 2, cy + 56, head, F(SERIF_B, 29), INK, cell_w - 4, 31, 1)
        y2 = text_block(d, cx + 2, y2, summ, F(SANS, 17), INK, cell_w - 4, 18, 2)
        d.text((cx + 2, y2 + 1), tag, font=F(SANS_B, 14), fill=RED)
        if idx % 2 == 0:
            d.line([cx + cell_w + 4, cy, cx + cell_w + 4, cy + cell_h], fill=GREY, width=1)
    ny = ly + 2 * cell_h + 8
    d.line([M, ny, W - M, ny], fill=INK, width=2)
    # Numbers strip
    d.rectangle([M, ny + 4, W - M, ny + 48], fill=(235, 225, 195))
    nw = (W - 2 * M) // 6
    for i, (num, cap) in enumerate(NUMBERS):
        x = M + i * nw + 6
        d.text((x, ny + 5), num, font=F(SERIF_B, 24), fill=RED)
        text_block(d, x, ny + 30, cap, F(SANS, 12), INK, nw - 10, 11, 1)
    ty2 = ny + 52
    d.line([M, ty2, W - M, ty2], fill=INK, width=2)
    # Tier-2 + map
    ty2 += 4
    map_w = 292; map_x = (W - map_w) // 2
    col_w = map_x - M - 8
    d.text((map_x, ty2), "WHERE IT HAPPENED", font=F(SANS_B, 16), fill=INK)
    draw_map(d, map_x, ty2 + 20, map_w, 150)
    d.text((map_x, ty2 + 174), "Pins 1-4 leads, 5-12 tier-2 stories.", font=F(SANS, 13), fill=GREY)
    for side, rows in enumerate([TIER_LEFT, TIER_RIGHT]):
        bx = M if side == 0 else W - M - col_w
        for j, (head, summ, tag, kind) in enumerate(rows):
            ry = ty2 + j * 56
            pictogram(d, bx, ry + 4, kind)
            text_block(d, bx + 42, ry, head, F(SANS_B, 24), INK, col_w - 44, 25, 1)
            text_block(d, bx + 42, ry + 25, summ, F(SANS, 17), INK, col_w - 44, 18, 1)
            d.text((bx + 42, ry + 43), tag, font=F(SANS_B, 11), fill=RED)
    by = ty2 + 282
    d.line([M, by, W - M, by], fill=INK, width=2)
    # Briefs
    d.text((M, by + 2), "BRIEFS - THE REST OF MONDAY IN SHORT", font=F(SANS_B, 16), fill=RED)
    bw = (W - 2 * M - 16) // 3
    bf = F(SANS, 22)
    for ci, (region, items) in enumerate(BRIEF_COLS):
        x = M + ci * (bw + 8); y = by + 20
        d.rectangle([x - 2, y - 2, x + bw, y + 20], fill=DARK)
        d.text((x, y), region, font=F(SANS_B, 18), fill=WHITE)
        y += 23
        for it in items:
            y = text_block(d, x, y, "- " + it, bf, INK, bw, 20, 1)
    # Footer
    fy = H - 44
    d.rectangle([0, fy, W, H], fill=DARK)
    legend = "HOW SURE: CONFIRMED = 2+ outlets  -  OFFICIAL = on record  -  REPORTED = 1 outlet / one side"
    d.text((M, fy + 3), legend, font=F(SANS_B, 14), fill=WHITE)
    dc = "DATE CHECK - LEFT OUT (OLDER): Hague verdict 19 Nov - Van Gogh sale 19 Nov - Cyrus wedding 22 Nov - NOT YET: Spain votes 29 Nov"
    d.text((M, fy + 22), dc, font=F(SANS_B, 13), fill=(255, 210, 120))
    out = os.path.join(BASE, "entry.png")
    img.save(out, optimize=True)
    print(out, os.path.getsize(out))

if __name__ == "__main__":
    main()
