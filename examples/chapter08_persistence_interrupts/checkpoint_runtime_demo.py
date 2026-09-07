"""Persist thread state while injecting dependencies through Runtime."""

from __future__ import annotations

import operator
from typing import Annotated, TypedDict

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.runtime import Runtime

from .support_context import AgentContext, FakeSupportService


class ConversationState(TypedDict, total=False):
    """Serializable data that evolves across invocations in one thread."""

    history: Annotated[list[str], operator.add]
    turn_count: int


def answer_order(
    state: ConversationState,
    runtime: Runtime[AgentContext],
) -> dict[str, object]:
    """Use runtime dependencies without placing them in checkpointed state."""

    question = state["history"][-1]
    status = runtime.context.support_service.query_order_status(
        tenant_id=runtime.context.tenant_id,
        order_id="A1001",
    )
    return {
        "history": [f"assistant:{question} -> {status}"],
        "turn_count": state.get("turn_count", 0) + 1,
    }


def build_conversation_graph(checkpointer=None):
    """Compile a graph with thread-level checkpoint persistence."""

    builder = StateGraph(ConversationState, context_schema=AgentContext)
    builder.add_node("answer_order", answer_order)
    builder.add_edge(START, "answer_order")
    builder.add_edge("answer_order", END)
    saver = checkpointer if checkpointer is not None else InMemorySaver()
    return builder.compile(checkpointer=saver)


def main() -> None:
    service = FakeSupportService()
    context = AgentContext(
        tenant_id="company_001",
        support_service=service,
    )
    graph = build_conversation_graph()
    same_thread = {"configurable": {"thread_id": "thread-001"}}
    another_thread = {"configurable": {"thread_id": "thread-002"}}

    first = graph.invoke(
        {"history": ["user:查询订单 A1001"]},
        config=same_thread,
        context=context,
    )
    second = graph.invoke(
        {"history": ["user:再查一次"]},
        config=same_thread,
        context=context,
    )
    isolated = graph.invoke(
        {"history": ["user:新会话查询"]},
        config=another_thread,
        context=context,
    )

    print(f"同一 thread 第一次：turn_count={first['turn_count']}")
    print(f"同一 thread 第二次：turn_count={second['turn_count']}")
    print(f"另一 thread：turn_count={isolated['turn_count']}")
    print(f"同一 thread 历史：{second['history']}")


if __name__ == "__main__":
    main()
