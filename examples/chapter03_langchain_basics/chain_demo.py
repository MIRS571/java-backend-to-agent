"""Offline LangChain examples for messages, prompts, LCEL, and parsers."""

from __future__ import annotations

import asyncio
from collections.abc import Iterator

from langchain_core.language_models.fake_chat_models import FakeListChatModel
from langchain_core.messages import BaseMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate


def build_prompt() -> ChatPromptTemplate:
    """Create the prompt contract used by every offline chain."""

    return ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "你是企业售后助手。只根据用户问题给出简洁的下一步建议。",
            ),
            ("human", "{question}"),
        ]
    )


def build_offline_chain(responses: list[str]):
    """Compose prompt -> fake chat model -> string parser with LCEL."""

    model = FakeListChatModel(responses=responses)
    parser = StrOutputParser()
    return build_prompt() | model | parser


def inspect_formatted_messages(question: str) -> list[BaseMessage]:
    """Show the messages produced before any model is invoked."""

    prompt_value = build_prompt().invoke({"question": question})
    return prompt_value.to_messages()


def invoke_once(question: str) -> str:
    """Run one synchronous chain invocation."""

    chain = build_offline_chain(["请先确认订单状态，再决定是否可以取消。"])
    return chain.invoke({"question": question})


def invoke_batch(questions: list[str]) -> list[str]:
    """Run multiple independent inputs through one chain."""

    responses = [
        f"第 {index} 个问题已进入售后处理流程。"
        for index in range(1, len(questions) + 1)
    ]
    chain = build_offline_chain(responses)
    return chain.batch([{"question": question} for question in questions])


async def invoke_async(question: str) -> str:
    """Run one asynchronous chain invocation."""

    chain = build_offline_chain(["异步调用已完成，仍需由业务服务确认最终结果。"])
    return await chain.ainvoke({"question": question})


def stream_text(question: str) -> Iterator[str]:
    """Yield parser output chunks from a streaming-capable fake model."""

    chain = build_offline_chain(["流式输出也必须经过应用层的业务校验。"])
    yield from chain.stream({"question": question})


def main() -> None:
    question = "订单已经发货，还能直接取消吗？"
    messages = inspect_formatted_messages(question)

    print("格式化后的 Message：")
    for message in messages:
        print(f"- {message.type}: {message.content}")

    print(f"\ninvoke: {invoke_once(question)}")
    print(f"batch: {invoke_batch([question, '退款需要哪些信息？'])}")
    print(f"ainvoke: {asyncio.run(invoke_async(question))}")
    print(f"stream: {''.join(stream_text(question))}")


if __name__ == "__main__":
    main()
