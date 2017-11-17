import sys
import matplotlib
import matplotlib.pyplot as plt
from PyQt5 import QtWidgets


class mpl_imshow:
    # def __init__(self, frame):
    def __init__(self, nframe):
        self.frame = nframe
        self.stream = cv2.VideoCapture()
        self.image = plt.imshow(self.frame, aspect='auto')
        self.config()
        # img = plt.imshow(frame, aspect='auto')
        # img.set_data(frame)
        # self.start(img=img, frame=frame)
        # self.image.set_data(self.frame)
        # self.image.set_data(self.frame)
        # if plt.get_fignums():
        #     plt.pause(0.01)
        # else:
        #     sys.exit()

    def config(self):
        matplotlib.rcParams['figure.subplot.bottom'] = '0.0'
        matplotlib.rcParams['figure.subplot.left'] = '0.0'
        matplotlib.rcParams['figure.subplot.top'] = '1.0'
        matplotlib.rcParams['figure.subplot.right'] = '1.0'
        matplotlib.rcParams['figure.subplot.right'] = '1.0'
        matplotlib.rcParams["figure.figsize"] = [(self.frame.shape[1] / int(matplotlib.rcParams['figure.dpi'])),
                                                 ((self.frame.shape[0] - 48) / int(matplotlib.rcParams['figure.dpi']))]
        plt.switch_backend('Qt5Agg')
        plt.get_current_fig_manager().canvas.manager.window.findChild(QtWidgets.QToolBar).setVisible(False)
        plt.get_current_fig_manager().canvas.manager.window.statusBar().setVisible(False)

    def start(self):
        self.update()
        return self

    def update(self):
        self.image.set_data(self.frame)
        plt.pause(0.01)
        # while True:
        #     # _, frame = cap.read()
        #     # _, self.frame = self.stream.read()
        #     self.image.set_data(self.frame)
        #     plt.pause(0.01)

if __name__ == '__main__':
    import cv2

    cap = cv2.VideoCapture(0)
    # img = plt.imshow(cap.read()[1], aspect='auto')

    while 1:
        _, frame = cap.read()
        # mpl_imshow(frame).start(img, frame)
        # mpl_imshow(frame).start()
        mpl_imshow(frame).start()
        # mpl_imshow().start(img, frame)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break
        if plt.get_fignums():
            plt.pause(0.01)
        else:
            break
    cap.release()
