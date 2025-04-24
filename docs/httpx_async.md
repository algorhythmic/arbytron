# HTTPX Async Support

Source: https://www.python-httpx.org/async/

## Overview
- The `AsyncClient` class enables asynchronous HTTP requests using Python `asyncio`.
- Features include HTTP/2 support, connection pooling, timeout control, streaming responses, and pluggable transports.

## Usage Example
```python
import httpx

async def fetch(url: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()
```

## Key Sections
- **Making Async Requests**: `await client.get/post/etc.`
- **Client Lifecycle**: open via `async with` or explicit `await client.aclose()`.
- **Advanced**: streaming request/response bodies, custom transports.
