#!/usr/bin/env python3

import re
import io
import os
import refparser


def getallgenes(ecocycfile):
    """ From a gene name, get a string with a link to ecocyc if relevant
    """
    knowngenes = dict()
    table = open(ecocycfile, 'r').readlines()
    for line in table[1:]:
        tokens = line.rstrip('\n').split(',')
        searchgenename = re.search('[a-z]{3}[A-Z]?', tokens[1])
        if searchgenename:
            genename = searchgenename.group(0)
            knowngenes[genename] = (tokens[0], tokens[2])  # Store ecocyc ID and b name
    return knowngenes


def formatgene(gene, allgenes):
    """ Transform a string containing a gene name into a link to EcoCyc
    """
    searchgenename = re.search('[a-z]{3}[A-Z]?', gene)
    if not searchgenename:
        return(gene)
    genename = searchgenename.group(0)
    if not genename in allgenes:
        return(gene)
    (eco, bname) = allgenes[genename]
    return('<a class="gene" href="http://ecocyc.org/gene?orgid=ECOLI&id=%s">%s</a>' % (eco, gene))


def printtable1(ftab1, allgenes):
    """ Print Table 1 in html format
    With links to ecocyc using the 'allgenes' dictionary
    """
    output = io.StringIO()
    f = open(ftab1, 'r')
    tab = f.readlines()
    f.close()

    print('<div id="table1"><table>', file=output)
    print('<caption><span class="anchor" id="table1-anchor"></span><h1>%s</h1></caption>' % tab[0], file=output)
    print('<col class="selection">\n<col class="gene">\n<col class="type">\n', file=output)

    tokens = tab[1].split(';')
    print('<tr><th>%s</th><th>%s</th><th>%s</th></tr>' % (tokens[1], tokens[2], tokens[0]), file=output)

    for line in tab[2:]:
        tokens = line.split(';')
        assert(len(tokens) == 3)
        print('<tr><td>%s</td><td>%s</td><td>%s</td></tr>' % (tokens[1], formatgene(tokens[2], allgenes), tokens[0]), file=output)
    print('</table></div>', file=output)
    return(output.getvalue())


def printtable2(ftab2, allgenes):
    """ Print Table 2 in html format
    With links to ecocyc using the 'allgenes' dictionary
    """
    output = io.StringIO()
    g = open(ftab2, 'r')
    tab = g.readlines()
    g.close()

    print('<div id="table2"><table>', file=output)
    print('<caption><span class="anchor" id="table2-anchor"></span><h1>%s</h1></caption>' % tab[0].rstrip('\n'), file=output)
    print('<col class="gene">\n<col class="organism">\n<col class="selection">\n<col class="references">\n<col class="alteration">', file=output)
    tokens = tab[1].rstrip('\n').split(';')
    print('<tr><th>%s</th><th>%s</th><th>%s</th><th>%s</th><th>%s</th></tr>' % (tokens[0], tokens[1], tokens[2], tokens[3], tokens[4]), file=output)

    for line in tab[2:]:
        print('<tr>', end='', file=output)
        tokens = line.rstrip('\n').split(';')
        print('<td>%s</td><td>%s</td><td>%s</td>' % (formatgene(tokens[0], allgenes), tokens[1], tokens[2]), end='', file=output)
        allrefs = []
        for ur in tokens[3].split(','):
            ur = ur.strip(' ')
            if '-' in ur:
                dual = ur.split('-')
                for i in range(int(dual[0]), int(dual[1])+1):
                    allrefs.append(str(i))
            else:
                allrefs.append(ur)
        print('<td>', end='', file=output)
        for ref in allrefs:
            if '%0A' in ref:
                print('Hem hem')
                exit(0)
            print('<a href="#ref%s">%s</a> ' % (ref, ref), end='', file=output)
        print('</td><td>%s</td>' % tokens[4], end='', file=output)
        print('</tr>', file=output)
    print('</table></div>', file=output)
    return(output.getvalue())


