import matplotlib.pyplot as plt

# Input sizes
sizes = [100, 1000, 5000, 10000, 20000, 50000, 100000]

# Execution times
quick = [0.000005, 0.000058, 0.000252, 0.000562, 0.001334, 0.004780, 0.013914]
merge = [0.000007, 0.000074, 0.000367, 0.000777, 0.001737, 0.004766, 0.008740]
heap = [0.000007, 0.000090, 0.000493, 0.001059, 0.002456, 0.006447, 0.012901]
count = [0.000003, 0.000012, 0.000026, 0.000045, 0.000088, 0.000192, 0.000427]

# Function to plot individual algorithm
def plot_single(sizes, times, name):
    plt.figure(figsize=(8,5))
    plt.plot(sizes, times, marker='o')
    #plt.yscale('log')
    plt.xlabel('Array Size')
    plt.ylabel('Execution Time (s, log scale)')
    plt.title(f'{name} Execution Time')
    plt.grid(True, which="both", ls="--", lw=0.5)
    plt.show()

# Plot individual graphs
plot_single(sizes, quick, "QuickSort")
plot_single(sizes, merge, "MergeSort")
plot_single(sizes, heap, "HeapSort")
plot_single(sizes, count, "CountingSort")

# Plot combined graph
plt.figure(figsize=(10,6))
plt.plot(sizes, quick, marker='o', label='QuickSort')
plt.plot(sizes, merge, marker='s', label='MergeSort')
plt.plot(sizes, heap, marker='^', label='HeapSort')
plt.plot(sizes, count, marker='x', label='CountingSort')
#plt.yscale('log')
plt.xlabel('Array Size')
plt.ylabel('Execution Time (s, log scale)')
plt.title('Sorting Algorithms Comparison')
plt.legend()
plt.grid(True, which="both", ls="--", lw=0.5)
plt.show()