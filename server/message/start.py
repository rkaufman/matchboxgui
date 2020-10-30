from multiprocessing import Process
import os
import sys
import pathlib
main_path = pathlib.Path(__file__).parent.parent.absolute()
if main_path not in sys.path:
    sys.path.append(str(main_path))
from db import sqlitedb
from message.camera_manager import CameraSender
from message.message_hub import MessageHub
from message.face_finder import FaceFinder
import threading
from time import sleep

def start_cam():
    CameraSender()

def start_msg():
    MessageHub()

def start_ff():
    FaceFinder()

def run():
    print('starting message hub')
    msg_proc = MessageHub()
    sleep(5.0)
    print('starting camera')
    cam_proc = Process(target=start_cam, args=()).start()
    sleep(3.0)
    print('starting face finder')
    ff_proc = Process(target=start_ff, args=()).start()
    

if __name__ == '__main__':
    run()