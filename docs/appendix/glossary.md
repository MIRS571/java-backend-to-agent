# Agent 术语表

| 术语 | 简要含义 |
| --- | --- |
| LLM | 接收上下文并生成后续 token 的语言模型 |
| Message | 带有角色和内容的模型输入或输出单元 |
| Prompt | 交给模型的指令和上下文组织方式 |
| Structured Output | 让模型结果符合预定义字段结构，并在程序侧校验 |
| Tool Calling | 模型生成结构化工具请求，由程序决定是否执行 |
| Agent | 让模型在状态、工具和控制流程中参与决策的应用系统 |
| RAG | 检索外部资料并把结果作为上下文交给模型生成 |
| Embedding | 把文本映射为可比较的数值向量 |
| Vector Store | 保存向量、原文和元数据并提供相似度检索的组件 |
| Retriever | 面向查询返回相关 `Document` 的统一接口 |
| Reranker | 对召回候选进行更精细的相关性重新排序 |
| LCEL | 使用 Runnable 与 `|` 表达 LangChain 数据流的组合方式 |
| State | LangGraph 一次工作流中持续传递和更新的数据 |
| Node | 读取 State 并返回局部更新的工作流步骤 |
| Edge | 决定 LangGraph 下一执行节点的控制流连接 |
| Reducer | 合并 State 旧值与节点新值的策略 |
| Runtime Context | 向节点提供当次可信身份和依赖引用的调用期上下文 |
| Checkpointer | 按线程保存 LangGraph 执行快照的持久化组件 |
| Interrupt | 在图中暂停并把待处理信息交给外部调用者的机制 |
| SSE | 服务端通过单个 HTTP 连接持续发送文本事件的协议 |
| MCP | 让模型应用发现和调用外部工具、资源与 Prompt 的协议 |
| Trace | 一次请求中模型、检索、节点和工具调用组成的完整执行记录 |
| Idempotency | 同一逻辑请求重复执行时，业务效果仍等同于执行一次 |
| Tenant Filter | 在数据库或向量检索查询内部限制租户数据范围的条件 |
