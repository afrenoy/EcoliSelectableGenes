#!/usr/bin/env python3

import sys

if len(sys.argv)<2:
    print('Argument expected')
    exit(-1)

f=open(sys.argv[1],'r')
tab=f.readlines()
f.close()

ts='unknown'
print(tab[0].rstrip('\n'))
print(tab[1].rstrip('\n'))
for line in tab[2:]:
    if ';' in line:
        t1=line.split(';')[0]
        t2=line.split(';')[1]
        print('%s;%s;%s'%(ts,t1,t2.rstrip('\n')))
    else:
        ts=line.rstrip('\n')

#print(tab)

