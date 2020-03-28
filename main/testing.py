from gevent.pywsgi import WSGIServer
from app import saveInfo_app
import gevent
import threading
import signal
import os

# server = WSGIServer(('0.0.0.0', 7497), saveInfo_app)

# def start():
#     server.serve_forever()
#     server.stop()
#     server.close()

# def shutdown(num, info):
#     print(f'Shutting down website server...\n'
#           f'{num} {info}')
#     server.stop()
#     server.close()

# def stop():
#     signal.signal(signal.SIGINT, shutdown)

class WebServer(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        global server
        self.server = gevent.pywsgi.WSGIServer(('0.0.0.0', 7497), saveInfo_app)
        gevent.signal(signal.SIGINT, self.shutdown)
        self.server.serve_forever()

    def shutdown(self):
        print(f'Shutting down website server...\n')
        self.server.stop()
        # self.server.close()
        exit(signal.SIGINT)



if __name__ == "__main__":
    # server = None
    # WebServer().start()
    server = WebServer()
    
    server.start()
    
    os.kill(int(server.ident),signal.SIGINT)
    # WebServer().stop()