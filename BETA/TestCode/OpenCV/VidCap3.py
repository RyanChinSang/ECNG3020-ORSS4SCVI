from __future__ import print_function
from threading import Thread
import sys
import cv2
import numpy as np


class VideoStream:
    def __init__(self, src=None, height=None, width=None, ratio=None):
        cv2.setUseOptimized(True)
        if src is None:
            camera_list = []
            for i in range(10):
                cap = cv2.VideoCapture(i)
                if cap.isOpened():
                    camera_list += [i]
                    cap.release()
            if len(camera_list) == 1:
                src = camera_list[0]
            elif len(camera_list) == 0:
                src = -1
                print('NOTICE: There were no detected working cameras for indexes 0 to 10!')
            else:
                src = camera_list[0]
                msg = 'NOTICE: There are ' + str(len(camera_list) - 1) \
                      + ' other operational camera source(s) available: ' + str(camera_list[1:])
                print(msg.replace('are', 'is')) if len(camera_list) - 1 == 1 else print(msg)
        self.avg = np.array([])
        self.freq = cv2.getTickFrequency()
        self.begin = 0
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
        self.begin = cv2.getTickCount()
        return (not self.released), self.resize(frame=self.frame, width=width, height=height, ratio=ratio)

    def release(self):
        self.stream.release()
        self.released = True

    def isOpened(self):
        return not self.released

    def fps(self):
        self.avg = np.append(self.avg, (self.freq / (cv2.getTickCount() - self.begin)))
        return self.avg[-1]

    def avg_fps(self):
        self.avg = np.append(self.avg, (self.freq / (cv2.getTickCount() - self.begin)))
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
    # cap = cv2.VideoCapture(0)
    cap = VideoStream().start()
    # cap = VideoStream(height=360, ratio=(16 / 9)).start()
    # cap = VideoStream(width=1280).start()  # Camera feed: 640*480 (default) -- WARNING (good)
    # cap = VideoStream(width=1280, height=720).start()  # Camera feed: 1280*720
    # cap = VideoStream(width=512, height=512).start()  # Camera feed: 640*480
    # cap = VideoStream(width=480, ratio=(16/9)).start()  # Camera feed: 424*240
    # cap = VideoStream(width=480, ratio=(4/3)).start()  # Camera feed: 640*360
    # cap = VideoStream(width=640, ratio=(4/3)).start()  # Camera feed: 640*480
    while cap.isOpened():
        # FPS CASE A
        # print('{:.2f}'.format(cap.fps()))
        # print('{:.2f}'.format(cap.avg_fps()))
        ret, frame = cap.read()
        # ret, frame = cap.read(width=512)  # Window size: 512*384
        # ret, frame = cap.read(height=512)  # Window size: 683*512
        # ret, frame = cap.read(width=512, ratio=1)  # Window size: 512*512
        # ret, frame = cap.read(height=480, ratio=(16/9))  # Window size: 854*480
        # ret, frame = cap.read(width=1280, height=720)  # Window size: 1280*720
        # ret, frame = cap.read(width=1280, height=720, ratio=(4/3))  # Window size: [Camera feed] -- WARNING (good)
        # ret, frame = cap.read(width=1280, height=720, ratio=(16/9))  # Window size: 1280*720
        # print(frame.shape[:2])
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
        # FPS CASE B
        print('{:.2f}'.format(cap.fps()))
        # print('{:.2f}'.format(cap.avg_fps()))
    cv2.destroyAllWindows()


'''
Changelog:

07.11.17 (v1.3)
1- Renamed stop() to release() to conform with cv2.VideoCapture()'s release function
2- Added a 'pass' when no conditions were set for read() and start() to prevent the coded 'WARNING-default' message
3- Added the boolean self.grabbed to the return of read() - conform with cv2.VideoCapture()
4- Change the value of read() independently of stream.read() upon release() (independent of stream.release())
5- Allow the possibility of letting the whole loop run completely of whether the camera is active, or not
6- Specify exactly what is being imported by default for use in the VideoStream class;
    a. Added setUseOptimized for openCV (may be an improvement)
7- Renamed self.release to self.released to avoid name collision
8- Added isOpened() to conform with cv2.VideoCapture()

15.11.17 (v.1.4)
1- Added new functions fps() and avg_fps() for displaying the current fps, and average fps respectively
   a. Added import numpy library
   b. Added initialization for class variables:
      i. self.freq
     ii. self.start
         A. is initialized as 0 so as to ensure the first value is very small REF: FPS CASE A
            I. This ensures that the average fps is not out-of-whack for the first few seconds of runtime due to a large
               number causing  inaccurate fps averages for that time.
         B. is updated with every read() call
    iii. self.avg
   NB1: For FPS CASE B, the first and last values of fps() are significantly lower when the loop starts and ends 
        (pressing 'q') respectively.
   NB2: #1.b.ii.A.I. is only the case when avg_fps() or fps() is called before the first read() in the local loop
   NB3: In consideration of these notes, fps() and avg_fps() needs to be called at the right time. Else, the results
        will be incorrect.
2- Cleaned up some redundant language in config() (matches what was coded for resize())

16.11.17 (v1.5)
1- Added full support for Python 2
   NB1: The Python 3 implementation is slightly faster

30.11.17 (v1.6)
1- Added a searching method to find all working video source(s)
   NB1: This is especially useful if the only working video source is not indexed as 0
   NB2: It will always use the first working video source
2- Renamed inconsistencies between documented self.start and coded self.s, to self.begin
'''