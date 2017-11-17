import matplotlib
import matplotlib.pyplot as plt
from PyQt5 import QtWidgets

matplotlib.rcParams['figure.subplot.bottom'] = '0.0'
matplotlib.rcParams['figure.subplot.left'] = '0.0'
matplotlib.rcParams['figure.subplot.top'] = '1.0'
matplotlib.rcParams['figure.subplot.right'] = '1.0'
matplotlib.rcParams['figure.subplot.right'] = '1.0'
matplotlib.rcParams["figure.figsize"] = [(frame.shape[1] / int(matplotlib.rcParams['figure.dpi'])),
                                         ((frame.shape[0] - (48 + 20)) / int(matplotlib.rcParams['figure.dpi']))]
# for key in matplotlib.rcParams:
#     if 'keymap' in key:
#         print(key + ": " + str(matplotlib.rcParams.get(key)))
plt.switch_backend('Qt5Agg')
# plt.get_current_fig_manager().canvas.mpl_connect('key_press_event', key_press_handler)
# plt.get_current_fig_manager().canvas.mpl_connect('draw_event', active_handler)
# plt.get_current_fig_manager().canvas.mpl_connect('close_event', close_handler)
# plt.get_current_fig_manager().canvas.set_window_title('ORSS4SCVI ' + version)
plt.get_current_fig_manager().canvas.manager.window.findChild(QtWidgets.QToolBar).setVisible(False)
plt.get_current_fig_manager().canvas.manager.window.statusBar().setVisible(False)
# plt.get_current_fig_manager().window.setWindowIcon(QtGui.QIcon(PATH_TO_ICON))
plt.axis('off')