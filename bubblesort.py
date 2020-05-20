#!/usr/bin/env python3


def bubblesort(A):
   for i in range(0,len(A)-1):
       swapped=0
       for j in range(0,(len(A)-i-1)):
           if A[j]>A[j+1]:
               temp=A[j]
               A[j]=A[j+1]
               A[j+1]=temp
               swapped=1
       if(swapped==0):
            break
   for i in A:
       print(i,end=" ")



if __name__=="__main__":
    A=[13,1400,23,423,14,133,18,9,1]
    bubblesort(A)

