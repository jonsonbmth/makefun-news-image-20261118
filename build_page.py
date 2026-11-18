#!/usr/bin/env python3
"""Compose the 18 November 2026 front page (1024x1024) from generated photos.

Run:  python3 build_page.py
Writes entry.png next to this file. Deterministic: same inputs -> same bytes
(PIL PNG output carries no timestamps; all layout is fixed arithmetic).

Design: a broadsheet front page on cream paper. Masthead, black date bar,
one wide hero (Gulf), two half-width heroes (APEC, Xavier), two rows of four
story cards, a dotted world map with 12 numbered markers, a 24-item
"also" list and a sources footer. 36 distinct verified stories in total.

Vertical budget (1024 px):
  top bar 0-18 | masthead 19-76 | date bar 80-102 | hero 1 106-280 |
  heroes 2-3 290-470 | cards 480-616, 620-756 | map 768-884 |
  also 890-1004 | footer 1008-1022
"""

import os
from PIL import Image, ImageDraw, ImageFont, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")

W, H = 1024, 1024
MARGIN = 16
CONTENT_W = W - 2 * MARGIN

PAPER = (247, 242, 231)
INK = (22, 22, 22)
RED = (172, 32, 32)
MUTED = (96, 90, 78)
RULE = (186, 178, 156)
MAP_DOT = (172, 154, 120)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-%s.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-%s.ttf"
DEJAVU_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


F = {
    "masthead": font(SERIF % "Bold", 52),
    "date": font(SANS % "Bold", 15),
    "dateline": font(SANS % "Bold", 9),
    "topbar": font(SANS % "Bold", 10),
    "kicker": font(SANS % "Bold", 11),
    "kicker_sm": font(SANS % "Bold", 9),
    "hero1_head": font(SERIF % "Bold", 32),
    "hero1_body": font(SERIF % "Regular", 14),
    "hero_head": font(SERIF % "Bold", 20),
    "hero_body": font(SERIF % "Regular", 13),
    "card_head": font(SERIF % "Bold", 14),
    "card_body": font(SERIF % "Regular", 11),
    "stat": font(SERIF % "Bold", 30),
    "section": font(SANS % "Bold", 13),
    "map_item": font(SANS % "Regular", 11),
    "map_num": font(DEJAVU_BOLD, 7),
    "also": font(SANS % "Regular", 10),
    "caption": font(SERIF % "Italic", 10),
    "footer": font(SANS % "Regular", 9),
}


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines fitting max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_w:
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


def draw_limited(draw, x, y, text, fnt, fill, max_w, max_lines, leading):
    """Draw text wrapped to at most max_lines; ellipsis if truncated."""
    lines = wrap(draw, text, fnt, max_w)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        while lines and draw.textlength(lines[-1] + " ...", font=fnt) > max_w:
            lines[-1] = lines[-1][:-1]
        lines[-1] += " ..."
    return draw_lines(draw, x, y, lines, fnt, fill, leading)


def photo(name, w, h, cy=0.5):
    """Center-crop an asset photo to exactly w x h.

    cy shifts the crop window vertically (0.5 = centre, higher = lower
    in the frame) so a wide strip can keep the people in shot.
    """
    im = Image.open(os.path.join(ASSETS, name)).convert("RGB")
    return ImageOps.fit(im, (w, h), Image.LANCZOS, centering=(0.5, cy))


def rule(draw, y, x0=MARGIN, x1=W - MARGIN, width=1, fill=RULE):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


