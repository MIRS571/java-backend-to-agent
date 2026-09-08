# 课程路线与验证进度

本文件是课程顺序和完成状态的唯一进度来源。章节通过自动质量门槛后可以标记为“内容完成”，但这不代表学习者已经掌握。

## 基础设施状态

| 项目 | 状态 | 说明 |
| --- | --- | --- |
| uv 项目与锁文件 | 完成 | `pyproject.toml` 与 `uv.lock` 已建立，项目依赖版本已固定 |
| MkDocs Material | 完成 | `mkdocs build --strict` 已成功，本地站点与 GitHub Pages 工作流已配置 |
| 离线质量门槛 | 完成 | Ruff、86 个 pytest 测试和 MkDocs 严格构建通过 |
| 全局文档审校 | 完成 | 2026-09-08 完成导航、链接、术语、版本和页面样式复核 |

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
| 9 | FastAPI 分层、生命周期、SSE 与 Java 流式转发 | 内容完成（2026-09-07） |
| 10 | PostgreSQL、Redis、Qdrant、Docker、幂等与重试 | 内容完成（2026-09-07） |
| 11 | Agent 评估、可观测性、安全、MCP 与多 Agent 边界 | 内容完成（2026-09-07） |
| 12 | `enterprise-support-agent` 综合案例拆解 | 内容完成（2026-09-07） |

## 当前入口

- 当前阶段：12 章课程内容全部完成，不代表学习者已经掌握。
- 已交付：第 12 章按真实请求顺序拆解 `enterprise-support-agent`，明确 Java/Python 责任、订单查询、政策 RAG、退款审批恢复、SSE 转发和完整项目阅读路径。
- 全局审校：统一课程导航与首页入口，补强 API、术语、排错和 Java 对照附录，并为章节结构、内部链接和 MkDocs 导航增加自动约束。
- 验证环境：Python 3.12，`FastAPI 0.141.1`、`Starlette 1.6.0`、`LangGraph 1.2.11`、`LangChain 1.4.0`、`langchain-core 1.6.1`、`langchain-openai 1.6.0`、`langchain-qdrant 1.1.0`、`qdrant-client 1.19.0`、`Pydantic 2.13.5`、`HTTPX 0.28.1`、`pytest 9.1.1`、`ruff 0.16.5`、`MkDocs 1.6.1`、`mkdocs-material 9.7.7`。
- 已验证：`uv sync --locked`、`uv run ruff check .`、86 个 pytest 测试、`uv run mkdocs build --strict`，以及第 12 章离线请求流程示例。
- 已知局限：第 12 章示例只验证架构顺序，不启动完整项目的模型与基础设施；完整案例快照仍保留生产认证、TLS/mTLS、密钥轮换和联合部署等上线工作。
- 下一入口：逐章回答思考题，并按第 12 章阅读顺序审查完整案例仓库。

## 进度更新规则

每次只完成一章。更新状态时必须同时记录：

- 验证日期与关键依赖版本；
- 已交付的可观察结果；
- 实际执行的验证命令；
- 仍然存在的局限；
- 下一章的准确入口。
