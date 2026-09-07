# Examples

每个已完成章节可以拥有一个独立目录，例如：

```text
examples/chapter01_agent_basics/
examples/chapter03_langchain/
examples/chapter06_qdrant/
```

目录只在对应章节真正开始时创建。每个示例必须提供明确入口、固定运行命令和离线测试；需要模型或外部服务的部分必须单独标记为 integration。

## 已完成示例

- [`chapter01_agent_basics`](chapter01_agent_basics/README.md)：使用离线 Fake Model 观察显式上下文边界。
- [`chapter02_python_fastapi`](chapter02_python_fastapi/README.md)：使用离线协程和 FastAPI API 边界理解 `uv`、`async` 与请求校验。
- [`chapter03_langchain_basics`](chapter03_langchain_basics/README.md)：使用离线 Chat Model 观察 Message、Prompt、LCEL、Parser 和调用方式。
- [`chapter04_structured_tools`](chapter04_structured_tools/README.md)：使用离线数据验证 Structured Output Schema，并观察完整 Tool Calling 协议循环。
- [`chapter05_rag_basics`](chapter05_rag_basics/README.md)：使用可重复的本地向量演示 Document、切分、检索、Context 格式化和 2-step RAG。
- [`chapter06_enterprise_rag`](chapter06_enterprise_rag/README.md)：使用 Qdrant 内存模式验证稳定 ID、租户过滤、引用和 Recall@k。
- [`chapter07_langgraph_basics`](chapter07_langgraph_basics/README.md)：使用两个离线图理解 State、Reducer、条件路由、MessagesState 和 ToolNode。
