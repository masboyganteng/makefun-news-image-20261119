#!/usr/bin/env python3
"""Draw the news-image-20261119 front page: THE WORLD IN ONE DAY.

Local-only generator. Uses PIL + DejaVu fonts available on this VM.
Deterministic: fixed layout, fixed text, no timestamps, no randomness.
Output: entry.png, 1024x1024.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)      # warm newsprint
INK = (20, 20, 20)          # near-black
RED = (178, 34, 34)         # headline red
BLUE = (18, 64, 120)        # deep blue
GREY = (90, 86, 76)
RULE = (60, 58, 52)
CARD = (255, 255, 255)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap returning lines that fit `width` pixels."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        if not words:
            lines.append("")
            continue
        cur = words[0]
        for w in words[1:]:
            trial = cur + " " + w
            if draw.textlength(trial, font=fnt) <= width:
                cur = trial
            else:
                lines.append(cur)
                cur = w
        lines.append(cur)
    return lines


def draw_centered(draw, y, text, fnt, fill, cx=W // 2):
    draw.text((cx, y), text, font=fnt, fill=fill, anchor="ma")


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 40  # margin
    x0, x1 = M, W - M

    # ---- top thin double rule ----
    d.line([(x0, 24), (x1, 24)], fill=RULE, width=3)
    d.line([(x0, 30), (x1, 30)], fill=RULE, width=1)

    # ---- masthead ----
    f_mast = font(SERIF_B, 60)
    draw_centered(d, 36, "THE WORLD IN ONE DAY", f_mast, INK)
    f_tag = font(SANS, 18)
    draw_centered(d, 106, "One day  •  One planet  •  Every story that mattered",
                  f_tag, GREY)

    # ---- date bar ----
    d.line([(x0, 140), (x1, 140)], fill=RULE, width=2)
    f_date = font(SANS_B, 29)
    draw_centered(d, 149, "THURSDAY, 19 NOVEMBER 2026", f_date, RED)
    d.line([(x0, 192), (x1, 192)], fill=RULE, width=2)

    # ---- hero story: 204 .. 458 (254 tall) ----
    hy0, hy1 = 204, 458
    d.rectangle([x0, hy0, x1, hy1], fill=CARD, outline=RULE, width=2)
    d.rectangle([x0, hy0, x1, hy0 + 8], fill=RED)
    f_kick = font(SANS_B, 19)
    d.text((x0 + 22, hy0 + 20), "TOP STORY  —  THE GULF", font=f_kick, fill=RED)
    f_hero = font(SERIF_B, 42)
    hero_lines = wrap(d, "U.S. and Iran strike again —\nwar spreads across the Gulf",
                      f_hero, x1 - x0 - 44)
    y = hy0 + 48
    for ln in hero_lines:
        d.text((x0 + 22, y), ln, font=f_hero, fill=INK)
        y += 48
    f_body = font(SANS, 19)
    hero_body = (
        "The U.S. hit missile sites on Iran's Qeshm Island on 17 Nov, after "
        "Iran struck a U.S. radar site in Bahrain. On 18 Nov Iran hit a U.S. "
        "base in Kuwait and struck Bahrain again; merchant ships were attacked "
        "in the Strait of Hormuz. U.S. carriers in the region: now three.")
    body_lines = wrap(d, hero_body, f_body, x1 - x0 - 44)
    y += 4
    for ln in body_lines:
        d.text((x0 + 22, y), ln, font=f_body, fill=(40, 40, 40))
        y += 24

    # ---- grid of six stories: 3 cols x 2 rows ----
    stories = [
        ("CULTURE", "GTA VI rolls out worldwide",
         "Gamers return to Vice City as GTA VI begins its global rollout — "
         "after a 13-year wait."),
        ("DIPLOMACY", "Trump, Xi and Putin to meet",
         "The three leaders will hold trilateral talks in Shenzhen during the "
         "APEC summit, 19 Nov."),
        ("AMERICA", "Jeffries to lead the House",
         "Democrats nominate Hakeem Jeffries — set to be the first Black "
         "Speaker of the U.S. House."),
        ("SPACE", "Voyager 1 reaches a light-day",
         "NASA's Voyager 1 passes the one-light-day milestone, almost 50 years "
         "after launch."),
        ("WEATHER", "Cyclone Akvan bears down",
         "Akvan strengthens in the Bay of Bengal; landfall expected on India's "
         "Andhra Pradesh coast, 20 Nov."),
        ("EUROPE", "EU proposes €45bn Ukraine loan",
         "Brussels proposes a €45bn loan for Ukraine, to be repaid once Russia "
         "pays war reparations."),
    ]
    gy0 = 472
    cell_w = (x1 - x0 - 2 * 14) // 3
    cell_h = 186
    row_gap = 12
    f_tag2 = font(SANS_B, 15)
    f_head = font(SERIF_B, 22)
    f_cell = font(SANS, 16)
    for i, (tag, head, body) in enumerate(stories):
        r, c = divmod(i, 3)
        cx0 = x0 + c * (cell_w + 14)
        cy0 = gy0 + r * (cell_h + row_gap)
        d.rectangle([cx0, cy0, cx0 + cell_w, cy0 + cell_h],
                    fill=CARD, outline=(150, 146, 134), width=1)
        d.rectangle([cx0, cy0, cx0 + cell_w, cy0 + 5], fill=BLUE)
        d.text((cx0 + 14, cy0 + 13), tag, font=f_tag2, fill=BLUE)
        hl = wrap(d, head, f_head, cell_w - 28)
        y = cy0 + 38
        for ln in hl[:2]:
            d.text((cx0 + 14, y), ln, font=f_head, fill=INK)
            y += 26
        bl = wrap(d, body, f_cell, cell_w - 28)
        y += 4
        for ln in bl[:3]:
            d.text((cx0 + 14, y), ln, font=f_cell, fill=(45, 45, 45))
            y += 20

    # ---- also-today strip: 870 .. 1000 ----
    ay0, ay1 = 870, 1000
    d.rectangle([x0, ay0, x1, ay1], fill=(232, 226, 208),
                outline=RULE, width=2)
    f_also = font(SANS_B, 19)
    d.text((x0 + 20, ay0 + 10), "ALSO TODAY", font=f_also, fill=RED)
    f_item = font(SANS, 17)
    items = [
        "Nvidia: interim CEO Colette Kress promises faster pay rises after "
        "founder Jensen Huang steps down; Nvidia stops shipping H-series chips "
        "to mainland China.",
        "Fed minutes: most officials expect further interest-rate rises.",
        "India beat Pakistan 2-1 in the SAFF Championship final in Dhaka.",
    ]
    y = ay0 + 38
    for it in items:
        lines = wrap(d, "•  " + it, f_item, x1 - x0 - 40)
        for ln in lines:
            d.text((x0 + 20, y), ln, font=f_item, fill=(35, 35, 35))
            y += 21
        y += 2

    img.save("entry.png", format="PNG", optimize=True)


if __name__ == "__main__":
    main()