# ---------------------------------------------------------------- world map
# Rough continent outlines in (lon, lat). Rendered as a dot grid clipped to
# the land polygons, so the map reads as a classic dotted newspaper map.
CONTINENTS = [
    # North America
    [(-168, 65), (-150, 70), (-130, 70), (-115, 68), (-100, 69), (-90, 69),
     (-82, 66), (-78, 71), (-68, 58), (-60, 52), (-64, 45), (-70, 41),
     (-74, 40), (-76, 35), (-81, 31), (-80, 26), (-84, 30), (-89, 30),
     (-91, 29), (-97, 26), (-97, 16), (-94, 17), (-90, 14), (-86, 12),
     (-83, 9), (-79, 9), (-83, 10), (-87, 13), (-90, 15), (-97, 16),
     (-105, 20), (-109, 23), (-114, 28), (-117, 33), (-122, 37), (-124, 40),
     (-124, 48), (-128, 50), (-135, 58), (-145, 60), (-158, 58), (-162, 58)],
    # Greenland
    [(-45, 60), (-40, 65), (-30, 68), (-22, 70), (-30, 76), (-45, 76),
     (-58, 74), (-55, 70), (-52, 64)],
    # South America
    [(-79, 9), (-77, 4), (-80, -3), (-81, -6), (-77, -12), (-75, -15),
     (-70, -18), (-70, -23), (-70, -30), (-71, -35), (-73, -40), (-73, -45),
     (-70, -50), (-68, -54), (-65, -55), (-68, -50), (-65, -45), (-62, -40),
     (-58, -35), (-52, -32), (-48, -28), (-41, -23), (-39, -17), (-35, -9),
     (-35, -6), (-41, -3), (-44, -2), (-50, 0), (-52, 4), (-58, 6),
     (-62, 9), (-68, 11), (-72, 12), (-76, 10)],
    # Europe
    [(-10, 36), (-9, 43), (-2, 48), (-4, 49), (0, 51), (3, 53), (8, 57),
     (10, 59), (5, 60), (5, 62), (12, 64), (18, 69), (25, 71), (30, 70),
     (28, 66), (24, 64), (21, 60), (18, 56), (21, 55), (24, 58), (28, 60),
     (30, 62), (32, 66), (40, 68), (45, 66), (40, 62), (35, 60), (32, 58),
     (30, 55), (28, 52), (30, 50), (28, 46), (24, 44), (23, 40), (20, 40),
     (18, 42), (16, 44), (12, 44), (10, 44), (8, 44), (7, 44), (3, 43),
     (0, 38), (-2, 37), (-6, 36), (-9, 37)],
    # Africa
    [(-6, 35), (-10, 31), (-17, 21), (-17, 15), (-13, 8), (-8, 5), (6, 4),
     (9, 4), (9, -1), (13, -12), (12, -18), (17, -29), (19, -34), (25, -34),
     (32, -29), (35, -24), (40, -15), (40, -10), (42, -2), (46, 5), (51, 11),
     (48, 11), (44, 8), (43, 12), (40, 15), (39, 20), (38, 22), (37, 25),
     (35, 28), (33, 31), (30, 31), (25, 32), (20, 32), (15, 32), (11, 34),
     (10, 37), (5, 37), (0, 36)],
    # Asia (incl. Middle East, India, SE Asia)
    [(30, 70), (35, 68), (40, 68), (45, 66), (50, 69), (60, 69), (70, 72),
     (80, 73), (90, 75), (100, 77), (110, 74), (120, 73), (130, 72),
     (140, 72), (150, 70), (160, 69), (170, 67), (178, 65), (178, 62),
     (170, 60), (162, 58), (158, 52), (150, 45), (142, 42), (140, 38),
     (135, 35), (130, 33), (127, 35), (122, 38), (120, 32), (122, 28),
     (118, 25), (112, 22), (108, 18), (105, 10), (104, 8), (100, 7),
     (98, 10), (95, 16), (92, 21), (88, 22), (85, 19), (82, 16), (80, 13),
     (77, 8), (75, 11), (73, 16), (70, 21), (67, 24), (66, 25), (61, 25),
     (57, 26), (54, 26), (51, 28), (50, 29), (48, 30), (44, 29), (43, 27),
     (40, 28), (39, 25), (42, 20), (43, 15), (45, 12), (43, 12), (40, 15),
     (39, 21), (38, 25), (36, 30), (36, 36), (33, 36), (30, 36), (28, 40),
     (30, 45), (32, 50), (30, 55), (30, 60), (28, 64)],
    # Indonesia
    [(95, 5), (105, 0), (110, -5), (115, -8), (120, -10), (125, -9),
     (130, -4), (135, -3), (140, -8), (141, -2), (135, 0), (130, 2),
     (125, 1), (120, 0), (115, 3), (110, 5), (105, 6), (100, 6)],
    # Japan
    [(130, 31), (133, 34), (137, 35), (140, 36), (141, 39), (142, 44),
     (145, 44), (143, 40), (140, 35), (136, 33), (132, 31)],
    # United Kingdom
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (1, 53), (1, 51),
     (-2, 50)],
    # New Zealand
    [(167, -45), (172, -41), (175, -38), (178, -38), (174, -41), (170, -44)],
    # Australia
    [(114, -22), (114, -28), (115, -33), (118, -35), (124, -33), (129, -32),
     (132, -32), (135, -35), (138, -35), (140, -38), (145, -38), (150, -37),
     (153, -32), (153, -27), (151, -24), (146, -19), (142, -15), (142, -11),
     (140, -17), (136, -12), (132, -12), (130, -13), (126, -14), (122, -17),
     (118, -20)],
    # Madagascar
    [(44, -12), (47, -15), (50, -17), (49, -20), (47, -24), (45, -25),
     (44, -20), (43, -16)],
]

