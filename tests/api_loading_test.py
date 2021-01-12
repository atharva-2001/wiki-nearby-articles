import requests
import json
from multiprocessing import Barrier, Lock, Process

from time import sleep
import sys

# Spinning cursor

      
# Progress bar
# def progress_bar():
#   for i in range(100):
#     time.sleep(0.1)
#     sys.stdout.write('\r{:02d}: {}'.format(i, '#' * (i / 2)))
#     sys.stdout.flush()
#     print("coming")

# if __name__ == '__main__':
#     procs = []
#     procs.append(Process(target=get))
#     procs.append(Process(target=progress_bar))
#     map(lambda x: x.start(), procs)
#     map(lambda x: x.join(), procs)

#! /usr/bin/env python3
from multiprocessing import Barrier, Lock, Process
from time import time
from datetime import datetime
from threading import Thread
import os

def get_calls():
    S = requests.Session()
    URL = "https://en.wikipedia.org/w/api.php"

    PARAMS = {
                "action": "query",
                "format": "json",
                "titles": "Atom",
                "prop": "extracts",
                "exsentences": "4",
                "exlimit": "1",
                "explaintext": "1",
                "formatversion": "2",
                }
    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()
    sys.stdout.flush()
    print(DATA)
    os._exit(0)
    return DATA

def spinning_cursor():
  while True:
    for cursor in '\\|/-':
      sleep(0.1)
      # Use '\r' to move cursor back to line beginning
      # Or use '\b' to erase the last character
      sys.stdout.write('\r{}'.format(cursor))
      # Force Python to write data into terminal.
      sys.stdout.flush()

Thread(target=get_calls, daemon=True).start()
Thread(target=spinning_cursor).start()

# while True:
    # for cursor in '\\|/-':
    #     sleep(0.1)
    #     # Use '\r' to move cursor back to line beginning
    #     # Or use '\b' to erase the last character
    #     sys.stdout.write('\r{}'.format(cursor))
    #     # Force Python to write data into terminal.
    #     sys.stdout.flush()
# th.join()
# def main():
#     synchronizer = Barrier(2)
#     serializer = Lock()
#     Process(target=test, args=(synchronizer, serializer)).start()
#     Process(target=spinning_cursor, args=(synchronizer, serializer)).start()
    
    # Process(target=test, args=(synchronizer, serializer)).start()

# def test(synchronizer, serializer):
#     synchronizer.wait()
#     now = time()
#     with serializer:
#         S = requests.Session()
#         URL = "https://en.wikipedia.org/w/api.php"

#         PARAMS = {
#                     "action": "query",
#                     "format": "json",
#                     "titles": "Atom",
#                     "prop": "extracts",
#                     "exsentences": "4",
#                     "exlimit": "1",
#                     "explaintext": "1",
#                     "formatversion": "2",
#                     }
#         R = S.get(url=URL, params=PARAMS)
#         DATA = R.json()
#         return DATA

# if __name__ == '__main__':
#     main()
# from multiprocessing import Process, Lock

# def f(l, i):
#     l.acquire()
#     try:
#         print('hello world', i)
#     finally:
#         l.release()

# if __name__ == '__main__':
#     lock = Lock()

#     for num in range(10):
#         Process(target=f, args=(lock, num)).start()