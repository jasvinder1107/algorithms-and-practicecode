#!/usr/bin/env python3


def partition(A,start,end):
    pivot=A[end]
    pindex=start
    i=start
    while i <=(end-1):
        if A[i] <= pivot:
            temp=A[i]
            A[i]=A[pindex]
            A[pindex]=temp 
            pindex=pindex+1
        i=i+1
    temp1=A[pindex]
    A[pindex]=A[end]
    A[end]=temp1
    return pindex
    

def quicksort(A,start,end):
    if start<end:
        pin=partition(A,start,end)
        quicksort(A,start,pin-1)
        quicksort(A,pin+1,end)
    return A

if __name__=="__main__":
    #A=[12,140,111,90,80,30]
    A=[32,144,145,78,200,16,12,10,6,1]
    B=quicksort(A,0,len(A)-1)
    for i in B:
        print(i,end=" ")

