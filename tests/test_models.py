import pytest
from datetime import datetime
from models import PriceLevel, MarketQuote, ArbitrageCandidate, Settings


def test_price_level():
    pl = PriceLevel(bid=0.5, ask=0.6)
    assert pl.bid == 0.5
    assert pl.ask == 0.6


def test_market_quote():
    sample = {
        "platform": "kalshi",
        "event_id": "e1",
        "market_id": "m1",
        "outcomes": {
            "Yes": {"bid": 0.7, "ask": 0.8},
            "No": {"bid": 0.9, "ask": 1.0}
        },
        "timestamp": "2025-04-01T12:00:00Z"
    }
    mq = MarketQuote.parse_obj(sample)
    assert mq.platform == "kalshi"
    assert mq.event_id == "e1"
    assert "Yes" in mq.outcomes
    assert isinstance(mq.outcomes["Yes"], PriceLevel)
    assert mq.timestamp == datetime.fromisoformat("2025-04-01T12:00:00+00:00")


def test_arbitrage_candidate():
    sample = {
        "event_key": "e1",
        "platform_quotes": [
            {
                "platform": "kalshi",
                "event_id": "e1",
                "market_id": "m1",
                "outcomes": {"Yes": {"bid": 0.7, "ask": 0.8}},
                "timestamp": "2025-04-01T12:00:00Z"
            }
        ]
    }
    ac = ArbitrageCandidate.parse_obj(sample)
    assert ac.event_key == "e1"
    assert isinstance(ac.platform_quotes, list)
    assert isinstance(ac.platform_quotes[0], MarketQuote)


def test_settings_model():
    settings = Settings(
        kalshi_api_key="testkey",
        polymarket_rpc_url="http://localhost",
        min_spread=0.01,
        min_apy=0.02,
        max_slippage=0.03
    )
    assert settings.kalshi_api_key == "testkey"
    assert settings.min_spread == 0.01
