"""Small images for a Markdown-first profile: logos, data charts and Memoji."""

from datetime import date, timedelta
from math import ceil
from xml.etree import ElementTree as ET

from art import measure, svg_file, text
from svg_assets import OUTPUT, ROOT, image

ICONS = {
    "HTML": "html",
    "CSS": "css",
    "JavaScript": "javascript",
    "Tailwind CSS": "tailwind",
    "PHP": "php",
    "Java": "java",
    "React": "react",
    "TypeScript": "typescript",
    "C++": "cpp",
    "Astro": "astro",
}
THEME = """:root{--paper:#F3EFE7;--ink:#382D26;--line:#DACEBE;--muted:#796956;--empty:#E3D8C8;--one:#C4AE93;--two:#A48768;--three:#806347;--four:#5E4733}.mark-dark{display:none}@media(prefers-color-scheme:dark){:root{--paper:#211E1B;--ink:#EDE3D4;--line:#4A3E32;--muted:#C0AE97;--empty:#3E3329;--one:#70573F;--two:#98734F;--three:#C39A6D;--four:#EAD0AB}.mark-light{display:none}.mark-dark{display:inline}}"""


def titles():
    symbols = [
        (
            "technologies",
            "Tecnologías",
            '<path d="M12 10C10 12 6 15 4 18C6 21 10 24 12 26M20 8L16 28M24 10C26 12 30 15 32 18C30 21 26 24 24 26"/>',
        ),
        (
            "github",
            "GitHub",
            '<path d="M10 6C10 12 10 22 10 30M10 24C10 16 26 22 26 8"/><g fill="var(--paper)"><circle cx="10" cy="6" r="2.6"/><circle cx="10" cy="30" r="2.6"/><circle cx="26" cy="8" r="2.6"/></g>',
        ),
    ]
    icon_layout = {
        "technologies": (15.8, 0.85, 4),
        "github": (15.6, 0.85, 7.4),
    }
    for slug, label, drawing in symbols:
        end = 1 + measure(label, 30, "editorial")
        body = text(label, 1, 41, 30, "var(--ink)", "editorial")
        top, scale, left = icon_layout[slug]
        x = end + 12 - left * scale
        body += f'<g transform="translate({x:.4f} {top}) scale({scale})" fill="none" stroke="var(--three)" stroke-width="{1.53/scale:.4f}" stroke-linecap="round" stroke-linejoin="round">{drawing}</g>'
        svg_file(
            OUTPUT / "titles" / f"{slug}.svg", ceil(end + 47), 57, body, label, THEME
        )


def marks(profile):
    for members in profile["technologies"].values():
        for name in members:
            slug = ICONS[name]
            body = '<defs><filter id="lift" x="-40%" y="-40%" width="180%" height="200%"><feDropShadow dx="0" dy="2" stdDeviation=".8" flood-color="#8B694C" flood-opacity=".12"/></filter></defs><g filter="url(#lift)">'
            icon = f"assets/profile/tech/{slug}.svg"
            icon_y = 13 if slug == "astro" else 8
            if slug == "astro":
                body += (
                    '<g class="mark-light">' + image(icon, 22, icon_y, 34, 34) + "</g>"
                )
                body += (
                    '<g class="mark-dark">'
                    + image(icon, 22, icon_y, 34, 34, theme="dark")
                    + "</g>"
                )
            else:
                body += image(icon, 22, icon_y, 34, 34)
            body += "</g>"
            body += text(name, (78 - measure(name, 11.5)) / 2, 62, 11.5, "var(--ink)")
            svg_file(OUTPUT / "marks" / f"{slug}.svg", 78, 88, body, name, THEME)


