#!/usr/bin/env python3
"""Generate a conceptual Denver metro transit map summary."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class Corridor:
    direction: str
    routes: str
    areas: str


@dataclass(frozen=True)
class Improvement:
    title: str
    rationale: str


CORRIDORS = [
    Corridor("North/Northwest", "US-36", "Westminster, Broomfield, Boulder"),
    Corridor(
        "Northeast",
        "I-70 + Peña Boulevard",
        "Commerce City, Aurora, Denver International Airport (DIA)",
    ),
    Corridor(
        "East/Southeast",
        "I-225 + I-70/I-76 connectors",
        "Aurora and eastern suburbs",
    ),
    Corridor(
        "South/Southwest",
        "I-25 + Santa Fe",
        "Englewood, Littleton, Highlands Ranch",
    ),
    Corridor("West", "US-6 + I-70", "Lakewood, Golden, mountain access points"),
]

LAYERS = [
    "Urban core: Union Station, Civic Center, Capitol, and major job centers",
    "Existing rail lines: light rail and commuter rail branches",
    "Bus trunk routes: east-west and north-south frequent service corridors",
    "Suburban activity centers: Aurora Medical Campus, Tech Center, Lakewood, Boulder corridor nodes",
    "Regional gateways: DIA, intercity rail/bus terminals, park-and-ride hubs",
]

IMPROVEMENTS = [
    Improvement(
        "Build stronger east-west rail connections",
        "Reduces forced downtown transfers and improves crosstown trips.",
    ),
    Improvement(
        "Increase frequency on existing lines",
        '5-10 minute all-day service creates a "show up and go" rider experience.',
    ),
    Improvement(
        "Add infill stations in dense mixed-use areas",
        "Improves access and supports transit-oriented development without building full new corridors.",
    ),
    Improvement(
        "Expand commuter/regional rail to major suburban nodes",
        "Connects Boulder-area jobs, southeast office districts, and growing north metro communities.",
    ),
    Improvement(
        "Improve airport and late-night service",
        "Better serves workers and travelers outside classic peak commute windows.",
    ),
    Improvement(
        "Design seamless transfers",
        "Timed transfer hubs help rail, frequent buses, and micromobility function as one network.",
    ),
    Improvement(
        "Pair rail with transit-priority streets",
        "Bus lanes, safer crossings, and protected bike lanes improve station access.",
    ),
]

MAP_UPGRADE = [
    "Frequent Network Layer: routes every 10-15 minutes or better",
    "Regional Rail Layer: airport + commuter services with travel times",
    "Transfer Hub Symbols: highlighted interchanges with walking-transfer times",
    "Growth Overlay: planned housing/jobs to prioritize future train lines",
]


def build_payload() -> dict:
    return {
        "title": "Denver Metro Area Map (Conceptual Overview)",
        "corridors": [asdict(c) for c in CORRIDORS],
        "transit_layers": LAYERS,
        "improvements": [asdict(i) for i in IMPROVEMENTS],
        "map_upgrade": MAP_UPGRADE,
    }


def render_text(payload: dict) -> str:
    lines: list[str] = []
    lines.append(payload["title"])
    lines.append("=" * len(payload["title"]))
    lines.append("\nMajor corridors")
    for corridor in payload["corridors"]:
        lines.append(
            f"- {corridor['direction']}: {corridor['routes']} -> {corridor['areas']}"
        )

    lines.append("\nTransit map layers")
    for layer in payload["transit_layers"]:
        lines.append(f"- {layer}")

    lines.append("\nTrain expansion priorities")
    for idx, improvement in enumerate(payload["improvements"], start=1):
        lines.append(f"{idx}. {improvement['title']}: {improvement['rationale']}")

    lines.append("\nMap upgrade concept")
    for item in payload["map_upgrade"]:
        lines.append(f"- {item}")

    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Print a conceptual Denver metro map + train expansion recommendations."
    )
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Output format (default: text).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_payload()
    if args.format == "json":
        print(json.dumps(payload, indent=2))
        return

    print(render_text(payload))


if __name__ == "__main__":
    main()
