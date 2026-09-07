"""A deterministic StateGraph with state updates and conditional routing."""

from __future__ import annotations

import operator
from typing import Annotated, Literal, TypedDict

from langgraph.graph import END, START, StateGraph


class SupportState(TypedDict, total=False):
    """Serializable state shared by every node in this graph."""

    question: str
    intent: Literal["order_query", "general"]
    answer: str
    path: Annotated[list[str], operator.add]


def classify_intent(state: SupportState) -> dict[str, object]:
    """Classify with deterministic code so graph behavior is testable."""

    intent = "order_query" if "订单" in state["question"] else "general"
    return {"intent": intent, "path": ["classify_intent"]}


def route_intent(state: SupportState) -> Literal["query_order", "general_response"]:
    """Choose the next node without changing state."""

    if state["intent"] == "order_query":
        return "query_order"
    return "general_response"


def query_order(state: SupportState) -> dict[str, object]:
    """Represent a deterministic business-query branch."""

    return {
        "answer": "订单 A1001 当前状态为已发货。",
        "path": ["query_order"],
    }


def general_response(state: SupportState) -> dict[str, object]:
    """Represent a branch that does not need a business query."""

    return {
        "answer": f"已收到问题：{state['question']}",
        "path": ["general_response"],
    }


def build_routing_graph():
    """Build and compile an executable conditional graph."""

    builder = StateGraph(SupportState)
    builder.add_node("classify_intent", classify_intent)
    builder.add_node("query_order", query_order)
    builder.add_node("general_response", general_response)

    builder.add_edge(START, "classify_intent")
    builder.add_conditional_edges("classify_intent", route_intent)
    builder.add_edge("query_order", END)
    builder.add_edge("general_response", END)
    return builder.compile()


def run_routing_graph(question: str) -> SupportState:
    """Invoke the compiled graph with one initial state snapshot."""

    graph = build_routing_graph()
    return graph.invoke({"question": question, "path": []})


def main() -> None:
    order_result = run_routing_graph("查询订单 A1001")
    general_result = run_routing_graph("你好")

    print(f"订单分支：{order_result}")
    print(f"普通分支：{general_result}")


if __name__ == "__main__":
    main()
