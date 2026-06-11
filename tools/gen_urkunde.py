#!/usr/bin/env python3
"""Erzeugt die Adoptionsurkunde (PDF, A4) mit QR-Code zur App.

Aufruf:  tools/.venv/bin/python tools/gen_urkunde.py
Output:  Adoptionsurkunde.pdf im Projektordner
"""
import os, struct, zlib, tempfile

import segno
from reportlab.lib.colors import Color, HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

URL = "https://michalsokolowskiberlin-oss.github.io/benji-gustav/"
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(HERE, "Adoptionsurkunde.pdf")

# ---------- Pixel-Hunde (identisch zur App) ----------
PAL = {
    "b": (223, 174, 107, 255), "d": (185, 133, 74, 255),
    "g": (169, 169, 182, 255), "G": (126, 126, 140, 255),
    "w": (255, 246, 232, 255), "k": (43, 36, 32, 255),
    "p": (244, 160, 181, 255), ".": (0, 0, 0, 0),
}
BENJI = [
    ".dd.........dd.",
    ".dbbbbbbbbbbbd.",
    ".dbbbbbbbbbbbd.",
    ".ddbbbbbbbbbdd.",
    "..bbbbbbbbbbb..",
    "..bbbbbbbbbbb..",
    "..pbwwwwwwwbp..",
    "..bwwwwkwwwwb..",
    "...bbwwwwwbb...",
    "...bbbbbbbbb...",
    "..bbbbbbbbbbb..",
    "..bb.bbbbb.bb..",
    "..dd.ddddd.dd..",
]
GUSTAV = [
    ".G...........G.",
    ".GG.........GG.",
    ".GgG.......GgG.",
    "..gwwgggggwwg..",
    "..ggggggggggg..",
    "..ggggggggggg..",
    "..pgwwwwwwwgp..",
    "..gwwwwkwwwwg..",
    "...gwwwwwwwg...",
    "...ggwwwwwgg...",
    "..ggggggggggg..",
    "..gg.ggggg.gg..",
    "..GG.GGGGG.GG..",
]
EYES = [(4, 4), (4, 5), (5, 4), (5, 5), (9, 4), (9, 5), (10, 4), (10, 5)]
SHINE = [(5, 4), (10, 4)]
SMILE = [(6, 8), (8, 8)]


def write_png(path, rows_rgba, w, h):
    raw = b"".join(b"\x00" + bytes(c for px in row for c in px) for row in rows_rgba)

    def chunk(tag, data):
        return (struct.pack(">I", len(data)) + tag + data
                + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF))

    ihdr = struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0)
    png = (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
           + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))
    with open(path, "wb") as f:
        f.write(png)


