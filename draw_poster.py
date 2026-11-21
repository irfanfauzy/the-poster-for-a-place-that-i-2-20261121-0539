#!/usr/bin/env python3
"""Draw the travel poster for VELDRIA, a place that does not exist.

make.fun competition `the-poster-for-a-place-that-i-2-20261121-0539`:
a program that writes one image to /output/entry.png — a travel poster
for a place that does not exist. Output must be at most 1,048,576 bytes
and 1024x1024 pixels.

The poster is drawn from scratch with Python/PIL (DejaVu fonts, vector
shapes only, no photos, no network). `main.ts` copies the bundled
entry.png to the grader's output folder, deterministically.

Local check:
    python3 draw_poster.py && ls -l entry.png
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
"""
import math
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
CREAM = (245, 238, 221)
INK = (32, 38, 58)
TEAL_DARK = (23, 52, 74)
RUST = (176, 92, 52)
GOLD = (232, 178, 90)
SUN = (247, 215, 116)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
serif_bold = lambda s: ImageFont.truetype(FONT_DIR + "DejaVuSerif-Bold.ttf", s)
serif = lambda s: ImageFont.truetype(FONT_DIR + "DejaVuSerif.ttf", s)
serif_it = lambda s: ImageFont.truetype(FONT_DIR + "DejaVuSerif.ttf", s)  # no Italic file on this VM; plain Serif stands in
sans = lambda s: ImageFont.truetype(FONT_DIR + "DejaVuSans.ttf", s)
sans_bold = lambda s: ImageFont.truetype(FONT_DIR + "DejaVuSans-Bold.ttf", s)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def draw_spaced(draw, cx, y, text, font, fill, tracking=10):
    """Draw centred text with letter tracking."""
    widths = [draw.textlength(ch, font=font) for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = cx - total / 2
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=font, fill=fill)
        x += w + tracking


