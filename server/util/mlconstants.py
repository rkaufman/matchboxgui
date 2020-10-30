from util.model_type import ModelType
# Constants
# The constants remaining in this file are the


# CPU detection ------------------------------------------------------------------------------------------------------
CPU_FACE_MODEL_PATH = './libs/TensorflowFaceDetector/model/frozen_inference_graph_face.pb'
#CPU_ALPR_MODEL_PATH = './model/version2/cpu/lpr_frozen_inference_graph_dharun.pb'
CPU_ALPR_MODEL_PATH = './model/version2/cpu/lpr_frozen_inference_graph_stevefielding_2018_07_25_14-00.pb'
CPU_COCO_MODEL_PATH = './model/version2/cpu/frozen_inference_graph2.pb'
CPU_COCO_LABEL_PATH = './model/version2/coco_labels_paper.txt'
## http://download.tensorflow.org/models/object_detection/ssdlite_mobilenet_v2_coco_2018_05_09.tar.gz
CPU_LABELS_TO_DETECT = {777, 778, 1, 2, 3, 4, 5, 6, 7, 8, 47, 77} # skip any labels but these
# 777 face
# 778 plate
# 1 person
# 2 bicycle
# 3 car
# 4 motorcycle
# 5 airplane
# 6 bus
# 7 train
# 8 truck
# 47 cup # testing
# 77 cell phone # testing


# Coral detection ------------------------------------------------------------------------------------------------------
#CORAL_MODEL_PATH   = './model/mobilenet_ssd_v2_face_quant_postprocess_edgetpu.tflite'
TPU_FACE_WIN_MODEL_PATH = './model/version2/tflite/coco_ssd_mobilenet_v1_1.0_quant_2018_06_29/detect.tflite'
TPU_FACE_MODEL_PATH = './model/version2/edgetpu/mobilenet_ssd_v2_face_quant_postprocess_edgetpu.tflite'
TPU_ALPR_MODEL_PATH = 'TBD'
TPU_COCO_MODEL_PATH = './model/version2/edgetpu/mobilenet_ssd_v2_coco_quant_postprocess_edgetpu.tflite'
TPU_COCO_LABEL_PATH = './model/version2/coco_labels.txt'
TPU_LABELS_TO_DETECT = {777, 778, 0, 1, 2, 3, 4, 5, 6, 7, 9, 27, 31, 33, 46, 76} # skip any labels but these
# 777 face
# 778 plate
# 0  person
# 1  bicycle
# 2  car
# 3  motorcycle
# 4  airplane
# 5  bus
# 6  train
# 7  truck
# 9  boat
# 27 backpack
# 31 handbag
# 33 suitcase
# 46 cup # testing
# 76 cell phone # testing
# CORAL_DETECTION_THRESHOLD = 0.1
# CORAL_MAX_OBJECTS_TO_DETECT = 50

FACE_CLASS_ID = 777 # coco has classes; face only single class. It needs unique label when merged with coco detections
LPR_CLASS_ID = 778 # LPR class id

#MODELS_TO_RUN = {ModelType.face, ModelType.lpr, ModelType.coco}
#MODELS_TO_RUN = {ModelType.coco}
MODELS_TO_RUN = {ModelType.face}
#MODELS_TO_RUN = {ModelType.lpr}

MXSERVER_BASE_COLLECTION_ID = "36537"

# Web browser client
CONTINUE_RUNNING_WITHOUT_ATTACHED_CLIENT = True
CLIENT_TIMEOUT_SECONDS = 5

# Tracker; same tracker for each platform
# TRACKING_MAX_AGE = 1 # how long until we remove tracker; default=1
# TRACKING_MIN_HITS = 3 # how many hits until we start tracking object; default=3
# TRACKING_MIN_IOU = 0.6 # Min IOU (intersection over untion) to be a valid id/score pair when tracking

# Onboard camera device id. Usually zero
ONBOARD_CAMERA_DEVICE_ID = 0
# Resize image after reading from source. Affect display and detection
# Set to zero to skip resizing
# RESIZE_IMAGE_BEFORE_PREDICTION = True
# RESIZE_IMAGE_WIDTH = 800

# Face submit to MXSERVER
# MIN_FACE_SIZE = 4 # Percentage of face width to imagee width
# MAX_FACES_TO_SUBMIT_WHILE_TRACKING = 3
#### SUBMIT_ON_EXIT = True  #### This is not currently used
#### FACE_CACHE_DELETE_FACE_DELAY = 5    # Seconds from last submit to #### This is not currently used
# SHOULD_SUBMIT_FACE_SEARCHES = True
# MIN_FACE_SCORE_TO_SUBMIT = 0.1
### MIN_FACE_SCORE_TO_DISPLAY = 0.05 ####  This is not currently used
# FACE_CACHE_PROCESSING_INTERVAL = 2  # Integer seconds (3 = 3 seconds), or float (0.5 = half second)

# MXSERVER
# MX_HOST = "blackoak.mxservercloud.com"
# MX__USERNAME = "admin"
# MX_PASSWORD = "MXserver1!"
# MX_USE_TLS = True

# MX_SEARCH_PATH = "/api/face-searches"
# MX_RETAIN_IMAGE = True
# MX_MEDIA_SEARCH = True
# MX_COLLECTED_FROM = "mbDevice"
# MX_COLLECTED_LOCATION = "sb"
# MX_WATCHLISTS = ""

# Misc
# PRINT_SCORES_IDS_ON_SUBMIT_IMAGES = True

# Monitor stream to restart on connection issue
MAX_MISSED_CONSECUTIVE_FRAMES = 5
MISSED_FRAME_DELAY = 0.25


NETWORK_CONFIGURATON_FILE = "./network/network_config"
NETWORK_PRIMARY_INTERFACE_NAME = "eth0" #"en0"

# For REST API: this is where we save face images
#LOCAL_MX_MOUNT_PATH = '/Users/j2/dev/mxcloud/Shares/MXSERVER'
#LOCAL_MX_MOUNT_PATH = '/Volumes/faceFinderNFS'
LOCAL_MX_MOUNT_PATH = '/Volumes/MXSERVER'
TEMPLATE_RESPONSE_OBJECT = 'util/mxserver_objects/mx_json_response.json'
# TODO: The shape predictor is license for non-commercial use, so this
# TODO:     is for prototyping use only.
DLIB_LANDMARK_MODEL = 'model/dlib/shape_predictor_68_face_landmarks.dat'

# Error/debug logs
ERROR_LOGFILE = 'logs/error.log'

# Offline mode
OFFLINE_MODE_LOCAL_DIRECTORY = 'offlinemode'
OFFLINE_MODE_STORAGE_DIRECTORY = '/media/sd/offlinemode'


# messaging constants
HOST_IP = '127.0.0.1'
MESSAGE_HUB_PORT = 5555
CAMERA_IMAGE_SENDING_PORT = 5556
FACE_FINDER_IMAGE_SENDING_PORT = 5557
CAMERA_QUEUE = 'camera_queue'
FACE_FINDER_QUEUE = 'face_finder_queue'
