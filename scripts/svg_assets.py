"""Shared self-contained SVG image embedding."""

import base64
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets/profile"


def image(relative, x, y, width, height, fit="xMidYMid meet", theme=None):
    path = ROOT / relative
    data = path.read_bytes()
    if path.suffix == ".svg" and path.stem == "astro" and theme == "dark":
        data = data.replace(b"#000014", b"#F3EFE7").replace(b"#150426", b"#DED3C4")
    mime = {".svg": "image/svg+xml", ".png": "image/png", ".jpg": "image/jpeg"}[
        path.suffix
    ]
    uri = base64.b64encode(data).decode()
    return f'<image x="{x}" y="{y}" width="{width}" height="{height}" preserveAspectRatio="{fit}" href="data:{mime};base64,{uri}"/>'
