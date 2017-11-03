import threading
from queue import Queue
import time

print_lock = threading.Lock()


# def exampleJob(worker):
#     time.sleep(0.5)
#     with print_lock:
#         print(threading.current_thread().name, worker)


def exampleJob2():
    time.sleep(0.5)


# def threader():
#     while True:
#         worker = q.get()
#         exampleJob(worker)
#         q.task_done()


# q = Queue()
start = time.time()
for x in range(10):
    # t = threading.Thread(target=threader)
    threading.Thread(target=exampleJob2(), args=(), daemon=True).start()
    # t = threading.Thread(target=exampleJob2())
    # t.daemon = True
    # t.start()
# start = time.time()
# for worker in range(20):
#     q.put(worker)
# q.join()
print('Entire job took:', time.time() - start)
