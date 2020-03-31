# AEAD_Chacha20_Poly1305

## 1. Introduction

The aim of this lab is to implement AEAD_CHACHA20_POLY1305 following the standard RFC8439

## 2. Requirements
- python3 (tested with 3.7.3)

## 3. Implementation

- __chacha20.py__ implementation of chacha20
- __poly1305.py__ implementation of poly1305
- __aead_chacha20_poly1305.py__ aead using chacha20 and poly1305
- __utils.py__ some usefull functions to handle types
- __test_demo.py__ unittest based on the RFC test vectors + a demonstration of the implementation with dumb parameters

## 4. How to use

```
python3 test_demo.py
```
It will output first the demo, and then the result fo the unittests
