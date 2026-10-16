#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""bake_fonts_ft.py - the bake of bake_fonts.py without Windows.

GDI draws small Tahoma as 1-bit, hinted glyphs; FreeType's monochrome
target with the TrueType hinter gives the same kind of pixels from the
font files at hand (Wine's Tahoma, LGPL). The output is the same
`TMP4FNT1` format, so compat/platform_text.cpp reads it unchanged.

The GDI rules that matter: a positive lfHeight is the CELL height
(ascent + descent), so the em size is height * unitsPerEm / (ascent +
descent); glyph rows start at the cell top and the baseline sits at the
ascent; italic is a synthetic shear.
"""
import os
import sys

import bake_fonts

FONT_DIR = '/usr/share/wine/fonts'
FACE_FILES = {
    ('tahoma', False): 'tahoma.ttf',
    ('tahoma', True): 'tahomabd.ttf',
}
# Faces the client asks for that have no file here; on Windows GDI would
# substitute a sans as well.
FACE_ALIASES = {'arial': 'tahoma', 'ariala': 'tahoma'}

EXTRA_FONTS = [('Ariala', 12, False, False)]


def font_file(face, bold):
    """The font file for a face and weight, or None."""
    name = FACE_ALIASES.get(face.lower(), face.lower())
    path = os.path.join(FONT_DIR, FACE_FILES.get((name, bold), ''))
    return path if os.path.isfile(path) else None


def win_metrics(path):
    """usWinAscent/usWinDescent from the OS/2 table - what GDI sizes the cell by.
    The hhea ascender of Wine's Tahoma is lower and cuts the accents of Ğ, İ, Ş."""
    import struct
    data = open(path, 'rb').read()
    count = struct.unpack_from('>H', data, 4)[0]
    for i in range(count):
        entry = 12 + 16 * i
        if data[entry:entry + 4] == b'OS/2':
            offset = struct.unpack_from('>I', data, entry + 8)[0]
            return struct.unpack_from('>HH', data, offset + 74)
    raise ValueError('no OS/2 table in ' + path)


def bake_one(face, height, italic, bold):
    """(cy, glyphs) in the bake_fonts.save layout, or None without a font file."""
    import freetype

    path = font_file(face, bold)
    if not path:
        return None
    ft = freetype.Face(path)
    upm = ft.units_per_EM
    ascent, descent = win_metrics(path)
    ppem = height * upm / float(ascent + descent)
    ft.set_char_size(0, int(round(ppem * 64)), 72, 72)
    if italic:
        ft.set_transform(freetype.Matrix(0x10000, int(0.2 * 0x10000), 0, 0x10000), freetype.Vector(0, 0))

    ascent_px = int(round(ascent * ppem / upm))
    cy = ascent_px + int(round(descent * ppem / upm))

    glyphs = []
    for first, last in bake_fonts.RANGES:
        for code in range(first, last + 1):
            if not ft.get_char_index(code):
                continue
            ft.load_char(chr(code), freetype.FT_LOAD_RENDER | freetype.FT_LOAD_TARGET_MONO)
            slot = ft.glyph
            bitmap = slot.bitmap
            advance = int(round(slot.advance.x / 64.0))
            width, rows, pitch = bitmap.width, bitmap.rows, bitmap.pitch
            source = bitmap.buffer
            byte_count = (width + 7) // 8
            data = bytearray()
            for y in range(cy):
                row = bytearray(byte_count)
                source_y = y - (ascent_px - slot.bitmap_top)
                if 0 <= source_y < rows:
                    base = source_y * pitch
                    for x in range(width):
                        if source[base + (x >> 3)] & (0x80 >> (x & 7)):
                            row[x >> 3] |= 0x80 >> (x & 7)
                data += row
            if width:
                a, b, c, x0 = float(slot.bitmap_left), float(width), float(advance - slot.bitmap_left - width), slot.bitmap_left
            else:
                a, b, c, x0 = 0.0, float(advance), 0.0, 0
            glyphs.append((code, a, b, c, advance, x0, width, cy, bytes(data)))
    return cy, dotted_capital_i(glyphs)


def glyph_pixels(glyph):
    """Set of lit (x, y) cell positions of a baked glyph."""
    x0, width, cy, data = glyph[5], glyph[6], glyph[7], glyph[8]
    byte_count = (width + 7) // 8
    return {(x0 + x, y) for y in range(cy) for x in range(width)
            if data[y * byte_count + (x >> 3)] & (0x80 >> (x & 7))}


def glyph_from_pixels(code, advance, cy, pixels):
    """A baked glyph tuple holding `pixels`."""
    x0 = min(x for x, _ in pixels)
    width = max(x for x, _ in pixels) - x0 + 1
    byte_count = (width + 7) // 8
    data = bytearray(byte_count * cy)
    for x, y in pixels:
        data[y * byte_count + ((x - x0) >> 3)] |= 0x80 >> ((x - x0) & 7)
    return (code, float(x0), float(width), float(advance - x0 - width), advance, x0, width, cy, bytes(data))


def dotted_capital_i(glyphs):
    """Wine's Tahoma draws U+0130 as a bare 1 px stem inside the advance of the
    serifed I, which reads as "İ stemci"; Windows Tahoma draws I with a dot."""
    by_code = {g[0]: i for i, g in enumerate(glyphs)}
    if 0x49 not in by_code or 0x130 not in by_code:
        return glyphs
    plain, dotted = glyphs[by_code[0x49]], glyphs[by_code[0x130]]
    plain_pixels, dotted_pixels = glyph_pixels(plain), glyph_pixels(dotted)
    if not plain_pixels or not dotted_pixels:
        return glyphs
    cap_top = min(y for _, y in plain_pixels)
    dot = {(x, y) for x, y in dotted_pixels if y < cap_top}
    stem = dotted_pixels - dot
    if not dot or not stem:
        return glyphs

    def centre(pixels):
        xs = [x for x, _ in pixels]
        return (min(xs) + max(xs)) / 2.0

    shift = int(round(centre(plain_pixels) - centre(stem)))
    pixels = plain_pixels | {(x + shift, y) for x, y in dot}
    glyphs = list(glyphs)
    glyphs[by_code[0x130]] = glyph_from_pixels(0x130, plain[4], plain[7], pixels)
    return glyphs


def build(target):
    """Bakes bake_fonts.FONTS plus EXTRA_FONTS into `target`; returns the file count."""
    fonts = list(bake_fonts.FONTS)
    for face, height, italic, bold in EXTRA_FONTS:
        for scale in bake_fonts.SCALES:
            entry = (face, int(height * scale + 0.5), italic, bold)
            if entry not in fonts:
                fonts.append(entry)
    how_many = 0
    for face, height, italic, bold in fonts:
        result = bake_one(face, height, italic, bold)
        name = bake_fonts.key_name(face, height, italic, bold)
        if not result:
            print('  %s: no font file' % name)
            continue
        cy, glyphs = result
        bake_fonts.save(os.path.join(target, name + '.bin'), cy, glyphs)
        how_many += 1
    print('FreeType-baked fonts: %d' % how_many)
    return how_many


if __name__ == '__main__':
    sys.exit(0 if build(sys.argv[1] if len(sys.argv) > 1 else bake_fonts.TARGET) > 0 else 1)
