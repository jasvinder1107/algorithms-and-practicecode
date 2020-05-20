#!/usr/bin/env python3

import math
import os
import random
import re
import sys
import numpy as np

# Complete the matrixRotation function below.
def matrixRotation(matrix, r,m,n):
    print("Before rotation")
    print('\n'.join([''.join(['{:4}'.format(item) for item in row]) 
    for row in matrix]))
    for p in range(0,r):  
          temp=matrix[m-1][0]
          j=0
          i=m-1
          #starting with i=3 an j=0
          while i>0:
              matrix[i][j]=matrix[i-1][j]
              i=i-1

          #value of i=0 and j=0
          while j<n-1:
              matrix[i][j]=matrix[i][j+1]
              j=j+1

          # value of i=0 and j=3 
          while i < m-1:
              matrix[i][j]=matrix[i+1][j]
              i=i+1
          #value of i=3 and j=3
          while j>1 :
              matrix[i][j]=matrix[i][j-1]
              j=j-1
          matrix[i][j]=temp 
          """
          if matrix has 4 or more column it will form the inner matrix below code will deal with this portion of the problem.

          """
          rangemn=[m,n]
          numberofrotations=int(min(rangemn)/2)-1
          for inner in range(0,numberofrotations):
             if n>=4 and m>=4:
                 firstelement=[1+inner,1+inner]
                 lastelement=[(m-2-inner),(n-2-inner)]
                 temp1=matrix[lastelement[0]][firstelement[0]]
                 i=lastelement[0]
                 j=firstelement[1]
                 # i=2, j=1
                 while i>firstelement[0]:
                     matrix[i][j]=matrix[i-1][j]
                     i=i-1
                 #i=1 ,j=1
                 while j<lastelement[1]:
                     matrix[i][j]=matrix[i][j+1]
                     j=j+1
                 #i=1,j=2
                 while i<lastelement[0]:
                     matrix[i][j]=matrix[i+1][j]
                     i=i+1
                 if n > 4:
                    while j>firstelement[0]:
                      matrix[i][j]=matrix[i][j-1]
                      j=j-1
                    matrix[i][j+1]=temp1
                 else:
                    matrix[i][j]=temp1
                   
          print("After {} rotation".format(p+1))
          print('\n'.join([''.join(['{:4}'.format(item) for item in row]) 
            for row in matrix]))

if __name__ == '__main__':

    m = 4 

    n = 4 

    r = 2

    matrix = [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]]
    #matrix=[[1,2,3,4,5],[6,7,8,9,10],[11,12,13,14,15],[16,17,18,19,20]]
    #matrix=[[1,2,3,4,5,6,7],[8,9,10,11,12,13,14],[15,16,17,18,19,20,21],[22,23,24,25,26,27,28]]
    #matrix=[[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16],[17,18,19,20]]
    #matrix=[[1,2,3],[4,5,6]]
    #matrix=[[1,2,3,4],[5,6,7,8],[9,10,11,12],[12,13,14,15],[16,17,18,19],[20,21,22,23],[24,25,26,27]]
    #matrix=[[1,2,3,4,5],[6,7,8,9,10]]
    #matrix=np.random.randint(20,size=(m,n))
    matrixRotation(matrix,r,m,n)
