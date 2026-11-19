#!/usr/bin/env python3
"""One-image world news brief for 19 November 2026.

Deterministic: the same bytes are written on every run. No network, no clock, no randomness.
The facts below were gathered during the build session from public news archives.
"""
from pathlib import Path
import os

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
DATE = "19 NOVEMBER 2026"

# Top stories of the day, condensed to one line each.
STORIES = [
    ("DIPLOMACY", "HISTORIC THREE-WAY TALKS", "Trump, Xi and Putin meet in Shenzhen for the first US-China-Russia trilateral; AI governance split on display."),
    ("TECH", "GTA VI GOES LIVE", "The long-awaited game launches worldwide, setting a new entertainment-release record before its first weekend."),
    ("CLIMATE", "CYCLONE AKVAN NEARS INDIA", "Severe storm tracks toward Odisha and Andhra Pradesh, with landfall expected the following day."),
    ("WAR", "KERCH BRIDGE HIT AGAIN", "A third Ukrainian strike in four days halts rail traffic on the bridge to occupied Crimea."),
    ("RIGHTS", "MYANMAR GENOCIDE RULING", "The top UN court says Myanmar forces killed 10,000 Rohingya, in a landmark genocide-allegation judgment."),
    ("ENERGY", "IRAN'S OIL LEVERAGE SLIPS", "Weakness in Tehran's Hormuz leverage raises fears of escalation rather than concession."),
]

BG = (11, 16, 32)
PANEL = (20, 29, 52)
PANEL2 = (25, 36, 62)
INK = (240, 246, 252)
MUTED = (151, 170, 196)
ACCENT = (95, 224, 179)
WARM = (255, 186, 96)
RED = (255, 115, 115)


def font(size, bold=False):
    """A bundled font where possible, a safe fallback everywhere else."""
    candidates = [
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    try:
        return ImageFont.load_default(size=size)
    except TypeError:
        return ImageFont.load_default()


F_SMALL = font(15)
F_TAG = font(15, True)
F_TITLE = font(31, True)
F_HEAD = font(20, True)
F_BODY = font(15)
F_HERO = font(58, True)
F_DATE = font(19, True)


def wrap(draw, text, fnt, max_width):
    words = text.split()
    lines, current = [], ""
    for word in words:
        trial = f"{current} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_width or not current:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def card(draw, box, tag, headline, detail, accent):
    x0, y0, x1, y1 = box
    draw.rounded_rectangle(box, radius=14, fill=PANEL, outline=(42, 58, 92), width=1)
    draw.rounded_rectangle((x0, y0, x0 + 5, y1), radius=2, fill=accent)
    draw.text((x0 + 22, y0 + 13), tag, font=F_TAG, fill=accent)
    draw.text((x0 + 22, y0 + 38), headline, font=F_HEAD, fill=INK)
    y = y0 + 68
    for line in wrap(draw, detail, F_BODY, x1 - x0 - 44)[:3]:
        draw.text((x0 + 22, y), line, font=F_BODY, fill=MUTED)
        y += 20


def build():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # Subtle grid, drawn from fixed coordinates so both runs are byte-identical.
    for x in range(0, W, 64):
        d.line((x, 0, x, H), fill=(16, 23, 42), width=1)
    for y in range(0, H, 64):
        d.line((0, y, W, y), fill=(16, 23, 42), width=1)

    d.rectangle((0, 0, W, 6), fill=ACCENT)
    d.text((48, 28), "WORLD / ONE IMAGE", font=F_DATE, fill=ACCENT)
    d.text((W - 48 - d.textlength(DATE, font=F_DATE), 28), DATE, font=F_DATE, fill=MUTED)
    d.line((48, 68, W - 48, 68), fill=(42, 58, 92), width=1)

    d.text((48, 96), "THREE LEADERS.", font=F_HERO, fill=INK)
    d.text((48, 164), "ONE TABLE.", font=F_HERO, fill=ACCENT)
    d.text((50, 238), "Trump, Xi and Putin open the first trilateral summit in Shenzhen;", font=F_TITLE, fill=MUTED)
    d.text((50, 279), "AI rules, Ukraine and nuclear stability sit on the same agenda.", font=F_TITLE, fill=MUTED)

    colors = [ACCENT, WARM, (120, 190, 255), RED, (200, 150, 255), WARM]
    for i, (tag, headline, detail) in enumerate(STORIES):
        col, row = i % 2, i // 2
        x0 = 48 + col * 472
        y0 = 350 + row * 178
        card(d, (x0, y0, x0 + 448, y0 + 156), tag, headline, detail, colors[i])

    d.line((48, 906, W - 48, 906), fill=(42, 58, 92), width=1)
    d.text((48, 924), "A single picture of the day's news — curated from public reporting.", font=F_SMALL, fill=INK)
    d.text((48, 950), "Sources: Euronews · CNN · Hindustan Times · AP · Yahoo News", font=F_SMALL, fill=MUTED)
    d.text((48, 976), "Compiled for make.fun · news-image-20261119 · no live data at run time", font=F_SMALL, fill=MUTED)

    return img


def main():
    out = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    Path(out).mkdir(parents=True, exist_ok=True)
    image = build()
    image.save(Path(out) / "entry.png", format="PNG", optimize=True)
    print(f"wrote {Path(out) / 'entry.png'} ({image.size[0]}x{image.size[1]})")


if __name__ == "__main__":
    main()
