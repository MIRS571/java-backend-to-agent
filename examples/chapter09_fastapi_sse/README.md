# 第 9 章示例：FastAPI、LangGraph 与 SSE

本目录演示以下分层：

```text
HTTP Router -> AgentGraphService -> Compiled LangGraph
      |                  |
      |                  -> ainvoke / astream
      -> JSON / StreamingResponse(SSE)
```

启动服务（在仓库根目录运行）：

```powershell
uv run uvicorn examples.chapter09_fastapi_sse.app:app --reload
```

然后打开 <http://127.0.0.1:8000/docs> 测试普通 JSON 接口。Swagger UI 不适合观察逐块 SSE 到达时间；流式接口可使用：

```powershell
curl.exe -N -X POST http://127.0.0.1:8000/api/v1/agent/chat/stream `
  -H "Content-Type: application/json" `
  -d '{"user_id":"user-001","thread_id":"thread-001","message":"订单什么时候发货？"}'
```

本示例不调用真实模型或数据库。`java/AgentSseRelay.java` 展示 Spring WebFlux 使用 `WebClient` 转发 SSE 的核心写法；它是集成参考，不是本 Python 仓库中的独立 Maven 项目。
