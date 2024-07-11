# Numba is an open-source JIT (Just-In-Time) compiler that translates a subset of Python and NumPy code into fast machine code using LLVM (Low-Level Virtual Machine). 
# JIT Compilation: Numba can compile Python functions at runtime to machine code, which can significantly improve execution speed.

import numba
import numpy as np
import time

# Define a function to be accelerated
@numba.jit
def sum_array(arr):
    total = 0
    for i in range(len(arr)):
        total += arr[i]
    return total

# Create a large NumPy array
array = np.random.rand(100000000)

# Measure the time taken by the Numba-accelerated function
start_time = time.time()
result = sum_array(array)
end_time = time.time()
print("Result:", result)
print("Time taken with Numba:", end_time - start_time)

# Define the same function without Numba for comparison
def sum_array_no_numba(arr):
    total = 0
    for i in range(len(arr)):
        total += arr[i]
    return total

# Measure the time taken by the non-Numba function
start_time = time.time()
result = sum_array_no_numba(array)
end_time = time.time()
print("Result:", result)
print("Time taken without Numba:", end_time - start_time)
