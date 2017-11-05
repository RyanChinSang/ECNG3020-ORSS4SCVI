import os
import cv2
import matplotlib
import matplotlib.pyplot as plt
from threading import Thread
from PyQt5 import QtWidgets, QtGui


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


def close_handler(event):
    cap.stop()


def active_handler(event):
    # print('work')
    pass


def key_press_handler(event):
    print(event.key)


def configure(frame, version):
    matplotlib.rcParams['figure.subplot.bottom'] = '0.0'
    matplotlib.rcParams['figure.subplot.left'] = '0.0'
    matplotlib.rcParams['figure.subplot.top'] = '1.0'
    matplotlib.rcParams['figure.subplot.right'] = '1.0'
    matplotlib.rcParams['figure.subplot.right'] = '1.0'
    matplotlib.rcParams["figure.figsize"] = [(frame.shape[1] / int(matplotlib.rcParams['figure.dpi'])),
                                             ((frame.shape[0] - 48) / int(matplotlib.rcParams['figure.dpi']))]
    for key in matplotlib.rcParams:
        if 'keymap' in key:
            print(key + ": " + str(matplotlib.rcParams.get(key)))
    plt.switch_backend('Qt5Agg')
    plt.get_current_fig_manager().canvas.mpl_connect('key_press_event', key_press_handler)
    plt.get_current_fig_manager().canvas.mpl_connect('draw_event', active_handler)
    plt.get_current_fig_manager().canvas.mpl_connect('close_event', close_handler)
    plt.get_current_fig_manager().canvas.set_window_title('ORSS4SCVI ' + version)
    plt.get_current_fig_manager().canvas.manager.window.findChild(QtWidgets.QToolBar).setVisible(False)
    plt.get_current_fig_manager().canvas.manager.window.statusBar().setVisible(False)
    # plt.get_current_fig_manager().window.wm_iconbitmap(os.path.dirname(__file__) + '/static/icons/icon.ico')
    plt.get_current_fig_manager().window.setWindowIcon(QtGui.QIcon('C:/Users/ryanc/PycharmProjects/ECNG3020-ORSS4SCVI/'
                                                                   'BETA/static/icons/icon.ico'))


def main():
    img = plt.imshow(cv2.cvtColor(cap.read(), cv2.COLOR_BGR2RGB), aspect='auto')
    while 1:
        frame = cap.read()
        img.set_data(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        if plt.get_fignums():
            plt.pause(0.01)
        else:
            break


cap = VideoStream(height=720, width=1280).start()
configure(cap.read(height=480, ratio=(16/9)), version='dev0.1a')
main()
