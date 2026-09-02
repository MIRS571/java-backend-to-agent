"""Run the Chapter 1 context demonstration."""

from __future__ import annotations

import json

from examples.chapter01_agent_basics.context_demo import (
    FakeChatModel,
    Message,
    ask,
    build_api_payload,
    build_messages,
)


def main() -> None:
    model = FakeChatModel()
    history: list[Message] = []

    first_question = "订单 A1001 已经发货了吗？"
    first_answer = ask(model, first_question)
    history.extend(
        [
            {"role": "user", "content": first_question},
            first_answer,
        ]
    )

    follow_up = "那还能直接取消吗？"
    without_history = ask(model, follow_up)
    with_history = ask(model, follow_up, history)

    payload = build_api_payload(
        model="offline-demo-model",
        messages=build_messages(history, follow_up),
    )

    print("第一次回答：", first_answer["content"])
    print("不带历史追问：", without_history["content"])
    print("带历史追问：", with_history["content"])
    print("\n带历史请求的 JSON：")
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
