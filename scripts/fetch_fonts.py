"""Download official font sources and their licenses for the artwork builder."""

from pathlib import Path
from urllib.parse import quote
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
SOURCES = {
    "Outfit[wght].ttf": "ofl/outfit/Outfit[wght].ttf",
    "ZenKakuGothicNew-Bold.ttf": "ofl/zenkakugothicnew/ZenKakuGothicNew-Bold.ttf",
    "BricolageGrotesque.ttf": "ofl/bricolagegrotesque/BricolageGrotesque[opsz,wdth,wght].ttf",
}

if __name__ == "__main__":
    cache = ROOT / ".cache/fonts"
    cache.mkdir(parents=True, exist_ok=True)
    for name, source in SOURCES.items():
        base = "https://raw.githubusercontent.com/google/fonts/main/"
        with urlopen(base + quote(source, safe="/"), timeout=40) as response:
            (cache / name).write_bytes(response.read())
        with urlopen(
            base + source.rsplit("/", 1)[0] + "/OFL.txt", timeout=30
        ) as response:
            (
                ROOT / "docs" / (name.split("[")[0].replace(".ttf", "") + "-OFL.txt")
            ).write_bytes(response.read())
        print(f"Descargada: {name}")
