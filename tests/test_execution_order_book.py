import pytest
from services.execution_order_book import KalshiOrderBookExecutor

class DummyClient:
    def __init__(self):
        self.orders = []
        self.cancellations = []

    async def place_order(self, market_id, outcome, side, price, size):
        resp = {"order_id": "o1", "market_id": market_id, "outcome": outcome, "side": side, "price": price, "size": size}
        self.orders.append((market_id, outcome, side, price, size))
        return resp

    async def cancel_order(self, order_id):
        self.cancellations.append(order_id)
        return {"cancelled": order_id}

@pytest.mark.asyncio
async def test_place_order_fee():
    client = DummyClient()
    executor = KalshiOrderBookExecutor(client, fee_rate=0.02)
    resp = await executor.place_order("m1", "Yes", "BUY", 0.5, 10)
    assert client.orders[0] == ("m1", "Yes", "BUY", 0.5, 10)
    assert resp["order_id"] == "o1"
    expected_fee = 0.5 * 10 * 0.02
    assert resp["fee"] == pytest.approx(expected_fee)

@pytest.mark.asyncio
async def test_cancel_order():
    client = DummyClient()
    executor = KalshiOrderBookExecutor(client, fee_rate=0.02)
    result = await executor.cancel_order("o1")
    assert client.cancellations == ["o1"]
    assert result == {"cancelled": "o1"}
