# 第 3 章：LangChain 模型、Message、Prompt、LCEL、Parser 与调用方式

> 本章状态：内容完成。最近复核：2026-09-08。关键依赖：LangChain 1.4.0、langchain-core 1.6.1、langchain-openai 1.6.0、Pydantic 2.13.5、Python 3.12。

## 1. 本章解决的问题

第 1 章说明了模型调用的真实边界：应用要组织 Message、调用模型、检查输出。问题是，不同模型提供商的 SDK、消息格式、同步/异步调用和流式接口并不完全相同。项目一旦同时有 Prompt、模型、解析、检索或工具步骤，直接把厂商 SDK 调用散落在业务代码中，就很难看清数据从哪里来、变成了什么、在哪一步失败。

LangChain 的核心作用不是“替模型思考”，而是提供一组可组合的应用接口。本章建立一个稳定的最小链路：

```text
输入字典 -> Prompt -> Message -> Chat Model -> AIMessage -> Parser -> 业务可用值
```

完成本章后，应当能够区分：

- `Message` 是模型交互的数据对象，不是业务实体；
- `ChatPromptTemplate` 把输入变量格式化为消息；
- Chat Model 接收消息并返回 `AIMessage`；
- LCEL 的 `|` 连接可运行步骤，而不是 Python 的位运算；
- `StrOutputParser` 只提取文本，不验证业务事实；
- 应该在何时选择 `invoke`、`ainvoke`、`batch` 和 `stream`。

本章不讲 Tool Calling、结构化输出、RAG、Agent 循环或图编排。它们都建立在本章的输入/输出链路上，后续章节按顺序展开。

## 2. 背景与技术动机

一个真实 Agent API 通常至少有三类变化来源：模型提供商替换、Prompt 迭代、模型输出形状变化。若 Controller 或 Service 直接拼字符串并调用厂商 SDK，变化会扩散到业务层，测试也会被真实网络和费用绑定。

LangChain 把这些职责拆开：

| 对象 | 要解决的问题 | 不解决什么 |
| --- | --- | --- |
| `BaseMessage` / `AIMessage` | 统一角色化消息和模型响应 | 不证明消息内容真实或有权限 |
| `ChatPromptTemplate` | 将受控变量格式化成消息序列 | 不替代安全策略或业务校验 |
| Chat Model | 适配某个模型提供商的调用接口 | 不执行订单、支付等确定性业务 |
| `Runnable` / LCEL | 组合步骤、统一调用方式和追踪边界 | 不自动设计正确的业务流程 |
| Output Parser | 把模型输出转成下游需要的形状 | 不保证结构化结果本身正确 |

因此，LangChain 是**应用编排层的抽象**。它减少模型接入和步骤组合的重复代码，但不会取消模型的不确定性，也不会替代 Java 服务的权限、事务或领域规则。

## 3. 核心心智模型

### 3.1 Chat Model 的输入和输出不是普通字符串

现代对话模型通常接收 Message 序列，返回 `AIMessage`。下面的两条消息分别表达应用指令和用户输入：

```python
from langchain_core.messages import HumanMessage, SystemMessage

messages = [
    SystemMessage(content="你是企业售后助手。"),
    HumanMessage(content="订单已经发货，还能直接取消吗？"),
]
```

`AIMessage` 的 `content` 常包含自然语言文本，但响应还可能携带 `tool_calls`、usage metadata、finish reason 或多模态内容。把完整 `AIMessage` 直接当成字符串，是后续解析错误的常见来源。

LangChain 中的 Chat Model 属于 `Runnable`：它可以被调用、批量调用、异步调用或流式调用。真实模型常使用提供商集成包，例如 `langchain-openai` 提供 `ChatOpenAI`；离线测试则应使用 Fake Model，而不是发起付费请求。

### 3.2 Prompt 是“输入合同”，不是一段普通字符串

`ChatPromptTemplate` 声明模型调用需要哪些变量，以及这些变量被放入什么角色、什么位置：

```python
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你是企业售后助手。"),
        ("human", "{question}"),
    ]
)

prompt_value = prompt.invoke(
    {"question": "订单已经发货，还能直接取消吗？"}
)
```

这里 `prompt.invoke()` 的输出不是最终文本，而是 `ChatPromptValue`。调用 `prompt_value.to_messages()` 后，才能得到已替换变量的 `SystemMessage` 与 `HumanMessage`。

模板变量缺失时会在格式化阶段失败，这是有价值的早期错误。若想让花括号作为文本出现，需要写成 `{{` 和 `}}`；否则模板会把它误认为变量名。

