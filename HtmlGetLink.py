# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 21:52:34 2015
@author: Brian Ma
"""
from bs4 import BeautifulSoup
import numpy as np
import numpy.matlib
from urllib.request import Request, urlopen
from urllib.parse import urljoin
import eigenvector
import matplotlib.pyplot as plt
#------------------------------------------------------------------------------
num = 200
links = []
A = np.matlib.zeros((num,num),dtype=np.float64)
#------------------------------------------------------------------------------
def Refresh(A):
    global num,links
    temp = num
    if num > len(links):
        h = num- len(links)
        for i in range(h):
            A = np.delete(A, np.s_[temp-1], 1)
            A =np.delete(A, temp-1, 0)
            temp-=1
        return A
    else:
        return A
#------------------------------------------------------------------------------
def Rank(A):
    global links
    mydict = []
    for i in range(0,len(links)):
        mydict.append([A[i,0],links[i]])
    mydict.sort(reverse=True)
    return mydict
#------------------------------------------------------------------------------
def GetTitle(url):
    try:
         html_page = urlopen(url)
         soup = BeautifulSoup(html_page, "lxml")
         return str(soup.title.string)
    except:
        return ""
#------------------------------------------------------------------------------
def FindIndex(url, links):
     return int(links.index(url))
#-------------------------------------------------------------------------------
def IsInTheList(url, links):
    if url in links:
        return True
    else:
        return False
#------------------------------------------------------------------------------
def IsWeb(link):
    if len(link) > 100:
        return False
    mylist = ['#','Top','.pdf','.wmv','.jpg','.mp4','.ppt','.docx','downloadfile','www.plurk.com','.rar','.zip','.flv'] 
    for key in mylist:
        if link.find(key) >=0:
            return False
    return True
#------------------------------------------------------------------------------
def Is_ntut_web(link):
    #if (link.find("http://www.ntut.edu.tw") >= 0) and IsWeb(link):
    if link.find("http://www.")>=0 and link.find(".ntut.edu.tw") >= 0 and IsWeb(link):
        return True
    return False
#------------------------------------------------------------------------------

def MyParser(url,index):
    global links,A,num
    if (not IsInTheList(url, links)) and (len(links) <= num) and Is_ntut_web(url):
        try:
            soup = BeautifulSoup(urlopen(url), "lxml")
            result = soup.find("meta",attrs={"http-equiv":"refresh"})
            meta = str(soup.html.head.meta)
            if result:
                links.append(url)
                wait,text=result["content"].split(";")
                if text.lower().startswith("url="):
                    pice=text[4:]
                    tempUrl = urljoin('http://www.ntut.edu.tw',pice)
                    print(url)
                    MyParser(tempUrl,FindIndex(url,links))
                    if index != FindIndex(url,links):
                        A[FindIndex(url,links),index]=1
            elif meta.find('text/html;') >= 0:
                links.append(url)
                for link in soup.findAll('a'):
                    #print(A[:,0])
                    tempUrl = link.get('href')
                    tempUrl = urljoin("http://www.ntut.edu.tw",tempUrl)
                    MyParser(tempUrl,FindIndex(url,links))
                    if index != FindIndex(url,links):
                        A[FindIndex(url,links),index]=1
        except:
            pass
    elif IsInTheList(url, links) and (len(links) <= num+1):
        if index != FindIndex(url,links):
            A[FindIndex(url,links),index]=1
#------------------------------------------------------------------------------
def PlottingMatrix(A):
    plt.ion()
    plt.matshow(A, vmin=0.001, vmax=0.05) 
    plt.colorbar()
#------------------------------------------------------------------------------
if __name__=="__main__":
    MyParser("http://www.ntut.edu.tw/files/11-1021-5787.php",0)
    print("[over]\n-------------------------------------")
    links.pop()
    print(A.shape)
    A = Refresh(A)
    print(A.shape)
    print(len(links))
    #eigenvector.ShowMatrix(A,'i')
    PlottingMatrix(eigenvector.ProcessMatrix(A))

    finalA = eigenvector.FindEigenvector(A)
    eigenvector.ShowMatrix(finalA,'f')
    for i in range(len(links)):
        print("No.%-3d [%.6f] %s %s"%(i+1,finalA[i,0], ("["+GetTitle(links[i])+"]"),links[i]))
    print("---------------------------------------------------------------------------")
    mydict = Rank(finalA)
    i = 1
    for key,value in mydict:
        print("No.%-3d [%.6f] %s %s"%(i,key, ("["+GetTitle(value)+"]"),value))
        i+=1
#-------------------------------------------------------------------------------
# python c:\EM_PJ\HtmlGetLink.py
