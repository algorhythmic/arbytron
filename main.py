import asyncio
from models import Settings
from logging_config import configure_logging
from db.session import AsyncSessionLocal
from connectors.rest_client import KalshiRestClient, PolymarketRestClient
from services.persistence import save_quotes

async def main():
    # Configure logging and load settings
    configure_logging()
    settings = Settings()

    # Initialize REST connectors
    kalshi_client = KalshiRestClient(base_url="https://api.kalshi.com", api_key=settings.kalshi_api_key)
    polymarket_client = PolymarketRestClient(base_url="https://api.polymarket.com", api_key=None)

    # Fetch and persist quotes
    async with AsyncSessionLocal() as session:
        quotes1 = await kalshi_client.fetch_quotes()
        quotes2 = await polymarket_client.fetch_quotes()
        all_quotes = quotes1 + quotes2
        await save_quotes(all_quotes, session)
        print(f"Persisted {len(all_quotes)} quotes")

    # Clean up clients
    await kalshi_client.close()
    await polymarket_client.close()

if __name__ == "__main__":
    asyncio.run(main())