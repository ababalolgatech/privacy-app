"""
Beginner policy-as-code example.

The script checks only application source files for a few easy-to-understand
privacy/security mistakes. It is intentionally small so you can explain it
during an interview.
"""

from pathlib import Path
import sys

APP_DIRECTORY = Path("app")

BAD_PATTERNS = {
    'password = "': "Possible hard-coded password",
    "password = '": "Possible hard-coded password",
    'api_key = "': "Possible hard-coded API key",
    "api_key = '": "Possible hard-coded API key",
    "print(request": "Possible logging/printing of a full request",
    "print(request.": "Possible logging/printing of request data",
}

problems: list[str] = []

for file_path in APP_DIRECTORY.rglob("*.py"):
    text = file_path.read_text(encoding="utf-8").lower()

    for pattern, message in BAD_PATTERNS.items():
        if pattern in text:
            problems.append(f"{file_path}: {message}")

if problems:
    print("PRIVACY POLICY CHECK FAILED")
    for problem in problems:
        print(f"- {problem}")
    sys.exit(1)

print("PRIVACY POLICY CHECK PASSED")
print("No beginner policy violations were found in app/.")
