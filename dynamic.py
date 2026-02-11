import time
import matplotlib.pyplot as plt

def fibonacci(n):
    if n <= 1:
        return n

    A = [0] * (n + 1)
    A[0] = 0
    A[1] = 1
    for i in range(2, n + 1):
        A[i] = A[i-1] + A[i-2]
    return A[n]


n_values = [501, 631, 794, 1000, 1259, 1585, 1995, 2512, 3162,
            3981, 5012, 6310, 7943, 10000, 12589, 15849]

execution_times_dp = []

print(f"{'n':>7} | {'Time (s)':>12}")
print("-" * 22)

for n in n_values:
    start = time.perf_counter()
    fibonacci(n)
    end = time.perf_counter()
    exec_time = end - start
    execution_times_dp.append(exec_time)
    print(f"{n:>7} | {exec_time:>12.6f}")

plt.figure(figsize=(12,6))
plt.plot(n_values, execution_times_dp, marker='o', color='green')
plt.title("Dynamic Programming Fibonacci Function")
plt.xlabel("n-th Fibonacci Term")
plt.ylabel("Time (seconds)")
plt.grid(True)
plt.legend()
plt.show()
