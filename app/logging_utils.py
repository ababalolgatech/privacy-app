import logging
from app.privacy import redact_sensitive_text


class RedactingFormatter(logging.Formatter):
    """Formatter that redacts common PII patterns from the final log message."""

    def format(self, record: logging.LogRecord) -> str:
        rendered = super().format(record)
        return redact_sensitive_text(rendered)


def configure_logging() -> logging.Logger:
    logger = logging.getLogger("privacy_demo")
    logger.setLevel(logging.INFO)
    logger.propagate = True

    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(
            RedactingFormatter("%(levelname)s %(name)s %(message)s")
        )
        logger.addHandler(handler)
    return logger
