import os
import cv2
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from PyQt5 import QtWidgets, QtGui
from Base.VideoStream import VideoStream


def configure(frame, version):
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
    plt.get_current_fig_manager().canvas.set_window_title('ORSS4SCVI ' + version)
    # print((os.path.dirname(__file__) + '/static/icons/icon.ico').replace((version.replace('.', '') + '/'), ''))
    plt.get_current_fig_manager().window.setWindowIcon(QtGui.QIcon(
        (os.path.dirname(__file__) + '/static/icons/icon.ico').replace((version.replace('.', '') + '/'), '')))
    plt.axis('off')


def grab_frame(cap):
    ret, frame = cap.read()
    return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


def update(i):
    s = cv2.getTickCount()
    im1.set_data(grab_frame(cap))
    f = cv2.getTickCount()
    print('{:.2f}'.format(cv2.getTickFrequency() / (f - s)))


def close(event):
    if event.key == 'q':
        plt.close(event.canvas.figure)
        cap.release()


cap = VideoStream().start()
configure(frame=cap.read()[1], version='dev0.1b')
# ax1 = plt.subplot()
im1 = plt.imshow(grab_frame(cap), aspect='auto')
# im1 = ax1.imshow(grab_frame(cap), aspect='auto')
# ax1.legend('hi')
# plt.legend('hit', loc='best', ncol=2, mode="expand", shadow=True, fancybox=True)
ani = animation.FuncAnimation(plt.gcf(), update, interval=0.01)
# plt.gcf().text(5, 15, 'hi')
cid = plt.gcf().canvas.mpl_connect("key_press_event", close)
# plt.plot(label='hi')
# plt.text(5, 15, 'matplotlib', bbox=dict(facecolor='red', alpha=0.5))
# plt.text(20, 0.5,'matplotlib', horizontalalignment='center', verticalalignment='center')
# plt.text(60, .025, r'$\mu=100,\ \sigma=15$')
plt.show()

# code that should be executed after window is closed.
