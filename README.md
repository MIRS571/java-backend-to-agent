# Java Backend to Agent

面向 Java 后端开发者的企业级 AI Agent 工程教程。课程以中文讲解为主，保留准确的英文 API、类型和协议名，重点覆盖 LangChain、RAG、LangGraph 以及它们与 Spring Boot 的协作边界。

> **课程状态：** 12 章内容、离线示例和自动测试全部完成。内容完成不等于已经掌握；能够解释数据流、运行示例并定位故障才是学习验收目标。

## 项目定位

很多 Agent 示例只展示几行模型调用，无法回答“身份从哪里来、业务事实存在哪里、失败后如何恢复”。本项目从工程问题出发，按以下顺序组织每章：

```text
问题与约束 → 核心心智模型 → 真实执行顺序 → 最小示例
          → 关键 API → Java 类比 → 生产边界 → 思考题
```

适合以下读者：

- 熟悉 Java、Spring Boot 和常见后端技术栈；
- 能阅读 Python 基础代码，但工程实践较少；
- 希望学习 AI 应用与 Agent 工程，而不是模型训练；
- 希望把模型、RAG 和工作流接入现有企业后端。

## 课程地图

| 阶段 | 章节 | 主要能力 |
| --- | --- | --- |
| 建立边界 | [第 1 章](docs/chapter01/agent-and-llm-api.md) · [第 2 章](docs/chapter02/python-uv-async-fastapi.md) | LLM API、上下文、必要 Python、uv、异步与 FastAPI |
| LangChain | [第 3 章](docs/chapter03/langchain-basics.md) · [第 4 章](docs/chapter04/structured-output-and-tools.md) | Message、Prompt、LCEL、Structured Output、Tool Calling |
| RAG | [第 5 章](docs/chapter05/rag-basics.md) · [第 6 章](docs/chapter06/enterprise-rag-with-qdrant.md) | Document、Embedding、Retriever、Qdrant、多租户与评估 |
| LangGraph | [第 7 章](docs/chapter07/langgraph-basics.md) · [第 8 章](docs/chapter08/persistence-runtime-interrupts.md) | State、Node、路由、Checkpointer、Runtime、Interrupt |
| 企业工程 | [第 9 章](docs/chapter09/fastapi-sse-java-relay.md) · [第 10 章](docs/chapter10/infrastructure-reliability.md) · [第 11 章](docs/chapter11/quality-security-and-boundaries.md) | SSE、Spring 转发、存储、幂等、评估、安全与架构边界 |
| 综合应用 | [第 12 章](docs/chapter12/enterprise-support-agent-walkthrough.md) | 拆解独立的企业售后 Agent 完整项目 |

完整进度和验证记录见 [ROADMAP.md](ROADMAP.md)。

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

完整质量检查：

```powershell
uv run ruff check .
uv run pytest
uv run mkdocs build --strict
```

## 模型配置

只有需要真实模型的 integration 示例才读取本地 `.env`：

```ini
LLM_MODEL=
LLM_API_KEY=
LLM_BASE_URL=
```

仓库不会保存厂商地址、模型名或密钥。普通测试不访问付费模型；integration 测试在缺少本地配置时跳过。

## 仓库结构

```text
docs/       教程正文、学习方法和附录
examples/   与章节对应的最小可运行示例
src/        多章节复用的少量公共代码
tests/      离线测试和仓库质量约束
infra/      Qdrant、Redis、PostgreSQL 等学习环境
```

## 内容原则

- 先讲背景、目的和局限，再讲 API；
- 区分 Python 语法、框架约定、模型协议和业务设计；
- Java 类比只用于建立入口，并明确不等价之处；
- Demo 保持可读，生产必须补充安全、租户、持久化、评估和可观测性；
- 技术行为优先引用官方文档，并记录验证日期和依赖版本。

## 完整项目

第 12 章链接并拆解独立项目 [Enterprise Support Agent](https://github.com/MIRS571/Enterprise-Support-Agent)。教程只提炼最小模式，不复制完整项目。

## 开源许可

- 代码与配置：MIT，见 [LICENSE-CODE](LICENSE-CODE)；
- 原创教程文档：CC BY-NC-SA 4.0，见 [LICENSE-DOCS](LICENSE-DOCS)；
- 双许可证边界说明：见 [LICENSE](LICENSE)。
