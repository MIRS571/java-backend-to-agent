# 课程路线与验证进度

本文件是课程顺序和完成状态的唯一进度来源。章节通过自动质量门槛后可以标记为“内容完成”，但这不代表学习者已经掌握。

## 基础设施状态

| 项目 | 状态 | 说明 |
| --- | --- | --- |
| uv 项目与锁文件 | 完成 | `pyproject.toml` 与 `uv.lock` 已建立，项目依赖版本已固定 |
| MkDocs Material | 完成 | `mkdocs build --strict` 已成功，本地站点与 GitHub Pages 工作流已配置 |
| 离线质量门槛 | 完成 | Ruff、51 个 pytest 测试和 MkDocs 严格构建通过 |
| 全局课程 Skill | 完成 | `java-agent-course-lead` 已安装并通过 `quick_validate.py` |

## 12 章主线

| 章 | 内容 | 状态 |
| ---: | --- | --- |
| 1 | Agent、LLM API、消息、上下文与模型局限 | 内容完成（2026-09-02） |
| 2 | Java 开发者所需的 Python、uv、异步与 FastAPI | 内容完成（2026-09-02） |
| 3 | LangChain 模型、Message、Prompt、LCEL、Parser 与调用方式 | 内容完成（2026-09-04） |
| 4 | Structured Output、Pydantic、Tool Calling 与工具循环 | 内容完成（2026-09-05） |
| 5 | RAG：Document、切分、Embedding、向量检索与 Retriever | 内容完成（2026-09-05） |
| 6 | Qdrant、稳定 ID、Metadata Filter、多租户、引用与评估 | 内容完成（2026-09-07） |
| 7 | LangGraph：State、Node、Edge、路由、MessagesState 与 ToolNode | 内容完成（2026-09-07） |
| 8 | Checkpointer、Memory、Runtime、Interrupt 与 Resume | 内容完成（2026-09-07） |
| 9 | FastAPI 分层、生命周期、SSE 与 Java 流式转发 | 待开始 |
| 10 | PostgreSQL、Redis、Qdrant、Docker、幂等与重试 | 待开始 |
| 11 | Agent 评估、可观测性、安全、MCP 与多 Agent 边界 | 待开始 |
| 12 | `enterprise-support-agent` 综合案例拆解 | 待开始 |

## 当前入口

- 当前阶段：第 1～8 章内容完成，不代表学习者已经掌握。
- 已交付：第 1～7 章完成 Agent、LangChain、Tool Calling、企业 RAG 与 LangGraph 基础主线；第 8 章完成 Checkpointer、thread_id、线程级 Memory、Runtime Context、依赖与 State 的边界、Interrupt 暂停及 Command Resume。
- 验证环境：Python 3.12，`LangGraph 1.2.11`、`LangChain 1.4.0`、`langchain-core 1.6.1`、`langchain-openai 1.6.0`、`langchain-qdrant 1.1.0`、`qdrant-client 1.19.0`、`Pydantic 2.13.5`、`pytest 9.1.1`、`ruff 0.16.5`、`MkDocs 1.6.1`、`mkdocs-material 9.7.7`。
- 已验证：`uv sync --locked`、`uv run ruff check .`、51 个 pytest 测试、`uv run mkdocs build --strict`，以及第 1～8 章的离线示例运行命令。
- 已知局限：第 8 章使用进程内 `InMemorySaver` 与 Fake Service；不验证 PostgreSQL Checkpointer、跨进程/多实例恢复、并发审批、真实权限系统、异步流式服务或生产幂等。
- 下一入口：第 9 章“FastAPI 分层、生命周期、SSE 与 Java 流式转发”。

## 进度更新规则

每次只完成一章。更新状态时必须同时记录：

- 验证日期与关键依赖版本；
- 已交付的可观察结果；
- 实际执行的验证命令；
- 仍然存在的局限；
- 下一章的准确入口。
