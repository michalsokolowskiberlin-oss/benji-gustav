#!/usr/bin/env python3
"""Erzeugt die App-Icons (PNG) ohne externe Abhängigkeiten.

Das Icon zeigt ein Pixel-Hundegesicht: linke Hälfte Benji (beige,
Schlappohr), rechte Hälfte Gustav (grau, Stehohr).

Aufruf:  python3 tools/gen_icons.py
"""
import os, struct, zlib

# 16x16-Pixelraster. Buchstaben = Farben, "." = Hintergrund.
GRID = [
    "................",
    "............G...",
    ".dd........GG...",
    ".ddbbbbbbgggG...",
    ".ddbbbbbbgggg...",
    ".ddbbbbbbgggg...",
    "..bbbbbbbgggg...",
    "..bkbbbbbggkg...",
    "..bbbbbbbgggg...",
    "..pbwwwwwwwgp...",
    "..bwwwwkwwwwg...",
    "...bwwwwwwwg....",
    "...bbwwwwwgg....",
    "....bbbbggg.....",
    "................",
    "................",
]

PAL = {
    ".": (253, 246, 236, 255),   # Hintergrund (Creme)
    "b": (223, 174, 107, 255),   # Benji Fell
    "d": (185, 133, 74, 255),    # Benji Ohren
    "g": (169, 169, 182, 255),   # Gustav Fell
    "G": (126, 126, 140, 255),   # Gustav Ohren
    "w": (255, 246, 232, 255),   # Schnauze
    "k": (43, 36, 32, 255),      # Augen/Nase
    "p": (244, 160, 181, 255),   # Wangen
}


def write_png(path, size):
    n = len(GRID)
    cell = size // (n + 2)          # 1 Zelle Rand rundherum
    off = (size - cell * n) // 2
    bg = PAL["."]

    rows = []
    for y in range(size):
        row = bytearray([0])        # Filtertyp 0
        gy = (y - off) // cell if cell else -1
        for x in range(size):
            gx = (x - off) // cell if cell else -1
            if 0 <= gy < n and 0 <= gx < n:
                c = PAL.get(GRID[gy][gx], bg)
            else:
                c = bg
            row += bytes(c)
        rows.append(bytes(row))

    def chunk(tag, data):
        return (struct.pack(">I", len(data)) + tag + data
                + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF))

    ihdr = struct.pack(">IIBBBBB", size, size, 8, 6, 0, 0, 0)
    idat = zlib.compress(b"".join(rows), 9)
    png = (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
           + chunk(b"IDAT", idat) + chunk(b"IEND", b""))
    with open(path, "wb") as f:
        f.write(png)
    print(f"  {path}  ({size}x{size}, {len(png)} Bytes)")


if __name__ == "__main__":
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    icons = os.path.join(here, "icons")
    os.makedirs(icons, exist_ok=True)
    write_png(os.path.join(icons, "icon-192.png"), 192)
    write_png(os.path.join(icons, "icon-512.png"), 512)
    write_png(os.path.join(icons, "apple-touch-icon.png"), 180)
    print("Fertig! 🐾")
