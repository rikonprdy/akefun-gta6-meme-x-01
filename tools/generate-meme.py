#!/usr/bin/env python3
"""Draw the gta6-meme-x-01 meme: an Indonesian quote card in the Cretivox style.

Provenance
----------
Everything on the card is drawn here with Pillow from scratch, except one
asset: the make.fun ghost mark, the official press-kit file
``assets/mark-1024.png`` (white ghost, sparkle eyes, magenta star coin on a
magenta disc, transparent corners, downloaded from https://make.fun/press/).
The mark is composited at the bottom-left, where the reference card carries
its credit line, next to a bold "make.fun" -- so the ghost is part of the
card, not a sticker pasted on a corner.

The joke (the entrant's own words, verbatim): "JANGAN GANGGU!! GUE MAU
NAMATIN GTA VI JALUR STREAMING BANG WINDAH." -- "don't disturb me, I'm
finishing GTA VI by watching Bang Windah's stream" (Bang Windah is a famous
Indonesian gaming streamer; many Indonesian gamers experience the game
through his stream instead of playing it themselves). The reference card is
a minimalist white quote card: big bold black italic text, a large
light-grey quotation mark bottom-right, a small credit bottom-left. No
"Cretivox" credit is copied: that is someone else's watermark and is left
out; the bottom-left carries the make.fun ghost and name instead.

Layout (1024x1024, judged shrunk to 480x480, so everything is large):
  plain white background
  quote text, Liberation Sans Bold Italic, black, left-aligned:
    "JANGAN GANGGU!!" large, then the four lines below it
  text is rendered then squeezed horizontally (x0.82) to the condensed
  heavy-italic look of the reference card
  giant light-grey quotation mark bottom-right
  make.fun ghost mark (~140 px) + bold "make.fun" bottom-left

Run:  python3 tools/generate-meme.py   (writes meme.png at the repo root)
Re-running reproduces meme.png byte for byte.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
MARK = ROOT / "assets" / "mark-1024.png"
OUT = ROOT / "meme.png"

W = H = 1024
BLACK = (0, 0, 0, 255)
QUOTE_GREY = (232, 232, 232, 255)

LIBERATION = "/usr/share/fonts/truetype/liberation"
BOLD_ITALIC = f"{LIBERATION}/LiberationSans-BoldItalic.ttf"
BOLD = f"{LIBERATION}/LiberationSans-Bold.ttf"

MARGIN = 48            # text left margin / right limit
SQUEEZE = 0.82         # horizontal condense, the reference card's look
MAX_TEXT_W = W - 2 * MARGIN

LINES = [
    ("JANGAN GANGGU!!", 118),   # headline, larger than the rest
    ("GUE MAU NAMATIN", 96),
    ("GTA VI JALUR", 96),
    ("STREAMING", 96),
    ("BANG WINDAH.", 96),
]


def text_layer(text, font, fill=BLACK):
    """Render one line on its own transparent layer; return layer, ink w/h."""
    probe = Image.new("RGBA", (8, 8))
    left, top, right, bottom = ImageDraw.Draw(probe).textbbox((0, 0), text, font=font)
    w, h = right - left, bottom - top
    layer = Image.new("RGBA", (w + 8, h + 8), (0, 0, 0, 0))
    ImageDraw.Draw(layer).text((4 - left, 4 - top), text, font=font, fill=fill)
    return layer, w, h


def draw_line(canvas, text, size, x, y):
    """Draw one condensed italic line; return the ink height used."""
    font = ImageFont.truetype(BOLD_ITALIC, size)
    layer, w, h = text_layer(text, font)
    squeezed_w = round(layer.width * SQUEEZE)
    if squeezed_w > MAX_TEXT_W:
        # shrink the font until the squeezed line fits the card
        size = int(size * MAX_TEXT_W / squeezed_w)
        font = ImageFont.truetype(BOLD_ITALIC, size)
        layer, w, h = text_layer(text, font)
        squeezed_w = round(layer.width * SQUEEZE)
    layer = layer.resize((squeezed_w, layer.height), Image.LANCZOS)
    canvas.paste(layer, (x, y - 4), layer)
    return h


def main():
    img = Image.new("RGBA", (W, H), (255, 255, 255, 255))

    # --- quote text, top of the card -------------------------------------
    y = 92
    for i, (text, size) in enumerate(LINES):
        h = draw_line(img, text, size, MARGIN, y)
        y += h
        y += 30 if i == 0 else 14  # wider gap after the headline

    # --- giant light-grey quotation mark, bottom-right --------------------
    # Render big, then crop to the glyph's actual ink (font metrics
    # over-report this glyph's box) and scale the ink to ~340 px tall.
    quote_font = ImageFont.truetype(BOLD, 470)
    qlayer, qw, qh = text_layer("\u201c", quote_font, fill=QUOTE_GREY)
    ink = qlayer.crop(qlayer.getbbox())
    target_h = 340
    target_w = round(ink.width * target_h / ink.height)
    ink = ink.resize((target_w, target_h), Image.LANCZOS)
    img.paste(ink, (995 - target_w, 995 - target_h), ink)

    # --- make.fun ghost + name, bottom-left (the card's credit line) -----
    ghost = Image.open(MARK).convert("RGBA").resize((140, 140), Image.LANCZOS)
    ghost_x, ghost_y = 56, H - 56 - 140
    img.paste(ghost, (ghost_x, ghost_y), ghost)

    name_font = ImageFont.truetype(BOLD_ITALIC, 46)
    nlayer, nw, nh = text_layer("make.fun", name_font)
    name_x = ghost_x + 140 + 22
    name_y = ghost_y + 70 - nh // 2  # vertically centred on the ghost
    img.paste(nlayer, (name_x, name_y - 4), nlayer)

    img.convert("RGB").save(OUT, format="PNG")


if __name__ == "__main__":
    main()
