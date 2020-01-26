#!/usr/bin/env python3

import sys
from math import log2


def theta(state, w):
    c = [[0 for u in range(w)] for k in range(5)]
    d = [[0 for u in range(w)] for k in range(5)]
    new_state = [[[0 for d in range(5*5*w)] for c in range(5)] for d in range(5)]
    for x in range(5):
        for z in range(w):
            c[x][z] = state[x][0][z] ^ state[x][1][z] ^ state[x][2][z] ^ state[x][3][z] ^ state[x][4][z] 

    for x in range(5):
        for z in range(w):
            d[x][z] = c[(x-1)%5][z] ^ c[(x+1)%5][(z-1)%w] 

    for x in range(5):
        for y in range(5):
            for z in range(w):
                new_state[x][y][z] = state[x][y][z] ^ d[x][z]
    return new_state

def rho(state, w):
    new_state = [[[0 for d in range(5*5*w)] for c in range(5)] for d in range(5)]
    x, y = 1, 0
    for z in range(w):
        new_state[0][0][z] = state[0][0][z]
    for t in range(24):
        for z in range(w):
            new_state[x][y][z] = state[x][y][(z-(t+1)*(t+2)//2)%w]
        x, y = y, (2*x+3*y)%5
    return new_state

def pi(state, w):
    new_state = [[[0 for d in range(5*5*w)] for c in range(5)] for d in range(5)]
    for x in range(5):
        for y in range(5):
            for z in range(w):
                new_state[x][y][z] = state[(x+3*y)%5][x][z]
    return new_state

def chi(state, w):
    new_state = [[[0 for d in range(5*5*w)] for c in range(5)] for d in range(5)]
    for x in range(5):
        for y in range(5):
            for z in range(w):
                new_state[x][y][z] = state[x][y][z] ^ ((state[(x+1)%5][y][z] ^ 1) & (state[(x+2)%5][y][z]))
    return new_state

def rc(t):
    if t % 255 == 0:
        return 1
    R = [1, 0, 0, 0, 0, 0, 0, 0]
    for i in range(1, (t%255)+1):
        R = [0] + R
        R[0] = R[0] ^ R[8]
        R[4] = R[4] ^ R[8]
        R[5] = R[5] ^ R[8]
        R[6] = R[6] ^ R[8]
        R = R[:8]
    return R[0]

rc_calculated = [rc(t) for t in range(255)]

def iota(state, w, ri):
    new_state = state
    l = int(log2(w))
    RC = [0 for i in range(w)]
    for j in range(l+1):
        RC[2**j-1] = rc_calculated[j+7*ri]
    for z in range(w):
        new_state[0][0][z] = new_state[0][0][z] ^ RC[z]
    return new_state


def bits_to_state(bits, w):
    state = [[[0 for d in range(w)] for c in range(5)] for p in range(5)]
    for x in range(5):
        for y in range(5):
            for z in range(w):
                state[x][y][z] = bits[w*(5*y+x)+z]
    return state

def state_to_bits(state, w):
    lanes = [["" for i in range(5)] for j in range(5)]
    for i in range(5):
        for j in range(5):
            for z in range(w):
                lanes[i][j] += str(state[i][j][z])
    planes = ["" for j in range(5)]
    for j in range(5):
        planes[j] = str(lanes[0][j]) + str(lanes[1][j]) + str(lanes[2][j]) + str(lanes[3][j]) + str(lanes[4][j])
    return planes[0] + planes[1] + planes[2] + planes[3] + planes[4]
   

def xor(arr1, arr2):
    res = []
    for i in range(len(arr1)):
        res.append(int(arr1[i])^int(arr2[i]))
    return res

def pad10star1(x, m):
    j = (-1*m -2)%x
    return [1] + [0]*j + [1]


def rnd(state, w, ri):
    a = theta(state, w)
    b = rho(a, w)
    c = pi(b, w)
    d = chi(c, w)
    return iota(d, w, ri)


def keccak_p(bits, nr, w):
    state = bits_to_state(bits, w)
    for ri in range(int(12+2*log2(w)-nr), int(12+2*log2(w))):
        state = rnd(state, w, ri)
    res = state_to_bits(state, w)
    return res

def sponge(N, d, r, b=1600, nr=24):
    P = N + pad10star1(r, len(N))
    n = len(P)//r
    c = b-r
    Pn = []
    for i in range(0, len(P), r):
        Pn.append(P[i:i+r])
    S = [0]*b
    for i in range(n):
        S = keccak_p(xor(S, Pn[i]+[0]*c), nr, b//25)
    Z = ""
    while True:
        for i in range(r):
            Z += str(S[i])
        if d <= len(Z):
            return Z[:d]
        else:
            S = keccakp(S, nr, b//25)
       
def keccak_c(N, d, r):
    return sponge(N, d, r)

def shake128(M, d):
    M = bits_from_string(M)
    M += [1]*4
    s =  keccak_c(M, d*8, 1600-256)
    hash_val = ""
    for i in range(0, len(s), 8):
        byte = s[i:i+8]
        hash_val += byte[::-1]
    return hex(int(hash_val, 2))[2:]

# found on stackoverflow
def bits_from_string(s):
    result = []
    for c in s:
        bits = bin(ord(c))[2:]
        bits = '00000000'[len(bits):] + bits
        result.extend([int(b) for b in bits[::-1]])
    return result



def main():
    if len(sys.argv) < 2:
        print("usage: shake128 <length> input")
        exit(0)
    else:
        length = int(sys.argv[1])
        data = sys.stdin.read() #.strip()
        s = shake128(data, int(length))
        print(s)
if __name__ == "__main__":
    main()
