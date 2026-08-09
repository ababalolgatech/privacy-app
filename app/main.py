from __future__ import annotations

import hashlib
import os
import re

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(
    title="Beginner Privacy DevSecOps Demo",
    version="1.0.0",
    description=(
        "A small FastAPI project that demonstrates a continuous CI security "
        "workflow from linting through DAST."
    ),
)

EMAIL_PATTERN = re.compile(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}")
SSN_PATTERN = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")


class TextRequest(BaseModel):
    text: str = Field(min_length=1, max_length=2000)


class IdentifierRequest(BaseModel):
    identifier: str = Field(min_length=1, max_length=200)


def require_api_key(x_api_key: str | None) -> None:
    """Tiny authentication example for learning purposes."""
    expected_key = os.getenv("APP_API_KEY", "demo-key")

    if x_api_key != expected_key:
        raise HTTPException(status_code=401, detail="Unauthorized")


@app.get("/")
def home() -> dict[str, object]:
    return {
        "message": "Beginner Privacy DevSecOps Demo",
        "endpoints": ["/health", "/redact", "/tokenize"],
    }


@app.get("/health")
def health() -> dict[str, str]:
    """Health endpoint used by people, CI, Docker, and Kubernetes."""
    return {"status": "ok"}


@app.post("/redact")
def redact(
    request: TextRequest,
    x_api_key: str | None = Header(default=None),
) -> dict[str, str]:
    """Redact simple email and SSN patterns."""
    require_api_key(x_api_key)

    safe_text = EMAIL_PATTERN.sub("[REDACTED_EMAIL]", request.text)
    safe_text = SSN_PATTERN.sub("[REDACTED_SSN]", safe_text)

    return {"redacted_text": safe_text}


@app.post("/tokenize")
def tokenize(
    request: IdentifierRequest,
    x_api_key: str | None = Header(default=None),
) -> dict[str, str]:
    """
    Create a simple pseudonymous token.

    This demonstrates the concept only. A production system would use
    enterprise key management and an approved tokenization design.
    """
    require_api_key(x_api_key)

    secret = os.getenv("TOKENIZATION_SECRET", "demo-secret")
    raw_value = f"{secret}:{request.identifier}".encode("utf-8")
    token = hashlib.sha256(raw_value).hexdigest()[:20]

    return {"token": token}
