#!/usr/bin/env python3
"""Creatin a Cashe class"""
import redis
from typing import Union
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
