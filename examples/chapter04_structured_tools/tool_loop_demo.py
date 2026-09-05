"""A deterministic model-request/tool-result/final-answer loop."""

from __future__ import annotations

import json
from typing import Any

from langchain.tools import tool
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage


@tool
def query_order(order_id: str) -> dict[str, str]:
    """查询一个订单的当前状态。"""

    orders = {
        "A1001": {
            "order_id": "A1001",
            "status": "shipped",
            "can_cancel_directly": "false",
        }
    }
    return orders.get(
        order_id.upper(),
        {
            "order_id": order_id.upper(),
            "status": "not_found",
            "can_cancel_directly": "false",
        },
    )


TOOLS = {query_order.name: query_order}


def fake_model_requests_tool() -> AIMessage:
    """Stand in for a model response containing one tool request."""

    return AIMessage(
        content="",
        tool_calls=[
            {
                "name": "query_order",
                "args": {"order_id": "A1001"},
                "id": "call-order-001",
            }
        ],
    )


def execute_requested_tools(ai_message: AIMessage) -> list[ToolMessage]:
    """Allowlist, validate, execute, and correlate requested tool calls."""

    results: list[ToolMessage] = []
    for tool_call in ai_message.tool_calls:
        tool_name = tool_call["name"]
        selected_tool = TOOLS.get(tool_name)
        if selected_tool is None:
            raise ValueError(f"不允许调用工具：{tool_name}")

        output: Any = selected_tool.invoke(tool_call["args"])
        results.append(
            ToolMessage(
                content=json.dumps(output, ensure_ascii=False),
                tool_call_id=tool_call["id"],
                name=tool_name,
            )
        )
    return results


def fake_model_writes_final_answer(tool_result: ToolMessage) -> AIMessage:
    """Stand in for the second model call after it sees tool data."""

    result = json.loads(str(tool_result.content))
    if result["status"] == "shipped":
        answer = "订单已发货，不能直接取消，请按退货流程处理。"
    else:
        answer = "没有查到该订单，请核对订单号。"
    return AIMessage(content=answer)


def run_offline_tool_loop(
    question: str,
) -> list[HumanMessage | AIMessage | ToolMessage]:
    """Run one complete tool loop and expose the message history."""

    messages: list[HumanMessage | AIMessage | ToolMessage] = [
        HumanMessage(content=question)
    ]
    request = fake_model_requests_tool()
    messages.append(request)

    tool_results = execute_requested_tools(request)
    messages.extend(tool_results)

    final_answer = fake_model_writes_final_answer(tool_results[0])
    messages.append(final_answer)
    return messages


def main() -> None:
    messages = run_offline_tool_loop("订单 A1001 已经发货，还能直接取消吗？")
    for index, message in enumerate(messages, start=1):
        print(f"{index}. {message.type}: {message.content}")
        if isinstance(message, AIMessage) and message.tool_calls:
            print(f"   tool_calls: {message.tool_calls}")
        if isinstance(message, ToolMessage):
            print(f"   tool_call_id: {message.tool_call_id}")


if __name__ == "__main__":
    main()
