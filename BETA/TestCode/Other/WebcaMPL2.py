import cv2
import matplotlib
import matplotlib.pyplot as plt
from PyQt5 import QtWidgets


def key_press(event):
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
    plt.get_current_fig_manager().canvas.mpl_connect('key_press_event', key_press)
    plt.get_current_fig_manager().canvas.set_window_title('ORSS4SCVI ' + version)
    plt.get_current_fig_manager().canvas.manager.window.findChild(QtWidgets.QToolBar).setVisible(False)
    plt.get_current_fig_manager().canvas.manager.window.statusBar().setVisible(False)


def main():
    img = plt.imshow(cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2RGB), aspect='auto')
    while True:
        _, frame = cap.read()
        img.set_data(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        if plt.get_fignums():
            plt.pause(0.01)
        else:
            break
    cap.release()


if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    configure(cap.read()[1], version='dev0.1a')
    main()
