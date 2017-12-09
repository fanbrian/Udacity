#NEW CLEANING PART - POSTAL CODE AND STREET NAMES
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 15:46:00 2017

@author: bfan
"""

###Prep for SQL###

import csv
import codecs
import pprint
import re
import xml.etree.cElementTree as ET

import cerberus

import schema

OSM_PATH = "/Users/bfan/Desktop/Udacity Course Materials/seattle_osm"

NODES_PATH = "nodes.csv"
NODE_TAGS_PATH = "nodes_tags.csv"
WAYS_PATH = "ways.csv"
WAY_NODES_PATH = "ways_nodes.csv"
WAY_TAGS_PATH = "ways_tags.csv"

LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

SCHEMA = schema = {
    'node': {
        'type': 'dict',
        'schema': {
            'id': {'required': True, 'type': 'integer', 'coerce': int},
            'lat': {'required': True, 'type': 'float', 'coerce': float},
            'lon': {'required': True, 'type': 'float', 'coerce': float},
            'user': {'required': True, 'type': 'string'},
            'uid': {'required': True, 'type': 'integer', 'coerce': int},
            'version': {'required': True, 'type': 'string'},
            'changeset': {'required': True, 'type': 'integer', 'coerce': int},
            'timestamp': {'required': True, 'type': 'string'}
        }
    },
    'node_tags': {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': {
                'id': {'required': True, 'type': 'integer', 'coerce': int},
                'key': {'required': True, 'type': 'string'},
                'value': {'required': True, 'type': 'string'},
                'type': {'required': True, 'type': 'string'}
            }
        }
    },
    'way': {
        'type': 'dict',
        'schema': {
            'id': {'required': True, 'type': 'integer', 'coerce': int},
            'user': {'required': True, 'type': 'string'},
            'uid': {'required': True, 'type': 'integer', 'coerce': int},
            'version': {'required': True, 'type': 'string'},
            'changeset': {'required': True, 'type': 'integer', 'coerce': int},
            'timestamp': {'required': True, 'type': 'string'}
        }
    },
    'way_nodes': {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': {
                'id': {'required': True, 'type': 'integer', 'coerce': int},
                'node_id': {'required': True, 'type': 'integer', 'coerce': int},
                'position': {'required': True, 'type': 'integer', 'coerce': int}
            }
        }
    },
    'way_tags': {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': {
                'id': {'required': True, 'type': 'integer', 'coerce': int},
                'key': {'required': True, 'type': 'string'},
                'value': {'required': True, 'type': 'string'},
                'type': {'required': True, 'type': 'string'}
            }
        }
    }
}

# Make sure the fields order in the csvs matches the column order in the sql table schema
NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)


expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons", "Lane", 'Circle', 'East', "North", 'West', "South", 
            "Northwest", "Northeast", 'Way', "Esplanade", "Terrace"]

mapping = { "St": "Street",
           "St ":"Street",
            "St.": "Street",
            "Ave": "Avenue",
            "Rd.":"Road",
           "NW":"Northwest",
           "NE":"Northeast",
           "n":""
            }
def replace(name, mapping):
    elements = name.split()
    for i in range(len(elements)):
        if elements[i] in mapping:
            elements[i] = mapping[elements[i]]
            name = " ".join(elements)
        else:
            pass
    return name

def shape_element(element, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS,
                  problem_chars=PROBLEMCHARS, default_tag_type='regular'):
    """Clean and shape node or way XML element to Python dict"""

    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    tags = [] 
    

                    
    if element.tag == 'node':
        for attr in node_attr_fields:
            node_attribs[attr] = element.get(attr)
        for tag_entry in element.iter('tag'):
            tag = {}
            tag['id'] = element.attrib['id']
            #conditions for tag type
            problem = problem_chars.search(tag_entry.attrib['k'])
            if problem:
                continue
            else:
                key = LOWER_COLON.search(tag_entry.attrib['k'])
                if key:
                    tag_type = tag_entry.attrib['k'].split(':',1)[0]
                    tag_field = tag_entry.attrib['k'].split(':',1)[1]
                    tag['type'] = tag_type
                    tag['key'] = tag_field
                    #fixing postal codes
                    if tag_entry.attrib['k'] == 'addr:postcode':
                        tag['value'] = tag_entry.attrib['v'][0:6]
                    #replacing street names
                    elif tag_entry.attrib['k'] =='addr:street':
                        tag['value'] = replace(tag_entry.attrib['v'], mapping)
                    else:
                        tag['value']= tag_entry.attrib['v']
                else:
                    tag['type'] = default_tag_type
                    tag['key']= tag_entry.attrib['k']
                    if tag_entry.attrib['k'] == 'addr:postcode':
                        tag['value'] = tag_entry.attrib['v'][0:6]
                    elif tag_entry.attrib['k'] =='addr:street':
                        tag['value'] = replace(tag_entry.attrib['v'], mapping)
                    else:
                        tag['value']= tag_entry.attrib['v']
                    tag['value']= tag_entry.attrib['v']
            tags.append(tag)
        return {'node': node_attribs, 'node_tags': tags}
        
    elif element.tag == 'way':
        for attr in way_attr_fields:
            way_attribs[attr] = element.get(attr)
        for tag_entry in element.iter('tag'):
            tag = {}
            tag['id'] = element.attrib['id']
            #type conditions
            problem = problem_chars.search(tag_entry.attrib['k'])
            if problem:
                continue
            else:
                key = LOWER_COLON.search(tag_entry.attrib['k'])
                if key:
                    tag['type'] = tag_entry.attrib['k'].split(':',1)[0]
                    tag['key'] = tag_entry.attrib['k'].split(':',1)[1]
                    if tag_entry.attrib['k'] == 'addr:postcode':
                        tag['value'] = tag_entry.attrib['v'][0:6]
                    elif tag_entry.attrib['k'] =='addr:street':
                        tag['value'] = replace(tag_entry.attrib['v'], mapping)
                    else:
                        tag['value'] = tag_entry.attrib['v']                   
                else:
                    tag['type'] = default_tag_type
                    tag['key']= tag_entry.attrib['k']
                    if tag_entry.attrib['k'] == 'addr:postcode':
                        tag['value'] = tag_entry.attrib['v'][0:6]
                    elif tag_entry.attrib['k'] =='addr:street':
                        tag['value'] = replace(tag_entry.attrib['v'], mapping)
                    else:
                        tag['value']= tag_entry.attrib['v']
                    tag['value'] = tag_entry.attrib['v'] 
            tags.append(tag)
        count = 0
        for nd in element.iter('nd'):
            nd_entry = {}
            nd_entry['id'] = element.attrib['id']
            nd_entry['node_id'] = nd.attrib['ref']
            nd_entry['position'] = count
            count += 1
            way_nodes.append(nd_entry)

        return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}
