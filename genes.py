#!/usr/bin/env python3

import re

def getallgenes():
    knowngenes=dict()
    table=open('ecocyc.csv','r').readlines()
    for line in table[1:]:
        tokens=line.rstrip('\n').split(',')
        searchgenename=re.search('[a-z]{3}[A-Z]?',tokens[1])
        if searchgenename:
            genename=searchgenename.group(0)
            knowngenes[genename]=(tokens[0],tokens[2]) # Store ecocyc ID and b name
    return knowngenes

