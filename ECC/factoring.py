#!/usr/bin/env python3

from math import sqrt, floor, log
from random import randint
from os import path
from X25519 import ladder
from time import time

# cache the primes during factorization
PRIMES_1000000 = []

def trial_division(n):
    factors = {}
    primes = get_primes(bound=1000000)
    for prime in primes:
        exponent = 0
        while n % prime == 0:
            exponent += 1 
            n = n // prime
        if exponent is not 0:
            factors[prime] = exponent
    return factors, n
    

def eratosthenes_sieve(N):
    A = {i:True for i in range(2, N+1)}
    for i in range(2, int(sqrt(N))):
        if A[i] == True:
            k = 0
            j = 0
            while True:
                j = i**2 + k*i
                k += 1
                if j > N:
                    break
                else:
                    A[j] = False
    return [key for key, val in A.items() if val != False]


def gcd(a, b):
    if b > a:
        return gcd(b, a)
    if(b == 0):
        return a
    return gcd(b, a % b)

def is_probable_prime(N, rounds=40):
    if N <= 3:
        return False
    if N % 2 == 0:
        return False
    r = 0
    d = N - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    for i in range(rounds):
        a = randint(2, N-1)
        x = pow(a, d, N)
        if x == 1 or x == N-1:
            continue
        for j in range(r-1):
            x = pow(x, 2, N)
            if x == N-1:
                break
        else:
            return False
    return True


def get_primes(bound=10000):
    if not PRIMES_1000000 == []:
        return primes_1000000
    if not path.isfile('primes/primes-'+str(bound)+'.txt'):
        print("Generating primes...")
        generate_primes(bound=bound)
    f = open("primes/primes-"+str(bound)+".txt", "r")
    data = f.read()
    f.close()
    return [int(val) for val in data.split(";")]

def generate_primes(bound=10000):
    f = open("primes/primes-"+str(bound)+".txt", "w+")
    i = 0
    for val in eratosthenes_sieve(bound):
        if i == 0:
            f.write(str(val))
            i += 1
        else:
            f.write(";"+str(val))
    f.close()
    

def ecm_trial(N, A, Q, bound):
    if gcd(A*A-4, N) != 1:
        return gcd(A*A-4, N) 
    for l in get_primes(bound=1000000):
        if l > bound:
            break
        else:
            k = floor(log(bound, l))
            Q = ladder(pow(l, k, N), Q, p=N, A=A)
    return gcd(Q[1], N)
        

def suyama_random_curve(N):
    sigma = randint(5, N)
    u, v = pow(sigma, 2, N)-5, 4*sigma % N
    Q = (pow(u, 3, N), pow(v, 3, N))
    A = pow(v,3,N) * (3*u+v) * pow(4*v * pow(u, 3, N), N-2, N) - 2 % N 
    return A, Q


def zimmermann_dodson_bound(digits):
    values = {40: 3*pow(10, 6), 
              45: 11*pow(10, 6), 
              50: 43*pow(10, 6), 
              55: 110*pow(10, 6), 
              60: 260*pow(10, 6), 
              65: 850*pow(10, 6)}
    if digits > 65:
        return 850*pow(10, 6)
    for k, v in values.items():
        if int(digits) <= k:
            return v
    return None


def factorization(N):
    start = time()
    factors = {}
    trial_factors, remaining = trial_division(N)
    Q = (1, 0)
    if remaining == 1: # already factored with trial division
        return {"status": "trial", "factors": trial_factors}
    else:
        factors = trial_factors
        N = remaining # what's left from trial division
        upper_bound, current_bound, step, A = 0, 0, 0, 0
        if is_probable_prime(N): # this factor is a prime, so no need to factor it again
            factors[N] = 1
        else: # otherwise, let's factor it
            digits = len(str(N)) # number of digits
            upper_bound = zimmermann_dodson_bound(digits) # getting Zimmermann and dodson bound
            step = upper_bound // 1000 
            for current_bound in range(0, upper_bound+step, step):
                if current_bound >= upper_bound:
                    print("Failed to factor", N)
                    print("Original factors:", factors)
                    exit(0)
                print("Current bound is", str(current_bound), "/", str(upper_bound), " and time elapsed is", time()-start, "seconds")
                A, Q = suyama_random_curve(N) # random curve generation with suyama method
                gcd = ecm_trial(N, A, Q, current_bound) 
                if gcd != 1 and gcd != N: # found the two prime factors
                    factors[N//gcd] = 1 
                    factors[gcd] = 1
                    break
    return {"status": "success", "factors": factors, "upper_bound": upper_bound, "bound": current_bound, "step": step, "time": time()-start, "aparameter": A, "beta": 1000000, "coords": Q}


