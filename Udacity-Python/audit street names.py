#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 15:42:26 2017

@author: bfan
"""

###Audit Street Names###

import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "sea_sample.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)


expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons", "Lane", 'Circle', 'East', "North", 'West', "South", 
            "Northwest", "Northeast", 'Way', "Esplanade", "Terrace"]

# UPDATE THIS VARIABLE
mapping = { "St": "Street",
           "St ":"Street",
            "St.": "Street",
            "Ave": "Avenue",
            "Rd.":"Road",
           "NW":"Northwest",
           "NE":"Northeast",
           "n":""
            }



def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            if street_type in mapping:
                new_type = update_name(street_type,mapping)
                street_types[new_type].add(new_type)
            else:
                street_types[street_type].add(street_name)


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


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


def update_name(name, mapping):
    m = street_type_re.search(name)
    print (name)
    if m:
        street_type = m.group()
        if name not in expected:
            name = re.sub(street_type_re, mapping[street_type] , name)
    return name


lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

def key_type(element, keys):
    if element.tag == "tag":
        value = element.attrib['k']
        if re.search(lower, value):
            keys['lower'] +=1 
        elif re.search(lower_colon, value):
            keys['lower_colon'] += 1
        elif re.search(problemchars, value):
            keys['problemchars'] += 1
        else:
            keys['other'] += 1
    print(keys)
    print('\n')# YOUR CODE HERE
    return keys

def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)
    return keys

def count_tags(filename):
        tags = {}
        for event, element in ET.iterparse(filename):
            if element.tag in tags:
                tags[element.tag] +=1
            else:
                tags[element.tag] = 1
        print(tags)
