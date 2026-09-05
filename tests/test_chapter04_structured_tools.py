import pytest
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from pydantic import ValidationError

from examples.chapter04_structured_tools.structured_output_demo import (
    UserRequestAnalysis,
    validate_offline_payload,
)
from examples.chapter04_structured_tools.tool_loop_demo import (
    execute_requested_tools,
    query_order,
    run_offline_tool_loop,
)


def test_structured_output_normalizes_and_validates_fields():
    result = validate_offline_payload(
        {
            "intent": "refund",
            "order_id": " a1001 ",
            "summary": "用户询问退款",
        }
    )

    assert result == UserRequestAnalysis(
        intent="refund",
        order_id="A1001",
        summary="用户询问退款",
    )


@pytest.mark.parametrize(
    "payload",
    [
        {"intent": "unknown", "order_id": None, "summary": "未知意图"},
        {"intent": "refund", "order_id": "   ", "summary": "退款"},
        {"intent": "refund", "order_id": None, "summary": ""},
        {
            "intent": "refund",
            "order_id": None,
            "summary": "退款",
            "unexpected": True,
        },
    ],
)
def test_structured_output_rejects_invalid_payload(payload):
    with pytest.raises(ValidationError):
        validate_offline_payload(payload)


def test_tool_schema_comes_from_signature_and_docstring():
    assert query_order.name == "query_order"
    assert query_order.args_schema.model_json_schema()["required"] == ["order_id"]
    assert "查询一个订单" in query_order.description


def test_tool_execution_returns_correlated_tool_message():
    request = AIMessage(
        content="",
        tool_calls=[
            {
                "name": "query_order",
                "args": {"order_id": "A1001"},
                "id": "call-test-001",
            }
        ],
    )

    result = execute_requested_tools(request)

    assert len(result) == 1
    assert result[0].tool_call_id == "call-test-001"
    assert '"status": "shipped"' in result[0].content


def test_complete_tool_loop_keeps_protocol_order():
    messages = run_offline_tool_loop("查询订单 A1001")

    assert isinstance(messages[0], HumanMessage)
    assert isinstance(messages[1], AIMessage)
    assert messages[1].tool_calls[0]["name"] == "query_order"
    assert isinstance(messages[2], ToolMessage)
    assert messages[2].tool_call_id == messages[1].tool_calls[0]["id"]
    assert isinstance(messages[3], AIMessage)
    assert "不能直接取消" in messages[3].content
