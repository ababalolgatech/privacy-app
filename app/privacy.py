import hashlib
import hmac
import re

EMAIL_PATTERN = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
SSN_PATTERN = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")
CARD_PATTERN = re.compile(r"\b(?:\d[ -]*?){13,16}\b")


def redact_sensitive_text(value: str) -> str:
    """Redact common sensitive patterns before logging or returning debug text."""
    value = EMAIL_PATTERN.sub("[REDACTED_EMAIL]", value)
    value = SSN_PATTERN.sub("[REDACTED_SSN]", value)
    value = CARD_PATTERN.sub("[REDACTED_CARD]", value)
    return value


def tokenize(value: str, key: str) -> str:
    """Create a deterministic HMAC token for demonstration purposes.

    This is pseudonymization, not a production token vault. Production systems
    should use an enterprise tokenization/KMS design appropriate to the data risk.
    """
    digest = hmac.new(
        key.encode("utf-8"), value.encode("utf-8"), hashlib.sha256
    ).hexdigest()
    return f"tok_{digest[:24]}"
