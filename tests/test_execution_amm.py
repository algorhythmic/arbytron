import pytest
from datetime import datetime
from models import MarketQuote, PriceLevel
from services.execution_amm import PolymarketAmmExecutor


def create_quote(platform: str, event_id: str, outcomes: dict) -> MarketQuote:
    levels = {k: PriceLevel(bid=v[0], ask=v[1]) for k, v in outcomes.items()}
    return MarketQuote(
        platform=platform,
        event_id=event_id,
        market_id=f"{event_id}_{platform}",
        outcomes=levels,
        timestamp=datetime.utcnow(),
    )


def test_simulate_swap_valid():
    # ask price 0.5, amount 10, max_slippage 0.1
    quote = create_quote("polymarket", "e1", {"Yes": (0.4, 0.5)})
    executor = PolymarketAmmExecutor(rpc_url="http://test", max_slippage=0.1)
    result = executor.simulate_swap(quote, "Yes", amount=10)
    cost = 0.5 * 10
    max_cost = cost * 1.1
    assert result["cost"] == pytest.approx(cost)
    assert result["max_cost"] == pytest.approx(max_cost)
    assert result["slippage"] == pytest.approx(0.1)
    assert result["gas_cost"] == pytest.approx(0.0)
    assert result["total_cost"] == pytest.approx(max_cost)


def test_simulate_swap_invalid_outcome():
    quote = create_quote("polymarket", "e1", {"Yes": (0.4, 0.5)})
    executor = PolymarketAmmExecutor(rpc_url="http://test", max_slippage=0.1)
    with pytest.raises(ValueError):
        executor.simulate_swap(quote, "No", amount=5)
