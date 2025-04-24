import json
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import Quote
from models import MarketQuote
from metrics import quotes_ingested


async def save_quotes(quotes: List[MarketQuote], session: AsyncSession) -> None:
    """Persist a list of MarketQuote objects and increment metrics."""
    for mq in quotes:
        q = Quote(
            platform=mq.platform,
            event_id=mq.event_id,
            market_id=mq.market_id,
            outcomes={k: v.dict() for k, v in mq.outcomes.items()},
            timestamp=mq.timestamp,
        )
        session.add(q)
    await session.commit()
    quotes_ingested.inc(len(quotes))
