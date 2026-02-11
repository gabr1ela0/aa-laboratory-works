import time
import matplotlib.pyplot as plt

def multiply(F, M):
    x = F[0][0] * M[0][0] + F[0][1] * M[1][0]
    y = F[0][0] * M[0][1] + F[0][1] * M[1][1]
    z = F[1][0] * M[0][0] + F[1][1] * M[1][0]
    w = F[1][0] * M[0][1] + F[1][1] * M[1][1]
    F[0][0] = x
    F[0][1] = y
    F[1][0] = z
    F[1][1] = w

def power(F, n):
    M = [[1, 1], [1, 0]]
    for _ in range(2, n + 1):
        multiply(F, M)

def fibonacci(n):
    F = [[1, 1], [1, 0]]
    if n == 0:
        return 0
    power(F, n - 1)
    return F[0][0]

n_values = [501, 631, 794, 1000, 1259, 1585, 1995, 2512, 3162,
            3981, 5012, 6310, 7943, 10000, 12589, 15849]

execution_times_matrix = []

print(f"{'n':>7} | {'Time (s)':>12}")
print("-" * 22)

for n in n_values:
    start = time.perf_counter()
    fibonacci(n)
    end = time.perf_counter()
    exec_time = end - start
    execution_times_matrix.append(exec_time)
    print(f"{n:>7} | {exec_time:>12.6f}")

plt.figure(figsize=(12,6))
plt.plot(n_values, execution_times_matrix, marker='o')
plt.title("Matrix Fibonacci Function")
plt.xlabel("n-th Fibonacci Term")
plt.ylabel("Time (seconds)")
plt.grid(True)
plt.show()
