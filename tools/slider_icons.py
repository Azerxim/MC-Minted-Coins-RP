#!/usr/bin/env python3
"""Writes the coin icon of each "New mint" slider into every language file.

A slider label is drawn centred on its slider, so the spaces that put the icon
just left of the slider depend on the width of the label in each language.
This script measures each label with the vanilla font (read from the client
jar) and writes the "dialog.minted_coins.create.<coin>.icon" keys.

Run it again after changing a slider label, the slider width or adding a
language:

    python3 tools/slider_icons.py ~/.minecraft/versions/26.3/26.3.jar

Languages without their own label fall back to en_us in game, and so do their
icon keys, so both stay aligned.
"""
import json
import math
import struct
import sys
import zipfile
import zlib
from pathlib import Path

PACK = Path(__file__).resolve().parent.parent
LANG_DIR = PACK / "assets/minted_coins/lang"

SLIDER_WIDTH = 240          # "width" of the number_range inputs in the data pack's create.json
ICON_WIDTH = 11             # visible width of the coin glyphs (assets/minted_coins/font/dialog.json)
ICON_ADVANCE = ICON_WIDTH + 1
GAP = 4                     # pixels between the icon and the slider
MODE = "outside"            # "outside": left of the slider; "inside": against its left edge
VALUE = "8"                 # every digit has the same width in the vanilla font

COINS = {"gold": "", "copper": "", "iron": "", "diamond": ""}
NEGATIVE = [chr(0xF801 + i) for i in range(8)]   # -1, -2, -4 … -128
POSITIVE = [chr(0xF821 + i) for i in range(8)]   # +1, +2, +4 … +128

# options.generic_value ("%s: %s") of the vanilla language files
LABEL_FORMATS = {"fr_fr": "%s : %s", "fr_ca": "%s : %s"}
DEFAULT_LABEL_FORMAT = "%s: %s"


