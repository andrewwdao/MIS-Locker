from gevent.pywsgi import WSGIServer
from app import saveInfo_app
import signal
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

class WebServer(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        global server
        server = WSGIServer(('0.0.0.0', 7497), saveInfo_app)
        server.serve_forever()


def shutdown(num, info):
    print(f'Shutting down website server...\n'
          f'{num} {info}')
    server.stop()
    server.close()


if __name__ == "__main__":
    server = None
    WebServer().start()

    signal.signal(signal.SIGINT, shutdown)