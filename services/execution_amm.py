from typing import Dict
from models import MarketQuote


class PolymarketAmmExecutor:
    """Executor for Polymarket AMM leg with simulation."""

    def __init__(self, rpc_url: str, max_slippage: float):
        self.rpc_url = rpc_url
        self.max_slippage = max_slippage

    def simulate_swap(
        self, quote: MarketQuote, outcome: str, amount: float
    ) -> Dict[str, float]:
        """
        Simulate cost to buy `amount` of `outcome` at ask price,
        applying max_slippage tolerance.
        Returns cost, max_cost, slippage, gas_cost, and total_cost.
        """
        if outcome not in quote.outcomes:
            raise ValueError(f"Outcome {outcome} not in quote")
        ask_price = quote.outcomes[outcome].ask
        cost = ask_price * amount
        max_cost = cost * (1 + self.max_slippage)
        slippage = self.max_slippage
        gas_cost = 0.0
        total_cost = max_cost + gas_cost
        return {
            "cost": cost,
            "max_cost": max_cost,
            "slippage": slippage,
            "gas_cost": gas_cost,
            "total_cost": total_cost,
        }
