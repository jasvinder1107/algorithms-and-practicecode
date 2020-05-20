#!/usr/bin/env python3


def merge(A,start,mid,end):
    i=start
    j=mid+1
    k=0
    temp=[0]*int(end-start+1)
    while i<=mid and j<=end:
        if A[i]>= A[j]:
            temp[k]=A[j]
            k=k+1
            j=j+1
        else:
            temp[k]=A[i]
            k=k+1
            i=i+1
    while i<=mid:
        temp[k]=A[i]
        i=i+1
        k=k+1
    while j<=end:
        temp[k]=A[j]
        j=j+1
        k=k+1
    p=start
    while p<=end:
        A[p]=temp[p-start]
        p=p+1
    return A 
def mergesort(A,start,end):
    if start < end:
        mid=int((start+end)/2)
        mergesort(A,start,mid)
        mergesort(A,mid+1,end)
        C=merge(A,start,mid,end)
        return C

if __name__=="__main__":
    A=[32,144,145,78,200,16,12,10,6,1]
    B=mergesort(A,0,len(A)-1)
    for i in B:
        print(i,end=" ")



