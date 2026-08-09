import os
from functools import lru_cache

from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "privacy-devsecops-demo"
    environment: str = os.getenv("APP_ENV", "local")
    api_key: str = os.getenv("DEMO_API_KEY", "")
    token_key: str = os.getenv("TOKENIZATION_KEY", "")

    @property
    def is_production(self) -> bool:
        return self.environment.lower() == "production"

    def validate_runtime_secrets(self) -> None:
        """Fail closed when required runtime secrets are missing or weak."""
        if len(self.api_key) < 16 or len(self.token_key) < 16:
            raise RuntimeError("Runtime secrets must be injected securely and be at least 16 characters")


@lru_cache
def get_settings() -> Settings:
    return Settings()
