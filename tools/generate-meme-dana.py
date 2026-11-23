#!/usr/bin/env python3
"""Edit Rieko's meme for gta6-meme-x-01 round 2: RDN -> DANA version.

Provenance
----------
Built on ``tools/generate-meme-rdn.py`` (same ghost + "make.fun" branding,
same positions). Two changes, both Rieko's choice on 2026-11-23 ~16:31 WIB:

1. The joke text changes from "Saldo RDN" to "Saldo DANA": RDN
   (Rekening Dana Nasabah, a stock brokerage cash account) is so
   strongly associated with stocks that only investors get the joke
   instantly; a DANA e-wallet balance of Rp 0 is relatable to everyone.
   Only the two "Saldo RDN" lines are repainted ("Rp 0" and
   "Rp 0,000000" are unchanged). Update 2026-11-23 ~16:38 WIB, at
   Rieko's request ("pake logo khasnya saja jangan hanya kata DANA"):
   the word DANA is not written out -- instead the line reads "Saldo"
   in the same bold black style followed by the official DANA logo
   (blue circle + "DANA" wordmark, brand colour #008CEB), so netizens
   recognise it at a glance. Logo source: the DANA brand SVG
   (``assets/dana-logo.svg``, viewBox 80x23), rasterised once to
   ``assets/dana-logo.png`` (1600x460, transparent) and scaled in
   this script to the same height as the "Saldo" text, the two centred
   as one row on the old lines' centres.
   Measured bboxes in the original (1080x1350):
   top    "Saldo RDN"  x 662-978,  y 258-309, centre (820, 283)
   bottom "Saldo RDN"  x 671-969,  y 928-976, centre (820, 952)

2. The "Warga Ritel Unyu" watermark badge is removed, at Rieko's
   request ("warga ritel unyu dihapus", 2026-11-23). The badge sat at
   about x 458-605, y 628-792, straddling the panel dividers. It is
   removed by cloning the clean art strip immediately to its left
   (same rows, shifted left by the art width) over the badge's art
   side only (x 458-554); the badge's white-panel side (x 559-605)
   is repainted panel white, so no art juts into the white panel.
   The cloned art is then lightly blurred (radius 2) to soften the
   seam, and the two divider lines the badge covered are redrawn:
   the horizontal divider (y 671-678, 8 px black) and the vertical
   divider (x 555-558, 4 px black). The badge area is busy foliage
   (above) and soft purple sky (below), so the clone reads as a
   continuation of the picture.

The make.fun branding is untouched: ghost 150 px + bold black
"make.fun" in the empty white space of the bottom-right panel,
below the "Rp 0,000000" punchline (text ends ~y1060, panel ends
y1350), centred as one row -- legible at 480 px wide, as before.

Run:  python3 tools/generate-meme-dana.py   (writes meme.png at the repo root)
Re-running reproduces meme.png byte for byte.
"""

import hashlib
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "assets" / "rdn-original.jpg"
MARK = ROOT / "assets" / "mark-1024.png"
LOGO = ROOT / "assets" / "dana-logo.png"  # DANA logo, 1600x460 transparent
LOGO_ASPECT = 80 / 23  # native viewBox of the DANA brand SVG
OUT = ROOT / "meme.png"

BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
GHOST_SIZE = 150
NAME_SIZE = 54
GAP = 18

# Measured "Saldo RDN" lines in the original (see docstring).
LINES = [
    {"bbox": (662, 258, 978, 309), "centre": (820, 283)},   # top panel
    {"bbox": (671, 928, 969, 976), "centre": (820, 952)},   # bottom panel
]

# Watermark badge mask (x0, y0, x1, y1), generous by a few px.
# The badge straddles the vertical divider: art side x0..VDIV[0]-1,
# white-panel side VDIV[1]+1..x1.
MASK = (458, 628, 605, 792)
# Panel dividers the badge covered (measured).
HDIV = (671, 678)   # horizontal divider rows (inclusive)
VDIV = (555, 558)   # vertical divider columns (inclusive)


