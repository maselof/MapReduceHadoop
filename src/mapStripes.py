#!/usr/bin/python3
import sys
from collections import defaultdict

prodMap = defaultdict(lambda: 0)
for line in sys.stdin:
    prods = line.strip().split(' ')
    for prod in prods:
        prodMap[prod] += 1
    
    prods.sort()
    for i in range(len(prods)):
        print(prods[i], end=' ')
        for j in range(len(prods)):
            if i != j:
                print(prods[j], prodMap[prods[j]], end=' ')
        print()
    prodMap.clear()
