import gevent
from gevent.pywsgi import WSGIServer
from app import saveInfo_app
import threading
import signal
import os


class WebServer(threading.Thread):
    def __init__(self):
        super().__init__()
        self.pid = os.getpid()
    

    def run(self):
        self.server = gevent.pywsgi.WSGIServer(('0.0.0.0', 7497), saveInfo_app)
        gevent.signal(signal.SIGINT, self.shutdown) # SIGINT will wait for last request to be served before shutdown, SIGTERM will kill it immediately
        self.server.serve_forever()

    # ======================== for development only =====================
    # def run(self):
    #     saveInfo_app.run(host='0.0.0.0', port=7497, debug=False)  # run collecting app
    # ===================================================================

    def shutdown(self): # SIGINT or SIGTERM doesn't really matter since what shutdown server stays here
        print(f'Shutting down website server...\n')
        self.server.stop()
        self.server.close()
        # exit(signal.SIGINT)

    # def start(self): --> existed already from parent 