def text_layer(text, font, fill=(0, 0, 0, 255)):
    """Render text on its own transparent layer; return layer, ink w/h."""
    probe = Image.new("RGBA", (8, 8))
    left, top, right, bottom = ImageDraw.Draw(probe).textbbox((0, 0), text, font=font)
    w, h = right - left, bottom - top
    layer = Image.new("RGBA", (w + 8, h + 8), (0, 0, 0, 0))
    ImageDraw.Draw(layer).text((4 - left, 4 - top), text, font=font, fill=fill)
    return layer, w, h


def size_for_height(text, target_h):
    """Largest bold size whose rendered ink height is <= target_h."""
    best = None
    for size in range(30, 121):
        font = ImageFont.truetype(BOLD, size)
        _, _, h = text_layer(text, font)
        if h <= target_h:
            best = (size, h)
        else:
            break
    return best


def main():
    img = Image.open(SRC).convert("RGBA")
    w, h = img.size
    assert (w, h) == (1080, 1350), (w, h)
    draw = ImageDraw.Draw(img)

    # --- 1. remove the "Warga Ritel Unyu" badge
    # art side: clone the clean strip immediately to its left
    x0, y0, x1, y1 = MASK
    ax1 = VDIV[0] - 1            # art side ends where the divider starts
    aw = ax1 - x0 + 1            # art-side width
    base = img.copy()  # read source from the untouched copy
    for y in range(y0, y1 + 1):
        for x in range(x0, ax1 + 1):
            img.putpixel((x, y), base.getpixel((x - aw, y)))
    # white-panel side: repaint panel white (sampled below in step 2)
    bg = img.getpixel((1050, 150))[:3]
    draw.rectangle([VDIV[1] + 1, y0, x1, y1], fill=bg + (255,))
    # soften the clone seam (blur pulls in the true neighbours)
    from PIL import ImageFilter

    region = img.crop((x0, y0, ax1 + 1, y1 + 1)).filter(
        ImageFilter.GaussianBlur(2)
    )
    img.paste(region, (x0, y0))
    # redraw the dividers the badge covered
    draw.rectangle([x0, HDIV[0], x1, HDIV[1]], fill=(0, 0, 0, 255))
    draw.rectangle([VDIV[0], y0, VDIV[1], y1], fill=(0, 0, 0, 255))

    # --- 2. repaint "Saldo RDN" -> "Saldo" + DANA logo on both panels
    # panel background bg was sampled in step 1
    logo_src = Image.open(LOGO).convert("RGBA")
    for line in LINES:
        (lx0, ly0, lx1, ly1) = line["bbox"]
        cx, cy = line["centre"]
        target_h = ly1 - ly0 + 1
        size, _ = size_for_height("Saldo", target_h)
        font = ImageFont.truetype(BOLD, size)
        slayer, sw, sh = text_layer("Saldo", font)
        # logo at the same height as the "Saldo" ink, as one centred row
        logo_h = sh
        logo_w = round(logo_h * LOGO_ASPECT)
        logo = logo_src.resize((logo_w, logo_h), Image.LANCZOS)
        gap = 14
        row_w = sw + gap + logo_w
        row_x = cx - row_w // 2
        # white out the old line generously (covers anti-aliasing halo)
        draw.rectangle([lx0 - 12, ly0 - 8, lx1 + 12, ly1 + 8], fill=bg + (255,))
        img.paste(slayer, (row_x, cy - sh // 2), slayer)
        img.paste(logo, (row_x + sw + gap, cy - logo_h // 2), logo)

    # --- 3. make.fun ghost + name, as in the RDN version
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
    print("sha256:", hashlib.sha256(OUT.read_bytes()).hexdigest())
    print("size:", OUT.stat().st_size, "bytes")


if __name__ == "__main__":
    main()
