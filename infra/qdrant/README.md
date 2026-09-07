# Qdrant 开发环境

此 Compose 文件用于本机学习和开发，不是生产部署方案。它使用命名 Volume，避免把数据库文件写入仓库。

在仓库根目录按需运行：

```powershell
docker compose -f infra/qdrant/compose.yml up -d
docker compose -f infra/qdrant/compose.yml ps
docker compose -f infra/qdrant/compose.yml down
```

REST API 与 Dashboard 使用 `http://127.0.0.1:6333`，gRPC 使用 `127.0.0.1:6334`。端口只绑定本机回环地址。

默认 Qdrant 不带认证，不能直接暴露到公网。生产环境还需要 TLS、认证、持久化、备份恢复、监控、高可用和网络访问控制。
