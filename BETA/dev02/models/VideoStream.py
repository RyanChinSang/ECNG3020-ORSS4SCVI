from __future__ import print_function
from threading import Thread
import sys
import cv2
import numpy as np


class VideoStream(object):
    def __init__(self, src=0, height=None, width=None, ratio=None):
        cv2.setUseOptimized(True)
        self.s = 0
        self.avg = np.array([])
        self.freq = cv2.getTickFrequency()
        self.stream = cv2.VideoCapture(src)
        self.config(dim=None, height=height, width=width, ratio=ratio)
        (self.grabbed, self.frame) = self.stream.read()
        self.released = not self.grabbed

    def start(self):
        if sys.version[0] == '3':
            Thread(target=self.update, args=(), daemon=True).start()
        else:
            Thread(target=self.update, args=()).start()
        return self

    def update(self):
        while True:
            if self.released:
                return
            (self.grabbed, self.frame) = self.stream.read()

    def read(self, width=None, height=None, ratio=None):
        self.s = cv2.getTickCount()
        return (not self.released), self.resize(frame=self.frame, width=width, height=height, ratio=ratio)

    def release(self):
        self.stream.release()
        self.released = True

    def isOpened(self):
        return not self.released

    def fps(self):
        self.avg = np.append(self.avg, (self.freq / (cv2.getTickCount() - self.s)))
        return self.avg[-1]

    def avg_fps(self):
        self.avg = np.append(self.avg, (self.freq / (cv2.getTickCount() - self.s)))
        return self.avg.mean()

    def config(self, dim, height, width, ratio):
        if ratio is None:
            if height and width:
                dim = (height, (height * float(width / height)))
            elif not height and not width:
                pass
            else:
                print('WARNING: Insufficient configuration parameters. The default was used.')
        else:
            if height:
                dim = (height, (height * float(ratio)))
            elif width:
                dim = ((width / float(ratio)), width)
        if dim:
            self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, self.round_up(dim[0]))
            self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, self.round_up(dim[1]))

    def resize(self, frame, width, height, ratio):
        dim = (dheight, dwidth) = frame.shape[:2]
        if ratio is None:
            if width and height:
                dim = (height, width)
            elif width and height is None:
                dim = ((dheight * (width / dwidth)), width)
            elif width is None and height:
                dim = (height, (dwidth * (height / dheight)))
        else:
            if width is None and height is None:
                dim = (dheight, (dheight * ratio))
            elif width is None and height:
                dim = (height, (height * ratio))
            elif width and height is None:
                dim = ((width / ratio), width)
            else:
                if (width / height) == ratio:
                    dim = (height, width)
                else:
                    print('WARNING: Window resolution (' + str(width) + '*' + str(height)
                          + ') does not agree with ratio ' + str(ratio) + '. The default was used.')
        return cv2.resize(frame, (self.round_up(dim[1]), self.round_up(dim[0])), interpolation=cv2.INTER_AREA)

    @staticmethod
    def round_up(num):
        return int(-(-num // 1))


if __name__ == '__main__':
    cap = VideoStream().start()
    while cap.isOpened():
        ret, frame = cap.read()
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
        print(cap.fps())
    cv2.destroyAllWindows()


'''
To add:
1- Fixes (see below)

To fix:
1- See #1.NB[1-3] in BETA.TestCode.OpenCV.VideoCap3.py

v1.5
'''
