# ECC 

## 1. Introduction

This lab contains two parts:
- First, the implementation of X25519 key exchange, in accordance with RFC7748
- Second, the implementation of lenstra's ECM integer factorization method

## 2. Requirements

-  python3

## 3. Implementation

The code is structured as follows:
- **X25519.py** is the imlpementation of X25519 key exchange using the Montgomery ladder.
- **test_X25519.py** is the file to run to test the X25519 key exchange. It outputs on the screen.
- **factoring.py** is the implementation of lenstra's ECM integer factorization method.
- **test_factoring.py** is the file to run to test lenstra's ECM integer factorization method implementation. It uses `challenge/leo-berton.chall` and outputs on a file located at `results/challenge-N.result`

__To check my final results, the file with all the details is `results/challenge.results`.__
I only managed to factor 8/12 numbers (failed to factor the last ones or lack of time).

## 5. How to use
```
python3 test_X25519.py
python3 test_factoring.py
```
