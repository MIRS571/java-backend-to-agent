"""在工具边界重新注入可信身份，并生成最小化追踪元数据。"""

from dataclasses import dataclass
from hashlib import sha256
from typing import Any


@dataclass(frozen=True)
class TrustedContext:
    tenant_id: str
    user_id: str
    roles: frozenset[str]


@dataclass(frozen=True)
class ToolRequest:
    name: str
    arguments: dict[str, Any]


@dataclass(frozen=True)
class PolicyDecision:
    allowed: bool
    reason: str


ALLOWED_TOOLS = {"get_order", "search_policy", "request_refund"}


def authorize_tool(
    request: ToolRequest,
    context: TrustedContext,
    *,
    human_approved: bool = False,
) -> PolicyDecision:
    """模型只能提出工具请求，权限由确定性代码决定。"""
    if request.name not in ALLOWED_TOOLS:
        return PolicyDecision(False, "tool_not_allowed")
    if request.name == "request_refund" and "refund:write" not in context.roles:
        return PolicyDecision(False, "missing_role")
    if request.name == "request_refund" and not human_approved:
        return PolicyDecision(False, "approval_required")
    return PolicyDecision(True, "allowed")


def trusted_arguments(
    request: ToolRequest,
    context: TrustedContext,
) -> dict[str, Any]:
    """忽略模型提供的身份字段，始终使用认证链路中的可信值。"""
    return {
        **request.arguments,
        "tenant_id": context.tenant_id,
        "user_id": context.user_id,
    }


def safe_trace_metadata(
    *, tenant_id: str, request_id: str, route: str, latency_ms: int
) -> dict[str, str | int]:
    """保留排障所需索引，不记录 Prompt、文档正文或密钥。"""
    tenant_hash = sha256(tenant_id.encode("utf-8")).hexdigest()[:12]
    return {
        "request_id": request_id,
        "tenant_hash": tenant_hash,
        "route": route,
        "latency_ms": latency_ms,
    }
