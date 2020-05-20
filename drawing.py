#!/usr/bin/env python

import os
import sys

def pageCount(n, p):
    count=0
    initialpage=1
    lastpage=n
    if n%2 == 0:
        #number of pages are even
        if (n//2) >= p:
            #start from begining  
            if p == initialpage:
                count=0
            else:
                while initialpage <= (n//2):
                    initialpage+=2
                    count+=1
                    if initialpage >= p:
                       break
                      
        elif (n//2) < p:
            # start from back
            if p == lastpage:
                count=0
            else:
                while lastpage > ((n//2)+1):
                    lastpage-=2
                    count+=1
                    if lastpage <= p:
                        break
       

    else:
        #number of pages are odd
        if (n//2)+1 > p:
            #start from begining
            if p == initialpage:
                count=0
            else: 
                while initialpage <= ((n//2)+1):
                    initialpage+=2
                    count+=1
                    if initialpage >= p:
                        break
        elif ((n//2)+1) <= p:
            #start from back
            if p == lastpage or (lastpage-p) == 1:
                count=0
            else:
                while lastpage  > ((n//2)+1):
                     lastpage-=2
                     count+=1
                     if lastpage <= p or (lastpage-p) == 1:
                         break
    return count 


if __name__ == '__main__':
            n = 15 
            p = 8
            result = pageCount(n, p)
            print(result)
