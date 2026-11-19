"""Dark editorial cover for Wednesday 18 November 2026.

One 1024x1024 image that sums up the day's world news.
Deterministic: fixed layout, fixed fonts, no timestamps, no randomness.
"""
from PIL import Image, ImageDraw, ImageFont

W = 1024
H = 1024

BG_TOP = (10, 12, 30)
BG_BOT = (24, 18, 48)
INK = (240, 241, 248)
MUTED = (168, 172, 196)
RULE = (74, 78, 110)
ACCENT = (255, 196, 64)

SANS = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
SANS_K = "/usr/share/fonts/truetype/noto/NotoSans-Black.ttf"
SERIF_B = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines = []
    cur = ""
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


def draw_wrapped(draw, xy, text, fnt, fill, max_w, leading):
    x, y = xy
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


HEADLINE = "THREE LEADERS, ONE TARMAC IN SHENZHEN"
HEAD_SUB = (
    "Xi Jinping met Donald Trump at the foot of Air Force One as APEC "
    "opened in Shenzhen, with Vladimir Putin already in talks with Xi "
    "ahead of Thursday's first-ever three-way summit."
)

TILES = [
    {
        "num": "01",
        "chip": "MIDDLE EAST",
        "color": (255, 107, 107),
        "title": "US jets strike Qeshm Island; Iran answers in the Gulf",
        "body": (
            "US fighters hit a Guard missile site on Qeshm Island. Iran "
            "said it targeted US forces in Kuwait, and a UAE ship was "
            "hit in the Strait of Hormuz."
        ),
    },
    {
        "num": "02",
        "chip": "HEALTH",
        "color": (96, 210, 180),
        "title": "US loses measles-free status after 26 years",
        "body": (
            "PAHO ruled the US no longer meets elimination criteria: "
            "5,412 confirmed cases in 2026 after a year of continuous "
            "spread, the most since 1991."
        ),
    },
    {
        "num": "03",
        "chip": "US POLITICS",
        "color": (110, 168, 255),
        "title": "Peltola wins Alaska, Democrats take Senate 56-44",
        "body": (
            "Mary Peltola beat Republican incumbent Dan Sullivan in "
            "the final Senate race of the midterms, sealing the "
            "56-44 Democratic majority."
        ),
    },
    {
        "num": "04",
        "chip": "SPACE",
        "color": (196, 150, 255),
        "title": "Voyager 1 crosses one light-day from Earth",
        "body": (
            "Voyager 1 reached a distance light needs a full 24 hours "
            "to cover - about 16 billion miles - a first for any "
            "human-made object."
        ),
    },
]

BRIEFS = (
    "Cyclone Akvan strengthens toward India's east coast  -  "
    "Nvidia posts $115.8B in quarterly revenue  -  "
    "Congo Ebola outbreak passes 11,000 cases"
)


def main():
    img = Image.new("RGB", (W, H), BG_TOP)
    d = ImageDraw.Draw(img)

    # vertical gradient background, band by band (deterministic)
    for y in range(H):
        t = y / (H - 1)
        r = int(BG_TOP[0] + (BG_BOT[0] - BG_TOP[0]) * t)
        g = int(BG_TOP[1] + (BG_BOT[1] - BG_TOP[1]) * t)
        b = int(BG_TOP[2] + (BG_BOT[2] - BG_TOP[2]) * t)
        d.line([(0, y), (W, y)], fill=(r, g, b))

    margin = 56

    # top strip
    d.text((margin, 42), "WORLD NEWS  -  COVER STORY", font=font(SANS_B, 22), fill=ACCENT)
    date_txt = "WEDNESDAY  -  18 NOV 2026"
    dw = d.textlength(date_txt, font=font(SANS, 20))
    d.text((W - margin - dw, 44), date_txt, font=font(SANS, 20), fill=MUTED)
    d.line([(margin, 84), (W - margin, 84)], fill=RULE, width=2)

    # huge headline
    y = 104
    y = draw_wrapped(d, (margin, y), HEADLINE, font(SANS_K, 70), INK, W - 2 * margin, 80)
    y += 10
    y = draw_wrapped(d, (margin, y), HEAD_SUB, font(SANS, 23), MUTED, W - 2 * margin, 33)
    y += 20
    d.line([(margin, y), (W - margin, y)], fill=ACCENT, width=4)
    y += 24

    # 2x2 tile grid
    gap = 22
    tile_w = (W - 2 * margin - gap) // 2
    tile_h = 212
    for i, tile in enumerate(TILES):
        col = i % 2
        row = i // 2
        x0 = margin + col * (tile_w + gap)
        y0 = y + row * (tile_h + gap)
        x1 = x0 + tile_w
        y1 = y0 + tile_h
        d.rounded_rectangle([x0, y0, x1, y1], radius=14, fill=(22, 25, 48), outline=RULE, width=1)
        # big numeral
        d.text((x0 + 20, y0 + 14), tile["num"], font=font(SERIF_B, 52), fill=tile["color"])
        # category chip
        chip_f = font(SANS_B, 17)
        chip_w = d.textlength(tile["chip"], font=chip_f) + 22
        cx = x1 - chip_w - 16
        d.rounded_rectangle([cx, y0 + 18, cx + chip_w, y0 + 50], radius=9, fill=tile["color"])
        d.text((cx + 11, y0 + 24), tile["chip"], font=chip_f, fill=(12, 12, 22))
        # title and body
        ty = draw_wrapped(d, (x0 + 20, y0 + 80), tile["title"], font(SANS_B, 23), INK, tile_w - 40, 29)
        draw_wrapped(d, (x0 + 20, ty + 4), tile["body"], font(SANS, 17), MUTED, tile_w - 40, 23)

    y = y + 2 * tile_h + gap + 22

    # briefs strip
    d.line([(margin, y), (W - margin, y)], fill=RULE, width=2)
    y += 16
    draw_wrapped(d, (margin, y), BRIEFS, font(SANS, 19), (205, 208, 224), W - 2 * margin, 27)

    # footer
    foot = "Wednesday, 18 November 2026 \u00b7 THE DAY IN ONE IMAGE"
    ff = font(SANS_B, 21)
    fw = d.textlength(foot, font=ff)
    d.text(((W - fw) / 2, H - 52), foot, font=ff, fill=ACCENT)

    img.save("news_image.png", format="PNG", optimize=False)
    print("saved news_image.png", img.size)


if __name__ == "__main__":
    main()
