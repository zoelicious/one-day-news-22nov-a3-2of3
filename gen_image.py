# One-day news front page for Sunday 22 November 2026.
# Drawn from scratch with Pillow: cream broadsheet, red masthead,
# three big hero panels, ten small panels, a real world map with
# numbered pins, a 25-item ALSO list, a DATE CHECK box and a footer.
# Everything is drawn inside its own box; Pillow never clips, so
# every illustration coordinate is computed from the panel rect.
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
CREAM = (248, 242, 223)
PAPER = (255, 253, 245)
INK = (26, 26, 26)
MUTED = (90, 84, 70)
RED = (176, 30, 36)
RED_DK = (140, 20, 26)
LINE = (201, 191, 165)
SEA = (214, 230, 228)
LAND = (232, 222, 188)
LAND_EDGE = (160, 148, 110)
NIGHT = (24, 34, 54)
GOLD = (212, 160, 40)

SERIF = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf"
SANS = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill=INK, leading=None, align="left", box_w=None):
    """Draw lines; returns y just below the last line."""
    lh = leading or int(fnt.size * 1.22)
    for ln in lines:
        if align == "center" and box_w is not None:
            lx = x + (box_w - draw.textlength(ln, font=fnt)) / 2
        else:
            lx = x
        draw.text((lx, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def panel_box(draw, x, y, w, h):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=4,
                           fill=PAPER, outline=LINE, width=1)


def badge(draw, x, y, num, r=10):
    """Red numbered circle; num is a str."""
    draw.ellipse([x - r, y - r, x + r, y + r], fill=RED, outline=(255, 255, 255), width=1)
    f = font(SANS_B, 11 if len(num) < 2 else 10)
    tw = draw.textlength(num, font=f)
    draw.text((x - tw / 2, y - 7 if len(num) < 2 else y - 6), num, font=f, fill=(255, 255, 255))


def kicker(draw, x, y, text, size=9):
    f = font(SANS_B, size)
    draw.text((x, y), text.upper(), font=f, fill=RED)
    return y + size + 3

# ---------------------------------------------------------------- illustrations
# Every scene takes the exact rect it may paint in (x0, y0, x1, y1) and
# stays inside it. Dark night scenes are confined to the illustration
# rect only; the page itself is never dark.

def scene_cop31(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(58, 74, 96))
    d.rectangle([x0, y0, x1, y0 + 14], fill=(38, 50, 70))
    # big wall clock, with its label to the right (never under it,
    # where the delegate rows would cover it)
    cx, cy, r = (x0 + x1) // 2, y0 + 30, 17
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(250, 244, 220), outline=RED, width=2)
    d.line([cx, cy, cx, cy - 11], fill=INK, width=2)
    d.line([cx, cy, cx + 8, cy + 4], fill=INK, width=2)
    d.text((cx + r + 5, cy - 5), "06:00 GMT", font=font(SANS_B, 9), fill=(255, 255, 255))
    # delegate desks, two rows of small figures
    for row in range(2):
        yy = y1 - 26 - row * 18
        for i in range(9):
            px = x0 + 12 + i * ((x1 - x0 - 24) // 8)
            d.ellipse([px, yy - 5, px + 7, yy + 2], fill=(232, 196, 120))
            d.rectangle([px - 2, yy + 2, px + 9, yy + 9], fill=(200, 210, 225) if i % 2 else (150, 170, 195))
        d.rectangle([x0 + 8, yy + 9, x1 - 8, yy + 12], fill=(120, 90, 60))
    # flags strip along the bottom
    cols = [(176, 30, 36), (255, 255, 255), (40, 90, 160), (212, 160, 40), (60, 140, 90)]
    for i, c in enumerate(cols * 3):
        fx = x0 + 10 + i * 20
        if fx + 14 > x1 - 8:
            break
        d.rectangle([fx, y1 - 8, fx + 14, y1 - 3], fill=c)


def scene_bahrain(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=NIGHT)
    # stars
    for sx, sy in [(0.12, 0.15), (0.3, 0.08), (0.55, 0.18), (0.78, 0.1), (0.9, 0.22), (0.42, 0.25)]:
        d.ellipse([x0 + sx * (x1 - x0) - 1, y0 + sy * (y1 - y0) - 1,
                   x0 + sx * (x1 - x0) + 1, y0 + sy * (y1 - y0) + 1], fill=(255, 255, 255))
    # industrial skyline silhouette
    base = y1 - 18
    d.rectangle([x0 + 14, base - 34, x0 + 60, base], fill=(12, 18, 30))
    d.rectangle([x0 + 70, base - 52, x0 + 78, base], fill=(12, 18, 30))
    d.rectangle([x0 + 86, base - 26, x0 + 150, base], fill=(12, 18, 30))
    d.rectangle([x0 + 160, base - 44, x0 + 168, base], fill=(12, 18, 30))
    d.rectangle([x0 + 178, base - 30, x1 - 14, base], fill=(12, 18, 30))
    # flames: layered triangles + glow ellipses, all above the base line
    for fx, fh, fw in [(0.30, 46, 26), (0.52, 58, 30), (0.74, 42, 24)]:
        px = x0 + fx * (x1 - x0)
        d.polygon([(px - fw, base), (px, base - fh), (px + fw, base)], fill=(230, 110, 20))
        d.polygon([(px - fw // 2, base), (px, base - fh + 14), (px + fw // 2, base)], fill=(245, 190, 40))
    d.ellipse([x0 + (x1 - x0) * 0.42, base - 66, x0 + (x1 - x0) * 0.62, base - 44], fill=(120, 120, 120))
    d.ellipse([x0 + (x1 - x0) * 0.58, base - 80, x0 + (x1 - x0) * 0.76, base - 60], fill=(150, 150, 150))
    d.rectangle([x0, base, x1, y1], fill=(8, 12, 22))


def scene_sparta(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(16, 28, 48))
    # moon
    d.ellipse([x1 - 52, y0 + 8, x1 - 30, y0 + 30], fill=(240, 236, 210))
    # sea
    sea_y = y0 + (y1 - y0) * 0.55
    d.rectangle([x0, sea_y, x1, y1], fill=(20, 44, 66))
    for i in range(5):
        wx = x0 + 20 + i * 55
        d.line([wx, sea_y + 14 + (i % 2) * 8, wx + 34, sea_y + 14 + (i % 2) * 8], fill=(90, 130, 160), width=2)
    # ship hull + superstructure
    hx0, hx1 = x0 + 34, x1 - 34
    hy = sea_y + 6
    d.polygon([(hx0, hy), (hx1, hy), (hx1 - 16, hy + 22), (hx0 + 10, hy + 22)], fill=(90, 30, 26))
    d.rectangle([hx0 + 60, hy - 26, hx0 + 130, hy], fill=(210, 205, 190))
    d.rectangle([hx0 + 70, hy - 38, hx0 + 96, hy - 26], fill=(170, 165, 150))
    # containers
    for i, c in enumerate([(200, 90, 60), (60, 120, 160), (200, 90, 60)]):
        d.rectangle([hx0 + 8 + i * 18, hy - 16, hx0 + 24 + i * 18, hy], fill=c)
    # fire on deck + smoke
    fx = (hx0 + hx1) // 2 + 30
    d.polygon([(fx - 16, hy - 24), (fx, hy - 52), (fx + 16, hy - 24)], fill=(235, 120, 25))
    d.polygon([(fx - 8, hy - 24), (fx, hy - 40), (fx + 8, hy - 24)], fill=(250, 200, 60))
    d.ellipse([fx - 6, hy - 66, fx + 18, hy - 46], fill=(130, 130, 130))
    d.ellipse([fx + 8, hy - 82, fx + 30, hy - 64], fill=(160, 160, 160))
    # small rescue boat
    d.polygon([(x0 + 8, y1 - 12), (x0 + 34, y1 - 12), (x0 + 28, y1 - 4), (x0 + 14, y1 - 4)], fill=(230, 220, 180))


def scene_small(d, kind, x0, y0, x1, y1):
    """Compact icon-scene for a small panel; clipped to its rect."""
    mid_y = (y0 + y1) // 2
    cx = (x0 + x1) // 2
    if kind == "vote":
        d.rectangle([x0, y0, x1, y1], fill=(226, 232, 240))
        d.rectangle([cx - 26, mid_y - 6, cx + 26, y1 - 6], fill=(176, 30, 36))
        d.rectangle([cx - 26, mid_y - 6, cx + 26, mid_y + 2], fill=(140, 20, 26))
        d.polygon([(cx - 4, mid_y - 22), (cx + 2, mid_y - 12), (cx + 16, mid_y - 26)], fill=(26, 26, 26))
        d.rectangle([cx - 30, y1 - 6, cx + 30, y1 - 3], fill=(120, 110, 95))
    elif kind == "tanker":
        d.rectangle([x0, y0, x1, y1], fill=(206, 226, 232))
        d.rectangle([x0, mid_y + 6, x1, y1], fill=(30, 70, 100))
        d.rectangle([x0 + 18, mid_y - 12, x1 - 30, mid_y + 6], fill=(150, 40, 36))
        d.rectangle([x1 - 30, mid_y - 22, x1 - 14, mid_y + 6], fill=(210, 205, 190))
        d.polygon([(x0 + 60, mid_y - 12), (x0 + 68, mid_y - 30), (x0 + 76, mid_y - 12)], fill=(235, 120, 25))
        d.ellipse([x0 + 58, mid_y - 40, x0 + 78, mid_y - 26], fill=(150, 150, 150))
    elif kind == "cricket":
        d.rectangle([x0, y0, x1, y1], fill=(214, 232, 200))
        d.ellipse([x0 + 10, y1 - 14, x1 - 10, y1 - 4], fill=(170, 200, 150))
        d.rounded_rectangle([cx - 8, y0 + 8, cx + 8, mid_y + 12], radius=4, fill=(190, 150, 90))
        d.ellipse([x1 - 34, y0 + 10, x1 - 18, y0 + 26], fill=(176, 30, 36))
        d.line([cx + 30, y0 + 14, x1 - 26, y0 + 18], fill=(26, 26, 26), width=2)
    elif kind == "f1":
        d.rectangle([x0, y0, x1, y1], fill=(30, 30, 34))
        d.rectangle([x0 + 12, mid_y - 2, x1 - 12, mid_y + 8], fill=(176, 30, 36))
        d.polygon([(x1 - 40, mid_y - 2), (x1 - 14, mid_y - 14), (x1 - 12, mid_y - 2)], fill=(200, 60, 60))
        d.ellipse([x0 + 26, mid_y + 4, x0 + 44, mid_y + 20], fill=(10, 10, 10), outline=(220, 220, 220))
        d.ellipse([x1 - 52, mid_y + 4, x1 - 34, mid_y + 20], fill=(10, 10, 10), outline=(220, 220, 220))
        d.text((cx - 30, y0 + 6), "LAS VEGAS", font=font(SANS_B, 9), fill=(250, 210, 90))
    elif kind == "arrest":
        d.rectangle([x0, y0, x1, y1], fill=(232, 226, 210))
        d.ellipse([cx - 30, y0 + 6, cx - 8, y0 + 28], fill=(200, 200, 200), outline=(90, 90, 90), width=3)
        d.ellipse([cx + 8, y0 + 6, cx + 30, y0 + 28], fill=(200, 200, 200), outline=(90, 90, 90), width=3)
        d.line([cx - 8, y0 + 17, cx + 8, y0 + 17], fill=(90, 90, 90), width=3)
        d.rectangle([x0 + 14, y1 - 12, x1 - 14, y1 - 6], fill=(90, 84, 70))
    elif kind == "fire":
        d.rectangle([x0, y0, x1, y1], fill=(40, 40, 44))
        d.rectangle([x0 + 16, mid_y - 6, x0 + 30, y1 - 6], fill=(120, 115, 105))
        d.rectangle([x0 + 44, mid_y - 14, x0 + 58, y1 - 6], fill=(120, 115, 105))
        d.polygon([(cx - 12, mid_y + 4), (cx + 4, mid_y - 22), (cx + 20, mid_y + 4)], fill=(235, 120, 25))
        d.polygon([(cx - 5, mid_y + 4), (cx + 4, mid_y - 10), (cx + 13, mid_y + 4)], fill=(250, 200, 60))
    elif kind == "boat":
        d.rectangle([x0, y0, x1, y1], fill=(206, 226, 232))
        d.rectangle([x0, mid_y + 8, x1, y1], fill=(40, 90, 120))
        d.polygon([(x0 + 20, mid_y + 8), (x1 - 20, mid_y + 8), (x1 - 34, mid_y + 22), (x0 + 34, mid_y + 22)], fill=(120, 80, 50))
        d.line([cx, mid_y - 18, cx, mid_y + 8], fill=(90, 70, 50), width=3)
        d.polygon([(cx, mid_y - 18), (cx, mid_y + 2), (cx + 22, mid_y + 2)], fill=(240, 240, 230))
    elif kind == "gaza":
        d.rectangle([x0, y0, x1, y1], fill=(232, 222, 196))
        d.rectangle([x0 + 14, mid_y - 4, x1 - 14, mid_y + 10], fill=(240, 238, 228))
        d.rectangle([x0 + 14, mid_y - 12, x0 + 60, mid_y - 4], fill=(200, 195, 180))
        d.ellipse([x0 + 24, mid_y + 6, x0 + 38, mid_y + 18], fill=(20, 20, 20))
        d.ellipse([x1 - 40, mid_y + 6, x1 - 26, mid_y + 18], fill=(20, 20, 20))
        d.polygon([(cx - 16, y0 + 8), (cx + 2, y0 + 20), (cx + 18, y0 + 6)], fill=(255, 255, 255))
    elif kind == "talks":
        d.rectangle([x0, y0, x1, y1], fill=(226, 230, 236))
        d.rectangle([x0 + 16, y1 - 8, x1 - 16, y1 - 4], fill=(140, 110, 70))
        d.ellipse([cx - 34, y0 + 3, cx - 14, y0 + 17], fill=(220, 180, 140))
        d.ellipse([cx + 14, y0 + 3, cx + 34, y0 + 17], fill=(210, 170, 130))
        d.rectangle([cx - 38, y0 + 19, cx - 10, y1 - 8], fill=(60, 80, 120))
        d.rectangle([cx + 10, y0 + 19, cx + 38, y1 - 8], fill=(90, 90, 90))
    elif kind == "coin":
        d.rectangle([x0, y0, x1, y1], fill=(238, 228, 190))
        d.ellipse([cx - 20, y0 + 4, cx + 20, y1 - 4], fill=(240, 180, 40), outline=(180, 130, 20), width=2)
        d.text((cx - 7, mid_y - 11), "B", font=font(SANS_B, 20), fill=(140, 95, 10))

# ---------------------------------------------------------------- content
# Hero order is fixed: 1 COP31, 2 Bahrain, 3 Sparta II. Cricket is a
# small panel (#6) and F1 a small panel (#7). Figures are the fresh
# ones: Pant 128, India 720/9, lead 352, NZ 105/2; Verstappen wins,
# Norris +0.639 second, Piastri third; COP31 NOT yet approved at
# build time (approval session opens 06:00 GMT), so panel 1 says
# "nears a deal", and the DATE CHECK lists final approval as
# not-yet-happened. ATP final and Liverpool v Man Utd are schedules
# only — neither had been played when this was drawn.

HEROES = [
    dict(num="1", place="ANTALYA, TURKIYE", tag="CLIMATE", scene="cop31",
         title="COP31 nears a deal as approval session opens",
         body="Package unveiled early Sunday after the Friday deadline passed with no text. Objections close 03:00 GMT; approval session opens 06:00 GMT with ~200 nations."),
    dict(num="2", place="BAHRAIN", tag="IRAN WAR", scene="bahrain",
         title="Iran strikes US bases in Bahrain",
         body="Strikes fell Saturday night, reported early Sunday. Iran claims two Patriot radars hit at al-Riffa and Awali; Bahrain says most were intercepted, one industrial site burned, no casualties."),
    dict(num="3", place="GULF OF FINLAND", tag="WAR", scene="sparta",
         title="Russian ship still burning in Finnish waters",
         body="Sparta II hit by two drones Saturday; fire still burning Sunday. 16 crew evacuated; Finland leads the rescue. Helsinki: Ukraine likely behind it."),
]

SMALL = [
    dict(num="4", place="HONG KONG", tag="POLITICS", scene="vote",
         title="Hong Kong votes for its Election Committee",
         body="856 candidates chase 723 seats; turnout 89.81% by 13:00."),
    dict(num="5", place="HORMUZ", tag="IRAN WAR", scene="tanker",
         title="Two tankers hit leaving Hormuz",
         body="One struck in the stern, one in the engine room; no casualties."),
    dict(num="6", place="WELLINGTON", tag="CRICKET", scene="cricket",
         title="Pant 128 as India declare 720/9, lead 352",
         body="Pant 128 off 153 balls; Jurel 78. NZ 105/2, trailing by 247."),
    dict(num="7", place="LAS VEGAS", tag="FORMULA ONE", scene="f1",
         title="Verstappen wins the Las Vegas GP",
         body="Third win in four years. Norris 2nd (+0.639), Piastri 3rd."),
    dict(num="8", place="SINALOA, MEXICO", tag="CRIME", scene="arrest",
         title="Mexico captures 'El Chapo Isidro'",
         body="FBI top-10 fugitive arrested; 11 killed in violence."),
    dict(num="9", place="BASRA, IRAQ", tag="DISASTER", scene="fire",
         title="Power-plant fire kills four in Basra",
         body="Blaze at the Hartha plant; 4 dead, 35 injured."),
    dict(num="10", place="BAYELSA, NIGERIA", tag="DISASTER", scene="boat",
         title="Boat carrying mourners capsizes, 24 dead",
         body="Passengers were heading to a funeral; toll rose to 24."),
    dict(num="11", place="GAZA", tag="CEASEFIRE", scene="gaza",
         title="Four killed as Gaza ceasefire frays",
         body="4 Palestinians dead, 14 hurt; food-aid vehicle hit, 3 killed."),
    dict(num="12", place="JERUSALEM", tag="POLITICS", scene="talks",
         title="Eisenkot invites Likud to coalition talks",
         body="Ex-general seeks the widest coalition; his bloc holds 48 of 120."),
    dict(num="13", place="WORLD", tag="MARKETS", scene="coin",
         title="Bitcoin holds above $60,000 on Sunday",
         body="$60,112 at 01:58 UTC, recovering from Saturday's $55,130 low."),
]

STATS = [
    ("723", "HONG KONG SEATS"),
    ("16", "SPARTA II CREW SAVED"),
    ("2", "US BASES HIT"),
    ("720/9", "INDIA DECLARE"),
    ("$60,112", "BITCOIN 01:58 UTC"),
    ("24", "BAYELSA DEAD"),
]

HOURS = [
    ("01:58 UTC", "Bitcoin $60,112"),
    ("03:00 GMT", "COP31 objections close"),
    ("04:00 UTC", "F1 finish, Las Vegas"),
    ("06:00 GMT", "COP31 approval opens"),
    ("13:00 WIB", "HK turnout 89.81%"),
    ("16:30 GMT", "Liverpool v Man Utd"),
    ("17:00 GMT", "ATP final"),
]

REGIONS = [("EUROPE", 9, (40, 90, 160)), ("MIDDLE EAST", 8, (176, 30, 36)),
           ("ASIA", 7, (200, 140, 40)), ("AMERICAS", 7, (60, 140, 90)),
           ("AFRICA", 3, (150, 100, 40)), ("OCEANIA", 3, (20, 120, 140)),
           ("GLOBAL", 1, (110, 110, 110))]

ALSO = [
    (14, "CIKANDE", "Candy factory fire kills 3 in Java, 36 missing"),
    (15, "N. KORDOFAN", "Landmine kills 22 on road to El-Obeid"),
    (16, "MANIPUR", "Toxic alcohol kills 11, 180+ in hospital"),
    (17, "WASHINGTON", "Nvidia faces SEC accounting probe"),
    (18, "BRASILIA", "Bolsonaro stays in intensive care"),
    (19, "BRUSSELS", "Belgian national strike to ground most flights Monday"),
    (20, "TALLINN", "Estonia to shut its Russia border on 1 Dec"),
    (21, "PARIS", "France seeks UN action over Myanmar ruling"),
    (22, "MANILA", "Chinese bomber turns back 170 km from capital"),
    (23, "LIVERPOOL", "Liverpool host Man Utd 16:30 GMT; Pochettino's first game"),
    (24, "TURIN", "Zverev meets Alcaraz for ATP title 17:00 GMT; No. 1 at stake"),
    (25, "RIYADH", "Saudi coalition downs three Houthi missiles"),
    (26, "GAZA", "Four nations press Israel on Gaza aid"),
    (27, "WASHINGTON", "US airlines warned of Thanksgiving terror threat"),
    (28, "NEW YORK", "US 'open to' a Western Hemisphere UN chief"),
    (29, "NEW DELHI", "Nepal's PM lands in Delhi on first visit"),
    (30, "MOGADISHU", "Somalia expels UAE ambassador, recalls envoy"),
    (31, "COPENHAGEN", "Denmark expels Russian attache over rapper plot"),
    (32, "BRUSSELS", "EU and Indonesia sign trade deal; 98.5% of tariffs scrapped"),
    (33, "TEHRAN", "Iran begins rationing electricity from Sunday, 2 hrs a day"),
    (34, "FLORIDA", "St Johns River breaks 73-year record; floods into January"),
    (35, "SEOUL", "South Korea repeats $75,000 bounty for exam-cheating tips"),
    (36, "NEW DELHI", "Japan to train live-fire in India, a first"),
    (37, "CANBERRA", "Australia rejects US report on AUKUS subs"),
    (38, "MELBOURNE", "Australia chase 188 to beat England in 1st T20"),
]

DATE_CHECK = ("Every story here happened, or was first reported, on Sunday 22 November 2026 "
    "in at least one time zone; some were still developing. Left out as earlier news: "
    "Russia's 400-drone barrage (Thu night into Fri) - Kryvyi Rih strike (Fri night) - "
    "Peru quake (Fri 20 Nov) - Russian missiles in Poland (19 Nov) - Kerch Bridge strikes "
    "(earlier this week) - Shenzhen summit (19 Nov) - Voyager 1 (18 Nov) - GTA VI launch "
    "(19 Nov) - Anthropic IPO debut (19 Nov). Not yet happened when drawn: final COP31 "
    "approval (06:00 GMT) - ATP final (17:00 GMT) - Liverpool v Man Utd (16:30 GMT).")

# ---------------------------------------------------------------- drawing
def draw_header(d):
    d.rectangle([0, 0, W, 8], fill=RED)
    d.rectangle([20, 14, 1004, 46], fill=RED)
    f = font(SANS_B, 17)
    d.text((32, 20), "THE WORLD IN ONE DAY", font=f, fill=(255, 255, 255))
    f2 = font(SANS_B, 11)
    tag = "THE DAY IN DIPLOMACY"
    d.text((1004 - 12 - d.textlength(tag, font=f2), 24), tag, font=f2, fill=(255, 220, 210))
    f3 = font(SERIF, 40)
    title = "Sunday 22 November 2026"
    d.text(((W - d.textlength(title, font=f3)) / 2, 52), title, font=f3, fill=INK)
    f4 = font(SERIF_R, 15)
    sub = "COP31 nears a deal in Antalya  ·  Iran strikes US bases in Bahrain  ·  Russian ship still burning in the Baltic"
    d.text(((W - d.textlength(sub, font=f4)) / 2, 98), sub, font=f4, fill=(70, 60, 45))


def draw_stats(d, y):
    x0, total_w, gap = 20, 984, 8
    bw = (total_w - gap * 5) / 6
    for i, (num, label) in enumerate(STATS):
        x = x0 + i * (bw + gap)
        d.rounded_rectangle([x, y, x + bw, y + 34], radius=3, fill=PAPER, outline=LINE, width=1)
        fn = font(SANS_B, 16)
        d.text((x + (bw - d.textlength(num, font=fn)) / 2, y + 2), num, font=fn, fill=RED)
        fl = font(SANS_B, 7.5)
        d.text((x + (bw - d.textlength(label, font=fl)) / 2, y + 22), label, font=fl, fill=MUTED)
    return y + 34


def draw_regions(d, y):
    total = sum(n for _, n, _ in REGIONS)
    x = 20
    unit = 984 / total
    for name, n, col in REGIONS:
        d.rectangle([x, y, x + unit * n, y + 10], fill=col)
        x += unit * n
    d.rectangle([20, y, 1004, y + 10], outline=INK, width=1)
    fl = font(SANS_B, 8.5)
    legend = "  ·  ".join(f"{name} {n}" for name, n, _ in REGIONS) + f"  —  {total} STORIES"
    d.text(((W - d.textlength(legend, font=fl)) / 2, y + 14), legend, font=fl, fill=MUTED)
    return y + 28


def draw_hours(d, y):
    d.rectangle([20, y, 1004, y + 30], fill=(238, 230, 205), outline=LINE, width=1)
    fl = font(SANS_B, 9)
    d.text((30, y + 9), "THE DAY BY HOURS", font=fl, fill=RED)
    cell_w = (984 - 150) / 7
    for i, (t, label) in enumerate(HOURS):
        cx = 178 + i * cell_w
        ft = font(SANS_B, 9.5)
        d.text((cx, y + 3), t, font=ft, fill=RED_DK)
        fl2 = font(SANS, 8.5)
        for j, ln in enumerate(wrap(d, label, fl2, cell_w - 6)):
            d.text((cx, y + 15 + j * 10), ln, font=fl2, fill=INK)
    return y + 30


def draw_hero(d, p, x, y, w, h):
    panel_box(d, x, y, w, h)
    ih = 88
    scene = {"cop31": scene_cop31, "bahrain": scene_bahrain, "sparta": scene_sparta}[p["scene"]]
    scene(d, x + 1, y + 1, x + w - 1, y + ih)
    badge(d, x + 16, y + 16, p["num"], r=11)
    ty = y + ih + 6
    ty = kicker(d, x + 10, ty, f"{p['place']}  ·  {p['tag']}", size=8.5)
    ft = font(SERIF, 16)
    lines = wrap(d, p["title"], ft, w - 20)
    ty = text_block(d, x + 10, ty, lines[:2], ft, leading=17)
    fb = font(SANS, 10.5)
    blines = wrap(d, p["body"], fb, w - 20)
    text_block(d, x + 10, ty + 2, blines[:3], fb, leading=12)


def draw_small(d, p, x, y, w, h):
    panel_box(d, x, y, w, h)
    ih = 38
    scene_small(d, p["scene"], x + 1, y + 1, x + w - 1, y + ih)
    badge(d, x + 14, y + 14, p["num"], r=9)
    ty = y + ih + 5
    ty = kicker(d, x + 8, ty, f"{p['place']}  ·  {p['tag']}", size=7.5)
    ft = font(SANS_B, 11)
    lines = wrap(d, p["title"], ft, w - 16)
    ty = text_block(d, x + 8, ty, lines[:2], ft, leading=12.5)
    fb = font(SANS, 9.5)
    blines = wrap(d, p["body"], fb, w - 16)
    text_block(d, x + 8, ty + 1, blines[:3], fb, leading=10.5)

# ---------------------------------------------------------------- map
# Coarse equirectangular continent outlines (lon, lat). Kept simple on
# purpose: at 984 x 110 px the map reads as a world map, and every pin
# sits on land. Pins that would collide (Bahrain / Basra / Hormuz,
# Gaza / Jerusalem) use a short leader line from the true spot to an
# offset numbered circle.

CONTINENTS = [
    [(-168, 66), (-140, 70), (-120, 71), (-100, 69), (-85, 66), (-80, 73), (-65, 60),
     (-55, 52), (-60, 46), (-70, 42), (-75, 35), (-81, 31), (-87, 30), (-91, 21),
     (-96, 18), (-102, 16), (-106, 21), (-112, 25), (-117, 30), (-123, 37), (-126, 42),
     (-131, 49), (-140, 60), (-152, 58), (-162, 58), (-168, 66)],
    [(-45, 60), (-32, 68), (-20, 70), (-24, 76), (-40, 80), (-55, 76), (-58, 70),
     (-52, 64), (-45, 60)],
    [(-80, 9), (-74, 11), (-62, 10), (-52, 5), (-50, 0), (-44, -3), (-35, -8),
     (-38, -15), (-41, -23), (-48, -28), (-53, -33), (-58, -38), (-65, -41),
     (-68, -50), (-70, -54), (-73, -48), (-73, -38), (-72, -28), (-70, -19),
     (-76, -14), (-80, -5), (-81, 0), (-80, 9)],
    [(-10, 36), (-9, 43), (-2, 48), (-4, 50), (1, 51), (4, 53), (8, 57), (10, 59),
     (6, 61), (12, 61), (18, 56), (21, 55), (24, 59), (28, 61), (30, 64), (25, 70),
     (18, 69), (12, 65), (6, 58), (9, 54), (14, 54), (19, 54), (24, 58), (28, 55),
     (23, 52), (18, 51), (15, 47), (12, 44), (8, 44), (3, 43), (0, 40), (-2, 37),
     (-6, 36), (-10, 36)],
    [(-6, 35), (0, 36), (10, 37), (12, 34), (20, 32), (30, 31), (32, 31), (34, 28),
     (36, 22), (38, 18), (40, 15), (43, 12), (48, 11), (51, 11), (51, 5), (48, 0),
     (42, -5), (40, -10), (39, -15), (36, -20), (33, -26), (28, -33), (20, -35),
     (17, -32), (15, -27), (13, -20), (12, -12), (13, -5), (9, 4), (4, 6), (-2, 5),
     (-8, 5), (-13, 8), (-16, 12), (-17, 16), (-16, 20), (-14, 25), (-10, 30), (-6, 35)],
    # Asia: traced clockwise — south coast eastward, then the north
    # coast back west, the return leg kept well north of the outward
    # leg so the polygon never pinches or self-intersects.
    [(32, 36), (40, 36), (44, 30), (48, 30), (54, 27), (57, 26), (61, 25),
     (66, 25), (70, 21), (73, 20), (77, 8), (80, 13), (85, 19), (89, 22),
     (92, 21), (96, 16), (99, 9), (103, 2), (104, 7), (107, 11), (109, 14),
     (106, 20), (109, 21), (114, 22), (118, 25), (121, 28), (122, 32),
     (120, 37), (122, 40), (127, 40), (130, 42), (135, 44), (139, 46),
     (141, 52), (142, 59), (139, 60), (132, 59), (128, 55), (124, 50),
     (120, 45), (116, 41), (111, 38), (107, 36), (103, 32), (99, 29),
     (96, 26), (93, 25), (90, 26), (86, 24), (83, 21), (80, 18), (77, 24),
     (74, 25), (71, 27), (68, 28), (65, 28), (62, 28), (59, 28), (56, 29),
     (53, 29), (50, 30), (47, 31), (44, 31), (41, 37), (38, 37), (36, 37),
     (32, 36)],
    [(113, -22), (114, -30), (115, -34), (118, -35), (124, -33), (129, -32),
     (132, -32), (135, -35), (138, -35), (140, -38), (145, -38), (150, -37),
     (153, -32), (153, -27), (150, -22), (146, -19), (142, -15), (142, -11),
     (137, -12), (135, -15), (132, -12), (130, -13), (126, -14), (122, -17),
     (118, -20), (113, -22)],
    # New Zealand, so the Wellington pin sits on land, not in the sea.
    [(167, -34), (172, -35), (174, -37), (176, -38), (178, -38), (176, -41),
     (174, -42), (172, -43), (170, -43), (168, -44), (167, -43), (168, -40),
     (166, -37), (167, -34)],
]

# (number, lon, lat, dx, dy) — dx/dy shift the numbered circle away
# from the true spot; a leader line joins them. (0, 0) = pin on the spot.
PINS = [
    ("1", 30.7, 36.9, 0, 0),
    ("2", 50.6, 26.2, -22, -6),
    ("3", 24.9, 60.2, 0, 0),
    ("4", 114.2, 22.3, 0, 0),
    ("5", 56.8, 26.9, 20, -12),
    ("6", 174.8, -41.3, 0, -10),
    ("7", -115.1, 36.2, 0, 0),
    ("8", -107.4, 24.8, 0, 0),
    ("9", 47.8, 30.5, -4, -20),
    ("10", 6.3, 4.9, 0, 0),
    ("11", 34.5, 31.5, -20, 8),
    ("12", 35.2, 31.8, 16, -14),
    ("13", -74.0, 40.7, 0, 0),
]


def draw_map(d, y, h):
    fh = font(SANS_B, 11)
    d.text((20, y), "WHERE IT HAPPENED", font=fh, fill=RED)
    fr = font(SANS, 9)
    note = "Numbered pins mark panels 1-13"
    d.text((1004 - d.textlength(note, font=fr), y + 1), note, font=fr, fill=MUTED)
    my0, my1 = y + 18, y + h
    d.rectangle([20, my0, 1004, my1], fill=SEA, outline=LINE, width=1)
    lat_top, lat_bot = 72, -48
    def px(lon, lat):
        return (20 + (lon + 180) / 360 * 984, my0 + (lat_top - lat) / (lat_top - lat_bot) * (my1 - my0))
    for poly in CONTINENTS:
        pts = [px(lon, lat) for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=LAND_EDGE)
    for num, lon, lat, dx, dy in PINS:
        tx, ty = px(lon, lat)
        cx, cy = tx + dx, ty + dy
        d.ellipse([tx - 2, ty - 2, tx + 2, ty + 2], fill=INK)
        if dx or dy:
            d.line([tx, ty, cx, cy], fill=INK, width=1)
        badge(d, cx, cy, num, r=8)
    return my1


def draw_also(d, y):
    fh = font(SANS_B, 11)
    d.text((20, y), "ALSO ON SUNDAY 22 NOVEMBER", font=fh, fill=RED)
    d.line([20, y + 16, 1004, y + 16], fill=RED, width=1)
    y += 22
    fnum = font(SANS_B, 9)
    fbody = font(SANS, 9)
    left = ALSO[:13]
    right = ALSO[13:]
    lh = 10.5
    for col_x, items in ((20, left), (512, right)):
        yy = y
        for num, place, text in items:
            d.text((col_x, yy), f"{num}.", font=fnum, fill=RED)
            d.text((col_x + 20, yy), f"{place} — ", font=fnum, fill=INK)
            pw = d.textlength(f"{place} — ", font=fnum)
            d.text((col_x + 20 + pw, yy), text, font=fbody, fill=INK)
            yy += lh
    return y + 13 * lh


def draw_datecheck(d, y):
    d.rounded_rectangle([20, y, 1004, y + 54], radius=4, fill=(250, 228, 224),
                        outline=RED, width=2)
    fh = font(SANS_B, 10)
    d.text((30, y + 5), "DATE CHECK", font=fh, fill=RED)
    fb = font(SANS, 9.5)
    lines = wrap(d, DATE_CHECK, fb, 944)
    text_block(d, 30, y + 19, lines[:3], fb, leading=11)
    return y + 54


def draw_footer(d, y):
    f = font(SANS, 8.5)
    d.text((20, y), "Sources: Reuters · AP · AFP · BBC · ATP · UKMTO · Al Jazeera · wires",
           font=f, fill=MUTED)
    d.text((20, y + 11), "HOW WE CHECKED: every story is dated to 22 November 2026 in at least one "
           "time zone; developing stories are labelled as reported, and what had not happened "
           "yet is listed in the DATE CHECK above.", font=f, fill=MUTED)


def build():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    draw_header(d)
    y = draw_stats(d, 120)
    y = draw_regions(d, y + 6)
    y = draw_hours(d, y + 4)
    # hero row: 3 panels
    hy, hh = y + 8, 180
    hw = 318
    for i, p in enumerate(HEROES):
        draw_hero(d, p, 20 + i * (hw + 15), hy, hw, hh)
    # small panels: 2 rows of 5
    sy, sh = hy + hh + 6, 112
    sw = 190
    for i, p in enumerate(SMALL):
        row, col = divmod(i, 5)
        draw_small(d, p, 20 + col * (sw + 8), sy + row * (sh + 6), sw, sh)
    my = sy + 2 * sh + 6 + 4
    my1 = draw_map(d, my, 100)
    ay = draw_also(d, my1 + 6)
    cy = draw_datecheck(d, ay + 6)
    draw_footer(d, cy + 6)
    return img


def main():
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img = build()
    # Flat-colour newsprint quantises cleanly to a 256-colour palette
    # (verified visually: text stays sharp), which keeps the file far
    # under the 180 KB target instead of ~183 KB as full-colour RGB.
    img = img.convert("P", palette=Image.ADAPTIVE, colors=256)
    img.save(out, optimize=True)
    size = os.path.getsize(out)
    print(f"wrote {out} {img.size[0]}x{img.size[1]} {size} bytes")
    if size > 200000:
        raise SystemExit(f"entry.png too big: {size} bytes (limit 200000)")


if __name__ == "__main__":
    main()
