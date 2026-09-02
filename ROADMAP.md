# 课程路线与验证进度

本文件是课程顺序和完成状态的唯一进度来源。章节通过自动质量门槛后可以标记为“内容完成”，但这不代表学习者已经掌握。

## 基础设施状态

| 项目 | 状态 | 说明 |
| --- | --- | --- |
| uv 项目与锁文件 | 完成 | `pyproject.toml` 与 `uv.lock` 已建立，项目依赖版本已固定 |
| MkDocs Material | 完成 | `mkdocs build --strict` 已成功，本地站点与 GitHub Pages 工作流已配置 |
| 离线质量门槛 | 完成 | Ruff、12 个 pytest 测试和 MkDocs 严格构建通过 |
| 全局课程 Skill | 完成 | `java-agent-course-lead` 已安装并通过 `quick_validate.py` |

## 12 章主线

| 章 | 内容 | 状态 |
| ---: | --- | --- |
| 1 | Agent、LLM API、消息、上下文与模型局限 | 内容完成（2026-09-02） |
| 2 | Java 开发者所需的 Python、uv、异步与 FastAPI | 内容完成（2026-09-02） |
| 3 | LangChain 模型、Message、Prompt、LCEL、Parser 与调用方式 | 待开始 |
| 4 | Structured Output、Pydantic、Tool Calling 与工具循环 | 待开始 |
| 5 | RAG：Document、切分、Embedding、向量检索与 Retriever | 待开始 |
| 6 | Qdrant、稳定 ID、Metadata Filter、多租户、引用与评估 | 待开始 |
| 7 | LangGraph：State、Node、Edge、路由、MessagesState 与 ToolNode | 待开始 |
| 8 | Checkpointer、Memory、Runtime、Interrupt 与 Resume | 待开始 |
| 9 | FastAPI 分层、生命周期、SSE 与 Java 流式转发 | 待开始 |
| 10 | PostgreSQL、Redis、Qdrant、Docker、幂等与重试 | 待开始 |
| 11 | Agent 评估、可观测性、安全、MCP 与多 Agent 边界 | 待开始 |
| 12 | `enterprise-support-agent` 综合案例拆解 | 待开始 |

## 当前入口

- 当前阶段：第 1、2 章内容完成，不代表学习者已经掌握。
- 已交付：第 1 章正文、显式上下文离线示例和 3 个章节测试；第 2 章正文、协程最小示例、FastAPI 请求/响应边界示例和 4 个章节测试。
- 验证环境：Python 3.12，`FastAPI 0.141.1`、`Uvicorn 0.52.4`、`Pydantic 2.13.4`、`HTTPX 0.28.1`、`pytest 9.1.1`、`ruff 0.16.5`、`MkDocs 1.6.1`、`mkdocs-material 9.7.7`。
- 已验证：`uv sync --locked`、`uv run ruff check .`、12 个 pytest 测试、`uv run mkdocs build --strict`、第 1 章示例、第 2 章异步示例，以及 FastAPI 服务的 `/health` 响应。
- 已知局限：第 2 章只提供确定性本地 API 边界，不测试真实模型、认证、数据库、依赖注入、SSE 或部署策略；这些内容按课程顺序在后续章节展开。
- 下一入口：第 3 章“LangChain 模型、Message、Prompt、LCEL、Parser 与调用方式”。

## 进度更新规则

每次只完成一章。更新状态时必须同时记录：

- 验证日期与关键依赖版本；
- 已交付的可观察结果；
- 实际执行的验证命令；
- 仍然存在的局限；
- 下一章的准确入口。
