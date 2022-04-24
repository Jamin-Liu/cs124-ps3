import sys
import random
import math
import bisect
import statistics
import time
import matplotlib.pyplot as plt
from numpy import extract, test


##########################
# READING THE INPUT FILE #
##########################

def build_array(filename):
    f = open(filename, "r")
    A = [int(f.readline().strip('\n')) for i in range(100)]
    return A
    

###################
# HEAP OPERATIONS #
###################

def insertion_sort(A):
    for i in range(1, len(A)):
        temp = A[i]
        j = i-1
        while j >= 0 and temp < A[j]:
            A[j + 1] = A[j]
            j -= 1
        A[j + 1] = temp
    

def insert(A, elt):
    bisect.insort_left(A, elt) # Approved library by Adam!


def extract_max(A):
    return A.pop(-1)


def build_heap(A):
    insertion_sort(A)


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


# Karmarkar-Karp Algorithm
def karmarkar_karp(A):
    H = A.copy()
    build_heap(H)
    while len(H) >= 2:
        max = extract_max(H)
        max -= extract_max(H)
        insert(H, max)
    return extract_max(H)


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


# Prepartition residue calculation helper
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


#####################
# GRAPHS AND TABLES #
#####################

def generate_random_problem(size):
    A = []
    for _ in range(size):
        A.append(random.randint(1, 10 ** 12))
    return A


def print_stats(lst):
    print("Residues: ")
    print(lst)
    print("Mean: " + str(sum(lst) / len(lst)))
    print("Max: " + str(max(lst)))
    print("Min: " + str(min(lst)))
    print("Standard Deviation: " + str(statistics.stdev(lst)))
    print("\n\n")


def test_karmarkar_karp(tests):
    residues = []
    for A in tests:
        residues.append(karmarkar_karp(A))
    print("karmarkar_karp:")
    print("\n")
    print_stats(residues)
    

def test_algorithm(tests, alg):
    residues = []
    for A in tests:
        residues.append(alg(A, 25000))
    print(alg.__name__ + ":")
    print("\n")
    print_stats(residues)

    
def graph_karmarkar_karp():
    times = []
    sizes = []

    for i in range(50, 550, 50):

        time_alg = 0

        for _ in range(50):
            A = generate_random_problem(i)
            start = time.time()
            _ = karmarkar_karp(A)
            end = time.time()
            time_alg += (end - start)

        time_alg /= 50
        time_alg *= 1000

        times.append(time_alg)
        sizes.append(i)

    plt.plot(sizes, times)
    plt.title("Karmarkar Karp: Run Time")        
    plt.ylabel("Average Run Time (milliseconds)")
    plt.xlabel("Array Size")
    plt.savefig("times_karmarkar_karp" + ".png")
    plt.subplots_adjust(left=0.5)
    plt.show()


def graph_alg(alg, name):
    times = []
    sizes = []

    for i in range(50, 550, 50):

        time_alg = 0

        for _ in range(20):
            A = generate_random_problem(i)
            start = time.time()
            _ = alg(A, 25000)
            end = time.time()
            time_alg += (end - start)

        time_alg /= 20
        time_alg *= 1000

        times.append(time_alg)
        sizes.append(i)

    plt.plot(sizes, times)
    plt.title(name + ": Run Time")
    plt.ylabel("Average Run Time (milliseconds)")
    plt.xlabel("Array Size")
    plt.savefig("time_" + (alg.__name__) + ".png")
    plt.subplots_adjust(left=0.5)
    plt.show()


def runtime_karmarkar_karp():
    time_alg = 0

    for _ in range(50):
        A = generate_random_problem(100)
        start = time.time()
        _ = karmarkar_karp(A)
        end = time.time()
        time_alg += (end - start)

    time_alg /= 50
    time_alg *= 1000
    print("Average Runtime karmark_karp: " + str(time_alg))


def runtime_alg(alg):
    time_alg = 0

    for _ in range(50):
        A = generate_random_problem(100)
        start = time.time()
        _ = alg(A, 25000)
        end = time.time()
        time_alg += (end - start)

    time_alg /= 50
    time_alg *= 1000
    print("Average Runtime " + alg.__name__ + ": " + str(time_alg))


################
# SYSTEM CALLS #
################

# Flag 0 - Standard Run
if int(sys.argv[1]) == 0:

    A = build_array(sys.argv[3])
    iter = 25000

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


# Flag 1 -Graphs and Tables
if int(sys.argv[1]) == 1:
    tests = []
    for _ in range(15):
        tests.append(generate_random_problem(100))

    test_karmarkar_karp(tests)
    test_algorithm(tests, repeated_random)
    test_algorithm(tests, hill_climbing)
    test_algorithm(tests, simulated_annealing)
    test_algorithm(tests, prepartition_repeated_random)
    test_algorithm(tests, prepartition_hill_climbing)
    test_algorithm(tests, prepartition_simulated_annealing)

    graph_karmarkar_karp()
    graph_alg(repeated_random, "Repeated Random")
    graph_alg(hill_climbing, "Hill Climbing")
    graph_alg(simulated_annealing, "Simulated Annealing")
    graph_alg(prepartition_repeated_random, "Prepartition Repeated Random")
    graph_alg(prepartition_hill_climbing, "Prepartition Hill Climbing")
    graph_alg(prepartition_simulated_annealing, "Prepartition Simulated Annealing")

    runtime_karmarkar_karp()
    runtime_alg(repeated_random)
    runtime_alg(hill_climbing)
    runtime_alg(simulated_annealing)
    runtime_alg(prepartition_repeated_random)
    runtime_alg(prepartition_hill_climbing)
    runtime_alg(prepartition_simulated_annealing)