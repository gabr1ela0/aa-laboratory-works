from decimal import Decimal, Context, ROUND_HALF_EVEN
import time
import matplotlib.pyplot as plt

def fibonacci(x):
    ctx = Context(prec=60, rounding=ROUND_HALF_EVEN)
    phi = Decimal((1 + Decimal(5).sqrt()))
    phi2 = Decimal((1 - Decimal(5).sqrt()))
    return int((ctx.power(phi, Decimal(x)) - ctx.power(phi2, Decimal(x))) / (2 ** x * Decimal(5).sqrt()))

n_values = [501, 631, 794, 1000, 1259, 1585, 1995, 2512, 3162,
            3981, 5012, 6310, 7943, 10000, 12589, 15849]

execution_times = []

print(f"{'n':>7} | {'Time (s)':>12}")
print("-" * 22)

for n in n_values:
    start = time.perf_counter()
    fibonacci(n)
    end = time.perf_counter()
    exec_time = end - start
    execution_times.append(exec_time)
    print(f"{n:>7} | {exec_time:>12.6f}")

plt.figure(figsize=(12,6))
plt.plot(n_values, execution_times, marker='o')
plt.title("Binet Formula Fibonacci Function")
plt.xlabel("n-th Fibonacci Term")
plt.ylabel("Time (seconds)")
plt.grid(True)
plt.show()
