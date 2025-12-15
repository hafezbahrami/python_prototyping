# Reference: https://tutswiki.com/python/threading/

# Most examples below are not cpu-limited tasks, so Python can actually do parallel processing using multi-threading

import threading
import time
from time import ctime

flag_multi_threadin_with_join_method = True
# -----------------------------------------------------------------------------------------------------------------------------
# Example 1: 
# (I) if there is no join() method, and all 3 threads can run without waiting any other thread to finish

# (II) What if we want the create a new thread only after the previous one has been completed or stopped? In that case, we use the 
# join() method as below. In this case, if thread0 started, it must finish the job before thread1 starts.
# join() pauses the main thread (for loop in this case) and wait for the running thread to complete.
# thread.join(1), only wait for 1 second.
# -----------------------------------------------------------------------------------------------------------------------------
def myThread_func(num):
    print("Thread %d: started at %s" % (num, ctime(time.time())))
    time.sleep(2)
    print("Thread %d: finished at %s" % (num, ctime(time.time())))

# Creating 3 threads (while the main thread is always running)
for i in range(0, 3):
    print("Creating thread %d at %s" % (i, ctime(time.time())))
    thread = threading.Thread(target=myThread_func, args=(i,))
    print("Starting thread %d at %s" % (i, ctime(time.time())))
    thread.start()
    if flag_multi_threadin_with_join_method:
        thread.join(1)
        print(f"\n Thread {i} alive: {thread.is_alive()} \n")
# -----------------------------------------------------------------------------------------------------------------------------
# Example 2: with join() method

# -----------------------------------------------------------------------------------------------------------------------------


