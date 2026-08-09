from pydantic import BaseModel, Field


class TokenizeRequest(BaseModel):
    value: str = Field(min_length=1, max_length=256)
    purpose: str = Field(min_length=3, max_length=120)


class TokenizeResponse(BaseModel):
    token: str
    purpose: str
    classification: str = "sensitive"


class RedactRequest(BaseModel):
    text: str = Field(min_length=1, max_length=2000)


class RedactResponse(BaseModel):
    redacted_text: str
