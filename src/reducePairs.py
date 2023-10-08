#!/usr/bin/python3
import sys

lastPair, res = None, 0
for line in sys.stdin:
    products = line.strip().split("\t")
    if len(products) != 2:
        continue
    pair, val = products
    if lastPair and lastPair != pair:
        print(lastPair, "\t", str(res))
        if lastPair and lastPair.strip().split(" ")[0] != pair.strip().split(" ")[0]:
            print(pair.strip().split(" ")[0])
        lastPair, res = pair, int(val)
    else:
        if not lastPair:
            print(pair.strip().split(" ")[0])
        lastPair, res = pair, res + int(val)