# (lon, lat, number, dx, dy) — dx/dy nudge crowded markers; a leader line
# connects the true point to the nudged dot.
MARKERS = [
    (59, 24, 1, 8, 5),       # Gulf of Oman
    (48, 29, 2, -8, -6),     # Kuwait
    (36, 31, 3, -12, 4),     # Jordan
    (114, 22, 4, 0, 0),      # Shenzhen
    (-166, -11, 5, 0, 0),    # Pukapuka
    (178, -18, 6, -4, 0),    # Suva, Fiji
    (-150, 64, 7, 0, 0),     # Alaska
    (4, 51, 8, 0, 0),        # Brussels
    (34, 31, 9, 4, 10),      # Gaza
    (26, 46, 10, 12, -9),    # Romania
    (127, 37, 11, 0, 0),     # Seoul
    (4, 52, 12, -11, -8),    # The Hague
]

MAP_PLACES = [
    "1. Gulf of Oman — U.S. sinks 5 tankers",
    "2. Kuwait — air defences down drones",
    "3. Jordan — missiles at Al-Azraq base",
    "4. Shenzhen — APEC summit opens",
    "5. Pukapuka — Xavier, gusts 315 km/h",
    "6. Suva — Fiji declares disaster",
    "7. Alaska — Peltola wins Senate seat",
    "8. Brussels — €45bn Ukraine loan",
    "9. Gaza — truce warning to the UN",
    "10. Romania — M5.3 quake",
    "11. Seoul — growth forecast raised",
    "12. The Hague — ICJ ruling Thursday",
]


def draw_map(draw, box):
    """Dotted world map in box (x0, y0, x1, y1); lon -180..180, lat 75..-60."""
    x0, y0, x1, y1 = box
    mw, mh = x1 - x0, y1 - y0

    def project(lon, lat):
        return (x0 + (lon + 180) / 360.0 * mw,
                y0 + (75 - lat) / 135.0 * mh)

    mask = Image.new("L", (mw, mh), 0)
    md = ImageDraw.Draw(mask)
    for poly in CONTINENTS:
        pts = [project(lon, lat) for lon, lat in poly]
        pts = [(px - x0, py - y0) for px, py in pts]
        md.polygon(pts, fill=255)
    pixels = mask.load()
    step = 4
    for gy in range(0, mh, step):
        for gx in range(0, mw, step):
            if pixels[gx, gy]:
                draw.ellipse([x0 + gx - 1, y0 + gy - 1,
                              x0 + gx + 1, y0 + gy + 1], fill=MAP_DOT)
    draw.rectangle([x0, y0, x1, y1], outline=RULE, width=1)
    for lon, lat, num, dx, dy in MARKERS:
        px, py = project(lon, lat)
        cx, cy = px + dx, py + dy
        if dx or dy:
            draw.line([(px, py), (cx, cy)], fill=RED, width=1)
        r = 5 if num >= 10 else 4.5
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED,
                     outline=(255, 255, 255), width=1)
        label = str(num)
        tw = draw.textlength(label, font=F["map_num"])
        draw.text((cx - tw / 2, cy - 3.5), label, font=F["map_num"],
                  fill=(255, 255, 255))


