#!/usr/bin/env python3

import math
import os
import random
import re
import sys

# Complete the migratoryBirds function below.
def migratoryBirds(arr):
    birdtype={"1":0,"2":0,"3":0,"4":0,"5":0}
    max=0
    commonbird=9999
    for i in arr:
        if str(i) in birdtype.keys():
            birdtype[str(i)]+=1
    for k,v in birdtype.items():
        if v == max:
            if k < commonbird:
               max=v
               commonbird=k
        elif v > max:
             max=v
             commonbird=k
    return commonbird
        
              

if __name__ == '__main__':

    arr_count = 11

    arr = [1,2,3,4,5,4,3,2,1,3,4]

    result = migratoryBirds(arr)

    print(result)
