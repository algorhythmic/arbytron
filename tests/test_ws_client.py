import pytest
import json
import websockets
from connectors.ws_client import KalshiWSClient, PolymarketWSClient


class DummyConn:
    def __init__(self, messages):
        self.sent = []
        self.messages = list(messages)

    async def send(self, msg):
        self.sent.append(msg)

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self.messages:
            return self.messages.pop(0)
        raise StopAsyncIteration

    async def close(self):
        self.closed = True


@pytest.mark.asyncio
async def test_kalshi_ws_subscribe_listen_unsubscribe(monkeypatch):
    dummy = DummyConn(['{"foo": "bar"}'])
    monkeypatch.setattr(websockets, 'connect', lambda url, extra_headers=None: dummy)
    client = KalshiWSClient(api_key='testkey')
    await client.connect()
    await client.subscribe('order_book', market_id='m1')
    assert dummy.sent[0] == json.dumps({
        'id': 1,
        'cmd': 'subscribe',
        'params': {'channel': 'order_book', 'market_id': 'm1'}
    })
    results = [msg async for msg in client.listen()]
    assert results == [{'foo': 'bar'}]
    await client.unsubscribe('order_book', market_id='m1')
    assert dummy.sent[-1] == json.dumps({
        'id': 2,
        'cmd': 'unsubscribe',
        'params': {'channel': 'order_book', 'market_id': 'm1'}
    })
    await client.close()
    assert hasattr(dummy, 'closed')


@pytest.mark.asyncio
async def test_polymarket_ws_subscribe_listen_unsubscribe(monkeypatch):
    dummy = DummyConn(['msg1', 'msg2'])
    monkeypatch.setattr(websockets, 'connect', lambda url, extra_headers=None: dummy)
    client = PolymarketWSClient(api_key='testkey')
    await client.connect()
    await client.subscribe('user')
    assert dummy.sent[0] == 'SUBSCRIBE user'
    results = [msg async for msg in client.listen()]
    assert results == ['msg1', 'msg2']
    await client.unsubscribe('user')
    assert dummy.sent[-1] == 'UNSUBSCRIBE user'
    await client.close()
    assert hasattr(dummy, 'closed')
