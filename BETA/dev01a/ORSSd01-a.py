import os
import cv2
import queue
import pyttsx3
import webcolors
import threading
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import speech_recognition as sr
import matplotlib.patches as patches
from PyQt5 import QtWidgets, QtGui
# from BETA.dev01a.models.VideoStream import VideoStream
from Base.VideoStream import VideoStream
from BETA.dev01a.models.SpchRecg import internet, google_sr, sphinx_sr
# from BETA.dev01a.models.ColorID import


def s2t_listen():
    global s2t_string
    with voice_lock:
        # if internet():
        #     with sr.Microphone(device_index=0) as source:
        #         audio = sr.Recognizer().listen(source)
        #     s2t_string = google_sr(audio)
        # else:
        #     pass
        with sr.Microphone(device_index=0) as source:
            # print("Say something!")
            audio = sr.Recognizer().listen(source)
        if internet():
            # TODO: thread this?
            s2t_string = google_sr(audio)
        else:
            s2t_string = sphinx_sr(audio)


def close_handler(event):
    cap.release()
    plt.close('all')


def active_handler(event):
    global s2t_string
    if s2t_string == 'color':
        print('Colour ID function goes here (threaded)')
        # threading.Thread
        # s2t_string = None
    elif s2t_string == 'quit':
        close_handler(event)
    else:
        threading.Thread(target=s2t_listen, args=(), daemon=True).start()
        # threading.Thread(target=pprint, args=(s2t_string, ), daemon=True).start()
    # s2t_string = threading.Thread(target=s2t_listen, args=(), daemon=True).start()
    # print(s2t_string)


def key_press_handler(event):
    print(event.key)


def configure(frame, version):
    matplotlib.rcParams['figure.subplot.bottom'] = '0.0'
    matplotlib.rcParams['figure.subplot.left'] = '0.0'
    matplotlib.rcParams['figure.subplot.top'] = '1.0'
    matplotlib.rcParams['figure.subplot.right'] = '1.0'
    matplotlib.rcParams['figure.subplot.right'] = '1.0'
    matplotlib.rcParams["figure.figsize"] = [(frame.shape[1] / int(matplotlib.rcParams['figure.dpi'])),
                                             ((frame.shape[0] - (48 + 20)) / int(matplotlib.rcParams['figure.dpi']))]
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
    plt.axis('off')


def avg_color(frame):
    rgb = np.array([])
    for x in range(size * 2):
        for y in range(size * 2):
            if (x, y) == (0, 0):
                rgb = np.array([frame[int((frame_height / 2) - size) + x][
                                    int((frame_width / 2) - size) + y]])
            else:
                rgb = np.append(rgb, [frame[int((frame_height / 2) - size) + x][
                                          int((frame_width / 2) - size) + y]], axis=0)
    requested_color = rgb.mean(axis=0)
    min_colors = {}
    for key, name in webcolors.css3_hex_to_names.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_color[2]) ** 2
        gd = (g_c - requested_color[1]) ** 2
        bd = (b_c - requested_color[0]) ** 2
        min_colors[(rd + gd + bd)] = name

    closest_color = str(min_colors[min(min_colors.keys())])
    print(closest_color)
    threading.Thread(target=t2s_say, args=(closest_color,), daemon=True).start()


def t2s_say(word):
    t2s_engine.say(word)
    try:
        t2s_engine.runAndWait()
    except RuntimeError:
        pass


def main():
    global s2t_string
    fig = plt.gcf()
    ax = plt.gca()
    img = plt.imshow(cv2.cvtColor(init_frame, cv2.COLOR_BGR2RGB), aspect='auto')

    avg_fps = np.array([])

    freq = cv2.getTickFrequency()

    rect = patches.Rectangle(xy=(int((frame_width / 2) - size),
                                 int((frame_height / 2) - size)),  # Top-left point
                             width=int(size * 2),
                             height=int(size * 2),
                             linewidth=1,
                             edgecolor='white',
                             facecolor='none')
    ax.add_patch(rect)
    t = ax.text(5, 15, '{:.2f}'.format(0), color='white')

    while cap.isOpened():
        s = cv2.getTickCount()
        ret, frame = cap.read()
        img.set_data(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        if plt.get_fignums():
            fig.canvas.draw()
            fig.canvas.flush_events()
            plt.show(block=False)
            if s2t_string == 'color':
                threading.Thread(target=avg_color, args=(frame,), daemon=True).start()
                s2t_string = None
        f = cv2.getTickCount()
        avg_fps = np.append(avg_fps, (freq / (f - s)))
        t.set_text('{:.2f}'.format(avg_fps[-1]))
    print('avg_fps = {:.2f} fps'.format(np.average(avg_fps)))


# ---[GLOBALS]---
s2t_string = None
q = queue.Queue()
voice_lock = threading.Lock()
print_lock = threading.Lock()

t2s_engine = pyttsx3.init()
t2s_engine.setProperty('voice', t2s_engine.getProperty('voices')[1].__dict__.get('id'))

# cap = VideoStream().start()
cap = VideoStream(height=360, ratio=(16/9)).start()
init_frame = cap.read()[1]
frame_height, frame_width = init_frame.shape[:2]
size = 20
# ---------------

# configure(frame=cap.read(height=480, ratio=(16 / 9))[1], version='dev0.1a')
configure(frame=init_frame, version='dev0.1a')
main()


'''
TODO:
1- Add tensorflow operation
2- Add colourID operation --WORKS--
3- Add better offline/online operation; check/initialize if internet() as True/False
   a. Offline:
      i. Use keyboard/manual input only
     ii. Do not check for online (faster) - unless user uses specific input to do an online check
         a. This check with call internet() again and re-set the global var
    iii. Use sphinx offline speech2text on keypress (may remove / change to always offline listen / make configurable)
   b. Online:
      i. Use microphone to listen at all times using google, which updates a global var to call different functions
4- Find accurate ways to generalize constants' values

'''