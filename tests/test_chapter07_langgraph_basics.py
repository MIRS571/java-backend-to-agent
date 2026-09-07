from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langgraph.graph.message import add_messages

from examples.chapter07_langgraph_basics.message_tool_graph import (
    build_message_tool_graph,
    run_message_tool_graph,
)
from examples.chapter07_langgraph_basics.routing_graph import run_routing_graph


def test_conditional_graph_runs_order_branch_and_accumulates_path():
    result = run_routing_graph("查询订单 A1001")

    assert result["intent"] == "order_query"
    assert result["answer"] == "订单 A1001 当前状态为已发货。"
    assert result["path"] == ["classify_intent", "query_order"]


def test_conditional_graph_runs_only_general_branch():
    result = run_routing_graph("你好")

    assert result["intent"] == "general"
    assert result["answer"] == "已收到问题：你好"
    assert result["path"] == ["classify_intent", "general_response"]


def test_compiled_graph_implements_runnable_invocation():
    graph = build_message_tool_graph()

    result = graph.invoke(
        {"messages": [{"role": "user", "content": "缺少订单号"}]}
    )

    assert result["messages"][-1].content == "请提供需要查询的订单号。"


def test_messages_state_deserializes_and_appends_tool_protocol():
    result = run_message_tool_graph("查询订单 A1001")
    messages = result["messages"]

    assert len(messages) == 4
    assert isinstance(messages[0], HumanMessage)
    assert isinstance(messages[1], AIMessage)
    assert isinstance(messages[2], ToolMessage)
    assert isinstance(messages[3], AIMessage)
    assert messages[3].content == "订单 A1001 已发货，不能直接取消。"


def test_tool_message_correlates_with_ai_tool_call():
    messages = run_message_tool_graph("查询订单 A1001")["messages"]
    tool_request = messages[1]
    tool_result = messages[2]

    assert tool_request.tool_calls[0]["name"] == "query_order"
    assert tool_result.tool_call_id == tool_request.tool_calls[0]["id"]


def test_add_messages_replaces_same_message_id_instead_of_duplicating():
    before = [AIMessage(id="answer-1", content="旧答案")]
    update = [AIMessage(id="answer-1", content="新答案")]

    merged = add_messages(before, update)

    assert len(merged) == 1
    assert merged[0].content == "新答案"
