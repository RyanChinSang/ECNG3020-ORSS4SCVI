import sys
import matplotlib
import matplotlib.pyplot as plt
from PyQt5 import QtWidgets


class mpl_imshow:
    def __init__(self, frame):
        matplotlib.rcParams['figure.subplot.bottom'] = '0.0'
        matplotlib.rcParams['figure.subplot.left'] = '0.0'
        matplotlib.rcParams['figure.subplot.top'] = '1.0'
        matplotlib.rcParams['figure.subplot.right'] = '1.0'
        matplotlib.rcParams['figure.subplot.right'] = '1.0'
        matplotlib.rcParams["figure.figsize"] = [(frame.shape[1] / int(matplotlib.rcParams['figure.dpi'])),
                                                 ((frame.shape[0] - 48) / int(matplotlib.rcParams['figure.dpi']))]
        plt.switch_backend('Qt5Agg')
        plt.get_current_fig_manager().canvas.manager.window.findChild(QtWidgets.QToolBar).setVisible(False)
        plt.get_current_fig_manager().canvas.manager.window.statusBar().setVisible(False)
        # img = plt.imshow(frame, aspect='auto')
        # img.set_data(frame)
        # self.start(img=img, frame=frame)

    def start(self, img, frame):
        # img = plt.imshow(frame, aspect='auto')
        self.update(img, frame)

    def update(self, img, frame):
        img.set_data(frame)
        if plt.get_fignums():
            plt.pause(0.01)
        else:
            sys.exit()


if __name__ == '__main__':
    import cv2

    cap = cv2.VideoCapture(0)
    img = plt.imshow(cap.read()[1], aspect='auto')

    while 1:
        _, frame = cap.read()
        mpl_imshow(frame).start(img, frame)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break
    cap.release()