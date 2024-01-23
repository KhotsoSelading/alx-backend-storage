#!/usr/bin/env python3
"""
Topic: NoSQL
Name: Khotso Selading
Date: 22-01-2024
"""
import pymongo


def insert_school(mongo_collection, **kwargs):
    """
    insert into school
    """
    return mongo_collection.insert_one(kwargs).inserted_id
