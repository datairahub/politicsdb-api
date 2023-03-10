# -*- coding: utf-8 -*-
from collections import OrderedDict
from django.core.cache import cache


def compose_cache_name(base: str, params: dict):
    """
    Compose cache name based on dict params
    - input: base="LOREM", params={"ipsum": "dolor"}
    - output: LOREM_IPSUM_DOLOR
    """
    for key, val in OrderedDict(sorted(params.items())).items():
        base += f"_{key.upper()}_{val.upper()}"
    return base


def cached_stats(base: str):
    """
    Custom decorator to cache stats functions
    - Functions require pk, and params arguments
    """

    def decorator(func):
        def wrapper(pk: str, params: dict, *args, **kwargs):
            cache_name = compose_cache_name(f"{base}_{pk}", params)
            if cache.get(cache_name):
                return cache.get(cache_name)
            result = func(pk, params, *args, **kwargs)
            cache.set(cache_name, result, 60 * 60 * 24 * 30)
            return result

        return wrapper

    return decorator
