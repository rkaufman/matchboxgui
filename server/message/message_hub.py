import pathlib
main_path = pathlib.Path(__file__).parent.parent.absolute()
import sys
if main_path not in sys.path:
    sys.path.append(str(main_path))
import threading
from message.queue_manager import QueueManager
from multiprocessing import Queue, freeze_support
from util import mlconstants
import traceback

class MessageHub(threading.Thread):
    def __init__(self, host = None, port = None, authkey = None):
        threading.Thread.__init__(self, target=self._run, args=())
        if host is None:
            self._host = mlconstants.HOST_IP
        else:
            self._host = host
        if port is None:
            self._port = mlconstants.MESSAGE_HUB_PORT
        else:
            self._port = port
        if authkey is None:
            self._authkey = 'abc'
        else:
            self._authkey = authkey
        self._server = None
        self._mgr = None
        self.start()

    def _run(self):
        try:
            print('Starting message hub')
            face_finder_queue = Queue()
            cam_queue = Queue()
            process_face_cache_queue = Queue()
            QueueManager.register('face_finder_queue', callable=lambda:face_finder_queue)
            QueueManager.register('camera_queue', callable=lambda:cam_queue)
            QueueManager.register('process_face_cache_queue', callable=lambda:process_face_cache_queue)
            self._mgr = QueueManager(address=(self._host,int(self._port)), authkey=self._authkey.encode('utf-8'))
            self._server = self._mgr.get_server()
            self._server.serve_forever()
        except Exception as ex:
            print(ex)
            traceback.print_exc()
        finally:
            print('Stopped message hub')
    def stop(self):
        """Sets the stop event on the BaseManager to stop the message server"""
        print('Stopping message server.')
        self._server.stop_event.set()

if __name__ == "__main__":
    freeze_support()
    try:
        if len(sys.argv) > 1:
            hub = MessageHub(sys.argv[1], sys.argv[2], sys.argv[3])
        else:
            hub = MessageHub()
    except (KeyboardInterrupt, SystemExit):
        hub.stop()

