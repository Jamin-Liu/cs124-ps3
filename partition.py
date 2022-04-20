from operator import ilshift
import sys
import random
import math
import sys
import numpy as np
from torch import R

A = [10, 8, 7, 6, 5]

#############################
# HEAP CLASS AND OPERATIONS #
#############################
class max_heap:

    def __init__(self, maxsize):
        self.maxsize = maxsize
        self.size = 0
        self.heap = [0] * (self.maxsize + 1)
        self.heap[0] = sys.maxsize
        self.front = 1
    
    # Parent of node currently at pos
    def parent(self, pos):
        return pos // 2
    
    # Left child of node currently at pos
    def left_child(self, pos):
        return 2 * pos
    
    # Right child of node currently at pos
    def right_child(self, pos):
        return (2 * pos) + 1

    # Length of array
    def 

    #


######################################
# NUMBER PARTITION GENERAL FUNCTIONS #
######################################
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
    n = len(A)
    
    P = []
    for i in range(n):
        P.append(random.randint(1, n))
    
    A_prime = [0] * n 
    for i in range(n):
        A_prime[P[i]-1] = A_prime[P[i]-1] + A[i]

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


# Karmarkar-Karp Function

def karmarkar_karp(H):
    for i in range(H.size()):
        max = H.replace_max(0)
        max_p = H.peek()
        _ = H.replace_max(max - max_p)
    return H.peek()
# 

def 

def max_heapify(A):
    

# Build a max heap from an input array
def build_heap(A):
    n = len(A)
    H = [0] * (n + 1)
    H[0] = sys.maxsize

    for i in range(n):
        H[i+1] = A[i]
    
    for i in range(len(H)/2, 0, -1):
        max_heapify(i)

    return H

# need to build max heap
# need to build extract max function
# def construct_heap():
#     H = []
#     for i in range(100):
#         H.append(random.randint(1, sys.maxsize))

# 






# System Outputs
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