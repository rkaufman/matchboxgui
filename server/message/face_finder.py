import pathlib
main_path = pathlib.Path(__file__).parent.parent.absolute()
import sys
if main_path not in sys.path:
    sys.path.append(str(main_path))
import os
os.chdir(main_path)
import platform
import socket
import cv2
import numpy as np
import PIL
import imutils
import time
import util.detect as detect
import util.faceCache
import traceback
import threading
import imagezmq
import itertools
import tflite_runtime.interpreter as tflite
from db import db
from util import mlconstants, mlUtil
#from message.camera_manager import CameraSender
from status import Status
from status_type import StatusType
from decimal import Decimal
from util.model_type import ModelType
from PIL import Image
from threading import Thread
from message.queue_manager import QueueManager
from multiprocessing import freeze_support
from libs.sort import *
from processFaceCache import ProcessFaceCache
from datetime import datetime
from imutils.video import VideoStream

# Platform dependent runtime libraries that drive TPU
EDGETPU_SHARED_LIB = {
  'Linux': 'libedgetpu.so.1',
  'Darwin': 'libedgetpu.1.dylib',
  'Windows': 'edgetpu.dll'
}[platform.system()]

tracking_max_age = db.get_setting('tracking-max-age').setting
tracking_min_hits = db.get_setting('tracking-min-hits').setting

mot_tracker = Sort(max_age=tracking_max_age, min_hits=tracking_min_hits)


