"""用确定性数据描述综合项目的三条核心请求流程。"""

from dataclasses import dataclass
from enum import StrEnum


class Owner(StrEnum):
    CLIENT = "client"
    JAVA = "java"
    PYTHON = "python"
    INFRASTRUCTURE = "infrastructure"
    HUMAN = "human"


class FlowKind(StrEnum):
    ORDER_QUERY = "order_query"
    POLICY_QUERY = "policy_query"
    REFUND = "refund"


@dataclass(frozen=True)
class FlowStep:
    name: str
    owner: Owner
    responsibility: str


COMMON_PREFIX = (
    FlowStep("public_entry", Owner.JAVA, "认证用户并生成 request_id"),
    FlowStep("trusted_context", Owner.JAVA, "传递可信 tenant_id 与 user_id"),
    FlowStep("graph_route", Owner.PYTHON, "识别意图并选择显式工作流分支"),
)

FLOWS: dict[FlowKind, tuple[FlowStep, ...]] = {
    FlowKind.ORDER_QUERY: (
        *COMMON_PREFIX,
        FlowStep("business_query", Owner.JAVA, "按租户和用户读取订单事实"),
        FlowStep("answer", Owner.PYTHON, "基于业务事实生成回答"),
        FlowStep("sse_relay", Owner.JAVA, "无缓冲转发公开 SSE 事件"),
    ),
    FlowKind.POLICY_QUERY: (
        *COMMON_PREFIX,
        FlowStep("tenant_filter", Owner.INFRASTRUCTURE, "在 Qdrant 查询内隔离租户"),
        FlowStep("retrieval", Owner.PYTHON, "召回、融合、重排并格式化引用"),
        FlowStep("answer", Owner.PYTHON, "仅根据知识上下文生成回答"),
        FlowStep("sse_relay", Owner.JAVA, "无缓冲转发公开 SSE 事件"),
    ),
    FlowKind.REFUND: (
        *COMMON_PREFIX,
        FlowStep("eligibility", Owner.JAVA, "读取订单并校验退款资格"),
        FlowStep("interrupt", Owner.PYTHON, "保存 Checkpoint 并暂停 Graph"),
        FlowStep("human_approval", Owner.HUMAN, "明确批准或拒绝退款"),
        FlowStep("idempotency", Owner.JAVA, "声明稳定幂等键并检查请求指纹"),
        FlowStep("transactional_refund", Owner.JAVA, "原子更新业务订单状态"),
        FlowStep("result", Owner.PYTHON, "恢复 Graph 并形成最终结果"),
    ),
}


def validate_flow(kind: FlowKind, steps: tuple[FlowStep, ...]) -> None:
    """验证教学流程中不能被颠倒的安全顺序。"""
    names = [step.name for step in steps]
    if names[:3] != ["public_entry", "trusted_context", "graph_route"]:
        raise ValueError("请求必须先通过 Java 公共入口和可信身份链路")
    if steps[0].owner is not Owner.JAVA or steps[1].owner is not Owner.JAVA:
        raise ValueError("公共入口和可信身份必须由 Java 边界拥有")
    if (
        kind is FlowKind.POLICY_QUERY
        and names.index("tenant_filter") > names.index("retrieval")
    ):
        raise ValueError("租户过滤必须发生在召回之前")
    if kind is FlowKind.REFUND and not (
        names.index("human_approval")
        < names.index("idempotency")
        < names.index("transactional_refund")
    ):
        raise ValueError("退款必须按审批、幂等、事务写入的顺序执行")


def describe_flow(kind: FlowKind) -> str:
    steps = FLOWS[kind]
    validate_flow(kind, steps)
    lines = [
        f"{index}. [{step.owner}] {step.name}: {step.responsibility}"
        for index, step in enumerate(steps, 1)
    ]
    return "\n".join(lines)


def main() -> None:
    for kind in FlowKind:
        print(f"\n=== {kind} ===")
        print(describe_flow(kind))


if __name__ == "__main__":
    main()
