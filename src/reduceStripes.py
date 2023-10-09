#!/usr/bin/python3
import sys
from collections import defaultdict

currKey = None
prodMap = defaultdict(lambda: 0)
for line in sys.stdin:
    splitted = line.strip().split(' ')
    if len(splitted) < 2:
        continue
    
    key = splitted[0]
    if not currKey:
        currKey = key
    
    if currKey != key:
        for item in sorted(prodMap.items(), key=lambda item: -item[1]):
            print(currKey, item[0], item[1])
        currKey = key
        prodMap.clear()

    for i in range(1, len(splitted), 2):
        prodMap[splitted[i]] += int(splitted[i+1])

for item in sorted(prodMap.items(), key=lambda item: -item[1]):
    print(key, item[0], item[1])