"""Deterministic structured-output boundary without a live model request."""

from __future__ import annotations

from typing import Literal

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.runnables import Runnable
from pydantic import BaseModel, ConfigDict, Field, field_validator


class UserRequestAnalysis(BaseModel):
    """Validated data that the application expects from the model."""

    model_config = ConfigDict(extra="forbid")

    intent: Literal["order_query", "refund", "complaint", "other"] = Field(
        description="用户意图，只能选择一个已知分类"
    )
    order_id: str | None = Field(
        default=None,
        description="用户明确提到的订单号，没有则为 null",
    )
    summary: str = Field(
        min_length=1,
        max_length=100,
        description="对用户诉求的简短概括",
    )

    @field_validator("order_id")
    @classmethod
    def normalize_order_id(cls, value: str | None) -> str | None:
        """Normalize an optional ID and reject blank IDs."""

        if value is None:
            return None
        cleaned = value.strip().upper()
        if not cleaned:
            raise ValueError("order_id 不能只包含空格")
        return cleaned


def create_structured_model(
    model: BaseChatModel,
) -> Runnable[object, UserRequestAnalysis]:
    """Attach the response schema to a tool-capable chat model."""

    return model.with_structured_output(UserRequestAnalysis)


def validate_offline_payload(payload: dict[str, object]) -> UserRequestAnalysis:
    """Exercise the same Pydantic boundary with deterministic local data."""

    return UserRequestAnalysis.model_validate(payload)


def main() -> None:
    analysis = validate_offline_payload(
        {
            "intent": "refund",
            "order_id": " a1001 ",
            "summary": "用户询问订单退款流程",
        }
    )
    print(analysis.model_dump())


if __name__ == "__main__":
    main()
