from typing import Dict, Tuple, List
from pydantic import BaseModel


class Position(BaseModel):
    event_key: str
    outcome: str
    quantity: float
    avg_cost: float


class PortfolioManager:
    """Tracks positions, computes PnL, and identifies early-exit triggers."""

    def __init__(self):
        self.positions: Dict[Tuple[str, str], Position] = {}

    def record_fill(
        self,
        event_key: str,
        outcome: str,
        size: float,
        price: float,
        side: str,
    ) -> None:
        """Record a fill and update the position."""
        key = (event_key, outcome)
        if key not in self.positions:
            qty = size if side.upper() == "BUY" else -size
            avg = price if side.upper() == "BUY" else 0.0
            self.positions[key] = Position(
                event_key=event_key,
                outcome=outcome,
                quantity=qty,
                avg_cost=avg,
            )
        else:
            pos = self.positions[key]
            if side.upper() == "BUY":
                new_qty = pos.quantity + size
                pos.avg_cost = (
                    (pos.avg_cost * pos.quantity + price * size) / new_qty
                    if new_qty != 0
                    else 0.0
                )
                pos.quantity = new_qty
            else:
                pos.quantity -= size

    def compute_pnls(
        self, latest_prices: Dict[Tuple[str, str], float]
    ) -> Dict[Tuple[str, str], float]:
        """Compute PnL for each position given latest prices."""
        pnls: Dict[Tuple[str, str], float] = {}
        for key, pos in self.positions.items():
            price = latest_prices.get(key)
            if price is None:
                continue
            pnl = (price - pos.avg_cost) * pos.quantity
            pnls[key] = pnl
        return pnls

    def get_exits(
        self, latest_prices: Dict[Tuple[str, str], float], threshold: float
    ) -> List[Position]:
        """Return positions where PnL >= threshold."""
        exits: List[Position] = []
        pnls = self.compute_pnls(latest_prices)
        for key, pnl in pnls.items():
            if pnl >= threshold:
                exits.append(self.positions[key])
        return exits