# ------------------------------------------------------------------- content
HERO1 = {
    "img": "hero-gulf.webp",
    "kicker": "THE GULF WAR WIDENS  ·  OVERNIGHT",
    "headline": "U.S. SINKS FIVE IRANIAN TANKERS",
    "body": ("American forces destroyed five Iranian oil tankers overnight in "
             "the Gulf of Oman and off Kharg Island, U.S. Central Command "
             "said, after Iran's Revolutionary Guard twice fired ballistic "
             "missiles at a U.S. warship. Iran said it struck 10 ships near "
             "the Strait of Hormuz and fired missiles at U.S. forces in "
             "Jordan."),
    "caption": "A tanker burns in the Gulf of Oman at dawn — eight tankers hit in four days. Illustration.",
}

HEROES = [
    {
        "img": "hero-apec.webp",
        "kicker": "APEC  ·  SHENZHEN",
        "headline": "XI OPENS APEC AS TRUMP AND PUTIN ARRIVE",
        "body": ("China's Xi Jinping opened the APEC summit in Shenzhen, "
                 "urging “free and open trade”. Putin landed overnight; "
                 "Trump arrives from Manila later today. The three meet "
                 "Thursday — a first."),
    },
    {
        "img": "hero-xavier.webp",
        "kicker": "SEVERE TROPICAL CYCLONE XAVIER",
        "headline": "XAVIER BATTERS THE NORTHERN COOKS",
        "body": ("Category 5 Cyclone Xavier, gusts to 315 km/h, bore down "
                 "on Pukapuka and Nassau as shelters opened across the "
                 "Northern Cook Islands. The storm sat about 250 km "
                 "north-east of Pukapuka."),
    },
]

CARDS_ROW1 = [
    {"img": "card-peltola.webp", "kicker": "U.S. SENATE  ·  ALASKA",
     "headline": "PELTOLA WINS ALASKA",
     "body": ("Democrat Mary Peltola beat Dan Sullivan 50.1% to 45.8%, AP "
              "called — the first Alaska Native in the Senate. Democrats "
              "now hold 56–44.")},
    {"img": "card-eu.webp", "kicker": "BRUSSELS",
     "headline": "EU PROPOSES €45BN MORE FOR UKRAINE",
     "body": ("The Commission presents a €45bn loan plan for 2027 today, "
              "covering two-thirds of Kyiv's shortfall. Kyiv repays only "
              "on reparations.")},
    {"img": "card-fiji.webp", "kicker": "EL NIÑO DROUGHT",
     "headline": "FIJI DECLARES NATIONAL DISASTER",
     "body": ("PM Rabuka declared a 30-day state of disaster over the "
              "drought and redeployed $20m for emergency water. 19 of 44 "
              "sources are critical.")},
    {"img": "card-anthropic.webp", "kicker": "MARKETS  ·  IPO",
     "headline": "ANTHROPIC PRICES $64BN IPO TODAY",
     "body": ("The AI lab sets its final IPO price today ahead of "
              "Thursday's Nasdaq debut as ANT. The float could value it "
              "at up to $1.4tn.")},
]

CARDS_ROW2 = [
    {"img": "card-gaza.webp", "kicker": "GAZA  ·  UNITED NATIONS",
     "headline": "GAZA TRUCE “NEAR COLLAPSE”, WARNS BOARD",
     "body": ("The U.S.-backed Board of Peace told the UN the year-old "
              "ceasefire faces imminent collapse. 1,650 have died in Gaza "
              "since it began.")},
    {"stat": "M5.3", "kicker": "EARTHQUAKE  ·  00:48 UTC",
     "headline": "QUAKE SHAKES ROMANIA",
     "body": ("A magnitude 5.3 quake struck 16 km west of Nereju Mic, "
              "131 km deep. It was felt widely; no damage was reported.")},
    {"stat": "$100+", "kicker": "MARKETS",
     "headline": "OIL TOPS $100 ON GULF FIGHTING",
     "body": ("Brent crude pushed above $100 a barrel in early Wednesday "
              "trading as the U.S.–Iran confrontation escalated. Euro "
              "stocks fell 2.2%.")},
    {"stat": "3.9%", "kicker": "ECONOMY  ·  SEOUL",
     "headline": "KOREA LIFTS 2027 GROWTH FORECAST",
     "body": ("State think tank KDI raised its 2027 growth outlook to 3.9% "
              "from 2.2%, powered by the AI chip boom. Two-thirds of "
              "growth is chips.")},
]

