#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
- audits the OSMFILE and changes the variable 'mapping' to reflect the changes needed to fix
    the unexpected street types to the appropriate ones in the expected list.
    !!!You have to add mappings only for the actual problems you find in this OSMFILE,
    not a generalized solution, since that may and will depend on the particular area you are auditing.!!!
- fixes the street names.

    We have provided a simple test so that you see what exactly is expected
"""
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "savannah_hiltonhead.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)


expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road",
            "Trail", "Parkway", "Commons", "Walk", "B"]

# UPDATE THIS VARIABLE
mapping = { "St": "Street",
            "St.": "Street",
            "Ave": "Avenue",
            "Rd.": "Road",
            "Ln": "Lane",
            "Cir": "Circle",
            "Dr": "Drive",
            "Blvd": "Boulevard",
            "Ct": "Court",
            "Pl": "Place",
            "Sq": "Square",
            "Tr": "Trail",
            "Pkwy": "Parkway",
            "Cm": "Commons"
            }

# takes street types and street names and checks whether street name
# is one that's expected; if name is not expected, the name is added
# to street types dictionary
def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)

# takes a tag and returns value if it is a street name

def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


# takes OSM file and returns default dictionary set of street types (e.g., AVE, ST, CT)
def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    return street_types

# takes a string with street name as an argument and returns corrected name
def update_name(name, mapping):
    match = street_type_re.search(name)
    abbrev = match.group()
    l = len(abbrev)
    name = name[:-l] + mapping[abbrev]
    return name

def test():
    st_types = audit(OSMFILE)
    #assert len(st_types) == 5
    pprint.pprint(dict(st_types))

    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_name(name, mapping)
            return better_name
            '''
            print name, "=>", better_name
            if name == "West Lexington St.":
                assert better_name == "West Lexington Street"
            if name == "Baldwin Rd.":
                assert better_name == "Baldwin Road"
            '''


if __name__ == '__main__':
    test()
