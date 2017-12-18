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
from PIL import Image
from PyQt5 import QtWidgets, QtGui
from BETA.dev03.utils import label_map_util
from BETA.dev03.utils import visualization_utils as vis_util
from BETA.dev03.models.ObjectID import object_id
from BETA.dev03.models.ColorID import color_id
from BETA.dev03.models.Txt2Spch import t2s_say
from BETA.dev03.models.Spch2Txt import internet, google_sr
from BETA.dev03.models.VideoStream import VideoStream


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
        threading.Thread(target=color_id, args=(cap.read()[1], size, frame_height, frame_width, q),
                         daemon=True).start()
        threading.Thread(target=t2s_say, args=(q.get(), q), daemon=True).start()
        s2t_string = None
    elif 'quit' in str(s2t_string):
        close_handler(event)
    elif 'object' in str(s2t_string):
        if 'specific' in str(s2t_string):
            threading.Thread(target=object_id, args=(q, scores[0][0], classes[0][0], 1), daemon=True).start()
        else:
            threading.Thread(target=object_id, args=(q, scores[0][0], classes[0][0]), daemon=True).start()
        threading.Thread(target=t2s_say, args=(q.get(), q), daemon=True).start()
        s2t_string = None
    else:
        threading.Thread(target=s2t_listen, args=(), daemon=True).start()


def key_press_handler(event):
    global state, sslist
    if event.key == controls_dict.get('online check')[0]:
        threading.Thread(target=state_upd, args=(), daemon=True).start()
    if event.key == controls_dict.get('color check')[0]:
        threading.Thread(target=color_id, args=(cap.read()[1], size, frame_height, frame_width, q),
                         daemon=True).start()
        threading.Thread(target=t2s_say, args=(q.get(), q), daemon=True).start()
    if event.key == controls_dict.get('offline force')[0]:
        state = False
        print('Offline! Using offline mode')
    if event.key == controls_dict.get('save')[0]:
        extra_width = plt.get_current_fig_manager().window.width() - plt.get_current_fig_manager().canvas.width()
        extra_height = plt.get_current_fig_manager().window.height() - plt.get_current_fig_manager().canvas.height()
        plt.get_current_fig_manager().window.resize(frame_width + extra_width, frame_height + extra_height)
        try:
            newss = matplotlib.rcParams['savefig.directory'] + '/' + \
                    list(set(os.listdir(matplotlib.rcParams['savefig.directory'])) - set(sslist))[0]
            bbox = fig.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
            Image.open(newss).resize((int(bbox.width * fig.dpi), int(bbox.height * fig.dpi)), Image.ANTIALIAS).save(
                newss)
            sslist.append(newss)
        except IndexError:
            print('NOTICE: No file was saved.')
    if event.key == controls_dict.get('object check')[0]:
        threading.Thread(target=object_id, args=(q, scores[0][0], classes[0][0]), daemon=True).start()
        threading.Thread(target=t2s_say, args=(q.get(), q), daemon=True).start()
    if event.key == controls_dict.get('object check2')[0]:
        threading.Thread(target=object_id, args=(q, scores[0][0], classes[0][0], 1), daemon=True).start()
        threading.Thread(target=t2s_say, args=(q.get(), q), daemon=True).start()


def configure(frame, dir, version):
    global sslist
    maxlen = len(max(controls_dict, key=len))
    dpi = int(matplotlib.rcParams['figure.dpi'])
    savedir = os.path.join(os.path.dirname(__file__), dir).replace('\\', '/')
    if not os.path.isdir(savedir):
        try:
            os.makedirs(savedir)
        except OSError as exc:
            if not (exc.errno == exc.errno.EEXIST and os.path.isdir(savedir)):
                raise
    sslist = os.listdir(savedir)
    matplotlib.rcParams['savefig.directory'] = savedir
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
    # [z],[x],b,[n],[m]
    'all axes': ['a'],
    'back': ['left', 'c', 'backspace'],
    'color check': ['m'],  #
    'forward': ['right', 'v'],
    'fullscreen': ['f', 'ctrl+f'],
    'grid': ['g'],
    'grid minor': ['G'],
    'home': ['h', 'r', 'home'],
    'object check': ['n'],
    'object check2': ['ctrl+n'],
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
sslist = []

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

