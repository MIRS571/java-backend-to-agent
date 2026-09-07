from langgraph.types import Command

from examples.chapter08_persistence_interrupts.checkpoint_runtime_demo import (
    build_conversation_graph,
)
from examples.chapter08_persistence_interrupts.interrupt_resume_demo import (
    build_refund_graph,
)
from examples.chapter08_persistence_interrupts.support_context import (
    AgentContext,
    FakeSupportService,
)


def build_context(tenant_id: str = "company_001") -> AgentContext:
    return AgentContext(tenant_id, FakeSupportService())


def test_checkpointer_accumulates_state_for_same_thread():
    graph = build_conversation_graph()
    context = build_context()
    config = {"configurable": {"thread_id": "same-thread"}}

    graph.invoke(
        {"history": ["user:第一次"]}, config=config, context=context
    )
    result = graph.invoke(
        {"history": ["user:第二次"]}, config=config, context=context
    )

    assert result["turn_count"] == 2
    assert len(result["history"]) == 4
    assert graph.get_state(config).values["history"] == result["history"]


def test_different_thread_ids_have_isolated_state():
    graph = build_conversation_graph()
    context = build_context()

    first = graph.invoke(
        {"history": ["user:会话一"]},
        config={"configurable": {"thread_id": "thread-1"}},
        context=context,
    )
    second = graph.invoke(
        {"history": ["user:会话二"]},
        config={"configurable": {"thread_id": "thread-2"}},
        context=context,
    )

    assert first["turn_count"] == 1
    assert second["turn_count"] == 1
    assert first["history"][0] == "user:会话一"
    assert second["history"][0] == "user:会话二"


def test_runtime_context_is_used_but_not_saved_in_state():
    graph = build_conversation_graph()
    context = build_context(tenant_id="unknown_company")
    config = {"configurable": {"thread_id": "runtime-context"}}

    result = graph.invoke(
        {"history": ["user:查询"]}, config=config, context=context
    )

    assert result["history"][-1].endswith("订单不存在")
    assert "support_service" not in graph.get_state(config).values
    assert "tenant_id" not in graph.get_state(config).values


def test_interrupt_pauses_before_refund_side_effect():
    graph = build_refund_graph()
    context = build_context()
    config = {"configurable": {"thread_id": "refund-paused"}}

    result = graph.invoke(
        {"order_id": "A1001", "amount": 500, "path": []},
        config=config,
        context=context,
    )

    interrupts = result.get("__interrupt__", ())
    assert len(interrupts) == 1
    assert interrupts[0].value["type"] == "refund_approval"
    assert context.support_service.refund_calls == []


def test_resume_approved_refund_with_same_thread_executes_once():
    graph = build_refund_graph()
    context = build_context()
    config = {"configurable": {"thread_id": "refund-approved"}}
    initial = {"order_id": "A1001", "amount": 500, "path": []}

    graph.invoke(initial, config=config, context=context)
    result = graph.invoke(
        Command(resume={"approved": True}),
        config=config,
        context=context,
    )

    assert result["status"] == "退款已提交"
    assert result["path"] == ["request_approval", "execute_refund"]
    assert context.support_service.refund_calls == [("company_001", "A1001")]


def test_resume_rejected_refund_does_not_execute_side_effect():
    graph = build_refund_graph()
    context = build_context()
    config = {"configurable": {"thread_id": "refund-rejected"}}

    graph.invoke(
        {"order_id": "A1001", "amount": 500, "path": []},
        config=config,
        context=context,
    )
    result = graph.invoke(
        Command(resume={"approved": False}),
        config=config,
        context=context,
    )

    assert result["status"] == "退款已拒绝"
    assert result["path"] == ["request_approval", "reject_refund"]
    assert context.support_service.refund_calls == []
