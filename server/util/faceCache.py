
import datetime

class FaceCacheItem(object):
    def __init__(self, id, score, class_id, box, frame,
                 mx_offset_milliseconds=0,
                 mx_left_eye_x = None,
                 mx_left_eye_y = None,
                 mx_right_eye_x = None,
                 mx_right_eye_y = None,
                 mx_pitch = None,
                 mx_roll = None,
                 mx_yaw = None,
                 mx_uri = None,
                 mx_orig_frame_h = None,
                 mx_orig_frame_w = None,
                 mx_resize_frame_h = None,
                 mx_resize_frame_w = None):

        self.id = id
        self.score = score
        self.class_id = class_id
        self.box = box
        self.frame = frame
        self.timestamp = datetime.datetime.now() #date orig entered
        self.lastseen = datetime.datetime.now()
        self.lastsubmit = None
        self.submit_count = 0
        # MX REST API VALUES
        self.mx_left_eye_x = None
        self.mx_left_eye_y = None
        self.mx_right_eye_x = None
        self.mx_right_eye_y = None
        self.mx_pitch = None
        self.mx_roll = None
        self.mx_yaw = None
        self.mx_offset_milliseconds = mx_offset_milliseconds
        self.mx_uri = None
        self.mx_orig_frame_h = mx_orig_frame_h
        self.mx_orig_frame_w = mx_orig_frame_w
        self.mx_resize_frame_h = mx_resize_frame_h
        self.mx_resize_frame_w = mx_resize_frame_w

    def print(self):
        print(self.id, self.class_id, self.score, self.box, self.timestamp, self.lastsubmit, self.frame.shape)

    def printSummary(self):
        print(self.id, "\t score =", "{0:.6f}".format(self.score), "timestamp = ", self.timestamp, "lastsubmit =", self.lastsubmit, " submit_count =", self.submit_count)


class FaceCache(object):
    def __init__(self):
        self.dict = {}
        self.removed_items_dict = {}

    def add(self, id, face):
        self.dict[id] = face

    def delete(self, id):
        self.dict.pop(id, None)
        self.removed_items_dict[id] = True

    def delete_frame(self, id):
        self.dict[id].frame = None

    def get(self, id):
        if id in self.dict:
            return(self.dict[id])
        else:
            return None

    def print(self):
        print("Length = ", len(self.dict))
        for id, face in self.dict.items():
            face.printSummary()
