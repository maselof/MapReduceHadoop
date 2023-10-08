#!/usr/bin/python
import sys

for line in sys.stdin:
    products = line.strip().split(" ")
    for i in range(len(products)):
        for j in range(i + 1, len(products)):
            if products[i] and products[j]:
                print(products[i], products[j], "\t1")
