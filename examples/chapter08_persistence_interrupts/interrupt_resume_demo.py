"""Pause a refund graph for approval and resume it from a checkpoint."""

from __future__ import annotations

import operator
from typing import Annotated, Literal, TypedDict

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.runtime import Runtime
from langgraph.types import Command, interrupt

from .support_context import AgentContext, FakeSupportService


class RefundState(TypedDict, total=False):
    """Serializable workflow state for one refund request."""

    order_id: str
    amount: int
    approved: bool
    status: str
    path: Annotated[list[str], operator.add]


def request_approval(state: RefundState) -> dict[str, object]:
    """Pause and expose only JSON-serializable review information."""

    decision = interrupt(
        {
            "type": "refund_approval",
            "order_id": state["order_id"],
            "amount": state["amount"],
            "question": "是否批准这笔退款？",
        }
    )
    if not isinstance(decision, dict) or not isinstance(
        decision.get("approved"), bool
    ):
        raise ValueError("审批结果必须包含布尔类型的 approved 字段")
    return {
        "approved": decision["approved"],
        "path": ["request_approval"],
    }


def route_decision(state: RefundState) -> Literal["execute_refund", "reject_refund"]:
    """Route with deterministic business control after human input."""

    if state["approved"]:
        return "execute_refund"
    return "reject_refund"


def execute_refund(
    state: RefundState,
    runtime: Runtime[AgentContext],
) -> dict[str, object]:
    """Run the side effect only after approval has completed."""

    status = runtime.context.support_service.execute_refund(
        tenant_id=runtime.context.tenant_id,
        order_id=state["order_id"],
    )
    return {"status": status, "path": ["execute_refund"]}


def reject_refund(state: RefundState) -> dict[str, object]:
    """Finish without calling the refund service."""

    return {"status": "退款已拒绝", "path": ["reject_refund"]}


def build_refund_graph(checkpointer=None):
    """Compile an interruptible graph; a checkpointer is required to resume."""

    builder = StateGraph(RefundState, context_schema=AgentContext)
    builder.add_node("request_approval", request_approval)
    builder.add_node("execute_refund", execute_refund)
    builder.add_node("reject_refund", reject_refund)
    builder.add_edge(START, "request_approval")
    builder.add_conditional_edges("request_approval", route_decision)
    builder.add_edge("execute_refund", END)
    builder.add_edge("reject_refund", END)
    saver = checkpointer if checkpointer is not None else InMemorySaver()
    return builder.compile(checkpointer=saver)


def main() -> None:
    service = FakeSupportService()
    context = AgentContext("company_001", service)
    graph = build_refund_graph()
    config = {"configurable": {"thread_id": "refund-001"}}

    paused_result = graph.invoke(
        {
            "order_id": "A1001",
            "amount": 500,
            "path": [],
        },
        config=config,
        context=context,
    )
    interrupts = paused_result.get("__interrupt__", ())
    print(f"暂停原因：{interrupts[0].value}")
    print(f"暂停时退款调用次数：{len(service.refund_calls)}")

    resumed_result = graph.invoke(
        Command(resume={"approved": True}),
        config=config,
        context=context,
    )
    print(f"恢复后状态：{resumed_result['status']}")
    print(f"恢复后路径：{resumed_result['path']}")
    print(f"恢复后退款调用次数：{len(service.refund_calls)}")


if __name__ == "__main__":
    main()
