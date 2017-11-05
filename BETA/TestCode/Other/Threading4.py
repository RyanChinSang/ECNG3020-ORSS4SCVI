from threading import Thread
from six.moves import input

import cv2

cap = cv2.VideoCapture(0)
a_list = []


def input_thread(a_list):
    val = input()
    if val == 'a':
        Thread(target=a, args=(), daemon=True).start()
    elif val == 'b':
        Thread(target=b, args=(), daemon=True).start()
    else:
        a_list.append(True)


def do_stuff():
    Thread(target=input_thread, args=(a_list,), daemon=True).start()
    while not a_list:
        _, img = cap.read()
        cv2.imshow("img", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


def a():
    print("task a!")
    Thread(target=input_thread, args=(a_list,), daemon=True).start()


def b():
    print('task b!')
    Thread(target=input_thread, args=(a_list,), daemon=True).start()


do_stuff()
cap.release()
cv2.destroyAllWindows()
