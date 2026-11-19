#!/usr/bin/env python3
"""Build the V2 front page of THE WORLD TODAY for Wednesday 18 November 2026.

Composes a one-page newspaper from the illustration assets in assets/ and the
verified story list below, then writes entry.png (1024x1024, under 1 MiB).

Run:  python3 build_page.py
Needs Pillow (build-time only). The submitted program, main.py, is stdlib-only
and simply copies the finished entry.png to the output directory.
"""

import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
MARGIN = 18
CONTENT = W - 2 * MARGIN  # 988

PAPER = (247, 243, 233)
INK = (17, 17, 17)
RED = (172, 28, 28)
GREY = (96, 93, 86)
LIGHT = (236, 231, 219)
RULE = (52, 52, 52)
MAP_DOT = (64, 80, 96)
MAP_SEA = (233, 229, 216)

SERIF_PATHS = [
    "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
]
SERIF_REG_PATHS = [
    "/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
]
SANS_PATHS = [
    "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]
SANS_REG_PATHS = [
    "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]

_font_cache = {}


def font(paths, size):
    key = (paths[0], size)
    if key not in _font_cache:
        for p in paths:
            if os.path.exists(p):
                _font_cache[key] = ImageFont.truetype(p, size)
                break
        else:
            _font_cache[key] = ImageFont.load_default()
    return _font_cache[key]


def serif_b(size):
    return font(SERIF_PATHS, size)


def serif(size):
    return font(SERIF_REG_PATHS, size)


def sans_b(size):
    return font(SANS_PATHS, size)


def sans(size):
    return font(SANS_REG_PATHS, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns a list of lines fitting width."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, x, y, lines, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def draw_wrapped(draw, x, y, text, fnt, width, fill, leading):
    lines = wrap(draw, text, fnt, width)
    return draw_lines(draw, x, y, lines, fnt, fill, leading), lines


def cover(img, w, h, focus_y=0.5):
    """Centre-crop to the target aspect ratio, then resize.

    focus_y biases the vertical crop window: 0.0 keeps the top, 0.5 the
    middle, 1.0 the bottom. Useful when the key detail sits high in frame.
    """
    iw, ih = img.size
    target = w / h
    src = iw / ih
    if src > target:  # too wide: trim sides
        nw = int(ih * target)
        x0 = (iw - nw) // 2
        img = img.crop((x0, 0, x0 + nw, ih))
    else:  # too tall: trim top/bottom around the focus point
        nh = int(iw / target)
        y0 = int((ih - nh) * focus_y)
        img = img.crop((0, y0, iw, y0 + nh))
    return img.resize((w, h), Image.LANCZOS)


def photo(page, name, box, focus_y=0.5):
    """Paste an asset image into box (x, y, w, h) with a thin ink border."""
    x, y, w, h = box
    img = Image.open(os.path.join(ASSETS, name)).convert("RGB")
    page.paste(cover(img, w, h, focus_y), (x, y))
    d = ImageDraw.Draw(page)
    d.rectangle([x, y, x + w - 1, y + h - 1], outline=INK, width=1)


# ---------------------------------------------------------------- stories

HERO1 = {
    "kicker": "WAR IN THE GULF",
    "headline": "GULF WAR WIDENS AS IRAN HITS U.S. BASES",
    "deck": "Tehran strikes Kuwait and Bahrain after U.S. jets hit a missile "
            "site on Qeshm Island; five tankers sunk and oil tops $100.",
    "bullets": [
        "U.S. forces sink five Iranian tankers in the Gulf of Oman; "
        "crews told to abandon ship.",
        "Iran fires missiles at Al-Azraq base in Jordan; 18 of 20 "
        "intercepted, no casualties.",
        "Iran says it seized the tanker Ocean Koi; one ADNOC crew missing.",
    ],
    "image": "hero-gulf-v2.webp",
    "caption": "Crew abandon a burning tanker in the Gulf of Oman. Illustration.",
}

HERO2 = {
    "kicker": "APEC  •  SHENZHEN",
    "headline": "XI HOSTS PUTIN AS TRUMP LANDS FOR THREE-WAY TALKS",
    "body": "Xi Jinping and Vladimir Putin met in Shenzhen, a day before a "
            "trilateral summit with Donald Trump. Xi pledged to stand against "
            "protectionism; Putin attacked Western sanctions.",
    "image": "hero-apec-v2.webp",
}

HERO3 = {
    "kicker": "CYCLONE XAVIER  •  COOK ISLANDS",
    "headline": "CATEGORY 5 XAVIER BATTERS THE NORTHERN COOKS",
    "body": "Sustained winds of 220 km/h and gusts to 315 km/h lashed the "
            "northern Cook Islands as Xavier passed 280 km north-east of "
            "Pukapuka. Manihiki's wharves were damaged; no casualties reported.",
    "image": "hero-xavier-v2.webp",
}

CARDS = [
    {
        "kicker": "U.S. MIDTERMS",
        "headline": "Peltola wins Alaska; Democrats take Senate 56–44",
        "body": "Mary Peltola beat Dan Sullivan 50.1% to 45.8%, the first "
                "Alaska Native in the Senate.",
        "image": "card-peltola-v2.webp",
    },
    {
        "kicker": "IPO",
        "headline": "Anthropic prices at $83 in $81.3bn listing",
        "body": "Shares priced above the $70–$78 range; trading starts "
                "Thursday on Nasdaq as ANT.",
        "image": "card-anthropic-v2.webp",
    },
    {
        "kicker": "DROUGHT",
        "headline": "Fiji declares national disaster over drought",
        "body": "A 30-day state of disaster and FJ$20m in aid as El Niño "
                "parches the islands.",
        "image": "card-fiji-v2.webp",
    },
    {
        "kicker": "CONGO",
        "headline": "Ebola outbreak passes 11,000 cases",
        "body": "Cases more than doubled in three months in the second-largest "
                "outbreak on record.",
        "image": "card-ebola-v2.webp",
    },
    {
        "kicker": "GAZA",
        "headline": "Truce 'near collapse' as floods swamp camps",
        "body": "Trump's Board of Peace faults Israel and Hamas; WHO says "
                "950,000 are on flood-prone ground.",
        "image": "card-gaza-v2.webp",
    },
]

STATS = [
    ("$115.8bn", "NVIDIA'S QUARTER",
     "Revenue doubled as data-centre sales hit $107.6bn; Q4 guidance $130bn."),
    ("1 light-day", "VOYAGER 1",
     "First human-made object to reach one light-day out, 16.1bn miles away."),
    ("5,412", "MEASLES CASES",
     "The U.S. loses measles-free status after 26 years; 10 deaths in 2026."),
    ("€45bn", "EU LOAN FOR UKRAINE",
     "€20bn budget aid plus €25bn military, repaid only after reparations."),
]

# Dotted world map: 40 rows (lat 75 down to -55), 96 columns (lon -180 to 180).
# Each row lists inclusive column ranges that are land.
MAP_ROWS = [
    [(5, 15), (34, 40), (60, 95)],
    [(3, 9), (10, 30), (33, 41), (58, 95)],
    [(3, 10), (11, 31), (33, 40), (57, 95)],
    [(4, 10), (11, 32), (34, 38), (50, 54), (55, 95)],
    [(5, 10), (11, 32), (35, 37), (48, 55), (56, 95)],
    [(12, 32), (48, 55), (56, 94)],
    [(13, 31), (46, 47), (49, 54), (55, 93)],
    [(13, 30), (45, 58), (59, 75), (76, 85)],
    [(13, 30), (45, 58), (59, 74), (75, 86)],
    [(14, 30), (45, 57), (58, 72), (73, 84), (84, 86)],
    [(14, 30), (46, 57), (58, 64), (65, 74), (75, 84), (83, 86)],
    [(14, 30), (45, 56), (57, 64), (65, 72), (73, 83), (83, 85)],
    [(15, 29), (44, 57), (58, 64), (66, 72), (73, 82)],
    [(16, 25), (43, 58), (59, 64), (66, 73), (74, 82)],
    [(17, 25), (43, 58), (59, 63), (67, 73), (74, 80)],
    [(18, 25), (43, 59), (59, 62), (68, 72), (74, 79)],
    [(19, 26), (43, 59), (60, 62), (69, 71), (74, 78)],
    [(23, 27), (27, 32), (43, 56), (74, 77)],
    [(24, 27), (27, 35), (44, 57), (74, 76)],
    [(27, 36), (44, 58), (73, 76)],
    [(27, 37), (44, 59), (73, 77)],
    [(27, 37), (45, 59), (74, 79), (82, 86)],
    [(27, 37), (45, 59), (74, 78), (82, 86)],
    [(27, 37), (45, 59), (83, 86)],
    [(28, 37), (46, 59), (75, 80)],
    [(28, 37), (46, 58), (76, 81)],
    [(28, 37), (46, 58), (79, 86)],
    [(28, 36), (47, 58), (78, 87)],
    [(29, 36), (47, 57), (60, 61), (78, 88)],
    [(29, 36), (47, 56), (60, 61), (78, 88)],
    [(30, 36), (48, 56), (79, 88)],
    [(30, 35), (49, 55), (79, 87)],
    [(30, 35), (50, 54), (80, 86), (92, 93)],
    [(31, 35), (81, 85), (92, 94)],
    [(31, 34), (92, 93)],
    [(31, 34)],
    [(32, 34)],
    [(32, 33)],
    [(32, 33)],
    [],
]

# (number, lon, lat, legend label) — keep markers well spaced on the map.
MARKERS = [
    (1, 57, 25, "Gulf of Oman — U.S. sinks 5 tankers"),
    (2, 49, 28, "Kuwait, Bahrain & Jordan — Iran hits U.S. bases"),
    (3, 114, 22, "Shenzhen — Xi hosts Putin at APEC"),
    (4, -166, -11, "Pukapuka — Xavier gusts 315 km/h"),
    (5, 178, -18, "Suva — Fiji declares disaster"),
    (6, -150, 64, "Alaska — Peltola wins Senate seat"),
    (7, 4, 51, "Brussels — €45bn Ukraine loan"),
    (8, 30, 50, "Kyiv — 12 jets pledged at Ramstein"),
    (9, 127, 37, "Seoul — Growth forecast raised"),
    (10, -48, -16, "Brasília — Senate approves fiscal package"),
    (11, 29, 0, "Beni — Ebola passes 11,000 cases"),
    (12, -74, 41, "New York — Anthropic prices $83 IPO"),
]

ALSO = [
    "Kerch Bridge hit a third time",
    "Zverev beats Shelton, reaches semis",
    "'Human' is Cambridge Word of Year",
    "Google unveils Gemini 4 Neon",
    "Microsoft launches 7 models",
    "Trump announces Philippines pact",
    "Romania hit by M5.3 quake",
    "Lee meets Xi on peninsula peace",
    "Kahana elected Knesset speaker",
    "Myanmar to review ASEAN ties",
    "U.S. officer held in spy probe",
    "Critical Java flaw found by AI",
    "Saudi Arabia stops Houthi missile",
    "Australia sanctions settlers",
    "Russian drones strike Kyiv",
    "Thousands protest Fico in Slovakia",
    "Italy approves antisemitism law",
    "Nigeria approves state police law",
    "Two Ebola vaccines enter trials",
    "Sudan army gains in W. Kordofan",
    "Oil tops $100; stocks slide",
    "Waymo halts driverless taxis",
    "EU acts against Temu",
    "NATO unveils comms strategy",
]

SOURCES = ("Sources: AP, Reuters, AFP, BBC, Al Jazeera, UN News, RNZ, USGS, "
           "Yonhap, NASA/JPL, Fiji Met Service, JTWC. Illustrations are "
           "artist's impressions of the day's events.")


# Short legend labels for the map (kept to one line each).
LEGEND = [
    (1, "Gulf of Oman — 5 tankers sunk"),
    (2, "Kuwait, Bahrain, Jordan hit"),
    (3, "Shenzhen — Xi hosts Putin"),
    (4, "Pukapuka — gusts 315 km/h"),
    (5, "Suva — Fiji declares disaster"),
    (6, "Alaska — Peltola wins seat"),
    (7, "Brussels — €45bn loan"),
    (8, "Kyiv — 12 jets pledged"),
    (9, "Seoul — growth forecast up"),
    (10, "Brasília — fiscal package"),
    (11, "Beni — Ebola over 11,000"),
    (12, "New York — Anthropic IPO"),
]


def hrule(draw, y, weight=1, color=RULE):
    draw.line([(MARGIN, y), (W - MARGIN, y)], fill=color, width=weight)


def masthead(page, draw):
    title = "THE WORLD TODAY"
    fnt = serif_b(54)
    tw = draw.textlength(title, font=fnt)
    draw.text(((W - tw) / 2, 2), title, font=fnt, fill=INK)
    # date bar
    y = 62
    draw.text((MARGIN, y), "WEDNESDAY, 18 NOVEMBER 2026", font=sans_b(15), fill=INK)
    right = "38 STORIES  •  SIX CONTINENTS  •  ONE PAGE"
    rw = draw.textlength(right, font=sans_b(13))
    draw.text((W - MARGIN - rw, y + 1), right, font=sans_b(13), fill=GREY)
    hrule(draw, 82, weight=3)
    hrule(draw, 86, weight=1)


def hero1(page, draw):
    x0, y0 = MARGIN, 92
    img_w, img_h = 494, 176
    photo(page, HERO1["image"], (x0, y0, img_w, img_h))
    draw.text((x0, y0 + img_h + 4), HERO1["caption"], font=sans(10), fill=GREY)

    tx, tw = 524, W - MARGIN - 524
    y = y0 - 2
    draw.text((tx, y), HERO1["kicker"], font=sans_b(13), fill=RED)
    y += 18
    y, _ = draw_wrapped(draw, tx, y, HERO1["headline"], serif_b(29), tw, INK, 33)
    y += 4
    y, _ = draw_wrapped(draw, tx, y, HERO1["deck"], serif(15), tw, INK, 18)
    y += 6
    for bullet in HERO1["bullets"]:
        draw.text((tx, y), "•", font=sans_b(12), fill=RED)
        y, _ = draw_wrapped(draw, tx + 13, y, bullet, sans(12), tw - 13, INK, 14)
        y += 3


def hero_half(page, draw, hero, x0, y0, w, focus_y=0.5):
    photo(page, hero["image"], (x0, y0, w, 100), focus_y)
    y = y0 + 106
    draw.text((x0, y), hero["kicker"], font=sans_b(11), fill=RED)
    y += 15
    y, _ = draw_wrapped(draw, x0, y, hero["headline"], serif_b(19), w, INK, 22)
    y += 3
    draw_wrapped(draw, x0, y, hero["body"], sans(11), w, INK, 13)


def heroes_row(page, draw):
    y0 = 294
    half = (CONTENT - 12) // 2  # 488
    # APEC: keep the banner and faces in frame (top of the source image).
    hero_half(page, draw, HERO2, MARGIN, y0, half, focus_y=0.15)
    hero_half(page, draw, HERO3, MARGIN + half + 12, y0, half)


def cards_row(page, draw):
    y0 = 510
    cw = (CONTENT - 4 * 9) // 5  # 190
    for i, card in enumerate(CARDS):
        x = MARGIN + i * (cw + 9)
        photo(page, card["image"], (x, y0, cw, 94))
        y = y0 + 99
        draw.text((x, y), card["kicker"], font=sans_b(10), fill=RED)
        y += 13
        y, _ = draw_wrapped(draw, x, y, card["headline"], sans_b(12), cw, INK, 14)
        y += 2
        draw_wrapped(draw, x, y, card["body"], sans(10), cw, INK, 12)


def stats_row(page, draw):
    y0 = 692
    cw = (CONTENT - 3 * 9) // 4  # 240
    for i, (big, label, text) in enumerate(STATS):
        x = MARGIN + i * (cw + 9)
        draw.rectangle([x, y0, x + cw, y0 + 64], fill=LIGHT)
        draw.rectangle([x, y0, x + cw, y0 + 2], fill=RED)
        draw.text((x + 8, y0 + 5), big, font=serif_b(23), fill=INK)
        draw.text((x + 8, y0 + 30), label, font=sans_b(10), fill=RED)
        draw_wrapped(draw, x + 8, y0 + 42, text, sans(10), cw - 16, INK, 10)


def world_map(page, draw):
    y0 = 760
    draw.text((MARGIN, y0), "WHERE IT HAPPENED — 18 NOVEMBER 2026",
              font=sans_b(13), fill=INK)
    mx, my, mw, mh = MARGIN, y0 + 18, 582, 104
    draw.rectangle([mx, my, mx + mw, my + mh], fill=MAP_SEA, outline=RULE)
    # dotted continents
    step_x = mw / 96.0
    step_y = mh / 40.0
    for r, spans in enumerate(MAP_ROWS):
        cy = my + (r + 0.5) * step_y
        for lo, hi in spans:
            for c in range(lo, hi + 1):
                cx = mx + (c + 0.5) * step_x
                draw.ellipse([cx - 1.2, cy - 1.2, cx + 1.2, cy + 1.2],
                             fill=MAP_DOT)
    # numbered markers
    for num, lon, lat, _label in MARKERS:
        px = mx + (lon + 180) / 360.0 * mw
        py = my + (75 - lat) / 130.0 * mh
        px = min(max(px, mx + 8), mx + mw - 8)
        py = min(max(py, my + 8), my + mh - 8)
        draw.ellipse([px - 6, py - 6, px + 6, py + 6], fill=RED, outline=PAPER)
        t = str(num)
        fnt = sans_b(8 if num < 10 else 7)
        tw = draw.textlength(t, font=fnt)
        draw.text((px - tw / 2, py - 5), t, font=fnt, fill=(255, 255, 255))
    # legend: two columns of six, right of the map
    lx = mx + mw + 14
    col_w = (W - MARGIN - lx - 10) // 2
    for i, (num, label) in enumerate(LEGEND):
        col, row = divmod(i, 6)
        x = lx + col * (col_w + 10)
        y = my + 2 + row * 17
        draw.ellipse([x, y, x + 11, y + 11], fill=RED)
        t = str(num)
        fnt = sans_b(8 if num < 10 else 7)
        tw = draw.textlength(t, font=fnt)
        draw.text((x + (11 - tw) / 2, y + 1), t, font=fnt, fill=(255, 255, 255))
        draw.text((x + 15, y), label, font=sans(11), fill=INK)


def also_list(page, draw):
    y0 = 892
    draw.text((MARGIN, y0), "ALSO ON WEDNESDAY 18 NOVEMBER",
              font=sans_b(13), fill=INK)
    hrule(draw, y0 + 17, weight=1)
    col_w = (CONTENT - 3 * 9) // 4  # 240
    for col in range(4):
        x = MARGIN + col * (col_w + 9)
        if col:
            draw.line([(x - 5, y0 + 22), (x - 5, y0 + 128)], fill=LIGHT, width=1)
        y = y0 + 23
        for item in ALSO[col * 6:(col + 1) * 6]:
            draw.text((x, y), "•", font=sans_b(11), fill=RED)
            y, _ = draw_wrapped(draw, x + 11, y, item, sans(11), col_w - 11,
                                INK, 12)
            y += 2


def footer(draw):
    y = 1004
    draw_wrapped(draw, MARGIN, y, SOURCES, sans(9), CONTENT, GREY, 10)


def build():
    page = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(page)
    masthead(page, draw)
    hero1(page, draw)
    hrule(draw, 288, weight=1)
    heroes_row(page, draw)
    hrule(draw, 504, weight=1)
    cards_row(page, draw)
    stats_row(page, draw)
    hrule(draw, 756, weight=1)
    world_map(page, draw)
    hrule(draw, 888, weight=1)
    also_list(page, draw)
    footer(draw)
    page.save(OUT, "PNG", optimize=True)
    size = os.path.getsize(OUT)
    print(f"wrote {OUT}  {W}x{H}  {size} bytes")
    if size > 1048576:
        print("WARNING: over the 1 MiB limit")


if __name__ == "__main__":
    build()
