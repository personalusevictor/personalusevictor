"""Cache public GitHub metrics. A failed refresh never overwrites the last snapshot."""

import json
import re
from collections import Counter
from datetime import date, timedelta
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]


class Calendar(HTMLParser):
    def __init__(self):
        super().__init__()
        self.cells = {}
        self.counts = {}
        self.target = None
        self.words = []

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if "data-date" in attrs:
            self.cells[attrs["id"]] = attrs["data-date"]
        if tag == "tool-tip":
            self.target = attrs.get("for")
            self.words = []

    def handle_data(self, text):
        if self.target:
            self.words.append(text)

    def handle_endtag(self, tag):
        if tag == "tool-tip" and self.target:
            words = "".join(self.words).strip()
            match = re.match(r"(No|[\d,]+) contributions? on ", words)
            if match and self.target in self.cells:
                self.counts[self.cells[self.target]] = (
                    0 if match[1] == "No" else int(match[1].replace(",", ""))
                )
            self.target = None


def streaks(days, today):
    run = longest = 0
    start = today - timedelta(days=364)
    for offset in range(365):
        run = (
            run + 1 if days.get((start + timedelta(days=offset)).isoformat(), 0) else 0
        )
        longest = max(longest, run)
    cursor = today if days.get(today.isoformat(), 0) else today - timedelta(days=1)
    current = 0
    while cursor >= start and days.get(cursor.isoformat(), 0):
        current += 1
        cursor -= timedelta(days=1)
    return current, longest


def fetch(url):
    request = Request(
        url, headers={"User-Agent": "personalusevictor-readme", "Accept-Language": "en"}
    )
    with urlopen(request, timeout=30) as response:
        return response.read().decode()


def snapshot(username, today=None):
    today = today or date.today()
    repos = []
    for page in range(1, 101):
        batch = json.loads(
            fetch(
                f"https://api.github.com/users/{username}/repos?type=owner&per_page=100&page={page}"
            )
        )
        if not isinstance(batch, list):
            raise ValueError("GitHub no devolvió una lista de repositorios.")
        repos.extend(batch)
        if len(batch) < 100:
            break
    else:
        raise ValueError("La lista de repositorios supera el límite de paginación.")
    languages = Counter()
    for repo in repos:
        if not repo["fork"]:
            languages.update(json.loads(fetch(repo["languages_url"])))
    start = today - timedelta(days=364)
    calendar = Calendar()
    calendar.feed(fetch(f"https://github.com/users/{username}/contributions"))
    days = {
        key: value
        for key, value in calendar.counts.items()
        if str(start) <= key <= str(today)
    }
    if len(days) != 365:
        raise ValueError(
            f"Calendario incompleto: {len(days)} días. Se conserva la copia anterior."
        )
    current, longest = streaks(days, today)
    return {
        "updated": str(today),
        "public_repositories": len(repos),
        "languages": dict(languages.most_common()),
        "current_streak": current,
        "longest_streak": longest,
        "contributions": sum(days.values()),
        "days": days,
        "period_start": str(start),
    }


if __name__ == "__main__":
    username = json.loads((ROOT / "data/profile.json").read_text())["username"]
    result = snapshot(username)
    destination = ROOT / "data/github-stats.json"
    temporary = destination.with_suffix(".tmp")
    temporary.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    temporary.replace(destination)
    print(f"Estadísticas públicas actualizadas: {result['updated']}.")
