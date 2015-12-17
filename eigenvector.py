# -*- coding: utf-8 -*-
"""
Created on Sun Dec  6 14:23:01 2015

@author: Brian Ma
"""
import numpy as np
import numpy
from numpy import linalg as LA
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

    for j in range(col):
        for i  in range(row):
            if A[i,j] == 1:
                A[i,j] = 1/outputLink[j]
    G=0.85*A+(0.15)*(1/row)*1
    
    return A
#--------------------------------------
def FindEigenvector(A):
    tempA= A.copy()
    e_vals, e_vecs = LA.eig(ProcessMatrix(tempA))  
    e_vals = np.absolute(e_vals)
    e_vecs = np.absolute(e_vecs)
    for i in range(len(e_vals)):
        if numpy.allclose(e_vals[i],1.0):
            mysum = 0.0
            for j in e_vecs[:,i]:
                mysum+=j
            return e_vecs[:,i]/mysum
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
    #G=0.85*A+(0.15)*(1/row)*1
    #temp= G*temp
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
#------------------------------------
if __name__=="__main__":
    A=np.matrix([[0,0,0,0,0,0,1,0],
                 [1,0,1,1,0,0,0,0],
                 [1,0,0,0,0,0,0,0],
                 [0,1,0,0,0,0,0,0],
                 [0,0,1,1,0,0,1,0],
                 [0,0,0,1,1,0,0,1],
                 [0,0,0,0,1,0,0,1],
                 [0,0,0,0,1,1,1,0]
                 ],dtype=np.float64) 
    finalA = FindEigenvector(A)
    ShowMatrix(finalA,'f')
    #ShowMatrix(A,'f')
'''

'''

    
