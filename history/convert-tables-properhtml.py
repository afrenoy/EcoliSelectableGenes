#!/usr/bin/env python3
import markdown

f=open('table1.csv','r')
a=f.readlines()
f.close()
f=open('table1.csv','w')
print(a[0].rstrip('\n'),file=f)
for l in a[1:]:
    tokens=l.rstrip('\n').split(';')
    print('%s;%s;%s'%(tokens[0],markdown.markdown(tokens[1]).replace('<p>','').replace('</p>',''),tokens[2].replace('*','')),file=f)
f.close()

f=open('table2.csv','r')
b=f.readlines()
f.close()
f=open('table2.csv','w')
print(b[0].rstrip('\n'),file=f)
for l in b[1:]:
    if l.count(';')==3: # For many entries, no value is provided for the selected 'alteration'
        l=l.rstrip('\n')+'; \n'
    tokens=l.rstrip('\n').split(';')
    print('%s;%s;%s;%s;%s'%(tokens[0].replace('<i>','').replace('</i>',''),tokens[1],tokens[2].replace('<i>','<em>').replace('</i>','</em>'),tokens[3],tokens[4]),file=f)
f.close()

