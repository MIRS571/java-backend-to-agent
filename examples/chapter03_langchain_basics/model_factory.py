"""The boundary where a real provider-backed chat model is configured."""

from __future__ import annotations

from dataclasses import dataclass

from langchain_openai import ChatOpenAI


@dataclass(frozen=True)
class ModelSettings:
    """Trusted configuration supplied by application settings, not user input."""

    model: str
    api_key: str
    base_url: str | None = None
    timeout: float = 60
    max_retries: int = 2


def create_chat_model(settings: ModelSettings) -> ChatOpenAI:
    """Create a client without sending a model request."""

    return ChatOpenAI(
        model=settings.model,
        api_key=settings.api_key,
        base_url=settings.base_url,
        timeout=settings.timeout,
        max_retries=settings.max_retries,
    )
