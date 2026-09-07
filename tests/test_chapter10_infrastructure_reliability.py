from pathlib import Path

import pytest
import yaml

from examples.chapter10_infrastructure_reliability.reliability_demo import (
    IdempotencyConflictError,
    InMemoryIdempotencyStore,
    TemporaryReadError,
    request_fingerprint,
    retry_read,
    scoped_key,
)

ROOT = Path(__file__).resolve().parents[1]


def test_scoped_key_contains_namespace_tenant_and_resource():
    assert (
        scoped_key("rate", "company_001", "user_001")
        == "rate:company_001:user_001"
    )


@pytest.mark.parametrize("invalid", ["", "contains:separator"])
def test_scoped_key_rejects_ambiguous_components(invalid):
    with pytest.raises(ValueError):
        scoped_key("rate", "company_001", invalid)


def test_fingerprint_is_stable_across_dictionary_order():
    left = request_fingerprint({"order_id": "A1001", "amount": 500})
    right = request_fingerprint({"amount": 500, "order_id": "A1001"})

    assert left == right


def test_idempotency_reuses_result_without_repeating_operation():
    store = InMemoryIdempotencyStore()
    calls = 0

    def operation():
        nonlocal calls
        calls += 1
        return {"status": "accepted"}

    payload = {"order_id": "A1001", "amount": 500}
    first = store.execute_once("refund:tenant:req-1", payload, operation)
    second = store.execute_once("refund:tenant:req-1", payload, operation)

    assert first == second
    assert calls == 1


def test_idempotency_rejects_same_key_with_different_payload():
    store = InMemoryIdempotencyStore()
    store.execute_once("key", {"amount": 100}, lambda: {"status": "ok"})

    with pytest.raises(IdempotencyConflictError):
        store.execute_once(
            "key", {"amount": 200}, lambda: {"status": "wrong"}
        )


@pytest.mark.asyncio
async def test_retry_read_recovers_from_declared_temporary_failures():
    attempts = 0

    async def operation():
        nonlocal attempts
        attempts += 1
        if attempts < 3:
            raise TemporaryReadError("temporary")
        return "ok"

    assert await retry_read(operation, max_attempts=3) == "ok"
    assert attempts == 3


@pytest.mark.asyncio
async def test_retry_read_stops_at_attempt_limit():
    attempts = 0

    async def operation():
        nonlocal attempts
        attempts += 1
        raise TemporaryReadError("temporary")

    with pytest.raises(TemporaryReadError):
        await retry_read(operation, max_attempts=2)

    assert attempts == 2


def test_enterprise_compose_has_scoped_ports_and_named_volumes():
    compose = yaml.safe_load(
        (ROOT / "infra/enterprise/compose.yml").read_text(encoding="utf-8")
    )

    assert set(compose["services"]) == {"postgres", "redis", "qdrant"}
    for service in compose["services"].values():
        for port in service["ports"]:
            assert port.startswith("127.0.0.1:")
    assert set(compose["volumes"]) == {
        "postgres-data",
        "redis-data",
        "qdrant-data",
    }
