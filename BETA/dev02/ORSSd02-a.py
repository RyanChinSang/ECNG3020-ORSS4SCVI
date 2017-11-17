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
from BETA.dev02.models.VideoStream import VideoStream
from BETA.dev02.models.SpchRecg import internet, google_sr, sphinx_sr
from BETA.dev02.utils import visualization_utils as vis_util
from BETA.dev02.utils import label_map_util


def s2t_listen():
    global s2t_string
    with voice_lock:
        if internet():
            with sr.Microphone(device_index=0) as source:
                audio = sr.Recognizer().listen(source)
            # TODO: thread this?
            s2t_string = google_sr(audio)
        else:
            pass
        # with sr.Microphone(device_index=0) as source:
        #     # print('Say something!')
        #     audio = sr.Recognizer().listen(source)
        # if internet():
        #     s2t_string = google_sr(audio)
        # else:
        #     s2t_string = sphinx_sr(audio)


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
    min_dif = 16581375  # Maximum possible difference of (255)^3
    closest_color = None
    for color in colors_dict.keys():
        r_c, g_c, b_c = color.replace(' ', '').strip('[]').split(',')
        dif_val = ((int(r_c) - requested_color[0]) ** 2) + ((int(g_c) - requested_color[1]) ** 2) +\
                  ((int(b_c) - requested_color[2]) ** 2)
        if min_dif > dif_val:
            min_dif = dif_val
            closest_color = colors_dict[color]
    threading.Thread(target=t2s_say, args=(closest_color,), daemon=True).start()


def close_handler(event):
    cap.release()
    plt.close('all')


def active_handler(event):
    global s2t_string
    # if s2t_string == 'color':
    if 'color' in str(s2t_string):
        # print('Colour ID function goes here (threaded)')
        threading.Thread(target=avg_color, args=(), daemon=True).start()
        s2t_string = None
    elif 'quit' in str(s2t_string):
        close_handler(event)
    else:
        threading.Thread(target=s2t_listen, args=(), daemon=True).start()
        # print('ye')
        # threading.Thread(target=pprint, args=(s2t_string, ), daemon=True).start()
    # s2t_string = threading.Thread(target=s2t_listen, args=(), daemon=True).start()
    # print(s2t_string)


def key_press_handler(event):
    # a,c,v,f,g,G,g,h,r,p,q,W,Q,S,k,L,l,o
    if event.key == 'b':
        threading.Thread(target=online_op, args=(), daemon=True).start()
    if event.key == 'd':
        threading.Thread(target=avg_color, args=(), daemon=True).start()
    print(event.key)


def configure(frame, version):
    dpi = int(matplotlib.rcParams['figure.dpi'])
    matplotlib.rcParams['figure.subplot.bottom'] = '0.0'
    matplotlib.rcParams['figure.subplot.left'] = '0.0'
    matplotlib.rcParams['figure.subplot.top'] = '1.0'
    matplotlib.rcParams['figure.subplot.right'] = '1.0'
    matplotlib.rcParams['figure.subplot.right'] = '1.0'
    matplotlib.rcParams['figure.figsize'] = [(frame.shape[1] / dpi), ((frame.shape[0] - (48 + 20)) / dpi)]
    for key in matplotlib.rcParams:
        if 'keymap' in key:
            print(key + ': ' + str(matplotlib.rcParams.get(key)))
    plt.switch_backend('Qt5Agg')
    plt.get_current_fig_manager().canvas.mpl_connect('key_press_event', key_press_handler)
    # plt.get_current_fig_manager().canvas.mpl_connect('draw_event', active_handler)
    plt.get_current_fig_manager().canvas.mpl_connect('close_event', close_handler)
    plt.get_current_fig_manager().canvas.set_window_title('ORSS4SCVI ' + version)
    plt.get_current_fig_manager().canvas.manager.window.findChild(QtWidgets.QToolBar).setVisible(False)
    plt.get_current_fig_manager().canvas.manager.window.statusBar().setVisible(False)
    plt.get_current_fig_manager().window.setWindowIcon(QtGui.QIcon(PATH_TO_ICON))
    plt.axis('off')


