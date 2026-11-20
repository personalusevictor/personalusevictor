"""Shared vector typography and drawing primitives for the profile artwork."""

from functools import lru_cache
from html import escape
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen

ROOT = Path(__file__).resolve().parents[1]
FONTS = ROOT / ".cache/fonts"


@lru_cache(maxsize=None)
def font(name):
    filename, weight = {
        "text": ("Outfit[wght].ttf", 450),
        "regular": ("Outfit[wght].ttf", 400),
        "bold": ("Outfit[wght].ttf", 650),
        "editorial": ("BricolageGrotesque.ttf", 650),
        "jp-signature": ("ZenKakuGothicNew-Bold.ttf", None),
    }[name]
    result = TTFont(FONTS / filename)
    if not weight:
        return result
    axes = {"wght": weight}
    if name == "editorial":
        axes.update({"opsz": 32, "wdth": 100})
    return instantiateVariableFont(result, axes)


@lru_cache(maxsize=None)
def glyph(name, character):
    face = font(name)
    key = face.getBestCmap().get(ord(character))
    if key is None:
        raise ValueError(f"Glyph missing: {character!r} in {name}")
    pen = SVGPathPen(face.getGlyphSet())
    face.getGlyphSet()[key].draw(pen)
    outline = pen.getCommands()
    if name == "jp-signature" and character == "ト":
        # Fill the font's inward notch at the diagonal join, only in the header artwork.
        join = "V472L553 536"
        if join not in outline:
            raise ValueError(
                "Revisar la unión de ト tras actualizar la fuente japonesa."
            )
        outline = outline.replace(join, "V568L553 536", 1)
    return outline, face["hmtx"][key][0]


def measure(value, size, face="text"):
    return sum(glyph(face, c)[1] for c in value) * size / font(face)["head"].unitsPerEm


def text(value, x, y, size, color, face="text", max_width=None, opacity=1):
    scale = size / font(face)["head"].unitsPerEm
    position = 0
    paths = []
    for character in value:
        outline, advance = glyph(face, character)
        paths.append(f'<path transform="translate({position} 0)" d="{outline}"/>')
        position += advance
    if max_width:
        scale = min(scale, max_width / max(position, 1))
    return (
        f'<g aria-label="{escape(value)}" fill="{color}" opacity="{opacity}" transform="translate({x} {y}) scale({scale:.7f} {-scale:.7f})">'
        + "".join(paths)
        + "</g>"
    )


def lines(value, x, y, size, color, width, face="text", leading=1.35):
    result = []
    line = ""
    index = 0
    for word in value.split():
        candidate = (line + " " + word).strip()
        if line and measure(candidate, size, face) > width:
            result.append(text(line, x, y + index * size * leading, size, color, face))
            line = word
            index += 1
        else:
            line = candidate
    if line:
        result.append(text(line, x, y + index * size * leading, size, color, face))
    return "".join(result)


def svg_file(path, width, height, body, title, style=""):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title">
<title id="title">{escape(title)}</title>
<style>{style}\n@media(prefers-reduced-motion:reduce){{*{{animation:none!important}}.material-b{{opacity:0!important}}}}</style>
{body}
</svg>"""
    )
