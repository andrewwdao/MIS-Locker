from gevent.pywsgi import WSGIServer
import gevent
from app import saveInfo_app #, app_pid
import threading
import signal
import os


class WebServer(threading.Thread):
    def __init__(self):
        super().__init__()
        
    def run(self):
        self.server = WSGIServer(('0.0.0.0', 80), saveInfo_app)
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

    # def start(self): --> existed already from parent 

# ref: https://stackoverflow.com/questions/18277048/gevent-pywsgi-graceful-shutdown
