# 课程路线

## 最终目标

完成课程后，应当能够解释一个企业 Agent 请求从 Java 入口进入 Python 服务后，如何经过模型、工具、RAG 和 LangGraph，并最终以 JSON 或 SSE 返回。同时能够指出身份、权限、业务事实、缓存、向量数据和工作流状态分别属于哪一层。

```mermaid
flowchart LR
    A[基础边界<br/>1-2] --> B[LangChain<br/>3-4]
    B --> C[RAG<br/>5-6]
    C --> D[LangGraph<br/>7-8]
    D --> E[企业工程<br/>9-11]
    E --> F[综合案例<br/>12]
```

## 12 章依赖顺序

| 阶段 | 章 | 主题 | 解决的问题 |
| --- | ---: | --- | --- |
| 基础 | 1 | [Agent 与 LLM API](chapter01/agent-and-llm-api.md) | 模型接收什么，又能可靠完成什么 |
| 基础 | 2 | [最低必要 Python 与 FastAPI](chapter02/python-uv-async-fastapi.md) | 如何读写后续 Agent 工程代码 |
| LangChain | 3 | [模型、Message、Prompt 与 LCEL](chapter03/langchain-basics.md) | 如何统一组织模型输入、组合与输出 |
| LangChain | 4 | [Structured Output 与 Tool Calling](chapter04/structured-output-and-tools.md) | 如何让模型输出可校验数据并提出工具请求 |
| RAG | 5 | [RAG 基础](chapter05/rag-basics.md) | 如何让回答基于外部知识而非模型记忆 |
| RAG | 6 | [企业级 RAG](chapter06/enterprise-rag-with-qdrant.md) | 如何持久化、隔离、引用和评估检索结果 |
| LangGraph | 7 | [LangGraph 基础](chapter07/langgraph-basics.md) | 如何显式表示 State、Node 和控制流 |
| LangGraph | 8 | [持久化与人工审批](chapter08/persistence-runtime-interrupts.md) | 如何恢复会话并暂停高风险流程 |
| 企业工程 | 9 | [服务化与流式输出](chapter09/fastapi-sse-java-relay.md) | 如何通过 FastAPI 和 Java 提供 Agent 能力 |
| 企业工程 | 10 | [基础设施与可靠性](chapter10/infrastructure-reliability.md) | PostgreSQL、Redis、Qdrant 和 Docker 各负责什么 |
| 企业工程 | 11 | [质量、安全与架构边界](chapter11/quality-security-and-boundaries.md) | 如何评估、观察、防护以及判断高级方案是否必要 |
| 综合应用 | 12 | [企业售后 Agent 案例](chapter12/enterprise-support-agent-walkthrough.md) | 如何把全部部件放进可解释的企业系统 |

## 推荐学习方式

=== "首次完整学习"

    严格按 1 → 12 推进。每章先预测数据流，再运行示例，最后独立回答思考题。

=== "重点学习 RAG"

    先复习第 3～4 章的 LangChain 输入输出，再学习第 5～6 章，最后阅读第 11 章的评估与安全部分。

=== "重点学习 LangGraph"

    先确认第 4 章 Tool Calling 循环，再学习第 7～9 章，最后用第 12 章串起持久化、审批和 SSE。

=== "项目与面试复习"

    从第 12 章按真实请求顺序阅读完整项目，再使用[面试复习问题](appendix/interview-questions.md)检查能否解释取舍。

!!! warning "不要跳过边界"
    能调用模型并不等于能构建 Agent，能构建 Agent 也不等于能够安全上线。身份、租户、业务事实、幂等和评估不是附加功能，而是企业工程的基本约束。

12 章内容均已通过自动质量门槛。最新测试数量、验证版本、已知局限和下一入口以仓库根目录的 [`ROADMAP.md`](https://github.com/MIRS571/java-backend-to-agent/blob/main/ROADMAP.md) 为准。
