import json
from typing import AsyncIterator, Dict, Any
import websockets


class KalshiWSClient:
    """WebSocket client for Kalshi Market Data Feed."""

    def __init__(self, api_key: str, url: str = "wss://api.elections.kalshi.com/trade-api/ws/v2"):
        self.url = url
        self.api_key = api_key
        self.conn = None
        self._cmd_id = 0

    async def connect(self) -> None:
        headers = {"Authorization": f"Bearer {self.api_key}"}
        self.conn = await websockets.connect(self.url, extra_headers=headers)

    async def subscribe(self, channel: str, market_id: str = None) -> None:
        self._cmd_id += 1
        params = {"channel": channel}
        if market_id:
            params["market_id"] = market_id
        cmd = {"id": self._cmd_id, "cmd": "subscribe", "params": params}
        await self.conn.send(json.dumps(cmd))

    async def unsubscribe(self, channel: str, market_id: str = None) -> None:
        self._cmd_id += 1
        params = {"channel": channel}
        if market_id:
            params["market_id"] = market_id
        cmd = {"id": self._cmd_id, "cmd": "unsubscribe", "params": params}
        await self.conn.send(json.dumps(cmd))

    async def listen(self) -> AsyncIterator[Dict[str, Any]]:
        async for message in self.conn:
            yield json.loads(message)

    async def close(self) -> None:
        if self.conn:
            await self.conn.close()


class PolymarketWSClient:
    """WebSocket client for Polymarket CLOB API."""

    def __init__(self, api_key: str, url: str = "wss://ws-subscriptions-clob.polymarket.com/ws/"):
        self.url = url
        self.api_key = api_key
        self.conn = None

    async def connect(self) -> None:
        headers = {"Authorization": f"Bearer {self.api_key}"}
        self.conn = await websockets.connect(self.url, extra_headers=headers)

    async def subscribe(self, channel: str) -> None:
        await self.conn.send(f"SUBSCRIBE {channel}")

    async def unsubscribe(self, channel: str) -> None:
        await self.conn.send(f"UNSUBSCRIBE {channel}")

    async def listen(self) -> AsyncIterator[str]:
        async for message in self.conn:
            yield message

    async def close(self) -> None:
        if self.conn:
            await self.conn.close()