def online_op():
    # global internet
    # internet = internet()
    acth = None
    if internet():
        print('Online! Using online mode.')
        acth = plt.get_current_fig_manager().canvas.mpl_connect('draw_event', active_handler)
    else:
        print('Offline! Using offline mode.')
        if acth:
            plt.get_current_fig_manager().canvas.mpl_disconnect(acth)


# internet = internet()
# internet = 1 if internet() else 0
colors_dict = {'[240, 248, 255]': 'aliceblue',
          '[250, 235, 215]': 'antiquewhite',
          '[0, 255, 255]': 'cyan',
          '[127, 255, 212]': 'aquamarine',
          '[240, 255, 255]': 'azure',
          '[245, 245, 220]': 'beige',
          '[255, 228, 196]': 'bisque',
          '[0, 0, 0]': 'black',
          '[255, 235, 205]': 'blanchedalmond',
          '[0, 0, 255]': 'blue',
          '[138, 43, 226]': 'blueviolet',
          '[165, 42, 42]': 'brown',
          '[222, 184, 135]': 'burlywood',
          '[95, 158, 160]': 'cadetblue',
          '[127, 255, 0]': 'chartreuse',
          '[210, 105, 30]': 'chocolate',
          '[255, 127, 80]': 'coral',
          '[100, 149, 237]': 'cornflowerblue',
          '[255, 248, 220]': 'cornsilk',
          '[220, 20, 60]': 'crimson',
          '[0, 0, 139]': 'darkblue',
          '[0, 139, 139]': 'darkcyan',
          '[184, 134, 11]': 'darkgoldenrod',
          '[169, 169, 169]': 'darkgrey',
          '[0, 100, 0]': 'darkgreen',
          '[189, 183, 107]': 'darkkhaki',
          '[139, 0, 139]': 'darkmagenta',
          '[85, 107, 47]': 'darkolivegreen',
          '[255, 140, 0]': 'darkorange',
          '[153, 50, 204]': 'darkorchid',
          '[139, 0, 0]': 'darkred',
          '[233, 150, 122]': 'darksalmon',
          '[143, 188, 143]': 'darkseagreen',
          '[72, 61, 139]': 'darkslateblue',
          '[47, 79, 79]': 'darkslategrey',
          '[0, 206, 209]': 'darkturquoise',
          '[148, 0, 211]': 'darkviolet',
          '[255, 20, 147]': 'deeppink',
          '[0, 191, 255]': 'deepskyblue',
          '[105, 105, 105]': 'dimgrey',
          '[30, 144, 255]': 'dodgerblue',
          '[178, 34, 34]': 'firebrick',
          '[255, 250, 240]': 'floralwhite',
          '[34, 139, 34]': 'forestgreen',
          '[255, 0, 255]': 'magenta',
          '[220, 220, 220]': 'gainsboro',
          '[248, 248, 255]': 'ghostwhite',
          '[255, 215, 0]': 'gold',
          '[218, 165, 32]': 'goldenrod',
          '[128, 128, 128]': 'grey',
          '[0, 128, 0]': 'green',
          '[173, 255, 47]': 'greenyellow',
          '[240, 255, 240]': 'honeydew',
          '[255, 105, 180]': 'hotpink',
          '[205, 92, 92]': 'indianred',
          '[75, 0, 130]': 'indigo',
          '[255, 255, 240]': 'ivory',
          '[240, 230, 140]': 'khaki',
          '[230, 230, 250]': 'lavender',
          '[255, 240, 245]': 'lavenderblush',
          '[124, 252, 0]': 'lawngreen',
          '[255, 250, 205]': 'lemonchiffon',
          '[173, 216, 230]': 'lightblue',
          '[240, 128, 128]': 'lightcoral',
          '[224, 255, 255]': 'lightcyan',
          '[250, 250, 210]': 'lightgoldenrodyellow',
          '[211, 211, 211]': 'lightgrey',
          '[144, 238, 144]': 'lightgreen',
          '[255, 182, 193]': 'lightpink',
          '[255, 160, 122]': 'lightsalmon',
          '[32, 178, 170]': 'lightseagreen',
          '[135, 206, 250]': 'lightskyblue',
          '[119, 136, 153]': 'lightslategrey',
          '[176, 196, 222]': 'lightsteelblue',
          '[255, 255, 224]': 'lightyellow',
          '[0, 255, 0]': 'lime',
          '[50, 205, 50]': 'limegreen',
          '[250, 240, 230]': 'linen',
          '[128, 0, 0]': 'maroon',
          '[102, 205, 170]': 'mediumaquamarine',
          '[0, 0, 205]': 'mediumblue',
          '[186, 85, 211]': 'mediumorchid',
          '[147, 112, 219]': 'mediumpurple',
          '[60, 179, 113]': 'mediumseagreen',
          '[123, 104, 238]': 'mediumslateblue',
          '[0, 250, 154]': 'mediumspringgreen',
          '[72, 209, 204]': 'mediumturquoise',
          '[199, 21, 133]': 'mediumvioletred',
          '[25, 25, 112]': 'midnightblue',
          '[245, 255, 250]': 'mintcream',
          '[255, 228, 225]': 'mistyrose',
          '[255, 228, 181]': 'moccasin',
          '[255, 222, 173]': 'navajowhite',
          '[0, 0, 128]': 'navy',
          '[253, 245, 230]': 'oldlace',
          '[128, 128, 0]': 'olive',
          '[107, 142, 35]': 'olivedrab',
          '[255, 165, 0]': 'orange',
          '[255, 69, 0]': 'orangered',
          '[218, 112, 214]': 'orchid',
          '[238, 232, 170]': 'palegoldenrod',
          '[152, 251, 152]': 'palegreen',
          '[175, 238, 238]': 'paleturquoise',
          '[219, 112, 147]': 'palevioletred',
          '[255, 239, 213]': 'papayawhip',
          '[255, 218, 185]': 'peachpuff',
          '[205, 133, 63]': 'peru',
          '[255, 192, 203]': 'pink',
          '[221, 160, 221]': 'plum',
          '[176, 224, 230]': 'powderblue',
          '[128, 0, 128]': 'purple',
          '[255, 0, 0]': 'red',
          '[188, 143, 143]': 'rosybrown',
          '[65, 105, 225]': 'royalblue',
          '[139, 69, 19]': 'saddlebrown',
          '[250, 128, 114]': 'salmon',
          '[244, 164, 96]': 'sandybrown',
          '[46, 139, 87]': 'seagreen',
          '[255, 245, 238]': 'seashell',
          '[160, 82, 45]': 'sienna',
          '[192, 192, 192]': 'silver',
          '[135, 206, 235]': 'skyblue',
          '[106, 90, 205]': 'slateblue',
          '[112, 128, 144]': 'slategrey',
          '[255, 250, 250]': 'snow',
          '[0, 255, 127]': 'springgreen',
          '[70, 130, 180]': 'steelblue',
          '[210, 180, 140]': 'tan',
          '[0, 128, 128]': 'teal',
          '[216, 191, 216]': 'thistle',
          '[255, 99, 71]': 'tomato',
          '[64, 224, 208]': 'turquoise',
          '[238, 130, 238]': 'violet',
          '[245, 222, 179]': 'wheat',
          '[255, 255, 255]': 'white',
          '[245, 245, 245]': 'whitesmoke',
          '[255, 255, 0]': 'yellow',
          '[154, 205, 50]': 'yellowgreen'}
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

cap = VideoStream(src=-1, height=360, width=640).start()
# cap = VideoStream().start()
init_frame = cap.read()[1]
frame_height, frame_width = init_frame.shape[:2]
freq = cv2.getTickFrequency()

configure(frame=init_frame, version='dev0.2a')
online_op()
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
            t.set_text(f'{cap.fps():{0}.{3}}')  # Python 3.6 - specific code
            # t.set_text(''.join(cap.fps()))
