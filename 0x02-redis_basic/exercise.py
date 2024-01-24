#!/usr/bin/env python3
"""Creatin a Cashe class"""
import redis
from typing import Union, Callable, Optional
import uuid
from functools import wraps

def count_calls(method: Callable) -> Callable:
    """"""
    @wraps(method)
    def function_wrapper(self, *args, **kwargs):
        """"""
        key = method.__qualname__
        value = self._redis.get(key)
        if value:
            value = int(value) + 1
        else:
            value = 1
        
        self._redis.set(key, value)

        return method(self, *args, **kwargs)
    return function_wrapper

class Cache():
    def __init__(self) -> None:
        """Storing an instance of the redis client"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """This method take a data argument and returns a string"""
        random_key = str(uuid.uuid4())
        self._redis.set(random_key, data)
        return random_key

    def get(self, key: str, fn: Optional[Callable] = None):
        """This method takes a key string argument
            and an optional Callable argument named fn"""
        value = self._redis.get(key)

        if not value:
            return None

        if fn:
            return fn(value)
        else:
            return value

    def get_str(self, key: str):
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str):
        return self.get(key, fn=int)
