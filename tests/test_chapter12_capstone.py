from dataclasses import replace

import pytest

from examples.chapter12_capstone.request_flow_demo import (
    FLOWS,
    FlowKind,
    Owner,
    describe_flow,
    validate_flow,
)


@pytest.mark.parametrize("kind", list(FlowKind))
def test_all_documented_flows_are_valid(kind: FlowKind) -> None:
    validate_flow(kind, FLOWS[kind])


def test_business_facts_and_refund_remain_in_java() -> None:
    order_steps = {step.name: step for step in FLOWS[FlowKind.ORDER_QUERY]}
    refund_steps = {step.name: step for step in FLOWS[FlowKind.REFUND]}
    assert order_steps["business_query"].owner is Owner.JAVA
    assert refund_steps["transactional_refund"].owner is Owner.JAVA


def test_policy_filter_happens_before_retrieval() -> None:
    steps = FLOWS[FlowKind.POLICY_QUERY]
    names = [step.name for step in steps]
    assert names.index("tenant_filter") < names.index("retrieval")


def test_refund_rejects_idempotency_before_approval() -> None:
    steps = list(FLOWS[FlowKind.REFUND])
    approval_index = next(
        index for index, step in enumerate(steps) if step.name == "human_approval"
    )
    idempotency_index = next(
        index for index, step in enumerate(steps) if step.name == "idempotency"
    )
    steps[approval_index], steps[idempotency_index] = (
        steps[idempotency_index],
        steps[approval_index],
    )
    with pytest.raises(ValueError, match="审批、幂等、事务写入"):
        validate_flow(FlowKind.REFUND, tuple(steps))


def test_model_cannot_replace_java_public_entry() -> None:
    steps = list(FLOWS[FlowKind.ORDER_QUERY])
    steps[0] = replace(steps[0], owner=Owner.PYTHON)
    with pytest.raises(ValueError, match="必须由 Java 边界拥有"):
        validate_flow(FlowKind.ORDER_QUERY, tuple(steps))


def test_describe_flow_exposes_owner_and_responsibility() -> None:
    description = describe_flow(FlowKind.REFUND)
    assert "[java] idempotency" in description
    assert "[human] human_approval" in description
