"""Deterministic idempotency and retry patterns without external services."""

from __future__ import annotations

import asyncio
import hashlib
import json
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Any


class IdempotencyConflictError(ValueError):
    """The same key was reused for a different logical request."""


class TemporaryReadError(RuntimeError):
    """A transient failure that a read operation may retry."""


def scoped_key(namespace: str, tenant_id: str, resource_id: str) -> str:
    """Build a Redis-style key while preventing ambiguous separators."""

    components = (namespace, tenant_id, resource_id)
    if any(not item or ":" in item for item in components):
        raise ValueError("Key 组成部分不能为空或包含冒号")
    return ":".join(components)


def request_fingerprint(payload: dict[str, Any]) -> str:
    """Hash canonical JSON so key reuse with changed input can be rejected."""

    canonical = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class CompletedRecord:
    fingerprint: str
    result: dict[str, Any]


class InMemoryIdempotencyStore:
    """Model the completed-result part of a production idempotency store."""

    def __init__(self) -> None:
        self._records: dict[str, CompletedRecord] = {}

    def execute_once(
        self,
        key: str,
        payload: dict[str, Any],
        operation: Callable[[], dict[str, Any]],
    ) -> dict[str, Any]:
        fingerprint = request_fingerprint(payload)
        existing = self._records.get(key)
        if existing is not None:
            if existing.fingerprint != fingerprint:
                raise IdempotencyConflictError(
                    "同一幂等键不能用于不同请求"
                )
            return existing.result

        result = operation()
        self._records[key] = CompletedRecord(fingerprint, result)
        return result


async def retry_read(
    operation: Callable[[], Awaitable[str]],
    *,
    max_attempts: int = 3,
    base_delay_seconds: float = 0,
) -> str:
    """Retry only a declared transient read failure with exponential delay."""

    if max_attempts < 1:
        raise ValueError("max_attempts 必须至少为 1")

    for attempt in range(max_attempts):
        try:
            return await operation()
        except TemporaryReadError:
            if attempt == max_attempts - 1:
                raise
            await asyncio.sleep(base_delay_seconds * (2**attempt))

    raise AssertionError("unreachable")


async def main() -> None:
    store = InMemoryIdempotencyStore()
    calls = 0

    def refund() -> dict[str, Any]:
        nonlocal calls
        calls += 1
        return {"status": "accepted", "refund_id": "refund-001"}

    key = scoped_key("refund", "company_001", "request-001")
    payload = {"order_id": "A1001", "amount": 500}
    first = store.execute_once(key, payload, refund)
    second = store.execute_once(key, payload, refund)

    attempts = 0

    async def unstable_read() -> str:
        nonlocal attempts
        attempts += 1
        if attempts < 3:
            raise TemporaryReadError("temporary")
        return "订单已发货"

    read_result = await retry_read(unstable_read)
    print(f"两次幂等请求结果相同：{first == second}")
    print(f"退款实际执行次数：{calls}")
    print(f"读取重试次数：{attempts}，结果：{read_result}")


if __name__ == "__main__":
    asyncio.run(main())
