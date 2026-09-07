# 第 12 章示例

从仓库根目录运行：

```powershell
uv run python -m examples.chapter12_capstone.request_flow_demo
```

示例不启动完整项目，而是把订单查询、政策 RAG 和退款三条流程表示为可验证的数据。重点观察每一步的所有者，以及身份、租户过滤、人工审批、幂等和事务的先后顺序。
