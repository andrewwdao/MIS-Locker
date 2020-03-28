from gevent.pywsgi import WSGIServer
from gevent.event import Event
from app import saveInfo_app

stopper = Event()

http_server = WSGIServer(('0.0.0.0', 7497), saveInfo_app)
http_server.start()
stopper.wait()