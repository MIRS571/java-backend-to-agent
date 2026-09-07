"""Shared runtime dependencies for the chapter 8 examples."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class FakeSupportService:
    """A deterministic stand-in for a Java business service or database client."""

    refund_calls: list[tuple[str, str]] = field(default_factory=list)

    def query_order_status(self, tenant_id: str, order_id: str) -> str:
        """Return a tenant-scoped order status without using a real database."""

        if tenant_id == "company_001" and order_id == "A1001":
            return "已发货"
        return "订单不存在"

    def execute_refund(self, tenant_id: str, order_id: str) -> str:
        """Record a refund side effect so tests can verify execution count."""

        self.refund_calls.append((tenant_id, order_id))
        return "退款已提交"


@dataclass(frozen=True)
class AgentContext:
    """Trusted, per-invocation context injected into graph nodes."""

    tenant_id: str
    support_service: FakeSupportService
