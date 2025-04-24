import pytest
import json
from connectors import broker as broker_module

class DummyProducer:
    def __init__(self):
        self.started = False
        self.stopped = False
        self.sent = []

    async def start(self):
        self.started = True

    async def send_and_wait(self, topic, payload):
        self.sent.append((topic, payload))

    async def stop(self):
        self.stopped = True

class DummyRedis:
    def __init__(self):
        self.published = []
        self.closed = False

    async def publish(self, topic, payload):
        self.published.append((topic, payload))

    async def close(self):
        self.closed = True

@pytest.mark.asyncio
async def test_kafka_publisher(monkeypatch):
    dummy = DummyProducer()
    monkeypatch.setattr(broker_module.aiokafka, 'AIOKafkaProducer', lambda bootstrap_servers: dummy)
    pub = broker_module.KafkaPublisher(bootstrap_servers="server1:9092")
    await pub.start()
    assert dummy.started
    class Msg:
        def json(self):
            return json.dumps({"foo": "bar"})
    msg = Msg()
    await pub.publish("topic1", msg)
    # Expect payload as bytes
    assert dummy.sent == [("topic1", b'{"foo": "bar"}')]
    await pub.stop()
    assert dummy.stopped

@pytest.mark.asyncio
async def test_redis_publisher(monkeypatch):
    dummy = DummyRedis()
    async def dummy_from_url(addr):
        return dummy
    monkeypatch.setattr(broker_module.aioredis, 'from_url', dummy_from_url)
    pub = broker_module.RedisPublisher(address="redis://localhost:6379")
    await pub.start()
    assert pub.redis is dummy
    msg = {"baz": 123}
    await pub.publish("topic2", msg)
    assert dummy.published == [("topic2", json.dumps(msg))]
    await pub.stop()
    assert dummy.closed