ALSO = [
    "World Court rules Thursday on Myanmar genocide",
    "Zverev beats Shelton to reach ATP Finals semis",
    "Eritrean forces retake Badme; Tigray curfew",
    "Brazil Senate votes on Lula fiscal package",
    "M1.1 solar flare recorded at 02:57 UTC",
    "COP31 draft lists 144 disputed items",
    "DHS chief Mullin faces House threats hearing",
    "Bezos says he helped pick Pattinson as Bond",
    "India re-elected to ITU Council for 2027–30",
    "Pakistan cuts petrol Rs3 to Rs325 a litre",
    "Cyclone Akvan strengthens; Andhra on alert",
    "U.S. soldier held in UK over spy suspicion",
    "Pakistani man jailed 27 years over Iran plot",
    "Five EU states plan return hubs in Rwanda",
    "Serbia parliament opens; students in majority",
    "Turkey takes over opposition TV channel Sozcu",
    "Apple to stand trial in France over iPhones",
    "EU raises eurozone growth forecast to 1.2%",
    "France, Malaysia agree rare-earths partnership",
    "U.S. boosts funding for Pacific island states",
    "Rooftop solar lifts Pakistan solar to 28%",
    "Cambridge names “human” word of the year",
    "Tiger Woods to return to golf in December",
    "WHO warns of growing antimicrobial resistance",
]

FOOTER = ("Sources: AP, Reuters, AFP, BBC, Al Jazeera, UN News, RNZ, USGS, Yonhap, CNBC, PINA. "
          "All stories verified against reporting of Wednesday 18 November 2026; "
          "illustrations rendered for this edition.")


