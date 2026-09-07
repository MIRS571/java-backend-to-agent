"""Application service that hides LangGraph calling details from HTTP routes."""

from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Any, TypedDict

from .agent_graph import build_agent_graph
from .schemas import ChatRequest, ChatResponse


class AgentEvent(TypedDict):
    """Internal event contract before SSE encoding."""

    event: str
    data: dict[str, Any]


class AgentGraphService:
    """Expose stable application methods around a compiled graph."""

    def __init__(self, graph=None) -> None:
        self._graph = graph or build_agent_graph()
        self.closed = False

    async def chat(self, request: ChatRequest) -> ChatResponse:
        """Wait for the whole graph and return one JSON response."""

        self._ensure_open()
        result = await self._graph.ainvoke(request.model_dump())
        return ChatResponse(
            thread_id=request.thread_id,
            answer=result["answer"],
        )

    async def chat_stream(
        self,
        request: ChatRequest,
    ) -> AsyncIterator[AgentEvent]:
        """Translate LangGraph v2 custom parts into application events."""

        self._ensure_open()
        async for part in self._graph.astream(
            request.model_dump(),
            stream_mode="custom",
            version="v2",
        ):
            if part["type"] == "custom":
                yield part["data"]

        yield {
            "event": "done",
            "data": {"thread_id": request.thread_id},
        }

    async def aclose(self) -> None:
        """Close resources owned by this service exactly once."""

        self.closed = True

    def _ensure_open(self) -> None:
        if self.closed:
            raise RuntimeError("AgentGraphService 已关闭")
