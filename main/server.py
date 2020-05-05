from gevent.pywsgi import WSGIServer
import gevent
from app import saveInfo_app #, app_pid
from app.save_info.routes import app_pid
import threading
import signal
import os


class WebServer(threading.Thread):
    def __init__(self):
        super().__init__()
        # super(WebServer, self).__init__(*args, **kwargs)
        # self._stop_event = threading.Event()
        # self.pid = app_pid
        # self.ON_FLAG = True
        
    def run(self):
        # self.ON_FLAG = True
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
        # self.ON_FLAG = False
        # raise ValueError("Hello")
    
    def get_my_tid(self):
        """determines this (self's) thread id

        CAREFUL : this function is executed in the context of the caller
        thread, to get the identity of the thread represented by this
        instance.
        """
        if not self.isAlive():
            raise threading.ThreadError("the thread is not active")

        # do we have it cached?
        # if hasattr(self, "_thread_id"):
        #     return self._thread_id

        # no, look for it in the _active dict
        for tid, tobj in threading._active.items():
            if tobj is self:
                self._thread_id = tid
                return tid

        # TODO: in python 2.6, there's a simpler way to do : self.ident

        raise AssertionError("could not determine the thread's id")

        

    # def start(self): --> existed already from parent 

# ref: https://stackoverflow.com/questions/18277048/gevent-pywsgi-graceful-shutdown
