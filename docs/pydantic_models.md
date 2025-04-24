# Pydantic Models

Source: https://docs.pydantic.dev/latest/concepts/models/

## Basic Model Usage
```python
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict, List

class PriceLevel(BaseModel):
    bid: float
    ask: float

class MarketQuote(BaseModel):
    platform: str
    event_id: str
    market_id: str
    outcomes: Dict[str, PriceLevel]
    timestamp: datetime

class ArbitrageCandidate(BaseModel):
    event_key: str
    platform_quotes: List[MarketQuote]
```

## Validation & Serialization
- `.parse_obj()` to parse raw dicts.
- `.json()` to serialize models.

## Settings via BaseSettings
```python
from pydantic import BaseSettings

class Settings(BaseSettings):
    kalshi_api_key: str
    polymarket_rpc_url: str
    min_spread: float = 0.001
    class Config:
        env_file = '.env'
```
