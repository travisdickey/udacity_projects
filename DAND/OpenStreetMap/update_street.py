#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' fixes the street names '''

import re

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road",
            "Trail", "Parkway", "Commons"]

# Mapping for corrected street names
mapping = { "St": "Street",
            "St.": "Street",
            "Ave": "Avenue",
            "Rd.": "Road",
            "Rd": "Road",
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


# takes a string with street name as an argument and returns corrected name
def update_name(name, mapping):
    match = street_type_re.search(name)
    if match:
        street_type = match.group()
        if street_type not in expected:
            if street_type in mapping.keys():
                abbrev = match.group()
                l = len(abbrev)
                name = name[:-l] + mapping[abbrev]
    return name
