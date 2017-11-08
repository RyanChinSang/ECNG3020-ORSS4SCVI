import cv2
from threading import Thread


class VideoStream(object):
    def __init__(self, src=0, height=None, width=None, ratio=None):
        cv2.setUseOptimized(True)
        self.stream = cv2.VideoCapture(src)
        self.config(dim=None, height=height, width=width, ratio=ratio)
        (self.grabbed, self.frame) = self.stream.read()
        self.released = not self.grabbed

    def start(self):
        Thread(target=self.update, args=(), daemon=True).start()
        return self

    def update(self):
        while True:
            if self.released:
                return
            (self.grabbed, self.frame) = self.stream.read()

    def read(self, width=None, height=None, ratio=None):
        return (not self.released), self.resize(frame=self.frame, width=width, height=height, ratio=ratio)

    def release(self):
        self.stream.release()
        self.released = True

    def isOpened(self):
        return not self.released

    def config(self, dim, height, width, ratio):
        if ratio is None:
            if height and width:
                dim = (self.round_up(height), self.round_up(height * float(width / height)))
            elif not height and not width:
                pass
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
    # cap = cv2.VideoCapture(0)
    cap = VideoStream().start()
    while cap.isOpened():
        ret, frame = cap.read()
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
    cv2.destroyAllWindows()
