#!/usr/bin/env python3
"""
Topic: NoSQL
Name: Khotso Selading
Date: 22-01-2024
"""
import pymongo


def list_all(mongo_collection):
    """
    list all collections
    """
    if not mongo_collection:
        return []
    return list(mongo_collection.find())
