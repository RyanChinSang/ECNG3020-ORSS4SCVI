import threading
from queue import Queue
import time

# print_lock = threading.Lock()


# def exampleJob(worker):
def exampleJob():
    time.sleep(0.5)  # pretend to do some work.
    # print("hi")
    # print(threading.current_thread().name, worker)
    # with print_lock:
    #     print(threading.current_thread().name, worker)


# The threader thread pulls a worker from the queue and processes it
def threader():
    while True:
        # gets a worker from the queue
        # worker = q.get()
        q.get()
        # Run the example job with the available worker in queue (thread)
        # exampleJob(worker)
        exampleJob()
        # completed with the job
        q.task_done()


# Create the queue and threader
q = Queue()
start = time.time()
# how many threads are we going to allow for
for x in range(10):
    # t = threading.Thread(target=threader)
    # # classifying as a daemon, so they will die when the main dies
    # t.daemon = True
    # # begins, must come after daemon definition
    # t.start()
    threading.Thread(target=threader, args=(), daemon=True).start()


# 20 jobs assigned.
for worker in range(20):
    # print("a:" + str(q.__dict__))
    q.put(worker)
    # print("b:" + str(q.__dict__))

# wait until the thread terminates.
q.join()

# with 10 workers and 20 tasks, with each task being .5 seconds, then the completed job
# is ~1 second using threading. Normally 20 tasks with .5 seconds each would take 10 seconds.
print('Entire job took:', time.time() - start)
