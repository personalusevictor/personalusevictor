"""Compose the final profile and its section artwork."""

import json
from xml.etree import ElementTree as ET
from pathlib import Path

from art import measure, svg_file, text, lines
from markdown_art import THEME
from svg_assets import image

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets/profile/sections"


def artwork(stats):
    label = "En construcción"
    end = measure(label, 30, "editorial")
    body = text(label, 1, 41, 30, "var(--ink)", "editorial")
    body += f'<g transform="translate({end+13:.3f} 21.8) scale(1.2)" fill="none" stroke="var(--three)" stroke-width="1.275" stroke-linecap="round" stroke-linejoin="round"><path d="M0 15V2h18v13H0ZM0 6h18M5 2v4"/><path d="m6 9-2 2 2 2m6-4 2 2-2 2"/></g>'
    svg_file(OUTPUT / "work-title.svg", round(end + 49), 57, body, label, THEME)
    body = ""
    labels = [
        ("Repositorios públicos", stats["public_repositories"], ""),
        ("Contribuciones · 365 días", stats["contributions"], ""),
        ("Racha actual", stats["current_streak"], "días"),
        ("Mejor racha · 365 días", stats["longest_streak"], "días"),
    ]
    for i, (label, value, unit) in enumerate(labels):
        body = ""
        x = 0
        body += text(str(value), x, 45, 36, "var(--ink)", "editorial")
        if unit:
            unit = "día" if value == 1 else unit
            body += text(
                unit,
                x + measure(str(value), 36, "editorial") + 6,
                45,
                13,
                "var(--muted)",
            )
        body += text(label, x, 72, 12, "var(--muted)")
        svg_file(
            OUTPUT / f"activity-{i}.svg",
            180,
            89,
            body,
            f"{value} {label}",
            THEME,
        )


def introduction(profile):
    for mobile in (False, True):
        width, height = (400, 164) if mobile else (840, 124)
        left = 58 if mobile else 72
        body = image(
            "assets/profile/memoji.png",
            0,
            60 if mobile else 26,
            44 if mobile else 56,
            44 if mobile else 56,
        )
        body += text(
            "¡Hola! Soy Víctor.",
            left,
            31,
            21 if mobile else 22,
            "var(--ink)",
            "editorial",
        )
        bio = "Estudiante de segundo del Grado Superior de Desarrollo de Aplicaciones Web en La Palma, Canarias. Me gusta aprender construyendo proyectos, probando herramientas, investigando, diseñando y resolviendo problemas."
        body += lines(
            bio,
            left,
            62,
            14.5,
            "var(--ink)",
            width - left - 2,
            face="regular",
            leading=1.4,
        )
        body = '<g transform="translate(0 28)">' + body + "</g>"
        svg_file(
            OUTPUT / ("intro-mobile.svg" if mobile else "intro.svg"),
            width,
            height + 28,
            body,
            profile["introduction"].replace("**", ""),
            THEME,
        )


def project_cards():
    projects = json.loads((ROOT / "data/projects.json").read_text())["projects"]
    for project in projects:
        slug, name = project["id"], project["title"]
        description, detail = project["description"], project["detail"]
        technologies = " / ".join(project["technologies"])
        body = (
            '<rect x=".5" y=".5" width="269" height="319" rx="10" fill="var(--paper)"/>'
        )
        body += '<defs><clipPath id="card-cover"><rect x="0" y="0" width="270" height="320" rx="10"/></clipPath></defs><g clip-path="url(#card-cover)">'
        if slug == "vcode":
            body += '<defs><clipPath id="cover"><rect x="0" y="0" width="270" height="143" rx="0"/></clipPath></defs><g clip-path="url(#cover)">'
            body += (
                image("assets/work/vcode.jpg", 0, 0, 270, 143, "xMidYMid slice")
                + "</g>"
            )
        elif slug == "vtechshop":
            body += '<rect x="0" y="0" width="270" height="143" rx="0" fill="#EEE6DB"/>'
            body += image(
                "assets/profile/sections/sources/vtechshop.svg", 99, 35.5, 72, 72
            )
        else:
            body += '<rect x="0" y="0" width="270" height="143" rx="0" fill="var(--empty)"/><g fill="none" stroke="var(--muted)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="102" y="48" width="66" height="44" rx="3"/><path d="M122 105h26m-13-13v13m-9-43-8 8 8 8m18-16 8 8-8 8"/></g>'
        body += "</g>"
        body += text(
            name, 17, 174, 18 if slug != "department" else 16, "var(--ink)", "editorial"
        )
        body += lines(description, 17, 201, 13, "var(--muted)", 235, leading=1.4)
        body += lines(detail, 17, 250, 12, "var(--muted)", 235, leading=1.4)
        body += '<path d="M17 281h236" stroke="var(--line)"/>'
        body += text(technologies, 17, 303, 10.5, "var(--muted)")
        svg_file(
            OUTPUT / f"project-{slug}.svg",
            270,
            320,
            body,
            f"{name}. En desarrollo. {description} {detail} {technologies}",
            THEME,
        )
        card = ET.parse(OUTPUT / f"project-{slug}.svg")
        card.getroot().set("width", "294")
        card.getroot().set("height", str(324 * 294 / 281))
        card.getroot().set("viewBox", "-5.5 0 281 324")
        ET.register_namespace("", "http://www.w3.org/2000/svg")
        card.write(OUTPUT / f"project-{slug}.svg", encoding="utf-8")


