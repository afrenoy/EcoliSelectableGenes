#!/usr/bin/env python3

import os
import time
import string
from bs4 import BeautifulSoup
import re
import magic

def checkpdf(output):
    mime=magic.from_file('%s'%output,mime=True)
    if mime=='application/pdf':
        return True
    elif mime=='text/html' or 'empty' in mime:
        print('It seems that %s is not a valid pdf, mime type is %s'%(output,mime))
        return False
    else: # Bénéfice du doute...
        return True

# Search the article on google scholar
def getsource(gscholar,nref):
    output='gs_html/%s.html'%nref
    if os.path.exists(output):
        parsehtmlfromgs(nref)
        return
    print('html %s not found, trying to download'%output)
    number=int(nref.rstrip(string.ascii_lowercase))
    os.system('wget --header="Accept: text/html,application/xhtml+xml,application/xml,application/pdf" -e robots=off -H --user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0" "%s" -O "%s"'%(gscholar,output))
    time.sleep(0.2)

# Get pdf from google scholar results or sci hub
def parsehtmlfromgs(nref):
    output='pdf/%s.pdf'%nref
    if os.path.exists(output):
        if checkpdf(output):
            return
        else:
            os.remove(output)
    soup=BeautifulSoup(open('gs_html/'+nref+'.html','r').read(),'html.parser')
    res_section=soup.find(id='gs_ccl_results')
    if not res_section:
        print('%s does not look like a valid google scholar result, not doing anything'%output)
        return
    all_results=[x for x in res_section.find_all('div') if x.has_attr('class') and 'gs_r' in x['class']]
    if len(all_results)!=1:
        # Several matches
        print('none or several matches for %s on google scholar, not doing anything'%output)
        return
    else:
        result=all_results[0]
        searchdoi=re.search('10\.1[0-9]{3}(/|%2F)[^/ ?"]*',str(result))
        all_links=[x for x in result.find_all('a') if x.has_attr('href') and 'pdf' in x['href']]
        # If we have a single pdf on google scholar, try to download it
        if len(all_links)==1:
            print('pdf for %s found on google scholar, trying to download it'%output)
            link=all_links[0]['href']
            #print('link found for %s : %s'%(output,link))
            os.system('wget -e robots=off -H --user-agent="Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.3) Gecko/2008092416 Firefox/3.0.3" "%s" -O %s'%(link,output))
            # Check that we got a valid pdf (sneaky proxies...)
            if checkpdf(output):
                return
            print('download of %s from google scholar failed (not a valid pdf)'%output)
            # Check that the webpage we got instead of the pdf does not contain a doi (thanks springer!)
            if not searchdoi:
                fakepdf=open(output,'r').read()
                searchdoi=re.search('10\.1[0-9]{3}(/|%2F)[^/ ?"]*',fakepdf)
        # If none (or several) pdfs on google scholar, or if download failed, try sci-hub using the doi if any
        if len(all_links)>1:
            print('several pdfs for %s on google scholar'%output)
        if len(all_links)==0:
            print('no pdf for %s on google scholar'%output)
        if searchdoi:
            doi=searchdoi.group(0).split('.pdf')[0] # Remove .pdf from the doi
            print(' but found doi %s, trying to download from sci-hub'%doi)
            # Try to download from scihub
            os.system('wget -rHA "*.pdf" -e robots=off "http://sci-hub.bz/%s" -O %s'%(doi,output))
        else:
            print(' and no doi found for %s, not doing anything'%output)
            return

