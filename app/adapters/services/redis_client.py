from typing import NewType

from redis import Redis

RedisEndpointUrl = NewType("RedisEndpointUrl", str)
RedisPort = NewType("RedisPort", int)


class RedisClient:
    def __init__(
        self,
        endpoint_url: RedisEndpointUrl,
        port: RedisPort,
    ):
        self._redis = Redis(host=endpoint_url, port=port, db=0)

    def get(self, key: str):
        return self._redis.get(key)

    def set(self, key: str, value: str, ex: int = None):
        return self._redis.set(key, value, ex=ex)

    def delete(self, key: str):
        return self._redis.delete(key)
