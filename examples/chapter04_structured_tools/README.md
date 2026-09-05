# 第 4 章示例：Structured Output 与 Tool Calling

本目录包含两个互不混淆的边界：

- `structured_output_demo.py`：使用 Pydantic 验证模型应返回的数据形状；
- `tool_loop_demo.py`：离线演示模型提出工具调用、应用执行、结果回传和最终回答。

在仓库根目录运行：

```powershell
uv run python -m examples.chapter04_structured_tools.structured_output_demo
uv run python -m examples.chapter04_structured_tools.tool_loop_demo
```

示例不读取密钥、不访问网络。`fake_model_*` 函数只是固定产生模型本应返回的消息，让工具循环可以被观察和测试；真实模型接入时，分别用 `model.with_structured_output(...)` 与 `model.bind_tools(...)` 替换这些固定步骤。
