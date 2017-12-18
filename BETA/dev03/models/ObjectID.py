import os
from Base.Tensorflow.utils import label_map_util

MODEL_NAME = 'ssd_mobilenet_v1_coco_11_06_2017'
PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb'
PATH_TO_LABELS = os.path.join('data', 'mscoco_label_map.pbtxt')
NUM_CLASSES = 90
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map,
                                                            max_num_classes=NUM_CLASSES,
                                                            use_display_name=True)
category_index = label_map_util.create_category_index(categories)


def object_id(q, score, cind, mode=None):
    certainty = str(int(-(-(score * 100) // 1)))
    name = category_index.get(cind).get('name')
    if mode == 1:
        mesg = 'I am ' + certainty + ' percent sure that the object is a ' + name
        mesg.replace(' a ', ' an ') if name[0] in ['a', 'e', 'i', 'o', 'u'] else mesg
    else:
        mesg = name
    return q.put(mesg)
