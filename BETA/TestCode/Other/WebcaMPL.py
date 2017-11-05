import cv2
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def grab_frame(cap):
    ret, frame = cap.read()
    return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


# Initiate the two cameras
cap = cv2.VideoCapture(0)
# cap2 = cv2.VideoCapture(0)

# create two subplots
# ax1 = plt.subplot(1, 2, 1)
# ax2 = plt.subplot(1, 2, 2)

# create two image plots
im1 = plt.imshow(grab_frame(cap))
# im2 = ax2.imshow(grab_frame(cap2))


def update(i):
    im1.set_data(grab_frame(cap))
    # im2.set_data(grab_frame(cap2))


ani = FuncAnimation(plt.gcf(), update, interval=1)
# ani = FuncAnimation(plt.gcf(), update)


def close(event):
    if event.key == 'q':
        plt.close(event.canvas.figure)
        cap.release()


cid = plt.gcf().canvas.mpl_connect("key_press_event", close)

plt.show()

# code that should be executed after window is closed.
