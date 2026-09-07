"""用确定性规则完成一个可在 CI 运行的 Agent 离线评估。"""

from dataclasses import dataclass


@dataclass(frozen=True)
class EvaluationCase:
    case_id: str
    question: str
    expected_intent: str
    expected_tool: str | None
    required_terms: tuple[str, ...]


@dataclass(frozen=True)
class AgentResult:
    intent: str
    tool_calls: tuple[str, ...]
    answer: str


@dataclass(frozen=True)
class CaseScore:
    case_id: str
    intent_correct: bool
    tool_correct: bool
    answer_grounded: bool

    @property
    def score(self) -> float:
        return sum((self.intent_correct, self.tool_correct, self.answer_grounded)) / 3


def evaluate_case(case: EvaluationCase, result: AgentResult) -> CaseScore:
    """分别评价路由、工具轨迹和答案事实，不把它们混成一个模糊分数。"""
    expected_tools = () if case.expected_tool is None else (case.expected_tool,)
    normalized_answer = result.answer.casefold()
    return CaseScore(
        case_id=case.case_id,
        intent_correct=result.intent == case.expected_intent,
        tool_correct=result.tool_calls == expected_tools,
        answer_grounded=all(
            term.casefold() in normalized_answer for term in case.required_terms
        ),
    )


def summarize(scores: list[CaseScore]) -> dict[str, float]:
    if not scores:
        raise ValueError("评估集不能为空")
    size = len(scores)
    return {
        "intent_accuracy": sum(item.intent_correct for item in scores) / size,
        "tool_accuracy": sum(item.tool_correct for item in scores) / size,
        "grounded_rate": sum(item.answer_grounded for item in scores) / size,
        "overall_score": sum(item.score for item in scores) / size,
    }


def main() -> None:
    cases = [
        EvaluationCase(
            case_id="order-001",
            question="查询订单 A1001",
            expected_intent="order_query",
            expected_tool="get_order",
            required_terms=("A1001", "已发货"),
        ),
        EvaluationCase(
            case_id="policy-001",
            question="已经发货还能直接取消吗？",
            expected_intent="policy_query",
            expected_tool="search_policy",
            required_terms=("不能直接取消",),
        ),
    ]
    results = [
        AgentResult("order_query", ("get_order",), "订单 A1001 当前已发货。"),
        AgentResult("policy_query", ("search_policy",), "已发货订单不能直接取消。"),
    ]
    paired_results = zip(cases, results, strict=True)
    report = summarize(
        [evaluate_case(case, result) for case, result in paired_results]
    )
    for metric, value in report.items():
        print(f"{metric}: {value:.0%}")


if __name__ == "__main__":
    main()
