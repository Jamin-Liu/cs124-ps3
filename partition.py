from operator import ilshift
import sys
import random
import math
import numpy as np
from torch import R

A = [10, 8, 7, 6, 5]


# Function for creating a random solution
def generate_random_solution(A):
    S = []
    for i in range(len(A)):
        sign = 1 if random.random() < 0.5 else -1
        S.append(sign)
    return S


# Function for generating a random neighbor
def generate_random_neighbor(S):
    S_p = S
    n = len(S)
    denominator = n + (n * (n - 1)) / 2
    i = random.randint(0, n - 1)
    S_p[i] *= -1
    prob = n / denominator

    if random.random() > prob:
        j = i
        while j == i:
            j = random.randint(0, n - 1)
        S_p[j] *= -1

    return S_p


# Function for calculating residue
def calculate_residue(A, S):
    if len(A) != len(S):
        print("Error: A and S length mismatch")
        return
    
    residue = 0
    for i in range(len(A)):
        residue += (A[i] * S[i])
    
    return abs(residue)


# Prepartioning method
def prepartition(A, P):
    if len(A) != len(P):
        print("Error: A and P length mismatch")
        return
    
    A_prime = [0] * len(A)
    for i in range(len(A)):
        A_prime[P[i]] = A_prime[P[i]] + A[i]

    return A_prime


# Repeated random function
def repeated_random(A, iter):
    S = generate_random_solution(A)
    for _ in range(iter):
        S_p = generate_random_solution(A)
        if calculate_residue(A, S_p) < calculate_residue(A, S):
            S = S_p 
    return S


# Hill climbing function
def hill_climbing(A, iter):
    S = generate_random_solution(A)
    for _ in range(iter):
        S_p = generate_random_neighbor(S)
        if calculate_residue(A, S_p) < calculate_residue(A, S):
            S = S_p 
    return S


# Simulated annealing function
def simulated_annealing(A, iter):
    S = generate_random_solution(A)
    S_pp = S
    for i in range(iter):
        S_p = generate_random_neighbor(A, S)
        res_S = calculate_residue(A, S)
        res_S_p = calculate_residue(S_p)
        prob = math.exp(-(res_S_p - res_S)/ (pow(10,  10) * pow(0.8, i/300)))
        if res_S_p < res_S or random.rand() < prob:
            S = S_p
        if calculate_residue(A, S) < calculate_residue(A, S_pp):
            S_pp = S
        
    return S_pp


# Repeated random function (pre-partition version)
def prepartition_repeated_random(A, P, iter):
    A_prime = prepartition(A, P)
    return repeated_random(A_prime, iter)
    

# Hill climbing function (pre-partition version)
def prepartition_hill_climbing(A, P, iter):
    A_prime = prepartition(A, P)
    return hill_climbing(A_prime, iter)


# Simulated annealing function (pre-partition version)
def prepartition_simulated_annealing(A, P, iter):
    A_prime = prepartition(A, P)
    return simulated_annealing(A_prime, iter)

if int(sys.argv[2]) == 0:
    # run KK
    pass


if int(sys.argv[2]) == 1:
    # repeated random
    pass


if int(sys.argv[2]) == 2:
    # hill climbing
    pass


if int(sys.argv[2]) == 3:
    # simulated annealing
    pass


if int(sys.argv[2]) == 11:
    # prepartitioned repeated random
    pass


if int(sys.argv[2]) == 12:
    # prepartitioned hill climbing
    pass

if int(sys.argv[2]) == 13:
    # prepartitioned simulated annealing
    pass