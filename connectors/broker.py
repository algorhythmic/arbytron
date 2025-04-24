import json
from abc import ABC, abstractmethod
from typing import Any
import aiokafka
import aioredis


class Publisher(ABC):
    @abstractmethod
    async def start(self) -> None:
        pass

    @abstractmethod
    async def publish(self, topic: str, message: Any) -> None:
        pass

    @abstractmethod
    async def stop(self) -> None:
        pass


class KafkaPublisher(Publisher):
    def __init__(self, bootstrap_servers: str):
        self.producer = aiokafka.AIOKafkaProducer(bootstrap_servers=bootstrap_servers)

    async def start(self) -> None:
        await self.producer.start()

    async def publish(self, topic: str, message: Any) -> None:
        payload = message.json() if hasattr(message, "json") else json.dumps(message)
        await self.producer.send_and_wait(topic, payload.encode("utf-8"))

    async def stop(self) -> None:
        await self.producer.stop()


class RedisPublisher(Publisher):
    def __init__(self, address: str):
        self.address = address
        self.redis = None

    async def start(self) -> None:
        self.redis = await aioredis.from_url(self.address)

    async def publish(self, topic: str, message: Any) -> None:
        payload = message.json() if hasattr(message, "json") else json.dumps(message)
        await self.redis.publish(topic, payload)

    async def stop(self) -> None:
        await self.redis.close()
