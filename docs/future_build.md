# When to Introduce Big-Data Frameworks

As Arbytron grows—more platforms, higher message rates, larger historical archives—you may outgrow a simple Python+Redis+Postgres stack. Here’s when each technology makes sense:

---

## 1. Apache Kafka  
• **Use Case:** Durable, high-throughput message bus to decouple ingestion from downstream processing.  
• **When:**  
  - You hit hundreds of thousands of `MarketQuote` messages per second.  
  - Need multiple independent consumers (matching, analytics, alerting) reading the same stream.  
  - Require replay or time-travel of inbound data.

---

## 2. Apache Flink  
• **Use Case:** Stateful, low-latency stream processing (windowed joins, CEP, exactly-once).  
• **When:**  
  - You need continuous sliding-window analytics (e.g. rolling liquidity metrics).  
  - Must coordinate complex event-pattern detection across multiple streams.  
  - Require end-to-end exactly-once semantics on your arbitrage triggers.

---

## 3. Apache Spark (Structured Streaming & Batch)  
• **Use Case:** Large-scale batch or micro-batch analytics and ML pipelines.  
• **When:**  
  - Backtesting strategies over months/years of historical quotes (GBs–TBs).  
  - Training machine-learning models for predictive order-placement or risk scoring.  
  - Running nightly aggregations or report generation on your historical trade database.

---

## 4. Apache Iceberg  
• **Use Case:** ACID-compliant table format on object storage (S3/GCS) with schema evolution & time-travel.  
• **When:**  
  - You archive raw market data & trade logs in a data lake.  
  - Need efficient point-in-time queries (e.g. “what was the best ask at 2025-01-01T12:00Z?”).  
  - Require evolving your quote schema (adding fields) without rewriting massive datasets.

---

### Example Hybrid Architecture  
```text
[WS Ingestion] ➔ Kafka ➔  
    ├─ Flink (live arbitrage) ➔ Execution  
    ├─ Spark Streaming (metrics) ➔ Iceberg on S3  
    └─ Batch Spark jobs on Iceberg for backtests/ML
```
---

# REST to WebSocket

Switching from a pull-based REST client to a push-based WebSocket feed in the Data Acquisition layer turns it into a true streaming ingestion pipeline. You’d still normalize & validate into your MarketQuote model, but the way you get data, buffer it, and hand it off downstream changes:

## 1. Persistent Connection
Replace httpx polling + tenacity retries with a WebSocket client:
• websockets or aiohttp – async, low-latency, built-in ping/heartbeat.
• Reconnection logic with exponential back-off; health checks + alert on disconnect.

## 2. Event-Driven Pipeline
Ingest raw messages on arrival, don’t wait for a poll interval.
Publish normalized quotes to an internal message bus instead of calling the Matching module directly.
• Kafka (aiokafka) or Redis Streams for durable, ordered buffering.
• Optionally Faust for lightweight Python streaming (windowing, aggregation).

## 3. Concurrency & Back-Pressure
One asyncio Task per connection; use queues (asyncio.Queue, aiokafka producer) to decouple I/O from downstream processing.
Monitor queue lengths and throttle or shed load if the Matching/Execution layers lag.

## 4. Validation & Schema
Still use Pydantic to parse/validate each incoming WS payload into MarketQuote.
Raise & log schema errors, drop malformed messages.

## 5. Architecture Diagram (revised)
```text
┌─────────────────┐    ┌──────────────┐     ┌─────────────────┐
│ External WS     │──▶ │ WS Connector │──▶ │ Internal Broker │──┐
│ Endpoints       │    │ Service      │     │ (Kafka/Redis)   │  │
└─────────────────┘    └──────────────┘     └─────────────────┘  │
                                                                 ▼
                                                      ┌─────────────────┐
                                                      │ Matching &      │
                                                      │ Identification  │
                                                      │ Consumers       │
                                                      └─────────────────┘
```

## 6. Tech-Stack Shifts
HTTPX → websockets / aiohttp for ingestion
Tenacity → built-in reconnect+ping/heartbeat loop
Direct in-proc dispatch → Kafka/Redis Streams + aiokafka/aioredis
Add Faust (optional) for stateful stream processing
Keep Pydantic for model validation

## 7. Ops & Monitoring
Track WS-connection health, message lag (broker offsets), reconnection counts in Prometheus.
Autoscale WS connector pods based on queue lag.

---

In summary, you’ll split ingestion into a dedicated, event-driven microservice that maintains long-lived connections, publishes to a broker, and hand off to your existing matching/execution pipeline. This buys you lower latency, higher throughput, and better decoupling at the cost of introducing a message-broker tier and connection-management logic.