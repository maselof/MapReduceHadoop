#!/usr/bin/python3
import sys
from collections import defaultdict

pairsMap = defaultdict(lambda: 0)
currKey = None
for line in sys.stdin:
    splitted = line.strip().split(' ')
    if len(splitted) != 2:
        continue
    
    key, value = splitted
    if not currKey:
        currKey = key
    
    if currKey != key:
        for pair in sorted(pairsMap.items(), key=lambda item: -item[1]):
            print(currKey, pair[0], pair[1])
        pairsMap.clear()
        currKey = key

    pairsMap[value] += 1

for pair in sorted(pairsMap.items(), key=lambda item: -item[1]):
    print(currKey, pair[0], pair[1])