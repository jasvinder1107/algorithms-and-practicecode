#!/usr/bin/env python3

import math
import os
import random
import re
import sys

# Complete the birthday function below.
def birthday(s, d, m):
    count=0
    temp=0
    i=0
    if len(s)==1:
        if s[0]==d:
            count=1
    else:
        while i<len(s)-1:
            first=s[i]
            j=i+1
            if (len(s)-i) >= m:
                while j<(i+m):
                   temp+=s[j]
                   j+=1
            
                if (first+temp) == d:
                   count+=1
            temp=0
            i+=1
    return count
        

if __name__ == '__main__':

    n = 5

    s = [1,2,1,3,2]

    dm = [4,3]

    d = int(dm[0])

    m = int(dm[1])

    result = birthday(s, d, m)
    print(result)