# --------------------------------------------------------------------- build
def build():
    page = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(page)

    # --- top bar ------------------------------------------------------
    draw.text((MARGIN, 4), "WORLD EDITION", font=F["topbar"], fill=INK)
    right = "ONE DAY · ONE PAGE · THE WHOLE WORLD"
    draw.text((W - MARGIN - draw.textlength(right, font=F["topbar"]), 4),
              right, font=F["topbar"], fill=INK)
    rule(draw, 18, width=1)

    # --- masthead -----------------------------------------------------
    title = "THE WORLD TODAY"
    tw = draw.textlength(title, font=F["masthead"])
    draw.text(((W - tw) / 2, 19), title, font=F["masthead"], fill=INK)
    rule(draw, 76, width=2, fill=INK)

    # --- date bar -----------------------------------------------------
    draw.rectangle([MARGIN, 80, W - MARGIN, 102], fill=INK)
    date = "WEDNESDAY, 18 NOVEMBER 2026"
    tw = draw.textlength(date, font=F["date"])
    draw.text(((W - tw) / 2, 84), date, font=F["date"], fill=(255, 255, 255))
    draw.text((MARGIN + 8, 86), "VOL. I · No. 322", font=F["dateline"],
              fill=(220, 215, 200))
    right = "WORLD EDITION"
    draw.text((W - MARGIN - 8 - draw.textlength(right, font=F["dateline"]), 86),
              right, font=F["dateline"], fill=(220, 215, 200))

    # --- hero 1: Gulf, full width (106-280) ---------------------------
    y0, y1 = 106, 280
    img = photo(HERO1["img"], 524, y1 - y0, cy=0.62)
    page.paste(img, (MARGIN, y0))
    strip = Image.new("RGBA", (524, 20), (0, 0, 0, 150))
    page.paste(strip, (MARGIN, y1 - 20), strip)
    draw = ImageDraw.Draw(page)
    draw.text((MARGIN + 6, y1 - 17), HERO1["caption"], font=F["caption"],
              fill=(245, 242, 235))
    tx, tw2 = 556, W - MARGIN - 556
    draw.text((tx, y0 + 2), HERO1["kicker"], font=F["kicker"], fill=RED)
    y = draw_limited(draw, tx, y0 + 18, HERO1["headline"], F["hero1_head"],
                     INK, tw2, 2, 34)
    draw_limited(draw, tx, y + 8, HERO1["body"], F["hero1_body"], INK,
                 tw2, 5, 15)

    rule(draw, 286, width=1)

    # --- heroes 2 & 3: half width (290-470) ---------------------------
    col_w = (CONTENT_W - 24) // 2
    hy0 = 290
    for i, hero in enumerate(HEROES):
        x = MARGIN + i * (col_w + 24)
        img = photo(hero["img"], col_w, 92)
        page.paste(img, (x, hy0))
        draw = ImageDraw.Draw(page)
        draw.text((x, hy0 + 96), hero["kicker"], font=F["kicker"], fill=RED)
        y = draw_limited(draw, x, hy0 + 112, hero["headline"], F["hero_head"],
                         INK, col_w, 1, 24)
        draw_limited(draw, x, y + 2, hero["body"], F["hero_body"], INK,
                     col_w, 3, 14)

    rule(draw, 476, width=1)

    # --- card rows (480-616, 620-756) ---------------------------------
    def draw_card(x, y, w, card):
        if "img" in card:
            img = photo(card["img"], w, 54)
            page.paste(img, (x, y))
            draw.text((x, y + 58), card["kicker"], font=F["kicker_sm"],
                      fill=RED)
            ny = draw_limited(draw, x, y + 70, card["headline"],
                              F["card_head"], INK, w, 2, 14)
            draw_limited(draw, x, ny + 2, card["body"], F["card_body"],
                         INK, w, 3, 12)
        else:
            draw.text((x, y + 2), card["kicker"], font=F["kicker_sm"],
                      fill=RED)
            draw.text((x, y + 14), card["stat"], font=F["stat"], fill=RED)
            ny = draw_limited(draw, x, y + 50, card["headline"],
                              F["card_head"], INK, w, 2, 14)
            draw_limited(draw, x, ny + 2, card["body"], F["card_body"],
                         INK, w, 3, 12)

    card_w = (CONTENT_W - 3 * 8) // 4
    for row, cards in enumerate((CARDS_ROW1, CARDS_ROW2)):
        cy = 480 + row * 140
        for i, card in enumerate(cards):
            cx = MARGIN + i * (card_w + 8)
            draw_card(cx, cy, card_w, card)

    rule(draw, 762, width=1)

    # --- map section (768-884) ----------------------------------------
    draw.text((MARGIN, 768), "WHERE IT HAPPENED — 18 NOVEMBER 2026",
              font=F["section"], fill=INK)
    rule(draw, 784, x0=MARGIN, x1=280)
    draw_map(draw, (MARGIN, 790, 251, 878))
    lx0 = 266
    col2_w = 360
    for i, place in enumerate(MAP_PLACES):
        col = i // 6
        r = i % 6
        px = lx0 + col * (col2_w + 8)
        py = 790 + r * 15
        draw.text((px, py), place, font=F["map_item"], fill=INK)

    rule(draw, 884, width=1)

    # --- also list (890-1004) -----------------------------------------
    draw.text((MARGIN, 890), "ALSO ON WEDNESDAY 18 NOVEMBER",
              font=F["section"], fill=INK)
    rule(draw, 906, x0=MARGIN, x1=300)
    acols = 4
    acol_w = (CONTENT_W - 3 * 10) // acols
    for i, item in enumerate(ALSO):
        col = i // 6
        r = i % 6
        ax = MARGIN + col * (acol_w + 10)
        ay = 912 + r * 15
        draw.text((ax, ay), "•", font=F["also"], fill=RED)
        draw_limited(draw, ax + 10, ay, item, F["also"], INK, acol_w - 10,
                     1, 11)

    rule(draw, 1008, width=1)
    draw_limited(draw, MARGIN, 1011, FOOTER, F["footer"], MUTED,
                 CONTENT_W, 1, 10)

    out = os.path.join(HERE, "entry.png")
    page.save(out, "PNG", optimize=True)
    return out


if __name__ == "__main__":
    path = build()
    size = os.path.getsize(path)
    print(f"wrote {path} ({size} bytes)")
