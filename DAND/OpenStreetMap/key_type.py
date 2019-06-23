#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
'''
Checks 'k' value of each tag for potential problems and
for certain patterns, including "addr:street", which will
be used later when preparing files for SQL schema
'''
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

# takes an element from iterparsed file and returns dictionary
# with count of keys that meet defined patterns
def key_type(element, keys):
    if element.tag == "tag":
        for tag in element.iter("tag"):
            l = lower.search(tag.attrib['k'])
            l_c = lower_colon.search(tag.attrib['k'])
            pc = problemchars.search(tag.attrib['k'])
            if l:
                keys["lower"] += 1
            elif l_c:
                keys["lower_colon"] += 1
            elif pc:
                keys["problemchars"] += 1
            else:
                keys["other"] += 1
            pass

    return keys

# takes file and returns dictionary (keys) with count of defined patterns
def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    return keys

def test():
    # You can use another testfile 'map.osm' to look at your solution
    # Note that the assertion below will be incorrect then.
    # Note as well that the test function here is only used in the Test Run;
    # when you submit, your code will be checked against a different dataset.
    keys = process_map('sample.osm')
    pprint.pprint(keys)
    #assert keys == {'lower': 5, 'lower_colon': 0, 'other': 1, 'problemchars': 1}


if __name__ == "__main__":
    test()
