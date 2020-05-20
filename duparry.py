#!/usr/bin/env python3

a=[1,2,3,1,3,6,6]

for i in range(0,len(a)):
    if a[abs(a[i])] >=0:
        a[abs(a[i])]=-a[abs(a[i])]
    else:
       print(abs(a[i]),end=" ")
