from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)
HEADERS = {"X-API-Key": "demo-key"}


def test_health() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_redact_removes_email_and_ssn() -> None:
    response = client.post(
        "/redact",
        headers=HEADERS,
        json={"text": "Email alice@example.com and SSN 123-45-6789"},
    )

    assert response.status_code == 200

    result = response.json()["redacted_text"]

    assert "alice@example.com" not in result
    assert "123-45-6789" not in result
    assert "[REDACTED_EMAIL]" in result
    assert "[REDACTED_SSN]" in result


def test_redact_requires_api_key() -> None:
    response = client.post(
        "/redact",
        json={"text": "hello"},
    )

    assert response.status_code == 401


def test_tokenize_is_repeatable() -> None:
    payload = {"identifier": "member-123"}

    first = client.post("/tokenize", headers=HEADERS, json=payload)
    second = client.post("/tokenize", headers=HEADERS, json=payload)

    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json()["token"] == second.json()["token"]
