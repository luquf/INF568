#!/usr/bin/env python3

from hashlib import shake_128
import random, sys, string, time, os
import shake128

email = "leo.berton@polytechnique.edu"

def get_email(k=10):
    return email + " " + ''.join(random.choices(string.ascii_lowercase + string.digits, k=k)) 

def shake(x, n):
    #return shake128.shake128(x, n) # TOO SLOWWWW
    return shake_128(x.encode()).hexdigest(n)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: ./collision.py <output_length> <number_of_appended_bytes_to_email>")
        exit(0)
    n = int(sys.argv[1])
    k = int(sys.argv[2])
    path = "../collisions-"+str(n)
    if not os.path.exists(path):
        os.mkdir(path)
    print("Searching shake128 collisions on "+str(n)+" bytes outputs...")
    hash_dict = dict()
    start = time.time()
    i = 0
    nc = 0
    while True:
        data = get_email(k)
        hash_val = shake(data, n)
        if hash_val in hash_dict:
            print("## Collision found in", str(time.time()-start), "seconds on " + str(n) + " bytes ##")
            print("1.", data, ">>>", hash_val)
            print("2.", hash_dict[hash_val], ">>>", hash_val)
            start = time.time()
            nc+=1
            i+=1
        else:
            hash_dict[hash_val] = data
            i+=1
            print("Iteration:", i, "with", nc, "collisions found", end="\r", flush=True)


