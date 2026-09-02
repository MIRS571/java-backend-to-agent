# 第 2 章示例：uv、async 与 FastAPI

本目录有两个互不依赖的最小示例：

- `async_basics.py`：展示 `async def`、`await` 与 `asyncio.run()` 的调用顺序；
- `app.py`：展示 FastAPI 路由、请求模型、响应模型与输入校验。

在仓库根目录运行异步示例：

```powershell
uv run python -m examples.chapter02_python_fastapi.async_basics
```

启动 FastAPI 开发服务器：

```powershell
uv run uvicorn examples.chapter02_python_fastapi.app:app --reload
```

服务启动后，可在 <http://127.0.0.1:8000/docs> 查看自动生成的 OpenAPI 文档。停止服务使用 `Ctrl+C`。
