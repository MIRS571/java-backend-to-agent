# 第 10 章示例：基础设施与可靠性边界

`reliability_demo.py` 用进程内对象演示三项与具体 Redis Client 无关的核心规则：

- Key 必须包含租户与资源作用域；
- 同一幂等键复用相同结果，若请求内容改变则拒绝；
- 只对明确的临时读取错误做有限次数重试。

在仓库根目录运行：

```powershell
uv run python -m examples.chapter10_infrastructure_reliability.reliability_demo
```

该 Demo 没有模拟并发竞争、处理中状态或未知提交结果。真实退款必须由 Java 业务服务结合 Redis 原子操作和关系数据库事务实现。
