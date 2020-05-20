#!/usr/bin/env python3

def insertionsort(A):
    n=len(A)
    for i in range(1,n):
       key=A[i]
       j=i-1
       while j>=0 and A[j]>key:
          A[j+1]=A[j]
          j=j-1
       A[j+1]=key
    return A

if __name__=="__main__":
    A=[25,17,13,11,2]
    B=insertionsort(A)
    for i in B:
        print(i,end=" ")
