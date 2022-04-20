from operator import ilshift
import sys
import random
import math
import sys
import numpy as np
from torch import R

A = [10, 8, 7, 6, 5]

def build_array(filename):
    f = open(filename, "r")
    A = [int(f.readline().strip('\n')) for i in range(100)]
    return A

#############################
# HEAP CLASS AND OPERATIONS #
#############################
class max_heap:

    def __init__(self):
        self.heap = [0] * (101)
        self.heap[0] = sys.maxsize
        self.front = 1

    def size(self):
        return len(self.heap)

    def build_heap(self, A):
        n = len(A)
        self.heap = [0] * (n + 1)
        self.heap[0] = sys.maxsize

        for i in range(n):
            self.heap[i+1] = A[i]
        
        for i in range(self.size()/2, 0, -1):
            self.max_heapify(i)

        return self.heap
    
    # Swap two nodes at i and j
    def swap(self, i, j):
        self.heap[i], self.heap[j] = (self.heap[j], self.heap[i])

    # Parent of node currently at pos
    def parent(self, child):
        if child == 1:
            return -1
        return child / 2    
        
    # Left child of node currently at pos
    def left_child(self, parent):
        if parent > (self.size() / 2):
            return -1
        return parent * 2

    # Right child of node currently at pos
    def right_child(self, parent):
        if parent > (self.size() / 2):
            return -1
        return (parent * 2) + 1

    # Max-Heapify
    def max_heapify(self, pos):
        if pos == 0:
            return
        
        l = self.left_child(pos)
        r = self.right_child(pos)
        
        largest = pos
        size = self.size()
        
        if (l > -1) and (l < size) and (self.heap[l] > self.heap[pos]):
            largest = l
        
        if (r > -1) and (r < size) and (self.heap[r] > self.heap[largest]):
            largest = r
        
        if largest != pos:
            self.swap(largest, pos)
            self.max_heapify(largest)
    
    def peek(self):
        return self.heap[1]
    
    # Replace the maximum 
    def replace_max(self, rep):
        max = self.heap[1]
        self.heap[1] = rep
        self.max_heapify(1)
        
        return max


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
def prepartition(A):
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
def prepartition_repeated_random(A, iter):
    A_prime = prepartition(A)
    return repeated_random(A_prime, iter)
    

# Hill climbing function (pre-partition version)
def prepartition_hill_climbing(A, iter):
    A_prime = prepartition(A)
    return hill_climbing(A_prime, iter)


# Simulated annealing function (pre-partition version)
def prepartition_simulated_annealing(A, iter):
    A_prime = prepartition(A)
    return simulated_annealing(A_prime, iter)


# Karmarkar-Karp Function
def karmarkar_karp(H):
    for i in range(H.size()):
        max = H.replace_max(0)
        max_p = H.peek()
        _ = H.replace_max(max - max_p)
    return H.peek()


# Flag 0
if (sys.argv == 1):

    A = build_array(sys.argv[3])
    iter = 25000

    # Karmarkar Karp
    if int(sys.argv[2]) == 0:
        H = max_heap()
        H.build_heap(A)
        print(karmarkar_karp(H))

    # Repeated Random
    if int(sys.argv[2]) == 1:
        print(repeated_random(A, iter))

    # Hill Climbing
    if int(sys.argv[2]) == 2:
        print(hill_climbing(A, iter))

    # Simulated Annealing
    if int(sys.argv[2]) == 3:
        print(simulated_annealing(A, iter))

    # Prepartitioned Repeated Random
    if int(sys.argv[2]) == 11:
        print(prepartition_repeated_random(A, iter))

    # Prepartitioned Hill Climbing
    if int(sys.argv[2]) == 12:
        print(prepartition_hill_climbing(A, iter))
    
    # Prepartitioned Hill Climbing
    if int(sys.argv[2]) == 13:
        print(prepartition_simulated_annealing(A, iter))