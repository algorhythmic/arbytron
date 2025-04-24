import httpx
from tenacity import retry, stop_after_attempt, wait_exponential
from datetime import datetime
from typing import List, Dict, Any

from models import MarketQuote, PriceLevel


class RestConnectorBase:
    def __init__(
        self,
        base_url: str,
        api_key: str = None,
        timeout: float = 10.0,
        max_retries: int = 3,
    ):
        headers: Dict[str, str] = {}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"
        self.client = httpx.AsyncClient(
            base_url=base_url,
            headers=headers,
            timeout=httpx.Timeout(timeout),
        )
        self._max_retries = max_retries

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=5))
    async def _get_json(self, path: str, params: Dict[str, Any] = None) -> Any:
        response = await self.client.get(path, params=params)
        response.raise_for_status()
        return response.json()

    async def close(self) -> None:
        await self.client.aclose()


class KalshiRestClient(RestConnectorBase):
    """REST client for Kalshi order-book markets."""

    async def fetch_quotes(self) -> List[MarketQuote]:
        data = await self._get_json("/v1/markets")
        quotes: List[MarketQuote] = []
        for m in data.get("markets", []):
            outcomes_data = m.get("outcomes", {})  # expects {'Yes': {'bid': x, 'ask': y}, ...}
            outcomes = {k: PriceLevel(**v) for k, v in outcomes_data.items()}
            ts = m.get("timestamp") or m.get("updated_at")
            timestamp = datetime.fromisoformat(ts)
            quote = MarketQuote(
                platform="kalshi",
                event_id=m.get("event_id", ""),
                market_id=m.get("market_id", ""),
                outcomes=outcomes,
                timestamp=timestamp,
            )
            quotes.append(quote)
        return quotes

    async def place_order(self, market_id: str, outcome: str, side: str, price: float, size: float) -> Dict[str, Any]:
        """Place an order on Kalshi order-book markets."""
        payload = {
            "market_id": market_id,
            "outcome": outcome,
            "side": side,
            "price": price,
            "size": size,
        }
        response = await self.client.post("/v1/orders", json=payload)
        response.raise_for_status()
        return response.json()

    async def cancel_order(self, order_id: str) -> Dict[str, Any]:
        """Cancel an existing order by ID."""
        response = await self.client.delete(f"/v1/orders/{order_id}")
        response.raise_for_status()
        return response.json()


class PolymarketRestClient(RestConnectorBase):
    """REST client for Polymarket AMM markets."""

    async def fetch_quotes(self) -> List[MarketQuote]:
        data = await self._get_json("/api/v2/markets")
        quotes: List[MarketQuote] = []
        for m in data.get("markets", []):
            # map outcome list to {'OutcomeName': {'bid': x, 'ask': y}}
            raw_outcomes = m.get("outcomes", [])
            outcomes_dict: Dict[str, Dict[str, float]] = {
                o.get("outcome"): {"bid": o.get("bid_price"), "ask": o.get("ask_price")} for o in raw_outcomes
            }
            outcomes = {k: PriceLevel(**v) for k, v in outcomes_dict.items()}
            ts = m.get("updated_at") or m.get("timestamp")
            timestamp = datetime.fromisoformat(ts)
            quote = MarketQuote(
                platform="polymarket",
                event_id=m.get("event_id", ""),
                market_id=m.get("market_id", ""),
                outcomes=outcomes,
                timestamp=timestamp,
            )
            quotes.append(quote)
        return quotes
