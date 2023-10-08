import contextlib
import os
import subprocess
import sys
import pyhdfs
import random

PRODUCTS = ["banana", "potato", "milk", "bread", "eggs", "chips", "yogurt", "sausage", "cheese", "pita",
            "butter", "sunflowerOil", "juice", "soju", "beer", "croutons", "iceCream", "meat", "dill",
            "parsley", "bayLeaf", "coffee", "sugar", "pepper", "carrot", "cucumber", "broccoli"]


def createDataBase():
    res = os.system("ls src/db.txt")
    if res == 0:
        os.system("rm src/db.txt")

    f = open("src/db.txt", "w")
    s = ""
    for i in range(len(PRODUCTS)):
        n = random.randint(3, len(PRODUCTS) - 15)
        for j in range(n):
            s += PRODUCTS[random.randint(1, len(PRODUCTS) - 1)] + " "
        s += "\n"
        f.write(s)
        s = ""
    f.close()


def getDataFromCMD() -> list:
    if len(sys.argv) != 4:
        print("Need more arguments [host] [port] [username]")
        return []
    return sys.argv[1:4]


def main():
    # Download database in hdfs
    data = getDataFromCMD()
    if not data:
        return
    hdfsClient = pyhdfs.HdfsClient(hosts=f"{data[0]}:{data[1]}",
                                   user_name=f"{data[2]}")
    createDataBase()
    f = open("src/db.txt", "rb")
    hdfsClient.delete(f"/user/{data[2]}/products", recursive=True)
    hdfsClient.create(f"/user/{data[2]}/products/input", f)
    f.close()

    # Algorithm crossCorrelation
    hdfsClient.mkdirs(f"/user/{data[2]}/products/output")
    os.system(f"hdfs dfs -rm -r products/output")
    os.system("yarn jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar"
              " -files `pwd`/src/mapPairs.py,`pwd`/src/reducePairs.py"
              " -input products/input/"
              " -output products/output/"
              " -mapper `pwd`/src/mapPairs.py"
              " -combiner `pwd`/src/reducePairs.py"
              " -reducer `pwd`/src/reducePairs.py")
    hdfsClient.get_file_status(f"/user/{data[2]}/products/output/part-00000")

    # Adviser
    cat = subprocess.Popen(["hadoop", "fs", "-cat", f"/user/{data[2]}/products/output/part-00000"],
                           stdout=subprocess.PIPE)
    data = []
    for line in cat.stdout:
        data.append(str(line.decode("utf-8")).strip().split("\t"))
    print(data[0][0])
    while True:
        cmd = input("Input name product: ")
        cmd.split()
        res = []
        flag = False
        for i in range(len(data)):
            if flag and len(data[i]) == 2:
                res.append([data[i][0], int(data[i][1].strip())])
            if len(data[i]) == 1 and cmd == data[i][0]:
                flag = True
            if len(data[i]) == 1 and cmd != data[i][0]:
                flag = False
                continue
        if len(res) == 0:
            print("Product not found")
            continue
        res.sort(key=lambda x: x[1], reverse=True)
        for i in range(5):
            print(res[i][0].strip(), "\t", res[i][1])


if __name__ == "__main__":
    main()
