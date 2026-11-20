"""Validate the delivered profile, including links and calendar geometry."""

import json
import re
import unittest
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SVG = {"s": "http://www.w3.org/2000/svg"}


class ProfileHTML(HTMLParser):
    def __init__(self, content):
        super().__init__()
        self.images, self.sources, self.links = [], [], []
        self.feed(content)
        self.images.extend(
            {"alt": alt, "src": src}
            for alt, src in re.findall(r"!\[([^\]]*)\]\(([^)]+)\)", content)
        )
        self.links.extend(re.findall(r"(?<!!)\[(?!!)[^\]]+\]\(([^)]+)\)", content))
        self.links.extend(re.findall(r"\[!\[[^\]]*\]\([^)]+\)\]\(([^)]+)\)", content))

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == "img":
            self.images.append(values)
        elif tag == "source":
            self.sources.append(values)
        elif tag == "a" and "href" in values:
            self.links.append(values["href"])


class ProfileAssetsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.markdown = (ROOT / "README.md").read_text()
        cls.html = ProfileHTML(cls.markdown)
        cls.profile = json.loads((ROOT / "data/profile.json").read_text())
        cls.stats = json.loads((ROOT / "data/github-stats.json").read_text())

    def test_every_picture_resolves_and_has_accessible_text(self):
        self.assertGreaterEqual(len(self.html.images), 5)
        for image in self.html.images:
            decorative = image["src"] in {
                "assets/profile/sections/email-icon.svg",
                "assets/profile/sections/x-icon.svg",
                "assets/profile/sections/details-icon.svg",
            }
            self.assertTrue(decorative or image.get("alt", "").strip())
            self.assertTrue((ROOT / image["src"]).is_file(), image["src"])
        for source in self.html.sources:
            self.assertTrue((ROOT / source["srcset"]).is_file(), source["srcset"])

    def test_calendar_has_exactly_the_cached_days_and_fits_its_canvas(self):
        for file in [ROOT / "assets/profile/github-activity.svg"]:
            with self.subTest(file=file.name):
                root = ET.parse(file).getroot()
                _, _, width, height = map(float, root.get("viewBox").split())
                delivered = {}
                for rect in root.findall(".//s:rect", SVG):
                    title = rect.find("s:title", SVG)
                    if title is None:
                        continue
                    day, amount = title.text.split(": ", 1)
                    self.assertNotIn(day, delivered)
                    delivered[day] = int(amount.split()[0])
                    x, y = float(rect.get("x")), float(rect.get("y"))
                    w, h = float(rect.get("width")), float(rect.get("height"))
                    self.assertGreaterEqual(x, 0)
                    self.assertGreaterEqual(y, 0)
                    self.assertGreater(w, 0)
                    self.assertGreater(h, 0)
                    self.assertLessEqual(x + w, width + 0.01)
                    self.assertLessEqual(y + h, height + 0.01)
                self.assertEqual(len(delivered), 365)
                self.assertEqual(delivered, self.stats["days"])
                self.assertEqual(sum(delivered.values()), self.stats["contributions"])

    def test_artwork_has_no_scripts_or_remote_image_dependencies(self):
        for file in (ROOT / "assets/profile").glob("*.svg"):
            with self.subTest(file=file.name):
                root = ET.parse(file).getroot()
                self.assertIsNotNone(root.find("s:title", SVG))
                self.assertFalse(root.findall(".//s:script", SVG))
                self.assertFalse(root.findall(".//s:foreignObject", SVG))
                for image in root.findall(".//s:image", SVG):
                    self.assertTrue(image.get("href", "").startswith("data:image/"))

    def test_technology_labels_match_the_profile(self):
        declared = {
            item for group in self.profile["technologies"].values() for item in group
        }
        marks = [image for image in self.html.images if "/marks/" in image["src"]]
        labels = set()
        for mark in marks:
            root = ET.parse(ROOT / mark["src"]).getroot()
            title = root.find("s:title", SVG).text
            labels.add(title)
            self.assertTrue(mark["alt"].startswith(title))
        self.assertEqual(labels, declared)
        self.assertEqual(len(marks), len(declared))

    def test_metric_figures_use_the_verified_snapshot(self):
        numbers = Counter()
        for index in range(4):
            root = ET.parse(
                ROOT / f"assets/profile/sections/activity-{index}.svg"
            ).getroot()
            numbers.update(
                node.get("aria-label")
                for node in root.iter()
                if node.get("aria-label", "").isdecimal()
            )
        expected = Counter(
            str(self.stats[key])
            for key in (
                "public_repositories",
                "contributions",
                "current_streak",
                "longest_streak",
            )
        )
        self.assertEqual(numbers, expected)

    def test_body_is_native_markdown_and_keeps_the_agreed_content(self):
        body = self.markdown.split("</picture>", 1)[1]
        self.assertNotRegex(body, r"<(?:script|style|iframe)\b|\bon\w+=")
        self.assertIn(self.profile["introduction"].replace("**", ""), body)
        self.assertNotIn("## Proyectos", body)
        self.assertNotIn("[Sobre mí](", body)
        self.assertNotIn("En clase y en mis prácticas", body)
        self.assertNotIn("También he trabajado con", body)
        self.assertNotIn("quiero profundizar", body)
        self.assertNotIn("| Actividad |", body)

    def test_project_visibility_and_contact_links_are_real(self):
        projects = json.loads((ROOT / "data/projects.json").read_text())["projects"]
        for project in projects:
            self.assertIn(
                f'assets/profile/sections/project-{project["id"]}.svg', self.markdown
            )
            if project["repository"]:
                self.assertIn(project["repository"], self.html.links)
        self.assertNotIn("https://github.com/personalusevictor/VCode", self.markdown)
        self.assertIn("mailto:" + self.profile["email"], self.html.links)
        self.assertIn(self.profile["social"], self.markdown)
        self.assertNotIn("1 días", self.markdown)
        for href, label in [
            ("mailto:" + self.profile["email"], self.profile["email"]),
            (self.profile["social"], "@personaluvictor"),
        ]:
            anchor = re.search(
                r'<a href="' + re.escape(href) + r'">(.*?)</a>', self.markdown, re.S
            )
            self.assertIsNotNone(
                anchor,
                "El contacto debe ser texto enlazado real para admitir subrayado en hover.",
            )
            self.assertIn(label, re.sub(r"<[^>]+>", "", anchor.group(1)))

    def test_navigation_targets_exist(self):
        headings = {
            line[3:].strip().lower().replace(" ", "-")
            for line in self.markdown.splitlines()
            if line.startswith("## ")
        }
        for href in self.html.links:
            if href.startswith("#"):
                self.assertIn(href[1:], headings)


if __name__ == "__main__":
    unittest.main()
