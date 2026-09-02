# 面试复习问题

这些问题用于检查能否解释工程取舍，不提供背诵答案。

1. Tool Calling 与直接让模型输出一段自然语言指令有什么本质差异？
2. Structured Output 能保证哪些事情，不能保证哪些事情？
3. RAG 的入库流程和查询流程为什么必须分开？
4. 为什么多租户过滤必须进入 Qdrant 或数据库查询条件？
5. LangGraph State、Runtime 和 Checkpointer 各自保存什么？
6. `interrupt` 恢复时为什么必须复用相同的 `thread_id`？
7. SSE 为什么通常使用 WebClient/Flux 转发，而不优先使用 OpenFeign？
8. Redis 适合保存哪些 Agent 数据，又不应该成为哪些数据的事实来源？
9. Java 与 Python 在企业 Agent 系统中应如何划分职责？
10. 如何证明一个 Agent 项目不仅“能回答”，而且可评估、可追踪、可控？
