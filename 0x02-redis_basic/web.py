#!/usr/bin/env python3
"""
Topic: Redis
Name: Khotso Selading
Date: 22-01-2024
"""

import redis
import requests
from typing import Callable
from functools import wraps

# Use a different name for the Redis instance to avoid name conflicts
redis_instance = redis.Redis()


def wrap_requests(fn: Callable) -> Callable:
    """ Decoration wrapper """
    @wraps(fn)
    def wrapper(url):
        """ The wrapper for decorator """
        try:
            # Increment access counter
            redis_instance.incr(f"count:{url}")

            # Check if response is cached
            cached_response = redis_instance.get(f"cached:{url}")
            if cached_response:
                return cached_response.decode('utf-8')

            # If not cached, Make the request 
            result = fn(url)

            # Cache the response with an expiration time of 10 seconds
            redis_instance.setex(f"cached:{url}", 10, result)

            return result
        except Exception as e:
            # Handle exceptions, log, or raise as appropriate
            print(f"An error occurred: {e}")
            return f"Error: {e}"

    return wrapper


@wrap_requests
def get_page(url: str) -> str:
    """ Get page content """
    response = requests.get(url)
    return response.text
