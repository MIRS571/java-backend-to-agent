"""A minimal, deterministic demonstration of ``async`` and ``await``."""

from __future__ import annotations

import asyncio


async def wait_for_upstream_response() -> str:
    """Simulate a cooperative I/O wait without performing network I/O."""

    await asyncio.sleep(0)
    return "upstream response received"


async def main() -> None:
    response = await wait_for_upstream_response()
    print(response)


if __name__ == "__main__":
    asyncio.run(main())
