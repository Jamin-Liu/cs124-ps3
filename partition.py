import random
A = [10, 8, 7, 6, 5]

generate_random_solution(A):
    S = []
    for i in len(A):
        sign = 1 if random.random() < 0.5 else -1
        S.append(sign)
    return S