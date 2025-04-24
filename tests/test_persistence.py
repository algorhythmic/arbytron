import pytest
from datetime import datetime
from models import MarketQuote, PriceLevel
from services.persistence import save_quotes

class DummySession:
    def __init__(self):
        self.added = []
        self.committed = False

    def add(self, item):
        self.added.append(item)

    async def commit(self):
        self.committed = True

@pytest.mark.asyncio
async def test_save_quotes_and_metrics(monkeypatch):
    # Prepare dummy quotes
    q1 = MarketQuote(
        platform="kalshi",
        event_id="e1",
        market_id="m1",
        outcomes={"Yes": PriceLevel(bid=0.5, ask=0.6)},
        timestamp=datetime.utcnow()
    )
    q2 = MarketQuote(
        platform="polymarket",
        event_id="e1",
        market_id="m2",
        outcomes={"No": PriceLevel(bid=0.4, ask=0.5)},
        timestamp=datetime.utcnow()
    )
    session = DummySession()
    inc_calls = []
    monkeypatch.setattr(
        'services.persistence.quotes_ingested',
        type('C', (), {'inc': lambda self, n: inc_calls.append(n)})()
    )
    # Call persistence
    await save_quotes([q1, q2], session)
    # Verify session add and commit
    assert len(session.added) == 2
    assert session.committed is True
    # Verify metrics increment
    assert inc_calls == [2]
