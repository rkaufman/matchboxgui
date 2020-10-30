from queue import Queue
import datetime


class ProcessingQueueItem(object):
    def __init__(self, id, assets):
        self.id = id
        self.timestamp = datetime.datetime.now()
        self.assets = assets


class ProcessingQueue(object):
    """
    A queue for managing REST API processing requests.
    This is meant to handle multiple incoming client requests where only one request can be handled at a time
    but multiple threads are waiting for their turn to be able to process the request.
    An incoming request is queued and the process that put the item on the queue waits until it's item
    is released from the queue, using getNext(id).

    A process that wants to process a request and have the next item in the queue wait until
    the process is FINISHED should:
        1. Verify that the specified request ID is in the front of the queue
        2. Access the item with peek() to keep it in front of the line, so another process won't also process
        3. Pop the item with getNext() once processing is complete
    """

    def __init__(self):
        self.q = Queue()

    def put(self, item):
        self.q.put(item)

    """
    Access first item on queue, without popping it.
    """
    def peek(self):
        items = list(self.q.queue)
        return items[0]


    def getNext(self, request_id):
        """
        Pop item from the queue, only if it's my item (as identified by ID).
        This allows multiple threads to work while only processing one item concurrently.
        """
        items =  list(self.q.queue)

        if not items:
            return None

        # Only return item if it's the item belonging to requester.
        if items[0].id is request_id:
            return self.q.get()
        else:
            return None

    def get_position(self, request_id):
        """
        Returns position in queue, 1 for first in line. 0 for not exist
        """
        items = list(self.q.queue)
        ids = [i.id for i in items]
        try:
            index = ids.index(request_id)
            return index + 1
        except ValueError:
            return 0

    def size(self):
        return self.q.qsize()

    def exists(self, request_id):
        """
        Determine if ID is in queue.
        Return True if item is in queue.
        """

        items = list(self.q.queue)
        if not items:
            return False

        ids = [i.id for i in items]
        if not ids:
            return False

        if request_id in ids:
            return True
        else:
            return False

    def list(self, request_id):
        print("LIST ======================================", request_id)
        for item in list(self.q.queue):
            if item.id is request_id:
                print("LIST: ", item.id, " --> ", item.assets)
            else:
                print("LIST: not here for ", request_id)

    def list(self):
        print("LIST ====================================== ALL")
        for item in list(self.q.queue):
            print("LIST: ", item.id, " --> ", item.assets)
