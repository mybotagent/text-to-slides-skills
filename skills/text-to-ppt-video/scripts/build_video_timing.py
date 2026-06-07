#!/usr/bin/env python3
"""Build page-to-script timing JSON from scene JSON and Whisper segments."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", str(text or "").strip())


def read_segments(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict) and isinstance(data.get("segments"), list):
        return data["segments"]
    if isinstance(data, list):
        return data
    raise SystemExit("Whisper JSON must contain a segments array")


def choose_segment_index(segments: list[dict[str, Any]], target_seconds: float, minimum_index: int, maximum_index: int) -> int:
    start = max(0, minimum_index)
    end = max(start, min(maximum_index, len(segments) - 1))
    for index in range(start, end + 1):
        if float(segments[index].get("end", 0)) >= target_seconds:
            return index
    return end


def build_timing(scenes: list[dict[str, Any]], segments: list[dict[str, Any]], hold_ms: int, min_scene_ms: int) -> list[dict[str, Any]]:
    if not scenes:
        raise SystemExit("No scenes found")
    if not segments:
        raise SystemExit("No Whisper segments found")

    total_seconds = max(float(segment.get("end", 0)) for segment in segments)
    script_lengths = [max(1, len(normalize(scene.get("script") or scene.get("notes") or scene.get("body") or scene.get("title")))) for scene in scenes]
    total_script = sum(script_lengths)

    timing: list[dict[str, Any]] = []
    start_ms = 0
    previous_segment_index = 0
    cumulative = 0

    for index, scene in enumerate(scenes, start=1):
        cumulative += script_lengths[index - 1]
        if index == len(scenes):
            end_segment_index = len(segments) - 1
        else:
            target_seconds = total_seconds * (cumulative / total_script)
            remaining_scenes = len(scenes) - index
            maximum_index = len(segments) - remaining_scenes - 1
            end_segment_index = choose_segment_index(segments, target_seconds, previous_segment_index, maximum_index)

        raw_end_ms = int(round(float(segments[end_segment_index].get("end", 0)) * 1000)) + hold_ms
        end_ms = max(start_ms + min_scene_ms, raw_end_ms)

        timing.append(
            {
                "page": scene.get("page", index),
                "startMs": start_ms,
                "endMs": end_ms,
                "durationMs": end_ms - start_ms,
                "title": scene.get("title", ""),
                "script": scene.get("script") or scene.get("notes") or "",
                "segmentStart": previous_segment_index,
                "segmentEnd": end_segment_index,
            }
        )
        start_ms = end_ms
        previous_segment_index = min(end_segment_index + 1, len(segments) - 1)

    return timing


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scenes_json", type=Path)
    parser.add_argument("whisper_json", type=Path)
    parser.add_argument("--output", "-o", type=Path, required=True)
    parser.add_argument("--hold-ms", type=int, default=350)
    parser.add_argument("--min-scene-ms", type=int, default=1200)
    args = parser.parse_args()

    deck = json.loads(args.scenes_json.read_text(encoding="utf-8"))
    scenes = deck.get("scenes") or deck.get("slides") or []
    segments = read_segments(args.whisper_json)
    timing = build_timing(scenes, segments, max(0, args.hold_ms), max(500, args.min_scene_ms))

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps({"title": deck.get("title", ""), "timing": timing}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {args.output} with {len(timing)} timing rows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
