#!/usr/bin/env python3
"""Find identifiers and secret-like values that should be reviewed before release."""

from __future__ import annotations

import re
import sys
from pathlib import Path


TEXT_SUFFIXES = {".md", ".yaml", ".yml", ".json", ".txt", ".py", ".sh"}
SKIP_NAMES = {"scan_publication_risks.py"}

RULES = {
    "vendor or private program identifier": re.compile(
        r"\b(?:oppo|oplus|coloros|heytap|finshell|osrc|misrc)\b", re.I
    ),
    "ticket-like identifier": re.compile(r"\b[A-Z]{2,12}-\d{4,}(?:-\d+)*\b"),
    "absolute user path": re.compile(r"/(?:Users|home)/[^/\s]+/"),
    "non-example Android package": re.compile(
        r"\b(?:com|org|net)\.(?!example\b)[a-zA-Z][\w]*(?:\.[\w]+)+\b"
    ),
    "IPv4 address": re.compile(
        r"\b(?!(?:127|10)\.)(?!192\.168\.)(?!172\.(?:1[6-9]|2\d|3[01])\.)"
        r"(?:\d{1,3}\.){3}\d{1,3}\b"
    ),
    "non-example domain": re.compile(
        r"\b(?!example\.(?:com|org|net)\b)(?!localhost\b)"
        r"[a-zA-Z0-9][a-zA-Z0-9.-]*\.(?:com|cn|net|org|io|dev|app)\b"
    ),
    "credential-like assignment": re.compile(
        r"(?i)\b(?:token|secret|password|passwd|cookie|authorization)\b"
        r"\s*[:=]\s*['\"][^'\"<>\s]{8,}['\"]"
    ),
}


def iter_text_files(root: Path):
    for path in sorted(root.rglob("*")):
        if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES and path.name not in SKIP_NAMES:
            yield path


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    findings = []
    for path in iter_text_files(root):
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            continue
        for line_number, line in enumerate(lines, 1):
            for rule_name, pattern in RULES.items():
                if pattern.search(line):
                    findings.append((path.relative_to(root), line_number, rule_name, line.strip()))

    for path, line_number, rule_name, line in findings:
        print(f"{path}:{line_number}: {rule_name}: {line}")

    if findings:
        print(f"\nFound {len(findings)} item(s); review and remove or explicitly allow each one.")
        return 1

    print("No publication-risk patterns found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
