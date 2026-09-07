# 企业基础设施学习拓扑

该 Compose 文件只用于本机学习 PostgreSQL、Redis 与 Qdrant 的职责边界，不是生产部署清单。

复制 `.env.example` 为该目录下的 `.env`，为四个变量填写本地开发值，然后在仓库根目录运行：

```powershell
docker compose --env-file infra/enterprise/.env `
  -f infra/enterprise/compose.yml config
docker compose --env-file infra/enterprise/.env `
  -f infra/enterprise/compose.yml up -d
docker compose --env-file infra/enterprise/.env `
  -f infra/enterprise/compose.yml down
```

所有端口只绑定本机回环地址，数据写入 Docker named volumes。生产环境必须补充私有网络、TLS、密钥管理、备份恢复、监控、容量规划与高可用，不能照搬此文件。
