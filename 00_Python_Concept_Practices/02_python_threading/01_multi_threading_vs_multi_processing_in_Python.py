import multiprocessing
import threading
import time

"""
Why multi-processoring in small iteration takes more time than multi-threading?

Process vs. Thread: To recap on the differences between process and thread, see the above figure. A process can have one or multiple 
threads. The main difference is that threads share virtual memory, program machine code and file descriptors; processes do not. This 
means spawning multiple processes using the multiprocessing package would require copying these overhead. Imagine we have a big tensor
in memory on which we need to do some parallelizable computations. Using multiprocessing would make the program copy that big tensor 
many times into each spawned sub-processes and thus causing significant decrease in performance. Depending on the number of sub-processes 
spawned and the complexity of the parallelizable computation, this could cause our program to be slower than the original single-threaded 
implementation.
"""

# Function to print the current processor or thread
def print_current_id(id_type):
    if id_type == "process":
        print(f"Current process ID: {multiprocessing.current_process().pid}")
    elif id_type == "thread":
        print(f"Current thread ID: {threading.current_thread().ident}")


# Function to perform a CPU-bound task
def cpu_bound_task(iterations, id_type):
    result = 0
    for _ in range(iterations):
        # print_current_id(id_type)  # Print current ID
        result += 1
    return result

# Function to run CPU-bound task using multiple processes
def run_multiprocessing(num_processes, iterations):
    processes = []
    start_time = time.time()

    # Create and start processes
    for _ in range(num_processes):
        process = multiprocessing.Process(target=cpu_bound_task, args=(iterations, "process"))
        process.start()
        processes.append(process)

    # Wait for all processes to finish
    for process in processes:
        process.join()

    end_time = time.time()
    print(f"{num_processes} processes took {end_time - start_time} seconds.")

# Function to run CPU-bound task using multiple threads
def run_multithreading(num_threads, iterations):
    threads = []
    start_time = time.time()

    # Create and start threads
    for _ in range(num_threads):
        thread = threading.Thread(target=cpu_bound_task, args=(iterations, "thread"))
        thread.start()
        threads.append(thread)

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    end_time = time.time()
    print(f"{num_threads} threads took {end_time - start_time} seconds.")

if __name__ == "__main__":
    #iterations = 10**7  # Number of iterations for CPU-bound task
    iterations = 10**7  # Number of iterations for CPU-bound task

    print("Starting multiprocessing:")
    run_multiprocessing(4, iterations)  # Multi-processing with 4 processes

    print("\nStarting multithreading:")
    run_multithreading(4, iterations)  # Multi-threading with 4 threads
