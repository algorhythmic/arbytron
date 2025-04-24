import pytest
from datetime import datetime
from models import MarketQuote, PriceLevel, Settings, ArbitrageCandidate
from services.opportunity import identify_opportunities, Opportunity


def create_quote(event_id: str, platform: str, bids_asks: dict) -> MarketQuote:
    outcomes = {k: PriceLevel(bid=v[0], ask=v[1]) for k, v in bids_asks.items()}
    return MarketQuote(
        platform=platform,
        event_id=event_id,
        market_id=f"{event_id}_{platform}",
        outcomes=outcomes,
        timestamp=datetime.utcnow()
    )


def test_no_opportunities_below_threshold():
    q1 = create_quote("e1", "kalshi", {"Yes": (0.6, 0.7), "No": (0.6, 0.7)})
    q2 = create_quote("e1", "polymarket", {"Yes": (0.6, 0.7), "No": (0.6, 0.7)})
    candidate = ArbitrageCandidate(event_key="e1", platform_quotes=[q1, q2])
    settings = Settings(kalshi_api_key="k", polymarket_rpc_url="url", min_spread=0.01)
    opps = identify_opportunities([candidate], settings)
    assert opps == []


def test_identify_positive_opportunity():
    q1 = create_quote("e2", "kalshi", {"Yes": (0.3, 0.4), "No": (0.4, 0.5)})
    q2 = create_quote("e2", "polymarket", {"Yes": (0.35, 0.45), "No": (0.38, 0.48)})
    candidate = ArbitrageCandidate(event_key="e2", platform_quotes=[q1, q2])
    settings = Settings(kalshi_api_key="k", polymarket_rpc_url="url", min_spread=0.05)
    opps = identify_opportunities([candidate], settings)
    assert len(opps) == 1
    opp = opps[0]
    assert isinstance(opp, Opportunity)
    # expected net_cost = 0.4 + 0.5 = 0.9
    assert opp.net_cost == pytest.approx(0.4 + 0.5)
    # expected spread = (1 - 0.9) / 0.9
    expected_spread = (1 - opp.net_cost) / opp.net_cost
    assert opp.spread == pytest.approx(expected_spread)
    assert opp.candidate == candidate
