from gevent.pywsgi import WSGIServer
from app import saveInfo_app
import gevent
import threading
import signal
import os


class WebServer(threading.Thread):
    def __init__(self):
        super().__init__()
        self.pid = os.getpid()
    

    def run(self):
        self.server = gevent.pywsgi.WSGIServer(('0.0.0.0', 7497), saveInfo_app)
        gevent.signal(signal.SIGINT, self.shutdown)
        self.server.serve_forever()


    def shutdown(self):
        print(f'Shutting down website server...\n')
        self.server.stop()
        # self.server.close()
        exit(signal.SIGINT)

    # def start(self): --> existed already from parent 
