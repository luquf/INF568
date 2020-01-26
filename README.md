# INF568 Shake128 implementation and collisions

## 1. Introduction

This implementation is following the FIPS202 standard. It was developed for the module INF568 Advanced Cryptology.

## 2. Requirements

- __python3__
- __hashlib__

## 3. Implementation

I chose python as it it faster to implement and easier to debug (debugging was still not fun). Still, the implementation is not very fast compared to what could be done in C.

- __code/shake128.py__ implementation of the shake128 hash function
- __code/bruteforce.py__ implementation of a brute force algorithm to find collisions
- __code/floyd.py__ implementation of Floyd's algorithm to find collisions
- __code/verify_collisions.py__ scripts that verifies the collisions I found

- __collisions-N/ex-i.1__ file containing the first image of the collision
- __collisions-N/ex-i.2__ file containing the second image of the collision


Example hashing with 32 ouput bytes:
```
python3 shake128.py 32 < /dev/null
7f9c2ba4e88f827d616045507605853ed73b8093f6efbc88eb1a6eacfa66ef26
```

## 4. Collisions

To find collisions on binary data including my email, I chose the format "email password" (e.g. leo.berton@polytechnique.edu dj734yhue6). I also choose to use the python hashlib implementation as it is way faster than my implementation...

I implemented a first brute force algorithm, which hashed the data (the password was generated randomly on a predefined number of bytes) and stored it in a dict(). It worked well for small output length (up to 5/6), but after it crashed my computer as the ram was totally full.

So I also implemented the collision search using Floyd's algorithm which was less greedy in term of memory.

I found collisions up to 8 bytes of output.

The time to find collisions was growing exponentially as the output length is growing. The following values are sample values of the time my code takes to find th first collision:

- N = 1 => 0.00021 sec (brute force)
- N = 2 => 0.002 sec (brute force)
- N = 3 => 0.016 sec (brute force)
- N = 4 => 0.15 sec (brute force)
- N = 5 => 4 sec (brute force)
- N = 6 => 173 sec (brute force)
- N = 7 => 1208 sec (floyd)
- N = 8 => 3960 sec (floyd)

## 5. How to use

```
python3 shake128.py output_length < stream.txt
python3 bruteforce.py output_length number_of_appended_bytes
python3 floyd.py output_length
