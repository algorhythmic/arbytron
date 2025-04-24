from typing import List, Dict
from models import MarketQuote, ArbitrageCandidate


def match_quotes(quotes: List[MarketQuote]) -> List[ArbitrageCandidate]:
    """
    Groups MarketQuote objects by event_id and returns arbitrage candidates for events available on multiple platforms.
    """
    groups: Dict[str, List[MarketQuote]] = {}
    for q in quotes:
        key = q.event_id
        groups.setdefault(key, []).append(q)

    candidates: List[ArbitrageCandidate] = []
    for key, qs in groups.items():
        if len(qs) > 1:
            candidates.append(ArbitrageCandidate(event_key=key, platform_quotes=qs))
    return candidates
