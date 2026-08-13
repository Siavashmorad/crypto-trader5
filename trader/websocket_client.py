from __future__ import annotations

import asyncio
import json
from collections.abc import Awaitable, Callable

import websockets


class TabdealDepthWebSocket:
    """Analysis-only public depth stream. No order/auth operations are performed."""

    def __init__(self, url: str, symbol: str, on_message: Callable[[dict], Awaitable[None]], reconnect_delay: float = 2.0):
        self.url = url
        self.symbol = symbol
        self.on_message = on_message
        self.reconnect_delay = reconnect_delay
        self._stop = False

    def stop(self) -> None:
        self._stop = True

    async def run(self) -> None:
        while not self._stop:
            try:
                async with websockets.connect(self.url, ping_interval=20, ping_timeout=20) as ws:
                    await ws.send(json.dumps({"method": "SUBSCRIBE", "params": [self.symbol], "id": 1}))
                    async for raw in ws:
                        if self._stop:
                            break
                        try:
                            message = json.loads(raw)
                            await self.on_message(message)
                        except (json.JSONDecodeError, TypeError):
                            continue
            except (OSError, asyncio.TimeoutError, websockets.WebSocketException):
                if not self._stop:
                    await asyncio.sleep(self.reconnect_delay)
