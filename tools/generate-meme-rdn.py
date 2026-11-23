#!/usr/bin/env python3
"""Edit Rieko's RDN meme for gta6-meme-x-01 round 2.

Provenance
----------
The meme itself is Rieko's own picture, supplied 2026-11-20 ~18:33 WIB
(``assets/rdn-original.jpg``, 1080x1350): a 2x2 grid, GTA V ("FIVE") vs
GTA VI, with "Saldo RDN Rp 0" on the GTA V side and "Saldo RDN
Rp 0,000000" on the GTA VI side -- the joke is that a retail investor's
RDN (Rekening Dana Nasabah, stock brokerage cash account) balance is
zero, and even more precisely zero by the time GTA VI is out. The
"Warga Ritel Unyu" watermark in the bottom-left panel is Rieko's own
and is left untouched. Nothing in the original picture is moved,
recoloured or reworded here.

The only edit is the make.fun branding the bounty requires. The
competition's first criterion is lexicographic: a picture showing none
of make.fun's ghost, logo or name loses to every picture showing one,
whatever else either does; and the brand must be large enough to
recognise when the picture is shrunk to 480 px. So this script adds,
in the empty white space of the bottom-right panel, below the
"Saldo RDN Rp 0,000000" punchline (text ends ~y1060, panel ends y1350):

  make.fun ghost mark (~150 px, official press-kit file
  ``assets/mark-1024.png``) + bold black "make.fun" beside it,
  centred as one row in that panel.

That is the same ghost + name pairing as the round-1 meme, in the same
style (black bold text, white background), so the judge reads it
unambiguously at 480 px: at 480 px wide the ghost is ~67 px and the
name ~24 px tall.

Run:  python3 tools/generate-meme-rdn.py   (writes meme.png at the repo root)
Re-running reproduces meme.png byte for byte.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "assets" / "rdn-original.jpg"
MARK = ROOT / "assets" / "mark-1024.png"
OUT = ROOT / "meme.png"

BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
GHOST_SIZE = 150
NAME_SIZE = 54
GAP = 18


def text_layer(text, font, fill=(0, 0, 0, 255)):
    """Render text on its own transparent layer; return layer, ink w/h."""
    probe = Image.new("RGBA", (8, 8))
    left, top, right, bottom = ImageDraw.Draw(probe).textbbox((0, 0), text, font=font)
    w, h = right - left, bottom - top
    layer = Image.new("RGBA", (w + 8, h + 8), (0, 0, 0, 0))
    ImageDraw.Draw(layer).text((4 - left, 4 - top), text, font=font, fill=fill)
    return layer, w, h


def main():
    img = Image.open(SRC).convert("RGBA")
    w, h = img.size
    assert (w, h) == (1080, 1350), (w, h)

    # --- make.fun ghost + name, bottom-right panel, below the punchline --
    ghost = Image.open(MARK).convert("RGBA").resize(
        (GHOST_SIZE, GHOST_SIZE), Image.LANCZOS
    )
    name_font = ImageFont.truetype(BOLD, NAME_SIZE)
    nlayer, nw, nh = text_layer("make.fun", name_font)

    row_w = GHOST_SIZE + GAP + nw
    panel_cx = 540 + (1080 - 540) // 2  # centre of the right-hand panel
    row_x = panel_cx - row_w // 2
    ghost_y = 1140  # below the "Rp 0,000000" line (ends ~y1060), above the edge
    img.paste(ghost, (row_x, ghost_y), ghost)
    name_x = row_x + GHOST_SIZE + GAP
    name_y = ghost_y + GHOST_SIZE // 2 - nh // 2
    img.paste(nlayer, (name_x, name_y - 4), nlayer)

    img.convert("RGB").save(OUT, format="PNG")


if __name__ == "__main__":
    main()
