"""FastAPI dependency declarations for application-scoped services."""

from typing import Annotated

from fastapi import Depends, Request

from .service import AgentGraphService


def get_agent_service(request: Request) -> AgentGraphService:
    """Read the service created by the application lifespan."""

    return request.app.state.agent_graph_service


AgentServiceDep = Annotated[
    AgentGraphService,
    Depends(get_agent_service),
]
