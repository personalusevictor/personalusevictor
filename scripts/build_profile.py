"""Generate a Markdown-first profile while preserving the approved animated header."""

import json
from pathlib import Path

from markdown_art import ICONS, activity_chart, marks, titles
from signature import banner, identity_assets
from profile_layout import render as render_layout

ROOT = Path(__file__).resolve().parents[1]


def header():
    return """<picture>
  <source media="(max-width:600px) and (prefers-color-scheme:dark)" srcset="assets/profile/header-mobile-dark.svg">
  <source media="(max-width:600px)" srcset="assets/profile/header-mobile-light.svg">
  <source media="(prefers-color-scheme:dark)" srcset="assets/profile/header-dark.svg">
  <img src="assets/profile/header-light.svg" width="100%" alt="Firma personalusevictor, con su kitsune animado y los nombres japoneses detrás.">
</picture>"""


def logo_row(names):
    return " ".join(
        f"![{name}](assets/profile/marks/{ICONS[name]}.svg)" for name in names
    )


def render(profile, stats):
    available = {name for group in profile["technologies"].values() for name in group}
    order = [
        "HTML",
        "CSS",
        "JavaScript",
        "TypeScript",
        "React",
        "Tailwind CSS",
        "PHP",
        "Java",
        "C++",
        "Astro",
    ]
    names = [name for name in order if name in available]
    technologies = "(assets/profile/titles/technologies.svg)\n\n" + logo_row(names)
    return render_layout(profile, stats, header(), technologies)


def build():
    profile = json.loads((ROOT / "data/profile.json").read_text())
    stats = json.loads((ROOT / "data/github-stats.json").read_text())
    for theme in ("light", "dark"):
        for mobile in (False, True):
            banner(theme, mobile)
    identity_assets()
    titles()
    marks(profile)
    activity_chart(stats)
    (ROOT / "README.md").write_text(render(profile, stats))
    print("README final y recursos generados.")


if __name__ == "__main__":
    build()
