# 第 7 章示例：LangGraph 基础

本目录包含两个离线图：

- `routing_graph.py`：`TypedDict State -> Node -> conditional edge -> END`；
- `message_tool_graph.py`：`MessagesState -> call_model -> ToolNode -> call_model -> END`。

在仓库根目录运行：

```powershell
uv run python -m examples.chapter07_langgraph_basics.routing_graph
uv run python -m examples.chapter07_langgraph_basics.message_tool_graph
```

两个示例都不访问模型或网络。`call_model` 使用确定性代码模拟模型在工具执行前后的两次响应，目的是观察 LangGraph 的 State 更新、条件路由、消息 reducer 和工具循环，而不是验证真实模型能力。
