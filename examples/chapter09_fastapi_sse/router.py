"""Thin HTTP adapter for normal JSON and SSE Agent responses."""

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from .dependencies import AgentServiceDep
from .schemas import ChatRequest, ChatResponse
from .sse import encode_sse

router = APIRouter(prefix="/api/v1/agent", tags=["Agent"])


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    service: AgentServiceDep,
) -> ChatResponse:
    """Return the final graph result as one validated JSON object."""

    return await service.chat(request)


@router.post("/chat/stream")
async def chat_stream(
    request: ChatRequest,
    service: AgentServiceDep,
) -> StreamingResponse:
    """Return application events as an SSE response body."""

    event_stream = (
        encode_sse(event)
        async for event in service.chat_stream(request)
    )
    return StreamingResponse(
        content=event_stream,
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )
