#!/usr/bin/env python3
"""Defining a Class Cache"""
import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Increments a counter in Redis each time
    the method is called"""
    @wraps(method)
    def wrapper(self, *args, **kwds):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwds)
    return wrapper


def call_history(method: Callable) -> Callable:
    """Records the input parameters and output of
    the method in Redis in a List"""
    @wraps(method)
    def wrapper(self, *args, **kwds):
        key = method.__qualname__
        inputs_list_key = key + ":inputs"
        output_list_key = key + ":outputs"
        self._redis.rpush(inputs_list_key, str(args))
        key_arg = method(self, *args, **kwds)
        self._redis.rpush(output_list_key, key_arg)
        return key_arg
    return wrapper


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


class Cache:
    """Class Cache"""
    def __init__(self) -> None:
        """Initializing a new Cache"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """takes a data argument, sets it to a random key and
        returns the key"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None):
        """Reads from Redis and recovers original type"""
        value = self._redis.get(key)
        if not value:
            return None
        if fn:
            return fn(value)
        else:
            return value

    def get_str(self, key: str) -> Optional[str]:
        """parametrize get method with string fn"""
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Optional[int]:
        """parametrize get method with integer fn"""
        return self.get(key, fn=int)

    def replay(self, method: Callable):
        """displays the history of calls of a particular function"""
        # Get the qualified name of the method
        key = method.__qualname_
        # Construct the Redis keys for inputs and outputs
        inputs_list_key = key + ":inputs"
        output_list_key = key + ":outputs"
        inputs = self._redis.lrange(inputs_list_key, 0, -1)
        outputs = self._redis.lrange(output_list_key, 0, -1)
        print(f"{key} was called {len(inputs)} times:")
        for input_args, output_key in zip(inputs, outputs):
            # Print the input arguments and the corresponding output key
            print(f"{key}(*{input_args.decode()}) -> {output_key.decode()}")