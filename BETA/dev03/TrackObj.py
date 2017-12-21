import numpy as np
import os
import tensorflow as tf
import cv2
from threading import Thread
# from Base.Tensorflow.utils import visualization_utils as vis_util
# from Base.Tensorflow.utils import label_map_util
from BETA.dev03.utils import visualization_utils as vis_util
from BETA.dev03.utils import label_map_util


class WebcamVideoStream:
    def __init__(self, src=1, width=480, height=360):
        # initialize the video camera stream and read the first frame
        # from the stream
        self.stream = cv2.VideoCapture(src)
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        (self.grabbed, self.frame) = self.stream.read()
        # initialize the variable used to indicate if the thread should
        # be stopped
        self.stopped = False

    def start(self):
        # start the thread to read frames from the video stream
        Thread(target=self.update, args=(), daemon=True).start()
        return self

    def update(self):
        # keep looping infinitely until the thread is stopped
        while True:
            # if the thread indicator variable is set, stop the thread
            if self.stopped:
                return
            # otherwise, read the next frame from the stream
            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
        # return the frame most recently read
        return self.frame

    def stop(self):
        # indicate that the thread should be stopped
        self.stream.release()
        self.stopped = True


def order_points(pts):
    # initialzie a list of coordinates that will be ordered
    # such that the first entry in the list is the top-left,
    # the second entry is the top-right, the third is the
    # bottom-right, and the fourth is the bottom-left
    rect = np.zeros((4, 2), dtype="float32")
    # the top-left point will have the smallest sum, whereas
    # the bottom-right point will have the largest sum
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    # now, compute the difference between the points, the
    # top-right point will have the smallest difference,
    # whereas the bottom-left will have the largest difference
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    # return the ordered coordinates
    return rect


def four_point_transform(image, pts):
    # obtain a consistent order of the points and unpack them
    # individually
    rect = order_points(pts)
    (tl, tr, br, bl) = rect
    # compute the width of the new image, which will be the
    # maximum distance between bottom-right and bottom-left
    # x-coordiates or the top-right and top-left x-coordinates
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))
    # compute the height of the new image, which will be the
    # maximum distance between the top-right and bottom-right
    # y-coordinates or the top-left and bottom-left y-coordinates
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))
    # now that we have the dimensions of the new image, construct
    # the set of destination points to obtain a "birds eye view",
    # (i.e. top-down view) of the image, again specifying points
    # in the top-left, top-right, bottom-right, and bottom-left
    # order
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")
    # compute the perspective transform matrix and then apply it
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
    # return the warped image
    return warped

# Global constant names
MODEL_NAME = 'ssd_mobilenet_v1_coco_11_06_2017'
PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb'
PATH_TO_LABELS = os.path.join('data', 'mscoco_label_map.pbtxt')
NUM_CLASSES = 90


# Load label map
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map,
                                                            max_num_classes=NUM_CLASSES,
                                                            use_display_name=True)
category_index = label_map_util.create_category_index(categories)
detection_graph = tf.Graph()
cv2.setUseOptimized(True)
fgbg = cv2.createBackgroundSubtractorMOG2()
cap = WebcamVideoStream().start()
size = 20

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
        while 1:
            image_np = cap.read()
            s = cv2.getTickCount()
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

            # width, height = image_np.shape[:2]
            # ymin = int(boxes[0][0][0] * height)
            # xmin = int(boxes[0][0][1] * width)
            # ymax = int(boxes[0][0][2] * height)
            # xmax = int(boxes[0][0][3] * width)
            # cv2.rectangle(image_np, (xmax, ymax), (xmin, ymin), (0, 0, 255), 2)
            # left = int(144.0395736694336)
            # right = int(492.6529312133789)
            # top = int(7.351409196853638)
            # bottom = int(357.8817844390869)
            # cv2.line(image_np, (left, top), (right, bottom), color=(0, 0, 255), lineType=8, thickness=1, shift=0)
            # cv2.rectangle(image_np, (int(vis_util.left), int(vis_util.top)), (int(vis_util.right), int(vis_util.bottom)), (0, 0, 255), 2)
            roi = image_np[int(vis_util.top):int(vis_util.bottom), int(vis_util.left):int(vis_util.right)]
            roi_w, roi_h = roi.shape[:2]
            # print(roi.shape[:2])
            cv2.rectangle(img=roi,
                          pt1=(int((roi_h / 2) - (size + 1)),
                               int((roi_w / 2) - (size + 1))),
                          pt2=(int((roi_h / 2) + (size + 1)),
                               int((roi_w / 2) + (size + 1))),
                          # pt1=(int((vis_util.left / 2) - (size + 1)),
                          #      int((vis_util.top / 2) - (size + 1))),
                          # pt2=(int((vis_util.right / 2) + (size + 1)),
                          #      int((vis_util.bottom / 2) + (size + 1))),
                          # pt1=(int(roi_w / 2),
                          #      int(roi_h / 2)),
                          # pt2=(int(roi_w / 2),
                          #      int(roi_h / 2)),
                          color=(255, 255, 255),
                          thickness=1,
                          lineType=cv2.LINE_AA,
                          shift=0)
            # be = fgbg.apply(roi)
            # res = cv2.bitwise_and(roi, roi, mask=be)
            f = cv2.getTickCount()
            cv2.putText(img=image_np,
                        text='fps: {:.2f}'.format(cv2.getTickFrequency()/(f-s)),
                        org=(0, 15),
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=0.5,
                        color=(255, 255, 255),
                        thickness=1,
                        lineType=cv2.LINE_AA,
                        bottomLeftOrigin=False)
            cv2.imshow('image', image_np)
            cv2.imshow('roi', roi)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cap.stop()
                cv2.destroyAllWindows()
                break
# partition the pixels in rectangle
