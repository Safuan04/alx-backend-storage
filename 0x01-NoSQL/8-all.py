#!/usr/bin/env python3
"""
- Defining a function named list_all
"""


def list_all(mongo_collection):
    """This is a function that lists all documents in a collection"""
    docs = []
    for doc in mongo_collection.find():
        docs.append(doc)

    return docs
