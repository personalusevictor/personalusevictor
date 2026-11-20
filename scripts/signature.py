"""Víctor's signature: supplied letterforms with a kitsune replacing the i dot."""

import base64
import json
import subprocess
from functools import lru_cache
from pathlib import Path
from xml.etree import ElementTree

from art import measure, svg_file, text
from contour_field import backdrop

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets/profile"
COLORS = {
    "light": {
        "paper": "#F3EFE7",
        "ink": "#382D26",
        "japanese": "#E7DED3",
        "field-line": "#9B8771",
    },
    "dark": {
        "paper": "#211E1B",
        "ink": "#EDE3D4",
        "japanese": "#393029",
        "field-line": "#C1AB8E",
    },
}


LAYERS = (
    "left",
    "right",
    "up",
    "down",
    "quarter",
    "half",
    "near",
    "closed",
    "wink-quarter",
    "wink-half",
    "wink-near",
    "wink-closed",
    "mouth-neutral",
    "mouth-think",
    "mouth-laugh",
    "mouth-surprise",
)


@lru_cache(maxsize=1)
def performance():
    subprocess.run(["node", str(ROOT / "scripts/compile_kitsune.mjs")], check=True)
    return json.loads((OUTPUT / "identity/kitsune-3d/performance.json").read_text())


def interpolate(track, time):
    for a, b in zip(track, track[1:]):
        if a[0] <= time <= b[0]:
            ratio = (time - a[0]) / (b[0] - a[0])
            return a[1] + (b[1] - a[1]) * ratio
    return track[-1][1]


@lru_cache(maxsize=1)
def motion_style():
    score = performance()
    duration, tracks = score["duration"], score["tracks"]
    keys = sorted(
        {time for key in ("x", "y", "roll", "scale") for time, _ in tracks[key]}
    )
    poses = []
    for time in keys:
        x, y, roll, scale = [
            interpolate(tracks[key], time) for key in ("x", "y", "roll", "scale")
        ]
        poses.append(
            f"{time / duration * 100:.5f}%{{transform:translate({x:.4f}px,{y:.4f}px) rotate({roll:.4f}deg) scale({scale:.5f})}}"
        )
    style = (
        STYLE
        + f".fox-head{{animation:fox-performance {duration}s linear infinite;transform-origin:0px 6px}}@keyframes fox-performance{{"
        + "".join(poses)
        + "}"
    )
    for layer in LAYERS:
        values = "".join(
            f"{time / duration * 100:.5f}%{{opacity:{value:.4f}}}"
            for time, value in tracks[layer]
        )
        style += f".fox-{layer}{{animation:fox-{layer} {duration}s linear infinite}}@keyframes fox-{layer}{{{values}}}"
    return style


STYLE = """
.arrive{animation:arrive 1s cubic-bezier(.16,1,.3,1) both}
.jp-name{opacity:1;animation:name 18s ease-in-out infinite}
.jp-alias{opacity:0;animation:alias 18s ease-in-out infinite}
.fox-reveal{animation:fox-reveal .85s cubic-bezier(.2,.8,.2,1) .35s both;transform-origin:0px 7px}
.fox-layer{opacity:0}.contour-static{display:none}
@keyframes arrive{from{opacity:0;transform:translateY(7px)}to{opacity:1;transform:translateY(0)}}
@keyframes name{0%,37%,100%{opacity:1}47%,87%{opacity:0}}
@keyframes alias{0%,37%,100%{opacity:0}47%,87%{opacity:1}}
@keyframes fox-reveal{0%{opacity:0;transform:translateY(3px) scale(.7)}65%{opacity:1;transform:translateY(-.6px) scale(1.05)}100%{opacity:1;transform:translateY(0) scale(1)}}
@media(prefers-reduced-motion:reduce){*{animation:none!important}.jp-name{opacity:1!important}.jp-alias,.fox-layer,.contour-motion{display:none!important}.contour-static{display:inline}}
"""


def name_outline():
    root = ElementTree.parse(OUTPUT / "identity/name-outline.svg").getroot()
    return root.find("{http://www.w3.org/2000/svg}path").attrib["d"]


@lru_cache(maxsize=20)
def fox_image(frame):
    path = OUTPUT / "identity/kitsune-3d" / f"{frame}.webp"
    return "data:image/webp;base64," + base64.b64encode(path.read_bytes()).decode()


