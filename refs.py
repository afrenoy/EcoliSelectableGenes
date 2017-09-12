#!/usr/bin/env python3

import os
import time
import string
from bs4 import BeautifulSoup

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

# Get pdf from google scholar results
def parsehtmlfromgs(nref):
    output='pdf/%s.pdf'%nref
    if os.path.exists(output):
        return
    print('pdf %s not found, trying to download'%output)
    soup=BeautifulSoup(open('gs_html/'+nref+'.html','r').read(),'html.parser')
    res_section=soup.find(id='gs_ccl_results')
    if not res_section:
        print('%s does not look like a valid google scholar result, not doing anything'%output)
        return
    all_results=[x for x in res_section.find_all('div') if x.has_attr('class') and 'gs_r' in x['class']]
    if len(all_results)!=1:
        # Several matches
        print('none or several matches for %s, not doing anything'%output)
    else:
        result=all_results[0]
        all_links=[x for x in result.find_all('a') if x.has_attr('href') and 'pdf' in x['href']]
        if len(all_links)!=1:
            print('none or several pdfs for %s, not doing anything'%output)
        else:
            link=all_links[0]['href']
            print('link found for %s : %s'%(output,link))
            os.system('wget -e robots=off -H --user-agent="Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.3) Gecko/2008092416 Firefox/3.0.3" "%s" -O %s'%(link,output))