### 3.3 LCEL 用数据流表达组合关系

LCEL（LangChain Expression Language）使用 `|` 将前一步的输出连接为后一步的输入：

```python
chain = prompt | model | StrOutputParser()
```

这句的运行顺序是：先把 `dict` 格式化为 `ChatPromptValue`，再交给 `model`，最后把 `AIMessage` 解析为 `str`。它不是并行执行，也不是模型调用发生在定义 `chain` 的这一行；真正执行发生在 `invoke()`、`ainvoke()`、`batch()` 或 `stream()`。

`|` 是 Python 的运算符重载：LangChain 的 `Runnable` 对象实现了相应协议，所以能被组合。它最接近 Java 中把多个 `Function` 或 Reactor 操作符串成数据管道，但 LCEL 的每一段还会携带输入/输出模式、配置和追踪信息。

### 3.4 Parser 只做“形状转换”

`StrOutputParser()` 接收模型输出并提取文本，链路最终结果才变成 `str`。它适合下一步只需要可展示文本的场景：

```python
answer: str = chain.invoke({"question": "退款需要哪些信息？"})
```

它不检查答案是否有证据、是否符合退款规则，也不会将文本变成受约束的领域对象。需要 Pydantic Schema 或模型原生结构化输出时，应进入第 4 章，而不是在本章用字符串解析器硬凑 JSON。

## 4. 输入、输出与执行流程

本章离线示例的完整运行顺序如下。Fake Model 只是替代网络模型，使每一步可重复观察；生产中该节点会替换为 `ChatOpenAI` 或其他提供商的 Chat Model。

```mermaid
flowchart LR
    Input[输入 dict<br/>{question: ...}] --> Prompt[ChatPromptTemplate]
    Prompt --> Value[ChatPromptValue<br/>已格式化的 Message]
    Value --> Model[Chat Model<br/>FakeListChatModel / ChatOpenAI]
    Model --> AI[AIMessage 或 Chunk]
    AI --> Parser[StrOutputParser]
    Parser --> Output[输出 str]

    Config[可信配置<br/>模型、密钥、超时、重试] -. 创建客户端 .-> Model
    Output -. 业务校验后 .-> Service[应用 Service]
```

运行时逐步展开：

1. 上层应用传入 `{"question": ...}`；它是链的输入合同，而不是 HTTP 请求本身。
2. `ChatPromptTemplate` 检查变量、替换模板，并输出 `ChatPromptValue`。
3. Chat Model 把 Message 序列交给模型提供商，并返回 `AIMessage` 或流式 Chunk。
4. `StrOutputParser` 提取文本内容，输出 `str`。
5. 应用 Service 仍须检查租户、权限、业务事实和高风险操作；LangChain 不拥有这些职责。

## 5. 最小可运行示例