def charts():
    source = ET.parse(ROOT / "assets/profile/github-activity.svg").getroot()
    ns = {"s": "http://www.w3.org/2000/svg"}
    extra = float(source.get("height")) - 258
    for name, viewbox, height in [
        ("languages", f"0 0 480 {112 + extra:g}", round((112 + extra) * 420 / 480)),
        ("calendar", f"0 {116 + extra:g} 480 142", 125),
    ]:
        # Separate viewports retain the original data and accessible day descriptions.
        tree = ET.fromstring(ET.tostring(source))
        tree.set("viewBox", viewbox)
        tree.set("width", "420")
        tree.set("height", str(height))
        tree.set("overflow", "hidden")
        tree.find("s:title", ns).text = (
            "Código público por lenguaje"
            if name == "languages"
            else "Calendario de contribuciones de los últimos 365 días"
        )
        if name == "languages":
            tree.find(".//s:clipPath/s:rect", ns).set("rx", "5.7")
        if name == "languages":
            nodes = list(tree)
            divider = next(
                i
                for i, node in enumerate(nodes)
                if node.tag.endswith("path")
                and node.get("d") == f"M0 {111 + extra:g}H480"
            )
            for node in nodes[divider:]:
                tree.remove(node)
        ET.register_namespace("", ns["s"])
        (OUTPUT / f"{name}.svg").write_bytes(ET.tostring(tree, encoding="utf-8"))


def contact_artwork():
    label = "Contacto"
    end = 1 + measure(label, 30, "editorial")
    body = text(label, 1, 41, 30, "var(--ink)", "editorial")
    source = ET.parse(ROOT / "assets/profile/icons/share-2.svg").getroot()
    drawing = "".join(ET.tostring(node, encoding="unicode") for node in source)
    notice = (ROOT / "docs/Lucide-LICENSE.txt").read_text().split("\n---", 1)[0]
    body += "<!--\n" + notice + "\n-->"
    body += f'<g transform="translate({end+9:.3f} 19.6) scale(1.1)" fill="none" stroke="var(--three)" stroke-width="1.391" stroke-linecap="round" stroke-linejoin="round">{drawing}</g>'
    svg_file(OUTPUT / "contact-title.svg", round(end + 48), 57, body, label, THEME)
    mail = '<g fill="none" stroke="var(--ink)" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><rect x="1" y="4" width="22" height="16" rx="2.5"/><path d="m2 6 10 7 10-7"/></g>'
    svg_file(OUTPUT / "email-icon.svg", 24, 24, mail, "Correo", THEME)
    logo = ET.parse(ROOT / "assets/profile/social/x.svg").getroot()
    path = logo.find("{http://www.w3.org/2000/svg}path").get("d")
    svg_file(
        OUTPUT / "x-icon.svg",
        24,
        24,
        f'<g transform="translate(.25 0) scale(.0195)" fill="var(--ink)"><path d="{path}"/></g>',
        "X",
        THEME,
    )
    body = '<g fill="none" stroke="var(--three)" stroke-width="1.5" stroke-linecap="round"><path d="M3 2v16h15M7 14V9m5 5V5m5 9V2"/></g>'
    svg_file(
        OUTPUT / "details-icon.svg", 20, 22, body, "Estadísticas detalladas", THEME
    )


def project_links():
    projects = json.loads((ROOT / "data/projects.json").read_text())["projects"]
    links = []
    for project in projects:
        image_link = f'![{project["title"]}: {project["description"]}](assets/profile/sections/project-{project["id"]}.svg)'
        links.append(
            f'[{image_link}]({project["repository"]})'
            if project["repository"]
            else image_link
        )
    return " ".join(links)


def render(profile, stats, header, technologies):
    artwork(stats)
    introduction(profile)
    project_cards()
    charts()
    contact_artwork()
    sections = [
        header,
        '<picture>\n  <source media="(max-width:600px)" srcset="assets/profile/sections/intro-mobile.svg">\n  <img src="assets/profile/sections/intro.svg" width="100%" alt="'
        + profile["introduction"].replace("**", "")
        + '">\n</picture>',
        "### ![En construcción](assets/profile/sections/work-title.svg)",
        project_links(),
        "### ![Tecnologías]" + technologies,
        "### ![GitHub](assets/profile/titles/github.svg)",
        " ".join(
            f"![{label}](assets/profile/sections/activity-{i}.svg)"
            for i, label in enumerate(
                [
                    "Repositorios públicos",
                    "Contribuciones del último año",
                    "Racha actual",
                    "Mejor racha del último año",
                ]
            )
        ),
        '<br>\n\n<details>\n<summary><picture><img src="assets/profile/sections/details-icon.svg" width="20" height="22" align="absmiddle" alt=""></picture> &nbsp; <strong>Lenguajes y contribuciones</strong></summary>\n\n<br>\n\n![Código público por lenguaje.](assets/profile/sections/languages.svg)\n\n![Calendario de contribuciones de los últimos 365 días.](assets/profile/sections/calendar.svg)\n\n<br>\n\n</details>',
        "### ![Contacto](assets/profile/sections/contact-title.svg)",
        f'<a href="mailto:{profile["email"]}"><img src="assets/profile/sections/email-icon.svg" width="24" height="24" align="absmiddle" alt="">&nbsp;{profile["email"]}</a>',
        f'<a href="{profile["social"]}"><img src="assets/profile/sections/x-icon.svg" width="24" height="24" align="absmiddle" alt="">&nbsp;@personaluvictor</a>',
    ]
    return "\n\n".join(sections) + "\n"
