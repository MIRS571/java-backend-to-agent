from examples.chapter01_agent_basics.context_demo import (
    FakeChatModel,
    Message,
    ask,
    build_api_payload,
    build_messages,
)


def test_payload_keeps_message_order_and_does_not_change_history():
    history: list[Message] = [
        {"role": "user", "content": "订单 A1001 已经发货了吗？"},
        {"role": "assistant", "content": "订单 A1001 当前状态：已发货。"},
    ]

    messages = build_messages(history, "那还能直接取消吗？")
    payload = build_api_payload("offline-demo-model", messages)

    assert [message["role"] for message in messages] == [
        "system",
        "user",
        "assistant",
        "user",
    ]
    assert payload["messages"] == messages
    assert len(history) == 2


def test_follow_up_without_history_reports_missing_context():
    answer = ask(FakeChatModel(), "那还能直接取消吗？")

    assert "缺少订单号和发货状态" in answer["content"]


def test_follow_up_with_history_uses_visible_context():
    history: list[Message] = [
        {"role": "user", "content": "订单 A1001 已经发货了吗？"},
        {"role": "assistant", "content": "订单 A1001 当前状态：已发货。"},
    ]

    answer = ask(FakeChatModel(), "那还能直接取消吗？", history)

    assert "不能直接取消" in answer["content"]
