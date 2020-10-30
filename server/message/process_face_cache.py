import threading
import datetime
import time
import faceSubmitter as FaceSubmitter
import os
import db.sqlitedb as db
from decimal import Decimal
import util.mlUtil as mlUtil
import traceback

class ProcessFaceCache(threading.Thread):
    def __init__(self, faceCache, id_score_dict_currently_tracked):
        threading.Thread.__init__(self)
        self.faceCache = faceCache
        self.id_score_dict_currently_tracked = id_score_dict_currently_tracked
        self._stop_event = threading.Event()
        self._pause = False

    def submitSearch(self, face, should_delete_after_submit = False):

        print('++++++++++++ submit search 0000', face)

        # Test if we've submitted too many faces for track
        if face.submit_count >= int(db.get_setting('max-faces-to-submit-while-tracking').setting):
            print('++++++++++++ submit search 1111')
            thread_lock = threading.Lock()
            with thread_lock:
                print("SUBMIT LOGIC max-faces-to-submit: DELETE(): ", face.id)
                self.faceCache.delete(face.id)
            return

        if not mlUtil.to_bool(db.get_setting('should-submit-face-searches').setting):
            return

        if face.score < Decimal(db.get_setting('min-face-qual-score').setting)/10:
            print('score to low')
            return

        # Test min face size
        #   If too small remove. This ID could get added again (and may or may not be too small at that point)
        (x1, y1, x2, y2) = face.box
        faceWidth = y2 - y1 # This is percentage as coords are relative
        faceWitchAsPercentage = faceWidth * 100
        if faceWitchAsPercentage < int(db.get_setting('min-face-size').setting):
            thread_lock = threading.Lock()
            with thread_lock:
                self.faceCache.delete(face.id)
            return

        

        print('++++++++++++ submit search 2222')
        faceSubmitter = FaceSubmitter.FaceSubmitter(face)
        print('++++++++++++ submit search 3333')
        faceSubmitter.daemon = True
        faceSubmitter.setDaemon(True)
        faceSubmitter.start()

    def pause(self):
        self._pause = True
        self._pausing()

    def stop(self):
        self._stop_event.set()

    def clear(self):
        thread_lock = threading.Lock()
        with thread_lock:
            self.faceCache.dict.clear()

    def stopped(self):
        return self._stop_event.is_set()

    def _pausing(self):
        while self._pause:
            time.sleep(10.0)

    def run(self):
        try:
            while not self._pause and not self._stop_event.isSet():

                print("****************** PROCESS FACE CACHE ****************** ", os.getpid())
                print("******************************************************** ")

                if not mlUtil.to_bool(db.get_setting('should-submit-face-searches').setting):
                    print("Not submitting face searches. Turn this on in settings")

                for id,face in list(self.faceCache.dict.items()):
                    print("Face cache ID -----> : ", id)

                    # Test if this we've lost tracking: In this case delete
                    currently_tracked = self.id_score_dict_currently_tracked[face.id]
                    if currently_tracked is None:
                        # Face no longer tracked: submit(). Future: wait one second to make sure track doesn't resume, or?
                        self.submitSearch(face, should_delete_after_submit=True)
                        thread_lock = threading.Lock()
                        with thread_lock:
                            now = datetime.datetime.now()
                            face.lastsubmit = now
                            face.lastseen = now
                            face.submit_count += 1

                            if should_delete_after_submit:
                                self.faceCache.delete(id)
                    else:
                        # tracking
                        self.submitSearch(face)
                print("\n\n\n")
                print("******************************************************** ")
                print("****************** PROCESS FACE CACHE ****************** ", os.getpid())

                face_cache_processing_interval = Decimal(db.get_setting('face-cache-processing-interval').setting)
                time.sleep(face_cache_processing_interval)
        except:
            traceback.print_exc()
