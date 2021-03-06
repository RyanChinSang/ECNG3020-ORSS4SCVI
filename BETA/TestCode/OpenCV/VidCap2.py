import cv2
from threading import Thread


class VideoStream:
    def __init__(self, src=0, height=None, width=None, ratio=None):
        self.stream = cv2.VideoCapture(src)
        self.config(dim=None, height=height, width=width, ratio=ratio)
        (self.grabbed, self.frame) = self.stream.read()
        self.stopped = False

    def start(self):
        Thread(target=self.update, args=(), daemon=True).start()
        return self

    def update(self):
        while True:
            if self.stopped:
                return
            (self.grabbed, self.frame) = self.stream.read()

    def read(self, width=None, height=None, ratio=None):
        return self.resize(frame=self.frame, width=width, height=height, ratio=ratio)

    def stop(self):
        self.stream.release()
        self.stopped = True

    def config(self, dim, height, width, ratio):
        if ratio is None:
            if height and width:
                dim = (self.round_up(height), self.round_up(height * float(width / height)))
            else:
                print("WARNING: Insufficient configuration parameters. The default was used.")
        else:
            if height:
                dim = (self.round_up(height), self.round_up(height * float(ratio)))
            elif width:
                dim = (self.round_up(width / float(ratio)), self.round_up(width))
        if dim is not None:
            self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, dim[0])
            self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, dim[1])

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
                    print("WARNING: Window resolution (" + str(width) + "*" + str(height)
                          + ") does not agree with ratio " + str(ratio) + ". The default was used.")
        return cv2.resize(frame, (self.round_up(dim[1]), self.round_up(dim[0])), interpolation=cv2.INTER_AREA)

    @staticmethod
    def round_up(num):
        return int(-(-num // 1))


if __name__ == '__main__':
    # cap = VideoStream().start()
    # cap = VideoStream(width=1280).start()  # Camera feed: 640*480 (default) -- WARNING (good)
    cap = VideoStream(width=1280, height=720).start()  # Camera feed: 1280*720
    # cap = VideoStream(width=512, height=512).start()  # Camera feed: 640*480
    # cap = VideoStream(width=480, ratio=(16/9)).start()  # Camera feed: 424*240
    # cap = VideoStream(width=480, ratio=(4/3)).start()  # Camera feed: 640*360
    # cap = VideoStream(width=640, ratio=(4/3)).start()  # Camera feed: 640*480
    while 1:
        # frame = cap.read()
        # frame = cap.read(width=512)  # Window size: 512*384
        # frame = cap.read(height=512)  # Window size: 683*512
        # frame = cap.read(width=512, ratio=1)  # Window size: 512*512
        frame = cap.read(height=480, ratio=(16/9))  # Window size: 854*480
        # frame = cap.read(width=1280, height=720)  # Window size: 1280*720
        # frame = cap.read(width=1280, height=720, ratio=(4/3))  # Window size: [Camera feed] -- WARNING (good)
        # frame = cap.read(width=1280, height=720, ratio=(16/9))  # Window size: 1280*720
        print(frame.shape[:2])
        # print(str(float(4/3)))
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.stop()
    cv2.destroyAllWindows()
