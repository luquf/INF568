#!/usr/bin/env python3

from binascii import b2a_hex as bytes_to_hex

def hex_to_ascii(h):
    return ''.join([chr(int(''.join(c), 16)) for c in zip(h[0::2], h[1::2])])

def ascii_to_hex(s):
    return  "".join([hex(ord(c))[2:].zfill(2) for c in s])


# BEGIN RFC 7748

def decodeLittleEndian(b, bits=255):
    return sum([b[i] << 8*i for i in range((bits+7)//8)])

def decodeUCoordinate(u, bits=255):
    u_list = [ord(b) for b in u]
    if bits % 8:
        u_list[-1] &= (1<<(bits%8))-1
    return decodeLittleEndian(u_list, bits)

def encodeUCoordinate(u, bits=255, p=2**255-19):
    u = u % p
    return ''.join([chr((u >> 8*i) & 0xff) for i in range((bits+7)//8)])

def decodeScalar25519(k):
    k_list = [ord(b) for b in k]
    k_list[0] &= 248
    k_list[31] &= 127
    k_list[31] |= 64
    return decodeLittleEndian(k_list, 255)

# END RFC 7748

def xADD(P, Q, PmQ, N):
    U = (P[0]-P[1])*(Q[0]+Q[1]) % N
    V = (P[0]+P[1])*(Q[0]-Q[1]) % N
    return (PmQ[1]*pow(U+V, 2, N) % N, PmQ[0]*pow(U-V, 2, N) % N)

def xDBL(P, N, A):
    Q = pow(P[0]+P[1], 2, N)
    R = pow(P[0]-P[1], 2, N)
    return (Q*R % N, (Q-R)*(R+(A+2)*P[0]*P[1]) % N)

def cswap(b, x0, x1):
    return ((1-b)*x0 + b*x1, b*x0 + (1-b)*x1)

def ladder(m, P, p=2**255-19, A=486662, A24=121665):
    x0, x1 = (1, 0), P
    for swap in bin(m)[2:]:
        swap = int(swap)
        d0 = xDBL(x0, p, A)
        d1 = xDBL(x1, p, A)
        add = xADD(x0, x1, P, p)
        x0 = (cswap(swap, d0[0], add[0])[0], cswap(swap, d0[1], add[1])[0])
        x1 = (cswap(swap, add[0], d1[0])[0], cswap(swap, add[1], d1[1])[0])
    return x0

def X25519(m, x, p=2**255-19):
    l = ladder(m, (x, 1))
    return l[0] * pow(l[1], p-2, p) % p


def diffie_hellman():
    try:
        a = decodeScalar25519(hex_to_ascii(bytes_to_hex(open("/dev/urandom","rb").read(32)).decode("utf-8")))
        b = decodeScalar25519(hex_to_ascii(bytes_to_hex(open("/dev/urandom","rb").read(32)).decode("utf-8")))
        
        basepoint = decodeUCoordinate("090000000000000000000000000000000")

        K_a = X25519(a, basepoint)
        K_b = X25519(b, basepoint)
        
        k_alice = X25519(a, K_b)
        k_bob = X25519(b, K_a)
        
        print("\n##### DIFFIE-HELLMAN #####\n")
        print("Alice's private:", a)
        print("Bob's private:", b, end="\n\n")
        print("Alice's public:", K_a)
        print("Bob's public:", K_b, end="\n\n")
        print("Alice's K:", k_alice)
        print("Bob's K:", k_bob, end="\n\n")
        print("Same shared secret:", k_alice == k_bob)
 
    except:
        print("Failed to read /dev/urandom")
        exit(1)