def render_dog(grid, tail_color, path, cell=24):
    gw, gh = len(grid[0]), len(grid)
    pixels = {}
    for r, row in enumerate(grid):
        for c, ch in enumerate(row):
            if ch != ".":
                pixels[(c, r)] = PAL[ch]
    for (c, r) in EYES:
        pixels[(c, r)] = PAL["k"]
    for (c, r) in SHINE:
        pixels[(c, r)] = PAL["w"]
    for (c, r) in SMILE:
        pixels[(c, r)] = PAL["k"]
    pixels[(14, 8)] = PAL[tail_color]   # Schwanz
    pixels[(13, 9)] = PAL[tail_color]

    w, h = gw * cell, gh * cell
    rows = []
    for y in range(h):
        row = []
        for x in range(w):
            row.append(pixels.get((x // cell, y // cell), (0, 0, 0, 0)))
        rows.append(row)
    write_png(path, rows, w, h)


# ---------- Schrift ----------
def setup_fonts():
    base = "/System/Library/Fonts/Supplemental"
    candidates = {
        "Urkunde": f"{base}/Georgia.ttf",
        "Urkunde-Bold": f"{base}/Georgia Bold.ttf",
        "Urkunde-Italic": f"{base}/Georgia Italic.ttf",
    }
    ok = True
    for name, path in candidates.items():
        if os.path.exists(path):
            pdfmetrics.registerFont(TTFont(name, path))
        else:
            ok = False
    if ok:
        return "Urkunde", "Urkunde-Bold", "Urkunde-Italic"
    return "Times-Roman", "Times-Bold", "Times-Italic"


# ---------- Zeichnen ----------
CREAM = HexColor("#fdf6ec")
BROWN = HexColor("#8a6642")
DARK = HexColor("#4a3c2e")
GOLD = HexColor("#c9a961")
SOFT = HexColor("#9b8569")
RED = HexColor("#d96d6d")


def heart(c, cx, cy, s, color):
    c.setFillColor(color)
    p = c.beginPath()
    p.moveTo(cx, cy - s)
    p.curveTo(cx - 1.7 * s, cy + 0.3 * s, cx - 0.55 * s, cy + 1.1 * s, cx, cy + 0.4 * s)
    p.curveTo(cx + 0.55 * s, cy + 1.1 * s, cx + 1.7 * s, cy + 0.3 * s, cx, cy - s)
    c.drawPath(p, stroke=0, fill=1)


def paw(c, cx, cy, s, alpha=0.10):
    col = Color(BROWN.red, BROWN.green, BROWN.blue, alpha=alpha)
    c.setFillColor(col)
    c.ellipse(cx - s * 0.55, cy - s * 0.5, cx + s * 0.55, cy + s * 0.25, stroke=0, fill=1)
    for dx, dy in [(-0.55, 0.55), (0, 0.75), (0.55, 0.55)]:
        r = s * 0.22
        c.circle(cx + dx * s, cy + dy * s, r, stroke=0, fill=1)


def centred_spaced(c, x, y, text, font, size, charspace, color):
    c.setFillColor(color)
    width = pdfmetrics.stringWidth(text, font, size) + charspace * (len(text) - 1)
    t = c.beginText()
    t.setTextOrigin(x - width / 2, y)
    t.setFont(font, size)
    t.setCharSpace(charspace)
    t.textOut(text)
    t.setCharSpace(0)  # wichtig: Tc wirkt sonst auf ALLE folgenden Texte weiter
    c.drawText(t)


def main():
    serif, serif_b, serif_i = setup_fonts()
    tmp = tempfile.mkdtemp()
    benji_png = os.path.join(tmp, "benji.png")
    gustav_png = os.path.join(tmp, "gustav.png")
    qr_png = os.path.join(tmp, "qr.png")
    render_dog(BENJI, "d", benji_png)
    render_dog(GUSTAV, "G", gustav_png)
    segno.make(URL, error="m").save(qr_png, scale=14, dark="#3b2f23", light=None, border=2)

    W, H = A4
    c = canvas.Canvas(OUT, pagesize=A4)
    c.setTitle("Adoptionsurkunde – Benji & Gustav")

    # Hintergrund + Rahmen
    c.setFillColor(CREAM)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    c.setStrokeColor(BROWN)
    c.setLineWidth(2.5)
    c.roundRect(26, 26, W - 52, H - 52, 14)
    c.setStrokeColor(GOLD)
    c.setLineWidth(1)
    c.setDash(3, 3)
    c.roundRect(36, 36, W - 72, H - 72, 10)
    c.setDash()

    # Pfoten in den Ecken
    for (px_, py_) in [(70, H - 78), (W - 70, H - 78), (70, 72), (W - 70, 72)]:
        paw(c, px_, py_, 16)

    # Titel
    centred_spaced(c, W / 2, H - 110, "ADOPTIONSURKUNDE", serif_b, 30, 4, DARK)
    c.setFont(serif_i, 13)
    c.setFillColor(SOFT)
    c.drawCentredString(W / 2, H - 134, "für zwei treue Gefährten")
    c.setStrokeColor(GOLD)
    c.setLineWidth(1)
    c.line(W / 2 - 90, H - 148, W / 2 + 90, H - 148)
    heart(c, W / 2, H - 146, 5, RED)

    # Hunde
    img_w = 116
    gap = 64
    left_x = W / 2 - gap / 2 - img_w
    right_x = W / 2 + gap / 2
    img_y = H - 296
    ih = img_w * 13 / 15
    c.drawImage(ImageReader(benji_png), left_x, img_y, img_w, ih, mask="auto")
    c.drawImage(ImageReader(gustav_png), right_x, img_y, img_w, ih, mask="auto")
    c.setFont(serif_b, 15)
    c.setFillColor(DARK)
    c.drawCentredString(left_x + img_w / 2, img_y - 22, "Benji")
    c.drawCentredString(right_x + img_w / 2, img_y - 22, "Gustav")
    heart(c, W / 2, img_y + ih / 2 - 4, 7, RED)

    # Haupttext
    c.setFont(serif, 12.5)
    c.setFillColor(DARK)
    text_y = img_y - 56
    for line in [
        "Hiermit wird feierlich beurkundet, dass die beiden Hunde",
        "Benji & Gustav",
        "ab dem heutigen Tag in die liebevollsten Hände ziehen,",
        "die man sich wünschen kann.",
    ]:
        if line == "Benji & Gustav":
            c.setFont(serif_b, 14)
            c.drawCentredString(W / 2, text_y, line)
            c.setFont(serif, 12.5)
        else:
            c.drawCentredString(W / 2, text_y, line)
        text_y -= 19

    # Pflegehinweise
    text_y -= 8
    centred_spaced(c, W / 2, text_y, "PFLEGEHINWEISE", serif_b, 10.5, 2.5, SOFT)
    text_y -= 18
    c.setFont(serif, 11)
    c.setFillColor(DARK)
    for line in [
        "täglich füttern und eine Runde Ball spielen",
        "Streicheleinheiten in unbegrenzter Menge",
        "abends das Licht ausmachen",
        "jeden Tag kurz vorbeischauen – sie warten schon",
    ]:
        c.drawCentredString(W / 2, text_y, line)
        text_y -= 16

    # QR-Block
    qr_size = 106
    box_w, box_h = 178, 158
    box_x, box_y = W / 2 - box_w / 2, text_y - box_h - 10
    c.setFillColor(Color(1, 1, 1, alpha=0.65))
    c.setStrokeColor(GOLD)
    c.setLineWidth(1)
    c.roundRect(box_x, box_y, box_w, box_h, 10, stroke=1, fill=1)
    c.drawImage(ImageReader(qr_png), W / 2 - qr_size / 2, box_y + box_h - qr_size - 10,
                qr_size, qr_size, mask="auto")
    c.setFont(serif_b, 10.5)
    c.setFillColor(DARK)
    c.drawCentredString(W / 2, box_y + 28, "Scanne mich –")
    c.drawCentredString(W / 2, box_y + 14, "deine Hunde ziehen bei dir ein")

    # Unterschriften
    sig_y = 104
    c.setStrokeColor(DARK)
    c.setLineWidth(0.8)
    c.line(86, sig_y, 266, sig_y)
    c.line(W - 266, sig_y, W - 86, sig_y)
    c.setFont(serif_i, 9.5)
    c.setFillColor(SOFT)
    c.drawCentredString(176, sig_y - 14, "adoptiert von")
    c.drawCentredString(W - 176, sig_y - 14, "mit Liebe übergeben von")
    c.setFont(serif, 10.5)
    c.setFillColor(DARK)
    c.drawCentredString(W / 2, 64, "Datum: ____________________")

    # Fußzeile
    c.setFont(serif_i, 8)
    c.setFillColor(SOFT)
    c.drawCentredString(W / 2, 46, URL)

    c.save()
    print(f"Fertig: {OUT}")


if __name__ == "__main__":
    main()
