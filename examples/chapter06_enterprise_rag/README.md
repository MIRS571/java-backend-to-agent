# 第 6 章示例：企业级 RAG 边界

示例使用 Qdrant Python Client 的 `:memory:` 模式验证：

- Collection 与向量维度配置；
- 可重复的 UUID Chunk ID；
- `QdrantVectorStore.add_documents()` 写入；
- `metadata.tenant_id` 查询内过滤；
- 稳定引用对象；
- 最小 `Recall@k` 检索评估。

在仓库根目录运行：

```powershell
uv run python -m examples.chapter06_enterprise_rag.qdrant_demo
```

该命令不需要 Docker、不访问网络，也不创建本地数据库文件。Docker Compose 只作为开发环境启动模板，位于 `infra/qdrant/compose.yml`，不会被测试自动启动。
