#!/usr/bin/env python3

A=[[1,2],[3,4],[5,6]]

m=len(A)
n=len(A[0])
b=[]
if m==1 and n==1:
   print(A[0][0])
else:
    dir=0
    T=0
    B=m-1
    L=0
    R=n-1
    while T<=B and L<=R:
        if dir == 0:
            i=L
            while i<=R:
                b.append(A[T][i])
                i=i+1
            dir=1
            T=T+1
        elif dir == 1:
            i=T
            while i<=B:
                b.append(A[i][R])
                i=i+1
            dir=2
            R=R-1
        elif dir == 2:
            i=R
            while i>=L:
                b.append(A[B][i])
                i=i-1
            B=B-1
            dir=3
        elif dir == 3:
            i=B
            while i>=T:
                b.append(A[i][L])
                i=i-1
            dir=0
            L=L+1
    for i in b:
        print(i,end=" ")
