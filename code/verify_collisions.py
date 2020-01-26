#!/usr/bin/env python3

import sys, os
from hashlib import shake_128

for i in range(1, 9):
    print("###### Collisions on", str(i), "bytes #####\n")
    path = "../collisions-"+str(i)
    tot = len([name for name in os.listdir(path)])
    for j in range(tot//2):
        f1 = open(path+"/ex-"+str(j)+".1", "r")
        f2 = open(path+"/ex-"+str(j)+".2", "r")
        data1 = f1.read()
        data2 = f2.read()
        print(data1, ">>>", shake_128(data1.encode()).hexdigest(i))
        print(data2, ">>>", shake_128(data2.encode()).hexdigest(i))
        print()
        f1.close()
        f2.close()
    print()
