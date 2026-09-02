"""Secret-safe local model configuration shared by course examples."""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(frozen=True)
class ModelSettings:
    """OpenAI-compatible model settings loaded without exposing their values."""

    model: str
    api_key: str
    base_url: str

    @classmethod
    def from_env(cls, *, load_file: bool = True) -> ModelSettings:
        """Load settings from process variables and optionally a local `.env`."""

        if load_file:
            load_dotenv()

        return cls(
            model=os.getenv("LLM_MODEL", "").strip(),
            api_key=os.getenv("LLM_API_KEY", "").strip(),
            base_url=os.getenv("LLM_BASE_URL", "").strip(),
        )

    def missing_variables(self) -> tuple[str, ...]:
        """Return missing variable names without returning configured values."""

        pairs = (
            ("LLM_MODEL", self.model),
            ("LLM_API_KEY", self.api_key),
            ("LLM_BASE_URL", self.base_url),
        )
        return tuple(name for name, value in pairs if not value)

    def require_complete(self) -> ModelSettings:
        """Raise a value-free error when required local settings are absent."""

        missing = self.missing_variables()
        if missing:
            names = ", ".join(missing)
            raise RuntimeError(f"Missing required environment variables: {names}")
        return self
