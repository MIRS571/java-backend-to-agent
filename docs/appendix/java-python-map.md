# Java / Python 概念映射

这些映射用于建立入口，不表示两边完全等价。

| Python / Agent 概念 | Java 入口类比 | 关键差异 |
| --- | --- | --- |
| `dataclass` | Java record / 简单 DTO | Python 默认仍可变，除非使用 `frozen=True` |
| Pydantic Model | DTO + Bean Validation | Pydantic 同时负责解析、转换与校验 |
| FastAPI `Depends` | Spring 依赖注入 | 依赖解析以请求调用链为核心，不是完整 Bean 容器 |
| FastAPI `lifespan` | Bean 初始化和销毁生命周期 | 使用异步上下文管理器显式包围应用生命周期 |
| `async` / `await` | `CompletableFuture` 或 Reactor 的异步边界 | Python 协程只有被等待或调度后才执行 |
| LangChain Runnable | 可组合的处理器接口 | `invoke`、`ainvoke`、`stream` 形成统一调用协议 |
| LangGraph State | 工作流实例状态 | 应是可序列化的每次运行数据，不是全局单例 |
| Checkpointer | 工作流状态持久化 | 保存的是图执行快照，不等于业务数据库 |
| Retriever | 查询端口 / Repository 接口 | 返回知识文档，不负责生成最终回答 |
| `AgentContext` / Runtime | 可信请求上下文 | 不是 Spring `ApplicationContext`，也不保存跨请求 Bean |
| Tool | 受控的应用服务端口 | 模型提出调用不等于通过鉴权 |
| `StreamingResponse` | 持续写出 HTTP 响应 | 不等同于 Reactor，内容仍来自 Python 迭代器 |
| Python async iterator | `Flux` 的增量消费视角 | Python 协程模型与 Reactor Publisher 协议不同 |
| `QdrantVectorStore` | Repository Adapter | 保存和查询向量，不拥有订单等业务事实 |
| `interrupt` / `Command` | 持久化人工任务与恢复命令 | 节点恢复可能重新执行，副作用顺序必须安全 |
| `app.state` | 应用级实例注册位置 | 不自动提供 Spring Bean 的作用域、代理和完整生命周期能力 |