class FaceFinder():
    def __init__(self, hasTpu = True,cam_host = None, cam_port = None, image_queue_host = None, image_queue_port = None, msg_queue_host = None, msg_queue_port = None):
        self._stop_event = threading.Event()
        self._shutdown_event = threading.Event()
        if cam_host is None:
            self._cam_host = mlconstants.HOST_IP
        else:
            self._cam_host = cam_host
        if cam_port is None:
            self._cam_port = mlconstants.CAMERA_IMAGE_SENDING_PORT
        else:
            self._cam_port = cam_port
        if image_queue_host is None:
            self._image_queue_host = mlconstants.HOST_IP
        else:
            self._image_queue_host = image_queue_host
        if image_queue_port is None:
            self._image_queue_port = mlconstants.FACE_FINDER_IMAGE_SENDING_PORT
        else:
            self._image_queue_port = image_queue_port
        if msg_queue_host is None:
            self._msg_queue_host = mlconstants.HOST_IP
        else:
            self._msg_queue_host = msg_queue_host
        if msg_queue_port is None:
            self._msg_queue_port = mlconstants.MESSAGE_HUB_PORT
        else:
            self._msg_queue_port = msg_queue_port
        self._msg_connected = False
        self._hasTpu = hasTpu
        self._face_cache = util.faceCache.FaceCache()
        self._id_scores_dict = {}
        self._process_face_cache_thread = ProcessFaceCache(self._face_cache, self._id_scores_dict)
        self._msg_thread = threading.Thread(target=self._msg, args=())
        self._msg_thread.daemon = False
        self._capture = None
        #self._camera_thread = threading.Thread(target=self._start_cam_thread, args=())
        #self._camera_thread.daemon = False
        #self._camera_thread.start()
        self._send_to_gui = False
        self._jpeg_quality = 95
        self._subscriber = None
        self._running = False
        self._face_finding_thread = threading.Thread(target=self._find_faces, args=())
        self._face_finding_thread.daemon = False
        self._gui_sender = None
        self._auto_restart = db.get_setting('auto-restart-stream').setting
        dbStatus = db.get_status('StatusType.STREAM')
        self._data = None
        self._data_ready = threading.Event()
        self._camera_queue = None
        timeout = time.time() + 15
        QueueManager.register("face_finder_queue")
        QueueManager.register('camera_queue')
        mgr = QueueManager(address=(self._msg_queue_host, int(self._msg_queue_port)),authkey='abc'.encode('utf-8'))
        while self._msg_connected == False and not self._shutdown_event.isSet():
            try:
                mgr.connect()
                self._msg_queue = mgr.face_finder_queue()
                self._camera_queue = mgr.camera_queue()
                self._msg_connected = True
                if time.time() > timeout:
                    TimeoutError()
            except TimeoutError:
                print('Failed to connect to message thread in allotted time')
            except Exception as mex:
                traceback.print_exc()
        if self._auto_restart == 'True' or dbStatus.status == 'True':
            self._camera_queue.put('start')
            self.start()
        else:
            self.start_msg()
    @property
    def is_shutdown(self):
        return self._shutdown_event.isSet()
        
    def _msg(self):
        print('Starting message thread waiting on start message')
        if self._shutdown_event.isSet():return
        while not self._shutdown_event.isSet():
            if self._msg_queue.empty():
                time.sleep(5.0)
            else:
                msg = self._msg_queue.get()
                print(msg)
                if(msg == 'stop'):
                    if not self._running:
                        continue
                    self.stop()
                elif msg == 'shutdown':
                    if not self._running:
                        continue
                    self.shutdown()
                elif msg == 'show':
                    self._send_to_gui = True
                elif msg == 'stop_show':
                    self._send_to_gui = False
                elif msg == 'start':
                    print('starting face finder')
                    if self._running:
                        continue
                    self.start()
                    break

    #def _start_cam_thread(self):
        #self._subscriber = CameraSender()
        #while not self._subscriber.shutdown:
            #pass

    def receive(self, timeout=15.0):
        flag = self._data_ready.wait(timeout=timeout)
        if not flag:
            print("Face finder flag is not")
        self._data_ready.clear()
        return self._data

    def stop(self):
        self._running = False
        self._stop_event.set()
        try:
            self._process_face_cache_thread.stop()
            self._process_face_cache_thread = None
        except Exception as pfcex:
            traceback.print_exc()
        self._face_finding_thread = None
        self._face_cache = None
        self._id_scores_dict = {}
        self._data = None
        self._capture.stop()
        self._capture = None
        #on a stop we want to restart the msg loop to wait for a start
        self._msg_thread = threading.Thread(target=self._msg, args=())
        self._msg_thread.start()
        db.update_status(Status(StatusType.STREAM, False, ''))

    def shutdown(self):
        self.stop()
        self._shutdown_event.set()
        if self._gui_sender is not None:
            self._gui_sender.close()
            self._gui_sender = None        

    def start(self):
        try:
            self._shutdown_event.clear()
            self._stop_event.clear()
            if self._face_cache is None:
                self._face_cache = util.faceCache.FaceCache()
            #if not self._camera_thread.isAlive():
                #self._camera_thread = None
                #self._camera_thread = threading.Thread(target=self._start_cam_thread, args=())
                #self._camera_thread.daemon = False
                #self._camera_thread.start()
            #delay for camera to start and send frames
            time.sleep(2.0)
            if self._process_face_cache_thread is None:
                self._process_face_cache_thread = ProcessFaceCache(self._face_cache, self._id_scores_dict)
            if self._face_finding_thread is None:
                self._face_finding_thread = threading.Thread(target=self._find_faces, args=())
            self._face_finding_thread.start()
            self._running = True
            print('started face finding thread')
        except Exception as ffe:
            print("Failed to start ff thread")
            print(ffe)
            traceback.print_exc()
            self._stop_event.set()
            self._process_face_cache_thread.stop()
            self._shutdown_event.set()
            print("ff thread completed with exception")

    def start_msg(self):
        try:
            self._shutdown_event.clear()
            if not self._msg_thread.is_alive():
                self._msg_thread.start()
        except Exception as mtex:
            traceback.print_exc()

    def send_to_gui(self):
        self._send_to_gui = True

    def _find_faces(self):
        print("starting face finder")
        
        coco_labels = ""
        labels_to_detect = {}
        # detector_face = tfFaceDetector.TensoflowFaceDetector(mlconstants.CPU_FACE_MODEL_PATH)
        ###detector_coco = tfFaceDetector.TensoflowFaceDetector(mlconstants.CPU_COCO_MODEL_PATH) # model opens with error
        detector_coco = None
        # detector_lpr  = tfFaceDetector.TensoflowFaceDetector(mlconstants.CPU_ALPR_MODEL_PATH)
        coco_labels = mlconstants.CPU_COCO_LABEL_PATH
        labels_to_detect = mlconstants.CPU_LABELS_TO_DETECT

        # TPU: If this device has a TPU chip (a Coral board or a workstation with a USB TPU dongle,
        # Then we can load the library that will handle the inference and use the TPU.
        # With no TPU, we are using the same interpreter library, but initiating it without an execution delegate.
        # The interpreter requires a tflite model in either case (not a .pb file) but the model for the TPU would
        # be compiled for the TPU and wouldn't necessarily run on the non-TPU environment.
        #
        # In non-TPU example below (has_tpu = False) we just usee an example coco detector, not a face detector.
        # TODO: should this load driver process be moved earlier, like class init. Or even before user clicks start.
        if self._hasTpu:
            try:
                graph_execution_delegate = [tflite.load_delegate(EDGETPU_SHARED_LIB)]
                model_path = mlconstants.TPU_FACE_MODEL_PATH
            except Exception as e:
                print("TPU access error. Is the TPU accessible? If this is an external TPU is it connected? Try to reconnect it. Error:", e)
                sqlitedb.add_log('An error occured trying to load the model.')
                return
        else:
            print('Unsupported processor no TPU installed.')
            return

        interpreter = tflite.Interpreter(
                                model_path=model_path,
                                experimental_delegates=graph_execution_delegate
                            )
        interpreter.allocate_tensors()
        

        label_dict = {} # dict int:string (class id int : class text string)
        with open(coco_labels) as f:
            lines = f.read().splitlines()

        for line in lines:
            linelist = line.split(None, 1)
            label_dict[int(linelist[0])] = linelist[1]

        db.update_status(Status(StatusType.STREAM, True, ''))

        tracking_min_iou = Decimal(sqlitedb.get_setting('tracking-min-iou').setting)
        resize_image_before_prediction = mlUtil.to_bool(sqlitedb.get_setting('resize-image-before-prediction').setting)
        resize_image_width = int(sqlitedb.get_setting('resize-image-width').setting)
        detection_threshold = Decimal(sqlitedb.get_setting('detection-thrshl').setting) # only DETECT objects > than this
        submit_threshold = Decimal(sqlitedb.get_setting('min-face-qual-score').setting) / 10 # only SUBMIT objs > than this
        max_objects_to_detect = int(sqlitedb.get_setting('max-objects-to-detect').setting)
        max_faces_to_submit_while_tracking = int(sqlitedb.get_setting('max-faces-to-submit-while-tracking').setting)

        framecount = 0
        missed_consecutive_frames = 0
        #if self._subscriber is None:
            #self._subscriber = VideoStreamSubscriber(self._cam_host, self._cam_port)
        
        try:
            if(self._process_face_cache_thread.is_alive()):
                self._process_face_cache_thread.run()
            else:
                try:
                    self._process_face_cache_thread.start()
                except:
                    self._face_cache = util.faceCache.FaceCache()
                    self._process_face_cache_thread = ProcessFaceCache(self._face_cache, self._id_scores_dict)
                    self._process_face_cache_thread.start()
        except Exception as pe:
            msg = "Error with face cache thread"
            print(msg)
            db.add_log(msg)
            traceback.print_exc()
            self.shutdown()
        try:
            if self._gui_sender is None:
                pass
                #self._gui_sender = imagezmq.ImageSender(connect_to="tcp://{}:{}".format(self._image_queue_host, self._image_queue_port), REQ_REP=False)
        except imagezmq.zmq.ZMQError as zer:
            print(zer)
            traceback.print_exc()
        #try:
            #self._camera_thread.start()
            #time.sleep(3.0)
            #self._camera_queue.put('start')
        #except:
            #print('camera error')

        #add cv2 stuff to read from camera
        self._cam_url = db.get_setting('rtsp-url').setting
        if not self._cam_url or not self._cam_url.strip():
            self._capture = VideoStream()
        else:
            self._capture = VideoStream(self._cam_url)
        self._capture.start()
        try:
            while not self._stop_event.isSet():
                if not self._msg_queue.empty():
                    msg = self._msg_queue.get()
                    print(msg)
                    if(msg == 'stop'):
                        if self._running:
                            self.stop()
                            break
                    elif msg == 'shutdown':
                        self.shutdown()
                        break
                    elif msg == 'show':
                        self._send_to_gui = True
                    elif msg == 'stop_show':
                        self._send_to_gui = False
                
                framecount += 1
                msg = "----------------------------------------------------> FRAME {}".format(framecount)
                if framecount % 100 == 0:
                   db.add_log("Processing video frames")

            
                data = self._capture.read()
                if data is None:
                    continue
                img = data
                #sqlitedb.rec_frame(num)
                print('Got new frame number from camera {} at {}'.format(framecount,datetime.now().strftime('%H:%M:%S.%f')[:-3]))
                
                frame = data
                if frame is None:
                    time.sleep(mlconstants.MISSED_FRAME_DELAY)
                    continue

                # Resize frame before prediction. May reduce preciction time, but postentially decrease accuracy
                if frame is not None and resize_image_before_prediction is True:
                    if resize_image_width > 0:
                        frame = imutils.resize(frame, width=resize_image_width)

                boxes_and_scores_final = np.zeros(shape=(1, 6))
                
                # Face
                if ModelType.face in mlconstants.MODELS_TO_RUN:
                    # TPU detector
                    pil_img = PIL.Image.fromarray(frame) # Convert numpy array to PIL Image
                    scale = detect.set_input(interpreter, pil_img.size, lambda size: pil_img.resize(size, Image.ANTIALIAS))
                    interpreter.allocate_tensors()
                    interpreter.invoke()
                    detectd_objects = detect.get_output(interpreter, detection_threshold, scale)
                    # print('detected object count:{}'.format(len(detectd_objects)))

                    for face in detectd_objects:
                        x1, y1, x2, y2 = face.bbox
                        singleobj = np.array([x1, y1, x2, y2, face.score, 777])
                        boxes_and_scores_final = np.vstack((boxes_and_scores_final, singleobj))

                    # Dummy label file: TODO: see if we can use an empty dict
                    labels =  {
                        "one": "1111",
                        "two": "2222"
                    }

                    # Filter out low scored
                    #   Don't need to do this as detection algorithm is
                    #   filtering min detect and min submit is filtered before submitting
                    # boxes_and_scores_filtered_face = np.array(
                    #     [row for row in boxes_and_scores_final if row[4] > detection_threshold])

                    # num_faces = boxes_and_scores_final.shape[0] # shape looks like: (1, 6). where 1 is num faces
                    # if num_faces > 1: # there is always our blank row
                    #     boxes_and_scores_final = np.append(boxes_and_scores_final, boxes_and_scores_filtered_face, axis=0)

                # COCO
                if ModelType.coco in mlconstants.MODELS_TO_RUN:
                    print("MODEL TO RUN = COCO")
                    (boxes, scores, classes, num_detections) = detector_coco.run(frame)

                    class_array = [[item] for item in classes[0]]  # convert to list of lists
                    scores_array = [[item] for item in scores[0]]  # convert to list of lists

                    boxes_and_scores = np.concatenate((np.array(boxes[0]), scores_array, class_array), axis=1)

                    boxes_and_scores_filtered_coco = np.array(
                        [row for row in boxes_and_scores if row[4] > detection_threshold])

                    if boxes_and_scores_filtered_coco.size > 0:
                        boxes_and_scores_final = np.append(boxes_and_scores_final, boxes_and_scores_filtered_coco, axis=0)

                # LPR
                # if ModelType.lpr in mlconstants.MODELS_TO_RUN:
                #     print("MODEL TO RUN = LPR")
                #     (boxes, scores, classes, num_detections) = detector_lpr.run(image)
                #     class_array = np.full((len(scores[0]), 1), mlconstants.LPR_CLASS_ID, dtype=int) # Add class
                #     scores_array = [[item] for item in scores[0]]  # convert to list of lists
                #     boxes_and_scores = np.concatenate((np.array(boxes[0]), scores_array, class_array), axis=1)
                #     boxes_and_scores_filtered_lpr = np.array(
                #         [row for row in boxes_and_scores if row[4] > detection_threshold])
                #
                #     if boxes_and_scores_filtered_lpr.size > 0:
                #         boxes_and_scores_final = np.append(boxes_and_scores_final, boxes_and_scores_filtered_lpr, axis=0)


                # ==============================================================================
                # Process Detections
                # ==============================================================================
                # Filter out zeros added as part of empty array creation
                boxes_and_scores_final = np.array(
                    [row for row in boxes_and_scores_final if row[4] > 0])

                # INPUT:  Boxes and scores --> OUTPUT: Boxes and IDs (we lose the scores)
                # TODO: This tracking process (mot_tracker.update()) loses the scores, hence the
                #  array below (ids_and_scores = [], which ties these together. This could be improved
                #  by modifiying the mot_tracker to return the scores as well as IDs)
                #print('boxes and final scores length: {}'.format(boxes_and_scores_final.shape[0]))
                if boxes_and_scores_final.shape[0] > 0:
                    tracked_objects_FROM_TRACKER = mot_tracker.update(boxes_and_scores_final[:,:5])
                else:
                    # Nothing tracked so skip rest of loop, but first display image
                    #yield cv2.imencode('.jpg', image)[1].tobytes()
                    if self._send_to_gui:
                        # print('Sending frame {} to GUI at {}'.format(num, datetime.now().strftime('%H:%M:%S.%f')[:-3]))
                        #sqlitedb.send_frame(num)
                        #self._gui_sender.send_jpg(num, cv2.imencode('.jpg', frame)[1].tobytes())
                        #mlUtil.add_frame_number_to_image(frame,num)
                        self._data = (framecount, cv2.imencode('.jpg', frame)[1].tobytes())
                        self._data_ready.set()
                    continue

                # IDs & Scores ------------------------------- start -------------------------------
                # Create list of ids & scores.
                ids_and_scores = []

                # Create every possible combo of pairs (detections and tracks)
                for r in itertools.product(boxes_and_scores_final, tracked_objects_FROM_TRACKER):
                    # print("R1", r[1])
                    # print("R0", r[0])
                    (_, _, _, _, id) = r[1]
                    (_, _, _, _, prob, class_id) = r[0]
                    # Then calculate IOU
                    overlap = mlUtil.iou(r[0], r[1])
                    # list of all io/scores/overlap
                    ids_and_scores.append((int(id), prob, class_id, overlap))

                # Filter out low IOS's
                ids_and_scores = np.array([row for row in ids_and_scores if row[3] > tracking_min_iou])
                # Add scores to tracked objects
                tracked_objects_with_scores = []
                if len(ids_and_scores) > 0:
                    db.update_status(Status(StatusType.FACEFIND, True, ''))
                    for row in ids_and_scores:
                        self._id_scores_dict[row[0]] = (row[1], row[2])

                    
                    # tracked_objects_with_scores: [x1, y1, x2, y2, tracking_id, prob, class_id]  //x1,y1,x2,y2=absolute coords
                    print('self._id_scores_dict length {}'.format(len(self._id_scores_dict)))
                    if len(self._id_scores_dict) != 0:
                        for item in tracked_objects_FROM_TRACKER:
                            id = item[4]
                            if id in self._id_scores_dict:
                                (prob, class_id) = self._id_scores_dict[id]
                                item = np.append(item, prob)
                                item = np.append(item, class_id)
                                tracked_objects_with_scores.append(item)
                # IDs & Scores -------------------------------  end  -------------------------------


                    # FaceCache ------------------------------- start -------------------------------
                    faceCache_lock = threading.Lock()

                    with faceCache_lock:
                        if len(tracked_objects_with_scores) > 0:
                            for trackedFace in tracked_objects_with_scores:
                                (new_x1, new_y1, new_x2, new_y2, new_id, new_score, new_class_id) = trackedFace
                                new_id = int(new_id) # tracker returns floats, convert ID to int
                                new_class_id = int(new_class_id)

                                # Note: Image deep copy so the faces cropped and sent to MX don't have boxes printed on them
                                original_image = np.copy(frame)
                                trackedFaceItem = util.faceCache.FaceCacheItem(new_id, new_score, new_class_id,(new_x1, new_y1, new_x2, new_y2), original_image)

                                existing_face = self._face_cache.get(new_id)
                                if existing_face is not None:
                                    # We have an existing face
                                    if existing_face.submit_count < max_faces_to_submit_while_tracking:
                                        old_score = existing_face.score
                                        if new_score > old_score:
                                            # If it's better add it; preserve original timestamp & submit_count
                                            trackedFaceItem.timestamp = existing_face.timestamp
                                            trackedFaceItem.submit_count = existing_face.submit_count
                                            self._face_cache.add(new_id, trackedFaceItem)
                                            print(new_id, "<----->", trackedFaceItem)
                                else:
                                    # New face so add it
                                    #   But only add if the ID has not already been removed. This could happen
                                    #   if the face hit the limit on MAX_FACES_TO_SUBMIT_WHILE_TRACKING and got
                                    #   deleted from the cache, but is still being tracked.
                                    if new_id not in self._face_cache.removed_items_dict:
                                        self._face_cache.add(new_id, trackedFaceItem)
                if not self._send_to_gui:
                    continue
                mlUtil.addBoxToImage_tpu(tracked_objects_with_scores, frame, label_dict, submit_threshold)
                #self._gui_sender.send_jpg(num, cv2.imencode('.jpg', frame)[1].tobytes())
                #mlUtil.add_frame_number_to_image(frame,num)
                self._data = (framecount, cv2.imencode('.jpg', frame)[1].tobytes())
                self._data_ready.set()
        except:
            traceback.print_exc()
            self.shutdown()



if __name__ == "__main__":
    freeze_support()
    if len(sys.argv) > 1:
        ff = FaceFinder(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7])
    else:
        ff = FaceFinder()
        
    while not ff.is_shutdown:
        continue
   