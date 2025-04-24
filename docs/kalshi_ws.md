# Kalshi WebSocket API Reference

Source: https://trading-api.readme.io/v2.0.0/reference/ws

## Endpoint
```
wss://api.elections.kalshi.com/trade-api/ws/v2
```
- Secure WebSocket (wss) over TLS.
- Requires API key authentication on connection.

## Protocol Overview
- All messages encoded as JSON.
- Bi-directional async messages:
  - **Commands** (client ➔ server) to subscribe/unsubscribe.
  - **Updates** (server ➔ client) with data for subscribed channels.
- Use `id` in commands to correlate responses.

## Command Format
```json
{
  "id": <int>,        // Unique within WS session
  "cmd": "subscribe"|"unsubscribe"|"update_subscription",
  "params": { ... }   // Channel-specific parameters
}
```

## Subscription Channels
- **order_book**: depth snapshots & deltas for a market.
- **ticker**: best bid/ask price updates.
- **trade**: executed trade events.
- **fill**: fill confirmations for orders.
- **market_lifecycle**: market open/close/status events.

### Example Subscribe
```json
{
  "id": 1,
  "cmd": "subscribe",
  "params": { "channel": "order_book", "market_id": "m1" }
}
```

## Server Messages
- Include same `id` as related command.
- Typical fields: `channel`, `data`, `timestamp`, `id`.
- Heartbeats may be sent to keep connection alive.

## Recovery & Heartbeats
- Clients may reconnect and resubscribe if connection drops.
- Server sends periodic heartbeats; monitor to detect timeouts.