def kitsune(animated=True):
    """The approved portrait stays intact beneath registered eye and mouth patches."""
    original = (
        '<image x="-10.8" y="-12.4" width="21.6" height="21.6" href="'
        + fox_image("open")
        + '"/>'
    )
    if not animated:
        return original
    result = '<g class="fox-reveal"><g class="fox-head">' + original
    result += '<defs><clipPath id="fox-eyelids"><ellipse cx="-3" cy=".7" rx="2.6" ry="1.65"/><ellipse cx="3" cy=".7" rx="2.6" ry="1.65"/></clipPath><clipPath id="fox-wink-eye"><ellipse cx="-3" cy=".7" rx="2.6" ry="1.65"/></clipPath><radialGradient id="fox-feather"><stop offset=".78" stop-color="white"/><stop offset="1" stop-color="black"/></radialGradient><mask id="fox-mouth-mask" maskUnits="userSpaceOnUse" x="-4" y="2.9" width="8" height="4.8"><ellipse cx="0" cy="5.2" rx="3.65" ry="2.12" fill="url(#fox-feather)"/></mask>'
    for frame in ("left", "right", "up", "down", "quarter", "half", "near", "closed"):
        result += f'<image id="eye-{frame}" x="{-10.8+300/1254*21.6:.8f}" y="{-12.4+650/1254*21.6:.8f}" width="{654/1254*21.6:.8f}" height="{230/1254*21.6:.8f}" href="{fox_image("eyes-"+frame)}"/>'
    result += '</defs><g clip-path="url(#fox-eyelids)">'
    for frame in ("left", "right", "up", "down", "quarter", "half", "near", "closed"):
        result += f'<use class="fox-layer fox-{frame}" data-fox-layer="{frame}" href="#eye-{frame}"/>'
    result += '</g><g clip-path="url(#fox-wink-eye)">'
    for frame in ("quarter", "half", "near", "closed"):
        result += f'<use class="fox-layer fox-wink-{frame}" data-fox-layer="wink-{frame}" href="#eye-{frame}"/>'
    result += '</g><g mask="url(#fox-mouth-mask)">'
    for frame in ("neutral", "think", "laugh", "surprise"):
        layer = "mouth-" + frame
        result += f'<image class="fox-layer fox-{layer}" data-fox-layer="{layer}" x="{-10.8+400/1254*21.6:.8f}" y="{-12.4+900/1254*21.6:.8f}" width="{460/1254*21.6:.8f}" height="{280/1254*21.6:.8f}" href="{fox_image(layer)}"/>'
    return result + "</g></g></g>"


def wordmark(p, x, baseline, scale, animated=True):
    return f"""<g transform="translate({x:.3f} {baseline:.3f}) scale({scale:.5f})">
    <path fill="{p['ink']}" d="{name_outline()}"/>
    <g transform="translate(240.33 -30.36)">{kitsune(animated)}</g>
    </g>"""


def center(value, y, size, color, width, face="text"):
    return text(value, (width - measure(value, size, face)) / 2, y, size, color, face)


def banner(theme, mobile=False):
    p = COLORS[theme]
    w, h = (420, 234) if mobile else (900, 308)
    scale = (w - (42 if mobile else 204)) / 318.51
    x = (w - 318.51 * scale) / 2
    baseline = 140 if mobile else 184
    body = f"""<defs>
      <clipPath id="edge"><rect width="{w}" height="{h}" rx="20"/></clipPath>
    </defs>
    <rect width="{w}" height="{h}" rx="20" fill="{p['paper']}"/>
    <g clip-path="url(#edge)">"""
    body += backdrop(p["field-line"], w, h)
    for index, label in enumerate(["ビクトル", "ヴイモ"]):
        body += '<g class="' + ("jp-name" if index == 0 else "jp-alias") + '">'
        body += center(
            label,
            150 if mobile else 197,
            76 if mobile else 130,
            p["japanese"],
            w,
            "jp-signature",
        )
        body += "</g>"
    body += '</g><g class="arrive">' + wordmark(p, x, baseline, scale) + "</g>"
    svg_file(
        OUTPUT / f'header{"-mobile" if mobile else ""}-{theme}.svg',
        w,
        h,
        body,
        "personalusevictor. Un kitsune con zarcillo sustituye al punto de la i. ビクトル y ヴイモ alternan detrás de la firma.",
        motion_style(),
    )


def identity_assets():
    for theme, p in COLORS.items():
        svg_file(
            OUTPUT / f"identity/signature-{theme}.svg",
            740,
            150,
            wordmark(p, 25, 110, 690 / 318.51, animated=False),
            "Firma personalusevictor con el punto de la i en forma de kitsune.",
        )
        svg_file(
            OUTPUT / f"identity/kitsune-{theme}.svg",
            64,
            64,
            f'<g transform="translate(32 32) scale(2.5)">{kitsune(animated=False)}</g>',
            "Detalle kitsune de la firma de Víctor, con su zarcillo.",
        )
    svg_file(
        OUTPUT / "identity/kitsune-live.svg",
        160,
        160,
        f'<g transform="translate(80 88) scale(6)">{kitsune(animated=True)}</g>',
        "Kitsune de Víctor: actuación dirigida con miradas, expresiones, parpadeos y descansos.",
        motion_style(),
    )
    for name, source in [
        ("banner", OUTPUT / "header-light.svg"),
        ("signature", OUTPUT / "identity/signature-light.svg"),
        ("kitsune", OUTPUT / "identity/kitsune-light.svg"),
    ]:
        content = source.read_text()
        for token, color in COLORS["light"].items():
            content = content.replace(color, f"var(--signature-{token},{color})")
        dark = ";".join(
            f"--signature-{token}:{color}" for token, color in COLORS["dark"].items()
        )
        content = content.replace(
            "<style>", f"<style>@media(prefers-color-scheme:dark){{:root{{{dark}}}}}", 1
        )
        (OUTPUT / f"identity/{name}.svg").write_text(content)


if __name__ == "__main__":
    for theme in COLORS:
        for mobile in (False, True):
            banner(theme, mobile)
    identity_assets()
