#!/usr/bin/env python3
"""Defining a function named schools_by_topic"""


def schools_by_topic(mongo_collection, topic):
    """This is a function that returns the list
        of school having a specific topic"""
    wanted_schools = []
    for doc in mongo_collection.find():
        for the_topic in doc['topics']:
            if the_topic == topic:
                wanted_schools.append(doc)

    return wanted_schools
