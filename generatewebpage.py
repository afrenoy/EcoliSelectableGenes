#!/usr/bin/env python3

import markdown
def translate(string):
    return markdown.markdown(string).replace('<p>','').replace('</p>','')

import sys
if len(sys.argv)<4:
    print("3 arguments expected: 1st table, 2nd table, and references")
    exit(-1)


# Table 1
import io
def printtable1(ftab1):
    output=io.StringIO()
    f=open(ftab1,'r')
    tab=[translate(t) for t in f.readlines()]
    f.close()

    print('<h1><a name="tab1"></a>%s</h1>'%tab[0],file=output)
    print('<table>',file=output)
    for line in tab[1:]:
        print('<tr>',file=output)
        tokens=line.split(';')
        for t in tokens:
            print('<td>',file=output)
            print(t,file=output)
            print('</td>',file=output)
        print('</tr>',file=output)
    print('</table>',file=output)
    return(output.getvalue())

# Table 2
def printtable2(ftab2):
    output=io.StringIO()
    g=open(ftab2,'r')
    tab=g.readlines()
    g.close()

    print('<h1><a name="tab2"></a>%s</h1>'%tab[0],file=output)
    print('<table>',file=output)

    tokens=tab[1].split(';')
    print('<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>'%(tokens[0],tokens[1],tokens[2],tokens[3],tokens[4]),end='',file=output)

    for line in tab[2:]:
        if line.count(';')==3:
            #print(line)
            line=line.rstrip('\n')+'; \n'
            #print(line)
        print('<tr>',file=output)
        tokens=line.split(';')
        print('<td>%s</td><td>%s</td><td>%s</td>'%(tokens[0],tokens[1],tokens[2]),end='',file=output)
        allrefs=[]
        for ur in tokens[3].split(','):
            ur=ur.strip(' ')
            if '-' in ur:
                dual=ur.split('-')
                for i in range(int(dual[0]),int(dual[1])+1):
                    allrefs.append(str(i))
            else:
                allrefs.append(ur)
        print('<td>',end='',file=output)
        for ref in allrefs:
            if '%0A' in ref:
                print('Hem hem')
                exit(0)
            print('<a href="#ref%s">%s</a> '%(ref,ref),end='',file=output)
        print('</td><td>%s</td>'%tokens[4],end='',file=output)
        print('</tr>',file=output)
    print('</table>',file=output)
    return(output.getvalue())

# References
def printtableref(fref):
    output=io.StringIO()
    import refs
    h=open(fref,'r')
    refs=h.readlines()
    h.close()

    print('<h1><a name="ref"></a>References</h1>',file=output)
    print('<table>',file=output)
    references=dict()
    for ref in refs:
        tokens=ref.split(';')
        if ' p. ' in tokens[3]:
            tokens[3]=tokens[3].split(' p. ')[0].rstrip(',')+'.'
        tokens[3]=tokens[3].lstrip(' .')
        references[tokens[0]]=(tokens[1],int(tokens[2]),tokens[3])
        strquery=tokens[3].rstrip(' .').replace('<i>','').replace('</i>','')
        gscholar='https://scholar.google.ch/scholar?hl=en&q=%s'%strquery
        print('<tr><td><a name="ref%s"></a>%s</td><td>%s <i>%s</i>. %s</td><td><a href="%s">google scholar</a></td></tr>'%(tokens[0],tokens[0],tokens[1],tokens[2],tokens[3],gscholar),file=output)
        #refs.getsource(gscholar,tokens[0]) # Try to download the pdf / find doi / bibtex record / ...
    print('</table>',file=output)
    return(output.getvalue())

output=io.StringIO()
print('<!DOCTYPE html>\n<html>\n<head>\n\t<meta charset=\"UTF-8\">\n\t<title>Larossa</title>\n\t<link rel="stylesheet" href="style.css">\n</head>\n<body>\n',file=output)
print('<div id="menu"><nav><ul><li><a href="#about">About</a></li><li><a href="#tab1">Selections giving rise to mutants</a></li><li><a href="#tab2">Genes for which selections exist</a></li><li><a href="#ref">References</a></li></ul></nav></div>\n<div id="main">',file=output)
print('<h1 id="about">About this document</h1><p>This is data from chapter 139 of E coli and Salmonella, reproduced without permission. </br>The pdf has been converted to html and parsed using a few bash and python scripts availabe on <a href="http://github.com/frenoy/ecosal">github</a>.</p><p>The raw data can be downloaded as csv files:</p><ul><li><a href="table1-4.csv">Table 1</a>: Selections giving rise to mutants</li><li><a href="table2-4.csv">Table 2</a>: Genes for which selections exist</li><li><a href="references-4.csv">Table 3</a>: References</li></ul>',file=output)
print(printtable1(sys.argv[1]),file=output)
print(printtable2(sys.argv[2]),file=output)
print(printtableref(sys.argv[3]),file=output)
print('</div></body>\n</html>',file=output)
print(output.getvalue())

