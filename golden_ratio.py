from decimal import Decimal, getcontext, ROUND_HALF_EVEN
from decimal import Context
import time
import matplotlib.pyplot as plt

getcontext().prec = 100
getcontext().rounding = ROUND_HALF_EVEN


def fib_golden_ratio(n):
    if n == 0:
        return 0
    if n == 1 or n == 2:
        return 1

    ctx = Context(prec=100, rounding=ROUND_HALF_EVEN)

    phi = (Decimal(1) + Decimal(5).sqrt()) / 2

    return int(
        (Decimal(phi) ** Decimal(n) / Decimal(5).sqrt())
        .to_integral_value(rounding=ROUND_HALF_EVEN)
    )


n_values = [
    501, 631, 794, 1000, 1259, 1585, 1995, 2512,
    3162, 3981, 5012, 6310, 7943, 10000, 12589, 15849
]

execution_times = []

print(f"{'n':>7} | {'Time (s)':>12}")
print("-" * 22)

for n in n_values:
    start = time.perf_counter()
    fib_golden_ratio(n)
    end = time.perf_counter()

    t = end - start
    execution_times.append(t)

    print(f"{n:>7} | {t:>12.6f}")

plt.figure(figsize=(10, 5))
plt.plot(n_values, execution_times, marker='o')
plt.xlabel("n-th Fibonacci term")
plt.ylabel("Time (seconds)")
plt.title("Golden Ratio Approximation Fibonacci Performance")
plt.grid(True)
plt.show()
