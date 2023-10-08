#!/usr/bin/python
import sys

(lastPair, res) = (None, 0)
counts = []
for line in sys.stdin:
    products = line.strip().split("\t")
    (pair, val) = products
    if lastPair and lastPair != pair:
        print(lastPair, "\t", str(res))
        if lastPair and lastPair.strip().split(" ")[0] != pair.strip().split(" ")[0]:
            print(pair.strip().split(" ")[0])
        (lastPair, res) = (pair, int(val))
    else:
        if not lastPair:
            print(pair.strip().split(" ")[0])
        (lastPair, res) = (pair, res + int(val))
