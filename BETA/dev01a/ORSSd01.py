import os
import cv2
import matplotlib
import matplotlib.pyplot as plt
import speech_recognition as sr
from threading import Thread
from PyQt5 import QtWidgets, QtGui
from BETA.dev01a.models.VideoStream import VideoStream
from BETA.dev01a.models.SpchRecg import internet, google_sr, sphinx_sr


def listen_sr():
    with sr.Microphone(device_index=0) as source:
        # print("Say something!")
        audio = sr.Recognizer().listen(source)
    if internet():
        Thread(target=google_sr, args=(audio,), daemon=True).start()
    else:
        Thread(target=sphinx_sr, args=(audio,), daemon=True).start()


def close_handler(event):
    cap.stop()


def active_handler(event):
    Thread(target=listen_sr, args=(), daemon=True).start()
    # if
    # print('work')
    # pass


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
    plt.get_current_fig_manager().window.setWindowIcon(QtGui.QIcon(
        (os.path.dirname(__file__) + '/static/icons/icon.ico').replace((version.replace('.', '') + '/'), '')))


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
configure(cap.read(height=480, ratio=(16 / 9)), version='dev0.1a')
main()
