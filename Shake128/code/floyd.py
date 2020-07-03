#!/usr/bin/env python3

from hashlib import shake_128
import sys
import time

base = "leo.berton@polytechnique.edu "
x0 = ""

def shake(x, n):
    return shake_128((base+x).encode()).hexdigest(n)

def rho(x0, n):
    s, T, H = 1, shake(x0, n), shake(shake(x0, n), n)
    while H != T:
        s, T, H = s+1, shake(T, n), shake(shake(H, n), n)
    T1, T2 = T, x0
    fT1, fT2 = shake(T1, n), shake(T2, n)
    while fT1 != fT2:
        T1, T2 = fT1, fT2
        fT1, fT2 = shake(T1, n), shake(T2, n)
    return (T1, T2)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python3 rho.py <output_length>")
        exit(0)
    n = int(sys.argv[1])
    start = time.time()
    print("Searching shake128 collisions on "+str(n)+" bytes outputs...")
    ret = rho(x0, n)
    print("## Collision found in", str(time.time()-start),"on", str(n), "bytes ##")
    print(base+ret[0], ">>>", shake(ret[0], n))
    print(base+ret[1], ">>>", shake(ret[1], n))



