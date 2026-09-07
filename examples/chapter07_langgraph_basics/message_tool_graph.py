"""An offline MessagesState graph using ToolNode and tools_condition."""

from __future__ import annotations

import json

from langchain.tools import tool
from langchain_core.messages import AIMessage, ToolMessage
from langgraph.graph import START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition


@tool
def query_order(order_id: str) -> dict[str, str]:
    """查询订单当前状态。"""

    if order_id.upper() == "A1001":
        return {"order_id": "A1001", "status": "shipped"}
    return {"order_id": order_id.upper(), "status": "not_found"}


def call_model(state: MessagesState) -> dict[str, list[AIMessage]]:
    """Deterministically emulate model decisions before and after a tool call."""

    last_message = state["messages"][-1]
    if isinstance(last_message, ToolMessage):
        tool_result = json.loads(str(last_message.content))
        if tool_result["status"] == "shipped":
            content = "订单 A1001 已发货，不能直接取消。"
        else:
            content = "没有查询到该订单。"
        return {"messages": [AIMessage(content=content)]}

    question = str(last_message.content)
    if "A1001" not in question:
        return {"messages": [AIMessage(content="请提供需要查询的订单号。")]}

    return {
        "messages": [
            AIMessage(
                content="",
                tool_calls=[
                    {
                        "name": "query_order",
                        "args": {"order_id": "A1001"},
                        "id": "call-order-001",
                    }
                ],
            )
        ]
    }


def build_message_tool_graph():
    """Compile model -> optional tools -> model loop."""

    builder = StateGraph(MessagesState)
    builder.add_node("call_model", call_model)
    builder.add_node("tools", ToolNode([query_order]))

    builder.add_edge(START, "call_model")
    builder.add_conditional_edges("call_model", tools_condition)
    builder.add_edge("tools", "call_model")
    return builder.compile()


def run_message_tool_graph(question: str) -> MessagesState:
    """Run the graph from a serialized message dictionary."""

    graph = build_message_tool_graph()
    return graph.invoke(
        {"messages": [{"role": "user", "content": question}]}
    )


def main() -> None:
    result = run_message_tool_graph("查询订单 A1001")
    for index, message in enumerate(result["messages"], start=1):
        print(f"{index}. {message.type}: {message.content}")
        if isinstance(message, AIMessage) and message.tool_calls:
            print(f"   tool_calls: {message.tool_calls}")


if __name__ == "__main__":
    main()
