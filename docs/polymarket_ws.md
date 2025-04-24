# Polymarket CLOB WebSocket API Reference

Source: https://docs.polymarket.com/#introduction

## Endpoint
```text
wss://ws-subscriptions-clob.polymarket.com/ws/
```

## Authentication
- Use API key authentication on WS handshake (via query param or header as per Polymarket spec).

## Subscription Commands
- To subscribe or unsubscribe to channels, send plain-text commands:
```text
SUBSCRIBE {channel}
UNSUBSCRIBE {channel}
```
Available channels:
- **user** (authenticated channel for user orders/trades)
- **market** (public channel for order book updates)

## User Channel
- Subscribe: `SUBSCRIBE user`
- Requires valid API key.

### `trade` Message
Emitted on trade executions or status updates.
```json
{
  "asset_id": "...",
  "event_type": "trade",
  "maker_orders": [ /* list of maker order objects */ ],
  "market": "<market_id>",
  "outcome": "YES|NO",
  "price": "<price>",
  "size": "<size>",
  "status": "MATCHED|MINED|CONFIRMED|RETRYING|FAILED",
  "timestamp": "<unix_ts>",
  "type": "TRADE"
}
```

### `order` Message
Emitted on order placement, update, or cancellation.
```json
{
  "event_type": "order",
  "id": "<order_id>",
  "market": "<market_id>",
  "price": "<price>",
  "side": "BUY|SELL",
  "size_matched": "<matched_size>",
  "timestamp": "<unix_ts>",
  "type": "PLACEMENT|UPDATE|CANCELLATION"
}
```

## Market Channel
- Subscribe: `SUBSCRIBE market`
- No authentication required.

### `book` Message
Depth snapshot or delta for order book.
```json
{
  "event_type": "book",
  "buys": [ {"price": "<p>", "size": "<s>"}, ... ],
  "sells": [ {"price": "<p>", "size": "<s>"}, ... ],
  "timestamp": "<unix_ts>",
  "hash": "<state_hash>"
}
```

### `price_change` Message
Emitted on book updates.
```json
{
  "event_type": "price_change",
  "changes": [ {"price": "<p>", "side": "BUY|SELL", "size": "<s>"}, ... ],
  "timestamp": "<unix_ts>",
  "hash": "<state_hash>"
}
```

### `tick_size_change` Message
Emitted when market tick size changes.
```json
{
  "event_type": "tick_size_change",
  "old_tick_size": "<old>",
  "new_tick_size": "<new>",
  "timestamp": "<unix_ts>"
}
```
