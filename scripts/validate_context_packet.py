#!/usr/bin/env python3
"""Validate a Map Mind context artifact for safe handoff."""

from __future__ import annotations

import argparse
import os
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

SECRET_PATTERNS = {
    "possible private key": r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
    "possible api key": r"(?i)\b(api[_-]?key|token|secret|password)\b\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{16,}",
    "possible github token": r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b",
    "possible openai key": r"\bsk-[A-Za-z0-9_\-]{20,}\b",
    "possible aws access key": r"\bAKIA[0-9A-Z]{16}\b",
}

VAGUE_NEXT = re.compile(r"(?i)\b(continue|finish|handle|do the rest|follow up|look into it|fix stuff)\b")
TODO_RE = re.compile(r"(?i)\b(todo|tbd|fixme|xxx)\b")
ABS_PATH = r"/(?:[\w.@+~-][\w .@+~-]*/)+[\w.@+~-][\w .@+~-]*"
REL_FILE = r"(?:\.{1,2}/)?[\w@+\-][\w@+\-./ ]+\.(?:py|js|ts|tsx|jsx|md|json|yaml|yml|toml|txt|sh|css|html|go|rs|java|rb|php|swift|kt|sql)"
PATH_RE = re.compile(rf"(?P<path>{ABS_PATH}|{REL_FILE})")


def parse_sections(text: str) -> dict[str, str]:
    matches = list(re.finditer(r"^##\s+(.+?)\s*$", text, flags=re.MULTILINE))
    sections: dict[str, str] = {}
    for index, match in enumerate(matches):
        title = match.group(1).strip()
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections[title] = text[start:end].strip()
    return sections


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
    sections = parse_sections(text)
    if "Success Condition" in sections and "Sources Inspected" in sections:
        return "context-map"
    if "Must Preserve" in sections and "Verification Needed" in sections:
        return "resume-brief"
    return "handoff-packet"


def validate(
    text: str,
    *,
    artifact_type: str = "auto",
    strict_paths: bool = False,
    max_words: int = 1800,
) -> tuple[str, list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    sections = parse_sections(text)
    detected_type = detect_artifact_type(text, artifact_type)
    required_sections = ARTIFACT_SECTIONS[detected_type]

    for section in required_sections:
        body = sections.get(section)
        if body is None:
            errors.append(f"Missing required section: {section}")
        elif len(body.split()) < 2:
            warnings.append(f"Section is empty or too thin: {section}")

    if len(text.split()) > max_words:
        warnings.append(f"Packet exceeds max word budget: {len(text.split())}>{max_words}")

    for label, pattern in SECRET_PATTERNS.items():
        if re.search(pattern, text):
            errors.append(f"Secret-like content detected: {label}")

    next_actions = sections.get("Next Actions", sections.get("Next Action", ""))
    if not re.search(r"(?m)^\s*(?:\d+\.|-|\*)\s+\S+", next_actions):
        if detected_type == "resume-brief" and len(next_actions.split()) >= 3:
            pass
        else:
            errors.append("Next Actions must contain concrete ordered or bulleted actions.")
    if VAGUE_NEXT.search(next_actions):
        warnings.append("Next Actions contains vague continuation language.")

    if TODO_RE.search(text):
        warnings.append("Packet contains TODO/TBD/FIXME-style placeholder language.")

    facts = sections.get("Facts Verified", sections.get("Verified Facts", ""))
    if facts and not any(marker in facts.lower() for marker in ["`", "/", ".md", ".py", ".ts", ".js", "command", "source", "user said", "tool"]):
        warnings.append("Facts Verified has no obvious source anchors.")

    assumptions = sections.get("Assumptions", sections.get("Uncertainties", ""))
    if detected_type != "resume-brief" and not assumptions:
        warnings.append("Assumptions section missing content; say `None known` if there are none.")

    raw_paths = {m.group("path").strip("`'\"),.;") for m in PATH_RE.finditer(text)}
    missing_paths: list[str] = []
    for raw in sorted(raw_paths):
        if "://" in raw or raw.startswith("Source:"):
            continue
        expanded = os.path.expanduser(raw)
        if raw.startswith("/") and not Path(expanded).exists():
            missing_paths.append(raw)

    if missing_paths:
        message = "Missing absolute file references: " + ", ".join(missing_paths[:10])
        if strict_paths:
            errors.append(message)
        else:
            warnings.append(message)

    if errors:
        verdict = "FAIL"
    elif warnings:
        verdict = "WARN"
    else:
        verdict = "PASS"
    return verdict, errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("packet", help="Markdown context artifact to validate")
    parser.add_argument(
        "--type",
        choices=["auto", "context-map", "handoff-packet", "resume-brief"],
        default="auto",
        help="Artifact type. Defaults to auto-detection from headings.",
    )
    parser.add_argument("--strict-paths", action="store_true", help="Fail when absolute local file refs are missing")
    parser.add_argument("--max-words", type=int, default=1800, help="Maximum allowed words")
    args = parser.parse_args()

    text = Path(args.packet).read_text(encoding="utf-8")
    artifact_type = detect_artifact_type(text, args.type)
    verdict, errors, warnings = validate(
        text,
        artifact_type=artifact_type,
        strict_paths=args.strict_paths,
        max_words=args.max_words,
    )
    print(verdict)
    print(f"TYPE: {artifact_type}")
    for error in errors:
        print(f"ERROR: {error}")
    for warning in warnings:
        print(f"WARN: {warning}")
    return 0 if verdict in {"PASS", "WARN"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
