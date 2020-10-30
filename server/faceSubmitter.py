import cv2
import requests
import threading
import urllib3
from PIL import Image
import util.mlUtil as mlUtil
from util.mx_auth import MxAuth as mx
from collections import namedtuple
from status import Status
from status_type import StatusType
from requests_toolbelt import MultipartEncoder
from util.classification_category import ClassificationCategory
import util.mlconstants as mlconstants
import os
from pathlib import Path
from random import randrange
from datetime import datetime
import json
import db.db as db


class FaceSubmitter(threading.Thread):
    def __init__(self, faceItem):
        threading.Thread.__init__(self)
        self.faceItem = faceItem


    def run(self):
        # [h, w] = self.faceItem.frame.shape[:2]
        (x1, y1, x2, y2) = self.faceItem.box
        face_cropped = self.faceItem.frame[int(y1):int(y2), int(x1):int(x2)]

        print_scores_ids_on_submit_images = mlUtil.to_bool(sqlitedb.get_setting('print-scores-ids-on-submit-images').setting)

        if print_scores_ids_on_submit_images is True:
            score_str = "{0:.4f}".format(self.faceItem.score)
            msg = str(int(self.faceItem.id)) + ": " + score_str
            cv2.putText(face_cropped, msg, (2, 16), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2)

        # TODO: this error was noted: Image.fromarray(face_cropped) --> ValueError: tile cannot extend outside image
        # TODO:     when face_cropped == 0. Determine what cases make it zero. Possibly face partially out of frame.
        if face_cropped.size == 0:
            return

        mx_retain_image = sqlitedb.get_setting('mx-retain-image').setting
        mx_media_search = sqlitedb.get_setting('mx-media-search').setting
        mx_collected_from = sqlitedb.get_setting('mx-collected-from').setting
        mx_collected_location = sqlitedb.get_setting('mx-collected-location').setting
        mx_watchlists = sqlitedb.get_setting('mx-watchlists').setting
        mx_search_path = sqlitedb.get_setting('mx-search-path').setting

        # Offline mode <start> =====================================================================================
        offline_mode = mlUtil.to_bool(db.get_setting('mx-use-offlinemode').setting)
        if offline_mode:
            offline_mode = mlUtil.to_bool(db.get_setting('mx-use-offlinemode').setting)

            if offline_mode:
                # Set directory to save images. First try the permanent storage directory (SD card)
                #    If that doesn't exist use directory located at the same level as the MatchboxEdge directory.
                #    This approach should automatically work for dev workstations.
                # TODO: do we need to handle full disk scenario? Add to new status screen, via sql log msg.
                # Permanent storage
                if os.path.exists(mlconstants.OFFLINE_MODE_STORAGE_DIRECTORY):
                    offline_dir = mlconstants.OFFLINE_MODE_STORAGE_DIRECTORY
                else:
                    # Set to OFFLINE_MODE_LOCAL_DIRECTORY which is next to MatchboxEdge dir
                    offline_dir = os.path.join(Path.cwd().resolve().parent, mlconstants.OFFLINE_MODE_LOCAL_DIRECTORY)
                    # Create directory if it doesn't exist
                    if not os.path.exists(offline_dir):
                        os.makedirs(offline_dir)

                if not Path(offline_dir).exists():
                    print("The offlne directory doesn't exist: ", offline_dir)
                    ## TODO - this is a failure condition. Can't save any files. Add to new status UI when integrated
                else:
                    face_cropped_corrected = cv2.cvtColor(face_cropped, cv2.COLOR_BGR2RGB)
                    save_image = Image.fromarray(face_cropped_corrected)

                    random_string = str(randrange(9999)).zfill(4) # random number padded to 4 digits with zeros
                    local_time_string = datetime.today().strftime('%Y%m%d_%H-%M-%S')
                    local_time_string_for_file = datetime.today().strftime('%Y-%m-%d-%H-%M-%S')
                    utc_time_string_for_file = datetime.utcnow().strftime('%Y-%m-%d-%H-%M-%S')

                    image_filename = "face_" + local_time_string + "_" + random_string + ".png"
                    image_filepath = os.path.join(offline_dir, image_filename)
                    save_image.save(image_filepath)

                    metadata = {}
                    metadata['object'] = "face"
                    metadata['image_filename'] = image_filename
                    metadata['retain_image'] = mx_retain_image
                    metadata['media_search'] = mx_media_search
                    metadata['retain_image'] = mx_retain_image
                    metadata['collected_from'] = mx_collected_from
                    metadata['collected_location'] = mx_collected_location
                    metadata['watchlists'] = mx_watchlists.replace(" ", "")
                    metadata['local_time'] = local_time_string_for_file
                    metadata['utc_time'] = utc_time_string_for_file
                    json_data = json.dumps(metadata)

                    metadata_filename = "face_" + local_time_string + "_" + random_string + ".json"
                    metadata_filepath = os.path.join(offline_dir, metadata_filename)
                    with open(metadata_filepath, 'w') as file:
                        file.write(json_data)
        # Offline mode <end> =======================================================================================

        # Bail out if user has selected to not submit faces
        # We had this over in processFaceCache, but moved to here
        #  so we always come here so we can save via offline mode if needed, and
        #  and we're already on another thread.
        if not mlUtil.to_bool(db.get_setting('should-submit-face-searches').setting):
            return

        (success, hdrs, cookies, cookieList, authLabel, authToken) = mx.login()

        mx_use_tls = mlUtil.to_bool(sqlitedb.get_setting('mx-use-tls').setting)
        protocol = "https://" if mx_use_tls else "http://"
        mx_host = sqlitedb.get_setting('mx-host').setting

        print('FaceSubmitter -----------------------------------------')
        if success is not True:
            msg = "Unable to login to server for submission: " + mx_host
            print(msg)
            sqlitedb.add_log(msg)
            return

        if self.faceItem.class_id == ClassificationCategory.face.value:

            query_string = "?RetainImage=" + mx_retain_image + \
                           "&MediaSearch=" + mx_media_search + \
                           "&CollectedFrom=" + mx_collected_from + \
                           "&CollectedLocation=" + mx_collected_location + \
                           "&FileName=test.png" + \
                           "&Watchlists=" + mx_watchlists.replace(" ", "")
            submit_url = protocol + mx_host + mx_search_path + query_string

            print("query_string: ", query_string)

            content_type = 'image/jpeg'
            headers = {'content-type': content_type}
            cookies = {authLabel: authToken}

            # encode image as jpeg
            _, img_encoded = cv2.imencode('.jpg', face_cropped)

            success = False
            try:
                response = requests.post(submit_url, data=img_encoded.tostring(), headers=headers, cookies=cookies, verify=False, timeout=15)
                response.raise_for_status()
                success = True
            except requests.exceptions.HTTPError as errh:
                print("Http Error:", errh)
            except requests.exceptions.ConnectionError as errc:
                print("Error Connecting:", errc)
            except requests.exceptions.Timeout as errt:
                print("Timeout Error:", errt)
            except requests.exceptions.RequestException as err:
                print("Other login error:", err)
            except urllib3.exceptions.NewConnectionError as errnc:
                print("Could not connect to MXSERVER instance at: {}".format(mx_host))

            if success:
                sqlitedb.update_status(Status(StatusType.SEARCH, True, ''))

                print(response.text) # This has search ID
                print("Status Code: ", response.status_code) # "201" on success
                print("Reason: ", response.reason) # "Created" on success

                response_object = json.loads(response.text, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
                msg = "Face submit status: " + response_object.message
                if response_object.id is not None:
                    msg = msg + "Search ID: " + str(response_object.id)

                sqlitedb.add_log(msg)
                print(msg)

        else:
            # submit object as generic object (non-face)

            mx_search_path = "/api/asset/mediaupload"
            submit_url = protocol + mx_host + mx_search_path

            _, img_encoded = cv2.imencode('.jpg', face_cropped)

            class_name = 'unknown'
            try:
                class_name = ClassificationCategory(self.faceItem.class_id).name
            except ValueError:
                print("No classification category for object found: ", self.faceItem.class_id)

            meta = {"object_class": class_name, "subtype": "none"}

            collection_id = mlconstants.MXSERVER_BASE_COLLECTION_ID # '36537'

            success = False
            try:
                cookies = {authLabel: authToken}
                data = MultipartEncoder(
                    fields = {
                        'label': 'Vehicle',
                        'metadata': (None, str(meta), 'application/json; charset=UTF-8'),
                        'ParentAssetID': collection_id,
                        'file':  ('.jpg', img_encoded.tostring(), 'image/jpeg'),
                        'addedmetadata' : 'true'
                    }
                )
                response = requests.post(submit_url, data=data, headers={'Content-Type': data.content_type}, cookies=cookies, verify=False, timeout=15)

                # print("*** SUBMITING response   ----------------------------------------------------------------------")
                # print(response.text)  # This has search ID
                # print("Status Code: ", response.status_code)  # "201" on success
                # print("Reason: ", response.reason)  # "Created" on success
                # print("*** SUBMITING response   ----------------------------------------------------------------------")

                response.raise_for_status()
                success = True

            except requests.exceptions.HTTPError as errh:
                print("Http Error:", errh)
            except requests.exceptions.ConnectionError as errc:
                print("Error Connecting:", errc)
            except requests.exceptions.Timeout as errt:
                print("Timeout Error:", errt)
            except requests.exceptions.RequestException as err:
                print("Other login error:", err)
            except urllib3.exceptions.NewConnectionError as errnc:
                print("Could not connect to MXSERVER instance at: {}".format(mx_host))

            if success:
                sqlitedb.update_status(Status(StatusType.SEARCH, True, ''))
                msg = "Asset uploaded, for object type: " + class_name
                sqlitedb.add_log(msg)
                print(msg)
