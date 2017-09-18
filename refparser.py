#!/usr/bin/env python3

import os
import time
import string
from bs4 import BeautifulSoup
import re
import magic
import urllib.request


def checkpdf(output):
    """ Check whether a PDF file exists and is a valid PDF
    So far we only exclude files that are html or empty, which is the most likely outcome if the publisher tried to prevent downloads with wget
    """
    mime = magic.from_file('%s' % output, mime=True)
    if mime == 'application/pdf':
        return True
    elif mime == 'text/html' or 'empty' in mime:
        print('It seems that %s is not a valid pdf, mime type is %s' % (output, mime))
        return False
    else:  # Could still be a PDF, "magic" sometimes fails on crappy old files
        return True


def getsource(gscholarquery, nref):
    """Search the article on google scholar and call the parser on the returned webpage
    The google scholar webpage will be saved as gs_html/refnumber.html
    If this file already exist this function will return without doing anything
    """
    output = 'gs_html/%s.html' % nref
    if os.path.exists(output):
        parsehtmlfromgs(nref)
        return
    print('html file %s not found, trying to download' % output)
    os.system('wget --header="Accept: text/html,application/xhtml+xml,application/xml,application/pdf" -e robots=off -H --user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0" "%s" -O "%s"' % (gscholarquery, output))
    if os.path.exists(output):
        parsehtmlfromgs(nref)
        return
    print('failed to download %s' % output)


def getpdffromscihub(doi, output):
    """ Get a pdf from sci-hub using a DOI
    If the pdf alreay exists it will be erased (this function is only supposed to be called after checking the pdf has not already been successfully downloaded)
    """
    print('try to download pdf %s from sci-hub using doi %s' % (output, doi))
    os.system('wget -rHA "*.pdf" -e robots=off "http://sci-hub.bz/%s" -O %s' % (doi, output))
    if not checkpdf(output):
        os.remove(output)
        return False
    return True


def parsehtmlfromgs(nref):
    """Parse a google scholar search result and try to download a PDF
    We first try to get the pdf following the link provided by google scholar if available
    Otherwise if we find a DOI on google scholar page or when following the download link, we try to get a PDF from sci-hub
    This function should only be called after the google shcolar page has been downloaded as an html file by "getsource"
    """
    output = 'pdf/%s.pdf' % nref
    if os.path.exists(output):
        if checkpdf(output):
            return
        else:
            os.remove(output)
    soup = BeautifulSoup(open('gs_html/'+nref+'.html', 'r').read(), 'html.parser')
    res_section = soup.find(id='gs_ccl_results')
    if not res_section:
        print('%s does not look like a valid google scholar result, not doing anything' % output)
        return
    all_results = [x for x in res_section.find_all('div') if x.has_attr('class') and 'gs_r' in x['class']]
    if len(all_results) != 1:
        # Several matches
        print('none or several matches for %s on google scholar, not doing anything' % output)
        return
    else:
        result = all_results[0]
        searchdoi = re.search('10\.1[0-9]{3}(/|%2F)[^/ ?"]*', str(result))
        all_links = [x for x in result.find_all('a') if x.has_attr('href') and 'pdf' in x['href']]
        # If we have a single pdf on google scholar, try to download it
        if len(all_links) == 1:
            print('pdf for %s found on google scholar, trying to download it' % output)
            link = all_links[0]['href']
            os.system('wget -e robots=off -H --user-agent="Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.3) Gecko/2008092416 Firefox/3.0.3" "%s" -O %s' % (link, output))
            # Check that we got a valid pdf (sneaky proxies...)
            if checkpdf(output):
                return
            print('download of %s from google scholar failed (not a valid pdf)' % output)
            # Check that the webpage we got instead of the pdf does not contain a DOI (thanks springer!)
            if not searchdoi:
                fakepdf = open(output, 'r').read()
                searchdoi = re.search('10\.1[0-9]{3}(/|%2F)[^/ ?"]*', fakepdf)
        # If none or several PDFs on google scholar, or if download failed, try sci-hub using the DOI if any
        if len(all_links) > 1:
            print('several pdfs for %s on google scholar' % output)
        if len(all_links) == 0:
            print('no pdf for %s on google scholar' % output)
        if searchdoi:
            doi = searchdoi.group(0).split('.pdf')[0]  # Remove ".pdf" from the DOI
            getpdffromscihub(doi, output)  # Try to download from sci-hub
        else:
            print(' and no doi found for %s on google scholar' % output)
            # try to follow the link to the publisher website, and from there get a doi to use sci-hub
            htmllink = result.find('a')['href']  # Follow first link
            html = urllib.request.urlopen('http://www.sciencedirect.com/science/article/pii/S000398616480028X').read()
            searchdoi = re.search('10\.1[0-9]{3}(/|%2F)[^/ ?"]*', str(html))
            if searchdoi:
                doi = searchdoi.group(0).split('.pdf')[0]
                getpdffromscihub(doi, output)
            return

