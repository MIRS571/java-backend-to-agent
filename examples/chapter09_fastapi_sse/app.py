"""FastAPI application factory and application resource lifecycle."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from .router import router
from .service import AgentGraphService


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Create shared services before requests and close them at shutdown."""

    service = AgentGraphService()
    app.state.agent_graph_service = service
    try:
        yield
    finally:
        await service.aclose()


def create_app() -> FastAPI:
    """Create an isolated app instance for production and tests."""

    app = FastAPI(title="Agent API", version="0.1.0", lifespan=lifespan)
    app.include_router(router)
    return app


app = create_app()
