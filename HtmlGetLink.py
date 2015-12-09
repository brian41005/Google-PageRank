# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 21:52:34 2015

@author: Brian Ma
"""
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import re
#------------------------------------------------------------------------------
links = []
#------------------------------------------------------------------------------
def IsInTheList(url, links):
    for i in links:
        if url == i:
            return True
    return False
#------------------------------------------------------------------------------
def Is_ntut_web(link):
    if link.find("ntut") >= 0:
        return True
    return False
#------------------------------------------------------------------------------
def MyParser(url):
    global links
    if not IsInTheList(url, links):
        try:
            html_page = urlopen(url)
            soup = BeautifulSoup(html_page, "lxml")
            meta = str(soup.html.head.meta)
            if meta.find('text/html;') >= 0:
                #print("進入[%s]"%(url))
                links.append(url)
                for link in soup.findAll('a', attrs={'href': re.compile("^http://")}):
                    tempUrl = link.get('href')
                    if Is_ntut_web(tempUrl):
                        MyParser(tempUrl)
                        print("目前links數量:%d"%(len(links)))
            #else:
                #print(meta)
        except:
            pass
    #else:
        #print("[%s] 已爬過"%(url))
#------------------------------------------------------------------------------
if __name__=="__main__":
    MyParser("http://www.ntut.edu.tw/bin/home.php")
    print("[over]\n-------------------------------------")
    for url in links:
        print(url)
#-------------------------------------------------------------------------------
#python c:\EM_PJ\HtmlGetLink.py
