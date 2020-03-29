from gevent.pywsgi import WSGIServer
import gevent
from app import saveInfo_app
import threading
import signal
import os


class WebServer(threading.Thread):
    def __init__(self):
        super().__init__()
        self.pid = os.getpid()
        
    def run(self):
        self.server = WSGIServer(('0.0.0.0', 7497), saveInfo_app)
        self.gevent_signal = gevent.hub.signal(signal.SIGTERM, self.shutdown)
        self.server.serve_forever()

    # ======================== for development only =====================
    # def run(self):
    #     saveInfo_app.run(host='0.0.0.0', port=7497, debug=False)  # run collecting app
    # ===================================================================

    def shutdown(self): # SIGINT or SIGTERM doesn't really matter since what shutdown server stays here
        print(f'Shutting down server...\n')
        self.server.stop()
        self.server.close()
        self.gevent_signal.cancel()
        # raise SystemExit
        # exit(signal.SIGINT)

    # def start(self): --> existed already from parent 
