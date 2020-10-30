import pathlib
main_path = pathlib.Path(__file__).parent.parent.absolute()
import sys
if main_path not in sys.path:
    sys.path.append(str(main_path))
import threading
import queue
import imagezmq
import traceback
from imagezmq import zmq
from db import sqlitedb

class VideoStreamSubscriber:
    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port
        self._started = False
        self._stop = False
        self._receiver = None
        self._data = None
        self._data_ready = threading.Event()
        self._thread = threading.Thread(target=self._run, args=())
        self._thread.daemon = True
        self._thread.start()

    def receive(self, timeout=15.0):
        flag = self._data_ready.wait(timeout=timeout)
        if not flag:
            print("Timeout while reading from subscriber tcp://{}:{}".format(self.hostname, self.port))
            return None
        self._data_ready.clear()
        return self._data
    def _run(self):
        if not self._stop and self._started:
            return
        if self._receiver is None:
            try:
                self._receiver = imagezmq.ImageHub("tcp://{}:{}".format(self.hostname, self.port), REQ_REP = False)
            except zmq.ZMQError as er:
                print(er)
                traceback.print_exc()
                return
        self._started = True
        try:
            while not self._stop:
                self._data = self._receiver.recv_jpg()
                #telemetry remove me
                #sqlitedb.rec_frame(self._data[0])
                self._data_ready.set()
        finally:
            self._receiver.close()

    def close(self):
        self._stop = True
if __name__ == "__main__":
     try:
         vss = VideoStreamSubscriber(sys.argv[1], sys.argv[2])
     except:
         traceback.print_exc()

