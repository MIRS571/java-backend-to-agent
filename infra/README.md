# Infrastructure

课程推进到对应章节后，本目录将提供 Qdrant、PostgreSQL 和 Redis 的 Docker Compose 教学配置。

基础设施遵守三条规则：

1. 服务版本明确，Volume 路径不提交 Git。
2. 示例数据可以重建，密钥不写入 Compose 文件。
3. 只有章节真正使用某个服务时才加入配置，避免为了技术栈列表提前堆积容器。
