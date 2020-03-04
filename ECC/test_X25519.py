from X25519 import *
import os


def test_curve25519():
    
    m = decodeScalar25519(hex_to_ascii("a546e36bf0527c9d3b16154b82465edd62144c0ac1fc5a18506a2244ba449ac4"))
    x = decodeUCoordinate(hex_to_ascii("e6db6867583030db3594c1a424b15f7c726624ec26b3353b10a903a6d0ab1c4c"))
    res = X25519(m, x)
    print("#### TEST 1: RFC7748 #####\n")
    print("Input scalar:", "a546e36bf0527c9d3b16154b82465edd62144c0ac1fc5a18506a2244ba449ac4")
    print("Input u-coordinate:", "e6db6867583030db3594c1a424b15f7c726624ec26b3353b10a903a6d0ab1c4c")
    print("Output u-coordinate:", ascii_to_hex(encodeUCoordinate(res))) 
    
    m = decodeScalar25519(hex_to_ascii("4b66e9d4d1b4673c5ad22691957d6af5c11b6421e0ea01d42ca4169e7918ba0d"))
    x = decodeUCoordinate(hex_to_ascii("e5210f12786811d3f4b7959d0538ae2c31dbe7106fc03c3efc4cd549c715a493"))
    res = X25519(m, x)
    print("\n##### TEST 2: RFC7748 #####\n")
    print("Input scalar:", "4b66e9d4d1b4673c5ad22691957d6af5c11b6421e0ea01d42ca4169e7918ba0d")
    print("Input u-coordinate:", "e5210f12786811d3f4b7959d0538ae2c31dbe7106fc03c3efc4cd549c715a493")
    print("Output u-coordinate:", ascii_to_hex(encodeUCoordinate(res)), end="\n\n")


if __name__ == "__main__":
    test_curve25519()
    diffie_hellman()