cap = VideoStream(src=1, height=360, width=640).start()
init_frame = cap.read()[1]
frame_height, frame_width = init_frame.shape[:2]
freq = cv2.getTickFrequency()

configure(frame=init_frame, dir='Screenshots', version='dev0.3a')
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
            # print("image_tensor: " + str(image_tensor))
            # image_tensor: Tensor("image_tensor:0", shape=(1, ?, ?, 3), dtype=uint8)

            # print("detection_boxes: " + str(detection_boxes))
            # detection_boxes: Tensor("detection_boxes:0", shape=(1, ?, ?), dtype=float32)

            # print("detection_scores: " + str(detection_scores))
            # detection_scores: Tensor("detection_scores:0", shape=(1, ?), dtype=float32)

            # print("detection_classes: " + str(detection_classes))
            # detection_classes: Tensor("detection_classes:0", shape=(1, ?), dtype=float32)

            # print("num_detection: " + str(num_detections))
            # num_detection: Tensor("num_detections:0", shape=(1,), dtype=float32)
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
            # print('boxes: ' + str(boxes))
            # boxes: [[[2.63233036e-01   9.72492695e-02   9.92589355e-01   5.72609603e-01]
            #          [7.19112396e-01   5.55130064e-01   9.96551991e-01   1.00000000e+00]
            #         [2.37120599e-01   3.56891155e-02   8.93018365e-01   4.50947762e-01]
            # [7.50454903e-01
            # 6.30083859e-01
            # 9.15959597e-01
            # 8.98784459e-01]
            # [6.80188656e-01   1.09961107e-02   9.80296612e-01   1.58909887e-01]
            # [7.86455035e-01
            # 7.25021958e-01
            # 8.48524213e-01
            # 8.17462564e-01]
            # [2.64620632e-01   8.82135332e-02   9.72439885e-01   5.64934492e-01]
            # [4.90889758e-01
            # 7.95773864e-01
            # 7.57265687e-01
            # 1.00000000e+00]
            # [5.43915153e-01   3.50910604e-01   6.69583678e-01   3.84075522e-01]
            # [7.80053496e-01
            # 7.75898635e-01
            # 8.57262254e-01
            # 8.75568330e-01]
            # [6.11732781e-01   1.38083175e-01   7.19360650e-01   1.52957037e-01]
            # [5.10535717e-01
            # 5.00972390e-01
            # 1.00000000e+00
            # 1.00000000e+00]
            # [5.12118340e-01   1.76011920e-02   9.96823072e-01   9.86555159e-01]
            # [7.92069435e-01
            # 6.63512230e-01
            # 9.30275440e-01
            # 9.23985004e-01]
            # [8.42998922e-01   1.99951157e-02   9.96141732e-01   1.52078450e-01]
            # [8.30831885e-01
            # 2.43511289e-01
            # 9.97818589e-01
            # 4.38577145e-01]
            # [6.78026736e-01   0.00000000e+00   1.00000000e+00   5.87970018e-02]
            # [8.43337178e-01
            # 7.62445152e-01
            # 9.08263326e-01
            # 8.81841958e-01]
            # [7.12601125e-01   1.00041300e-01   1.00000000e+00   1.00000000e+00]
            # [7.67016351e-01
            # 7.24602103e-01
            # 9.54493582e-01
            # 8.95415664e-01]
            # [7.65917063e-01   6.55036807e-01   9.66166973e-01   8.59221101e-01]
            # [2.63409168e-01
            # 1.62346125e-01
            # 9.27784562e-01
            # 4.70638990e-01]
            # [2.23505557e-01   2.56216645e-01   9.54036653e-01   6.96712375e-01]
            # [6.70895576e-01
            # 1.38236970e-01
            # 7.69492984e-01
            # 1.66339576e-01]
            # [2.44334549e-01   1.58347636e-02   8.91730785e-01   4.85886276e-01]
            # [8.26819837e-01
            # 7.18856514e-01
            # 9.06503141e-01
            # 8.34951460e-01]
            # [6.53106868e-01   2.28239954e-01   7.41801560e-01   3.53568316e-01]
            # [8.48088503e-01
            # 7.34943449e-02
            # 9.92168903e-01
            # 1.58813402e-01]
            # [9.20053363e-01   5.98525226e-01   9.94040489e-01   7.07560360e-01]
            # [6.74306452e-01
            # 4.05299515e-01
            # 9.82243478e-01
            # 5.83256483e-01]
            # [6.48979604e-01   1.81494653e-03   1.00000000e+00   2.43716046e-01]
            # [4.09931123e-01
            # 2.02223435e-02
            # 8.05424750e-01
            # 1.47238284e-01]
            # [3.05538476e-01   3.23820710e-02   6.30053639e-01   4.46364373e-01]
            # [6.57227337e-01
            # 2.70195305e-04
            # 9.04079735e-01
            # 2.43534055e-02]
            # [6.22564614e-01   1.33069187e-01   9.85441744e-01   5.40563226e-01]
            # [2.52565712e-01
            # 3.18843797e-02
            # 8.06461453e-01
            # 2.30569243e-01]
            # [7.89971769e-01   0.00000000e+00   9.66980755e-01   1.71081960e-01]
            # [8.41533661e-01
            # 5.00915766e-01
            # 1.00000000e+00
            # 1.00000000e+00]
            # [8.56782138e-01   1.45923853e-01   9.91466701e-01   2.15852052e-01]
            # [4.29342628e-01
            # 1.32896826e-02
            # 9.20997381e-01
            # 4.41452563e-02]
            # [7.86960483e-01   6.42244577e-01   8.62439394e-01   7.75912881e-01]
            # [7.20284224e-01
            # 0.00000000e+00
            # 8.89764309e-01
            # 1.64142147e-01]
            # [5.12151420e-01   3.36574018e-03   9.82065976e-01   1.66197479e-01]
            # [4.94888365e-01
            # 3.57887328e-01
            # 6.15545809e-01
            # 3.86628985e-01]
            # [6.08135402e-01   2.21387029e-01   6.48899496e-01   2.51530617e-01]
            # [5.68636358e-01
            # 2.06697181e-01
            # 8.16901147e-01
            # 3.73856068e-01]
            # [6.04478121e-01   3.28873664e-01   7.11622596e-01   3.79092306e-01]
            # [6.79646611e-01
            # 0.00000000e+00
            # 8.43087077e-01
            # 1.58570915e-01]
            # [6.78774059e-01   3.27272326e-01   9.91890132e-01   4.41306740e-01]
            # [8.32164705e-01
            # 2.64483392e-01
            # 9.99865830e-01
            # 4.77592289e-01]
            # [8.07269394e-01   7.14283139e-02   8.98133099e-01   1.60093784e-01]
            # [5.90886295e-01
            # 2.50287801e-01
            # 6.43287122e-01
            # 3.09312552e-01]
            # [7.93670893e-01   2.21211046e-01   1.00000000e+00   3.91851097e-01]
            # [8.42553794e-01
            # 8.20005655e-01
            # 9.04277503e-01
            # 9.03982043e-01]
            # [7.96919346e-01   1.48203477e-01   9.27457571e-01   2.09697500e-01]
            # [8.17582965e-01
            # 3.17820758e-01
            # 9.92344618e-01
            # 4.49741393e-01]
            # [2.67845869e-01   4.32047248e-02   9.32597041e-01   8.42114151e-01]
            # [3.00255984e-01
            # 6.00171983e-01
            # 1.00000000e+00
            # 1.00000000e+00]
            # [7.31533885e-01   6.66146725e-02   8.92157912e-01   3.24316323e-01]
            # [2.85993367e-01
            # 8.04535866e-01
            # 7.94510484e-01
            # 9.93633270e-01]
            # [6.51734412e-01   4.03899550e-01   9.91533577e-01   5.78818321e-01]
            # [2.93439656e-01
            # 3.41495842e-01
            # 9.25386786e-01
            # 5.58921456e-01]
            # [6.38388038e-01   3.88189852e-01   9.02189612e-01   5.48720121e-01]
            # [8.09302986e-01
            # 4.21325207e-01
            # 9.65256155e-01
            # 4.80541527e-01]
            # [5.32702625e-01   5.06039523e-03   1.00000000e+00   4.48769480e-02]
            # [9.50426102e-01
            # 9.04067457e-02
            # 9.98136997e-01
            # 1.68715268e-01]
            # [7.94026673e-01   3.18204850e-01   9.90994394e-01   4.32918876e-01]
            # [6.31420732e-01
            # 2.03433111e-01
            # 6.99017763e-01
            # 2.48129115e-01]
            # [7.99338639e-01   0.00000000e+00   9.78179753e-01   3.31633836e-02]
            # [7.90307283e-01
            # 8.23676944e-01
            # 8.54419827e-01
            # 9.00860071e-01]
            # [7.80439079e-01   1.31152034e-01   1.00000000e+00   3.06781709e-01]
            # [5.99425316e-01
            # 2.74388313e-01
            # 9.09430504e-01
            # 4.11148906e-01]
            # [7.65983462e-01   2.84347028e-01   9.89693165e-01   4.20870751e-01]
            # [8.23001087e-01
            # 1.13459289e-01
            # 9.94158089e-01
            # 3.89429629e-01]
            # [6.25042796e-01   2.14452773e-01   8.79753590e-01   3.83538455e-01]
            # [8.26434493e-01
            # 4.88047823e-02
            # 1.00000000e+00
            # 1.95877224e-01]
            # [8.34437311e-01   4.76108789e-02   9.99206364e-01   3.25301915e-01]
            # [6.79351866e-01
            # 4.03250039e-01
            # 8.31701219e-01
            # 4.93081272e-01]
            # [3.46749902e-01   9.97863710e-03   7.74508357e-01   4.33152057e-02]
            # [9.10294473e-01
            # 6.55500412e-01
            # 9.95485246e-01
            # 7.51419783e-01]
            # [7.23021209e-01   4.68390346e-01   9.82381999e-01   6.18049383e-01]
            # [8.45210493e-01
            # 3.69765610e-01
            # 1.00000000e+00
            # 9.91415977e-01]
            # [7.42070973e-01   1.44468807e-03   9.27310288e-01   2.76696868e-02]
            # [6.77552044e-01
            # 7.11859912e-02
            # 8.45951021e-01
            # 3.03862095e-01]
            # [4.61866736e-01   9.43394363e-01   8.19630861e-01   9.94388759e-01]
            # [5.31370699e-01
            # 3.75910282e-01
            # 6.64116442e-01
            # 4.14220691e-01]
            # [5.01824975e-01   4.19312809e-03   7.55396605e-01   2.06644498e-02]
            # [7.16367006e-01
            # 2.38079429e-01
            # 7.85908222e-01
            # 3.60712349e-01]
            # [8.63201439e-01   5.44769168e-01   9.64279354e-01   5.99739194e-01]
            # [6.38712764e-01
            # 3.98197770e-01
            # 7.75014043e-01
            # 4.93560851e-01]
            # [9.58309233e-01   1.19525298e-01   9.97892201e-01   2.63653278e-01]
            # [4.41503257e-01
            # 2.13102579e-01
            # 7.43152261e-01
            # 3.64955068e-01]
            # [6.95687473e-01   1.19917080e-01   9.90951598e-01   2.73282468e-01]
            # [3.38222921e-01
            # 0.00000000e+00
            # 7.35024154e-01
            # 5.03624558e-01]
            # [6.75179005e-01   2.22492054e-01   9.73046303e-01   3.82892072e-01]
            # [7.90715754e-01
            # 1.26844496e-02
            # 9.79999244e-01
            # 2.05159590e-01]
            # [5.28232098e-01   1.74262375e-02   9.77141500e-01   3.71109068e-01]
            # [8.76232862e-01
            # 4.12731022e-01
            # 9.86811876e-01
            # 4.85727280e-01]
            # [1.52592361e-01   5.32040954e-01   9.57127154e-01   9.93209720e-01]
            # [7.69277573e-01
            # 4.19288486e-01
            # 8.84642243e-01
            # 4.72922891e-01]]]
            # print('scores: ' + str(scores))
            # scores: [[0.92973822  0.39686394  0.17461708  0.14730477  0.11827202  0.11242164
            #           0.10726039  0.09607999  0.08559249  0.08192549  0.08175166  0.07791726
            #           0.07776562  0.07772722  0.07752729  0.07097574  0.06930999  0.06887712
            #           0.06874228  0.06843274  0.06679926  0.06292398  0.06082833  0.05999289
            #           0.05997828  0.05941917  0.05905463  0.05751398  0.05682041  0.05672655
            #           0.05610438  0.05559316  0.0542715   0.05383616  0.0537176   0.05358627
            #           0.05263264  0.05200152  0.05094003  0.05056275  0.05009294  0.05000618
            #           0.04970911  0.04970011  0.04968807  0.04891298  0.04818729  0.04790786
            #           0.04729499  0.04646889  0.04642607  0.04619163  0.04606514  0.0459594
            #           0.04544649  0.0453539   0.04523933  0.04486589  0.04464923  0.0446334
            #           0.04414469  0.04389279  0.04363523  0.04328584  0.04321729  0.0432079
            #           0.04303761  0.04294647  0.04274838  0.04269595  0.0424169   0.04240253
            #           0.04201635  0.04187248  0.04176852  0.04155673  0.04112948  0.04108905
            #           0.04094079  0.04072878  0.04056267  0.04009283  0.03961392  0.03932149
            #           0.0392894   0.03922085  0.03887592  0.03875808  0.03849145  0.03841605
            #           0.03839261  0.03832981  0.03828708  0.03827956  0.03817309  0.03799195
            #           0.03747408  0.03742593  0.03732589  0.03728329]]
            # print('classes: ' + str(classes))
            # classes: [[1.  65.  62.  54.  62.  54.  62.  82.  77.  54.  44.  65.  65.  54.
            #            62.  62.  62.  54.  65.  54.  54.   1.   1.  44.  72.  54.  32.  62.
            #            84.   1.  62.  72.  62.  62.   1.  72.  62.  65.  62.   1.  54.  62.
            #            62.  77.  77.  32.  77.  62.  31.   1.  62.  77.  62.  54.  62.  62.
            #            1.  65.  67.  82.  62.   1.  62.  62.   1.  62.   1.  77.  62.  54.
            #            62.  32.  27.  62.  32.  62.  62.  62.   1.  84.  62.  67.  62.  67.
            #            82.  77.   1.  32.  62.  62.  62.  77.   1.  62.  32.  67.   3.  62.
            #            1.  62.]]
            # print('num: ' + str(num))
            # num: [100.]
            # print([category_index.get(i) for i in classes[0]])
            # print(scores)
            img.set_data(cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB))
            # print([n.name for n in tf.get_default_graph().as_graph_def().node])
            if plt.get_fignums():
                fig.canvas.draw()
                fig.canvas.flush_events()
                plt.show(block=False)
            t.set_text(f'{cap.fps():{0}.{3}}')
