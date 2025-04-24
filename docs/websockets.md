# Python WebSockets (websockets library)

Source: https://websockets.readthedocs.io/en/stable/intro/index.html

## Requirements
- Python ≥ 3.9
- No external dependencies

## Installation
```bash
pip install websockets
```

## Usage Example
```python
import asyncio
import websockets

async def main():
    uri = "wss://example.com/feed"
    async with websockets.connect(uri) as ws:
        await ws.send("Hello server!")
        message = await ws.recv()
        print(f"Received: {message}")

asyncio.run(main())
```

## Key Concepts
- `websockets.connect()`: open/close WebSocket connection.
- `send()` / `recv()`: send and receive messages.
- Context manager handles handshake and teardown.
