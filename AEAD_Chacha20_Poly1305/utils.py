#!/usr/bin/env python3

from math import floor

class utils:
    
    # from geeksforgeeks
    @staticmethod
    def left_roll(val, num, modulo):
        return (val << num) % modulo | (val >> (32 - num))

    @staticmethod
    def to_hex(val):
        fmt = "0x%0.8x" % val
        return fmt.format(val)
        
    @staticmethod
    def to_2hex(val):
        fmt = "0x%0.2x" % val
        return fmt.format(val)

    @staticmethod
    def to_int(val):
        return int(val, 16)
    
    # from stackoverflow
    @staticmethod
    def hex_to_ascii(h):
        return ''.join([chr(int(''.join(c), 16)) for c in zip(h[0::2], h[1::2])])

    # from stackoverflow
    @staticmethod
    def ascii_to_hex(s):
        return  "".join([hex(ord(c))[2:].zfill(2) for c in s])
