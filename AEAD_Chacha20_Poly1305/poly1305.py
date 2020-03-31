#!/usr/bin/env python3

from struct import pack, unpack
from math import ceil
from utils import utils
from chacha20 import *

class Poly1305:

    @staticmethod
    def clamp(r): 
        return r & 0x0ffffffc0ffffffc0ffffffc0fffffff

    @staticmethod
    def le_bytes_to_num(b):
        return int.from_bytes(b, byteorder='little')
    
    # https://stackoverflow.com/questions/37334169/python-convert-integer-to-16-byte-bytes
    @staticmethod
    def num_to_16_le_bytes(n):
        return bytes([((n >> (i * 8)) & 0xff) for i in range(16)])
   
    @staticmethod
    def poly1305_mac(msg, key):
        r = Poly1305.le_bytes_to_num(key[0:16])
        r = Poly1305.clamp(r)
        s = Poly1305.le_bytes_to_num(key[16:32])
        a = 0  # a is the accumulator
        p = (1 << 130) - 5
        for i in range(1, ceil(len(msg)/16)+1):
            n = Poly1305.le_bytes_to_num(msg[((i-1)*16):(i*16)] + b'\x01')
            a += n
            a = (r * a) % p
        a += s
        return Poly1305.num_to_16_le_bytes(a)

    @staticmethod 
    def poly1305_key_gen(key, nonce):
        counter = 0
        block = Chacha20Block()
        block.chacha20_block(key, counter, nonce)
        key = block.serialize()
        # 64 instead of 32 as it is in hexdecimal format
        return key[0:64]

