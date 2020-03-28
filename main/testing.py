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
        self.pid = os.getpid()
    
    # def pid(self):
        # return self.pid

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


# class WebServer():
#     def __init__(self):
#         self.server = gevent.pywsgi.WSGIServer(('0.0.0.0', 7497), saveInfo_app)
#         gevent.signal(signal.SIGINT, self.shutdown)

#     def stop(self):
#         print(f'Shutting down website server...\n')
#         self.server.stop()

#     def run(self):
#         self.server.serve_forever()

#     def shutdown(self):
#         print(f'Shutting down website server...\n')
#         self.server.stop()
#         # self.server.close()
#         exit(signal.SIGINT)


if __name__ == "__main__":
    # server = None
    # WebServer().start()
    server = WebServer()
    
    server.start()
    
    print(server.pid)

    # server.stop()
    os.kill(int(server.pid),signal.SIGINT)
    # WebServer().stop()