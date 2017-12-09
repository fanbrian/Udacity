#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 15:41:23 2017

@author: bfan
"""

###Iterative Parsing###

import xml.etree.cElementTree as ET
import pprint

def count_tags(filename):
        tags = {}
        for event, element in ET.iterparse(filename):
            if element.tag in tags:
                tags[element.tag] +=1
            else:
                tags[element.tag] = 1
        print(tags)