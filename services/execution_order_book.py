from typing import Any, Dict
from connectors.rest_client import KalshiRestClient


class KalshiOrderBookExecutor:
    """Executor for Kalshi order-book leg with fee tracking."""

    def __init__(self, client: KalshiRestClient, fee_rate: float):
        self.client = client
        self.fee_rate = fee_rate

    async def place_order(
        self, market_id: str, outcome: str, side: str, price: float, size: float
    ) -> Dict[str, Any]:
        """Place order and compute fee."""
        resp = await self.client.place_order(market_id, outcome, side, price, size)
        fee = price * size * self.fee_rate
        resp["fee"] = fee
        return resp

    async def cancel_order(self, order_id: str) -> Dict[str, Any]:
        """Cancel order."""
        return await self.client.cancel_order(order_id)
