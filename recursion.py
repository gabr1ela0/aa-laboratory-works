import time
import matplotlib.pyplot as plt

def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# Input values
n_values = [5, 7, 10, 12, 15, 17, 20, 22, 25, 27, 30, 32, 35, 37, 40, 42, 45]

# Table
execution_times = []

print(f"{'n':>5} | {'Time (s)':>10}")
print("-" * 20)

for n in n_values:
    start = time.time()
    fibonacci(n)
    end = time.time()
    exec_time = end - start
    execution_times.append(exec_time)
    print(f"{n:>5} | {exec_time:>10.2f}")

# Plotting the graph
plt.figure(figsize=(10,6))
plt.plot(n_values, execution_times, marker='o')
plt.title("Recursive Fibonacci Function")
plt.xlabel("n-th Fibonacci Term")
plt.ylabel("Time (seconds)")
plt.grid(True)
plt.show()
