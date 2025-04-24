from typing import List, Dict
from pydantic import BaseModel
from models import ArbitrageCandidate, PriceLevel
from models import Settings


class Opportunity(BaseModel):
    event_key: str
    net_cost: float
    spread: float
    slippage: float
    apy: float
    candidate: ArbitrageCandidate


def identify_opportunities(
    candidates: List[ArbitrageCandidate], settings: Settings
) -> List[Opportunity]:
    opportunities: List[Opportunity] = []
    for c in candidates:
        # compute min ask price per outcome and its slippage (ask - bid)
        min_asks: Dict[str, float] = {}
        slippages: Dict[str, float] = {}
        for mq in c.platform_quotes:
            for outcome, pl in mq.outcomes.items():
                ask = pl.ask
                bid = pl.bid
                if outcome not in min_asks or ask < min_asks[outcome]:
                    min_asks[outcome] = ask
                    slippages[outcome] = ask - bid
        # net cost to buy one of each outcome
        net_cost = sum(min_asks.values())
        # profit assuming payout = 1
        profit = 1.0 - net_cost
        # spread relative to cost
        spread = profit / net_cost if net_cost > 0 else 0.0
        # average slippage across outcomes
        slippage = sum(slippages.values()) / len(slippages) if slippages else 0.0
        # APY placeholder equal to spread
        apy = spread
        # filter by minimum spread threshold
        if spread >= settings.min_spread:
            opp = Opportunity(
                event_key=c.event_key,
                net_cost=net_cost,
                spread=spread,
                slippage=slippage,
                apy=apy,
                candidate=c,
            )
            opportunities.append(opp)
    return opportunities
