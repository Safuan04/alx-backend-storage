#!/usr/bin/env python3
"""Creatin a Cashe class"""
import redis
from typing import Union, Callable, Optional
import uuid


class Cache():
    def __init__(self) -> None:
        """Storing an instance of the redis client"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """This method take a data argument and returns a string"""
        random_key = str(uuid.uuid4())
        self._redis.set(random_key, data)
        return random_key

    def get(self, key: str, fn: Optional[Callable]):
        """This method takes a key string argument
            and an optional Callable argument named fn"""
        value = self._redis.get(key)

        if not value:
            return None

        if fn:
            return fn(value)
        else:
            return value

    def get_str(self, key):
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key):
        return self.get(key, fn=int)