def read_png(data):
    """RGBA rows of a PNG (colour types 0, 2, 3, 4, 6; any bit depth up to 8)."""
    pos, idat, palette, trns = 8, b"", None, None
    while pos < len(data):
        length, kind = struct.unpack(">I4s", data[pos:pos + 8])
        chunk = data[pos + 8:pos + 8 + length]
        pos += 12 + length
        if kind == b"IHDR":
            width, height, depth, colour = struct.unpack(">IIBB", chunk[:10])
        elif kind == b"PLTE":
            palette = [tuple(chunk[i:i + 3]) for i in range(0, len(chunk), 3)]
        elif kind == b"tRNS":
            trns = chunk
        elif kind == b"IDAT":
            idat += chunk
    channels = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}[colour]
    bits = channels * depth
    stride = (width * bits + 7) // 8
    step = max(1, bits // 8)
    raw = zlib.decompress(idat)
    rows, prev, offset = [], bytearray(stride), 0
    for _ in range(height):
        kind = raw[offset]
        line = bytearray(raw[offset + 1:offset + 1 + stride])
        offset += 1 + stride
        for i in range(stride):
            a = line[i - step] if i >= step else 0
            b = prev[i]
            c = prev[i - step] if i >= step else 0
            if kind == 1:
                line[i] = (line[i] + a) & 255
            elif kind == 2:
                line[i] = (line[i] + b) & 255
            elif kind == 3:
                line[i] = (line[i] + (a + b) // 2) & 255
            elif kind == 4:
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                line[i] = (line[i] + (a if pa <= pb and pa <= pc else b if pb <= pc else c)) & 255
        prev = line
        samples = []
        if depth < 8:
            for byte in line:
                for shift in range(8 - depth, -1, -depth):
                    samples.append((byte >> shift) & ((1 << depth) - 1))
        else:
            samples = list(line)
        row = []
        for x in range(width):
            s = samples[x * channels:(x + 1) * channels]
            if colour == 3:
                alpha = trns[s[0]] if trns and s[0] < len(trns) else 255
                row.append((*palette[s[0]], alpha))
            elif colour == 6:
                row.append(tuple(s))
            elif colour == 4:
                row.append((s[0], s[0], s[0], s[1]))
            else:
                row.append((*s[:3], 255) if colour == 2 else (s[0], s[0], s[0], 255))
        rows.append(row)
    return width, height, rows


class Font:
    """Advances of the vanilla default font, as the game computes them."""

    def __init__(self, jar_path):
        self.advances = {}
        with zipfile.ZipFile(jar_path) as jar:
            def load(font_id):
                namespace, path = font_id.split(":")
                return json.loads(jar.read(f"assets/{namespace}/font/{path}.json"))
            for provider in load("minecraft:default")["providers"]:
                if provider["type"] == "reference":
                    for inner in load(provider["id"])["providers"]:
                        self.add(jar, inner)

    def add(self, jar, provider):
        if provider["type"] == "space":
            for char, advance in provider["advances"].items():
                self.advances.setdefault(char, advance)
        elif provider["type"] == "bitmap":
            namespace, path = provider["file"].split(":")
            width, height, pixels = read_png(jar.read(f"assets/{namespace}/textures/{path}"))
            grid = provider["chars"]
            cell_w, cell_h = width // len(grid[0]), height // len(grid)
            scale = provider.get("height", 8) / cell_h
            for row, line in enumerate(grid):
                for col, char in enumerate(line):
                    if char in ("\0", " ") or char in self.advances:
                        continue
                    actual = 0
                    for x in range(cell_w - 1, -1, -1):
                        if any(pixels[row * cell_h + y][col * cell_w + x][3] for y in range(cell_h)):
                            actual = x + 1
                            break
                    self.advances[char] = int(0.5 + actual * scale) + 1

    def width(self, text):
        missing = sorted({c for c in text if c not in self.advances})
        if missing:
            raise SystemExit(f"Not in the vanilla bitmap font (unifont?): {missing!r} in {text!r}")
        return math.ceil(sum(self.advances[c] for c in text))


def spaces(pixels):
    chars = NEGATIVE if pixels < 0 else POSITIVE
    pixels = abs(pixels)
    if pixels > 255:
        raise SystemExit(f"Shift of {pixels}px is too large")
    return "".join(chars[i] for i in range(8) if pixels >> i & 1)


def icon_prefix(font, label, label_format):
    message = label_format.replace("%s", label, 1).replace("%s", VALUE, 1)
    total = font.width(message)
    if total > SLIDER_WIDTH - 4:
        raise SystemExit(f"{message!r} is {total}px wide: it would scroll in a {SLIDER_WIDTH}px slider")
    left = SLIDER_WIDTH // 2 - total // 2          # where the game starts drawing the label
    target = -(GAP + ICON_WIDTH) if MODE == "outside" else GAP
    shift = left - target
    return spaces(-shift) + "{icon}" + spaces(shift - ICON_ADVANCE)


def dump(data):
    text = json.dumps(data, indent=2, ensure_ascii=False)
    return "".join(f"\\u{ord(c):04x}" if 0xE000 <= ord(c) <= 0xF8FF else c for c in text) + "\n"


def main():
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    font = Font(sys.argv[1])
    digits = {font.advances[d] for d in "0123456789"}
    if len(digits) != 1:
        print(f"warning: digits have different widths {digits}, the icon moves with the value")
    english = json.loads((LANG_DIR / "en_us.json").read_text(encoding="utf-8"))
    for path in sorted(LANG_DIR.glob("*.json")):
        lang = json.loads(path.read_text(encoding="utf-8"))
        label_format = LABEL_FORMATS.get(path.stem, DEFAULT_LABEL_FORMAT)
        result = {}
        for key, value in lang.items():
            if key.endswith(".icon") and key.startswith("dialog.minted_coins.create."):
                continue
            result[key] = value
            for coin, glyph in COINS.items():
                if key == f"dialog.minted_coins.create.{coin}":
                    result[key + ".icon"] = icon_prefix(font, value, label_format).replace("{icon}", glyph)
        for coin, glyph in COINS.items():
            key = f"dialog.minted_coins.create.{coin}"
            if key not in lang and key in english:
                print(f"{path.stem}: no {key}, falls back to en_us")
        path.write_text(dump(result), encoding="utf-8", newline="
")
        print(f"{path.stem}: icons written ({label_format!r})")


if __name__ == "__main__":
    main()
