import contextlib
import os
import subprocess
import sys
import pyhdfs
import random

PRODUCTS = ["banana", "potato", "milk", "bread", "eggs", "chips", "yogurt", "sausage", "cheese", "pita",
            "butter", "sunflowerOil", "juice", "soju", "beer", "croutons", "iceCream", "meat", "dill",
            "parsley", "bayLeaf", "coffee", "sugar", "pepper", "carrot", "cucumber", "broccoli"]


def createDataBase(cnt, min_check_size, max_check_size):
    res = os.system("ls src/db.txt")
    if res == 0:
        os.system("rm src/db.txt")

    f = open("src/db.txt", "w")
    s = ""
    max_check_size = min(max_check_size, len(PRODUCTS))
    for i in range(cnt):
        n = random.randint(min_check_size, max_check_size)
        prods_cnt = len(PRODUCTS)
        for j in range(n):
            randidx = random.randint(0, prods_cnt - 1)
            s += PRODUCTS[randidx] + " "
            PRODUCTS[randidx], PRODUCTS[prods_cnt-1] = PRODUCTS[prods_cnt-1], PRODUCTS[randidx]
            prods_cnt -= 1
        s += "\n"
        f.write(s)
        s = ""
    f.close()


def getArgs() -> list:
    if len(sys.argv) != 5:
        print("[host] [port] [username] [pairs|stripes]")
        return []
    return sys.argv[1:5]


def main():
    # Upload database
    args = getArgs()
    if not args:
        return
    hdfsClient = pyhdfs.HdfsClient(hosts=f"{args[0]}:{args[1]}",
                                   user_name=f"{args[2]}")
    createDataBase(30, 3, 10)
    f = open("src/db.txt", "rb")
    hdfsClient.delete(f"/user/{args[2]}/products/input", recursive=True)
    hdfsClient.create(f"/user/{args[2]}/products/input", f)
    f.close()

    # Cross-correlation
    mapper = None
    reducer = None
    dir = None
    if args[3] == "pairs":
        mapper = "mapPairs.py"
        reducer = "reducePairs.py"
        dir = "pairs/"
    elif args[3] == "stripes":
        mapper = "mapStripes.py"
        reducer = "reduceStripes.py"
        dir = "stripes/"
    else:
        print("Algorithm must be 'pairs' or 'stripes'")
        return

    os.system(f"hadoop fs -rm -r /user/{args[2]}/products/output/{dir}")
    os.system("yarn jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar"
              " -files `pwd`/src/mapPairs.py,`pwd`/src/reducePairs.py"
              " -input products/input/"
              f" -output products/output/{dir}"
              f" -mapper `pwd`/src/{mapper}"
              f" -reducer `pwd`/src/{reducer}")

    product = input("Enter product name: ")
    adviseCnt = 10
    localResPath = "./src/ccres.txt"
    hdfsClient.copy_to_local(f"/user/{args[2]}/products/output/{dir}/part-00000", localResPath)
    with open(localResPath) as res:
        lines = res.readlines()
        offset = None
        for i in range(len(lines)):
            record = lines[i].strip().split(' ')
            if record[0] == product:
                offset = i
                break    
        if offset is None:
            print("Product not found")
            return

        idx = 0
        while offset+idx < len(lines) and adviseCnt > 0:
            record = lines[offset+idx].strip().split(' ')
            if record[0] != product:
                break
            print(f"{idx+1}. {record[1]}")
            adviseCnt -= 1
            idx += 1
        print()


if __name__ == "__main__":
    main()
