import threading
import queue
# from BETA.dev02.test2 import f2

q = queue.Queue()


def f1(a, q):
    return q.put(a + 5)


def f2(a, q):
    a = q.get()
    return q.put(a * 2)


a = 3
# 3+5 = 8
# 8*2 = 16
t1 = threading.Thread(target=f1, args=(a, q)).start()
t2 = threading.Thread(target=f2, args=(a, q)).start()
# q.put(t1.start())
# a = q.get()
# q.put(t2.start())
# a = q.get()

# print(q.__dict__)
print(q.get())

# REF1: https://www.slideshare.net/dabeaz/an-introduction-to-python-concurrency
# REF2: https://stackoverflow.com/questions/15461413/how-to-share-a-variable-between-2-threads
