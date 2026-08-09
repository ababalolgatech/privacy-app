from app.privacy import redact_sensitive_text, tokenize


def test_tokenize_changes_input() -> None:
    assert tokenize("member-123", "test-key") != "member-123"


def test_redaction_handles_email_and_ssn() -> None:
    result = redact_sensitive_text("a@example.com has SSN 123-45-6789")
    assert result == "[REDACTED_EMAIL] has SSN [REDACTED_SSN]"
