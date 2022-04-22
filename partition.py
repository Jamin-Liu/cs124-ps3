import sys
import random
import math
import heapq

##########################
# READING THE INPUT FILE #
##########################

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
        
        for i in range(int(self.size()/2), 0, -1):
            self.max_heapify(i)

        return self.heap
    
    # Swap two nodes at i and j
    def swap(self, i, j):
        self.heap[i], self.heap[j] = (self.heap[j], self.heap[i])

    # Parent of node 
    def parent(self, child):
        if child == 1:
            return -1
        return child / 2    
        
    # Left child of node
    def left_child(self, parent):
        if parent > (self.size() / 2):
            return -1
        return parent * 2

    # Right child of node
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
    
    # Access the first element of the heap
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
    S_p = S.copy()
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


# Repeated random function
def repeated_random(A, iter):
    S = generate_random_solution(A)
    for _ in range(iter):
        S_p = generate_random_solution(A)
        if calculate_residue(A, S_p) < calculate_residue(A, S):
            S = S_p 
    return calculate_residue(A, S)


# Hill climbing function
def hill_climbing(A, iter):
    S = generate_random_solution(A)
    min_res = calculate_residue(A, S)
    for _ in range(iter):
        S_p = generate_random_neighbor(S)
        res_S_p = calculate_residue(A, S_p)
        if res_S_p < min_res:
            min_res = res_S_p
    return min_res


# Simulated annealing function
def simulated_annealing(A, iter):
    S = generate_random_solution(A)
    S_pp = S
    for i in range(iter):
        S_p = generate_random_neighbor(S)
        res_S = calculate_residue(A, S)
        res_S_p = calculate_residue(A, S_p)
        if res_S_p < res_S:
            S = S_p
        else:
            prob = math.exp(-1 * (res_S_p - res_S) / (10 ** 10) * (0.8 ** (i/300)))
            if random.random() < prob:
                S = S_p
        if calculate_residue(A, S) < calculate_residue(A, S_pp):
            S_pp = S
            
    return calculate_residue(A, S_pp)


# Generate random partition
def generate_random_partition(A):
    n = len(A)
    P = []
    for _ in range(n):
        P.append(random.randint(1, n))
    return P


# Generate random neighbor to partition P
def generate_random_neighbor_partition(P):
    P_p = P.copy()
    n = len(P)
    i = random.randint(1, n)
    j = P[i - 1]
    while j == P[i - 1]:
        j = random.randint(1, n)
    P_p[i - 1] = j
    return P_p


# Prepartioning method
def prepartition(A, P):
    n = len(A)
    A_p = [0] * n 
    for i in range(n):
        A_p[P[i]-1] = A_p[P[i]-1] + A[i]
    return A_p


def prepartition_calculate_residue(A, P):
    A_p = prepartition(A, P)
    return karmarkar_karp(A_p)


# Repeated random function (pre-partition version)
def prepartition_repeated_random(A, iter):
    P = generate_random_partition(A)
    A_p = prepartition(A, P)
    min_res = karmarkar_karp(A_p)
    for _ in range(iter):
        P_p = generate_random_partition(A)
        A_pp = prepartition(A, P_p)
        res_A_pp = karmarkar_karp(A_pp) 
        if res_A_pp < min_res:
            min_res = res_A_pp
    return min_res
    

# Hill climbing function (pre-partition version)
def prepartition_hill_climbing(A, iter):
    P = generate_random_partition(A)
    A_p = prepartition(A, P)
    min_res = karmarkar_karp(A_p)
    for _ in range(iter):
        P_p = generate_random_neighbor_partition(P)
        A_pp = prepartition(A, P_p)
        res_A_pp = karmarkar_karp(A_pp) 
        if res_A_pp < min_res:
            min_res = res_A_pp
    return min_res


# Simulated annealing function (pre-partition version)
def prepartition_simulated_annealing(A, iter):
    P = generate_random_partition(A)
    P_copy = P
    for i in range(iter):
        P_p = generate_random_neighbor_partition(P)
        res_A_p = prepartition_calculate_residue(A, P)
        res_A_pp = prepartition_calculate_residue(A, P_p)
        if res_A_pp < res_A_p :
            P = P_p
        else:
            prob = math.exp(-1 * (res_A_pp - res_A_p) / (10 ** 10) * (0.8 ** (i/300)))
            if random.random() < prob:
                P = P_p
        if prepartition_calculate_residue(A, P) < prepartition_calculate_residue(A, P_copy):
            P_copy = P
            
    return prepartition_calculate_residue(A, P_copy)


    # P = generate_random_solution(A)
    # P_copy = P.copy()
    # for i in range(iter):
    #     A_p = prepartition(A, P)
    #     P_p = generate_random_neighbor_partition(P)
    #     A_pp = prepartition(A, P_p)
    #     res_A_pp = karmarkar_karp(A_pp)
    #     res_A_p = karmarkar_karp(A_p)
    #     if res_A_pp < res_A_p :
    #         P = P_p
    #     else:
    #         prob = math.exp(-1 * (res_A_pp - res_A_p) / (10 ** 10) * (0.8 ** (i/300)))
    #         if random.random() < prob:
    #             P = P_p
    #     A_pcopy = A_p = prepartition(A, P_copy)
    #     if res_A_p < karmarkar_karp(A_pcopy):
    #         P_copy = P
            
    # A_final = prepartition(A, P_copy)
    # return karmarkar_karp(A_final)


# Karmarkar-Karp Function
def karmarkar_karp(A):
    H = max_heap()
    H.build_heap(A)
    for _ in range(H.size()):
        max = H.replace_max(0)
        max_p = H.peek()
        _ = H.replace_max(max - max_p)
    return H.peek()


################
# SYSTEM CALLS #
################

# A = [10, 8, 7, 6, 5]
# iter = 15
# print(prepartition_simulated_annealing(A, iter))

# Flag 0
if int(sys.argv[1]) == 0:

    A = build_array(sys.argv[3])
    #A = [10, 8, 7, 6, 5]
    iter = 10000

    # Karmarkar Karp
    if int(sys.argv[2]) == 0:
        print(karmarkar_karp(A))

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