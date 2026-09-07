"""A deterministic asynchronous graph that emits custom stream events."""

from __future__ import annotations

import asyncio
from typing import TypedDict

from langgraph.config import get_stream_writer
from langgraph.graph import END, START, StateGraph


class AgentState(TypedDict, total=False):
    """Serializable state for one request."""

    user_id: str
    thread_id: str
    message: str
    answer: str


async def generate_answer(state: AgentState) -> dict[str, str]:
    """Emit deterministic chunks while building one final state update."""

    writer = get_stream_writer()
    chunks = ["已收到问题：", state["message"]]

    writer(
        {
            "event": "metadata",
            "data": {"thread_id": state["thread_id"]},
        }
    )
    for chunk in chunks:
        writer({"event": "token", "data": {"content": chunk}})
        await asyncio.sleep(0)

    return {"answer": "".join(chunks)}


def build_agent_graph():
    """Compile the workflow once; the FastAPI lifespan owns the result."""

    builder = StateGraph(AgentState)
    builder.add_node("generate_answer", generate_answer)
    builder.add_edge(START, "generate_answer")
    builder.add_edge("generate_answer", END)
    return builder.compile()
