#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 15:41:40 2017

@author: bfan
"""
###Tag Types###
import xml.etree.cElementTree as ET
import pprint
import re


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