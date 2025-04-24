import pytest
from datetime import datetime

from models import MarketQuote, PriceLevel
from services.match import match_quotes


def create_quote(event_id: str, platform: str, bid: float = 0.5, ask: float = 0.6) -> MarketQuote:
    outcomes = {"Yes": PriceLevel(bid=bid, ask=ask)}
    return MarketQuote(
        platform=platform,
        event_id=event_id,
        market_id=f"m_{platform}",
        outcomes=outcomes,
        timestamp=datetime.utcnow(),
    )


def test_no_match_single_quote():
    q1 = create_quote("e1", "kalshi")
    candidates = match_quotes([q1])
    assert candidates == []


def test_match_two_quotes():
    q1 = create_quote("e2", "kalshi", bid=0.7, ask=0.8)
    q2 = create_quote("e2", "polymarket", bid=0.75, ask=0.85)
    candidates = match_quotes([q1, q2])
    assert len(candidates) == 1
    cand = candidates[0]
    assert cand.event_key == "e2"
    assert set(q.platform for q in cand.platform_quotes) == {"kalshi", "polymarket"}


def test_multiple_events():
    q1 = create_quote("e3", "kalshi")
    q2 = create_quote("e3", "polymarket")
    q3 = create_quote("e4", "kalshi")
    q4 = create_quote("e5", "polymarket")
    candidates = match_quotes([q1, q2, q3, q4])
    keys = {c.event_key for c in candidates}
    assert keys == {"e3"}
