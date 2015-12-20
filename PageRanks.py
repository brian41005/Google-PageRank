# -*- coding: utf-8 -*-
"""
Created on Sat Dec 19 14:15:22 2015

@author: Brian Ma
"""
import lxml
from bs4 import BeautifulSoup
import numpy as np
import numpy.matlib
import numpy 
from urllib.request import Request, urlopen
from urllib.parse import urljoin
import matplotlib.pylab as plt
import os
from numpy import linalg as LA
import tkinter.filedialog
#--------------------------------------
num = 2000
links = []
A = np.matlib.zeros((num,num),dtype=np.float64)
NumberOfScans = 0
#--------------------------------------
def GetNumberOfColLink(A):
    row ,col =A.shape
    number = []
    for i in range(col):
        number.append(0)    
    
    for j in range(col):
        for i in range(row):
            if A[i,j] == 1:
               number[j] +=1
    return number
#--------------------------------------
def ProcessMatrix(A):
    row ,col =A.shape
    outputLink = GetNumberOfColLink(A)
    alpha = 0.85
    for j in range(col):
        for i  in range(row):
            if A[i,j] == 1:
                A[i,j] = 1/outputLink[j]
    ONE = np.ones((row ,col),dtype=np.float64)
    G=alpha*A+((1-alpha)*(1/row)*ONE)#google matrix
    #ShowMatrix(G,'f')
    return G
#--------------------------------------
def FindEigenvector(A):
    tempA= A.copy()
    tempA = ProcessMatrix(tempA)
    e_vals, e_vecs = LA.eig(tempA)  
    e_vals = np.absolute(e_vals)
    e_vecs = np.absolute(e_vecs)
    #print(e_vals)
    #print(e_vecs)
    for i in range(len(e_vals)):
        if numpy.allclose(e_vals[i],1.0):
            mysum = 0.0
            for j in e_vecs[:,i]:
                mysum+=j
            return e_vecs[:,i]/mysum
    
    mysum = 0.0
    for j in e_vecs[:,0]:
        mysum+=j
    return e_vecs[:,0]/mysum
    '''
    row ,col =tempA.shape
    initialnum = 1/row
    v= [[initialnum]]
    for i in range(row-1):
        v = np.append(v, np.matrix([initialnum]), axis=0)
    temp=tempA*v
    i=0

    while True:
        if not numpy.allclose(temp,tempA*temp):
            temp=tempA*temp
            i+=1
        else:
            break
    return temp
    '''
#------------------------------------
def ShowMatrix(A,key):
    row , col = A.shape
    for i in range(100): 
        print("_",end="")
    print()
    for i in range(row):
        for j in range(col):
            if key=='f':
                print("%.4f"%(A[i,j]),end =" ")
            else:
                print("%d"%(A[i,j]),end =" ")
        print()
    for i in range(100): 
        print("_",end="")
    print()
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
        mydict.append([A[i,0],GetTitle(links[i]),links[i]])
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
    mylist = ['Member.php','BlogList.php','PrdList.php','U-Tech','#','Top','.pdf','.wmv','.jpg','.mp4','.ppt','.docx','downloadfile','www.plurk.com','.rar','.zip','.flv','mp3'] 
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
    global links,A,num,NumberOfScans
    if (not IsInTheList(url, links)) and (len(links) <= num) and Is_ntut_web(url):
        try:
            soup = BeautifulSoup(urlopen(url), "lxml")
            NumberOfScans +=1
            result = soup.find("meta",attrs={"http-equiv":"refresh"})
            meta = str(soup.html.head.meta)
            if result:
                links.append(url)
                wait,text=result["content"].split(";")
                if text.lower().startswith("url="):
                    pice=text[4:]
                    tempUrl = urljoin('http://www.ntut.edu.tw',pice)
                    os.system('cls')
                    print("Number of scans: %d"%(NumberOfScans))
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
    q75,q25 = np.percentile(A,[75,25])
    print("A.min=%.6f A.max=%.6f Q75=%.6f Q25=%.6f"%(A.min(), A.max(), q75, q25))
    plt.matshow(A, vmin=A.min(), vmax=0.06) 
    plt.colorbar()
    plt.show()
#------------------------------------------------------------------------------
def SaveRanks(myDict):
    try:
        file = open("c:\EM_PJ\PageRanks.txt", "a")
        i = 1
        for rank, title, link in myDict:
            try:
                file.write("No.%-3d  [%.6f]  [%s] %s\n"%(i, rank, title, link))
            except:
                file.write("No.%-3d  [%.6f]  [%s] %s\n"%(i, rank, ""   , link))
            i+=1
        file.close()
        print("[Saving is successful]")
    except FileExistsError as msg:
        print(msg)
#------------------------------------------------------------------------------
if __name__=="__main__":
    os.system("mode con cols=80 lines=20")
    os.system("COLOR 70")
    print("================================ START ===============================")
    MyParser('http://www.ntut.edu.tw/files/17-1021.php',0)
    links.pop()
    print("================================[over]================================")
    print(A.shape)
    A = Refresh(A)
    print(A.shape)
    print(len(links))
    print("計算中...")
    finalA = FindEigenvector(A)
    myDict = Rank(finalA)
    print("計算完畢")
    print("儲存資料中...")
    SaveRanks(myDict)
    print("儲存完畢")
    print("繪製矩陣中...")
    PlottingMatrix(ProcessMatrix(A))
    print("繪製矩陣完畢")
    os.system("PAUSE")
#-------------------------------------------------------------------------------
# python c:\EM_PJ\PageRanks.py
