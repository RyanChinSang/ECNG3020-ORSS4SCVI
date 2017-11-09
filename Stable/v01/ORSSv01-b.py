import os
import cv2
import queue
import pyttsx3
import webcolors
import threading
import matplotlib
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import speech_recognition as sr
import matplotlib.patches as patches
from PyQt5 import QtWidgets, QtGui
from Stable.v01.models.VideoStream import VideoStream
from Stable.v01.models.SpchRecg import internet, google_sr, sphinx_sr
from Stable.v01.utils import visualization_utils as vis_util
from Stable.v01.utils import label_map_util


def s2t_listen():
    global s2t_string
    with voice_lock:
        with sr.Microphone(device_index=0) as source:
            audio = sr.Recognizer().listen(source)
        if internet():
            # TODO: thread this?
            s2t_string = google_sr(audio)
        else:
            s2t_string = sphinx_sr(audio)


def t2s_say(word):
    t2s_engine.say(word)
    try:
        t2s_engine.runAndWait()
    except RuntimeError:
        pass


def avg_color():
    frame = cap.read()[1]
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


def close_handler(event):
    cap.release()
    plt.close('all')


def active_handler(event):
    global s2t_string
    if 'color' in str(s2t_string):
        threading.Thread(target=avg_color, args=(), daemon=True).start()
        s2t_string = None
    elif 'quit' in str(s2t_string):
        close_handler(event)
    else:
        threading.Thread(target=s2t_listen, args=(), daemon=True).start()


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
    plt.get_current_fig_manager().window.setWindowIcon(QtGui.QIcon(PATH_TO_ICON))
    plt.axis('off')


avg_fps = np.array([])
size = 20
s2t_string = None
q = queue.Queue()
voice_lock = threading.Lock()
print_lock = threading.Lock()

t2s_engine = pyttsx3.init()
t2s_engine.setProperty('voice', t2s_engine.getProperty('voices')[1].__dict__.get('id'))

MODEL_NAME = 'ssd_mobilenet_v1_coco_11_06_2017'
PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb'
PATH_TO_LABELS = os.path.join('data', 'mscoco_label_map.pbtxt')
PATH_TO_ICON = os.path.dirname(__file__) + '/static/icons/icon.ico'
NUM_CLASSES = 90
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map,
                                                            max_num_classes=NUM_CLASSES,
                                                            use_display_name=True)
category_index = label_map_util.create_category_index(categories)
detection_graph = tf.Graph()

cap = VideoStream(height=360, ratio=(16/9)).start()
init_frame = cap.read()[1]
frame_height, frame_width = init_frame.shape[:2]
freq = cv2.getTickFrequency()

configure(frame=init_frame, version='v0.1b')
fig = plt.gcf()
ax = plt.gca()
img = plt.imshow(cv2.cvtColor(init_frame, cv2.COLOR_BGR2RGB), aspect='auto')
rect = patches.Rectangle(xy=(int((frame_width / 2) - size),
                             int((frame_height / 2) - size)),  # Top-left point
                         width=int(size * 2),
                         height=int(size * 2),
                         linewidth=1,
                         edgecolor='white',
                         facecolor='none')
ax.add_patch(rect)
t = ax.text(5, 15, '{:.2f}'.format(0), color='white')


with detection_graph.as_default():
    # Load a frozen Tensorflow model into memory.
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')
    # Detection
    with tf.Session(graph=detection_graph) as sess:
        image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
        detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
        detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
        detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
        num_detections = detection_graph.get_tensor_by_name('num_detections:0')
        while cap.isOpened():
            s = cv2.getTickCount()
            _, image_np = cap.read()

            image_np_expanded = np.expand_dims(image_np, axis=0)
            (boxes, scores, classes, num) = sess.run(
                [detection_boxes, detection_scores, detection_classes, num_detections],
                feed_dict={image_tensor: image_np_expanded})
            vis_util.visualize_boxes_and_labels_on_image_array(
                image_np,
                np.squeeze(boxes),
                np.squeeze(classes).astype(np.int32),
                np.squeeze(scores),
                category_index,
                use_normalized_coordinates=True,
                line_thickness=2)

            img.set_data(cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB))
            if plt.get_fignums():
                fig.canvas.draw()
                fig.canvas.flush_events()
                plt.show(block=False)
            f = cv2.getTickCount()
            avg_fps = np.append(avg_fps, (freq / (f - s)))
            t.set_text('{:.2f}'.format(avg_fps[-1]))