def main():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img, "RGBA")

    # ---- scene: sky gradient, (28,28)-(996,700) ----
    sx0, sy0, sx1, sy1 = 28, 28, 996, 700
    top = (24, 40, 72)      # deep dusk indigo
    mid = (84, 96, 110)     # hazy blue
    hor = (214, 122, 62)    # ember horizon
    for y in range(sy0, sy1):
        t = (y - sy0) / (sy1 - sy0)
        if t < 0.55:
            c = lerp(top, mid, t / 0.55)
        else:
            c = lerp(mid, hor, (t - 0.55) / 0.45)
        d.line([(sx0, y), (sx1, y)], fill=c)
    d.rectangle([sx0, sy0, sx1, sy1], outline=INK, width=3)

    # stars in the upper sky
    import random
    rng = random.Random(20261121)
    for _ in range(70):
        x = rng.randint(sx0 + 8, sx1 - 8)
        y = rng.randint(sy0 + 8, sy0 + 220)
        r = rng.choice([1, 1, 2])
        d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 244, 214, 200))

    # sun + halo, low over the horizon
    sun_cx, sun_cy, sun_r = 712, 486, 88
    for rr, alpha in ((150, 26), (125, 40), (105, 60)):
        d.ellipse([sun_cx - rr, sun_cy - rr, sun_cx + rr, sun_cy + rr],
                  fill=SUN + (alpha,))
    d.ellipse([sun_cx - sun_r, sun_cy - sun_r, sun_cx + sun_r, sun_cy + sun_r],
              fill=SUN)
    d.ellipse([sun_cx - sun_r, sun_cy - sun_r, sun_cx + sun_r, sun_cy + sun_r],
              outline=(190, 120, 50), width=3)

    # clouds: flat-bottomed vintage puffs
    def cloud(cx, cy, s, tone):
        for dx, dy, r in ((-52, 8, 26), (-18, -12, 34), (22, -6, 30), (52, 10, 22)):
            d.ellipse([cx + dx * s / 40 - r * s / 40, cy + dy * s / 40 - r * s / 40,
                       cx + dx * s / 40 + r * s / 40, cy + dy * s / 40 + r * s / 40],
                      fill=tone)
        d.rectangle([cx - 62 * s / 40, cy + 2, cx + 62 * s / 40, cy + 16 * s / 40],
                    fill=tone)
    cloud(220, 170, 40, (244, 226, 196, 170))
    cloud(880, 130, 30, (244, 226, 196, 150))
    cloud(480, 110, 24, (232, 200, 170, 130))

    # ---- sea at the bottom of the scene ----
    sea_y = 596
    for y in range(sea_y, sy1):
        t = (y - sea_y) / (sy1 - sea_y)
        d.line([(sx0, y), (sx1, y)], fill=lerp((46, 84, 102), (16, 40, 60), t))
    # sun reflection: broken golden column
    for i, (yy, ww) in enumerate([(606, 120), (622, 96), (640, 130), (660, 84), (680, 110)]):
        d.rectangle([sun_cx - ww // 2, yy, sun_cx + ww // 2, yy + 5],
                    fill=(247, 200, 110, 200 - i * 25))
    # wave strokes
    for yy in (612, 636, 664, 688):
        for xx in range(sx0 + 20, sx1 - 20, 86):
            d.arc([xx, yy, xx + 56, yy + 14], 200, 340,
                  fill=(210, 225, 225, 160), width=3)

    # ---- floating islands ----
    def island(cx, base_y, w, h, scale=1.0):
        # rock: tapered underside
        rock = [(cx - w // 2, base_y), (cx - w // 4, base_y + h),
                (cx, base_y + int(h * 1.25)), (cx + w // 4, base_y + h),
                (cx + w // 2, base_y)]
        d.polygon(rock, fill=(74, 58, 48))
        d.polygon([(cx - w // 2, base_y), (cx - w // 4, base_y + h),
                   (cx, base_y + int(h * 1.25))], fill=(92, 72, 58))
        # grassy cap
        d.ellipse([cx - w // 2 - 6, base_y - 14, cx + w // 2 + 6, base_y + 12],
                  fill=(86, 122, 74))
        d.ellipse([cx - w // 2 - 6, base_y - 14, cx + w // 2 + 6, base_y + 2],
                  fill=(110, 146, 92))

    def house(x, y, s=1.0):
        bw, bh = int(34 * s), int(26 * s)
        d.rectangle([x, y, x + bw, y + bh], fill=(244, 232, 205),
                    outline=INK, width=2)
        d.polygon([(x - 4, y), (x + bw // 2, y - int(18 * s)), (x + bw + 4, y)],
                  fill=RUST, outline=INK)
        d.rectangle([x + bw // 2 - 4, y + bh - 12, x + bw // 2 + 4, y + bh],
                    fill=INK)
        d.rectangle([x + 6, y + 6, x + 12, y + 12], fill=(247, 215, 116))
        d.rectangle([x + bw - 12, y + 6, x + bw - 6, y + 12], fill=(247, 215, 116))

    def lighthouse(x, y, s=1.0):
        w, h = int(20 * s), int(64 * s)
        d.rectangle([x, y - h, x + w, y], fill=(244, 238, 221), outline=INK, width=2)
        for i in range(3):
            yy = y - h + i * (h // 3)
            d.rectangle([x, yy, x + w, yy + h // 6], fill=RUST)
        d.rectangle([x - 4, y - h - 12, x + w + 4, y - h], fill=INK)
        d.ellipse([x + 2, y - h - 24, x + w - 2, y - h - 10], fill=SUN)
        # light beam
        d.polygon([(x + w // 2, y - h - 16), (x + w + 150, y - h - 60),
                   (x + w + 150, y - h + 8)], fill=(247, 215, 116, 70))

    def waterfall(x, y0, y1):
        d.rectangle([x, y0, x + 10, y1], fill=(178, 214, 224))
        for yy in range(y0 + 6, y1, 16):
            d.line([(x + 2, yy), (x + 8, yy + 8)], fill=(255, 255, 255, 220), width=2)

    # left island with lighthouse
    island(250, 470, 300, 92)
    lighthouse(196, 470)
    house(240, 438, 1.0)
    house(300, 444, 0.85)
    waterfall(330, 480, 596)
    # right island with houses
    island(800, 520, 260, 80)
    house(742, 490, 1.0)
    house(806, 496, 0.9)
    house(856, 500, 0.75)
    waterfall(880, 528, 596)
    # small far island
    island(500, 420, 130, 46, 0.7)
    house(478, 398, 0.62)

    # ---- airship ----
    ax, ay = 430, 250
    d.ellipse([ax - 130, ay - 34, ax + 130, ay + 34], fill=(232, 178, 90),
              outline=INK, width=3)
    d.ellipse([ax - 130, ay - 34, ax + 130, ay + 34], outline=(120, 60, 30), width=2)
    for stripe_x in (-70, -20, 30, 80):
        d.arc([ax + stripe_x - 26, ay - 34, ax + stripe_x + 26, ay + 34],
              270, 90, fill=RUST, width=6)
    d.polygon([(ax + 96, ay - 26), (ax + 150, ay - 52), (ax + 150, ay - 6)],
              fill=RUST, outline=INK)
    d.polygon([(ax + 96, ay + 26), (ax + 150, ay + 52), (ax + 150, ay + 6)],
              fill=RUST, outline=INK)
    d.rectangle([ax - 52, ay + 34, ax + 52, ay + 62], fill=(96, 66, 44),
                outline=INK, width=2)
    for wx in range(ax - 40, ax + 48, 22):
        d.ellipse([wx, ay + 42, wx + 10, ay + 52], fill=SUN)
    d.line([(ax, ay + 62), (ax, ay + 78)], fill=INK, width=2)
    d.ellipse([ax - 5, ay + 78, ax + 5, ay + 88], fill=INK)

    # birds
    for bx, by, s in ((180, 300, 14), (240, 260, 11), (620, 210, 12),
                      (560, 320, 9), (880, 300, 11)):
        d.arc([bx - s, by - s // 2, bx, by + s // 2], 200, 340, fill=INK, width=3)
        d.arc([bx, by - s // 2, bx + s, by + s // 2], 200, 340, fill=INK, width=3)

    # ---- title band ----
    d.line([(sx0, 728), (sx1, 728)], fill=INK, width=3)
    d.line([(sx0, 736), (sx1, 736)], fill=RUST, width=2)
    draw_spaced(d, 512, 758, "VELDRIA", serif_bold(118), INK, tracking=26)
    draw_spaced(d, 512, 892, "THE CITY THAT SAILS AT DUSK",
                serif(30), RUST, tracking=8)
    d.line([(150, 940), (380, 940)], fill=INK, width=2)
    d.line([(644, 940), (874, 940)], fill=INK, width=2)
    d.ellipse([502, 932, 522, 952], fill=GOLD, outline=INK, width=2)
    d.text((512, 962), "No roads. Only tides.  •  Visit the island that never stays put.",
           font=serif_it(21), fill=INK, anchor="ma")
    # footer strip
    d.text((512, 1002 - 28 + 6), "", font=sans(10), fill=INK)
    # thin outer frame
    d.rectangle([8, 8, 1016, 1016], outline=INK, width=3)
    d.rectangle([16, 16, 1008, 1008], outline=RUST, width=1)

    img.save("entry.png", format="PNG", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()