完整示例位于 [`examples/chapter03_langchain_basics`](https://github.com/MIRS571/java-backend-to-agent/tree/main/examples/chapter03_langchain_basics)。在仓库根目录运行：

```powershell
uv run python -m examples.chapter03_langchain_basics.chain_demo
```

示例依次输出格式化后的 Message、同步调用、批量调用、异步调用和流式输出。它不读取 `.env`，不访问网络，也不会调用真实模型。

核心组合代码位于 [`chain_demo.py`](https://github.com/MIRS571/java-backend-to-agent/blob/main/examples/chapter03_langchain_basics/chain_demo.py)：

```python
def build_offline_chain(responses: list[str]):
    model = FakeListChatModel(responses=responses)
    parser = StrOutputParser()
    return build_prompt() | model | parser
```

这段代码只**定义**链。下面才是执行链：

```python
answer = chain.invoke(
    {"question": "订单已经发货，还能直接取消吗？"}
)
```

真实模型客户端的创建边界位于 [`model_factory.py`](https://github.com/MIRS571/java-backend-to-agent/blob/main/examples/chapter03_langchain_basics/model_factory.py)。它只构造 `ChatOpenAI` 对象，不在构造时发送模型请求：

```python
return ChatOpenAI(
    model=settings.model,
    api_key=settings.api_key,
    base_url=settings.base_url,
    timeout=settings.timeout,
    max_retries=settings.max_retries,
)
```

`ModelSettings` 必须来自可信应用配置，不能来自用户消息。模型名、密钥、基础地址、超时和重试都属于客户端配置；用户问题只属于一次调用的输入。

## 6. 关键 API 解释

| API | 接收什么 | 返回什么 / 何时执行 | 关键边界 |
| --- | --- | --- | --- |
| `ChatPromptTemplate.from_messages()` | 角色与模板的序列 | Prompt Runnable | 定义模板时不调用模型 |
| `prompt.invoke(dict)` | 模板变量 | `ChatPromptValue` | 缺少变量会在此阶段报错 |
| `prompt_value.to_messages()` | 无额外输入 | `list[BaseMessage]` | 用于观察最终消息，不是必须的生产步骤 |
| `ChatOpenAI(...)` | 可信客户端配置 | Chat Model 对象 | 创建对象不等于发起网络调用 |
| `model.invoke(messages)` | 字符串或 Message 序列 | 通常为 `AIMessage` | 内容可能不止纯文本 |
| `StrOutputParser()` | 模型输出 | Parser Runnable | 只提取文本，不做业务验证 |
| `a | b` | 两个兼容的 Runnable | 组合后的 RunnableSequence | 定义数据流，不立即执行 |
| `chain.invoke(input)` | 单个输入 | 最终输出 | 适合同步脚本或同步边界 |
| `await chain.ainvoke(input)` | 单个输入 | 最终输出 | 只能在 `async def` 中使用 |
| `chain.batch(inputs)` | 多个独立输入 | 输出列表 | 默认实现适合 I/O；不等于提供商原生批处理 |
| `chain.stream(input)` | 单个输入 | 输出 Chunk 迭代器 | 能否逐块返回取决于链中每个步骤 |

选择调用方式时，先看宿主环境和下游能力：

| 场景 | 首选 | 原因 |
| --- | --- | --- |
| 命令行脚本、一次性测试 | `invoke` | 调用和错误边界最直接 |
| FastAPI 异步路由、异步模型客户端 | `ainvoke` | 不阻塞事件循环等待 I/O |
| 多个互不依赖的离线任务 | `batch` | 统一管理多个输入；仍需限制并发 |
| 聊天界面需要逐步显示文本 | `stream` / `astream` | 将模型 Chunk 转换为后续 SSE 事件 |

第 9 章会把 `astream` 的输出真正封装为 SSE；本章只先建立“Chunk 不是最终业务结果”的认识。

## 7. Java / Spring 类比

| LangChain 对象 | Java / Spring 类比 | 类比的边界 |
| --- | --- | --- |
| `BaseMessage` | 调用模型服务的请求 DTO 中的一项 | 它表达对话角色，不是 JPA Entity 或业务事实 |
| `ChatPromptTemplate` | 构造下游请求的模板/Assembler | 不应承担权限与领域决策 |
| `ChatOpenAI` | 封装远程协议的 HTTP Client | LLM 输出不是确定性的第三方 REST DTO |
| `Runnable` | `Function<I, O>` 或一段 Reactor 链 | Runnable 还统一暴露调用、配置和追踪接口 |
| `prompt | model | parser` | `requestMapper -> client -> responseMapper` | 每段的输入、输出可能是 Message、Chunk 等非 HTTP DTO |
| `StrOutputParser` | 从第三方响应提取展示字段的 Mapper | 不等于 Bean Validation 或领域校验 |
| `batch` | 并发处理一批独立任务 | 默认不表示远端只收到一条批量 API 请求 |

Java 后端仍然应该拥有身份、授权、事务和关系型业务事实。Python/LangChain 层负责组织模型输入、检索、工具编排与模型输出处理；两者通过明确接口协作。

## 8. Demo 与企业级写法

| 当前 Demo | 企业级 Agent 服务应补充 |
| --- | --- |
| `FakeListChatModel` 固定返回值 | 真实提供商客户端、连接策略、超时和受控重试 |
| 单一 Prompt | Prompt 版本、评审、回归集和灰度策略 |
| `StrOutputParser` 输出文本 | Pydantic Structured Output、字段校验和错误映射 |
| 直接传入问题 | 从可信认证上下文注入 `user_id`、`tenant_id` 和权限 |
| 无并发限制的 `batch` | 并发上限、限流、队列与成本预算 |
| 无追踪 | trace ID、模型用量、延迟、失败原因和脱敏日志 |
| 单个模型配置 | Provider Adapter、能力探测和降级策略 |

真实模型接入不能把 `base_url` 当成“任何兼容接口都保证可用”的承诺。`ChatOpenAI` 面向官方 OpenAI API 规范；若第三方扩展了响应格式或行为，应确认其兼容性，必要时选用提供商专用集成包。这个判断来自 LangChain 官方集成文档。

## 9. 局限性与常见错误

### 9.1 把 `AIMessage` 当成 `str`

`model.invoke()` 返回的通常是 `AIMessage`，而不是最终文本。只需要展示文本时可以使用 `StrOutputParser`，或在明确了解响应形状后读取 `AIMessage.content`。但工具调用和结构化输出场景不能随意丢弃完整消息。

### 9.2 缺少 Prompt 变量或误用花括号

模板中存在 `{question}`，调用时却没有提供 `question`，会触发输入校验错误。要在 Prompt 中展示 JSON 示例或字面量花括号时，必须写成 `{{` 与 `}}`。这不是模型报错，而是模板格式化报错。

### 9.3 误以为 `|` 立刻执行模型调用

`prompt | model | parser` 只是组装 RunnableSequence。网络调用发生在 `invoke`、`ainvoke`、`batch`、`stream` 等执行方法。这个区别决定了何时捕获异常、何时记录 trace，以及怎样写不访问网络的单元测试。

### 9.4 错把 `batch` 当成提供商原生批处理

LangChain `Runnable.batch()` 的默认实现会并发调用 `invoke()`；它适合 I/O 型 Runnable，但不代表远端模型服务收到一条原生批量请求。生产中必须控制并发数和速率，并确认提供商是否另有批处理 API。

### 9.5 过早用字符串 Parser 处理 JSON

让模型“只输出 JSON”再用字符串解析，仍可能得到截断、额外文字或字段缺失。需要可靠字段时应使用第 4 章的 Pydantic Schema 与 Structured Output，而不是把 `StrOutputParser` 当作验证器。

### 9.6 用 Fake Model 宣称真实模型集成成功

Fake Model 只能验证 Prompt、LCEL、Parser 和业务适配逻辑。真实凭证、网络、模型能力和配额属于 integration 测试范围，应与普通离线测试分开。

## 10. 本章总结

- LangChain 用统一的 Runnable 抽象组织 Prompt、模型、Parser、Retriever 和工具等应用步骤。
- `ChatPromptTemplate` 将变量格式化为 Message；Chat Model 返回 `AIMessage`；Parser 再将它转换为下游需要的形状。
- LCEL 的 `|` 声明数据流，不会立即调用模型。
- `invoke`、`ainvoke`、`batch` 和 `stream` 是不同的执行方式，应根据宿主环境、并发需求和下游流式能力选择。
- `StrOutputParser` 只能提取文本；结构化校验、工具调用、授权和领域事实仍在其他层解决。
- 离线 Fake Model 适合单元测试；真实模型集成必须有独立的配置、成本与错误边界。

## 11. 思考题

1. 为什么 `ChatPromptTemplate.invoke()` 的结果不是最终模型答案？它与 `chain.invoke()` 分别停在哪个阶段？
2. 若一个客服 Agent 需要返回“订单号、建议动作、依据”，为什么 `StrOutputParser` 不足以承担最终输出边界？
3. 为什么 `prompt | model | parser` 在定义时不应该触发网络调用？这对测试有什么价值？
4. `batch()` 的默认并发实现与提供商原生批处理 API 在成本、限流和失败处理上可能有什么区别？
5. 在 Java 网关与 Python Agent 服务并存时，模型配置、用户问题和租户身份分别应由哪一层提供？

## 12. 官方参考资料与验证版本

官方资料：

- [LangChain：安装与集成包](https://docs.langchain.com/oss/python/langchain/install)
- [LangChain：ChatOpenAI 集成](https://docs.langchain.com/oss/python/integrations/chat/openai)
- [LangChain Reference：ChatPromptTemplate](https://reference.langchain.com/python/langchain-core/prompts/chat/ChatPromptTemplate)
- [LangChain Reference：Runnable 与调用方式](https://reference.langchain.com/python/langchain-core/runnables/base/Runnable)
- [LangChain Reference：RunnableLambda 与流式边界](https://reference.langchain.com/python/langchain-core/runnables/base/RunnableLambda)
- [LangChain Reference：语言模型与 Fake Chat Model](https://reference.langchain.com/python/langchain-core/language_models)

资料与依赖版本于 2026-09-08 复核。示例锁定 LangChain 1.4.0、langchain-core 1.6.1、langchain-openai 1.6.0、Pydantic 2.13.5、pytest 9.1.1、Ruff 0.16.5 和 Python 3.12。离线示例不访问模型 API；真实客户端构造与网络调用边界已分离。
