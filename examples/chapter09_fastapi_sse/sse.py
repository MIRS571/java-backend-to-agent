"""Encode application events using the Server-Sent Events wire format."""

import json

from .service import AgentEvent


def encode_sse(event: AgentEvent) -> str:
    """Return one complete SSE frame terminated by a blank line."""

    data = json.dumps(event["data"], ensure_ascii=False, separators=(",", ":"))
    return f"event: {event['event']}\ndata: {data}\n\n"
