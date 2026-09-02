import asyncio

from httpx import ASGITransport, AsyncClient

from examples.chapter02_python_fastapi.app import app
from examples.chapter02_python_fastapi.async_basics import (
    wait_for_upstream_response,
)


async def request(
    method: str,
    path: str,
    json: dict[str, str] | None = None,
):
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport,
        base_url="http://testserver",
    ) as client:
        return await client.request(method, path, json=json)


def test_async_function_returns_a_value_after_awaiting():
    assert asyncio.run(wait_for_upstream_response()) == "upstream response received"


def test_health_endpoint_returns_ok():
    response = asyncio.run(request("GET", "/health"))

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_preview_endpoint_normalizes_message_and_uses_response_model():
    response = asyncio.run(
        request(
            "POST",
            "/api/v1/messages/preview",
            json={"message": "  hello agent  ", "language": "en"},
        )
    )

    assert response.status_code == 200
    assert response.json() == {
        "normalized_message": "hello agent",
        "language": "en",
        "preview": "Received: hello agent",
    }


def test_preview_endpoint_rejects_whitespace_only_message():
    response = asyncio.run(
        request(
            "POST",
            "/api/v1/messages/preview",
            json={"message": "   ", "language": "zh"},
        )
    )

    assert response.status_code == 422
    assert response.json()["detail"] == "message cannot contain only whitespace"
