"""
Converts themes.py's ANSI-256 color escape codes to hex, so the web
frontend's theme picker is driven by the same THEMES dict the terminal
renderer uses. this dynamically fettchs any change in the themes dict.
"""

import re
from themes import THEMES

_ANSI_CODE_RE = re.compile(r"\[38;5;(\d+)m")

# Standard xterm 16-color basic palette (codes 0-15)
_BASIC_16 = [
    (0, 0, 0), (128, 0, 0), (0, 128, 0), (128, 128, 0),
    (0, 0, 128), (128, 0, 128), (0, 128, 128), (192, 192, 192),
    (128, 128, 128), (255, 0, 0), (0, 255, 0), (255, 255, 0),
    (0, 0, 255), (255, 0, 255), (0, 255, 255), (255, 255, 255),
]


def _cube_component(v):
    return 0 if v == 0 else 55 + 40 * v


def ansi256_to_rgb(code):
    if code < 16:
        return _BASIC_16[code]
    if code <= 231:
        code -= 16
        r, rem = divmod(code, 36)
        g, b = divmod(rem, 6)
        return (_cube_component(r), _cube_component(g), _cube_component(b))
    v = 8 + (code - 232) * 10
    return (v, v, v)


def ansi_escape_to_hex(escape_code):
    match = _ANSI_CODE_RE.search(escape_code)
    if not match:
        return "#888888"
    r, g, b = ansi256_to_rgb(int(match.group(1)))
    return "#{:02x}{:02x}{:02x}".format(r, g, b)


def serialize_themes():
    result = {}
    for theme_name, palette in THEMES.items():
        hex_palette = {}
        for color_id, escape_code in palette.items():
            if color_id == 0:
                continue  # the "reset" code, not a drawable color
            key = "ghost" if color_id == -1 else str(color_id)
            hex_palette[key] = ansi_escape_to_hex(escape_code)
        result[theme_name] = hex_palette
    return result
