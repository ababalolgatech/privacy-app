import hmac
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Header, HTTPException, status

from app.config import Settings, get_settings
from app.logging_utils import configure_logging
from app.models import RedactRequest, RedactResponse, TokenizeRequest, TokenizeResponse
from app.privacy import redact_sensitive_text, tokenize

logger = configure_logging()


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    settings = get_settings()
    settings.validate_runtime_secrets()
    logger.info("application_start environment=%s", settings.environment)
    yield
    logger.info("application_stop")


app = FastAPI(
    title="Privacy DevSecOps Demo",
    version="1.0.0",
    lifespan=lifespan,
)


def require_api_key(
    x_api_key: str = Header(default=""),
    settings: Settings = Depends(get_settings),
) -> None:
    if not x_api_key or not settings.api_key or not hmac.compare_digest(x_api_key, settings.api_key):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API credential",
        )


@app.get("/health/live")
def liveness() -> dict[str, str]:
    return {"status": "alive"}


@app.get("/health/ready")
def readiness() -> dict[str, str]:
    return {"status": "ready"}


@app.post(
    "/v1/tokenize",
    response_model=TokenizeResponse,
    dependencies=[Depends(require_api_key)],
)
def tokenize_value(
    request: TokenizeRequest,
    settings: Settings = Depends(get_settings),
) -> TokenizeResponse:
    # Deliberately log only metadata; never the raw sensitive value.
    logger.info("tokenization_request purpose=%s", redact_sensitive_text(request.purpose))
    return TokenizeResponse(
        token=tokenize(request.value, settings.token_key),
        purpose=request.purpose,
    )


@app.post(
    "/v1/redact",
    response_model=RedactResponse,
    dependencies=[Depends(require_api_key)],
)
def redact_value(request: RedactRequest) -> RedactResponse:
    return RedactResponse(redacted_text=redact_sensitive_text(request.text))
