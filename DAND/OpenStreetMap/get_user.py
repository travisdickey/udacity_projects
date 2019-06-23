#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
"""
Finds out how many unique users have contributed to the map in this area
"""
# takes iterparsed element and returns "uid" or None if key doesn't exist
def get_user(element):
     # see if the key exists:
    if element.get('uid'):
        uid = element.attrib["uid"]
        return uid
    else:
        # return None if the key doesn't exist
        return None

# takes the file and return a set of unique user IDs ("uid")
def process_map(filename):
    users = set()
    for _, element in ET.iterparse(filename):
        if get_user(element):
            users.add(get_user(element))
        pass

    return users


def test():

    users = process_map('sample.osm')
    pprint.pprint(users)
    #assert len(users) == 6

if __name__ == "__main__":
    test()
