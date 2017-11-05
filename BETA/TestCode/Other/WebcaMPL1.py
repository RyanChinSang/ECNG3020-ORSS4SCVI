import cv2
import matplotlib
import matplotlib.pyplot as plt
from PyQt5 import QtWidgets


def press(event):
    # if event.key == 'z'
    print(event.key)
    # sys.stdout.flush()
    # if event.key == 'x':
    #     visible = xl.get_visible()
    #     xl.set_visible(not visible)
    #     fig.canvas.draw()

cap = cv2.VideoCapture(0)
# print(cap.read()[1].shape[0])
# print(cap.read()[1].shape[1])
# matplotlib.rcParams['toolbar'] = 'None'
matplotlib.rcParams['figure.subplot.bottom'] = '0.0'
matplotlib.rcParams['figure.subplot.left'] = '0.0'
matplotlib.rcParams['figure.subplot.top'] = '1.0'
matplotlib.rcParams['figure.subplot.right'] = '1.0'
matplotlib.rcParams['figure.subplot.right'] = '1.0'
# dpi = int(matplotlib.rcParams['figure.dpi'])
# print(matplotlib.rcParams['figure.figsize'])
print(matplotlib.rcParams)
matplotlib.rcParams["figure.figsize"] = [(cap.read()[1].shape[1] / int(matplotlib.rcParams['figure.dpi'])),
                                         ((cap.read()[1].shape[0] - 48) / int(matplotlib.rcParams['figure.dpi']))]
# plt.gcf().canvas.mpl_connect('key_press_event', press)
# plt.
plt.switch_backend('Qt5Agg')
plt.get_current_fig_manager().canvas.manager.window.findChild(QtWidgets.QToolBar).setVisible(False)
# plt.get_current_fig_manager().canvas.manager.window.findChild(QtWidgets.QToolBar).setParent(None)
plt.get_current_fig_manager().canvas.manager.window.statusBar().setVisible(False)
plt.get_current_fig_manager().canvas.set_window_title('ORSS4SCVI dev0.1a')
plt.get_current_fig_manager().canvas.mpl_connect('key_press_event', press)
# plt.get_current_fig_manager().canvas.manager.window.statusBar().setParent(None)
# plt.subplots_adjust(left=0.0, right=1.0, bottom=0.0, top=1.0)
# plt.get_current_fig_manager().canvas.manager.window.statusBar().setParent(None)
# plt.get_current_fig_manager().__dict__.get('canvas').__dict__.get('figure').__dict__.get('subplotpars').__dict__ = \
#     {'validate': True, 'left': 0.000, 'right': 1.000, 'bottom': 0.000, 'top': 1.000, 'wspace': 0.000, 'hspace': 0.000}
# plt.figure()
# fig = plt.figure(figsize=(6.4,4.8))
# im1 = fig.figimage(cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2RGB))
# plt.show()
# ax = fig.add_subplot(111)
# im1 = ax.imshow(cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2RGB), aspect='auto')
im1 = plt.imshow(cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2RGB), aspect='auto')


while True:
    _, frame = cap.read()
    # im1.set_data(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    im1.set_data(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    if not plt.get_fignums():
        break
    else:
        plt.pause(0.01)

cap.release()
