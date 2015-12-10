# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 21:52:34 2015

@author: Brian Ma
"""
from bs4 import BeautifulSoup
import numpy as np
import numpy.matlib
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from urllib.parse import urljoin
import re
import eigenvector
#------------------------------------------------------------------------------
num = 20
row =num
col = num
links = []
A = np.matlib.zeros((row,col),dtype=np.float64)
#------------------------------------------------------------------------------
def FindIndex(url, links):
    return int(links.index(url))
#-------------------------------------------------------------------------------
def IsInTheList(url, links):
    for i in links:
        if url == i:
            return True
    return False
#------------------------------------------------------------------------------
def Is_ntut_web(link):
    if link.find("http://www.ntut.edu.tw") >= 0:
        return True
    return False
#------------------------------------------------------------------------------
def MyParser(url,index):
    global links,A,num
    if (not IsInTheList(url, links)) and (len(links) <= num):
        try:
            html_page = urlopen(url)
            soup = BeautifulSoup(html_page, "lxml")
            meta = str(soup.html.head.meta)
            if meta.find('text/html;') >= 0:
                links.append(url)
                for link in soup.findAll('a'):
                    tempUrl = link.get('href')
                    tempUrl = urljoin("http://www.ntut.edu.tw",tempUrl)
                    if Is_ntut_web(tempUrl):
                        print("進入%s"%(tempUrl))
                        MyParser(tempUrl,FindIndex(url,links))
            #else:
                #print(meta)
        except:
            pass
    elif IsInTheList(url, links) and (len(links) <= num+1):
        if index != FindIndex(url,links):
            print("(%d:%d)"%(FindIndex(url,links),index))
            A[FindIndex(url,links),index]=1
            #print(A[FindIndex(url,links),index])
#------------------------------------------------------------------------------
if __name__=="__main__":
    MyParser("http://www.ntut.edu.tw/files/17-1021.php",0)
    print("[over]\n-------------------------------------")
    for url in links:
        print(url)
    eigenvector.ShowMatrix(A)
    eigenvector.ShowMatrix(eigenvector.FindEigenvector(A))
#-------------------------------------------------------------------------------
#python c:\EM_PJ\HtmlGetLink.py