#!/usr/bin/env python3
"""Render exactly one slide PNG from a compact JSON plan."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont


FORMATS = {
    "wide": (1280, 720),
    "square": (1080, 1080),
    "card": (1080, 1350),
}


def font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "/System/Library/Fonts/AppleSDGothicNeo.ttc",
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            try:
                return ImageFont.truetype(path, size=size, index=0)
            except Exception:
                continue
    return ImageFont.load_default()


def wrap(draw: ImageDraw.ImageDraw, text: str, face: ImageFont.ImageFont, max_width: int, max_lines: int) -> list[str]:
    korean = bool(re.search(r"[\u3131-\ud7a3]", text))
    units = list(text) if korean else text.split()
    sep = "" if korean else " "
    lines: list[str] = []
    current = ""
    for unit in units:
        trial = f"{current}{sep if current else ''}{unit}"
        if draw.textlength(trial, font=face) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = unit
    if current:
        lines.append(current)
    return lines[:max_lines]


def draw_lines(draw: ImageDraw.ImageDraw, x: int, y: int, lines: list[str], face: ImageFont.ImageFont, fill: str, gap: int) -> int:
    for line in lines:
        draw.text((x, y), line, font=face, fill=fill)
        box = draw.textbbox((x, y), line, font=face)
        y += box[3] - box[1] + gap
    return y


def render(slide: dict[str, Any], size: tuple[int, int]) -> Image.Image:
    w, h = size
    image = Image.new("RGB", size, "#F7F8FA")
    draw = ImageDraw.Draw(image)

    ink = "#111827"
    muted = "#5F6673"
    accent = str(slide.get("accent") or "#C0392B")
    track = "#E4E7EC"

    px = int(w * 0.075)
    py = int(h * 0.105)
    content_w = int(w * 0.72)

    eyebrow_font = font(max(15, int(w * 0.016)))
    title_font = font(max(34, int(w * 0.048)))
    metric_font = font(max(62, int(w * 0.118)))
    body_font = font(max(20, int(w * 0.026)))
    point_font = font(max(18, int(w * 0.023)))
    footer_font = font(max(12, int(w * 0.014)))

    draw.rectangle((px, int(py * 0.7), px + int(w * 0.075), int(py * 0.7) + max(5, int(h * 0.008))), fill=accent)

    eyebrow = str(slide.get("eyebrow") or "One-slide brief").upper()
    draw.text((px, py), eyebrow, font=eyebrow_font, fill=accent)

    title_lines = wrap(draw, str(slide.get("title") or "Untitled slide"), title_font, content_w, 2)
    y = draw_lines(draw, px, int(py * 1.45), title_lines, title_font, ink, int(h * 0.018))

    metric = str(slide.get("metric") or "").strip()
    if metric:
        y += int(h * 0.035)
        draw.text((px, y), metric, font=metric_font, fill=accent)
        y += int(h * 0.15)

    body = str(slide.get("body") or "")
    if body:
        y += int(h * 0.02)
        y = draw_lines(draw, px, y, wrap(draw, body, body_font, content_w, 2), body_font, muted, int(h * 0.014))

    points = [str(point) for point in slide.get("points", [])][:4]
    if points:
        y += int(h * 0.045)
        chip_h = max(32, int(h * 0.06))
        for point in points:
            draw.rounded_rectangle((px, y, px + int(w * 0.58), y + chip_h), radius=6, fill="#FFFFFF", outline=track, width=1)
            draw.ellipse((px + 16, y + chip_h // 2 - 4, px + 24, y + chip_h // 2 + 4), fill=accent)
            draw.text((px + 40, y + int(chip_h * 0.24)), point, font=point_font, fill=ink)
            y += chip_h + int(h * 0.014)

    footer = str(slide.get("footer") or "text-to-one-slide")
    draw.text((px, h - int(h * 0.07)), footer, font=footer_font, fill=muted)
    draw.text((w - int(w * 0.18), h - int(h * 0.07)), "1 / 1", font=footer_font, fill=muted)
    return image


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", "-o", type=Path, default=Path("one-slide.png"))
    parser.add_argument("--format", choices=FORMATS.keys(), default="wide")
    args = parser.parse_args()

    slide = json.loads(args.input.read_text(encoding="utf-8"))
    image = render(slide, FORMATS[args.format])
    args.output.parent.mkdir(parents=True, exist_ok=True)
    image.save(args.output)
    print(f"Wrote {args.output} at {image.size[0]}x{image.size[1]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
