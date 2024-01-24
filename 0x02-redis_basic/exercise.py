#!/usr/bin/env python3
"""
Topic: Redis
Name: Khotso Selading
Date: 22-01-2024
"""
import sys
from functools import wraps
from typing import Union, Optional, Callable
from uuid import uuid4

import redis

UnionOfTypes = Union[str, bytes, int, float]


def count_calls(method: Callable) -> Callable:
    """
    This decorator is used to count the number of times a method is called.
    It increments a counter in Redis for each method call.
    """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrap
        :param self:
        :param args:
        :param kwargs:
        :return:
        """
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """
    This decorator is used to store the input parameters and output of a method
    in two separate lists in Redis.
    """
    key = method.__qualname__
    i = "".join([key, ":inputs"])
    o = "".join([key, ":outputs"])

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ Wrapp """
        self._redis.rpush(i, str(args))
        res = method(self, *args, **kwargs)
        self._redis.rpush(o, str(res))
        return res

    return wrapper


class Cache:
    """
    Redis Cache class
    """

    def __init__(self):
        """
        Constructor initializes a Redis connection and flushes the database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: UnionOfTypes) -> str:
        """
        Method generates a random key (using uuid4),stores the input data in
        Redis using the generated key, and returns the key.
        """
        key = str(uuid4())
        if isinstance(data, (int, float)):
            data = str(data)
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) \
            -> UnionOfTypes:
        """
        Method retrieves data from Redis based on a given key. If a conversion
        function (fn) is provided, it is used to convert the data back to the
        desired format.
        """
        if fn:
            return fn(self._redis.get(key))
        data = self._redis.get(key)
        return data

    def get_int(self: bytes) -> int:
        """Helper method to convert bytes to an integer."""
        return int.from_bytes(self, sys.byteorder)

    def get_str(self: bytes) -> str:
        """Helper method to convert bytes to a string."""
        return self.decode("utf-8")
