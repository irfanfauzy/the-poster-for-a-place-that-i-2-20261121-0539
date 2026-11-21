#!/usr/bin/env python3
"""Draw "VELDRIA - The City That Sails at Dusk", a vintage travel poster.

make.fun competition `the-poster-for-a-place-that-i-2-20261121-0539`:
a poster for a place that does not exist. The program in this repo
(main.ts) copies the bundled entry.png to /output/entry.png; this
script is how that PNG is produced, from scratch, with Python/PIL.

Everything is vector shapes and text only (DejaVu fonts from the
system font directory). No photos, no network, no randomness beyond a
fixed seed, so re-running the script reproduces the same image.

    python3 draw_poster.py        # writes entry.png (1024x1024)
"""
import random

from PIL import Image, ImageDraw, ImageFont

SIZE = 1024
FONT_DIR = "/usr/share/fonts/truetype/dejavu/"

# Palette: cream paper, dusk indigo sky, ember horizon, sea teal.
PAPER = (246, 239, 222)
INK = (30, 36, 56)
SKY_TOP = (26, 40, 74)
SKY_MID = (88, 98, 116)
SKY_LOW = (216, 126, 64)
SEA_TOP = (48, 86, 104)
SEA_BOT = (15, 38, 58)
SUN_GOLD = (248, 214, 118)
GOLD = (233, 179, 92)
RUST = (178, 94, 54)
LEAF = (112, 148, 94)
LEAF_DARK = (86, 122, 74)
ROCK = (76, 60, 50)
ROCK_LIT = (94, 74, 60)
WALL = (245, 233, 206)
FOAM = (180, 216, 226)

# The framed scene area; the title band sits below it.
SCENE = (30, 30, 994, 688)
SEA_LINE = 588


def serif(size, bold=False):
    name = "DejaVuSerif-Bold.ttf" if bold else "DejaVuSerif.ttf"
    return ImageFont.truetype(FONT_DIR + name, size)


def blend(c1, c2, t):
    return tuple(round(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))


def tracked_text(draw, cx, y, text, font, fill, gap):
    """Draw `text` centred on `cx`, with `gap` px between letters."""
    widths = [draw.textlength(ch, font=font) for ch in text]
    total = sum(widths) + gap * (len(text) - 1)
    x = cx - total / 2
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=font, fill=fill)
        x += w + gap


def sky(draw):
    x0, y0, x1, y1 = SCENE
    for y in range(y0, y1):
        t = (y - y0) / (y1 - y0)
        if t < 0.5:
            colour = blend(SKY_TOP, SKY_MID, t / 0.5)
        else:
            colour = blend(SKY_MID, SKY_LOW, (t - 0.5) / 0.5)
        draw.line([(x0, y), (x1, y)], fill=colour)


def stars(draw, rng):
    x0, y0, x1, _ = SCENE
    for _ in range(80):
        x = rng.randint(x0 + 10, x1 - 10)
        y = rng.randint(y0 + 10, y0 + 210)
        r = rng.choice([1, 1, 1, 2])
        draw.ellipse([x - r, y - r, x + r, y + r],
                     fill=(255, 243, 210, 190))


def sun(draw):
    cx, cy, r = 700, 478, 92
    for radius, alpha in ((158, 22), (128, 36), (108, 55)):
        draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius],
                     fill=SUN_GOLD + (alpha,))
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=SUN_GOLD)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r],
                 outline=(188, 118, 48), width=3)


def cloud(draw, cx, cy, scale, alpha):
    tone = (245, 228, 198, alpha)
    puffs = [(-46, 6, 24), (-14, -12, 32), (20, -8, 28), (48, 8, 20)]
    for dx, dy, r in puffs:
        s = scale / 40
        draw.ellipse([cx + dx * s - r * s, cy + dy * s - r * s,
                      cx + dx * s + r * s, cy + dy * s + r * s], fill=tone)
    draw.rectangle([cx - 58 * scale / 40, cy + 2,
                    cx + 58 * scale / 40, cy + 14 * scale / 40], fill=tone)


