# Below is a simple example of a CPU-bound program that performs a computation using multiple threads. However, due to the presence 
# of the Global Interpreter Lock (GIL), the multithreading won't provide significant performance improvement compared to a single-threaded version:

# Even though we're using multiple threads in the multi-threaded version, due to the GIL, only one thread can execute Python bytecode at a 
# time. Therefore, the multithreaded version won't provide a significant performance improvement over the single-threaded version for CPU-bound 
# tasks. The output will demonstrate that the multi-threaded version doesn't achieve the expected speedup.

import threading
import time

# Function to perform a CPU-bound task
def cpu_bound_task():
    result = 0
    for _ in range(10**7):
        result += 1
    return result

# Function to execute CPU-bound task using multiple threads
def run_threads(num_threads):
    threads = []
    start_time = time.time()

    # Create and start threads
    for _ in range(num_threads):
        thread = threading.Thread(target=cpu_bound_task)
        thread.start()
        threads.append(thread)

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    end_time = time.time()
    print(f"{num_threads} threads took {end_time - start_time} seconds.")

if __name__ == "__main__":
    print("Starting single-threaded version:")
    run_threads(1)  # Single-threaded version

    print("\nStarting multi-threaded version:")
    run_threads(4)  # Multi-threaded version with 4 threads