#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file parses the XML OSM file and writes the records to CSV files according to the
following format. The "node" field holds a dictionary with the node attributes: id, user,
uid, version, lat, lon, timestamp, changeset. All other attributes are ignored.

The "node_tags" field holds a list of dictionaries, one per secondary tag. Each dictionary has
the tag attributes: id, key, value, type. Additionally, if the tag "k" value contains problematic
characters, the tag is ignored; if the tag "k" value contains a ":" the characters before the ":"
are set as the tag type and characters after the ":" are set as the tag key; if there are additional
":" in the "k" value they are ignored and kept as part of the tag key. If a node has no secondary
tags, then the "node_tags" field contains an empty list.

### If the element top level tag is "way": The dictionary has the format
{"way": ..., "way_tags": ..., "way_nodes": ...}. The "way" field holds a dictionary of
 the following top level way attributes: id, user, uid, version, timestamp, changeset.
 All other attributes are ignored. The "way_tags" field is processed exactly like "node_tags".
The "way_nodes" field holds a list of dictionaries, one for each nd child tag.
Each dictionary has the fields: id, node_id, position.
"""

import csv
import codecs
import pprint
import re
import xml.etree.cElementTree as ET
from collections import OrderedDict
import cerberus
from update_street import *
import schema

OSM_PATH = "savannah_hiltonhead.osm"

NODES_PATH = "nodes.csv"
NODE_TAGS_PATH = "nodes_tags.csv"
WAYS_PATH = "ways.csv"
WAY_NODES_PATH = "ways_nodes.csv"
WAY_TAGS_PATH = "ways_tags.csv"

LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

SCHEMA = schema.schema

NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']

def update_tags(element, problem_chars, TAGS_FIELDS, d, tags):
    '''
    change abbreviated street names to full names and fix zip codes;
    update labels for 'addr', 'regular', and 'tiger' type; return list
    of ordered dictionaries containing updated tags
    '''

    for tag in element.iter("tag"):
        a = OrderedDict(key= TAGS_FIELDS)
        a['id'] = d['id']
        pc = problem_chars.search(tag.attrib['k'])
        lc = LOWER_COLON.search(tag.attrib['k'])
        if pc:
            continue
        elif lc:
            string = tag.attrib['k']
            pos = string.find(':')
            a['key'], a['type'] = string[(pos + 1):], string[:pos]
        else:
            a['key'], a['type'] = tag.attrib['k'], 'regular'
        if a['key'] == 'street':
            a['value'] = update_name(tag.attrib['v'], mapping)
        elif a['key'] == 'postcode' or a['key'].find('zip') != -1:
            z_re = re.compile(r'\d{5}')
            z = tag.attrib['v']
            zipcode = z_re.findall(z)[0]
            a['value'] = zipcode #correct zip codes separated by semi-colon
        else:
            a['value'] = tag.attrib['v']
        tags.append(a)

def shape_element(element, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS,
                  problem_chars=PROBLEMCHARS, default_tag_type='regular'):
    """Clean and shape node or way XML element to Python dict"""

    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    tags = []  # Handle secondary tags the same way for both node and way elements
    if element.tag == 'node':
        for field in node_attr_fields:
            node_attribs[field] = element.get(field)
        update_tags(element, problem_chars, NODE_TAGS_FIELDS, node_attribs, tags)
        return {'node': node_attribs, 'node_tags': tags}
    elif element.tag == 'way':
        for field in way_attr_fields:
            way_attribs[field] = element.get(field)
        update_tags(element, problem_chars, WAY_TAGS_FIELDS, way_attribs, tags)
        position = 0
        for tag in element.iter('nd'):
            nd_dict = OrderedDict()
            nd_dict['id'] = way_attribs['id']
            nd_dict['node_id'] = tag.attrib['ref']
            nd_dict['position'] = position
            position += 1
            way_nodes.append(nd_dict)
        return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}



# ================================================== #
#               Helper Functions                     #
# ================================================== #
def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag"""

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


def validate_element(element, validator, schema=SCHEMA):
    """Raise ValidationError if element does not match schema"""
    if validator.validate(element, schema) is not True:
        field, errors = next(validator.errors.iteritems())
        message_string = "\nElement of type '{0}' has the following errors:\n{1}"
        error_string = pprint.pformat(errors)

        raise Exception(message_string.format(field, error_string))


class UnicodeDictWriter(csv.DictWriter, object):
    """Extend csv.DictWriter to handle Unicode input"""

    def writerow(self, row):
        super(UnicodeDictWriter, self).writerow({
            k: (v.encode('utf-8') if isinstance(v, unicode) else v) for k, v in row.iteritems()
        })

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


# ================================================== #
#               Main Function                        #
# ================================================== #
def process_map(file_in, validate):
    """Iteratively process each XML element and write to csv(s)"""

    with codecs.open(NODES_PATH, 'w') as nodes_file, \
         codecs.open(NODE_TAGS_PATH, 'w') as nodes_tags_file, \
         codecs.open(WAYS_PATH, 'w') as ways_file, \
         codecs.open(WAY_NODES_PATH, 'w') as way_nodes_file, \
         codecs.open(WAY_TAGS_PATH, 'w') as way_tags_file:

        nodes_writer = UnicodeDictWriter(nodes_file, NODE_FIELDS)
        node_tags_writer = UnicodeDictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
        ways_writer = UnicodeDictWriter(ways_file, WAY_FIELDS)
        way_nodes_writer = UnicodeDictWriter(way_nodes_file, WAY_NODES_FIELDS)
        way_tags_writer = UnicodeDictWriter(way_tags_file, WAY_TAGS_FIELDS)

        nodes_writer.writeheader()
        node_tags_writer.writeheader()
        ways_writer.writeheader()
        way_nodes_writer.writeheader()
        way_tags_writer.writeheader()

        validator = cerberus.Validator()

        for element in get_element(file_in, tags=('node', 'way')):
            el = shape_element(element)
            #print el
            if el:
                if validate is True:
                    validate_element(el, validator)

                if element.tag == 'node':
                    nodes_writer.writerow(el['node'])
                    node_tags_writer.writerows(el['node_tags'])
                elif element.tag == 'way':
                    ways_writer.writerow(el['way'])
                    way_nodes_writer.writerows(el['way_nodes'])
                    way_tags_writer.writerows(el['way_tags'])


if __name__ == '__main__':
    # Note: Validation is ~ 10X slower. For the project consider using a small
    # sample of the map when validating.
    process_map(OSM_PATH, validate=False)
