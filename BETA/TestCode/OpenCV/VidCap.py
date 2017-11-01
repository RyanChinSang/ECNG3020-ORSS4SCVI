import cv2
from threading import Thread


class VideoStream:
    def __init__(self, src=0, height=None, ratio=None):
        # initialize the video camera stream and read the first frame
        # from the stream
        self.stream = cv2.VideoCapture(src)
        self.conf(height=height, ratio=ratio)
        (self.grabbed, self.frame) = self.stream.read()
        # initialize the variable used to indicate if the thread should
        # be stopped
        self.stopped = False

    def conf(self, height, ratio):
        if height is None:
            pass
        else:
            self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, int(height))
            self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, int(height * ratio))

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


if __name__ == '__main__':
    cap = VideoStream(src=0, height=720, ratio=(16 / 9)).start()
    # cap = VideoStream(src=0).start()
    while 1:
        frame = cap.read()
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.stop()
    cv2.destroyAllWindows()
