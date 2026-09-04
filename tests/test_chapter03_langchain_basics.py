import asyncio

import pytest
from langchain_core.messages import HumanMessage, SystemMessage

from examples.chapter03_langchain_basics.chain_demo import (
    inspect_formatted_messages,
    invoke_async,
    invoke_batch,
    invoke_once,
    stream_text,
)
from examples.chapter03_langchain_basics.model_factory import (
    ModelSettings,
    create_chat_model,
)


def test_prompt_formats_system_and_human_messages():
    messages = inspect_formatted_messages("订单能取消吗？")

    assert isinstance(messages[0], SystemMessage)
    assert isinstance(messages[1], HumanMessage)
    assert messages[1].content == "订单能取消吗？"


def test_lcel_chain_invokes_model_and_parses_text():
    result = invoke_once("订单能取消吗？")

    assert result == "请先确认订单状态，再决定是否可以取消。"


def test_batch_keeps_one_output_per_input():
    result = invoke_batch(["第一个问题", "第二个问题"])

    assert result == [
        "第 1 个问题已进入售后处理流程。",
        "第 2 个问题已进入售后处理流程。",
    ]


def test_async_and_stream_invocation_return_parsed_text():
    async_result = asyncio.run(invoke_async("异步问题"))
    stream_result = "".join(stream_text("流式问题"))

    assert async_result == "异步调用已完成，仍需由业务服务确认最终结果。"
    assert stream_result == "流式输出也必须经过应用层的业务校验。"


def test_model_factory_only_constructs_a_client_without_a_request():
    settings = ModelSettings(
        model="offline-test-model",
        api_key="not-used-in-test",
        timeout=15,
        max_retries=1,
    )

    model = create_chat_model(settings)

    assert model.model_name == "offline-test-model"
    assert model.request_timeout == 15
    assert model.max_retries == 1


def test_model_settings_is_immutable():
    settings = ModelSettings(
        model="offline-test-model",
        api_key="not-used-in-test",
    )

    with pytest.raises(AttributeError):
        settings.model = "other-model"
