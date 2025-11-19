import logging
from logging.handlers import QueueHandler,QueueListener
from queue import Queue
import sys

log_queue = Queue()
_listener = None

def start_logging():
    global _listener
    handler = logging.StreamHandler(sys.stdout)
    fmt = "%(levelname)s: %(message)s"
    handler.setFormatter(logging.Formatter(fmt))
    _listener = QueueListener(log_queue,handler)
    _listener.start()
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    root.handlers = []
    root.addHandler(QueueHandler(log_queue))
    return _listener

def stop_logging():
    global _listener
    if _listener:
        _listener.stop()
        _listener = None