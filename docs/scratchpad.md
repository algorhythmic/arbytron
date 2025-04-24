# Background and Motivation  
Arbytron is an automated arbitrage bot framework for multi-outcome prediction markets, as defined in `docs/spec.md`. It will ingest market data, normalize quotes, match markets, identify arbitrage opportunities with precise fee and liquidity checks, execute trades atomically across AMM and order-book platforms, track open positions, manage risk, and persist data reliably.

## Key Challenges and Analysis  
- **Data Ingestion**: support REST polling and WebSocket streaming with asyncio, error handling, and rate limits.  
- **Repository Hygiene**: decide on ignore patterns for local artifacts and configs (`.env`, `.windsurfrules`, `notebooks/`, `.venv/`, `__pycache__/`, `*.pyc`).  
- **Model Normalization**: unify AMM and order-book quote structures for downstream processing.  
- **Fee Calculation**: implement Kalshi trading/maker formulas (roundup, rebates) and AMM pool fees.  
- **Opportunity Logic**: compute net costs, spread%, APY, and enforce liquidity thresholds.  
- **Atomic Execution**: coordinate multi-leg trades across on-chain and off-chain channels with rollback.  
- **Position Management**: track fills, LP shares, PnL, and support early-exit triggers.  
- **Scalability & Reliability**: use message broker (Kafka/Redis), structured logging, metrics, and robust persistence.
- **Dependency Management**: adopt UV best practice—declare dependencies in `pyproject.toml`, maintain a universal lockfile `uv.lock`, remove root `requirements.txt`, and optionally produce a pip-compatible `docs/requirements.txt` via `uv pip compile`.

## High-level Task Breakdown  
1. **Project Setup & Configuration**  
   - **Create and activate Python virtual environment** (`python -m venv .venv` + `source .venv/bin/activate`).
   - **Scaffold** Python 3.11+ project, `requirements.txt` or Poetry, Dockerfile, pre-commit hooks.  
   - **Success**: venv created & activated; repo builds, lint/test pipeline runs, Docker image builds locally.
2. **Data Models & Settings**  
   - Define Pydantic models (`MarketQuote`, `PriceLevel`, `ArbitrageCandidate`, settings).  
   - **Success**: models validate sample JSON without errors.
3. **REST Connector Implementation**  
   - Build httpx-based REST client with retry/timeout logic for Kalshi & Polymarket.  
   - **Success**: fetch and normalize quotes to `MarketQuote` objects.  
4. **WebSocket Connector**  
   - Implement asyncio+websockets client for real-time updates.  
   - **Success**: receive and validate live messages over WS.  
5. **Message Broker Integration**  
   - Abstract publisher interface; integrate aiokafka or aioredis streams.  
   - **Success**: market quotes published to broker topic/stream.  
6. **Market Matching Logic**  
   - Match events/series across platforms (exact & fuzzy).  
   - **Success**: generate correct `ArbitrageCandidate` lists for sample data.  
7. **Opportunity Identification Module**  
   - Compute slippage, volume-weighted prices, fees, net costs, spread, APY.  
   - **Success**: detect known arbitrage in test scenarios.  
8. **Execution Engine – AMM Leg**  
   - Develop Polymarket swap logic with slippage tolerance & gas.  
   - **Success**: simulate trade on testnet or mock.  
9. **Execution Engine – Order-Book Leg**  
   - Implement order placement/cancellation for Kalshi with fee tracking.  
   - **Success**: mock orders placed and fees calculated.  
10. **Position Tracker & Portfolio Manager**  
    - Record fills, LP shares, PnL; trigger early-exit based on thresholds.  
    - **Success**: accurate position state for sample trades.  
11. **Data Persistence & Logging**  
    - Define PostgreSQL schema, integrate async ORM, structured JSON logs, Prometheus metrics.  
    - **Success**: data persisted and metrics exposed.  
12. **Testing & CI/CD**  
    - Write pytest-asyncio tests, coverage targets; configure GitHub Actions.  
    - **Success**: CI pipeline passes all tests with coverage ≥80%.
13. **Main Entrypoint Implementation**  
   - Implement main entrypoint to orchestrate data ingestion, opportunity detection, and execution.  
   - **Success**: main entrypoint runs without errors and performs expected tasks.
14. **Configure .gitignore and scaffolding**  
   - Commit Message: `chore: add .gitignore entries and scaffold files`
   - Changes:
     - Create/update `.gitignore` with patterns:
       ```text
       # Local artifacts
       .env
       .windsurfrules
       .venv/
       __pycache__/
       *.pyc
       notebooks/
       ```
     - Add missing scaffolding files:
       - `services/__init__.py`
       - `tests/test_models.py`
   - **Success**: unwanted files no longer appear in `git status`; scaffolding files and docs remain tracked.
15. **Migrate to UV package manager**  
   - Generate `pyproject.toml` with `[project]` metadata and dependencies.  
   - Run `uv lock` to produce `uv.lock`.  
   - Remove root `requirements.txt`.  
   - Optionally run `uv pip compile docs/requirements.in --universal --output-file docs/requirements.txt` to support pip workflows.  
   - Update CI (`.github/workflows/ci.yml`) to replace `pip install -r requirements.txt` with `uv install` or `uv sync docs/requirements.txt`.  
   - Update README and developer docs to reflect UV commands.  
   - **Success**: `uv install` / `uv sync` reconstructs environment, CI passes, no root `requirements.txt` remains.

