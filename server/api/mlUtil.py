import cv2
import numpy as np
import distutils.util
from collections import namedtuple
import json
import socket
from datetime import datetime

def to_bool(bool_str):
    zero_or_one = distutils.util.strtobool(bool_str)
    as_boolean = bool(zero_or_one)
    return as_boolean

# addBoxToImage_tpu()
# Replacement for addBoxToImage_coral and addBoxToImage_mac which handled different model return values
# This works the same for a Coral Board or TPU accelerator (USB)
def addBoxToImage_tpu(tracked_objects_with_scores, image, label_dict, threshold):
    # tracked_objects_with_scores
    # box(x,y,x,y), tracking_id, prob, class_id  //box is absolute coords
    for obj in tracked_objects_with_scores:
        (x1, y1, x2, y2, tracking_id, prob, class_id) = obj

        x1 = int(x1)
        y1 = int(y1)
        x2 = int(x2)
        y2 = int(y2)

        # Use different box colors for above and below submission threshold
        if prob > threshold:
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 3) #BGR
        else:
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), 3) #BGR


        class_name = ""
        if int(class_id) in label_dict:
            class_name =  label_dict[int(class_id)]

        tracking_id_msg = 'ID: ' + str(int(tracking_id))
        prob_msg = '{0: .6f}'.format(prob)
        class_name_msg = ' (' + class_name + ')'
        msg = tracking_id_msg + ' ' + prob_msg + class_name_msg
        cv2.putText(image, msg, (x1 + 4, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (50, 50, 50), 1)

# This has been replaced by the TPU version above.
def addBoxToImage_coral(detections, id_score_dict, image, label_dict):
    # BOX =  (166.58152161892377, 311.63916369319213, 406.15092130497857, 517.0355224806976)

    for obj in detections:
        (x1, y1, x2, y2, id) = obj # orig
        x1 = int(x1)
        y1 = int(y1)
        x2 = int(x2)
        y2 = int(y2)
        image = cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 3)  # BGR

        if id in id_score_dict:
            (score, class_id) = id_score_dict[id]
            score_string = " {0: .6f}".format(score)

        class_name = ""
        if int(class_id) in label_dict:
            class_name =  label_dict[int(class_id)]
            #print("Category: ", class_name)

        msg = "ID = " + str(int(id)) + " " + class_name

        image = cv2.putText(image, msg, (x1 + 4, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 255, 255), 1)
        image = cv2.putText(image, score_string, (x1 + 4, y2 + 5), cv2.FONT_HERSHEY_SIMPLEX, .5, (255, 0, 255), 1)

    return image

# This has been replaced by the TPU version above.
def addBoxToImage_mac(detections, id_score_dict, image, label_dict):
    # BOX =  (0.4563725973610336, 0.4426787346480987, 0.6329397881610903, 0.8018401205314909)
    absolute_detections = []
    for obj in detections:
        [h, w] = image.shape[:2]
        box = convert_relative_to_absolute_coordinates(obj, h, w)
        absolute_detections.append(box)
    addBoxToImage_coral(absolute_detections, id_score_dict, image, label_dict)


def convert_relative_to_absolute_coordinates_new(box, h, w):
    (x1, y1, x2, y2) = box
    x1 = int(x1 * w)
    y1 = int(y1 * h)
    x2 = int(x2 * w)
    y2 = int(y2 * h)
    return ([x1, y1, x2, y2])

def convert_relative_to_absolute_coordinates_scaled_to_original(box, orig_h, orig_w, resized_h, resized_w):
    (x1, y1, x2, y2) = box
    x_scaling_factor = orig_w / resized_w
    y_scaling_factor = orig_h / resized_h
    x1 = int(x1 * resized_w * x_scaling_factor)
    y1 = int(y1 * resized_h * y_scaling_factor)
    x2 = int(x2 * resized_w * x_scaling_factor)
    y2 = int(y2 * resized_h * y_scaling_factor)
    chip_h = y2 - y1
    chip_w = x2 - x1
    return [x1, y1, x2, y2, chip_h, chip_w]


def convert_relative_to_absolute_coordinates(box, h, w):
    (x1, y1, x2, y2, id) = box
    x1 = int(x1 * w)
    y1 = int(y1 * h)
    x2 = int(x2 * w)
    y2 = int(y2 * h)
    return [x1, y1, x2, y2, id]

def expand_crop_area_relative(x1, y1, x2, y2):

    # TODO: scale the crop expansion based on h and w. Other wise we expand too much for small faces on big imgs
    w = max(x2 - x1, 0)
    h = max(y2 - y1, 0)

    # Detector crop is too tight, so expand the height.
    # This uses floats (relative coords)
    y1_expanded = y1 - (.15 * h)  # bring the to up
    y1 = max(y1_expanded, 0)  # Don't want y1 to be negative
    y2_expanded = y2 + (.15 * h)  # drop the bottom down
    y2 = min(y2_expanded, 1)

    x1_expanded = x1 - (.10 * w)  # Move to left
    x1 = max(x1_expanded, 0)  # Don't want x1 to be negative
    x2_expanded = x2 + (.10 * w) # move to right
    x2 = min(x2_expanded, 1) # Don't go beyond right edge

    return x1, y1, x2, y2

# def expand_crop_area_(x1, y1, x2, y2, h, w):
#     # Detector crop is too tight, so expand the height
#     y1_expanded = int(y1 - .25 * y1)  # bring the to up
#     y1 = max(y1_expanded, 0)  # Don't want y1 to be negative
#     y2_expanded = int(y2 + .15 * y2)  # drop the bottom down
#     y2 = min(y2_expanded, h)
#     return x1, y1, x2, y2

# Computes IUO between two bboxes in the form [x1,y1,x2,y2]
def iou(bb_test,bb_gt):
  xx1 = np.maximum(bb_test[0], bb_gt[0])
  yy1 = np.maximum(bb_test[1], bb_gt[1])
  xx2 = np.minimum(bb_test[2], bb_gt[2])
  yy2 = np.minimum(bb_test[3], bb_gt[3])
  w = np.maximum(0., xx2 - xx1)
  h = np.maximum(0., yy2 - yy1)
  wh = w * h
  o = wh / ((bb_test[2]-bb_test[0])*(bb_test[3]-bb_test[1])
    + (bb_gt[2]-bb_gt[0])*(bb_gt[3]-bb_gt[1]) - wh)
  return(o)


# Print request from requests library http request
def pretty_print_POST(req):
    print('{}\n{}\r\n{}\r\n\r\n{}\r\n{}'.format(
        '--------------------------------- START ---------------------------------',
        req.method + ' ' + req.url,
        '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        req.body,
        '---------------------------------  END  ---------------------------------',
    ))

def _json_object_hook(d):
    return namedtuple('X', d.keys())(*d.values())

def json2obj(data):
    return json.loads(data, object_hook=_json_object_hook)

def get_ip_address():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8',80))
        return s.getsockname()[0]
    except:
        return '0.0.0.0'

def add_frame_number_to_image(image, num):
    cv2.putText(image, 'Frame #{} at {}'.format(num, datetime.now().strftime('%H:%M:%S.%f')[:-3]),(1,25),cv2.FONT_HERSHEY_SIMPLEX,1,(233,17,207),1)