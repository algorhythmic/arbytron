import pytest
from datetime import datetime
import httpx

from connectors.rest_client import KalshiRestClient, PolymarketRestClient
from models import MarketQuote

@pytest.mark.asyncio
async def test_kalshi_fetch_quotes():
    sample = {"markets": [{
        "event_id": "e1",
        "market_id": "m1",
        "outcomes": {"Yes": {"bid": 0.7, "ask": 0.8}},
        "timestamp": "2025-04-01T12:00:00Z"
    }]}
    transport = httpx.MockTransport(lambda req: httpx.Response(200, json=sample))
    client = KalshiRestClient(base_url="http://test", api_key=None)
    client.client._transport = transport
    quotes = await client.fetch_quotes()
    assert len(quotes) == 1
    q = quotes[0]
    assert isinstance(q, MarketQuote)
    assert q.event_id == "e1"
    assert q.outcomes["Yes"].bid == 0.7

@pytest.mark.asyncio
async def test_polymarket_fetch_quotes():
    sample = {"markets": [{
        "event_id": "e2",
        "market_id": "m2",
        "outcomes": [{"outcome": "No", "bid_price": 0.4, "ask_price": 0.5}],
        "updated_at": "2025-04-02T15:30:00Z"
    }]}
    transport = httpx.MockTransport(lambda req: httpx.Response(200, json=sample))
    client = PolymarketRestClient(base_url="http://test", api_key=None)
    client.client._transport = transport
    quotes = await client.fetch_quotes()
    assert len(quotes) == 1
    q = quotes[0]
    assert isinstance(q, MarketQuote)
    assert q.market_id == "m2"
    assert q.outcomes["No"].ask == 0.5