## Git Commit Plan

1. **Task 1: Project setup & configuration**  
   - Commit Message: `feat: project setup & configuration`  
   - Changes: virtualenv scaffold, `requirements.txt` initial, `Dockerfile`, pre-commit hooks

2. **Task 2: Data models & settings**  
   - Commit Message: `feat: add Pydantic data models and settings`  
   - Changes: `models.py` with `MarketQuote`, `PriceLevel`, `ArbitrageCandidate`, `Settings`, plus scaffold `services/__init__.py` and tests (`tests/test_models.py`).

3. **Task 3: REST connector implementation**  
   - Commit Message: `feat: implement REST connectors for Kalshi & Polymarket`  
   - Changes: `connectors/rest_client.py`, tests for REST client

4. **Task 4: WebSocket connector**  
   - Commit Message: `feat: implement WebSocket clients`  
   - Changes: `connectors/ws_client.py`, tests for WS client

5. **Task 5: Message broker integration**  
   - Commit Message: `feat: add Kafka and Redis publishers`  
   - Changes: `connectors/broker.py`, tests for broker

6. **Task 6: Market matching logic**  
   - Commit Message: `feat: implement market matching logic`  
   - Changes: `services/match.py`, tests for matching

7. **Task 7: Opportunity identification**  
   - Commit Message: `feat: add opportunity identification module`  
   - Changes: `services/opportunity.py`, tests for opportunity logic

8. **Task 8: Execution engine – AMM leg**  
   - Commit Message: `feat: implement AMM execution engine`  
   - Changes: `services/execution_amm.py`, tests for AMM executor

9. **Task 9: Execution engine – order-book leg**  
   - Commit Message: `feat: implement order-book execution engine`  
   - Changes: `services/execution_order_book.py`, tests for order-book executor

10. **Task 10: Position tracker & portfolio manager**  
    - Commit Message: `feat: add position tracking and PnL logic`  
    - Changes: `services/position.py`, tests for position manager

11. **Task 11: Data persistence & logging**  
    - Commit Message: `feat: integrate database persistence and logging`  
    - Changes: `db/models.py`, `db/session.py`, `services/persistence.py`, `logging_config.py`, `metrics.py`, tests, updated `requirements.txt`

12. **Task 12: Testing & CI/CD**  
   - Commit Message: `ci: add CI pipeline and coverage`  
   - Changes: `pytest-cov` in `requirements.txt`, `.github/workflows/ci.yml`

13. **Task 13: Main Entrypoint**  
   - Commit Message: `feat: implement main entrypoint`  
   - Changes: `main.py` initialization, fetch & persist flow

14. **Task 14: Configure .gitignore and scaffolding**  
   - Commit Message: `chore: add .gitignore entries and scaffold files`  
   - Changes: `.gitignore`, `services/__init__.py`, `tests/test_models.py`

15. **Task 15: Migrate to UV package manager**  
   - Commit Message: `chore: migrate dependencies to UV (pyproject.toml & uv.lock)`  
   - Changes:
     - `pyproject.toml` (declared dependencies)
     - `uv.lock`
     - remove `requirements.txt`
     - optionally add `docs/requirements.in` and `docs/requirements.txt` for pip
     - update `.github/workflows/ci.yml`, README, docs to use UV

## Project Status Board  
- [ ] Task 1: Project setup & configuration  
- [ ] Task 2: Data models & settings  
- [ ] Task 3: REST connector implementation  
- [ ] Task 4: WebSocket connector  
- [ ] Task 5: Message broker integration  
- [ ] Task 6: Market matching logic  
- [ ] Task 7: Opportunity identification  
- [ ] Task 8: Execution engine – AMM leg  
- [ ] Task 9: Execution engine – order-book leg  
- [ ] Task 10: Position tracker & portfolio manager  
- [ ] Task 11: Data persistence & logging  
- [ ] Task 12: Testing & CI/CD  
- [ ] Task 13: Main Entrypoint Implementation  
- [ ] Task 14: Configure .gitignore and scaffolding  
- [ ] Task 15: Migrate to UV package manager  
+-> Ensures adoption of UV best practices and reproducible builds

## Executor's Feedback or Assistance Requests  
- Completed Task 2: Pydantic models implemented and validated via tests.
- Completed Task 3: REST connector built and tested with MockTransport.
- Completed Task 4: WS clients implemented and tested.
- Completed Task 5: Kafka & Redis publishers implemented and tested.
- Completed Task 6: Basic matching logic implemented and tested.
- Completed Task 7: Opportunity detection logic implemented and tested.
- Completed Task 8: AMM leg executor implemented and tested.
- Completed Task 9: Order-book leg executor implemented and tested.
- Completed Task 10: Position tracking and PnL logic implemented and tested.
- Completed Task 11: Persistence layer and logging configured with tests.
- Completed Task 12: CI pipeline configured with lint, mypy, pytest-cov.
- Completed Task 13: Main entrypoint implemented and verified fetching and persistence flow.
- Added web socket API reference docs based on official Kalshi & Polymarket sources.