#!/usr/bin/env python3

from chacha20 import *
from poly1305 import *
from aead_chacha20_poly1305 import *
from struct import unpack
from binascii import a2b_hex as hex_to_bytes
from binascii import b2a_hex as bytes_to_hex
from utils import utils
from math import floor
from unittest import TestCase, main

class TestRFC8439(TestCase): 

    def test_chacha20_block(self):
        key = hex_to_bytes("00:01:02:03:04:05:06:07:08:09:0a:0b:0c:0d:0e:0f:10:11:12:13:14:15:16:17:18:19:1a:1b:1c:1d:1e:1f".replace(":", ""))
        nonce = hex_to_bytes("00:00:00:09:00:00:00:4a:00:00:00:00".replace(":", ""))
        initial_counter = 1
        s = Chacha20Block()
        s.chacha20_block(key, initial_counter, nonce)
        self.assertEqual(s.serialize(), "10f1e7e4d13b5915500fdd1fa32071c4c7d1f4c733c068030422aa9ac3d46c4ed2826446079faa0914c2d705d98b02a2b5129cd1de164eb9cbd083e8a2503c4e")
    
    def test_quarter_round(self):
        state = ['0x879531e0', '0xc5ecf37d',  '0x516461b1',  '0xc9a62f8a',
                 '0x44c20ef3', '0x3390af7f',  '0xd9fc690b',  '0x2a5f714c',
                 '0x53372767', '0xb00a5631',  '0x974c541a',  '0x359e9963',
                 '0x5c971061', '0x3d631689',  '0x2098d9d6',  '0x91dbd320']

        res = ['0x879531e0', '0xc5ecf37d', '0xbdb886dc', '0xc9a62f8a',
               '0x44c20ef3', '0x3390af7f', '0xd9fc690b', '0xcfacafd2',
               '0xe46bea80', '0xb00a5631', '0x974c541a', '0x359e9963',
               '0x5c971061', '0xccc07c79', '0x2098d9d6', '0x91dbd320']
        for i in range(len(state)):
            state[i] = int(state[i], 16)
        s = Chacha20Block()
        s.state = state
        s.Qround(2, 7, 8, 13)
        for i in range(len(s.state)):
            s.state[i] = hex(s.state[i]) 
        s1 = Chacha20Block()
        s1.state = res
        self.assertEqual(s.__str__(), s1.__str__())
    
    def test_chacha20_encrypt(self):
        expected_cipher = "6e 2e 35 9a 25 68 f9 80 41 ba 07 28 dd 0d 69 81 e9 7e 7a ec 1d 43 60 c2 0a 27 af cc fd 9f ae 0b f9 1b 65 c5 52 47 33 ab 8f 59 3d ab cd 62 b3 57 16 39 d6 24 e6 51 52 ab 8f 53 0c 35 9f 08 61 d8 07 ca 0d bf 50 0d 6a 61 56 a3 8e 08 8a 22 b6 5e 52 bc 51 4d 16 cc f8 06 81 8c e9 1a b7 79 37 36 5a f9 0b bf 74 a3 5b e6 b4 0b 8e ed f2 78 5e 42 87 4d".replace(" ", "")
        key = hex_to_bytes("00:01:02:03:04:05:06:07:08:09:0a:0b:0c:0d:0e:0f:10:11:12:13:14:15:16:17:18:19:1a:1b:1c:1d:1e:1f".replace(":", ""))
        nonce = hex_to_bytes("00:00:00:00:00:00:00:4a:00:00:00:00".replace(":", ""))
        counter = 1
        text = b"Ladies and Gentlemen of the class of '99: If I could offer you only one tip for the future, sunscreen would be it."
        cipher = Chacha20Encryption.encrypt(key, counter, nonce, text)
        self.assertEqual(utils.ascii_to_hex(cipher), expected_cipher)
        plaintext = Chacha20Encryption.decrypt(key, counter, nonce, hex_to_bytes(utils.ascii_to_hex(cipher)))
        self.assertEqual(text.decode(), plaintext)
    
    
    def test_poly1305(self):
        msg = b"Cryptographic Forum Research Group"
        key = hex_to_bytes('85d6be7857556d337f4452fe42d506a80103808afb0db2fd4abff6af4149f51b')
        ret = Poly1305.poly1305_mac(msg, key)
        self.assertEqual(bytes_to_hex(ret).decode(), "a8:06:1d:c1:30:51:36:c6:c2:2b:8b:af:0c:01:27:a9".replace(":", ""))
    
    def test_chacha20_poly1305_key(self):
        key = hex_to_bytes("80 81 82 83 84 85 86 87 88 89 8a 8b 8c 8d 8e 8f 90 91 92 93 94 95 96 97 98 99 9a 9b 9c 9d 9e 9f".replace(" ", ""))
        nonce = hex_to_bytes("00 00 00 00 00 01 02 03 04 05 06 07".replace(" ", ""))
        one_time_key =  Poly1305.poly1305_key_gen(key, nonce)
        expected = "8a d5 a0 8b 90 5f 81 cc 81 50 40 27 4a b2 94 71 a8 33 b6 37 e3 fd 0d a5 08 db b8 e2 fd d1 a6 46".replace(" ", "")
        self.assertEqual(one_time_key, expected)

    def test_aead_chacha20_poly1305(self):
        text = b"Ladies and Gentlemen of the class of '99: If I could offer you only one tip for the future, sunscreen would be it."
        key = hex_to_bytes("80 81 82 83 84 85 86 87 88 89 8a 8b 8c 8d 8e 8f 90 91 92 93 94 95 96 97 98 99 9a 9b 9c 9d 9e 9f".replace(" ", ""))
        iv = hex_to_bytes("40 41 42 43 44 45 46 47".replace(" ", ""))
        constant = hex_to_bytes("07 00 00 00".replace(" ", ""))
        aad = hex_to_bytes("50 51 52 53 c0 c1 c2 c3 c4 c5 c6 c7".replace(" ", ""))
        cipher, tag = AEAD.chacha20_aead_encrypt(aad, key, iv, constant, text)
        tmp = tag
        self.assertEqual(utils.ascii_to_hex(cipher), "d31a8d34648e60db7b86afbc53ef7ec2a4aded51296e08fea9e2b5a736ee62d63dbea45e8ca9671282fafb69da92728b1a71de0a9e060b2905d6a5b67ecd3b3692ddbd7f2d778b8c9803aee328091b58fab324e4fad675945585808b4831d7bc3ff4def08e4b7a9de576d26586cec64b6116")
        self.assertEqual(bytes_to_hex(tag).decode(), "1a:e1:0b:59:4f:09:e2:6a:7e:90:2e:cb:d0:60:06:91".replace(":", ""))
        plain, tag = AEAD.chacha20_aead_decrypt(aad, key, iv, constant, hex_to_bytes(utils.ascii_to_hex(cipher)))
        self.assertEqual(text.decode(), plain)
        self.assertEqual(bytes_to_hex(tmp).decode(), bytes_to_hex(tag).decode())


class Demo:

    @staticmethod
    def aead_demo():
        # dumb values
        text = b"INF568 - Advanced cypto course was cool"
        key = b"##leo.berton@polytechnique.edu##" 
        iv = b"leo97leo"
        constant = b"1997" 
        aad = b"Palaiseau123"
        print("### AEAD Chacha20 Poly1305 demo ###")
        print("Using dumb values...")
        print("Text to encrypt:", text.decode())
        print("Key:", key.decode())
        print("IV:", iv.decode())
        print("Constant:", constant.decode())
        print("AAD:", aad.decode())
        cipher, tag1 = AEAD.chacha20_aead_encrypt(aad, key, iv, constant, text)
        print("Cipher:", cipher)
        print("Sender tag:", bytes_to_hex(tag1).decode())
        plain, tag2 = AEAD.chacha20_aead_decrypt(aad, key, iv, constant, hex_to_bytes(utils.ascii_to_hex(cipher)))
        print("Decrypted text:", plain)
        print("Receiver tag:", bytes_to_hex(tag2).decode(), end="\n\n")

    

if __name__ == "__main__":
    Demo.aead_demo()
    print("Running unit tests from RFC8439...")
    main()
