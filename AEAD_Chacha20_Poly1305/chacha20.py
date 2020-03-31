#!/usr/bin/env python3

from math import floor
from struct import pack, unpack
from binascii import b2a_hex as bytes_to_hex
from binascii import a2b_hex as hex_to_bytes
from utils import utils

class Chacha20Block:

    def __init__(self):
        self.constants = [utils.to_int('0x61707865'), 
                          utils.to_int('0x3320646e'), 
                          utils.to_int('0x79622d32'), 
                          utils.to_int('0x6b206574')]
        self.state = []
        self.counter = 1
        self.modulo = pow(2, 32)

    def __str__(self):
        return str(self.state[:4]) + "\n" + str(self.state[4:8]) + "\n" + str(self.state[8:12]) + "\n" + str(self.state[12:16])

    def quarter_round(self, a, b, c, d):
        a = (a + b) % self.modulo; d ^= a; d = utils.left_roll(d, 16, self.modulo)
        c = (c + d) % self.modulo; b ^= c; b = utils.left_roll(b, 12, self.modulo)
        a = (a + b) % self.modulo; d ^= a; d = utils.left_roll(d, 8, self.modulo)
        c = (c + d) % self.modulo; b ^= c; b = utils.left_roll(b, 7, self.modulo)
        return a, b, c, d

    def Qround(self, x, y, z, w):
        a, b, c, d = self.state[x], self.state[y], self.state[z], self.state[w]
        a, b, c, d = self.quarter_round(a, b, c, d)
        self.state[x], self.state[y], self.state[z], self.state[w] = a, b, c, d

    def inner_block(self):
        self.Qround(0, 4, 8, 12)
        self.Qround(1, 5, 9, 13)
        self.Qround(2, 6, 10, 14)
        self.Qround(3, 7, 11, 15)
        self.Qround(0, 5, 10, 15)
        self.Qround(1, 6, 11, 12)
        self.Qround(2, 7, 8, 13)
        self.Qround(3, 4, 9, 14)

    def initialize_block(self, key, counter, nonce):
        self.state += self.constants
        a = unpack("<IIIIIIII", key)
        self.state += a
        self.state.append(counter)
        b = unpack("<III", nonce)
        self.state += b

    def serialize(self):
        serialized_data = ""
        for i in range(len(self.state)):
            serialized_data += bytes_to_hex(pack("<I", self.state[i])).decode()
        return serialized_data

    def chacha20_block(self, key, counter, nonce):
        self.initialize_block(key, counter, nonce)
        initial_state = list(self.state)
        for i in range(10):
            self.inner_block()
        for i in range(len(self.state)):
            self.state[i] = (self.state[i] + initial_state[i]) % self.modulo
        return self.serialize() 

class Chacha20Encryption:

    @staticmethod
    def encrypt(key, counter, nonce, plaintext):
        encrypted_message = ""
        for j in range(floor(len(plaintext)/64)):
            block = Chacha20Block()
            key_stream = block.chacha20_block(key, counter+j, nonce)
            block_text = plaintext[j*64:j*64+64]
            for i in range(j*64, j+64, 1):
                hex_char = utils.to_2hex(block_text[i])
                key_char = key_stream[i*2:i*2+2] 
                encrypted_message += str(utils.to_2hex(int(hex_char, 16) ^ int(key_char, 16)))[2:]
        if len(plaintext) % 64 != 0:
            j = floor(len(plaintext)/64)
            block = Chacha20Block()
            key_stream = block.chacha20_block(key, counter+j, nonce)
            block_text = plaintext[j*64:len(plaintext)]
            for i in range(0, len(plaintext) % 64, 1):
                hex_char = utils.to_2hex(block_text[i])
                key_char = key_stream[i*2:i*2+2]
                encrypted_message += str(utils.to_2hex(int(hex_char, 16) ^ int(key_char, 16)))[2:]
        return utils.hex_to_ascii(encrypted_message)

        
    @staticmethod
    def decrypt(key, counter, nonce, cipher):
        decrypted_message = ""
        decrypted_message_hex = ""
        for j in range(floor(len(cipher)/64)):
            block = Chacha20Block()
            key_stream = block.chacha20_block(key, counter+j, nonce)
            block_cipher = cipher[j*64:j*64+64]
            for i in range(j*64, j+64, 1):
                hex_char = utils.to_2hex(block_cipher[i])
                key_char = key_stream[i*2:i*2+2] 
                decrypted_message_hex += str(utils.to_2hex(int(hex_char, 16) ^ int(key_char, 16)))[2:]
        decrypted_message += utils.hex_to_ascii(decrypted_message_hex)
        decrypted_message_hex = ""
        if len(cipher) % 64 != 0:
            j = floor(len(cipher)/64)
            block = Chacha20Block()
            key_stream = block.chacha20_block(key, counter+j, nonce)
            block_cipher = cipher[j*64:len(cipher)]
            for i in range(0, len(cipher) % 64, 1):
                hex_char = utils.to_2hex(block_cipher[i])
                key_char = key_stream[i*2:i*2+2]
                decrypted_message_hex += str(utils.to_2hex(int(hex_char, 16) ^ int(key_char, 16)))[2:]
        decrypted_message += utils.hex_to_ascii(decrypted_message_hex)
        return decrypted_message
            

