#!/usr/bin/env python3
"""Very small educational privacy policy check.

This is intentionally simple: it catches obvious anti-patterns in source/config files.
Enterprise use should rely on mature scanners and policy-as-code platforms too.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

SKIP_DIRS = {".git", ".venv", "venv", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}
TEXT_SUFFIXES = {".py", ".yaml", ".yml", ".json", ".toml", ".md", ".txt", ".env"}

RULES = [
    (
        "hard-coded-password",
        re.compile(r"(?i)(password|passwd)\s*[:=]\s*['\"](?!example|changeme)[^'\"]{8,}"),
        "Do not hard-code passwords; use a secret manager.",
    ),
    (
        "private-key",
        re.compile(r"-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----"),
        "Private key material must never be committed.",
    ),
    (
        "raw-ssn-log",
        re.compile(r"(?i)(logger|logging).*ssn"),
        "Do not log raw SSNs; log metadata or a token instead.",
    ),
]


def iter_files(root: Path):
    scanner_path = Path(__file__).resolve()
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if path.resolve() == scanner_path:
            continue  # Avoid matching the scanner's own rule definitions.
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.suffix.lower() in TEXT_SUFFIXES or path.name.startswith("Dockerfile"):
            yield path


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    findings: list[str] = []

    for path in iter_files(root):
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for rule_name, pattern, guidance in RULES:
            for match in pattern.finditer(text):
                line = text.count("\n", 0, match.start()) + 1
                findings.append(f"{path.relative_to(root)}:{line}: {rule_name}: {guidance}")

    if findings:
        print("Privacy policy check FAILED")
        print("\n".join(findings))
        return 1

    print("Privacy policy check PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
