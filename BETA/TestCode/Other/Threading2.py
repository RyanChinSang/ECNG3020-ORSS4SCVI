import threading
from queue import Queue
import time


def exampleJob():
    time.sleep(0.5)  # pretend to do some work.


def threader():
    while True:
        q.get()  # works without this line - gets the items's number
        exampleJob()
        q.task_done()


q = Queue()
start = time.time()
for x in range(10):
    threading.Thread(target=threader, args=(), daemon=True).start()
for worker in range(20):
    q.put(worker)
q.join()

print('Entire job took:', time.time() - start)

# time_taken ~= (#_workers / #_threads) * time_for_job
# time_taken ~= (#_items_in_source / #_worker_threads) * time_for_job
