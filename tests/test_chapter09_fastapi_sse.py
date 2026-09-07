import json

import httpx
import pytest

from examples.chapter09_fastapi_sse.app import create_app
from examples.chapter09_fastapi_sse.schemas import ChatRequest
from examples.chapter09_fastapi_sse.service import AgentGraphService
from examples.chapter09_fastapi_sse.sse import encode_sse


def request_body(message: str = "订单什么时候发货？") -> dict[str, str]:
    return {
        "user_id": "user-001",
        "thread_id": "thread-001",
        "message": message,
    }


@pytest.mark.asyncio
async def test_service_ainvoke_returns_final_answer():
    service = AgentGraphService()

    result = await service.chat(ChatRequest(**request_body()))

    assert result.thread_id == "thread-001"
    assert result.answer == "已收到问题：订单什么时候发货？"


@pytest.mark.asyncio
async def test_service_astream_exposes_ordered_application_events():
    service = AgentGraphService()
    request = ChatRequest(**request_body())

    events = [event async for event in service.chat_stream(request)]

    assert [event["event"] for event in events] == [
        "metadata",
        "token",
        "token",
        "done",
    ]
    assert events[1]["data"]["content"] == "已收到问题："
    assert events[-1]["data"]["thread_id"] == "thread-001"


def test_sse_encoder_uses_event_data_and_blank_line():
    frame = encode_sse(
        {"event": "token", "data": {"content": "你好\n世界"}}
    )

    assert frame.startswith("event: token\ndata: ")
    assert frame.endswith("\n\n")
    payload = frame.splitlines()[1].removeprefix("data: ")
    assert json.loads(payload) == {"content": "你好\n世界"}


@pytest.mark.asyncio
async def test_fastapi_lifespan_creates_and_closes_service():
    app = create_app()

    async with app.router.lifespan_context(app):
        service = app.state.agent_graph_service
        assert service.closed is False

    assert service.closed is True


@pytest.mark.asyncio
async def test_json_route_resolves_dependency_from_app_state():
    app = create_app()
    async with app.router.lifespan_context(app):
        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(
            transport=transport,
            base_url="http://testserver",
        ) as client:
            response = await client.post(
                "/api/v1/agent/chat",
                json=request_body(),
            )

    assert response.status_code == 200
    assert response.json() == {
        "thread_id": "thread-001",
        "answer": "已收到问题：订单什么时候发货？",
    }


@pytest.mark.asyncio
async def test_sse_route_returns_complete_protocol_frames():
    app = create_app()
    async with app.router.lifespan_context(app):
        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(
            transport=transport,
            base_url="http://testserver",
        ) as client:
            response = await client.post(
                "/api/v1/agent/chat/stream",
                json=request_body(),
            )

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/event-stream")
    assert response.headers["cache-control"] == "no-cache"
    assert response.headers["x-accel-buffering"] == "no"
    assert response.text.count("\n\n") == 4
    assert "event: metadata" in response.text
    assert "event: token" in response.text
    assert "event: done" in response.text


@pytest.mark.asyncio
async def test_blank_request_field_is_rejected_before_route_runs():
    app = create_app()
    async with app.router.lifespan_context(app):
        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(
            transport=transport,
            base_url="http://testserver",
        ) as client:
            response = await client.post(
                "/api/v1/agent/chat",
                json=request_body(message="   "),
            )

    assert response.status_code == 422
