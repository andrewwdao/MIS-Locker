from gevent.pywsgi import WSGIServer
from app import saveInfo_app
import signal

server = WSGIServer(('0.0.0.0', 7497), saveInfo_app)

def start():
    server.serve_forever()

def shutdown(num, info):
    print(f'Shutting down website server...\n'
          f'{num} {info}')
    server.stop()
    server.close()

def stop():
    signal.signal(signal.SIGINT, shutdown)