import threading


"""
The GIL is a mutex that allows only one thread to execute Python bytecode at a time. This means that even if multiple threads are created, 
only one thread can be actively executing Python code at any given moment.
The GIL ensures thread safety by preventing race conditions that could occur if multiple threads simultaneously accessed and modified Python 
objects.


Impact of GIL:

Since the task performed in count_up() is not CPU-bound enough, the threads spend most of their time waiting for the next iteration of the 
loop, rather than executing Python bytecode.
Consequently, even though multiple threads are created, they don't achieve true parallelism because they don't execute Python bytecode 
concurrently due to the GIL.
As a result, the performance of the multithreaded code won't be significantly different from running the same task in a single thread.

"""


GIL_preventing_task = True

# Function to perform a CPU-bound task
def calculate_sum_of_squares(start, end):
    """
    Since the below task requires the memory to be shared between various threads, GIL will prevent the multi-threading, and
    each thread will be run at a time.
    """
    total = 0
    for i in range(start, end):
        total += i ** 2
    print(f"Thread finished. Sum of squares from {start} to {end-1}: {total}")


# Function to perform a non-CPU-bound task
def print_hello_world(iterations):
    """
    A simple printing task, that does not require the shared memory between multiple-thread. Thus, GIL does not prevent it
    """
    for _ in range(iterations):
        print("Hello, world!")

# ---------------------------------------------------------------------------------------    

# Create and start multiple threads
threads = []
num_threads = 5
num_values = 10**7
values_per_thread = num_values // num_threads

if GIL_preventing_task:
    for i in range(num_threads):
        start = i * values_per_thread
        end = (i + 1) * values_per_thread
        thread = threading.Thread(target=calculate_sum_of_squares, args=(start, end))
        thread.start()
        threads.append(thread)
else:
    for _ in range(num_threads):
        thread = threading.Thread(target=print_hello_world, args=(num_iterations,))
        thread.start()
        threads.append(thread)
# Wait for all threads to finish
for thread in threads:
    thread.join()

print("All threads finished.")