#!/usr/bin/env python3

from struct import pack
from poly1305 import *
from binascii import b2a_hex as bytes_to_hex
from binascii import a2b_hex as hex_to_bytes

class AEAD:
    
    @staticmethod
    def pad16(x):
        if len(x) % 16 == 0: 
            return b''
        else:
            return b'\x00' * (16 - (len(x) % 16))
    
    @staticmethod
    def num_to_8_le_bytes(n):
        return pack("<Q", n)
    
    @staticmethod
    def chacha20_aead_encrypt(aad, key, iv, constant, plaintext):
        nonce = constant + iv
        otk = Poly1305.poly1305_key_gen(key, nonce)
        ciphertext = Chacha20Encryption.encrypt(key, 1, nonce, plaintext)
        mac_data = aad + AEAD.pad16(aad)
        mac_data += hex_to_bytes(utils.ascii_to_hex(ciphertext)) + AEAD.pad16(ciphertext)
        mac_data += AEAD.num_to_8_le_bytes(len(aad))
        mac_data += AEAD.num_to_8_le_bytes(len(ciphertext))
        tag = Poly1305.poly1305_mac(mac_data, hex_to_bytes(otk))
        return (ciphertext, tag)
    
    @staticmethod
    def chacha20_aead_decrypt(aad, key, iv, constant, ciphertext):
        nonce = constant + iv
        otk = Poly1305.poly1305_key_gen(key, nonce)
        plaintext = Chacha20Encryption.decrypt(key, 1, nonce, ciphertext)
        mac_data = aad + AEAD.pad16(aad)
        mac_data += ciphertext + AEAD.pad16(ciphertext)
        mac_data += AEAD.num_to_8_le_bytes(len(aad))
        mac_data += AEAD.num_to_8_le_bytes(len(ciphertext))
        tag = Poly1305.poly1305_mac(mac_data, hex_to_bytes(otk))
        return (plaintext, tag)


