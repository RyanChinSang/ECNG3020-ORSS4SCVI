import cv2
# import winsound
import multiprocessing as mp
from threading import Thread
from matplotlib import colors
import struct
import numpy as np


class WebcamVideoStream:
    def __init__(self, src=0):
        # initialize the video camera stream and read the first frame
        # from the stream
        self.stream = cv2.VideoCapture(src)
        (self.grabbed, self.frame) = self.stream.read()
        # initialize the variable used to indicate if the thread should
        # be stopped
        self.stopped = False

    def start(self):
        # start the thread to read frames from the video stream
        Thread(target=self.update, args=(), daemon=True).start()
        return self

    def update(self):
        # keep looping infinitely until the thread is stopped
        while True:
            # if the thread indicator variable is set, stop the thread
            if self.stopped:
                return
            # otherwise, read the next frame from the stream
            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
        # return the frame most recently read
        return self.frame

    def stop(self):
        # indicate that the thread should be stopped
        self.stream.release()
        self.stopped = True


# def rgb2name(carr, range):
#     colors_rgb = []
#     r = carr[0]
#     g = carr[1]
#     b = carr[2]
#     l1 = []
#     l2 = []
#     l3 = []
#     for key, value in colors.cnames.items():
#         colors_rgb.append((key, struct.unpack('BBB', bytes.fromhex(value.replace('#', '')))))
#     for val in colors_rgb:
#         if r - range <= val[1][0] <= r + range:
#             l1 += [val]
#     # print("l1: " + str(l1))
#     for val in l1:
#         if g - range <= val[1][1] <= g + range:
#             l2 += [val]
#     # print("l2: " + str(l2))
#     for val in l2:
#         if b - range <= val[1][2] <= b + range:
#             l3 += [val]
#     # print("l3: " + str(l3))
#     # if len(l3) > 1:
#     #     return rgb2name(carr, range - 1)
#     # elif len(l3) == 1:
#     #     return l3[0][0]
#     # else:
#     #     return rgb2name(carr, range + 1)
#     if len(l3) > 1:
#         return rgb2name(carr, range + 1)
#     elif len(l3) == 1:
#         return l3[0][0]
#     else:
#         # return []
#         if len(l2) > 1:
#             return rgb2name(carr, range + 1)
#         elif len(l2) == 1:
#             return l2[0][0]
#         else:
#             if len(l1) > 1:
#                 return rgb2name(carr, range + 1)
#             elif len(l1) == 1:
#                 return l1[0][0]
#             else:
#                 return []


def loop_a():
    # cap = WebcamVideoStream(src=0).start()
    cap = cv2.VideoCapture(0)
    while 1:
        _, frame = cap.read()
        # frame = cap.read()
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        cv2.rectangle(frame, (219, 159), (261, 201), (255, 255, 255), 2)
        r = 0
        g = 0
        b = 0
        for x in range(40):
            for y in range(40):
                r += rgb[160 + x][220 + y][0]
                g += rgb[160 + x][220 + y][1]
                b += rgb[160 + x][220 + y][2]
        avg = np.array([int(round(r / (40 * 40))), int(round(g / (40 * 40))), int(round(b / (40 * 40)))])
        Thread(target=rgb2name, args=(frame, avg, 10), daemon=True).start()
        # print(rgb2name(avg, 10))
        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            # cap.stop()
            cap.release()
            cv2.destroyAllWindows()
            break


def rgb2name(frame, carr, range):
    colors_rgb = []
    r = carr[0]
    g = carr[1]
    b = carr[2]
    l1 = []
    l2 = []
    l3 = []
    for key, value in colors.cnames.items():
        colors_rgb.append((key, struct.unpack('BBB', bytes.fromhex(value.replace('#', '')))))
    for val in colors_rgb:
        if r - range <= val[1][0] <= r + range:
            l1 += [val]
    # print("l1: " + str(l1))
    for val in l1:
        if g - range <= val[1][1] <= g + range:
            l2 += [val]
    # print("l2: " + str(l2))
    for val in l2:
        if b - range <= val[1][2] <= b + range:
            l3 += [val]
    if len(l1) > 1:
        if len(l2) > 1:
            if len(l3) > 1:
                return rgb2name(frame, carr, range - 1)
            elif len(l3) == 1:
                # print(l3[0][0])
                # return l3[0][0]
                # cv2.putText(img=frame,
                #             text=l3[0][0],
                #             org=(0, 15),
                #             fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                #             fontScale=0.5,
                #             color=(255, 255, 255),
                #             thickness=1,
                #             lineType=cv2.LINE_AA,
                #             bottomLeftOrigin=False
                #             )
                Thread(target=printt, args=(frame, l3[0][0]), daemon=True).start()
            else:
                return rgb2name(frame, carr, range - 1)
        elif len(l2) == 1:
            # print(l2[0][0])
            # return l2[0][0]
            # cv2.putText(img=frame,
            #             text=l2[0][0],
            #             org=(0, 15),
            #             fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            #             fontScale=0.5,
            #             color=(255, 255, 255),
            #             thickness=1,
            #             lineType=cv2.LINE_AA,
            #             bottomLeftOrigin=False
            #             )
            Thread(target=printt, args=(frame, l2[0][0]), daemon=True).start()
        else:
            return rgb2name(frame, carr, range - 1)
    elif len(l1) == 1:
        # print(l1[0][0])
        # return l1[0][0]
        # cv2.putText(img=frame,
        #             text=l1[0][0],
        #             org=(0, 15),
        #             fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        #             fontScale=0.5,
        #             color=(255, 255, 255),
        #             thickness=1,
        #             lineType=cv2.LINE_AA,
        #             bottomLeftOrigin=False
        #             )
        Thread(target=printt, args=(frame, l1[0][0]), daemon=True).start()
    else:
        # print([])
        # return []
        # cv2.putText(img=frame,
        #             text=[],
        #             org=(0, 15),
        #             fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        #             fontScale=0.5,
        #             color=(255, 255, 255),
        #             thickness=1,
        #             lineType=cv2.LINE_AA,
        #             bottomLeftOrigin=False
        #             )
        Thread(target=printt, args=(frame, []), daemon=True).start()


def printt(frame, text):
    cv2.putText(img=frame,
                text=text,
                org=(0, 15),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=0.5,
                color=(255, 255, 255),
                thickness=1,
                lineType=cv2.LINE_AA,
                bottomLeftOrigin=False
                )


if __name__ == '__main__':
    mp.set_start_method('spawn')
    mp.Process(target=loop_a).start()