def printtableref(fref):
    """ Print reference table in html format
    With links to a google scholar text with the full title
    And to a pdf if available
    The pdf have been extracted from google scholar or sci-hub using functions in 'refparser'.py
    To run this parsing again for example in case bibliographic informations are corrected, the corresponding line must be uncommented
    """
    output = io.StringIO()
    h = open(fref, 'r')
    refs = h.readlines()
    h.close()

    print('<div id="references"><table>', file=output)
    print('<caption><span class="anchor" id="references-anchor"></span><h1>References</h1></caption>', file=output)
    print('<col class="refnumber">\n<col class="reftitle">\n<col class="reflink">\n<col class="refpdf">', file=output)
    print('<tr><th>%s</th><th>%s</th><th>%s</th><th>%s</th></tr>' % ("Nº", "title", "link", "pdf"), file=output)

    references = dict()
    for ref in refs:
        tokens = ref.split(';')
        if ' p. ' in tokens[3]:
            tokens[3] = tokens[3].split(' p. ')[0].rstrip(',')+'.'
        tokens[3] = tokens[3].lstrip(' .')
        references[tokens[0]] = (tokens[1], int(tokens[2]), tokens[3])
        strquery = tokens[3].rstrip(' .').replace('<i>', '').replace('</i>', '')
        gscholarquery = 'https://scholar.google.ch/scholar?hl=en&q=%s' % (strquery.replace(' ', '%20'))
        pdf = 'pdf/%s.pdf' % tokens[0]
        pdflink = ('<a href="%s">pdf</a>' % pdf if os.path.exists(pdf) else '')
        print('<tr><td>%s</td><td><a id="ref%s" class="anchor"></a>%s. <i>%s</i>. %s <span class="journal">%s</span></td><td><a href="%s">google scholar</a></td><td>%s</td></tr>' % (tokens[0], tokens[0], tokens[1], tokens[2], tokens[3], tokens[4].rstrip('\n'), gscholarquery, pdflink), file=output)
#       refparser.getsource(gscholarquery, tokens[0])  # If uncommented, parse google scholar and try to download the pdf from there or from sci-hub.
    print('</table></div>', file=output)
    return(output.getvalue())


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        print('Usage: ./generatewebpage.py\n\nCreate the webpage index.html from the input files table1.csv, table2.csv, references.csv, ecocyc.csv, about.html, contribute.html, and footer.html\n')
        exit()
    output = io.StringIO()  # The buffer in which we will write the html
    print('<!DOCTYPE html>\n<html lang="en">\n<head>\n\t<meta charset="UTF-8">\n\t<meta name="description" content="E. coli and Salmonella: tables from chapter 139 (selections giving rise to mutants, genes for which selections exist) in a parsable format, with links to EcoCyc and PDFs">\n\t<title>Mutant selection tables for E. coli and Salmonella</title>\n\t<link rel="stylesheet" href="style.css">\n</head>\n<body>\n', file=output)
    print('<div id="menu"><nav><ul><li><a href="#about-anchor">About</a></li><li><a href="#table1-anchor">Selections giving rise to mutants</a></li><li><a href="#table2-anchor">Genes for which selections exist</a></li><li><a href="#references-anchor">References</a></li><li><a href="#contribute-anchor">Contribute</a></li></ul></nav></div>\n<div id="main">', file=output)
    print(open('about.html', 'r').read(), file=output)
    allgenes = getallgenes('ecocyc.csv')  # Load the mapping between ecocyc IDs and gene names so we can add links to ecocyc in the tables
    print(printtable1('table1.csv', allgenes), file=output)
    print(printtable2('table2.csv', allgenes), file=output)
    print(printtableref('references.csv'), file=output)
    print(open('contribute.html', 'r').read(), file=output)
    print('</div>\n%s</body>\n</html>' % open('footer.html', 'r').read(), file=output)

    outputfile = open('index.html', 'w')
    outputfile.write(output.getvalue())
    outputfile.close()

