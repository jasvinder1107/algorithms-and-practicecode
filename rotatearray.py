#!/usr/bin/env python3


def rotateArray(a,b):
    ret=[]
    if b > len(a):
        c=b%len(a) 
    else:
        c=b
    for i in range(len(a)-c):
        ret.append(a[i+c])
    for i in range(c):
        ret.append(a[i])
    return ret

if __name__=="__main__":
    a=[14,5,14,34,42,63,17,25,39,61,97,55,33,96,62,32,98,77,35]
    b=56
    c=rotateArray(a,b)
    for i in c:
        print(i,end=" ")
