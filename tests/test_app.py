import logging
import os

os.environ["DEMO_API_KEY"] = "local-demo-api-key-change-me"
os.environ["TOKENIZATION_KEY"] = "local-demo-token-key-change-me"

from fastapi.testclient import TestClient

from app.main import app

API_KEY = "local-demo-api-key-change-me"
HEADERS = {"X-API-Key": API_KEY}


def test_liveness() -> None:
    with TestClient(app) as client:
        response = client.get("/health/live")
    assert response.status_code == 200
    assert response.json() == {"status": "alive"}


def test_protected_endpoint_rejects_missing_key() -> None:
    with TestClient(app) as client:
        response = client.post(
            "/v1/tokenize",
            json={"value": "123-45-6789", "purpose": "member correlation"},
        )
    assert response.status_code == 401


def test_tokenization_is_deterministic_and_hides_raw_value() -> None:
    payload = {"value": "123-45-6789", "purpose": "member correlation"}
    with TestClient(app) as client:
        first = client.post("/v1/tokenize", json=payload, headers=HEADERS)
        second = client.post("/v1/tokenize", json=payload, headers=HEADERS)

    assert first.status_code == 200
    assert first.json()["token"] == second.json()["token"]
    assert first.json()["token"].startswith("tok_")
    assert payload["value"] not in first.text


def test_redaction_endpoint_masks_common_pii() -> None:
    text = "Email jane@example.com, SSN 123-45-6789, card 4111 1111 1111 1111"
    with TestClient(app) as client:
        response = client.post("/v1/redact", json={"text": text}, headers=HEADERS)

    assert response.status_code == 200
    redacted = response.json()["redacted_text"]
    assert "jane@example.com" not in redacted
    assert "123-45-6789" not in redacted
    assert "4111 1111 1111 1111" not in redacted
    assert "[REDACTED_EMAIL]" in redacted
    assert "[REDACTED_SSN]" in redacted
    assert "[REDACTED_CARD]" in redacted


def test_sensitive_value_not_written_to_application_log(caplog) -> None:
    raw_value = "123-45-6789"
    caplog.set_level(logging.INFO, logger="privacy_demo")
    with TestClient(app) as client:
        response = client.post(
            "/v1/tokenize",
            json={"value": raw_value, "purpose": "member correlation"},
            headers=HEADERS,
        )
    assert response.status_code == 200
    assert raw_value not in caplog.text
