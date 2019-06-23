#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.cElementTree as ET
from collections import defaultdict
import pprint
import re

# indicate file to be read
osmfile = "sample.osm"

# create the dict to put zipcodes into
def add_to_dict(data_dict, item):
    data_dict[item] += 1

# find the zipcodes
def get_postcode(element):
    for tag in element:
        if (tag.attrib['k'] == "addr:postcode") or (tag.attrib['k'].find('zip') != -1):
            postcode = tag.attrib['v']
            return postcode

# update zipcodes
def update_postal(postcode):
    z_re = re.compile(r'\d{5}')
    z = postcode
    postcode = z_re.findall(z)[0]
    return postcode


# aput the list of zipcodes into dict
def audit(osmfile):
    osm_file = open(osmfile, "r")
    data_dict = defaultdict(int)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if get_postcode(elem.iter("tag")):
                    postcode = get_postcode(elem.iter("tag"))
                    postcode = update_postal(postcode)
                    add_to_dict(data_dict, postcode)
    return data_dict


# test the zipcode audit and dict creation
def test():
    cleanzips = audit(osmfile)
    pprint.pprint(dict(cleanzips))



if __name__ == '__main__':
    test()
