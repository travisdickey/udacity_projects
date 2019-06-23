#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.cElementTree as ET
import pprint
'''
takes OSM file then finds tags and counts number of occurrences;
returns a dictionary with tag names as keys and counts of tags as values
'''
def count_tags(filename):
        tags = {}
        for event, elem in ET.iterparse(filename):
            if elem.tag not in tags.keys():
                tags[elem.tag] = 1
            else:
                tags[elem.tag] += 1
        return tags


my_file = 'sample.OSM'
count_tags(my_file)

def test():

    tags = count_tags('sample.osm')
    pprint.pprint(tags)
    '''
    assert tags == {'bounds': 1,
                     'member': 3,
                     'nd': 4,
                     'node': 20,
                     'osm': 1,
                     'relation': 1,
                     'tag': 7,
                     'way': 1}
    '''

if __name__ == "__main__":
    test()
