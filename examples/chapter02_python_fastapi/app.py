"""A small FastAPI boundary before real Agent behavior is introduced."""

from __future__ import annotations

from typing import Literal

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(
    title="Chapter 2 FastAPI Demo",
    version="0.1.0",
)


class MessagePreviewRequest(BaseModel):
    """The JSON request body accepted by the preview endpoint."""

    message: str = Field(min_length=1, max_length=200)
    language: Literal["zh", "en"] = "zh"


class MessagePreviewResponse(BaseModel):
    """The stable JSON shape returned by the preview endpoint."""

    normalized_message: str
    language: Literal["zh", "en"]
    preview: str


@app.get("/health")
def health() -> dict[str, str]:
    """Return a minimal health signal with no model or database dependency."""

    return {"status": "ok"}


@app.post(
    "/api/v1/messages/preview",
    response_model=MessagePreviewResponse,
)
def create_message_preview(
    request: MessagePreviewRequest,
) -> MessagePreviewResponse:
    """Validate, normalize, and return a deterministic preview."""

    normalized_message = request.message.strip()
    if not normalized_message:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="message cannot contain only whitespace",
        )

    prefix = "已接收" if request.language == "zh" else "Received"
    preview = f"{prefix}: {normalized_message}"
    return MessagePreviewResponse(
        normalized_message=normalized_message,
        language=request.language,
        preview=preview,
    )
