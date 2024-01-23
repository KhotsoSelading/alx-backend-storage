#!/usr/bin/env python3
"""
Topic: NoSQL
Name: Khotso Selading
Date: 22-01-2024
"""
import pymongo


def schools_by_topic(mongo_collection, topic):
    """
    a Python function that returns the list of school having a specific topic
    """
    return mongo_collection.find({"topics": topic})
