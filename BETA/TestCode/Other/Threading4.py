import _thread
from six.moves import input

import cv2

cap = cv2.VideoCapture(0)


# def get_feed():
#     _, img = cap.read()
#     cv2.imshow("img", img)


def input_thread(a_list):
    input()
    a_list.append(True)


def do_stuff():
    a_list = []
    _thread.start_new_thread(input_thread, (a_list,))
    while not a_list:
        _, img = cap.read()
        cv2.imshow("img", img)
        # get_feed()
        # print("Waiting for keystroke. . .")


do_stuff()
cap.release()
cv2.destroyAllWindows()
