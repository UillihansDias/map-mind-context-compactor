#!/usr/bin/env python3
"""Score a Map Mind context artifact for completeness and resumability."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


ARTIFACT_SECTIONS = {
    "context-map": [
        "Goal",
        "Success Condition",
        "Sources Inspected",
        "User Intent",
        "Constraints",
        "Decisions",
        "Verified Facts",
        "Assumptions",
        "Active Files / Code Areas",
        "Tool State / Environment",
        "Risks",
        "Open Questions",
        "Next Actions",
        "Non-Goals",
        "Implications for Next Agent",
    ],
    "handoff-packet": [
        "Goal",
        "Current State",
        "User Intent",
        "Constraints",
        "Decisions Made",
        "Facts Verified",
        "Assumptions",
        "Open Questions",
        "Active Files / Code Areas",
        "Tool State / Environment",
        "Risks",
        "Next Actions",
        "Non-Goals",
        "Resume Prompt",
        "Implications for Next Agent",
    ],
    "resume-brief": [
        "Resume Prompt",
        "Goal",
        "Current State",
        "Must Preserve",
        "Verified Facts",
        "Uncertainties",
        "Next Action",
        "Verification Needed",
    ],
}

SOURCE_HINTS = [
    "`",
    "/",
    ".md",
    ".py",
    ".ts",
    ".tsx",
    ".js",
    ".json",
    "command",
    "output",
    "user said",
    "source:",
]


def sections(text: str) -> dict[str, str]:
    matches = list(re.finditer(r"^##\s+(.+?)\s*$", text, flags=re.MULTILINE))
    result: dict[str, str] = {}
    for index, match in enumerate(matches):
        title = match.group(1).strip()
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        result[title] = text[start:end].strip()
    return result


def detect_artifact_type(text: str, requested: str = "auto") -> str:
    if requested != "auto":
        return requested
    first_heading = re.search(r"^#\s+(.+?)\s*$", text, flags=re.MULTILINE)
    if first_heading:
        heading = first_heading.group(1).strip().lower()
        if heading == "context map":
            return "context-map"
        if heading == "resume brief":
            return "resume-brief"
        if heading == "handoff packet":
            return "handoff-packet"
    found = sections(text)
    if "Success Condition" in found and "Sources Inspected" in found:
        return "context-map"
    if "Must Preserve" in found and "Verification Needed" in found:
        return "resume-brief"
    return "handoff-packet"


def score(text: str, *, artifact_type: str = "auto") -> tuple[int, list[str], str]:
    found = sections(text)
    detected_type = detect_artifact_type(text, artifact_type)
    required = ARTIFACT_SECTIONS[detected_type]
    points = 0
    max_points = 100
    notes: list[str] = []

    required_points = 60
    per_section = required_points / len(required)
    for section in required:
        body = found.get(section, "")
        if body and len(body) > 10:
            points += per_section
        else:
            notes.append(f"Missing or thin section: {section}")

    if any(hint.lower() in text.lower() for hint in SOURCE_HINTS):
        points += 10
    else:
        notes.append("No clear source anchors or file/tool references found.")

    next_actions = found.get("Next Actions", found.get("Next Action", ""))
    if re.search(r"(?im)^\s*(1\.|-|\*)\s+\S+", next_actions):
        points += 10
    elif detected_type == "resume-brief" and len(next_actions.split()) >= 3:
        points += 10
    else:
        notes.append("Next Actions is not concrete or list-like.")

    if len(text.split()) <= 1800:
        points += 10
    else:
        notes.append("Packet is over the default 1800-word handoff budget.")

    uncertainty_terms = ["assumption", "unknown", "unverified", "open", "risk", "not run", "pending"]
    if any(term in text.lower() for term in uncertainty_terms):
        points += 10
    else:
        notes.append("No explicit uncertainty, risk, or pending verification found.")

    return min(round(points), max_points), notes, detected_type


def verdict(points: int) -> str:
    if points >= 85:
        return "PASS"
    if points >= 65:
        return "WARN"
    return "FAIL"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("packet", help="Markdown context artifact to score")
    parser.add_argument(
        "--type",
        choices=["auto", "context-map", "handoff-packet", "resume-brief"],
        default="auto",
        help="Artifact type. Defaults to auto-detection from headings.",
    )
    args = parser.parse_args()

    text = Path(args.packet).read_text(encoding="utf-8")
    points, notes, artifact_type = score(text, artifact_type=args.type)
    print(f"{verdict(points)} {points}/100")
    print(f"TYPE: {artifact_type}")
    for note in notes:
        print(f"- {note}")
    return 0 if points >= 65 else 1


if __name__ == "__main__":
    raise SystemExit(main())
