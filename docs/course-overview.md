# 课程路线

## 目标

完成课程后，你应当能够说明一个企业 Agent 请求从 Java 网关进入 Python 服务后，如何经过模型、工具、RAG 和 LangGraph，并最终以普通响应或 SSE 返回；同时能够指出身份、权限、业务事实、缓存和持久化分别属于哪一层。

## 12 章依赖顺序

| 章 | 主题 | 解决的问题 |
| ---: | --- | --- |
| 1 | [Agent 与 LLM API](chapter01/agent-and-llm-api.md) | 模型到底接收什么，又能可靠地完成什么 |
| 2 | [最低必要 Python 与 FastAPI](chapter02/python-uv-async-fastapi.md) | 如何读写后续 Agent 工程代码 |
| 3 | [LangChain 核心](chapter03/langchain-basics.md) | 如何统一组织模型、消息、Prompt 与输出 |
| 4 | [Structured Output 与 Tool Calling](chapter04/structured-output-and-tools.md) | 如何让模型输出可验证数据并请求外部能力 |
| 5 | [RAG 基础](chapter05/rag-basics.md) | 如何让回答基于外部知识而非模型记忆 |
| 6 | [企业级 RAG](chapter06/enterprise-rag-with-qdrant.md) | 如何持久化、隔离、引用和评估检索结果 |
| 7 | [LangGraph 基础](chapter07/langgraph-basics.md) | 如何显式表示状态、节点和分支流程 |
| 8 | [持久化与人工审批](chapter08/persistence-runtime-interrupts.md) | 如何恢复会话并安全暂停高风险流程 |
| 9 | [服务化与流式输出](chapter09/fastapi-sse-java-relay.md) | 如何通过 FastAPI 和 Java 对外提供 Agent 能力 |
| 10 | [企业基础设施](chapter10/infrastructure-reliability.md) | PostgreSQL、Redis、Qdrant 和 Docker 各负责什么 |
| 11 | [质量与边界](chapter11/quality-security-and-boundaries.md) | 如何评估、观察、防护以及判断是否需要 MCP 或多 Agent |
| 12 | 综合案例 | 如何把所有部件放进可解释的企业售后系统 |

课程按依赖顺序推进。可以暂停复习或修正当前章，但不因为框架流行度随意跳过基础数据流。

最新完成状态以仓库根目录的 [`ROADMAP.md`](https://github.com/MIRS571/java-backend-to-agent/blob/main/ROADMAP.md) 为准。
