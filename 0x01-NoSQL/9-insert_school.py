#!/usr/bin/env python3
"""Defining a function named insert_school"""


def insert_school(mongo_collection, **kwargs):
    """This is a func that inserts a new document
        in a collection based on kwargs"""
    last_id = mongo_collection.insert_one({**kwargs}).inserted_id
    return last_id
