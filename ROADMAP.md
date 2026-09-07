# 课程路线与验证进度

本文件是课程顺序和完成状态的唯一进度来源。章节通过自动质量门槛后可以标记为“内容完成”，但这不代表学习者已经掌握。

## 基础设施状态

| 项目 | 状态 | 说明 |
| --- | --- | --- |
| uv 项目与锁文件 | 完成 | `pyproject.toml` 与 `uv.lock` 已建立，项目依赖版本已固定 |
| MkDocs Material | 完成 | `mkdocs build --strict` 已成功，本地站点与 GitHub Pages 工作流已配置 |
| 离线质量门槛 | 完成 | Ruff、39 个 pytest 测试和 MkDocs 严格构建通过 |
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
| 7 | LangGraph：State、Node、Edge、路由、MessagesState 与 ToolNode | 待开始 |
| 8 | Checkpointer、Memory、Runtime、Interrupt 与 Resume | 待开始 |
| 9 | FastAPI 分层、生命周期、SSE 与 Java 流式转发 | 待开始 |
| 10 | PostgreSQL、Redis、Qdrant、Docker、幂等与重试 | 待开始 |
| 11 | Agent 评估、可观测性、安全、MCP 与多 Agent 边界 | 待开始 |
| 12 | `enterprise-support-agent` 综合案例拆解 | 待开始 |

## 当前入口

- 当前阶段：第 1～6 章内容完成，不代表学习者已经掌握。
- 已交付：第 1～4 章完成 Agent、Python、LangChain 与 Tool Calling 基础；第 5 章完成 RAG 基础链路；第 6 章完成 Qdrant Collection、稳定 UUID、幂等 upsert、查询内租户过滤、结构化 Citation、Recall@k 与可选 Docker 开发模板。
- 验证环境：Python 3.12，`LangChain 1.4.0`、`langchain-core 1.6.1`、`langchain-openai 1.6.0`、`langchain-qdrant 1.1.0`、`qdrant-client 1.19.0`、`langchain-text-splitters 1.1.2`、`NumPy 2.5.2`、`Pydantic 2.13.5`、`pytest 9.1.1`、`ruff 0.16.5`、`MkDocs 1.6.1`、`mkdocs-material 9.7.7`；Docker 模板固定 Qdrant Server 1.18.2。
- 已验证：`uv sync --locked`、`uv run ruff check .`、39 个 pytest 测试、`uv run mkdocs build --strict`，以及第 1～6 章的离线示例运行命令；Compose YAML 的镜像、端口与 Volume 约束由离线测试验证。
- 已知局限：第 6 章使用 Qdrant 内存模式与教学 Embedding，不验证远程服务的网络、认证、持久化、高可用、生产语义检索或真实模型生成；Docker Compose 只提供本地开发模板。
- 下一入口：第 7 章“LangGraph：State、Node、Edge、路由、MessagesState 与 ToolNode”。

## 进度更新规则

每次只完成一章。更新状态时必须同时记录：

- 验证日期与关键依赖版本；
- 已交付的可观察结果；
- 实际执行的验证命令；
- 仍然存在的局限；
- 下一章的准确入口。