def sea(draw):
    x0, _, x1, y1 = SCENE
    for y in range(SEA_LINE, y1):
        t = (y - SEA_LINE) / (y1 - SEA_LINE)
        draw.line([(x0, y), (x1, y)], fill=blend(SEA_TOP, SEA_BOT, t))
    # Broken golden reflection under the sun.
    for i, (y, w) in enumerate([(598, 118), (614, 92), (632, 126),
                                (652, 80), (672, 104)]):
        draw.rectangle([700 - w // 2, y, 700 + w // 2, y + 5],
                       fill=(248, 202, 112, 195 - i * 28))
    # Wave strokes.
    for y in (604, 628, 656, 680):
        for x in range(x0 + 24, x1 - 24, 88):
            draw.arc([x, y, x + 54, y + 14], 200, 340,
                     fill=(212, 226, 226, 150), width=3)


def floating_island(draw, cx, base, width, height):
    """A rock that tapers to a point below, capped with green turf."""
    half = width // 2
    tip = base + int(height * 1.3)
    draw.polygon([(cx - half, base), (cx - half // 2, base + height),
                  (cx, tip), (cx + half // 2, base + height),
                  (cx + half, base)], fill=ROCK)
    draw.polygon([(cx - half, base), (cx - half // 2, base + height),
                  (cx, tip)], fill=ROCK_LIT)
    draw.ellipse([cx - half - 8, base - 16, cx + half + 8, base + 10],
                 fill=LEAF_DARK)
    draw.ellipse([cx - half - 8, base - 16, cx + half + 8, base],
                 fill=LEAF)


def cottage(draw, x, y, scale=1.0):
    w, h = int(36 * scale), int(26 * scale)
    draw.rectangle([x, y, x + w, y + h], fill=WALL, outline=INK, width=2)
    draw.polygon([(x - 4, y), (x + w // 2, y - int(18 * scale)),
                  (x + w + 4, y)], fill=RUST, outline=INK)
    draw.rectangle([x + w // 2 - 4, y + h - 12, x + w // 2 + 4, y + h],
                   fill=INK)
    for wx in (6, w - 13):
        draw.rectangle([x + wx, y + 6, x + wx + 7, y + 13],
                       fill=SUN_GOLD)


def lighthouse(draw, x, base, scale=1.0):
    w, h = int(22 * scale), int(66 * scale)
    draw.rectangle([x, base - h, x + w, base], fill=WALL, outline=INK,
                   width=2)
    for i in range(3):
        yy = base - h + i * (h // 3)
        draw.rectangle([x, yy, x + w, yy + h // 6], fill=RUST)
    draw.rectangle([x - 4, base - h - 12, x + w + 4, base - h], fill=INK)
    draw.ellipse([x + 3, base - h - 24, x + w - 3, base - h - 10],
                 fill=SUN_GOLD)
    # The lamp's beam, sweeping right across the dusk.
    draw.polygon([(x + w // 2, base - h - 16), (x + w + 150, base - h - 62),
                  (x + w + 150, base - h + 6)],
                 fill=(248, 216, 118, 70))


def waterfall(draw, x, y_top, y_bot):
    draw.rectangle([x, y_top, x + 10, y_bot], fill=FOAM)
    for y in range(y_top + 8, y_bot, 16):
        draw.line([(x + 2, y), (x + 8, y + 8)],
                  fill=(255, 255, 255, 220), width=2)


def airship(draw):
    cx, cy = 428, 246
    draw.ellipse([cx - 132, cy - 36, cx + 132, cy + 36], fill=GOLD,
                 outline=INK, width=3)
    # Stripes following the curve of the envelope.
    for off in (-72, -22, 28, 78):
        draw.arc([cx + off - 26, cy - 36, cx + off + 26, cy + 36],
                 270, 90, fill=RUST, width=6)
    # Tail fins.
    draw.polygon([(cx + 96, cy - 28), (cx + 152, cy - 54),
                  (cx + 152, cy - 8)], fill=RUST, outline=INK)
    draw.polygon([(cx + 96, cy + 28), (cx + 152, cy + 54),
                  (cx + 152, cy + 8)], fill=RUST, outline=INK)
    # Gondola with lit windows, hanging below the envelope.
    draw.rectangle([cx - 52, cy + 36, cx + 52, cy + 62], fill=(98, 68, 46),
                   outline=INK, width=2)
    for wx in range(cx - 40, cx + 48, 22):
        draw.ellipse([wx, cy + 44, wx + 10, cy + 54], fill=SUN_GOLD)
    draw.line([(cx, cy + 62), (cx, cy + 78)], fill=INK, width=2)
    draw.ellipse([cx - 5, cy + 78, cx + 5, cy + 88], fill=INK)


def birds(draw):
    for bx, by, s in ((176, 296, 14), (238, 258, 11), (618, 206, 12),
                      (558, 318, 9), (878, 296, 11)):
        draw.arc([bx - s, by - s // 2, bx, by + s // 2], 200, 340,
                 fill=INK, width=3)
        draw.arc([bx, by - s // 2, bx + s, by + s // 2], 200, 340,
                 fill=INK, width=3)


def title_band(draw):
    x0, _, x1, _ = SCENE
    draw.line([(x0, 722), (x1, 722)], fill=INK, width=3)
    draw.line([(x0, 730), (x1, 730)], fill=RUST, width=2)
    tracked_text(draw, 512, 752, "VELDRIA", serif(118, bold=True), INK, 26)
    tracked_text(draw, 512, 888, "THE CITY THAT SAILS AT DUSK",
                 serif(30), RUST, 8)
    draw.line([(150, 938), (380, 938)], fill=INK, width=2)
    draw.line([(644, 938), (874, 938)], fill=INK, width=2)
    draw.ellipse([502, 930, 522, 950], fill=GOLD, outline=INK, width=2)
    draw.text((512, 960),
              "No roads. Only tides.  \u2022  Visit the island that never stays put.",
              font=serif(21), fill=INK, anchor="ma")


def main():
    img = Image.new("RGB", (SIZE, SIZE), PAPER)
    draw = ImageDraw.Draw(img, "RGBA")
    rng = random.Random(20261121)

    sky(draw)
    stars(draw, rng)
    sun(draw)
    cloud(draw, 218, 168, 40, 170)
    cloud(draw, 878, 128, 30, 150)
    cloud(draw, 478, 108, 24, 130)
    sea(draw)

    # Three floating islands: lighthouse island, cottage island, far islet.
    floating_island(draw, 248, 468, 300, 92)
    lighthouse(draw, 194, 468)
    cottage(draw, 238, 436)
    cottage(draw, 298, 442, 0.85)
    waterfall(draw, 328, 478, SEA_LINE)

    floating_island(draw, 798, 518, 260, 80)
    cottage(draw, 740, 488)
    cottage(draw, 804, 494, 0.9)
    cottage(draw, 854, 498, 0.75)
    waterfall(draw, 878, 526, SEA_LINE)

    floating_island(draw, 498, 418, 130, 46)
    cottage(draw, 476, 396, 0.62)

    airship(draw)
    birds(draw)

    title_band(draw)

    # Scene frame, then the thin double outer border.
    draw.rectangle([SCENE[0], SCENE[1], SCENE[2], SCENE[3]], outline=INK,
                   width=3)
    draw.rectangle([8, 8, 1016, 1016], outline=INK, width=3)
    draw.rectangle([16, 16, 1008, 1008], outline=RUST, width=1)

    img.save("entry.png", format="PNG", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()
