# from gevent.pywsgi import WSGIServer
from app import saveInfo_app
import gevent
import threading

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

def shutdown(num, info):
    print(f'Shutting down website server...\n'
          f'{num} {info}')
    server.stop()
    server.close()
    exit(signal.SIGINT)

class WebServer(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        global server
        server = gevent.pywsgi.WSGIServer(('0.0.0.0', 7497), saveInfo_app)
        gevent.signal(signal.SIGINT, shutdown)
        server.serve_forever()



if __name__ == "__main__":
    server = None
    WebServer().start()
