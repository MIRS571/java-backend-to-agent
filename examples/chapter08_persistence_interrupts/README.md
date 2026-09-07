# 第 8 章示例：持久化、Runtime 与人工审批

本目录包含两个完全离线的 LangGraph 示例：

- `checkpoint_runtime_demo.py`：同一 `thread_id` 跨调用保留 State，不同 thread 相互隔离；节点通过 `Runtime[AgentContext]` 获取租户与 Service。
- `interrupt_resume_demo.py`：退款流程通过 `interrupt()` 暂停，再用相同 `thread_id` 和 `Command(resume=...)` 恢复。

在仓库根目录运行：

```powershell
uv run python -m examples.chapter08_persistence_interrupts.checkpoint_runtime_demo
uv run python -m examples.chapter08_persistence_interrupts.interrupt_resume_demo
```

示例使用 `InMemorySaver`，不访问模型、网络或真实数据库。进程退出后 checkpoint 会消失，因此它只适合学习与测试，不是生产持久化方案。
