# Arbytron

Arbytron is an automated arbitrage bot framework for multi-outcome prediction markets. It continuously monitors multiple venues (e.g. Kalshi, Polymarket), identifies cross-platform arbitrage opportunities, executes simultaneous trades to lock in guaranteed profit, and manages open positions with configurable risk controls.

## Features

- **Data Ingestion**  
  - REST-based polling via `httpx`  
  - WebSocket streaming via `websockets`
- **Message Broker Integration**  
  - Kafka (`aiokafka`)  
  - Redis Streams (`aioredis`)
- **Market Matching**  
  - Cross-platform event/market mapping
- **Opportunity Identification**  
  - Liquidity, fees, net-cost, spread & APY computation
- **Execution Engine**  
  - AMM (Polymarket) swaps with slippage & pool fees  
  - Order-Book (Kalshi) orders with fee tracking
- **Position Tracking & Portfolio Management**  
  - Fills, LP shares, PnL, early-exit scheduling
- **Persistence & Logging**  
  - PostgreSQL (async SQLAlchemy)  
  - Structured JSON logs (`structlog`)  
  - Prometheus metrics (`prometheus_client`)
- **CI/CD**  
  - GitHub Actions: lint, type-check, test, coverage

## Architecture

### High-Level Flow

```mermaid
flowchart LR
    DS["Data Source (REST)"] --> DA["Data Acquisition"]
    DA --> MM["Market Matching"]
    MM --> OI["Opportunity Identification"]
    OI --> EE["Execution Engine"]
    EE --> PR["Portfolio & Risk Management"]
    PR --> DP["Data Persistence"]
```

### Sequence Diagram

```mermaid
sequenceDiagram
    participant Poller as REST Poller
    participant WS as WebSocket Client
    participant DA as DataAcquisition
    participant BK as Broker (Kafka/Redis)
    participant MGR as MarketMatching
    participant ID as OpportunityIdentifier
    participant EXE as ExecutionEngine
    participant PM as Polymarket (AMM)
    participant KL as Kalshi (OrderBook)
    participant PT as PositionTracker
    participant PF as PortfolioManager

    alt v1: REST-based Ingestion
        Poller->>DA: HTTP GET /events & /markets
        DA->>DA: validate (Pydantic) & normalize → MarketQuote
        DA->>BK: publish MarketQuote
    else v2: WS-based Ingestion
        WS->>DA: on_message(raw JSON)
        DA->>DA: validate (Pydantic) & normalize → MarketQuote
        DA->>BK: publish MarketQuote
    end

    BK->>MGR: stream MarketQuote
    MGR->>ID: build ArbitrageCandidate list
    ID->>ID: compute liquidity, fees (AMM & OB), net_costs, spread, APY
    alt Opportunity Found
        ID->>EXE: dispatch order legs
        par AMM Leg
            EXE->>PM: on-chain swap (slippage & pool fee)
        and OB Leg
            EXE->>KL: place limit/market order (depth & fees)
        end
        EXE->>PT: record fills & LP shares
    end

    PF->>PT: fetch open positions
    PF->>ID: calculate exit value vs. profit target
    alt Early-Exit Triggered
        PF->>EXE: schedule exit legs
        par AMM Exit
            EXE->>PM: removeLiquidity or swap
        and OB Exit
            EXE->>KL: place sell orders
        end
        EXE->>PT: update/close position
    end
```

## Getting Started

### Prerequisites

- Python 3.11+  
- UV CLI (package manager)  
- Docker & Docker Compose (optional)

### Installation

```bash
git clone https://github.com/algorhythmic/arbytron.git
cd arbytron
python -m venv .venv
pip install uv               # install UV CLI
uv install                   # install dependencies
# or fallback:
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the project root:

```dotenv
KALSHI_API_KEY=your_kalshi_api_key
POLYMARKET_RPC_URL=your_polymarket_rpc_url
DATABASE_URL=postgresql+asyncpg://user:pass@localhost/arbytron
MIN_SPREAD=0.001
MIN_APY=0.0
MAX_SLIPPAGE=0.005
```

## Usage

```bash
python main.py
```

## Testing

```bash
pytest --cov
```

## Documentation

- Development plan: [docs/scratchpad.md](docs/scratchpad.md)  
- Technical specification: [docs/spec.md](docs/spec.md)  
- Architecture diagrams: [docs/diagrams.md](docs/diagrams.md)

## Contributing

Contributions are welcome! Please follow the commit plan in `docs/scratchpad.md` for consistent history.

## License

This project is licensed under the MIT License.
