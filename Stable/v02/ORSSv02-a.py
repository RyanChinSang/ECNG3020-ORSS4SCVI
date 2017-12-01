import os
import cv2
import queue
import pyttsx3
import threading
import matplotlib
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import speech_recognition as sr
import matplotlib.patches as patches
from PyQt5 import QtWidgets, QtGui
from Stable.v02.utils import label_map_util
from Stable.v02.utils import visualization_utils as vis_util
from Stable.v02.models.ColorID import avg_color
from Stable.v02.models.Txt2Spch import t2s_say
from Stable.v02.models.VideoStream import VideoStream
from Stable.v02.models.SpchRecg import internet, google_sr


def s2t_listen():
    global s2t_string, state
    with voice_lock:
        if state:
            with sr.Microphone(device_index=0) as source:
                audio = sr.Recognizer().listen(source)
            if state and internet():
                s2t_string = google_sr(audio)


def state_upd():
    global state
    state = internet()
    if state is True:
        print('Online! Using online mode.')
    else:
        print('Offline! Using offline mode')


def close_handler(event):
    cap.release()
    plt.close('all')


def active_handler(event):
    global s2t_string
    if 'color' in str(s2t_string):
        threading.Thread(target=avg_color, args=(cap.read()[1], size, frame_height, frame_width, q),
                         daemon=True).start()
        threading.Thread(target=t2s_say, args=(q.get(), q), daemon=True).start()
        s2t_string = None
    elif 'quit' in str(s2t_string):
        close_handler(event)
    else:
        threading.Thread(target=s2t_listen, args=(), daemon=True).start()


def key_press_handler(event):
    global state
    if event.key == controls_dict.get('online check')[0]:
        threading.Thread(target=state_upd, args=(), daemon=True).start()
    if event.key == controls_dict.get('color check')[0]:
        threading.Thread(target=avg_color, args=(cap.read()[1], size, frame_height, frame_width, q),
                         daemon=True).start()
        threading.Thread(target=t2s_say, args=(q.get(), q), daemon=True).start()
    if event.key == controls_dict.get('offline force')[0]:
        state = False
        print('Offline! Using offline mode')
    if event.key == controls_dict.get('save')[0]:
        extra_width = plt.get_current_fig_manager().window.width() - plt.get_current_fig_manager().canvas.width()
        extra_height = plt.get_current_fig_manager().window.height() - plt.get_current_fig_manager().canvas.height()
        plt.get_current_fig_manager().window.resize(frame_width + extra_width, frame_height + extra_height)


def configure(frame, dir, version):
    maxlen = len(max(controls_dict, key=len))
    dpi = int(matplotlib.rcParams['figure.dpi'])
    savedir = os.path.join(os.path.dirname(__file__), dir).replace('\\', '/')
    if not os.path.isdir(savedir):
        try:
            os.makedirs(savedir)
        except OSError as exc:
            if not (exc.errno == exc.errno.EEXIST and os.path.isdir(savedir)):
                raise
    matplotlib.rcParams["savefig.directory"] = savedir
    matplotlib.rcParams['figure.subplot.bottom'] = '0.0'
    matplotlib.rcParams['figure.subplot.left'] = '0.0'
    matplotlib.rcParams['figure.subplot.top'] = '1.0'
    matplotlib.rcParams['figure.subplot.right'] = '1.0'
    matplotlib.rcParams['figure.subplot.right'] = '1.0'
    matplotlib.rcParams['figure.figsize'] = [(frame.shape[1] / dpi), ((frame.shape[0] - (48 + 20)) / dpi)]
    plt.switch_backend('Qt5Agg')
    plt.get_current_fig_manager().canvas.mpl_connect('key_press_event', key_press_handler)
    plt.get_current_fig_manager().canvas.mpl_connect('draw_event', active_handler)
    plt.get_current_fig_manager().canvas.mpl_connect('close_event', close_handler)
    plt.get_current_fig_manager().canvas.set_window_title('ORSS4SCVI ' + version)
    plt.get_current_fig_manager().canvas.manager.window.findChild(QtWidgets.QToolBar).setVisible(False)
    plt.get_current_fig_manager().canvas.manager.window.statusBar().setVisible(False)
    plt.get_current_fig_manager().window.setWindowIcon(QtGui.QIcon(PATH_TO_ICON))
    plt.axis('off')
    for key in controls_dict:
        print(key.ljust(maxlen, ' ') + ': ' + str(controls_dict.get(key)).strip('[]').replace('\'', ''))
    state_upd()


controls_dict = {
    # a,c,v,f,g,G,g,h,r,p,q,W,Q,s,k,L,l,o,b,d
    # e,t,y,u,i
    # d,j
    # [z],[x],b,n,[m]
    'all axes': ['a'],
    'back': ['left', 'c', 'backspace'],
    'color check': ['m'],  #
    'forward': ['right', 'v'],
    'fullscreen': ['f', 'ctrl+f'],
    'grid': ['g'],
    'grid minor': ['G'],
    'home': ['h', 'r', 'home'],
    'offline force': ['x'],  #
    'online check': ['z'],  #
    'pan': ['p'],
    'quit': ['ctrl+w', 'cmd+w', 'q'],
    'quit all': ['W', 'cmd+W', 'Q'],
    'save': ['s', 'ctrl+s'],
    'xscale': ['k', 'L'],
    'yscale': ['l'],
    'zoom': ['o']
}
avg_fps = np.array([])
size = 20
state = None
s2t_string = None
q = queue.Queue()
voice_lock = threading.Lock()

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

cap = VideoStream(height=360, width=640).start()
init_frame = cap.read()[1]
frame_height, frame_width = init_frame.shape[:2]
freq = cv2.getTickFrequency()

configure(frame=init_frame, dir='Screenshots', version='v0.2a')
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
t = ax.text(5, 15, f'{0}', color='white')

with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')
    with tf.Session(graph=detection_graph) as sess:
        image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
        detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
        detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
        detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
        num_detections = detection_graph.get_tensor_by_name('num_detections:0')
        while cap.isOpened():
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
                line_thickness=1)
            img.set_data(cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB))
            if plt.get_fignums():
                fig.canvas.draw()
                fig.canvas.flush_events()
                plt.show(block=False)
            t.set_text(f'{cap.fps():{0}.{3}}')