def activity_chart(stats):
    languages = list(stats["languages"].items())
    rows = ceil(len(languages) / 2)
    extra = max(0, rows - 2) * 24
    body = text("Código público", 0, 27, 16, "var(--ink)", "editorial")
    total = sum(amount for _, amount in languages)
    light_ramp = ["#67432D", "#A16C46", "#CCA16E", "#E9D6B5"]
    dark_ramp = ["#9C6B46", "#C19569", "#DFC09A", "#F0E1CB"]

    def shade(ramp, position):
        spot = position * (len(ramp) - 1)
        left = min(int(spot), len(ramp) - 2)
        weight = spot - left
        a, b = ramp[left], ramp[left + 1]
        return "#" + "".join(
            f"{round(int(a[channel:channel+2], 16) * (1-weight) + int(b[channel:channel+2], 16) * weight):02x}"
            for channel in (1, 3, 5)
        )

    colors = [f"var(--language-{index})" for index in range(len(languages))]
    positions = [index / max(1, len(languages) - 1) for index in range(len(languages))]
    language_style = (
        ":root{"
        + "".join(
            f"--language-{index}:{shade(light_ramp, position)};"
            for index, position in enumerate(positions)
        )
        + "}@media(prefers-color-scheme:dark){:root{"
        + "".join(
            f"--language-{index}:{shade(dark_ramp, position)};"
            for index, position in enumerate(positions)
        )
        + "}}"
    )
    if total:
        body += '<defs><clipPath id="language-bar"><rect x="18" y="40" width="444" height="12" rx="3"/></clipPath><linearGradient id="language-sheen" x1="0" y1="0" x2="0" y2="1"><stop stop-color="white" stop-opacity=".14"/><stop offset="1" stop-color="white" stop-opacity="0"/></linearGradient></defs>'
        body += '<g clip-path="url(#language-bar)">'
        cursor = 18
        widths = [444 * amount / total for _, amount in languages]
        for index, ((name, amount), w) in enumerate(zip(languages, widths)):
            color = colors[index]
            body += f'<rect x="{cursor:.4f}" y="40" width="{w:.4f}" height="12" fill="{color}"/>'
            cursor += w
            if index < len(widths) - 1:
                separator = 1 if min(w, widths[index + 1]) >= 3 else 0.15
                body += f'<path d="M{cursor:.4f} 40v12" stroke="var(--paper)" stroke-width="{separator}"/>'
        body += '<rect x="18" y="40" width="444" height="12" fill="url(#language-sheen)"/></g>'
        for index, (name, amount) in enumerate(languages):
            color = colors[index]
            x, y = 18 + (index % 2) * 225, 72 + (index // 2) * 24
            body += f'<circle cx="{x+3}" cy="{y-4}" r="3.5" fill="{color}"/>'
            body += text(
                f"{name} · {100*amount/total:.1f}%", x + 15, y, 12, "var(--muted)"
            )
    else:
        body += text("Todavía no hay datos públicos.", 18, 72, 12, "var(--muted)")
    cy = 128 + extra
    body += f'<path d="M0 {111 + extra}H480" stroke="var(--line)" opacity=".65"/>'
    body += text(
        "Contribuciones · últimos 365 días", 0, cy, 15, "var(--ink)", "editorial"
    )
    start = date.fromisoformat(stats["period_start"])
    step = 444 / 53
    months = [
        "ene",
        "feb",
        "mar",
        "abr",
        "may",
        "jun",
        "jul",
        "ago",
        "sep",
        "oct",
        "nov",
        "dic",
    ]
    tones = ["empty", "one", "two", "three", "four"]
    for offset in range(365):
        day = start + timedelta(days=offset)
        index = offset + start.weekday()
        col, row = index // 7, index % 7
        if day.day == 1:
            body += text(
                months[day.month - 1], 18 + col * step, cy + 23, 9, "var(--muted)"
            )
        amount = stats["days"].get(str(day), 0)
        level = min(4, 1 + (amount > 3) + (amount > 7) + (amount > 12)) if amount else 0
        body += f'<rect x="{18+col*step:.4f}" y="{cy+35+row*step:.4f}" width="{step-1.5:.4f}" height="{step-1.5:.4f}" rx="1.1" fill="var(--{tones[level]})"><title>{day}: {amount} contribuciones</title></rect>'
    body += text("Menos", 18, 243 + extra, 10, "var(--muted)")
    for index, tone in enumerate(tones):
        body += f'<rect x="{55+index*11}" y="{235+extra}" width="8" height="8" rx="1.2" fill="var(--{tone})"/>'
    body += text("Más", 114, 243 + extra, 10, "var(--muted)")
    svg_file(
        OUTPUT / "github-activity.svg",
        480,
        258 + extra,
        body,
        "Distribución de lenguajes por bytes de código público propio y calendario de contribuciones visibles. Datos del "
        + stats["updated"]
        + ".",
        THEME + language_style,
    )
