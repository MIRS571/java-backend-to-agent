"""Show that conversation context is explicit input, not hidden model memory."""

from __future__ import annotations

from typing import TypedDict


class Message(TypedDict):
    """A minimal text message accepted by the offline demo model."""

    role: str
    content: str


SYSTEM_MESSAGE: Message = {
    "role": "system",
    "content": "你是售后助手。信息不足时必须明确说明缺少上下文。",
}


def build_messages(history: list[Message], question: str) -> list[Message]:
    """Build the complete context visible to the model for one request."""

    return [
        SYSTEM_MESSAGE.copy(),
        *(message.copy() for message in history),
        {"role": "user", "content": question},
    ]


def build_api_payload(model: str, messages: list[Message]) -> dict[str, object]:
    """Build a provider-neutral teaching payload without sending a request."""

    return {
        "model": model,
        "messages": [message.copy() for message in messages],
    }


class FakeChatModel:
    """Return deterministic answers so the example needs no API key or network."""

    def complete(self, messages: list[Message]) -> Message:
        question = next(
            message["content"]
            for message in reversed(messages)
            if message["role"] == "user"
        )
        visible_context = "\n".join(message["content"] for message in messages)

        if "A1001" in question and "发货" in question:
            answer = "订单 A1001 当前状态：已发货。"
        elif (
            "取消" in question
            and "A1001" in visible_context
            and "已发货" in visible_context
        ):
            answer = "订单 A1001 已发货，不能直接取消；需要进入退货流程。"
        elif "取消" in question:
            answer = "缺少订单号和发货状态，暂时无法判断是否可以直接取消。"
        else:
            answer = "当前离线示例只处理订单状态与取消问题。"

        return {"role": "assistant", "content": answer}


def ask(
    model: FakeChatModel,
    question: str,
    history: list[Message] | None = None,
) -> Message:
    """Send one complete request to the model."""

    messages = build_messages(history or [], question)
    return model.complete(messages)
