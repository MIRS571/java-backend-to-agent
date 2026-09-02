# 第 1 章离线示例：显式上下文

本示例使用确定性的 `FakeChatModel`，不访问网络，也不需要 API Key。它对比同一个追问在“不带历史”和“带历史”两种请求中的结果，用于证明：模型只能使用当前请求可见的上下文。

在仓库根目录运行：

```powershell
uv run python -m examples.chapter01_agent_basics.main
```

`FakeChatModel` 不是语言模型，也不模拟模型能力；它只把输入边界变成可观察、可测试的行为。
