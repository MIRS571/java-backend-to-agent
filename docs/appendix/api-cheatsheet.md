# API 速查方法

本附录不要求死记 API，而是提供统一阅读方法，并汇总课程中最容易混淆的主线接口。框架升级时先核对官方文档和项目锁定版本。

## 六个固定问题

遇到任何 API，依次确认：

1. 它属于哪个包和哪个对象？
2. 它是构造方法、普通方法、异步方法还是装饰器？
3. 输入参数的类型和必填条件是什么？
4. 返回值的具体类型是什么？
5. 是否访问网络、数据库或修改状态？
6. 失败时抛异常、返回空值，还是把错误写入状态？

## 当前基础命令

| 命令 | 作用 |
| --- | --- |
| `uv sync --locked` | 严格按照 `uv.lock` 同步项目环境 |
| `uv run <command>` | 在项目虚拟环境中运行命令 |
| `uv run pytest` | 执行离线测试 |
| `uv run ruff check .` | 检查 Python 代码与导入 |
| `uv run mkdocs serve` | 本地预览教学站点 |
| `uv run mkdocs build --strict` | 严格构建静态文档 |

## LangChain 调用协议

| API | 输入 | 返回 | 适用场景 |
| --- | --- | --- | --- |
| `invoke(input)` | 单个输入 | 单个完整结果 | 同步脚本或节点 |
| `ainvoke(input)` | 单个输入 | `await` 后得到完整结果 | 异步 Web 服务 |
| `batch(inputs)` | 多个输入 | 与输入顺序对应的结果列表 | 可独立处理的一批任务 |
| `stream(input)` | 单个输入 | 同步迭代器 | 同步增量消费 |
| `astream(input)` | 单个输入 | 异步迭代器 | SSE 等异步流式响应 |
| `with_structured_output(Schema)` | Pydantic/TypedDict Schema | 返回结构化对象的新 Runnable | 意图、参数和分类结果 |
| `bind_tools(tools)` | 工具 Schema 列表 | 可能产生 `tool_calls` 的模型 | 让模型提出工具请求 |

`invoke` 与 `ainvoke` 的差别主要是等待方式，不是回答质量。`stream` 只有在底层真正产生增量内容时才有流式价值。

## LangGraph 主线 API

| API | 做什么 | 不做什么 |
| --- | --- | --- |
| `StateGraph(State)` | 创建图定义 Builder | 不立即执行节点 |
| `add_node(name, fn)` | 注册处理步骤 | 不决定下一步 |
| `add_edge(a, b)` | 声明固定跳转 | 不表达 `else` |
| `add_conditional_edges(node, route)` | 运行时选择路径 | 路由函数不宜承担重业务副作用 |
| `compile(checkpointer=...)` | 生成可执行图 | 不启动 FastAPI 或数据库 |
| `ainvoke(input, config, context)` | 异步运行并返回最终 State | 不提供 token 流 |
| `astream(..., stream_mode=...)` | 异步返回 Graph 事件 | 不自动生成 SSE 帧 |
| `interrupt(value)` | 保存暂停点并向外暴露可序列化数据 | 不等于授权完成 |
| `Command(resume=value)` | 把外部决定送回暂停点 | 必须复用相同线程配置 |

## RAG 主线对象

| 对象 | 接收什么 | 返回或保存什么 |
| --- | --- | --- |
| `Document` | `page_content` 与 `metadata` | 统一文本载体 |
| Text Splitter | 文档和切分配置 | 多个继承 metadata 的 chunks |
| Embeddings | 文本或查询 | 数值向量 |
| Vector Store | Document、ID、向量和 metadata | 可检索的持久数据 |
| Retriever | query 与检索配置 | 相关 `Document` 列表 |
| `QdrantVectorStore` | Qdrant Client、Collection、Embedding | LangChain 与 Qdrant 的适配层 |

## FastAPI 与 SSE

| API | 责任 | 关键边界 |
| --- | --- | --- |
| `APIRouter` | 组织路由前缀和标签 | 不应装配所有长期资源 |
| `Depends` | 沿请求调用链解析依赖 | 不是完整 Spring IoC 容器 |
| `lifespan` | 包围应用启动到关闭 | `yield` 前启动，之后清理 |
| `StreamingResponse` | 消费迭代器并持续写 HTTP Body | 仍需正确编码 SSE 帧 |
| `media_type="text/event-stream"` | 声明 SSE 媒体类型 | 不会自动把普通 JSON 变成事件流 |
