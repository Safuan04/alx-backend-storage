#!/usr/bin/env python3
"""Creatin a Cashe class"""
import redis
from typing import Union, Callable, Optional
import uuid
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Decorator to count the number of calls to a method."""
    @wraps(method)
    def function_wrapper(self, *args, **kwargs):
        """Wrapper function to increment the call
            count before calling the method."""
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return function_wrapper


def call_history(method: Callable) -> Callable:
    """Decorator to record the history of calls to a method."""
    @wraps(method)
    def function_wrapper(self, *args):
        """Wrapper function to record inputs
            and outputs before calling the method."""
        key = method.__qualname__
        outputs_key = key + ":outputs"
        inputs_key = key + ":inputs"
        self._redis.rpush(inputs_key, str(args))

        result = method(self, *args)
        self._redis.rpush(outputs_key, result)
        return result
    return function_wrapper


def replay(method: Callable):
    """displays the history of calls of a particular function"""
    key = method.__qualname__
    r = redis.Redis()
    inputs_list_key = key + ":inputs"
    output_list_key = key + ":outputs"
    inputs = r.lrange(inputs_list_key, 0, -1)
    outputs = r.lrange(output_list_key, 0, -1)
    print(f"{key} was called {len(inputs)} times:")
    for in_args, op_key in zip(inputs, outputs):
        print(f"{key}(*{in_args.decode('utf-8')}) -> {op_key.decode('utf-8')}")


class Cache():
    def __init__(self) -> None:
        """Storing an instance of the redis client"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
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
        """Retrieve a string from the cache."""
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str):
        """Retrieve an integer from the cache."""
        return self.get(key, fn=int)
