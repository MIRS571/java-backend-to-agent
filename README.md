# Java Backend to Agent

面向 Java 后端开发者的企业级 AI Agent 工程教程。课程使用简洁的中文解释和可运行代码，重点覆盖 LangChain、RAG、LangGraph，以及它们与 Spring Boot 企业后端的协作边界。

> 当前状态：第 1～3 章内容已经完成，下一步是第 4 章“Structured Output、Pydantic、Tool Calling 与工具循环”。

## 为什么有这个项目

很多 Agent 教程要么只展示几行模型调用，要么一次引入大量框架 API。本项目采用另一条路线：先说明技术要解决的问题，再给出最小可运行实现，最后明确 Demo 与企业级实现之间的差距。

本项目特别适合：

- 熟悉 Java、Spring Boot 和常见后端技术栈；
- 能阅读 Python 基础代码，但独立编写经验有限；
- 希望学习 AI 应用和 Agent 工程，而不是模型训练；
- 希望把 LangChain、RAG、LangGraph 与现有后端系统结合。

## 学习主线

| 模块 | 主要内容 |
| --- | --- |
| 基础 | LLM API、消息、上下文、必要的 Python 与 FastAPI |
| LangChain | Prompt、LCEL、Structured Output、Tool Calling |
| RAG | Document、Embedding、Retriever、Qdrant、多租户与评估 |
| LangGraph | State、Node、路由、Checkpointer、Runtime、Interrupt |
| 企业集成 | SSE、Spring Boot、Redis、PostgreSQL、Docker、安全与可观测性 |
| 综合案例 | 拆解独立的 `enterprise-support-agent` 完整项目 |

完整章节和状态见 [ROADMAP.md](ROADMAP.md)。

当前可阅读：[第 1 章：Agent、LLM API、消息、上下文与模型局限](docs/chapter01/agent-and-llm-api.md)；[第 2 章：Python、uv、异步与 FastAPI](docs/chapter02/python-uv-async-fastapi.md)；[第 3 章：LangChain 基础](docs/chapter03/langchain-basics.md)。

## 快速开始

要求：Python 3.12 与 [uv](https://docs.astral.sh/uv/)。

```powershell
git clone https://github.com/MIRS571/java-backend-to-agent.git
cd java-backend-to-agent
uv sync --locked
uv run pytest
uv run mkdocs serve
```

文档预览默认地址：<http://127.0.0.1:8000>。

## 模型配置

复制 `.env.example` 为 `.env`，然后只在本地填写：

```ini
LLM_MODEL=
LLM_API_KEY=
LLM_BASE_URL=
```

仓库不会保存厂商地址、模型名或密钥。普通测试不访问付费模型；需要真实模型的 integration 测试会在缺少本地配置时跳过。

## 仓库结构

```text
docs/       教程正文和附录
examples/   与章节对应的最小可运行示例
src/        多章节复用的少量公共代码
tests/      离线测试和仓库约束检查
infra/      Qdrant、Redis、PostgreSQL 等基础设施说明
```

## 内容原则

- 先讲背景、目的和局限，再讲 API。
- 区分 Python 语法、框架约定、模型协议和业务设计。
- Java 类比只用于帮助理解，并说明类比失效的位置。
- 每章包含思考题，但不在正文直接给出答案。
- 技术 API 优先引用官方文档，并记录验证日期和依赖版本。

## 开源许可

- 代码与配置：MIT，见 [LICENSE-CODE](LICENSE-CODE)。
- 原创教程文档：CC BY-NC-SA 4.0，见 [LICENSE-DOCS](LICENSE-DOCS)。
- 双许可证边界说明：见 [LICENSE](LICENSE)。
