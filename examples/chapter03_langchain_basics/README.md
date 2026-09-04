# 第 3 章示例：LangChain 基础

本目录把模型调用拆成可观察的四个阶段：Message、Prompt、Chat Model 和 Parser。

`chain_demo.py` 只使用 `FakeListChatModel`，不会读取密钥、不会发起网络请求；它用于观察 LCEL 的输入、输出和调用方式。

在仓库根目录运行：

```powershell
uv run python -m examples.chapter03_langchain_basics.chain_demo
```

`model_factory.py` 展示真实 `ChatOpenAI` 客户端的创建边界，但不会自行读取环境变量或发起模型调用。上层应用应从 `.env` 或部署配置读取 `LLM_MODEL`、`LLM_API_KEY` 和可选的 `LLM_BASE_URL`，再构造 `ModelSettings`。
