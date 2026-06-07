#!/usr/bin/env python3
"""Convert plain text or markdown into a deck JSON plan."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def clean(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip())


def strip_bullet(line: str) -> str:
    return re.sub(r"^([-*+]|\d+[.)])\s+", "", clean(line))


def heading_from_line(line: str) -> str | None:
    markdown = re.match(r"^(#{1,3})\s+(.+)$", line)
    if markdown:
        return clean(markdown.group(2))
    if line.startswith(("-", "*", "+")) or re.match(r"^\d+[.)]\s+", line):
        return None
    if len(line) <= 70 and not re.search(r"[.!?。！？]$", line):
        return clean(line)
    return None


def sections_from_text(text: str) -> list[tuple[str, list[str]]]:
    sections: list[tuple[str, list[str]]] = []
    section_title = "Key points"
    section_lines: list[str] = []

    for raw in text.splitlines():
        line = clean(raw)
        if not line:
            continue
        heading = heading_from_line(line)
        if heading and section_lines:
            sections.append((section_title, section_lines))
            section_title = heading
            section_lines = []
        elif heading and section_title == "Key points":
            section_title = heading
        else:
            section_lines.append(line)

    if section_lines:
        sections.append((section_title, section_lines))
    return sections


def split_sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?。！？])\s+", text)
    return [clean(part) for part in parts if clean(part)]


def chunks(items: list[str], size: int) -> list[list[str]]:
    return [items[index : index + size] for index in range(0, len(items), size)]


def make_slides(text: str, max_bullets: int) -> list[dict]:
    slides: list[dict] = []
    for section, lines in sections_from_text(text):
        points: list[str] = []
        for line in lines:
            if line.startswith(("-", "*", "+")) or re.match(r"^\d+[.)]\s+", line):
                points.append(strip_bullet(line))
            else:
                points.extend(split_sentences(line))

        points = [point for point in points if point]
        for index, group in enumerate(chunks(points, max_bullets)):
            title = section if index == 0 else f"{section} ({index + 1})"
            slides.append(
                {
                    "section": section.upper()[:28],
                    "title": title[:90],
                    "bullets": group,
                    "notes": "\n".join(group),
                }
            )

    return slides


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", "-o", type=Path, default=Path("deck.json"))
    parser.add_argument("--title", default=None)
    parser.add_argument("--subtitle", default="")
    parser.add_argument("--source", default="Source: user-provided text")
    parser.add_argument("--theme", choices=["light", "dark"], default="light")
    parser.add_argument("--max-bullets", type=int, default=4)
    args = parser.parse_args()

    text = args.input.read_text(encoding="utf-8")
    deck_title = args.title or args.input.stem.replace("-", " ").replace("_", " ").title()
    slides = make_slides(text, max(1, args.max_bullets))
    if not slides:
        fallback = clean(text)
        slides = [{"section": "KEY POINTS", "title": deck_title, "bullets": [fallback[:120]], "notes": fallback}]

    deck = {
        "title": deck_title,
        "subtitle": args.subtitle,
        "theme": args.theme,
        "source": args.source,
        "slides": slides,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(deck, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {args.output} with {len(slides)} content slides")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
