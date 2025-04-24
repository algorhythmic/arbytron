from pydantic import BaseModel, BaseSettings
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


class Settings(BaseSettings):
    kalshi_api_key: str
    polymarket_rpc_url: str
    database_url: str = "postgresql+asyncpg://localhost/arbytron"
    min_spread: float = 0.001
    min_apy: float = 0.0
    max_slippage: float = 0.005

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
