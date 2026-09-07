from examples.chapter11_quality_security.evaluation_demo import (
    AgentResult,
    EvaluationCase,
    evaluate_case,
    summarize,
)
from examples.chapter11_quality_security.security_demo import (
    ToolRequest,
    TrustedContext,
    authorize_tool,
    safe_trace_metadata,
    trusted_arguments,
)


def test_evaluation_scores_three_dimensions() -> None:
    case = EvaluationCase(
        "case-1", "查询订单", "order_query", "get_order", ("A1001", "已发货")
    )
    score = evaluate_case(
        case,
        AgentResult("order_query", ("get_order",), "订单 A1001 已发货"),
    )
    assert score.score == 1.0


def test_wrong_tool_does_not_hide_correct_answer() -> None:
    case = EvaluationCase("case-1", "问题", "policy_query", "search_policy", ("不能",))
    score = evaluate_case(case, AgentResult("policy_query", (), "不能直接取消"))
    assert score.intent_correct is True
    assert score.tool_correct is False
    assert score.answer_grounded is True


def test_summary_rejects_empty_dataset() -> None:
    try:
        summarize([])
    except ValueError as exc:
        assert str(exc) == "评估集不能为空"
    else:
        raise AssertionError("空评估集必须被拒绝")


def test_unknown_tool_is_rejected() -> None:
    context = TrustedContext("tenant-a", "user-a", frozenset({"refund:write"}))
    decision = authorize_tool(ToolRequest("delete_database", {}), context)
    assert decision.allowed is False
    assert decision.reason == "tool_not_allowed"


def test_refund_requires_role_and_human_approval() -> None:
    request = ToolRequest("request_refund", {"order_id": "A1001"})
    no_role = TrustedContext("tenant-a", "user-a", frozenset())
    assert authorize_tool(request, no_role).reason == "missing_role"

    operator = TrustedContext("tenant-a", "user-a", frozenset({"refund:write"}))
    assert authorize_tool(request, operator).reason == "approval_required"
    assert authorize_tool(request, operator, human_approved=True).allowed is True


def test_trusted_identity_overrides_model_arguments() -> None:
    request = ToolRequest(
        "get_order", {"order_id": "A1001", "tenant_id": "attacker-tenant"}
    )
    context = TrustedContext("tenant-a", "user-a", frozenset())
    arguments = trusted_arguments(request, context)
    assert arguments["tenant_id"] == "tenant-a"
    assert arguments["user_id"] == "user-a"


def test_safe_trace_excludes_raw_tenant_and_content() -> None:
    metadata = safe_trace_metadata(
        tenant_id="tenant-secret",
        request_id="req-1",
        route="order_query",
        latency_ms=42,
    )
    assert metadata["tenant_hash"] != "tenant-secret"
    assert "prompt" not in metadata
    assert "document" not in metadata
