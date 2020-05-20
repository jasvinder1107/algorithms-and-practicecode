#!/usr/bin/env python3

def selectionsort(a,n):
    for i in range(0,n-1):
        imin=i
        for j in range((i+1),n):
            if a[j]<a[imin]:
               imin=j

        temp=a[i]
        a[i]=a[imin]
        a[imin]=temp
    print(a,end=" ")


if __name__=="__main__":
    A=[140,11,9,1,7,24,13,23,14]
    selectionsort(A,len(A))
